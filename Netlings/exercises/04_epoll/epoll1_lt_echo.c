// EXERCISE: epoll1_lt_echo — 水平触发（LT）epoll echo 服务器
// TOPIC: epoll_create1 / epoll_ctl / epoll_wait / accept4 / 非阻塞 socket
// DIFFICULTY: ★★★☆☆
// BOOK: man 7 epoll；man 2 epoll_ctl；man 2 accept4；modern Linux notes（UNP 成书时还没有 epoll）
// I AM NOT DONE
//
// 说明：
//   用法：epoll1_lt_echo PORT      监听 127.0.0.1:PORT，打印 "listening on port N"
//   - epoll_create1(EPOLL_CLOEXEC) 创建实例，监听 socket 以 EPOLLIN 注册
//   - 监听 socket 可读 → accept4(lfd, ..., SOCK_NONBLOCK | SOCK_CLOEXEC)，
//     再 EPOLL_CTL_ADD 把新连接以 EPOLLIN 加入 epoll（data.fd = 连接 fd）
//   - 连接可读 → read 一次，把读到的内容写回；read 返回 0 或出错（EAGAIN 除外）→
//     EPOLL_CTL_DEL + close
//   - 水平触发（默认）：只要 socket 缓冲区里还有数据，下一次 epoll_wait 还会报告它，
//     所以每个事件 read 一次就够了（边沿触发见 epoll2）
//   - 测试：100 个客户端并发，每个来回多条消息都要原样回显；所有客户端断开后，
//     服务器持有的 socket fd 要回落到只剩监听 socket；所有 socket / epoll fd 都应带 CLOEXEC，
//     连接 socket 应为 O_NONBLOCK（测试读 /proc/PID/fdinfo 检查）
//
//   epoll 相对 select/poll：兴趣列表常驻内核（红黑树），epoll_wait 只返回就绪的 fd，
//   复杂度与就绪数成正比而非与连接总数成正比。Redis 的 ae_epoll.c 正是 LT 模式的
//   epoll（每个事件读一次，读不完下次再来）；Node.js 的 libuv 在 Linux 上也是 epoll。
//   为什么要 CLOEXEC：服务器 fork+exec 子进程（CGI、插件、健康检查脚本）时，
//   不带 CLOEXEC 的 socket 会泄漏给子进程，连接关不掉、端口释放不了。
//   本题假设客户端读得及时；"写不进去怎么办"（EAGAIN 与背压）留到 epoll4。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
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

// 把 buf 写回非阻塞 socket。客户端不读导致写满（EAGAIN）时本题直接放弃这个连接
// （正确的做法：缓冲 + EPOLLOUT，见 epoll4）。成功返回 true
static bool write_back(int fd, const char *buf, size_t n) {
    while (n > 0) {
        ssize_t w = write(fd, buf, n);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            if (errno == EAGAIN)
                fprintf(stderr, "fd %d: peer not reading, dropping\n", fd);
            return false;
        }
        buf += w;
        n -= (size_t)w;
    }
    return true;
}

static void close_conn(int epfd, int fd) {
    // TODO: 先 EPOLL_CTL_DEL 把 fd 移出兴趣列表（失败时 perror），再 close(fd)
    //       （只 close 也会被 epoll 自动移除——前提是没有 dup 出的副本；显式 DEL 是好习惯）
}

static void on_accept(int epfd, int lfd) {
    // TODO: accept 时顺便把新 socket 设为非阻塞 + CLOEXEC —— 用 accept4 的 flags 参数
    int cfd = accept4(lfd, nullptr, nullptr, 0);
    if (cfd < 0) {
        if (errno != EAGAIN && errno != EINTR && errno != ECONNABORTED)
            perror("accept4");
        return;
    }
    // TODO: 用 EPOLL_CTL_ADD 把 cfd 以 EPOLLIN 注册进 epfd（ev.data.fd = cfd），
    //       失败时 perror 并 close(cfd)。现在新连接从没被加入 epoll，所以永远收不到它的数据
    (void)epfd;
}

static void on_readable(int epfd, int cfd) {
    char buf[16384];
    ssize_t n = read(cfd, buf, sizeof buf);
    if (n < 0 && (errno == EAGAIN || errno == EINTR))
        return; // 虚假唤醒：LT 下次还会通知
    if (n <= 0 || !write_back(cfd, buf, (size_t)n))
        close_conn(epfd, cfd);
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    signal(SIGPIPE, SIG_IGN); // 对端已关闭时 write 返回 EPIPE，而不是杀掉服务器

    int lfd = listen_on(atoi(argv[1]));
    int epfd = epoll_create1(EPOLL_CLOEXEC);
    if (epfd < 0)
        sl_die("epoll_create1");
    struct epoll_event lev = {.events = EPOLLIN, .data.fd = lfd};
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
                on_readable(epfd, fd); // EPOLLHUP/EPOLLERR 也走这里：read 会返回 0 或 -1
        }
    }
}
