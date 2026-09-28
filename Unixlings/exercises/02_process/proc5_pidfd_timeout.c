// EXERCISE: proc5_pidfd_timeout — 用 pidfd 实现 timeout(1)：限时运行命令，超时就杀掉
// TOPIC: pidfd_open / poll / pidfd_send_signal / SIGTERM→SIGKILL 升级 / PID 复用竞态
// DIFFICULTY: ★★★★☆
// BOOK: APUE §8.6 waitpid、§10.9 kill；man 2 pidfd_open、man 2 pidfd_send_signal（Linux 5.3+）
// I AM NOT DONE
//
// 说明：
//   用法：proc5_pidfd_timeout SECONDS cmd [args...]      （SECONDS 可以是小数，如 0.5）
//   - 启动子进程（脚手架已用 posix_spawnp 写好，并打印 "spawned <pid>"）
//   - 用 pidfd_open 拿到子进程的 pidfd，poll 它（子进程退出时 pidfd 变为可读），最多等 SECONDS 秒
//   - 子进程按时结束：回收它，以它的退出码退出（被信号杀死则 128+信号）
//   - 超时：pidfd_send_signal(pidfd, SIGTERM)；再给它 KILL_AFTER 秒，还不走就 SIGKILL；
//     回收后以 124 退出（和 coreutils timeout 一致）
//   - 内核不支持 pidfd_open（ENOSYS）时打印 "pidfd_open: not supported" 并以 125 退出
//
//   为什么用 pidfd 而不是 kill(pid, sig)？
//   PID 只是一个会被复用的数字。子进程退出、被回收（可能是别的线程/库替你 waitpid 了）之后，
//   内核可以把同一个 PID 分给一个毫不相干的新进程 —— 此时 kill(pid, SIGTERM) 就杀错了人。
//   pidfd 是指向"那一个进程"的文件描述符：进程死后 pidfd 依然指向那个已死的进程，
//   pidfd_send_signal 只会返回 ESRCH，绝不会误杀新进程。而且 pidfd 可以放进 poll/epoll，
//   让"等子进程退出"和"等超时/等 socket"统一进一个事件循环，不再需要 SIGCHLD 处理函数。
//
//   为什么重要：systemd 用 pidfd 管理服务进程；Go 1.23+ 的 os.Process、tokio::process、
//   Python 3.9 的 os.pidfd_open、Android 的 lmkd 都依赖它来避免 PID 复用竞态。

#include <errno.h>
#include <limits.h>
#include <poll.h>
#include <signal.h>
#include <spawn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

extern char **environ;

enum { EXIT_TIMEDOUT = 124, EXIT_NOPIDFD = 125, KILL_AFTER_MS = 2000 };

// 老 glibc 没有 pidfd_open 包装函数，直接走 syscall(2)
[[maybe_unused]] static int sl_pidfd_open(pid_t pid, unsigned flags) {
    return (int)syscall(SYS_pidfd_open, pid, flags);
}

[[maybe_unused]] static int sl_pidfd_send_signal(int pidfd, int sig) {
    return (int)syscall(SYS_pidfd_send_signal, pidfd, sig, nullptr, 0);
}

[[maybe_unused]] static long long now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

// TODO: poll pidfd 最多 timeout_ms 毫秒。子进程已退出返回 1，超时返回 0，出错返回 -1。
//       poll 被信号打断（EINTR）时要用**剩余**时间重试，而不是从头再等 timeout_ms。
[[maybe_unused]] static int wait_readable(int pidfd, long long timeout_ms) {
    return -1;
}

static int reap(pid_t pid) {
    int status;
    while (waitpid(pid, &status, 0) < 0) {
        if (errno != EINTR) {
            perror("waitpid");
            return 1;
        }
    }
    return WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
}

// TODO: 限时等待子进程 pid，返回本程序的退出码（见说明）
static int wait_with_timeout(pid_t pid, double seconds) {
    // BUG: 根本没有限时 —— 子进程不退出，我们就永远等下去
    return reap(pid);
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc < 3) {
        fprintf(stderr, "usage: %s SECONDS cmd [args...]\n", argv[0]);
        return 2;
    }
    char *end;
    double seconds = strtod(argv[1], &end);
    if (*end != '\0' || !(seconds >= 0) || seconds > 1e6) {
        fprintf(stderr, "proc5_pidfd_timeout: bad SECONDS: %s\n", argv[1]);
        return 2;
    }

    pid_t pid;
    int err = posix_spawnp(&pid, argv[2], nullptr, nullptr, &argv[2], environ);
    if (err) {
        fprintf(stderr, "proc5_pidfd_timeout: %s: %s\n", argv[2], strerror(err));
        return 127;
    }
    printf("spawned %d\n", (int)pid);

    return wait_with_timeout(pid, seconds);
}
