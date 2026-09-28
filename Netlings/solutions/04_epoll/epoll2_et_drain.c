// EXERCISE: epoll2_et_drain — 边沿触发（EPOLLET）：必须读到 EAGAIN 为止
// TOPIC: EPOLLET / 读空（drain）accept 与 read / EAGAIN
// DIFFICULTY: ★★★☆☆
// BOOK: man 7 epoll（"Level-triggered and edge-triggered" 与 Q&A 部分）；modern Linux notes
//
// 说明：
//   用法：epoll2_et_drain PORT      监听 127.0.0.1:PORT，打印 "listening on port N"
//   - 和 epoll1 一样是 echo 服务器，但监听 socket 与连接都以 EPOLLIN | EPOLLET 注册
//   - 边沿触发只在"状态变化"时通知一次：来了新数据/新连接的那一刻。
//     如果这次没把缓冲区读空，剩下的数据不会再触发任何通知 —— 连接从此"卡死"
//   - 所以：监听 socket 就绪时要循环 accept4 直到 EAGAIN；
//           连接就绪时要循环 read 直到 EAGAIN（read 返回 0 → 关闭）
//   - 测试 1：客户端一口气发 1 MiB，然后等完整的 1 MiB 回显
//   - 测试 2：先 SIGSTOP 冻结服务器，让 50 个连接同时在 accept 队列里排队，再 SIGCONT：
//     这 50 个连接只会产生【一次】边沿，服务器必须一次 accept 完
//
//   现实中：nginx 用 EPOLLET（ngx_epoll_module.c 里 EPOLLIN|EPOLLOUT|EPOLLET 一次注册、
//   读到 EAGAIN 为止），系统调用更少；Redis 用 LT，每次事件处理有上限、实现更简单也更公平；
//   Go netpoller 和 tokio/mio 也用 ET（mio 把 "读到 WouldBlock 为止" 写进了 API 契约）。
//   两种都对，但 ET 下"没读空"是会让连接永久挂起的 bug。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_EVENTS = 64 };

static int listen_on(int port) {
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    int one = 1;
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one) < 0)
        sl_die("setsockopt");
    struct sockaddr_in addr = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(fd, (struct sockaddr *)&addr, sizeof addr) < 0)
        sl_die("bind");
    if (listen(fd, SOMAXCONN) < 0)
        sl_die("listen");
    return fd;
}

// 把 buf 写回非阻塞 socket。简化：写满（EAGAIN）时用 poll 等它可写（最多 5s）。
// 这会暂停整个事件循环 —— 真正的服务器应缓冲并注册 EPOLLOUT，见 epoll4。
static bool write_back(int fd, const char *buf, size_t n) {
    while (n > 0) {
        ssize_t w = write(fd, buf, n);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            if (errno == EAGAIN) {
                struct pollfd pfd = {.fd = fd, .events = POLLOUT};
                if (poll(&pfd, 1, 5000) <= 0)
                    return false;
                continue;
            }
            return false;
        }
        buf += w;
        n -= (size_t)w;
    }
    return true;
}

static void close_conn(int epfd, int fd) {
    if (epoll_ctl(epfd, EPOLL_CTL_DEL, fd, nullptr) < 0)
        perror("epoll_ctl DEL");
    close(fd);
}

// 监听 socket 的一个边沿可能对应很多个排队的连接：accept 到 EAGAIN 为止
static void on_accept(int epfd, int lfd) {
    for (;;) {
        int cfd = accept4(lfd, nullptr, nullptr, SOCK_NONBLOCK | SOCK_CLOEXEC);
        if (cfd < 0) {
            if (errno == EINTR || errno == ECONNABORTED)
                continue;
            if (errno != EAGAIN)
                perror("accept4");
            return; // EAGAIN：队列已空
        }
        struct epoll_event ev = {.events = EPOLLIN | EPOLLET, .data.fd = cfd};
        if (epoll_ctl(epfd, EPOLL_CTL_ADD, cfd, &ev) < 0) {
            perror("epoll_ctl ADD");
            close(cfd);
        }
    }
}

// 一个边沿：把接收缓冲区读空（直到 EAGAIN），边读边回写
static void on_readable(int epfd, int cfd) {
    char buf[4096];
    for (;;) {
        ssize_t n = read(cfd, buf, sizeof buf);
        if (n < 0) {
            if (errno == EINTR)
                continue;
            if (errno == EAGAIN)
                return; // 读空了，等下一个边沿
            close_conn(epfd, cfd);
            return;
        }
        if (n == 0 || !write_back(cfd, buf, (size_t)n)) {
            close_conn(epfd, cfd);
            return;
        }
    }
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    signal(SIGPIPE, SIG_IGN);

    int lfd = listen_on(atoi(argv[1]));
    int epfd = epoll_create1(EPOLL_CLOEXEC);
    if (epfd < 0)
        sl_die("epoll_create1");
    struct epoll_event lev = {.events = EPOLLIN | EPOLLET, .data.fd = lfd};
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, lfd, &lev) < 0)
        sl_die("epoll_ctl ADD listen");
    printf("listening on port %s\n", argv[1]);

    struct epoll_event events[MAX_EVENTS];
    for (;;) {
        int n = epoll_wait(epfd, events, MAX_EVENTS, -1);
        if (n < 0) {
            if (errno == EINTR)
                continue;
            sl_die("epoll_wait");
        }
        for (int i = 0; i < n; i++) {
            int fd = events[i].data.fd;
            if (fd == lfd)
                on_accept(epfd, lfd);
            else
                on_readable(epfd, fd);
        }
    }
}
