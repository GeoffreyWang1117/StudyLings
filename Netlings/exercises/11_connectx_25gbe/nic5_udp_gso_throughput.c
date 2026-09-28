// EXERCISE: nic5_udp_gso_throughput — sendmmsg/recvmmsg 批量收发 + UDP GSO/GRO 压测
// TOPIC: sendmmsg / recvmmsg / UDP_SEGMENT（GSO）/ UDP_GRO / cmsg / SO_RCVBUFFORCE
// DIFFICULTY: ★★★★☆
// BOOK: man 2 sendmmsg；man 2 recvmmsg；man 7 udp（UDP_SEGMENT、UDP_GRO）；man 3 cmsg；"Accelerating UDP packet transmission for QUIC"（Cloudflare 博客，GSO 实测）
// I AM NOT DONE
//
// 说明：
//   用法：nic5_udp_gso_throughput send HOST PORT SECONDS [--gso]
//         nic5_udp_gso_throughput recv PORT [--gro] [--bind ADDR]
//   发送端：每个 UDP 数据报 SEG=1472 字节（1500 MTU − 20 IP − 8 UDP），开头 16 字节是头部
//     {magic, kind=DATA, seq}；连续发 SECONDS 秒，然后发几次 kind=END 的小包（带上总发送数），
//     打印 "sent bytes=B datagrams=D syscalls=S seconds=T gbps=X pps=Y gso=on|off refused=R"
//     - 默认：sendmmsg 一次系统调用交 64 个数据报
//     - --gso：setsockopt(IPPROTO_UDP, UDP_SEGMENT, SEG)，每个 msghdr 是一个 44*1472 = 64768 字节的
//       "超级包"，内核（或支持 UDP GSO 的网卡，比如 mlx5）在最后一刻才把它切成 44 个数据报；
//       缓冲区里每 SEG 字节放一个头部，切开后每个数据报都有自己的 seq。sendmmsg 一次交 8 个超级包
//   接收端：recvmmsg 一次最多收 16 个；打印 "listening on port N gro=on|off"。
//     - --gro：setsockopt(IPPROTO_UDP, UDP_GRO, 1)，内核把同一流的多个数据报合并成一个大 buffer 交上来，
//       cmsg（SOL_UDP, UDP_GRO）里给出段大小 gso_size：必须按 gso_size 把 buffer 切回一个个数据报来计数
//     - 收到 END（或 SIGTERM/SIGINT）后打印
//       "recv bytes=B datagrams=D seconds=T gbps=X pps=Y gro_batches=G bad=K sender_datagrams=S loss_pct=L"
//       bad = 头部损坏/截断的数据报数（正确的程序应为 0）
//
//   为什么这些重要：25 Gbit/s ÷ (1500×8 bit) ≈ 2.1 Mpps。一次 sendto 一个包，每个包都要走一遍
//   系统调用 + 路由/netfilter/qdisc/驱动，单核每秒只能处理几十万到一百多万个 → 单流远跑不满 25G。
//   - sendmmsg/recvmmsg 摊薄系统调用开销（一次陷入内核处理几十个包）
//   - GSO 更进一步：协议栈按 64 KB 走一趟，到网卡驱动（或网卡硬件 USO）才切分，每字节 CPU 开销降一个数量级
//   - GRO 是接收方向的对称优化。QUIC 实现（quiche、msquic、quic-go）和 WireGuard 都依赖它们
//
//   测试（loopback）：普通 / --gso / --gso+--gro 三种组合，接收到的数据报数 ≤ 发送数、不少于 20%
//   （loopback 在负载高时 socket 缓冲区会溢出丢包，所以只检查"大致"一致），bad 必须为 0，
//   --gro 时 gro_batches > 0。真实机器：对端运行 recv，设置 NETLINGS_PEER_IP（可选 NETLINGS_PEER_PORT，
//   默认 5201）后测试会跑 5 秒 --gso 发送并报告吞吐（只报告不判定，目标值见 docs/handoff）。

#include <arpa/inet.h>
#include <endian.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/udp.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

enum {
    SEG = 1472,             // 每个数据报的 UDP 负载
    GSO_SEGS = 65507 / SEG, // 一个超级包里的段数：总长不能超过 UDP 最大负载 65507（且 <= UDP_MAX_SEGMENTS 64）
    SEND_BATCH_PLAIN = 64,
    SEND_BATCH_GSO = 8,
    RECV_BATCH = 16,
    RECV_BUF = 65536,
    HDR = 16,
};
static_assert(GSO_SEGS == 44 && GSO_SEGS <= 64, "超级包段数");

static const uint32_t MAGIC = 0x4e4c3235; // "NL25"
enum { KIND_DATA = 1, KIND_END = 2 };

typedef struct {
    uint32_t magic;
    uint32_t kind;
    uint64_t seq; // DATA：序号；END：发送端发出的数据报总数
} wire_hdr;       // 网络字节序
static_assert(sizeof(wire_hdr) == HDR, "头部 16 字节");

static volatile sig_atomic_t g_stop;
static void on_signal(int sig) { g_stop = 1; }

static double now_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

static void put_hdr(uint8_t *p, uint32_t kind, uint64_t seq) {
    wire_hdr h = {.magic = htonl(MAGIC), .kind = htonl(kind), .seq = htobe64(seq)};
    memcpy(p, &h, sizeof h);
}

static bool get_hdr(const uint8_t *p, size_t len, uint32_t *kind, uint64_t *seq) {
    if (len < HDR)
        return false;
    wire_hdr h;
    memcpy(&h, p, sizeof h);
    if (ntohl(h.magic) != MAGIC)
        return false;
    *kind = ntohl(h.kind);
    *seq = be64toh(h.seq);
    return *kind == KIND_DATA || *kind == KIND_END;
}

// ---------------------------------------------------------------- 发送端

static int do_send(const char *host, const char *port, double seconds, bool gso) {
    struct addrinfo hints = {.ai_family = AF_INET, .ai_socktype = SOCK_DGRAM}, *ai;
    int gai = getaddrinfo(host, port, &hints, &ai);
    if (gai != 0) {
        fprintf(stderr, "getaddrinfo(%s, %s): %s\n", host, port, gai_strerror(gai));
        return 1;
    }
    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    // connect 之后 sendmmsg 不必每条都带地址，内核也能缓存路由
    if (connect(fd, ai->ai_addr, ai->ai_addrlen) < 0) {
        perror("connect");
        freeaddrinfo(ai);
        close(fd);
        return 1;
    }
    freeaddrinfo(ai);
    int sndbuf = 4 << 20;
    if (setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &sndbuf, sizeof sndbuf) < 0)
        perror("setsockopt(SO_SNDBUF)"); // 不致命

    if (gso) {
        // TODO: setsockopt(fd, IPPROTO_UDP, UDP_SEGMENT, &seg, sizeof seg)，seg = SEG（int）。
        //       失败时打印 "setsockopt(UDP_SEGMENT, ...): <strerror>" 并返回 1。
        //       没有这一步，下面每个 64768 字节的"超级包"会被当成**一个**巨大的 UDP 数据报发出去
        //       （在 1500 MTU 的真实网卡上还会被 IP 分片！）
    }

    const int batch = gso ? SEND_BATCH_GSO : SEND_BATCH_PLAIN;
    const size_t msg_len = gso ? (size_t)GSO_SEGS * SEG : SEG; // 每个 msghdr 的字节数
    const int segs_per_msg = gso ? GSO_SEGS : 1;
    uint8_t *buf = calloc((size_t)batch, msg_len);
    struct mmsghdr *msgs = calloc((size_t)batch, sizeof *msgs);
    struct iovec *iov = calloc((size_t)batch, sizeof *iov);
    if (buf == nullptr || msgs == nullptr || iov == nullptr) {
        perror("calloc");
        free(buf), free(msgs), free(iov);
        close(fd);
        return 1;
    }
    for (int i = 0; i < batch; i++) {
        iov[i] = (struct iovec){.iov_base = buf + (size_t)i * msg_len, .iov_len = msg_len};
        msgs[i].msg_hdr = (struct msghdr){.msg_iov = &iov[i], .msg_iovlen = 1};
        for (size_t off = HDR; off < msg_len; off++) // 填充一些可辨认的负载
            buf[(size_t)i * msg_len + off] = (uint8_t)off;
    }

    uint64_t seq = 0, datagrams = 0, bytes = 0, syscalls = 0, refused = 0;
    int rc = 0;
    double t0 = now_sec(), t1 = t0;
    while (!g_stop && (t1 = now_sec()) - t0 < seconds) {
        // 每个段开头写自己的头部（GSO 切分正好落在 SEG 边界上）
        for (int i = 0; i < batch; i++)
            for (int s = 0; s < segs_per_msg; s++)
                put_hdr(buf + (size_t)i * msg_len + (size_t)s * SEG, KIND_DATA, seq + (uint64_t)(i * segs_per_msg + s));
        int n = sendmmsg(fd, msgs, (unsigned)batch, 0);
        syscalls++;
        if (n < 0) {
            if (errno == EINTR)
                continue;
            if (errno == ECONNREFUSED) { // 对端还没开 / 已关闭（ICMP port unreachable），计数后继续
                refused++;
                continue;
            }
            if (errno == ENOBUFS || errno == EAGAIN)
                continue; // 发送队列满，稍后再试
            fprintf(stderr, "sendmmsg: %s%s\n", strerror(errno),
                    gso && errno == EIO ? "（出口网卡不支持 UDP GSO 所需的校验和卸载？）" : "");
            rc = 1;
            break;
        }
        // 部分成功：前 n 条已发出，剩下的下一轮用新的 seq 重发
        datagrams += (uint64_t)n * (uint64_t)segs_per_msg;
        bytes += (uint64_t)n * msg_len;
        seq += (uint64_t)n * (uint64_t)segs_per_msg;
    }
    double elapsed = t1 - t0;

    // END：普通小包（小于 gso_size 的发送不会被分段），发几次防丢
    uint8_t end[HDR];
    put_hdr(end, KIND_END, datagrams);
    for (int i = 0; i < 5; i++) {
        if (send(fd, end, sizeof end, 0) < 0 && errno != ECONNREFUSED) {
            perror("send(END)");
            rc = 1;
            break;
        }
        nanosleep(&(struct timespec){.tv_nsec = 20 * 1000 * 1000}, nullptr);
    }
    if (elapsed <= 0)
        elapsed = 1e-9;
    printf("sent bytes=%llu datagrams=%llu syscalls=%llu seconds=%.3f gbps=%.3f pps=%.0f gso=%s refused=%llu\n",
           (unsigned long long)bytes, (unsigned long long)datagrams, (unsigned long long)syscalls, elapsed,
           (double)bytes * 8 / elapsed / 1e9, (double)datagrams / elapsed, gso ? "on" : "off",
           (unsigned long long)refused);
    free(buf), free(msgs), free(iov);
    close(fd);
    return rc;
}

// ---------------------------------------------------------------- 接收端

typedef struct {
    uint64_t datagrams, bytes, bad, gro_batches, sender_datagrams;
    bool got_end;
    double first, last;
} rx_stats;

// 从 cmsg 里取 UDP_GRO 段大小；没有返回 0
static int gro_size(struct msghdr *mh) {
    for (struct cmsghdr *c = CMSG_FIRSTHDR(mh); c != nullptr; c = CMSG_NXTHDR(mh, c)) {
        if (c->cmsg_level == SOL_UDP && c->cmsg_type == UDP_GRO && c->cmsg_len >= CMSG_LEN(sizeof(int))) {
            int v;
            memcpy(&v, CMSG_DATA(c), sizeof v);
            return v;
        }
    }
    return 0;
}

// 处理一次收到的 buffer：GRO 合并时按 gso 切回数据报（最后一段可以更短）
static void account(rx_stats *st, const uint8_t *p, size_t len, int gso) {
    // TODO: GRO 合并时（gso > 0 且 gso < len）一个 buffer 里有多个数据报，每 gso 字节一个
    //       （最后一段可以更短）：step 应取 gso，并把 st->gro_batches 加 1。
    //       现在把整个 buffer 当成一个数据报，计数会少几十倍
    size_t step = len;
    for (size_t off = 0; off < len; off += step) {
        size_t seglen = len - off < step ? len - off : step;
        uint32_t kind;
        uint64_t seq;
        if (!get_hdr(p + off, seglen, &kind, &seq)) {
            st->bad++;
            continue;
        }
        if (kind == KIND_END) {
            st->got_end = true;
            st->sender_datagrams = seq;
            continue;
        }
        if (st->datagrams == 0)
            st->first = now_sec();
        st->datagrams++;
        st->bytes += seglen;
    }
    if (st->datagrams)
        st->last = now_sec();
}

static int do_recv(int port, bool gro, const char *bind_addr) {
    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    int rcvbuf = 8 << 20;
    // SO_RCVBUFFORCE 可以突破 net.core.rmem_max（需要 CAP_NET_ADMIN）；否则退回 SO_RCVBUF
    if (setsockopt(fd, SOL_SOCKET, SO_RCVBUFFORCE, &rcvbuf, sizeof rcvbuf) < 0 &&
        setsockopt(fd, SOL_SOCKET, SO_RCVBUF, &rcvbuf, sizeof rcvbuf) < 0)
        perror("setsockopt(SO_RCVBUF)");
    if (gro) {
        int one = 1;
        if (setsockopt(fd, IPPROTO_UDP, UDP_GRO, &one, sizeof one) < 0) {
            fprintf(stderr, "setsockopt(UDP_GRO): %s（需要 Linux 5.0+）\n", strerror(errno));
            close(fd);
            return 1;
        }
    }
    struct sockaddr_in addr = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    if (inet_pton(AF_INET, bind_addr, &addr.sin_addr) != 1) {
        fprintf(stderr, "无效的 IPv4 地址 %s\n", bind_addr);
        close(fd);
        return 2;
    }
    if (bind(fd, (struct sockaddr *)&addr, sizeof addr) < 0) {
        perror("bind");
        close(fd);
        return 1;
    }

    uint8_t *bufs = malloc((size_t)RECV_BATCH * RECV_BUF);
    struct mmsghdr msgs[RECV_BATCH];
    struct iovec iov[RECV_BATCH];
    // cmsg 缓冲区要按 cmsghdr 对齐
    union {
        char buf[CMSG_SPACE(sizeof(int))];
        struct cmsghdr align;
    } ctrl[RECV_BATCH];
    if (bufs == nullptr) {
        perror("malloc");
        close(fd);
        return 1;
    }
    printf("listening on port %d gro=%s\n", port, gro ? "on" : "off");

    rx_stats st = {};
    int rc = 0;
    while (!g_stop && !st.got_end) {
        for (int i = 0; i < RECV_BATCH; i++) {
            iov[i] = (struct iovec){.iov_base = bufs + (size_t)i * RECV_BUF, .iov_len = RECV_BUF};
            msgs[i].msg_hdr = (struct msghdr){
                .msg_iov = &iov[i], .msg_iovlen = 1, .msg_control = ctrl[i].buf, .msg_controllen = sizeof ctrl[i].buf};
            msgs[i].msg_len = 0;
        }
        int n = recvmmsg(fd, msgs, RECV_BATCH, MSG_WAITFORONE, nullptr);
        if (n < 0) {
            if (errno == EINTR)
                continue; // SIGTERM → 回到循环条件
            perror("recvmmsg");
            rc = 1;
            break;
        }
        for (int i = 0; i < n; i++) {
            if (msgs[i].msg_hdr.msg_flags & MSG_TRUNC) {
                st.bad++;
                continue;
            }
            account(&st, bufs + (size_t)i * RECV_BUF, msgs[i].msg_len, gro_size(&msgs[i].msg_hdr));
        }
    }
    double secs = st.last - st.first;
    if (secs <= 0)
        secs = 1e-9;
    double loss = st.sender_datagrams ? 100.0 * ((double)st.sender_datagrams - (double)st.datagrams) /
                                            (double)st.sender_datagrams
                                      : 0.0;
    printf("recv bytes=%llu datagrams=%llu seconds=%.3f gbps=%.3f pps=%.0f gro_batches=%llu bad=%llu "
           "sender_datagrams=%llu loss_pct=%.2f\n",
           (unsigned long long)st.bytes, (unsigned long long)st.datagrams, secs, (double)st.bytes * 8 / secs / 1e9,
           (double)st.datagrams / secs, (unsigned long long)st.gro_batches, (unsigned long long)st.bad,
           (unsigned long long)st.sender_datagrams, loss);
    free(bufs);
    close(fd);
    return rc;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    struct sigaction sa = {.sa_handler = on_signal}; // 不设 SA_RESTART：让 recvmmsg 返回 EINTR
    sigemptyset(&sa.sa_mask);
    if (sigaction(SIGTERM, &sa, nullptr) < 0 || sigaction(SIGINT, &sa, nullptr) < 0)
        sl_die("sigaction");

    if (argc >= 5 && strcmp(argv[1], "send") == 0) {
        bool gso = argc == 6 && strcmp(argv[5], "--gso") == 0;
        double secs = atof(argv[4]);
        if ((argc == 6 && !gso) || argc > 6 || secs <= 0) {
            fprintf(stderr, "usage: %s send HOST PORT SECONDS [--gso]\n", argv[0]);
            return 2;
        }
        return do_send(argv[2], argv[3], secs, gso);
    }
    if (argc >= 3 && strcmp(argv[1], "recv") == 0) {
        bool gro = false;
        const char *bind_addr = "0.0.0.0";
        for (int i = 3; i < argc; i++) {
            if (strcmp(argv[i], "--gro") == 0)
                gro = true;
            else if (strcmp(argv[i], "--bind") == 0 && i + 1 < argc)
                bind_addr = argv[++i];
            else {
                fprintf(stderr, "unknown option %s\n", argv[i]);
                return 2;
            }
        }
        int port = atoi(argv[2]);
        if (port <= 0 || port > 65535) {
            fprintf(stderr, "bad port %s\n", argv[2]);
            return 2;
        }
        return do_recv(port, gro, bind_addr);
    }
    fprintf(stderr, "usage: %s send HOST PORT SECONDS [--gso]\n       %s recv PORT [--gro] [--bind ADDR]\n", argv[0],
            argv[0]);
    return 2;
}
