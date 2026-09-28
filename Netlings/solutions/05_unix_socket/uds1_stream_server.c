// EXERCISE: uds1_stream_server — Unix domain stream socket 回显服务器：路径名与抽象命名空间
// TOPIC: AF_UNIX SOCK_STREAM / sockaddr_un / 陈旧 socket 文件 / 抽象地址
// DIFFICULTY: ★★☆☆☆
// BOOK: UNP §15.1-15.4；man 7 unix（Abstract sockets 一节）
//
// 说明：
//   用法：uds1_stream_server PATH
//     PATH 以 '@' 开头时使用 Linux 抽象命名空间（例如 @netlings-echo），否则是文件系统路径。
//   服务器 bind + listen 后打印 "listening on PATH"，然后逐个 accept 连接并原样回显，直到对端关闭。
//   收到 SIGTERM 时优雅退出：关闭监听 socket，删除 socket 文件，打印 "bye"，exit 0。
//
//   三个坑（探针都会检查）：
//   1. 陈旧 socket 文件：上一次运行崩溃（kill -9、OOM）后 socket 文件还在，再 bind 会 EADDRINUSE。
//      所以 bind 前要先 unlink(PATH)（ENOENT 可以忽略）。systemd、containerd、docker 都这么做。
//   2. 优雅退出时要 unlink 自己的 socket 文件，否则会留下垃圾，客户端 connect 得到 ECONNREFUSED。
//   3. 抽象地址：sun_path[0] = '\0'，名字放在 sun_path[1..]，没有文件，进程退出后内核自动回收
//      （Chrome、D-Bus、Android 的 @xxx socket 都是这种）。关键：addrlen 必须精确等于
//      offsetof(struct sockaddr_un, sun_path) + 1 + strlen(name)，因为抽象名字里 '\0' 也是有效字节，
//      用 sizeof(struct sockaddr_un) 会把后面一串 '\0' 也当成名字的一部分，别人就连不上了。
//
//   现代基础设施里的 UDS：/var/run/docker.sock、/run/containerd/containerd.sock、
//   PostgreSQL 的 /var/run/postgresql/.s.PGSQL.5432、nginx → php-fpm / gunicorn 的 upstream、
//   Redis 的 unixsocket 配置 —— 同机通信比 TCP loopback 更快，而且可以用文件权限做访问控制。

#include <errno.h>
#include <poll.h>
#include <signal.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#include "sl.h"

static volatile sig_atomic_t g_stop = 0;

static void on_term(int sig) {
    (void)sig;
    g_stop = 1;
}

// 把 PATH 填进 sockaddr_un，返回应当传给 bind/connect 的 addrlen；名字太长返回 0。
static socklen_t make_addr(const char *path, struct sockaddr_un *sa) {
    memset(sa, 0, sizeof(*sa));
    sa->sun_family = AF_UNIX;
    size_t base = offsetof(struct sockaddr_un, sun_path);
    if (path[0] == '@') {
        // 抽象命名空间：sun_path[0] = '\0'，名字紧跟其后，addrlen 精确到名字末尾
        size_t n = strlen(path + 1);
        if (n + 1 > sizeof(sa->sun_path))
            return 0;
        sa->sun_path[0] = '\0';
        memcpy(sa->sun_path + 1, path + 1, n);
        return (socklen_t)(base + 1 + n);
    }
    size_t n = strlen(path);
    if (n + 1 > sizeof(sa->sun_path)) // 路径名要留一个结尾 '\0'（通常上限 107 字节）
        return 0;
    memcpy(sa->sun_path, path, n + 1);
    return (socklen_t)(base + n + 1);
}

// 回显一个连接直到对端关闭（SIGTERM 此时被屏蔽，会在下一次 ppoll 时送达）
static void echo_conn(int fd) {
    char buf[4096];
    for (;;) {
        ssize_t r = read(fd, buf, sizeof buf);
        if (r == 0)
            return;
        if (r < 0) {
            if (errno == EINTR)
                continue;
            perror("read");
            return;
        }
        for (ssize_t off = 0; off < r;) {
            ssize_t w = write(fd, buf + off, (size_t)(r - off));
            if (w < 0) {
                if (errno == EINTR)
                    continue;
                perror("write");
                return;
            }
            off += w;
        }
    }
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PATH|@abstract\n", argv[0]);
        return 2;
    }
    const char *path = argv[1];
    bool abstract = path[0] == '@';

    // SIGTERM/SIGINT 平时屏蔽，只在 ppoll 等待新连接时放开 —— 这样"检查 g_stop"与"进入睡眠"
    // 之间没有竞态窗口（信号要么已经处理过，要么正好把 ppoll 唤醒成 EINTR）
    struct sigaction sa_term = {.sa_handler = on_term};
    sigemptyset(&sa_term.sa_mask);
    if (sigaction(SIGTERM, &sa_term, nullptr) < 0 || sigaction(SIGINT, &sa_term, nullptr) < 0)
        sl_die("sigaction");
    sigset_t block, waitmask;
    sigemptyset(&block);
    sigaddset(&block, SIGTERM);
    sigaddset(&block, SIGINT);
    if (sigprocmask(SIG_BLOCK, &block, &waitmask) < 0)
        sl_die("sigprocmask");
    signal(SIGPIPE, SIG_IGN); // 客户端提前关闭时 write 返回 EPIPE 而不是杀死服务器

    struct sockaddr_un sa;
    socklen_t len = make_addr(path, &sa);
    if (len == 0) {
        fprintf(stderr, "uds1_stream_server: name too long: %s\n", path);
        return 2;
    }

    int lfd = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (lfd < 0)
        sl_die("socket");

    // 删除上次崩溃留下的陈旧 socket 文件（抽象地址没有文件，不需要）
    if (!abstract && unlink(path) < 0 && errno != ENOENT)
        sl_die("unlink");

    if (bind(lfd, (struct sockaddr *)&sa, len) < 0)
        sl_die("bind");
    if (listen(lfd, 64) < 0)
        sl_die("listen");
    printf("listening on %s\n", path);

    while (!g_stop) {
        struct pollfd pfd = {.fd = lfd, .events = POLLIN};
        int n = ppoll(&pfd, 1, nullptr, &waitmask);
        if (n < 0) {
            if (errno == EINTR)
                continue; // 多半是 SIGTERM，回到 while 检查 g_stop
            sl_die("ppoll");
        }
        int cfd = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
        if (cfd < 0) {
            if (errno == EINTR || errno == ECONNABORTED)
                continue;
            sl_die("accept4");
        }
        echo_conn(cfd);
        close(cfd);
    }

    close(lfd);
    // 优雅退出：删除自己的 socket 文件
    if (!abstract && unlink(path) < 0)
        perror("unlink");
    printf("bye\n");
    return 0;
}
