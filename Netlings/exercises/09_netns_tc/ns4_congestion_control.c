// EXERCISE: ns4_congestion_control — 按连接选择拥塞控制算法：TCP_CONGESTION 设 bbr / cubic 并验证
// TOPIC: setsockopt/getsockopt(TCP_CONGESTION) / 可插拔拥塞控制模块 / BBR vs CUBIC / 错误码 ENOENT·EPERM
// DIFFICULTY: ★★☆☆☆
// BOOK: TCP/IP Illustrated Vol.1 (2nd ed.) §16（拥塞控制，CUBIC）；man 7 tcp；RFC 9438（CUBIC）；BBR 论文（ACM Queue 2016）
// I AM NOT DONE
//
// 说明：
//   用法：ns4_congestion_control server PORT
//         ns4_congestion_control client HOST PORT SECONDS ALGO
//   client：创建 socket 后、connect 之前用 setsockopt(IPPROTO_TCP, TCP_CONGESTION, ALGO) 为这一条连接
//   选择拥塞控制算法（不影响系统默认的 net.ipv4.tcp_congestion_control），再用 getsockopt 读回
//   内核实际使用的算法名，打印 "algo=<名字>"；然后发送 SECONDS 秒，打印 "goodput_mbps=<x>"。
//   设置失败必须报告并 exit 1，例如：
//       "TCP_CONGESTION 'foo': No such file or directory"   （ENOENT：没有这个算法/模块加载不了）
//       "TCP_CONGESTION 'cubic': Operation not permitted"   （EPERM：非 root 且不在
//                                                           net.ipv4.tcp_allowed_congestion_control 里）
//   server：同 ns3，读完丢掉，打印 "received <字节数>"。
//
//   要点：TCP_CONGESTION 的 level 是 IPPROTO_TCP（不是 SOL_SOCKET！在 SOL_SOCKET 层 13 号选项是
//   SO_LINGER）；optval 是算法名字符串，optlen 是 strlen；getsockopt 时给一个 TCP_CA_NAME_MAX(16)
//   字节的缓冲区。连接建立后也可以改，但在 connect 前设好，握手阶段（初始窗口）就用上了新算法。
//
//   为什么重要：CDN/视频服务（YouTube、Netflix、Cloudflare）对外网连接用 BBR，对数据中心内部连接用
//   DCTCP/CUBIC —— 正是靠按 socket 设置 TCP_CONGESTION；Go 的 syscall.SetsockoptString、nginx 没有
//   直接配置但可通过 BPF（bpf_setsockopt）或 `ip route ... congctl bbr` 按路由选择。
//
//   探针：在 127.0.0.1 上分别请求 bbr 和 cubic，要求 algo= 与请求一致，并用 `ss -tin` 从外部核对；
//   请求不存在的算法必须失败并报告 ENOENT；（root）netlab 中 tbf 50mbit 瓶颈下两种算法 goodput 都
//   在 30~60 Mbit/s；有 netem 的机器上（这台验证机没有）比较 1% 丢包 + 20ms 延迟下 BBR 明显快于 CUBIC。

#include <errno.h>
#include <fcntl.h>
#include <linux/tcp.h>
#include <netdb.h>
#include <netinet/in.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

#ifndef TCP_CA_NAME_MAX
#define TCP_CA_NAME_MAX 16
#endif

enum { CHUNK = 64 * 1024 };

// 为 fd 选择拥塞控制算法 algo。成功 0；失败 -1（errno 保留）。
static int set_congestion(int fd, const char *algo) {
    // BUG: 两个错误 —— 选项放在了 SOL_SOCKET 层（那里的 13 号是 SO_LINGER，内核返回 EINVAL），
    //      而且返回值被丢掉了，于是连接悄悄用着系统默认算法，调用者还以为设置成功了。
    // TODO: 用正确的 level，并把 setsockopt 的结果返回给调用者。
    (void)setsockopt(fd, SOL_SOCKET, TCP_CONGESTION, algo, (socklen_t)strlen(algo));
    return 0;
}

// 读回 fd 实际使用的算法名到 out[TCP_CA_NAME_MAX + 1]。成功 0；失败 -1。
static int get_congestion(int fd, char out[static TCP_CA_NAME_MAX + 1]) {
    socklen_t len = TCP_CA_NAME_MAX;
    memset(out, 0, TCP_CA_NAME_MAX + 1);
    return getsockopt(fd, IPPROTO_TCP, TCP_CONGESTION, out, &len);
}

// ---------------------------------------------------------------------------------------------
// 脚手架
// ---------------------------------------------------------------------------------------------
static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

static int run_server(int port) {
    int lfd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (lfd < 0)
        sl_die("socket");
    int one = 1;
    if (setsockopt(lfd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one) < 0)
        sl_die("SO_REUSEADDR");
    struct sockaddr_in sa = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    sa.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(lfd, (struct sockaddr *)&sa, sizeof sa) < 0)
        sl_die("bind");
    if (listen(lfd, 16) < 0)
        sl_die("listen");
    printf("listening on port %d\n", port);
    static char buf[256 * 1024];
    for (;;) {
        int cfd = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
        if (cfd < 0) {
            if (errno == EINTR || errno == ECONNABORTED)
                continue;
            sl_die("accept");
        }
        uint64_t total = 0;
        for (;;) {
            ssize_t n = read(cfd, buf, sizeof buf);
            if (n > 0) {
                total += (uint64_t)n;
                continue;
            }
            if (n < 0 && errno == EINTR)
                continue;
            break;
        }
        close(cfd);
        printf("received %llu\n", (unsigned long long)total);
    }
}

static int run_client(const char *host, const char *port, double seconds, const char *algo) {
    struct addrinfo hints = {.ai_family = AF_INET, .ai_socktype = SOCK_STREAM};
    struct addrinfo *res = nullptr;
    int rc = getaddrinfo(host, port, &hints, &res);
    if (rc != 0) {
        fprintf(stderr, "getaddrinfo %s: %s\n", host, gai_strerror(rc));
        return 1;
    }
    int fd = socket(res->ai_family, res->ai_socktype | SOCK_CLOEXEC, res->ai_protocol);
    if (fd < 0)
        sl_die("socket");

    if (set_congestion(fd, algo) < 0) {
        fprintf(stderr, "TCP_CONGESTION '%s': %s\n", algo, strerror(errno));
        freeaddrinfo(res);
        close(fd);
        return 1;
    }
    if (connect(fd, res->ai_addr, res->ai_addrlen) < 0)
        sl_die("connect");
    freeaddrinfo(res);

    char name[TCP_CA_NAME_MAX + 1];
    if (get_congestion(fd, name) < 0)
        sl_die("getsockopt TCP_CONGESTION");
    printf("algo=%s\n", name);

    int fl = fcntl(fd, F_GETFL);
    if (fl < 0 || fcntl(fd, F_SETFL, fl | O_NONBLOCK) < 0)
        sl_die("fcntl O_NONBLOCK");
    char *chunk = calloc(1, CHUNK);
    if (chunk == nullptr)
        sl_die("calloc");
    double t0 = now_s(), end = t0 + seconds;
    for (double t = t0; t < end; t = now_s()) {
        struct pollfd pfd = {.fd = fd, .events = POLLOUT};
        int pr = poll(&pfd, 1, (int)((end - t) * 1000) + 1);
        if (pr < 0 && errno != EINTR)
            sl_die("poll");
        if (pr > 0) {
            ssize_t w = write(fd, chunk, CHUNK);
            if (w < 0 && errno != EAGAIN && errno != EINTR)
                sl_die("write");
        }
    }
    double elapsed = now_s() - t0;
    struct tcp_info ti = {};
    socklen_t tlen = sizeof ti;
    if (getsockopt(fd, IPPROTO_TCP, TCP_INFO, &ti, &tlen) < 0)
        sl_die("getsockopt TCP_INFO");
    printf("goodput_mbps=%.2f retrans=%u\n", (double)ti.tcpi_bytes_acked * 8.0 / elapsed / 1e6,
           ti.tcpi_total_retrans);
    free(chunk);
    close(fd);
    return 0;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 3 && strcmp(argv[1], "server") == 0)
        return run_server(atoi(argv[2]));
    if (argc == 6 && strcmp(argv[1], "client") == 0) {
        double secs = atof(argv[4]);
        if (secs <= 0) {
            fprintf(stderr, "SECONDS must be positive\n");
            return 2;
        }
        return run_client(argv[2], argv[3], secs, argv[5]);
    }
    fprintf(stderr, "usage: %s server PORT | client HOST PORT SECONDS ALGO\n", argv[0]);
    return 2;
}
