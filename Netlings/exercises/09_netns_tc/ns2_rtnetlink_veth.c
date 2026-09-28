// EXERCISE: ns2_rtnetlink_veth — 手写 `ip link add type veth`：用裸 rtnetlink 建 veth、跨 netns 搬网卡、配地址
// TOPIC: NETLINK_ROUTE / RTM_NEWLINK·RTM_NEWADDR / 嵌套 rtattr / IFLA_NET_NS_PID / NLMSG_ERROR ACK
// DIFFICULTY: ★★★★☆
// BOOK: man 7 netlink；man 7 rtnetlink；man 4 veth；RFC 3549；iproute2 源码 ip/iplink.c、lib/libnetlink.c
// I AM NOT DONE
//
// 说明：
//   用法：ns2_rtnetlink_veth
//   全程 rootless：和 ns1 一样先进入自己的 user+net namespace（脚手架已写好），然后：
//     1. fork 一个子进程，子进程再 unshare(CLONE_NEWNET) —— 现在有两个 netns："父" 和 "子"。
//     2. 父进程用 RTM_NEWLINK 创建 veth 对 sl0 <-> sl1，并在 peer 的属性里带上
//        IFLA_NET_NS_PID=<子进程 pid>，让 sl1 在创建时就出现在子进程的 netns 里。
//        消息结构（嵌套属性，这正是 netlink 难写的地方）：
//          nlmsghdr | ifinfomsg | IFLA_IFNAME "sl0"
//                             | IFLA_LINKINFO { IFLA_INFO_KIND "veth"
//                                               IFLA_INFO_DATA { VETH_INFO_PEER { ifinfomsg
//                                                                                 IFLA_IFNAME "sl1"
//                                                                                 IFLA_NET_NS_PID u32 } } }
//        注意 VETH_INFO_PEER 的负载先是一个裸的 struct ifinfomsg，后面才跟属性。
//     3. 两边各自用 RTM_NEWADDR（IFA_LOCAL + IFA_ADDRESS）配地址：10.99.0.1/24 与 10.99.0.2/24，
//        再用 RTM_NEWLINK（ifi_flags = ifi_change = IFF_UP）把网卡 up 起来。
//     4. 父进程向 10.99.0.2 发一个 UDP 数据报，子进程回显；父进程收到后打印 "udp over veth ok"。
//
//   脚手架已提供：nl_open、属性追加 nla_put/nla_put_raw、嵌套 nla_nest_start/nla_nest_end、
//   nl_talk（发送请求 + 等待 NLMSG_ERROR 形式的 ACK，error!=0 时转成 errno）。
//   你要写的是三条消息的内容：nl_create_veth、nl_add_ipv4、nl_link_up。
//
//   为什么重要：这就是 `ip link add ... type veth peer ... netns ...`、Docker libnetwork、
//   Kubernetes CNI 的 bridge/ptp/veth 插件、systemd-networkd、NetworkManager 在底层做的事。
//   Go 的 vishvananda/netlink、Rust 的 rtnetlink crate 也只是把这些 TLV 包装了一下。
//
//   探针：运行程序，要求 exit 0 且输出 "udp over veth ok"（数据报真的穿过了你建的 veth）。
//   若系统禁用非特权 user namespace，程序打印 "userns unavailable" 并 exit 3，探针 skip。

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <linux/if_link.h>
#include <linux/netlink.h>
#include <linux/rtnetlink.h>
#include <linux/veth.h>
#include <net/if.h>
#include <netinet/in.h>
#include <poll.h>
#include <sched.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>

#include "sl.h"

enum { UDP_PORT = 7777, PREFIX = 24 };
static const char PARENT_IP[] = "10.99.0.1";
static const char CHILD_IP[] = "10.99.0.2";

// ---------------------------------------------------------------------------------------------
// 脚手架：user namespace（与 ns1 相同）
// ---------------------------------------------------------------------------------------------
static int write_file(const char *path, const char *text) {
    int fd = open(path, O_WRONLY | O_CLOEXEC);
    if (fd < 0)
        return -1;
    size_t len = strlen(text);
    ssize_t w = write(fd, text, len);
    int saved = errno;
    close(fd);
    if (w != (ssize_t)len) {
        errno = w < 0 ? saved : EIO;
        return -1;
    }
    return 0;
}

static int enter_private_netns(void) {
    uid_t uid = getuid();
    gid_t gid = getgid();
    if (unshare(CLONE_NEWUSER | CLONE_NEWNET) < 0)
        return -1;
    if (write_file("/proc/self/setgroups", "deny") < 0 && errno != ENOENT)
        return -1;
    char map[64];
    snprintf(map, sizeof map, "0 %u 1\n", (unsigned)uid);
    if (write_file("/proc/self/uid_map", map) < 0)
        return -1;
    snprintf(map, sizeof map, "0 %u 1\n", (unsigned)gid);
    return write_file("/proc/self/gid_map", map);
}

// ---------------------------------------------------------------------------------------------
// 脚手架：netlink 消息构造与收发
// ---------------------------------------------------------------------------------------------
enum { NL_BUFSZ = 4096 };

// 一条正在构造的请求：buf 里放 nlmsghdr + 固定头 + 属性，nh->nlmsg_len 始终是当前总长度。
typedef struct {
    alignas(struct nlmsghdr) char buf[NL_BUFSZ];
} nlreq;

// 初始化请求：写好 nlmsghdr（type/flags），并在其后预留 fixed_len 字节的固定头（清零）。
// 返回固定头的指针（struct ifinfomsg * 或 struct ifaddrmsg *）。
[[maybe_unused]] static void *nl_init(nlreq *r, uint16_t type, uint16_t flags, size_t fixed_len) {
    memset(r->buf, 0, sizeof r->buf);
    struct nlmsghdr *nh = (struct nlmsghdr *)r->buf;
    nh->nlmsg_len = (uint32_t)NLMSG_LENGTH(fixed_len);
    nh->nlmsg_type = type;
    nh->nlmsg_flags = (uint16_t)(NLM_F_REQUEST | NLM_F_ACK | flags);
    return NLMSG_DATA(nh);
}

static struct nlmsghdr *nl_hdr(nlreq *r) { return (struct nlmsghdr *)r->buf; }

// 在消息尾部追加一个属性 (type, data[len])，自动按 RTA_ALIGN 补齐。返回该属性的指针。
static struct rtattr *nla_put(nlreq *r, uint16_t type, const void *data, size_t len) {
    struct nlmsghdr *nh = nl_hdr(r);
    size_t off = NLMSG_ALIGN(nh->nlmsg_len);
    size_t need = RTA_LENGTH(len);
    if (off + RTA_ALIGN(need) > sizeof r->buf) {
        fprintf(stderr, "netlink request too large\n");
        exit(1);
    }
    struct rtattr *rta = (struct rtattr *)(r->buf + off);
    rta->rta_type = type;
    rta->rta_len = (uint16_t)need;
    if (len)
        memcpy(RTA_DATA(rta), data, len);
    nh->nlmsg_len = (uint32_t)(off + RTA_ALIGN(need));
    return rta;
}

[[maybe_unused]] static struct rtattr *nla_put_str(nlreq *r, uint16_t type, const char *s) {
    return nla_put(r, type, s, strlen(s) + 1); // 字符串属性包含结尾的 '\0'
}

[[maybe_unused]] static struct rtattr *nla_put_u32(nlreq *r, uint16_t type, uint32_t v) {
    return nla_put(r, type, &v, sizeof v);
}

// 追加一段不带属性头的裸数据（例如 VETH_INFO_PEER 里的 struct ifinfomsg）。返回其指针。
[[maybe_unused]] static void *nla_put_raw(nlreq *r, size_t len) {
    struct nlmsghdr *nh = nl_hdr(r);
    size_t off = NLMSG_ALIGN(nh->nlmsg_len);
    if (off + NLMSG_ALIGN(len) > sizeof r->buf) {
        fprintf(stderr, "netlink request too large\n");
        exit(1);
    }
    nh->nlmsg_len = (uint32_t)(off + NLMSG_ALIGN(len));
    return r->buf + off; // nl_init 已经清零
}

// 嵌套属性：先放一个空的属性头，写完子属性后用 nla_nest_end 回填长度。
[[maybe_unused]] static struct rtattr *nla_nest_start(nlreq *r, uint16_t type) { return nla_put(r, type, nullptr, 0); }

[[maybe_unused]] static void nla_nest_end(nlreq *r, struct rtattr *nest) {
    nest->rta_len = (uint16_t)(r->buf + nl_hdr(r)->nlmsg_len - (char *)nest);
}

static int nl_open(void) {
    int fd = socket(AF_NETLINK, SOCK_RAW | SOCK_CLOEXEC, NETLINK_ROUTE);
    if (fd < 0)
        return -1;
    struct sockaddr_nl sa = {.nl_family = AF_NETLINK};
    if (bind(fd, (struct sockaddr *)&sa, sizeof sa) < 0) {
        int saved = errno;
        close(fd);
        errno = saved;
        return -1;
    }
    return fd;
}

// 发送请求并等待内核的 ACK。内核用 NLMSG_ERROR 消息回答：error == 0 表示成功（这就是 ACK），
// error < 0 是负的 errno。成功返回 0；失败返回 -1 并设置 errno。
[[maybe_unused]] static int nl_talk(int fd, nlreq *r) {
    static uint32_t seq = 1;
    struct nlmsghdr *nh = nl_hdr(r);
    nh->nlmsg_seq = seq++;
    struct sockaddr_nl kernel = {.nl_family = AF_NETLINK}; // nl_pid = 0 → 内核
    if (sendto(fd, nh, nh->nlmsg_len, 0, (struct sockaddr *)&kernel, sizeof kernel) < 0)
        return -1;
    alignas(struct nlmsghdr) char buf[8192];
    for (;;) {
        ssize_t n = recv(fd, buf, sizeof buf, 0);
        if (n < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        size_t len = (size_t)n;
        for (struct nlmsghdr *m = (struct nlmsghdr *)buf; NLMSG_OK(m, len); m = NLMSG_NEXT(m, len)) {
            if (m->nlmsg_seq != nh->nlmsg_seq)
                continue;
            if (m->nlmsg_type == NLMSG_ERROR) {
                const struct nlmsgerr *e = NLMSG_DATA(m);
                if (e->error == 0)
                    return 0;
                errno = -e->error;
                return -1;
            }
        }
    }
}

// ---------------------------------------------------------------------------------------------
// 练习：三条 rtnetlink 消息
// ---------------------------------------------------------------------------------------------

// 创建 veth 对 name <-> peer，peer 直接放进进程 peer_pid 所在的 netns。
static int nl_create_veth(int fd, const char *name, const char *peer, pid_t peer_pid) {
    // TODO: 按文件头的结构图构造 RTM_NEWLINK 请求（flags: NLM_F_CREATE | NLM_F_EXCL）：
    //   nlreq r; struct ifinfomsg *ifi = nl_init(&r, RTM_NEWLINK, ..., sizeof *ifi);
    //   IFLA_IFNAME=name；嵌套 IFLA_LINKINFO { IFLA_INFO_KIND "veth", IFLA_INFO_DATA { VETH_INFO_PEER {
    //   先 nla_put_raw 一个 struct ifinfomsg，再 IFLA_IFNAME=peer、IFLA_NET_NS_PID=peer_pid } } }
    //   每个 nla_nest_start 都要有对应的 nla_nest_end（由内向外）；最后 return nl_talk(fd, &r)。
    (void)fd, (void)name, (void)peer, (void)peer_pid;
    errno = ENOSYS;
    return -1;
}

// 给 ifindex 加 IPv4 地址 ip/prefix（`ip addr add ip/prefix dev X`）。
static int nl_add_ipv4(int fd, int ifindex, const char *ip, int prefix) {
    // TODO: inet_pton 解析 ip；RTM_NEWADDR（NLM_F_CREATE | NLM_F_EXCL），固定头是 struct ifaddrmsg：
    //   ifa_family=AF_INET, ifa_prefixlen=prefix, ifa_scope=RT_SCOPE_UNIVERSE, ifa_index=ifindex；
    //   属性 IFA_LOCAL 和 IFA_ADDRESS 都是 4 字节的 struct in_addr。
    (void)fd, (void)ifindex, (void)ip, (void)prefix;
    errno = ENOSYS;
    return -1;
}

// 把 ifindex 置为 UP（`ip link set X up`）。
static int nl_link_up(int fd, int ifindex) {
    // TODO: RTM_NEWLINK（不需要 CREATE），struct ifinfomsg 里 ifi_index=ifindex，
    //   ifi_flags=IFF_UP，ifi_change=IFF_UP（ifi_change 是"要修改哪些位"的掩码）。
    (void)fd, (void)ifindex;
    errno = ENOSYS;
    return -1;
}

// ---------------------------------------------------------------------------------------------
// 脚手架：两端的配置与 UDP 往返
// ---------------------------------------------------------------------------------------------
static void configure(const char *who, const char *ifname, const char *ip) {
    int nl = nl_open();
    if (nl < 0)
        sl_die("socket(NETLINK_ROUTE)");
    unsigned idx = if_nametoindex(ifname);
    if (idx == 0) {
        fprintf(stderr, "%s: 接口 %s 不存在（veth 没建出来 / 没搬到这个 netns？）\n", who, ifname);
        exit(1);
    }
    if (nl_add_ipv4(nl, (int)idx, ip, PREFIX) < 0)
        sl_die("RTM_NEWADDR");
    if (nl_link_up(nl, (int)idx) < 0)
        sl_die("RTM_NEWLINK (IFF_UP)");
    close(nl);
    printf("%s: %s %s/%d up\n", who, ifname, ip, PREFIX);
}

static void xwrite1(int fd, char c) {
    if (write(fd, &c, 1) != 1)
        sl_die("pipe write");
}

static bool xread1(int fd, char expect) {
    char c;
    ssize_t n;
    do {
        n = read(fd, &c, 1);
    } while (n < 0 && errno == EINTR);
    return n == 1 && c == expect;
}

static struct sockaddr_in sin_of(const char *ip) {
    struct sockaddr_in sa = {.sin_family = AF_INET, .sin_port = htons(UDP_PORT)};
    if (inet_pton(AF_INET, ip, &sa.sin_addr) != 1) {
        fprintf(stderr, "bad ip %s\n", ip);
        exit(1);
    }
    return sa;
}

[[noreturn]] static void child(int to_parent, int from_parent) {
    if (unshare(CLONE_NEWNET) < 0)
        sl_die("child unshare(CLONE_NEWNET)");
    xwrite1(to_parent, 'n'); // 我的 netns 已就绪，可以把 peer 搬进来了
    if (!xread1(from_parent, 'g'))
        _exit(1); // 父进程出错退出了
    configure("child", "sl1", CHILD_IP);

    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    struct sockaddr_in me = sin_of(CHILD_IP);
    if (bind(fd, (struct sockaddr *)&me, sizeof me) < 0)
        sl_die("child bind");
    xwrite1(to_parent, 'b');

    struct pollfd pfd = {.fd = fd, .events = POLLIN};
    if (poll(&pfd, 1, 15000) != 1) {
        fprintf(stderr, "child: 15s 内没收到数据报\n");
        _exit(1);
    }
    char buf[256];
    struct sockaddr_in from;
    socklen_t flen = sizeof from;
    ssize_t n = recvfrom(fd, buf, sizeof buf - 1, 0, (struct sockaddr *)&from, &flen);
    if (n < 0)
        sl_die("child recvfrom");
    buf[n] = '\0';
    char reply[300];
    int rn = snprintf(reply, sizeof reply, "echo:%s", buf);
    if (sendto(fd, reply, (size_t)rn, 0, (struct sockaddr *)&from, flen) < 0)
        sl_die("child sendto");
    close(fd);
    _exit(0);
}

int main(void) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (enter_private_netns() < 0) {
        if (errno == EPERM || errno == EACCES || errno == EINVAL || errno == ENOSPC) {
            printf("userns unavailable: %s\n", strerror(errno));
            return 3;
        }
        sl_die("enter_private_netns");
    }

    int c2p[2], p2c[2];
    if (pipe2(c2p, O_CLOEXEC) < 0 || pipe2(p2c, O_CLOEXEC) < 0)
        sl_die("pipe2");
    pid_t pid = fork();
    if (pid < 0)
        sl_die("fork");
    if (pid == 0) {
        close(c2p[0]);
        close(p2c[1]);
        child(c2p[1], p2c[0]);
    }
    close(c2p[1]);
    close(p2c[0]);

    int status = 1;
    if (!xread1(c2p[0], 'n')) {
        fprintf(stderr, "parent: child failed to create its netns\n");
        goto out;
    }
    int nl = nl_open();
    if (nl < 0)
        sl_die("socket(NETLINK_ROUTE)");
    if (nl_create_veth(nl, "sl0", "sl1", pid) < 0) {
        fprintf(stderr, "RTM_NEWLINK veth: %s\n", strerror(errno));
        close(nl);
        goto out;
    }
    close(nl);
    printf("veth sl0 <-> sl1 created, sl1 moved to netns of pid %d\n", (int)pid);
    configure("parent", "sl0", PARENT_IP);
    xwrite1(p2c[1], 'g');
    if (!xread1(c2p[0], 'b')) {
        fprintf(stderr, "parent: child failed to configure sl1\n");
        goto out;
    }

    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    struct sockaddr_in dst = sin_of(CHILD_IP);
    if (connect(fd, (struct sockaddr *)&dst, sizeof dst) < 0)
        sl_die("connect");
    // 链路刚 up 时 carrier/ARP 可能还没就绪：每 200ms 重发一次，最多 5 秒。
    for (int attempt = 0; attempt < 25 && status != 0; attempt++) {
        if (send(fd, "ping", 4, 0) < 0 && errno != ECONNREFUSED && errno != EHOSTUNREACH)
            sl_die("send");
        struct pollfd pfd = {.fd = fd, .events = POLLIN};
        if (poll(&pfd, 1, 200) == 1) {
            char buf[64];
            ssize_t n = recv(fd, buf, sizeof buf - 1, 0);
            if (n > 0) {
                buf[n] = '\0';
                if (strcmp(buf, "echo:ping") == 0) {
                    puts("udp over veth ok");
                    status = 0;
                }
            }
        }
    }
    close(fd);
    if (status != 0)
        fprintf(stderr, "parent: no UDP reply over the veth\n");

out:
    close(p2c[1]); // 子进程若还在等 'g'，读到 EOF 后退出
    int ws;
    if (waitpid(pid, &ws, 0) < 0)
        sl_die("waitpid");
    close(c2p[0]);
    if (status == 0 && !(WIFEXITED(ws) && WEXITSTATUS(ws) == 0)) {
        fprintf(stderr, "child exited abnormally\n");
        status = 1;
    }
    return status;
}
