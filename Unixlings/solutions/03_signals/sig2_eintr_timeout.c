// EXERCISE: sig2_eintr_timeout — 用 SIGALRM + EINTR 给阻塞的 read 加超时
// TOPIC: 被中断的系统调用、SA_RESTART、alarm(2)
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §10.5（中断的系统调用）, §10.10（alarm/pause）, §10.14（sigaction 的 SA_RESTART）
//
// 说明：
//   用法：sig2_eintr_timeout SECONDS
//   从 stdin 读一行，最多等 SECONDS 秒：
//     - 读到一行 → 打印 "got: <这一行>"，退出码 0
//     - 超时     → 打印 "timeout"，退出码 3
//   实现方式是经典的 UNIX 超时技巧：
//     1. 用 sigaction 为 SIGALRM 安装一个（什么也不做的）处理函数，且 **不带 SA_RESTART**
//     2. alarm(SECONDS) 定一个闹钟，然后阻塞在 read(2)
//     3. 闹钟响 → 信号处理函数运行 → 内核让被打断的 read 返回 -1，errno == EINTR
//   如果设置了 SA_RESTART，内核会在处理函数返回后自动重启 read，于是永远等下去——超时失效。
//   （glibc 的 signal(2) 默认就带 SA_RESTART 语义！）
//   测试会：保持 stdin 管道打开但不写数据，要求程序在超时后打印 timeout；再测有输入的情况。
//
//   为什么重要：EINTR 是每个系统程序员都会踩的坑。Redis、nginx 的每个 read/write/epoll_wait 循环
//   都要处理 EINTR；Go runtime 在 Go 1.14 引入异步抢占（用 SIGURG）后，大量 cgo/syscall 代码
//   突然开始收到 EINTR。现代代码更常用 poll/epoll 的超时参数、timerfd 或 SO_RCVTIMEO，
//   但理解"信号打断系统调用"是理解这些机制的基础。

#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "sl.h"

static void on_alarm(int signo) {
    (void)signo;  // 什么也不用做：它存在的意义就是"打断" read
}

// TODO: 为 SIGALRM 安装 on_alarm。关键在 sa_flags
static void install_alarm_handler(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_handler = on_alarm;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;  // 不要 SA_RESTART，否则 read 会被自动重启，超时永远不会发生
    if (sigaction(SIGALRM, &sa, nullptr) < 0)
        sl_die("sigaction");
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s SECONDS\n", argv[0]);
        return 2;
    }
    unsigned seconds = (unsigned)strtoul(argv[1], nullptr, 10);
    if (seconds == 0) {
        fprintf(stderr, "sig2_eintr_timeout: bad timeout\n");
        return 2;
    }

    install_alarm_handler();
    alarm(seconds);

    char line[4096];
    size_t len = 0;
    while (len < sizeof line - 1) {
        ssize_t r = read(STDIN_FILENO, line + len, sizeof line - 1 - len);
        if (r < 0) {
            // TODO: 被 SIGALRM 打断（EINTR）说明超时了：打印 timeout，返回 3
            if (errno == EINTR) {
                puts("timeout");
                return 3;
            }
            sl_die("read");
        }
        if (r == 0)
            break;  // EOF
        len += (size_t)r;
        if (memchr(line + len - (size_t)r, '\n', (size_t)r))
            break;
    }
    alarm(0);  // 成功读到数据：取消闹钟，免得它之后在不该响的地方响

    line[len] = '\0';
    line[strcspn(line, "\n")] = '\0';
    printf("got: %s\n", line);
    return 0;
}
