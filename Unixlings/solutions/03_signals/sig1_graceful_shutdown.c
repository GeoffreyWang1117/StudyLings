// EXERCISE: sig1_graceful_shutdown — 收到 SIGTERM/SIGINT 时优雅退出
// TOPIC: sigaction、volatile sig_atomic_t 标志位、异步信号安全
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §10.2-10.3, §10.6（可重入函数）, §10.14（sigaction）；man 7 signal-safety
//
// 说明：
//   用法：sig1_graceful_shutdown
//   程序模拟一个"服务器"：打印 ready，然后在主循环里每 50ms 做一次"工作"（nanosleep 一个 tick）。
//   收到 SIGTERM 或 SIGINT 时必须"优雅关闭"：
//     - 用 sigaction(2) 安装处理函数（不要用老式的 signal(2)，它的语义在不同系统上不一致）
//     - 处理函数里只做一件事：把一个 volatile sig_atomic_t 标志置 1
//       （printf / malloc / exit 都不是 async-signal-safe 的：信号可能正好打断主程序里的
//        printf，此时在处理函数里再 printf 会破坏 stdio 内部状态甚至死锁）
//     - 主循环发现标志后跳出，做收尾工作，打印 "graceful shutdown"，以退出码 0 结束
//   测试会：启动程序 → 等 ready → 发 SIGTERM（或 SIGINT）→ 要求退出码 0 且输出 graceful shutdown。
//
//   为什么重要：Kubernetes 删除 Pod 时先给容器的 PID 1 发 SIGTERM，等 terminationGracePeriodSeconds
//   （默认 30s）后再发 SIGKILL。这段时间里服务应当停止接新请求、处理完手上的请求、刷盘、关连接。
//   nginx（SIGQUIT 优雅退出）、Redis（SIGTERM 时先 SAVE 再退出）、Go 的 signal.NotifyContext、
//   Node 的 process.on('SIGTERM') 做的都是这件事。没装处理函数的进程会被 SIGTERM 直接杀死，
//   正在处理的请求全部中断。

#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

// 处理函数和主循环之间唯一共享的状态
static volatile sig_atomic_t g_stop = 0;

// TODO: 处理函数只允许设置标志（异步信号安全）
static void on_signal(int signo) {
    (void)signo;
    g_stop = 1;
}

// TODO: 用 sigaction 为 SIGTERM 和 SIGINT 安装 on_signal
static void install_handlers(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_handler = on_signal;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;  // 不要 SA_RESTART：让阻塞调用（nanosleep、accept…）被打断，尽快回到主循环
    if (sigaction(SIGTERM, &sa, nullptr) < 0)
        sl_die("sigaction SIGTERM");
    if (sigaction(SIGINT, &sa, nullptr) < 0)
        sl_die("sigaction SIGINT");
}

int main(void) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    install_handlers();

    puts("ready");
    unsigned long ticks = 0;
    const struct timespec tick = {.tv_sec = 0, .tv_nsec = 50 * 1000 * 1000};
    while (!g_stop) {
        // "处理一个请求"。nanosleep 被信号打断时返回 -1/EINTR，下一轮循环就会看到 g_stop
        if (nanosleep(&tick, nullptr) == 0)
            ticks++;
    }

    // 收尾工作：真实服务器在这里关闭监听 socket、等待进行中的请求、刷写日志/数据
    printf("processed %lu ticks\n", ticks);
    puts("graceful shutdown");
    return 0;
}
