// EXERCISE: sig4_signalfd_loop — 用 signalfd 把信号变成事件循环里的普通 fd
// TOPIC: sigprocmask、signalfd(2)、poll(2) 事件循环
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §10.12（sigprocmask）, §14.4.2（poll）；man 2 signalfd（Linux 2.6.22+）
//
// 说明：
//   用法：sig4_signalfd_loop
//   现代 Linux 服务器很少在异步的信号处理函数里干活，而是把信号"同步化"：
//     1. 用 sigprocmask 阻塞 SIGHUP、SIGTERM、SIGINT —— 它们不再异步递送，而是挂起（pending）
//     2. signalfd 创建一个 fd，挂起的信号可以像数据一样从这个 fd 里 read 出来
//        （每次读出一个 struct signalfd_siginfo）
//     3. 在 poll 循环里同时等 {signalfd, stdin}，信号和 I/O 在同一个地方、同一个线程里处理
//   行为：
//     - 启动后打印 ready
//     - SIGHUP  → 打印 "reload"（模拟重新加载配置）
//     - stdin 每读到一行 → 打印 "echo: <这一行>"
//     - SIGTERM / SIGINT 或 stdin EOF → 打印 "bye"，退出码 0
//   注意：必须在 **创建 signalfd 之前** 阻塞信号。signalfd 只是"读挂起信号"的另一个接口，
//   不会阻止信号按默认动作递送——没阻塞的话，SIGHUP/SIGTERM 的默认动作直接把进程杀掉。
//   测试会：发两次 SIGHUP（各得到一行 reload），写一行文本，再发 SIGTERM，要求 bye 且退出码 0。
//
//   为什么重要：`nginx -s reload` 就是给 master 进程发 SIGHUP；systemd 用 signalfd 处理所有信号；
//   libuv（Node.js）、tokio 的 signal 模块用 self-pipe 技巧做同样的事——都是为了把信号变成
//   事件循环里的一个普通事件，从而彻底避开"处理函数里只能调用异步信号安全函数"的限制。

#include <errno.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/signalfd.h>
#include <unistd.h>

#include "sl.h"

// 处理 signalfd 可读：读出一个 signalfd_siginfo 并分派。返回 true 表示应该退出
// TODO: read 一个 struct signalfd_siginfo；SIGHUP → 打印 reload；SIGTERM/SIGINT → 返回 true
static bool handle_signal(int sfd) {
    struct signalfd_siginfo si;
    ssize_t r = read(sfd, &si, sizeof si);
    if (r < 0) {
        if (errno == EINTR || errno == EAGAIN)
            return false;
        sl_die("read signalfd");
    }
    if ((size_t)r != sizeof si) {
        fprintf(stderr, "signalfd: short read\n");
        exit(1);
    }
    switch (si.ssi_signo) {
    case SIGHUP:
        puts("reload");
        return false;
    case SIGTERM:
    case SIGINT:
        return true;
    default:
        return false;
    }
}

// 行缓冲：stdin 的一次 read 可能包含半行或多行
static char g_line[4096];
static size_t g_len = 0;

// 处理 stdin 可读。返回 true 表示 EOF（应该退出）
static bool handle_stdin(void) {
    ssize_t r = read(STDIN_FILENO, g_line + g_len, sizeof g_line - 1 - g_len);
    if (r < 0) {
        if (errno == EINTR)
            return false;
        sl_die("read stdin");
    }
    if (r == 0)
        return true;
    g_len += (size_t)r;
    char *start = g_line, *nl;
    while ((nl = memchr(start, '\n', g_len - (size_t)(start - g_line))) != nullptr) {
        *nl = '\0';
        printf("echo: %s\n", start);
        start = nl + 1;
    }
    g_len -= (size_t)(start - g_line);
    memmove(g_line, start, g_len);
    if (g_len == sizeof g_line - 1) {  // 超长的一行：直接吐出去
        g_line[g_len] = '\0';
        printf("echo: %s\n", g_line);
        g_len = 0;
    }
    return false;
}

int main(void) {
    setvbuf(stdout, nullptr, _IOLBF, 0);

    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGHUP);
    sigaddset(&mask, SIGTERM);
    sigaddset(&mask, SIGINT);

    // TODO: 在创建 signalfd 之前，先用 sigprocmask 阻塞 mask 里的信号
    if (sigprocmask(SIG_BLOCK, &mask, nullptr) < 0)
        sl_die("sigprocmask");

    int sfd = signalfd(-1, &mask, SFD_CLOEXEC);
    if (sfd < 0)
        sl_die("signalfd");

    puts("ready");

    struct pollfd fds[2] = {
        {.fd = sfd, .events = POLLIN},
        {.fd = STDIN_FILENO, .events = POLLIN},
    };
    bool done = false;
    while (!done) {
        int n = poll(fds, 2, -1);
        if (n < 0) {
            if (errno == EINTR)
                continue;
            sl_die("poll");
        }
        if (fds[0].revents & POLLIN)
            done = handle_signal(sfd);
        if (!done && (fds[1].revents & (POLLIN | POLLHUP | POLLERR)))
            done = handle_stdin();
    }

    puts("bye");
    close(sfd);
    return 0;
}
