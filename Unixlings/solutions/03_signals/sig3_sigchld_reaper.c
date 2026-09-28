// EXERCISE: sig3_sigchld_reaper — 在 SIGCHLD 处理函数里循环回收子进程
// TOPIC: SIGCHLD、信号不排队（合并）、waitpid(WNOHANG)、保存/恢复 errno
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §8.6（wait/waitpid）, §10.7（SIGCLD 语义）, §10.8（可靠信号：信号不排队）
//
// 说明：
//   用法：sig3_sigchld_reaper N
//   程序 fork 出 N 个子进程，它们几乎同时退出。父进程靠 SIGCHLD 处理函数回收它们，
//   然后打印 ready 并阻塞读 stdin，直到 EOF 才打印 "reaped K" 退出。
//   关键事实：标准信号 **不排队**。N 个子进程在 SIGCHLD 被阻塞期间退出，解除阻塞后
//   只会递送 **一次** SIGCHLD。所以处理函数必须：
//     - 循环 while (waitpid(-1, &status, WNOHANG) > 0) 把所有已退出的子进程都收掉
//     - 进入时保存 errno、离开时恢复（waitpid 最终会把 errno 设成 ECHILD，
//       而处理函数可能打断了主程序里一个刚失败、正准备检查 errno 的系统调用）
//   为了让这个现象 100% 可复现，脚手架代码故意在 SIGCHLD 被阻塞时让全部子进程退出。
//   测试会：N=64，等到 ready 后检查 /proc，要求该进程没有任何僵尸（Z 状态）子进程。
//
//   为什么重要：nginx master、Apache prefork、PostgreSQL postmaster 都用这种方式回收 worker。
//   Docker 容器里的 PID 1 如果是你的程序，孤儿进程都会被过继给它——不回收就会堆满僵尸，
//   最终耗尽 PID。这正是 tini、dumb-init、docker run --init 存在的原因。

#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_CHILDREN = 1024 };

static volatile sig_atomic_t g_reaped = 0;

// TODO: 一次 SIGCHLD 可能代表很多个子进程退出：循环 waitpid(WNOHANG) 直到没有可回收的；
//       并保存/恢复 errno
static void on_sigchld(int signo) {
    (void)signo;
    int saved_errno = errno;
    int status;
    while (waitpid(-1, &status, WNOHANG) > 0)
        g_reaped = g_reaped + 1;
    errno = saved_errno;
}

static void install_sigchld_handler(void) {
    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_handler = on_sigchld;
    sigemptyset(&sa.sa_mask);
    // SA_RESTART：主循环的 read(stdin) 被 SIGCHLD 打断后自动重启
    // SA_NOCLDSTOP：子进程只是被暂停（SIGSTOP）时不要通知
    sa.sa_flags = SA_RESTART | SA_NOCLDSTOP;
    if (sigaction(SIGCHLD, &sa, nullptr) < 0)
        sl_die("sigaction");
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s N\n", argv[0]);
        return 2;
    }
    long n = strtol(argv[1], nullptr, 10);
    if (n <= 0 || n > MAX_CHILDREN) {
        fprintf(stderr, "sig3_sigchld_reaper: N must be 1..%d\n", MAX_CHILDREN);
        return 2;
    }

    install_sigchld_handler();

    // ---- 脚手架：制造"N 个子进程退出，只来一次 SIGCHLD"的场景 ----
    sigset_t chld, old;
    sigemptyset(&chld);
    sigaddset(&chld, SIGCHLD);
    if (sigprocmask(SIG_BLOCK, &chld, &old) < 0)
        sl_die("sigprocmask");

    int gate[2];  // 子进程阻塞读 gate[0]，父进程关闭 gate[1] 时它们一起退出
    if (pipe(gate) < 0)
        sl_die("pipe");
    pid_t pids[MAX_CHILDREN];
    for (long i = 0; i < n; i++) {
        pid_t pid = fork();
        if (pid < 0)
            sl_die("fork");
        if (pid == 0) {
            close(gate[1]);
            char c;
            (void)read(gate[0], &c, 1);  // 等父进程关闭写端（EOF）
            _exit(0);
        }
        pids[i] = pid;
    }
    close(gate[0]);
    close(gate[1]);  // 放行：所有子进程同时退出
    for (long i = 0; i < n; i++) {
        siginfo_t si;
        // WNOWAIT：等它变成僵尸，但不回收——回收是 SIGCHLD 处理函数的工作
        while (waitid(P_PID, (id_t)pids[i], &si, WEXITED | WNOWAIT) < 0) {
            if (errno != EINTR)
                sl_die("waitid");
        }
    }
    // 此刻 N 个子进程都是僵尸，内核里只挂着 **一个** 待决的 SIGCHLD
    if (sigprocmask(SIG_SETMASK, &old, nullptr) < 0)
        sl_die("sigprocmask");
    // ---- 脚手架结束 ----

    puts("ready");

    char buf[256];
    for (;;) {
        ssize_t r = read(STDIN_FILENO, buf, sizeof buf);
        if (r == 0)
            break;
        if (r < 0) {
            if (errno == EINTR)
                continue;
            sl_die("read");
        }
    }
    printf("reaped %d\n", (int)g_reaped);
    return 0;
}
