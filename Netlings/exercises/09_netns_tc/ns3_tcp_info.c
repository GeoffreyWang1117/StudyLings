// EXERCISE: ns3_tcp_info — 自己写一个 `ss -ti`：边发数据边用 TCP_INFO 观察 RTT、cwnd、重传和交付速率
// TOPIC: getsockopt(TCP_INFO) / struct tcp_info / delivery_rate·pacing_rate / goodput 的正确算法
// DIFFICULTY: ★★★☆☆
// BOOK: TCP/IP Illustrated Vol.1 (2nd ed.) §14（超时与重传）、§16（拥塞控制）；man 7 tcp；include/uapi/linux/tcp.h
// I AM NOT DONE
//
// 说明：
//   用法：ns3_tcp_info server PORT
//         ns3_tcp_info client HOST PORT SECONDS
//   server：监听 PORT，逐个 accept 连接，把数据读完丢掉，打印 "received <字节数>"。
//   client：连接后用非阻塞 socket 持续发送 SECONDS 秒；每 200ms 用 getsockopt(TCP_INFO) 取一次
//   内核里这条连接的状态，打印一行：
//       t=<秒> rtt_us=<平滑RTT> cwnd=<拥塞窗口(段)> retrans=<累计重传段数>
//       delivery_mbps=<交付速率> pacing_mbps=<pacing 速率> acked=<已被确认字节数>
//   结束时打印 "goodput_mbps=<x> retrans=<n>"。
//
//   要点：
//   1. struct tcp_info 请用 <linux/tcp.h> 里的版本（glibc 的 <netinet/tcp.h> 版本太老，没有
//      tcpi_delivery_rate / tcpi_bytes_acked）。getsockopt 的 optlen 是 in/out：老内核返回的结构
//      可能更短，新字段就是 0。
//   2. 速率字段 tcpi_delivery_rate / tcpi_pacing_rate 的单位是 字节/秒（×8/1e6 才是 Mbit/s）；
//      tcpi_rtt 是微秒；tcpi_snd_cwnd 单位是"段"（MSS 个数）。
//   3. goodput 不能用"write 成功了多少字节 / 时间"：write 返回只代表数据进了本机的发送缓冲区
//      （可以有好几 MB！），要用对端确认过的字节数 tcpi_bytes_acked / 时间。
//
//   为什么重要：`ss -ti`、iperf3 的 retr/cwnd 列、Envoy/nginx 的 upstream RTT 指标、
//   Google 的 BBR 调参、QUIC 的 qlog，全都来自这几个字段。线上排查"慢"时第一眼就看它们。
//
//   探针（需要 root，用 netlab 建两个 netns + veth）：客户端出口加 `tc qdisc tbf rate 50mbit`，
//   SECONDS=3，要求 goodput 在 30~60 Mbit/s、采样行的 rtt_us/cwnd/pacing 为正、delivery_mbps 接近瓶颈。
//   有 netem 的机器上（这台验证机没有）还会加 delay 40ms 要求 rtt_us >= 40000，加 loss 1% 要求 retrans > 0。

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

enum { SAMPLE_MS = 200, CHUNK = 64 * 1024 };

typedef struct {
    uint32_t rtt_us;
    uint32_t cwnd;
    uint32_t total_retrans;
    double delivery_mbps;
    double pacing_mbps;
    uint64_t bytes_acked;
} tcp_sample;

// 字节/秒 → Mbit/s
[[maybe_unused]] static double bps_to_mbps(uint64_t bytes_per_sec) { return (double)bytes_per_sec * 8.0 / 1e6; }

// 读取 fd 的 TCP_INFO 并填入 *s。成功 0，失败 -1。
static int read_tcp_info(int fd, tcp_sample *s) {
    // TODO: struct tcp_info ti = {}; socklen_t len = sizeof ti;
    //       getsockopt(fd, IPPROTO_TCP, TCP_INFO, &ti, &len)，失败返回 -1；
    //       然后把 tcpi_rtt、tcpi_snd_cwnd、tcpi_total_retrans、tcpi_delivery_rate、tcpi_pacing_rate、
    //       tcpi_bytes_acked 填进 *s（两个速率是 字节/秒，用 bps_to_mbps 换算；
    //       pacing_rate == UINT64_MAX 表示"不限速"，记为 0）。
    (void)fd;
    *s = (tcp_sample){}; // 占位：全是 0
    return 0;
}

// goodput：对端确认的字节数 / 经过的秒数，单位 Mbit/s。
static double goodput_mbps(uint64_t bytes_acked, double seconds) {
    // TODO: bytes_acked * 8 / seconds / 1e6（seconds <= 0 时返回 0）。
    //       想一想：为什么不能用"write 返回的字节总数"来算？
    (void)bytes_acked, (void)seconds;
    return 0;
}

// ---------------------------------------------------------------------------------------------
// 脚手架
// ---------------------------------------------------------------------------------------------
static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

static int dial(const char *host, const char *port) {
    struct addrinfo hints = {.ai_family = AF_INET, .ai_socktype = SOCK_STREAM};
    struct addrinfo *res = nullptr;
    int rc = getaddrinfo(host, port, &hints, &res);
    if (rc != 0) {
        fprintf(stderr, "getaddrinfo %s: %s\n", host, gai_strerror(rc));
        exit(1);
    }
    int fd = socket(res->ai_family, res->ai_socktype | SOCK_CLOEXEC, res->ai_protocol);
    if (fd < 0)
        sl_die("socket");
    if (connect(fd, res->ai_addr, res->ai_addrlen) < 0)
        sl_die("connect");
    freeaddrinfo(res);
    return fd;
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
            break; // EOF 或错误（例如对端 RST）
        }
        close(cfd);
        printf("received %llu\n", (unsigned long long)total);
    }
}

static int run_client(const char *host, const char *port, double seconds) {
    int fd = dial(host, port);
    int fl = fcntl(fd, F_GETFL);
    if (fl < 0 || fcntl(fd, F_SETFL, fl | O_NONBLOCK) < 0)
        sl_die("fcntl O_NONBLOCK");

    char *chunk = calloc(1, CHUNK);
    if (chunk == nullptr)
        sl_die("calloc");
    double t0 = now_s(), next = t0 + SAMPLE_MS / 1000.0, end = t0 + seconds;
    tcp_sample s = {};
    for (;;) {
        double t = now_s();
        if (t >= next) {
            if (read_tcp_info(fd, &s) < 0)
                sl_die("getsockopt TCP_INFO");
            printf("t=%.2f rtt_us=%u cwnd=%u retrans=%u delivery_mbps=%.2f pacing_mbps=%.2f acked=%llu\n",
                   t - t0, s.rtt_us, s.cwnd, s.total_retrans, s.delivery_mbps, s.pacing_mbps,
                   (unsigned long long)s.bytes_acked);
            next += SAMPLE_MS / 1000.0;
        }
        if (t >= end)
            break;
        double until = (next < end ? next : end) - t;
        int wait_ms = until > 0 ? (int)(until * 1000) + 1 : 0;
        struct pollfd pfd = {.fd = fd, .events = POLLOUT};
        int pr = poll(&pfd, 1, wait_ms);
        if (pr < 0 && errno != EINTR)
            sl_die("poll");
        if (pr > 0) {
            ssize_t w = write(fd, chunk, CHUNK);
            if (w < 0 && errno != EAGAIN && errno != EINTR)
                sl_die("write");
        }
    }
    double elapsed = now_s() - t0;
    if (read_tcp_info(fd, &s) < 0)
        sl_die("getsockopt TCP_INFO");
    printf("goodput_mbps=%.2f retrans=%u\n", goodput_mbps(s.bytes_acked, elapsed), s.total_retrans);
    free(chunk);
    close(fd);
    return 0;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 3 && strcmp(argv[1], "server") == 0)
        return run_server(atoi(argv[2]));
    if (argc == 5 && strcmp(argv[1], "client") == 0) {
        double secs = atof(argv[4]);
        if (secs <= 0) {
            fprintf(stderr, "SECONDS must be positive\n");
            return 2;
        }
        return run_client(argv[2], argv[3], secs);
    }
    fprintf(stderr, "usage: %s server PORT | client HOST PORT SECONDS\n", argv[0]);
    return 2;
}
