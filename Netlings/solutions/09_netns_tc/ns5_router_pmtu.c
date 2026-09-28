// EXERCISE: ns5_router_pmtu — 经过路由器的路径 MTU 发现：DF 位、ICMP Fragmentation Needed、EMSGSIZE 与 IP_MTU
// TOPIC: IP_MTU_DISCOVER=IP_PMTUDISC_DO / EMSGSIZE / getsockopt(IP_MTU) / 路由器转发与 ICMP type 3 code 4
// DIFFICULTY: ★★★★☆
// BOOK: TCP/IP Illustrated Vol.1 (2nd ed.) §10.7–10.8（UDP 与 IP 分片、PMTUD）、§8（ICMP）；RFC 1191；RFC 8899（DPLPMTUD）；man 7 ip
//
// 说明：
//   用法：ns5_router_pmtu server PORT
//         ns5_router_pmtu client HOST PORT [TOTAL]
//   拓扑（探针用 netlab 搭）：client ──MTU 1500── router ──MTU 1400── server，router 打开 ip_forward。
//
//   client 把 TOTAL（默认 200000）字节切成数据报，停等式可靠发送：每个数据报带 8 字节头
//   {offset, total}（网络序），server 回 4 字节 ACK（下一个期望的 offset），200ms 没 ACK 就重发。
//   socket 已设置 IP_MTU_DISCOVER = IP_PMTUDISC_DO：永远带 DF 位、本机绝不分片。于是：
//     1. 一开始按以太网 MTU 1500 切片（1500 - 20 IP - 8 UDP - 8 头 = 1464 字节负载）。
//     2. 第一个 1500 字节的包到达 router，出口 MTU 只有 1400 且 DF=1 → router 丢包并回
//        ICMP "Fragmentation Needed"（type 3 code 4，里面带 next-hop MTU = 1400）。
//     3. client 内核收到 ICMP，把 1400 记进这条路由的 PMTU 缓存（`ip route get` 能看到 "mtu 1400"），
//        之后对这个已 connect 的 socket：send 超过 PMTU 的数据报直接失败 EMSGSIZE，
//        等待 ACK 时 recv 也可能拿到这个异步错误 EMSGSIZE。
//     4. 你要做的：遇到 EMSGSIZE 时用 getsockopt(IPPROTO_IP, IP_MTU) 读出当前路径 MTU，
//        按它重新计算切片大小，然后重发当前这一片（它刚才被 router 丢了）。
//   结束时打印 "path_mtu=<IP_MTU 读到的值>" 和 "delivered <已确认字节数>"。server 收齐后打印
//   "received <字节数> bytes"。
//
//   为什么重要：IPv6 路由器根本不分片，IPv4 上各种隧道（VXLAN、GRE、IPsec、WireGuard、
//   Kubernetes overlay 网络）又会吃掉几十字节 MTU。QUIC（RFC 9000 §14、RFC 8899）、WireGuard、
//   DNS over UDP (EDNS0 buffer size) 都必须自己做 PMTU 发现：设 DF，按 EMSGSIZE/IP_MTU 或探测结果
//   调整报文大小。ICMP 被防火墙过滤时会出现经典的 "PMTU 黑洞"（连接能建立、大包卡死）。
//
//   探针（需要 root，3 个 netns + 路由）：要求 client 打印 path_mtu=1400、全部字节送达，
//   server 收到的字节数与 TOTAL 一致。

#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum {
    IP_UDP_OVERHEAD = 20 + 8, // IPv4 头（无选项）+ UDP 头
    HDR = 8,                  // 我们自己的 {offset, total}
    ACK_TIMEOUT_MS = 200,
    MAX_TIMEOUTS = 25,        // 连续这么多次没 ACK 就放弃（约 5 秒）
    DEFAULT_TOTAL = 200000,
};

// 返回内核当前记录的、到已 connect 对端的路径 MTU（字节）；失败返回 -1。
static int path_mtu(int fd) {
    int mtu = 0;
    socklen_t len = sizeof mtu;
    if (getsockopt(fd, IPPROTO_IP, IP_MTU, &mtu, &len) < 0)
        return -1;
    return mtu;
}

// 在 send 或 recv 得到 EMSGSIZE 之后调用：更新 *chunk（每个数据报的负载字节数）。
// 返回 0 表示已调整、应立即重发当前片；返回 -1 表示无法恢复。
static int on_emsgsize(int fd, int *chunk) {
    int mtu = path_mtu(fd);
    if (mtu < 0) {
        perror("getsockopt IP_MTU");
        return -1;
    }
    int c = mtu - IP_UDP_OVERHEAD - HDR;
    if (c <= 0 || c >= *chunk) { // PMTU 没变小却还 EMSGSIZE：不该发生，避免死循环
        fprintf(stderr, "EMSGSIZE but path mtu is %d (chunk %d)\n", mtu, *chunk);
        return -1;
    }
    printf("EMSGSIZE: path mtu now %d, chunk %d -> %d\n", mtu, *chunk, c);
    *chunk = c;
    return 0;
}

// ---------------------------------------------------------------------------------------------
// 脚手架
// ---------------------------------------------------------------------------------------------
static int run_server(int port) {
    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    struct sockaddr_in sa = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    sa.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(fd, (struct sockaddr *)&sa, sizeof sa) < 0)
        sl_die("bind");
    printf("listening on port %d\n", port);
    static char buf[65536];
    uint32_t expected = 0;
    bool done = false;
    for (;;) {
        struct sockaddr_in from;
        socklen_t flen = sizeof from;
        ssize_t n = recvfrom(fd, buf, sizeof buf, 0, (struct sockaddr *)&from, &flen);
        if (n < 0) {
            if (errno == EINTR)
                continue;
            sl_die("recvfrom");
        }
        if (n < HDR)
            continue;
        uint32_t off, total;
        memcpy(&off, buf, 4);
        memcpy(&total, buf + 4, 4);
        off = ntohl(off);
        total = ntohl(total);
        if (off == expected)
            expected += (uint32_t)(n - HDR); // 按序到达才接收；重复/乱序的只重发 ACK
        uint32_t ack = htonl(expected);
        if (sendto(fd, &ack, sizeof ack, 0, (struct sockaddr *)&from, flen) < 0)
            perror("sendto ack");
        if (!done && total > 0 && expected >= total) {
            printf("received %u bytes\n", expected);
            done = true;
        }
    }
}

static int dial_udp(const char *host, const char *port) {
    struct addrinfo hints = {.ai_family = AF_INET, .ai_socktype = SOCK_DGRAM};
    struct addrinfo *res = nullptr;
    int rc = getaddrinfo(host, port, &hints, &res);
    if (rc != 0) {
        fprintf(stderr, "getaddrinfo %s: %s\n", host, gai_strerror(rc));
        exit(1);
    }
    int fd = socket(res->ai_family, res->ai_socktype | SOCK_CLOEXEC, res->ai_protocol);
    if (fd < 0)
        sl_die("socket");
    // DF 位 + 本机不分片：超过已知 PMTU 的 send 直接 EMSGSIZE。
    int pmtu = IP_PMTUDISC_DO;
    if (setsockopt(fd, IPPROTO_IP, IP_MTU_DISCOVER, &pmtu, sizeof pmtu) < 0)
        sl_die("IP_MTU_DISCOVER");
    if (connect(fd, res->ai_addr, res->ai_addrlen) < 0) // connect 后才能收到 ICMP 错误、读 IP_MTU
        sl_die("connect");
    freeaddrinfo(res);
    return fd;
}

static int run_client(const char *host, const char *port, uint32_t total) {
    int fd = dial_udp(host, port);
    int chunk = 1500 - IP_UDP_OVERHEAD - HDR; // 乐观假设：一路都是以太网 MTU 1500
    char *pkt = malloc(65536);
    if (pkt == nullptr)
        sl_die("malloc");
    uint32_t acked = 0;
    int timeouts = 0;
    int status = 1;

    while (acked < total) {
        uint32_t len = total - acked < (uint32_t)chunk ? total - acked : (uint32_t)chunk;
        uint32_t off_be = htonl(acked), total_be = htonl(total);
        memcpy(pkt, &off_be, 4);
        memcpy(pkt + 4, &total_be, 4);
        memset(pkt + HDR, (int)('a' + acked % 26), len);

        if (send(fd, pkt, HDR + len, 0) < 0) {
            if (errno == EMSGSIZE) {
                if (on_emsgsize(fd, &chunk) < 0)
                    goto out;
                continue; // 按新的切片大小重发
            }
            if (errno != ECONNREFUSED) // 服务器还没起来时的 ICMP port unreachable：当成丢包
                sl_die("send");
        }

        struct pollfd pfd = {.fd = fd, .events = POLLIN};
        int pr = poll(&pfd, 1, ACK_TIMEOUT_MS);
        if (pr < 0 && errno != EINTR)
            sl_die("poll");
        if (pr <= 0) {
            if (++timeouts >= MAX_TIMEOUTS) {
                fprintf(stderr, "gave up after %d timeouts (acked %u of %u)\n", timeouts, acked, total);
                goto out;
            }
            continue; // 超时重发
        }
        uint32_t ack;
        ssize_t n = recv(fd, &ack, sizeof ack, 0);
        if (n < 0) {
            // ICMP 带来的异步错误会在这里冒出来（sk_err）。
            if (errno == EMSGSIZE) {
                if (on_emsgsize(fd, &chunk) < 0)
                    goto out;
                continue;
            }
            if (errno == ECONNREFUSED || errno == EINTR)
                continue;
            sl_die("recv");
        }
        if (n == sizeof ack && ntohl(ack) > acked) {
            acked = ntohl(ack);
            timeouts = 0;
        }
    }
    status = 0;
out:
    printf("path_mtu=%d\n", path_mtu(fd));
    printf("delivered %u\n", acked);
    free(pkt);
    close(fd);
    return status;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 3 && strcmp(argv[1], "server") == 0)
        return run_server(atoi(argv[2]));
    if ((argc == 4 || argc == 5) && strcmp(argv[1], "client") == 0) {
        long total = argc == 5 ? atol(argv[4]) : DEFAULT_TOTAL;
        if (total <= 0 || total > 100000000) {
            fprintf(stderr, "TOTAL must be in 1..100000000\n");
            return 2;
        }
        return run_client(argv[2], argv[3], (uint32_t)total);
    }
    fprintf(stderr, "usage: %s server PORT | client HOST PORT [TOTAL]\n", argv[0]);
    return 2;
}
