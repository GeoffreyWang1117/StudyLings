// EXERCISE: poll2_chat — 用 poll(2) 写一个多人聊天室（广播给其他人）
// TOPIC: I/O 多路复用：poll / struct pollfd / POLLHUP / 连接的增删
// DIFFICULTY: ★★★☆☆
// BOOK: UNP §6.10-6.11 (poll, tcpservpoll)；man 2 poll
//
// 说明：
//   用法：poll2_chat PORT      监听 127.0.0.1:PORT，打印 "listening on port N"
//   - 每个新连接分配一个递增编号 id（从 1 开始），服务器先给它发一行 "hello <id>"，
//     并在 stdout 打印 "join <id>"（这些已经写好）
//   - 客户端每发来一整行 <line>，就把 "<id>: <line>\n" 发给【除发送者以外】的所有在线客户端
//   - 客户端断开（read 返回 0、出错，或 revents 里有 POLLHUP/POLLERR）：close 它，
//     并把它从 pollfd 数组里【删掉】（和最后一个元素交换即可），打印 "leave <id>"
//   - 测试：3 个客户端互发消息，确认发送者收不到自己的消息；然后一个客户端断开，
//     其余两个还能继续聊，且服务器不会因为残留的 fd 而 100% CPU 空转
//
//   poll 相比 select：没有 FD_SETSIZE 上限，events/revents 分开所以不用每轮重建；
//   但每次调用仍要把整个数组拷进内核并线性扫描 —— O(n)。libuv 在不支持 epoll/kqueue 的平台、
//   OpenSSH、systemd 的很多小工具、Go 以外的大量 CLI 都还在用 poll。
//   "连接关闭后没把 fd 从监听集合中删掉"是事件循环里最经典的 bug：
//   已关闭（或 EOF）的 fd 会一直报告就绪，事件循环就变成了 busy loop。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_CONNS = 64, LINE_MAX_LEN = 1024 };

// pfds[0] 是监听 socket；pfds[1..nfds) 是客户端，conns[i] 与 pfds[i] 一一对应
struct conn {
    int id;
    size_t len;              // inbuf 中已积累、还没凑成整行的字节数
    char inbuf[LINE_MAX_LEN];
};

static struct pollfd pfds[MAX_CONNS + 1];
static struct conn conns[MAX_CONNS + 1];
static nfds_t nfds = 0;
static int next_id = 1;

static int listen_on(int port) {
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
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

// MSG_NOSIGNAL：对端已关闭时返回 EPIPE 而不是用 SIGPIPE 杀掉整个服务器
static void send_all(int fd, const char *buf, size_t n) {
    while (n > 0) {
        ssize_t w = send(fd, buf, n, MSG_NOSIGNAL);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            return; // 发送失败的连接会在它自己的 POLLHUP/read==0 时被清理
        }
        buf += w;
        n -= (size_t)w;
    }
}

static void add_conn(int cfd) {
    if (nfds == MAX_CONNS + 1) {
        close(cfd);
        return;
    }
    pfds[nfds] = (struct pollfd){.fd = cfd, .events = POLLIN};
    conns[nfds] = (struct conn){.id = next_id++};
    char hello[32];
    int n = snprintf(hello, sizeof hello, "hello %d\n", conns[nfds].id);
    send_all(cfd, hello, (size_t)n);
    printf("join %d\n", conns[nfds].id);
    nfds++;
}

// 把 "<id>: <line>\n" 发给除 pfds[from] 以外的所有客户端
static void broadcast(nfds_t from, const char *line, size_t len) {
    char msg[LINE_MAX_LEN + 32];
    int n = snprintf(msg, sizeof msg, "%d: %.*s\n", conns[from].id, (int)len, line);
    for (nfds_t i = 1; i < nfds; i++) {
        if (i == from)
            continue;
        send_all(pfds[i].fd, msg, (size_t)n);
    }
}

// 关闭 pfds[i]：用最后一个元素填补空位，数组保持紧凑
static void remove_conn(nfds_t i) {
    printf("leave %d\n", conns[i].id);
    close(pfds[i].fd);
    nfds--;
    pfds[i] = pfds[nfds];
    conns[i] = conns[nfds];
}

// 读一次，把完整的行广播出去。返回 false 表示连接已关闭/出错
static bool handle_readable(nfds_t i) {
    struct conn *c = &conns[i];
    ssize_t n = read(pfds[i].fd, c->inbuf + c->len, sizeof c->inbuf - c->len);
    if (n < 0 && errno == EINTR)
        return true;
    if (n <= 0)
        return false;
    c->len += (size_t)n;

    char *start = c->inbuf;
    char *nl;
    while ((nl = memchr(start, '\n', c->len - (size_t)(start - c->inbuf))) != nullptr) {
        broadcast(i, start, (size_t)(nl - start));
        start = nl + 1;
    }
    c->len -= (size_t)(start - c->inbuf);
    memmove(c->inbuf, start, c->len);
    if (c->len == sizeof c->inbuf) { // 一行太长：直接当作一整行发出去
        broadcast(i, c->inbuf, c->len);
        c->len = 0;
    }
    return true;
}

static void serve(int lfd) {
    pfds[0] = (struct pollfd){.fd = lfd, .events = POLLIN};
    nfds = 1;
    for (;;) {
        if (poll(pfds, nfds, -1) < 0) {
            if (errno == EINTR)
                continue;
            sl_die("poll");
        }

        // 倒序遍历：remove_conn 会把最后一个元素搬到 i，倒序保证它已经处理过
        for (nfds_t i = nfds - 1; i >= 1; i--) {
            short re = pfds[i].revents;
            if ((re & (POLLIN | POLLHUP | POLLERR)) && !handle_readable(i))
                remove_conn(i);
        }

        if (pfds[0].revents & POLLIN) {
            int cfd = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
            if (cfd >= 0)
                add_conn(cfd);
            else if (errno != EINTR && errno != ECONNABORTED)
                perror("accept4");
        }
    }
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    int lfd = listen_on(atoi(argv[1]));
    printf("listening on port %s\n", argv[1]);
    serve(lfd);
}
