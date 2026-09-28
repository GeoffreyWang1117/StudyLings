// EXERCISE: epoll4_backpressure — 写不进去时不阻塞：输出缓冲 + EPOLLOUT + 背压
// TOPIC: 非阻塞 write / EAGAIN / EPOLLOUT 的开与关 / EPOLL_CTL_MOD / 高水位线
// DIFFICULTY: ★★★★☆
// BOOK: man 7 epoll；man 7 tcp（SO_SNDBUF）；modern Linux notes
// I AM NOT DONE
//
// 说明：
//   用法：epoll4_backpressure PORT      监听 127.0.0.1:PORT，打印 "listening on port N"
//   - LT 模式 echo 服务器，但要正确处理"对端不读"的情况：
//     * 读到数据后尽量直接写回；写不完（短写或 EAGAIN）的部分追加到该连接的输出缓冲区，
//       并为该连接打开 EPOLLOUT
//     * EPOLLOUT 就绪 → 继续写输出缓冲区；写空后【关掉】EPOLLOUT（LT 下 socket 几乎总是可写，
//       不关的话 epoll_wait 会不停返回 → 空转）
//     * 背压：某连接待发送数据 > HIGH_WATER（1 MiB）时【关掉】它的 EPOLLIN，不再从它读；
//       降回 HIGH_WATER 以下再打开。否则一个只发不收的客户端能把服务器内存吃光
//   - 用 update_interest() 根据缓冲区状态算出应有的事件集合，变化时 EPOLL_CTL_MOD
//   - 测试：客户端 A 发 8 MiB 但不读；同时客户端 B 发一小段，必须在几秒内收到回显；
//     之后 A 把 8 MiB 全读回来且内容一致。另有一个 64 MiB 的用例检查服务器内存不会随之膨胀
//
//   这就是所有事件驱动服务器里的 "write queue"：Node.js 的 socket.write() 返回 false 与
//   'drain' 事件、libuv 的 uv_write 队列、Redis 的 client-output-buffer-limit、
//   nginx 的 ngx_http_write_filter + 发送缓冲、tokio 的 AsyncWrite 返回 Poll::Pending，
//   说的都是同一件事：永远不要在事件循环里阻塞等一个慢客户端。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_EVENTS = 64, READ_CHUNK = 64 * 1024 };
static const size_t HIGH_WATER = 1024 * 1024;

struct conn {
    int fd;
    uint32_t events; // 当前在 epoll 里注册的事件集合
    char *out;       // 待发送数据：out[off .. len)
    size_t off, len, cap;
};

static int epfd;

static size_t pending(const struct conn *c) {
    return c->len - c->off;
}

// 把 data 追加到输出缓冲区（先把已发送的部分挪走，不够再扩容）
[[maybe_unused]] static void out_append(struct conn *c, const char *data, size_t n) {
    if (c->off > 0) {
        memmove(c->out, c->out + c->off, pending(c));
        c->len -= c->off;
        c->off = 0;
    }
    if (c->len + n > c->cap) {
        size_t cap = c->cap ? c->cap : READ_CHUNK;
        while (cap < c->len + n)
            cap *= 2;
        char *p = realloc(c->out, cap);
        if (!p)
            sl_die("realloc");
        c->out = p;
        c->cap = cap;
    }
    memcpy(c->out + c->len, data, n);
    c->len += n;
}

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

static void close_conn(struct conn *c) {
    if (epoll_ctl(epfd, EPOLL_CTL_DEL, c->fd, nullptr) < 0)
        perror("epoll_ctl DEL");
    close(c->fd);
    free(c->out);
    free(c);
}

static void on_accept(int lfd) {
    for (;;) {
        int cfd = accept4(lfd, nullptr, nullptr, SOCK_NONBLOCK | SOCK_CLOEXEC);
        if (cfd < 0) {
            if (errno == EINTR || errno == ECONNABORTED)
                continue;
            if (errno != EAGAIN)
                perror("accept4");
            return;
        }
        struct conn *c = calloc(1, sizeof *c);
        if (!c)
            sl_die("calloc");
        c->fd = cfd;
        c->events = EPOLLIN;
        struct epoll_event ev = {.events = c->events, .data.ptr = c};
        if (epoll_ctl(epfd, EPOLL_CTL_ADD, cfd, &ev) < 0) {
            perror("epoll_ctl ADD");
            close(cfd);
            free(c);
        }
    }
}

// 根据缓冲区状态决定关心哪些事件：
//   待发送 <= HIGH_WATER → EPOLLIN（还能接着读）；待发送 > 0 → EPOLLOUT（等可写再发）
// 与当前注册的不同才 EPOLL_CTL_MOD（系统调用不便宜）
static void update_interest(struct conn *c) {
    // TODO: 按上面的规则算出 want；want != c->events 时
    //       epoll_ctl(epfd, EPOLL_CTL_MOD, c->fd, &(struct epoll_event){.events = want, .data.ptr = c})，
    //       失败 sl_die，成功后更新 c->events
    (void)c;
    (void)HIGH_WATER;
}

// 尽量把输出缓冲区写出去。返回 false 表示连接出错应关闭
static bool flush_out(struct conn *c) {
    // TODO: 循环 write(c->fd, c->out + c->off, pending(c))，每次 c->off += w：
    //       EINTR → 重试；EAGAIN → 停下（留给下次 EPOLLOUT）；其他错误 → return false。
    //       缓冲区写空后把 off、len 都归零
    (void)pending;
    return true;
}

// 读一块，写回。返回 false 表示应关闭
static bool on_readable(struct conn *c) {
    char buf[READ_CHUNK];
    ssize_t n = read(c->fd, buf, sizeof buf);
    if (n < 0)
        return errno == EAGAIN || errno == EINTR;
    if (n == 0)
        return false;
    // BUG: "阻塞式"写法：对端不读时 write 一直返回 EAGAIN，这里就原地空转，
    //      整个事件循环卡死在这一个慢客户端上，其他客户端全部饿死。
    // TODO: 改成 out_append(c, buf, n) 然后 return flush_out(c)；
    //       写不完的留在缓冲区里，main 循环会调用 update_interest 打开 EPOLLOUT
    size_t off = 0;
    while (off < (size_t)n) {
        ssize_t w = write(c->fd, buf + off, (size_t)n - off);
        if (w < 0) {
            if (errno == EAGAIN || errno == EINTR)
                continue;
            return false;
        }
        off += (size_t)w;
    }
    return true;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    signal(SIGPIPE, SIG_IGN);

    int lfd = listen_on(atoi(argv[1]));
    epfd = epoll_create1(EPOLL_CLOEXEC);
    if (epfd < 0)
        sl_die("epoll_create1");
    struct epoll_event lev = {.events = EPOLLIN, .data.ptr = nullptr}; // ptr == nullptr 表示监听 socket
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
            struct conn *c = events[i].data.ptr;
            if (!c) {
                on_accept(lfd);
                continue;
            }
            uint32_t re = events[i].events;
            bool ok = true;
            if (re & EPOLLOUT)
                ok = flush_out(c);
            if (ok && (re & (EPOLLIN | EPOLLHUP | EPOLLERR)))
                ok = on_readable(c);
            if (ok)
                update_interest(c);
            else
                close_conn(c);
        }
    }
}
