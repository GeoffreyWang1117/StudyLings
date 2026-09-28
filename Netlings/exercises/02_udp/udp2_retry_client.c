// EXERCISE: udp2_retry_client — 像 DNS 解析器那样用 UDP：connect 过的 socket、超时与重传
// TOPIC: 已连接 UDP socket / ICMP port unreachable → ECONNREFUSED / poll 超时 / 重传
// DIFFICULTY: ★★★☆☆
// BOOK: UNP §8.9（服务器未运行）、§8.11（UDP 的 connect）、§14.2（超时）、§22.5（可靠性：超时重传）；man 7 udp
// I AM NOT DONE
//
// 说明：
//   用法：udp2_retry_client HOST PORT MESSAGE
//   向 HOST:PORT 发送一个数据报 MESSAGE，等待回复最多 300ms；没等到就重发，最多发送 3 次。
//   - 收到回复：打印回复内容并换行，exit 0
//   - 对方端口没人监听（内核回 ICMP port unreachable）：打印 "refused"，exit 2
//   - 3 次都没回复：打印 "timeout"，exit 3
//
//   要点：
//   1. UDP 不可靠：丢包了没人告诉你，客户端必须自己超时 + 重传。glibc 的 stub resolver
//      （/etc/resolv.conf 的 timeout:/attempts:）、Go 的 DNS 客户端、c-ares（Node.js/curl 用它）都这么做。
//   2. 未 connect 的 UDP socket 收不到 ICMP 错误：内核不知道该把错误交给谁（UNP §8.9 的"异步错误"）。
//      对 UDP socket 调 connect() 不会发任何包，只是记下默认对端，之后：可以用 send/recv；
//      只收这个对端的数据报；ICMP port unreachable 会以 ECONNREFUSED 的形式从下一次 recv/send 报告。
//      这样"服务器没开"能在几毫秒内得知，而不是傻等所有重传超时。
//   3. 等待用 poll(POLLIN, 300)（或 SO_RCVTIMEO）。有待处理的 socket 错误时 poll 会返回 POLLERR，
//      这时调用 recv 就会拿到 ECONNREFUSED。
//
//   探针会检查：没人监听 → refused；前 2 个数据报被故意忽略的服务器 → 重传后拿到回复（恰好发 3 次）；
//   从不回复的服务器 → timeout（恰好发 3 次，总耗时约 0.9 秒）。

#include <errno.h>
#include <netdb.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_TRIES = 3, TIMEOUT_MS = 300 };

static int refused(void) {
    puts("refused");
    return 2;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s HOST PORT MESSAGE\n", argv[0]);
        return 1;
    }
    const char *msg = argv[3];
    size_t mlen = strlen(msg);

    struct addrinfo hints = {.ai_family = AF_UNSPEC, .ai_socktype = SOCK_DGRAM};
    struct addrinfo *res = nullptr;
    int rc = getaddrinfo(argv[1], argv[2], &hints, &res);
    if (rc != 0) {
        fprintf(stderr, "udp2_retry_client: getaddrinfo: %s\n", gai_strerror(rc));
        return 1;
    }
    int fd = socket(res->ai_family, res->ai_socktype | SOCK_CLOEXEC, res->ai_protocol);
    if (fd < 0)
        sl_die("socket");

    // TODO: connect() 这个 UDP socket，之后用 send/recv；这样 ICMP 错误才会以 ECONNREFUSED 报告给我们。
    //       现在用的是 sendto 到 res->ai_addr（未连接的 socket 永远收不到 ECONNREFUSED）。

    static char buf[65536];
    // TODO: 最多发送 MAX_TRIES 次，每次等待 TIMEOUT_MS 毫秒。
    for (int attempt = 0; attempt < 1; attempt++) { // BUG: 只发一次，丢一个包就失败
        if (sendto(fd, msg, mlen, 0, res->ai_addr, res->ai_addrlen) < 0) {
            if (errno == ECONNREFUSED) { // 上一次的 ICMP 错误也可能在 send 时报告
                close(fd);
                freeaddrinfo(res);
                return refused();
            }
            sl_die("send");
        }

        struct pollfd pfd = {.fd = fd, .events = POLLIN};
        int n;
        do {
            n = poll(&pfd, 1, TIMEOUT_MS);
        } while (n < 0 && errno == EINTR);
        if (n < 0)
            sl_die("poll");
        if (n == 0)
            continue; // 超时：重传

        ssize_t r = recv(fd, buf, sizeof buf, 0);
        if (r < 0) {
            if (errno == ECONNREFUSED) {
                close(fd);
                freeaddrinfo(res);
                return refused();
            }
            sl_die("recv");
        }
        printf("%.*s\n", (int)r, buf);
        close(fd);
        freeaddrinfo(res);
        return 0;
    }
    close(fd);
    freeaddrinfo(res);
    puts("timeout");
    return 3;
}
