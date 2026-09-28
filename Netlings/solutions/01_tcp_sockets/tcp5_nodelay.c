// EXERCISE: tcp5_nodelay — 复现 Nagle + 延迟 ACK 的 "写-写-读" 40ms 卡顿，用 TCP_NODELAY 消除
// TOPIC: setsockopt(TCP_NODELAY) / Nagle 算法 / delayed ACK / 请求-响应延迟
// DIFFICULTY: ★★☆☆☆
// BOOK: UNP §7.9（TCP_NODELAY）；TCP/IP Illustrated Vol.1 §15.4（Nagle 与延迟 ACK 的交互）；man 7 tcp
//
// 说明：
//   用法：tcp5_nodelay HOST PORT ROUNDS
//   做 ROUNDS 轮请求-响应：每轮先 write 4 字节大端长度头，再单独 write 一个小 body，
//   然后等服务器回 1 字节。最后打印 "avg_ms=<每轮平均毫秒数>"。
//
//   现象（先别改代码，自己跑一遍看看）：在 Linux loopback 上每轮大约 40ms！
//   原因：Nagle 算法规定"网络上已有未被确认的小段时，新的小段先攒着不发"。
//     第一次 write（头）立即发出；第二次 write（body）因为头还没被 ACK，被 Nagle 扣住；
//     服务器收到头后在等 body，没有数据要回，于是走延迟 ACK（Linux 最少 ~40ms）才发 ACK；
//     ACK 到了 body 才发出 —— 每轮白等一个延迟 ACK 定时器。
//   修法（任选其一，探针只测延迟）：
//     a) setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one) —— 本练习的 TODO；
//     b) 把头和 body 拼成一次 write，或用 writev 一次交给内核（更好：还少一次系统调用）。
//   现代软件几乎都默认关闭 Nagle：Go 的 net.TCPConn 默认 SetNoDelay(true)，Node.js 18+ 默认
//   noDelay，nginx 的 `tcp_nodelay on;`（默认开），Redis、gRPC、Envoy 都设置 TCP_NODELAY，
//   tokio 需要显式 set_nodelay(true)。
//
//   探针：一个 Python 服务器先读 4 字节头、再读 body、再回 1 字节；跑 30 轮，
//   要求 avg_ms < 10（修好后通常远小于 1ms）。

#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

// 脚手架：与 tcp1_client 相同的 getaddrinfo + 逐个地址尝试。
static int dial(const char *host, const char *port) {
    struct addrinfo hints = {.ai_family = AF_UNSPEC, .ai_socktype = SOCK_STREAM};
    struct addrinfo *res = nullptr;
    int rc = getaddrinfo(host, port, &hints, &res);
    if (rc != 0) {
        fprintf(stderr, "tcp5_nodelay: getaddrinfo %s: %s\n", host, gai_strerror(rc));
        exit(1);
    }
    int fd = -1, last_err = EHOSTUNREACH;
    for (struct addrinfo *ai = res; ai != nullptr; ai = ai->ai_next) {
        fd = socket(ai->ai_family, ai->ai_socktype | SOCK_CLOEXEC, ai->ai_protocol);
        if (fd < 0) {
            last_err = errno;
            continue;
        }
        if (connect(fd, ai->ai_addr, ai->ai_addrlen) == 0)
            break;
        last_err = errno;
        close(fd);
        fd = -1;
    }
    freeaddrinfo(res);
    if (fd < 0)
        errno = last_err;
    return fd;
}

static int write_all(int fd, const void *buf, size_t n) {
    const char *p = buf;
    while (n > 0) {
        ssize_t w = write(fd, p, n);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        p += w;
        n -= (size_t)w;
    }
    return 0;
}

static double now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1e3 + (double)ts.tv_nsec / 1e6;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s HOST PORT ROUNDS\n", argv[0]);
        return 2;
    }
    int rounds = atoi(argv[3]);
    if (rounds <= 0) {
        fprintf(stderr, "tcp5_nodelay: ROUNDS must be positive\n");
        return 2;
    }
    int fd = dial(argv[1], argv[2]);
    if (fd < 0) {
        fprintf(stderr, "tcp5_nodelay: connect %s:%s: %s\n", argv[1], argv[2], strerror(errno));
        return 1;
    }

    // TODO: 关闭 Nagle 算法：setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, ...)。
    //       （或者把下面的两次 write 合并成一次 / writev —— 探针只测延迟。）
    int one = 1;
    if (setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one) < 0)
        sl_die("setsockopt TCP_NODELAY");

    static const char body[] = "GET /tiny/request/body HTTP/9";
    static_assert(sizeof body - 1 < 256, "body must stay a small segment");
    uint32_t be_len = htonl((uint32_t)(sizeof body - 1));

    double total = 0;
    for (int i = 0; i < rounds; i++) {
        double t0 = now_ms();
        if (write_all(fd, &be_len, sizeof be_len) < 0) // 第一次小写：头
            sl_die("write header");
        if (write_all(fd, body, sizeof body - 1) < 0) // 第二次小写：body
            sl_die("write body");
        char reply;
        ssize_t r;
        do {
            r = read(fd, &reply, 1);
        } while (r < 0 && errno == EINTR);
        if (r < 0)
            sl_die("read");
        if (r == 0) {
            fprintf(stderr, "tcp5_nodelay: server closed the connection\n");
            return 1;
        }
        total += now_ms() - t0;
    }
    close(fd);
    printf("avg_ms=%.3f\n", total / rounds);
    return 0;
}
