// EXERCISE: proc1_fork_wait — fork N 个子进程，用 waitpid 全部回收并解码退出状态
// TOPIC: fork / _exit / waitpid / WIFEXITED / WEXITSTATUS / 僵尸进程
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §8.3 fork、§8.5 exit、§8.6 wait 和 waitpid（图 8.4 状态宏）
//
// 说明：
//   用法：proc1_fork_wait N        （1 <= N <= 20）
//   - 父进程 fork N 个子进程；第 i 个子进程（i 从 1 开始）立刻 _exit(i)
//   - 父进程每 fork 一个就打印 "forked <pid> code <i>"（脚手架已写好）
//   - 然后回收**所有**子进程：每回收一个打印一行 "child <pid> exited <code>"，
//     最后打印 "total <所有 code 之和>"、"done"
//   - 打印 "done" 后程序阻塞读 stdin，直到 EOF 才退出 —— 测试趁这时检查 /proc，
//     确认你没有留下僵尸进程（state 'Z'）
//
//   waitpid 写回的 status 不是退出码！它是内核打包的一个 int：退出码在高 8 位，
//   被信号杀死时低 7 位是信号编号……必须用 WIFEXITED / WEXITSTATUS / WIFSIGNALED /
//   WTERMSIG 这组宏解码。直接打印 status 会得到 256、512 这种数字。
//
//   为什么重要：nginx master、gunicorn/uwsgi 的 arbiter、Redis 的 BGSAVE 子进程、
//   Docker 里的 PID 1（tini / dumb-init）都在做同一件事 —— 循环 waitpid 回收子进程、
//   根据退出状态决定是否重启 worker。不回收就会堆积僵尸，最终耗尽 PID。

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

enum { MAX_CHILDREN = 20 };

// TODO: 回收 n 个子进程。每回收一个，打印 "child <pid> exited <code>"，
//       code 用 WIFEXITED/WEXITSTATUS 解码（被信号杀死则按 shell 惯例记为 128+信号）。
//       waitpid 被信号打断（EINTR）要重试。返回所有 code 之和；出错返回 -1。
static int reap_all(int n) {
    int total = 0;
    for (int reaped = 0; reaped < n;) {
        int status;
        pid_t pid = waitpid(-1, &status, 0);
        if (pid < 0) {
            if (errno == EINTR)
                continue;
            perror("waitpid");
            return -1;
        }
        int code;
        if (WIFEXITED(status))
            code = WEXITSTATUS(status);
        else if (WIFSIGNALED(status))
            code = 128 + WTERMSIG(status);
        else
            continue; // 没有用 WUNTRACED，理论上不会走到这里
        printf("child %d exited %d\n", (int)pid, code);
        total += code;
        reaped++;
    }
    return total;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s N\n", argv[0]);
        return 2;
    }
    int n = atoi(argv[1]);
    if (n < 1 || n > MAX_CHILDREN) {
        fprintf(stderr, "proc1_fork_wait: N must be 1..%d\n", MAX_CHILDREN);
        return 2;
    }

    for (int i = 1; i <= n; i++) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            return 1;
        }
        if (pid == 0)
            _exit(i); // 子进程：立刻以 i 退出（为什么是 _exit 而不是 exit？见 proc6）
        printf("forked %d code %d\n", (int)pid, i);
    }

    int total = reap_all(n);
    if (total < 0)
        return 1;
    printf("total %d\n", total);
    puts("done");

    // 等 stdin EOF 再退出，给测试检查僵尸的机会
    char buf[64];
    while (read(STDIN_FILENO, buf, sizeof buf) > 0) {
    }
    return 0;
}
