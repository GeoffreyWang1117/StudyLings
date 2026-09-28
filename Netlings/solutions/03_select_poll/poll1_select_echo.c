// EXERCISE: poll1_select_echo — 用 select(2) 写单线程多客户端 echo 服务器
// TOPIC: I/O 多路复用：select / fd_set / FD_SETSIZE
// DIFFICULTY: ★★☆☆☆
// BOOK: UNP §6.3, §6.8 (select, str_cli/tcpservselect)；man 2 select
//
// 说明：
//   用法：poll1_select_echo PORT      监听 127.0.0.1:PORT，打印 "listening on port N"
//   - 一个线程、一个循环，同时服务所有客户端：客户端发来什么就原样发回什么
//   - 核心：每轮循环都要"重建" fd_set —— select 返回时会把没就绪的位清掉（值-结果参数）
//   - 只对 FD_ISSET 为真的 fd 调用 read/accept，这样 read 一定不会阻塞；
//     一个"只连不说话"的客户端绝不能卡住别人（迭代服务器就会卡住）
//   - read 返回 0（对端关闭）或出错：close 并从客户端表中移除
//   - 测试：先连一个沉默的客户端，再让 20 个客户端并发、交错地发多条消息，每条都必须原样回来
//
//   为什么 select 算"遗留"但仍到处可见：fd_set 是固定大小的位图，FD_SETSIZE = 1024，
//   fd >= 1024 时 FD_SET 直接越界写内存（glibc 的 _FORTIFY_SOURCE 会 abort）；每次调用
//   都要把整个位图拷进内核、内核再线性扫描 0..maxfd，O(maxfd)。所以 nginx/Redis/libuv 在
//   Linux 上都用 epoll（第 04 章）。但 select 是 POSIX 里最可移植的接口：Python 的
//   selectors 兜底实现、很多嵌入式/老代码、Windows 的 Winsock 都还在用它，必须读得懂。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_CLIENTS = 64 };

static int clients[MAX_CLIENTS]; // -1 表示空槽

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

// 把 buf[0..n) 全部写出去（阻塞 socket 上 write 也可能短写）
static int write_all(int fd, const char *buf, size_t n) {
    while (n > 0) {
        ssize_t w = write(fd, buf, n);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        buf += w;
        n -= (size_t)w;
    }
    return 0;
}

static void add_client(int cfd) {
    // fd_set 只能表示 0..FD_SETSIZE-1，超出就不能交给 select
    if (cfd >= FD_SETSIZE) {
        fprintf(stderr, "fd %d >= FD_SETSIZE, rejecting\n", cfd);
        close(cfd);
        return;
    }
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (clients[i] < 0) {
            clients[i] = cfd;
            return;
        }
    }
    fprintf(stderr, "too many clients, rejecting fd %d\n", cfd);
    close(cfd);
}

// 处理一个可读的客户端。返回 false 表示应该关闭它
static bool echo_once(int cfd) {
    char buf[4096];
    ssize_t n = read(cfd, buf, sizeof buf);
    if (n < 0 && errno == EINTR)
        return true;
    if (n <= 0)
        return false;
    return write_all(cfd, buf, (size_t)n) == 0;
}

static void serve(int lfd) {
    for (;;) {
        // 每轮都重建：select 会改写传入的 fd_set
        fd_set rset;
        FD_ZERO(&rset);
        FD_SET(lfd, &rset);
        int maxfd = lfd;
        for (int i = 0; i < MAX_CLIENTS; i++) {
            if (clients[i] >= 0) {
                FD_SET(clients[i], &rset);
                if (clients[i] > maxfd)
                    maxfd = clients[i];
            }
        }

        int nready = select(maxfd + 1, &rset, nullptr, nullptr, nullptr);
        if (nready < 0) {
            if (errno == EINTR)
                continue;
            sl_die("select");
        }

        if (FD_ISSET(lfd, &rset)) {
            int cfd = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
            if (cfd >= 0)
                add_client(cfd);
            else if (errno != EINTR && errno != ECONNABORTED)
                perror("accept4");
        }

        for (int i = 0; i < MAX_CLIENTS; i++) {
            int cfd = clients[i];
            if (cfd >= 0 && FD_ISSET(cfd, &rset) && !echo_once(cfd)) {
                close(cfd);
                clients[i] = -1;
            }
        }
    }
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    signal(SIGPIPE, SIG_IGN); // 对端已关闭时 write 返回 EPIPE，而不是把整个服务器杀掉
    for (int i = 0; i < MAX_CLIENTS; i++)
        clients[i] = -1;

    int lfd = listen_on(atoi(argv[1]));
    printf("listening on port %s\n", argv[1]);
    serve(lfd);
}
