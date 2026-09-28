// EXERCISE: ns1_unshare_net — 不用 root，用 user namespace + network namespace 造一个"只有 lo 的世界"
// TOPIC: unshare(CLONE_NEWUSER|CLONE_NEWNET) / uid_map·gid_map·setgroups / SIOCSIFFLAGS / getifaddrs
// DIFFICULTY: ★★★☆☆
// BOOK: man 7 network_namespaces；man 7 user_namespaces；man 2 unshare；man 7 netdevice；man 3 getifaddrs
// I AM NOT DONE
//
// 说明：
//   用法：ns1_unshare_net PORT
//   1. unshare(CLONE_NEWUSER | CLONE_NEWNET)：进程进入一个新的 user namespace 和新的 network namespace。
//      新 netns 里只有一个 lo，而且是 DOWN 的；没有路由、没有 iptables 规则、端口表是空的。
//   2. 写 /proc/self/setgroups ("deny")、/proc/self/uid_map ("0 <原uid> 1")、/proc/self/gid_map：
//      把调用者映射成新 userns 里的 root。这样普通用户也拥有了"这个 netns 里的" CAP_NET_ADMIN，
//      可以配置网卡 —— 这就是 rootless 容器（podman、rootless docker、`unshare -rn`）的原理。
//      （必须先写 setgroups=deny 才能以非特权身份写 gid_map，防止借 setgroups 丢掉补充组绕过权限。）
//   3. 用 ioctl(SIOCGIFFLAGS/SIOCSIFFLAGS) 给 lo 加上 IFF_UP —— 也就是 `ip link set lo up` 的老式写法。
//      lo 不 up 的话，连 127.0.0.1 都连不上（ENETUNREACH）。
//   4. getifaddrs() 列出接口，每个接口打印一行 "if <名字>"（去重）。
//   5. 在 127.0.0.1:PORT 上 listen，自己 connect 自己并收发一个字节，打印 "self-connect ok"，
//      再打印 "ready"，然后阻塞到 stdin EOF 再退出。
//
//   为什么重要：`docker run --network none`、`unshare -rn`、Kubernetes Pod 的 "pause" 容器、
//   systemd 的 PrivateNetwork=yes、Chrome/Firefox 的沙箱进程，都是先得到这样一个空 netns，
//   再由 CNI 插件 / libnetwork 往里面插 veth（下一题）。netns 隔离的是整个协议栈：接口、路由、
//   端口号、conntrack、/proc/sys/net 都各有一份。
//
//   探针：宿主机上先占住 127.0.0.1:PORT（只 bind 不 listen）→ 你的程序在自己的 netns 里仍然能
//   bind 同一个端口；输出里接口只有 lo；运行期间从宿主机 connect 127.0.0.1:PORT 必须被拒绝
//   （ECONNREFUSED —— 那是另一个协议栈）；/proc/<pid>/ns/net 与探针自己的不同。
//   若系统禁用了非特权 user namespace（unshare 返回 EPERM），程序打印 "userns unavailable" 并
//   exit 3，探针会 skip（Ubuntu 24.04+ 需要 sysctl kernel.apparmor_restrict_unprivileged_userns=0
//   或以 root 运行）。

#include <errno.h>
#include <fcntl.h>
#include <ifaddrs.h>
#include <net/if.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

// 脚手架：把一小段文本写进 /proc 文件（必须一次 write 写完，/proc/self/uid_map 只接受一次写入）。
[[maybe_unused]] static int write_file(const char *path, const char *text) {
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

// 进入新的 user + network namespace，并把当前 uid/gid 映射成其中的 root。
// 成功返回 0；失败返回 -1（errno 保留）。
static int enter_private_netns(void) {
    // TODO: 1) 先记下 getuid()/getgid()（unshare 之后在映射写好前它们会变成 overflow id 65534）；
    //       2) unshare(CLONE_NEWUSER | CLONE_NEWNET)；
    //       3) write_file("/proc/self/setgroups", "deny")（ENOENT 可忽略）；
    //       4) write_file("/proc/self/uid_map", "0 <uid> 1\n") 和 gid_map 同理。
    return 0; // 占位：什么都没做，进程还在宿主机的 netns 里
}

// 给接口 ifname 加上 IFF_UP（等价于 `ip link set <ifname> up`）。成功 0，失败 -1。
static int link_up(const char *ifname) {
    // TODO: 建一个任意的 socket（如 AF_INET/SOCK_DGRAM）承载 ioctl；
    //       struct ifreq 填 ifr_name，SIOCGIFFLAGS 读出旧 flags，或上 IFF_UP，再 SIOCSIFFLAGS 写回。
    //       别忘了 close 这个 socket。
    (void)ifname;
    return 0; // 占位
}

// 脚手架：列出接口（getifaddrs 对每个接口的每个地址族返回一项，这里按名字去重）。
static void list_interfaces(void) {
    struct ifaddrs *ifs = nullptr;
    if (getifaddrs(&ifs) < 0)
        sl_die("getifaddrs");
    for (struct ifaddrs *a = ifs; a != nullptr; a = a->ifa_next) {
        bool seen = false;
        for (struct ifaddrs *b = ifs; b != a; b = b->ifa_next)
            if (strcmp(a->ifa_name, b->ifa_name) == 0)
                seen = true;
        if (!seen)
            printf("if %s\n", a->ifa_name);
    }
    freeifaddrs(ifs);
}

// 脚手架：listen 127.0.0.1:port，自己连自己，收发一个字节。返回监听 fd。
static int self_connect(int port) {
    struct sockaddr_in addr = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    int lfd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (lfd < 0)
        sl_die("socket");
    if (bind(lfd, (struct sockaddr *)&addr, sizeof addr) < 0)
        sl_die("bind 127.0.0.1");
    if (listen(lfd, 8) < 0)
        sl_die("listen");
    int cfd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (cfd < 0)
        sl_die("socket");
    if (connect(cfd, (struct sockaddr *)&addr, sizeof addr) < 0)
        sl_die("connect 127.0.0.1 (lo 是 up 的吗？)");
    int afd = accept(lfd, nullptr, nullptr);
    if (afd < 0)
        sl_die("accept");
    char c = '!';
    if (write(cfd, &c, 1) != 1 || read(afd, &c, 1) != 1)
        sl_die("self-connect exchange");
    close(afd);
    close(cfd);
    return lfd;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    int port = atoi(argv[1]);
    if (port <= 0 || port > 65535) {
        fprintf(stderr, "ns1_unshare_net: bad port\n");
        return 2;
    }

    if (enter_private_netns() < 0) {
        if (errno == EPERM || errno == EACCES || errno == EINVAL || errno == ENOSPC) {
            printf("userns unavailable: %s\n", strerror(errno));
            return 3;
        }
        sl_die("enter_private_netns");
    }
    if (link_up("lo") < 0)
        sl_die("SIOCSIFFLAGS lo");

    list_interfaces();
    int lfd = self_connect(port);
    puts("self-connect ok");
    puts("ready");

    // 阻塞到 stdin EOF：探针趁这段时间从宿主机检查端口和 /proc/<pid>/ns/net。
    char buf[256];
    while (read(STDIN_FILENO, buf, sizeof buf) > 0) {
    }
    close(lfd);
    return 0;
}
