// EXERCISE: proc4_posix_spawn — 用 posix_spawnp 代替 fork+exec，捕获子进程的 stdout
// TOPIC: posix_spawnp / posix_spawn_file_actions / 管道读取 / 返回错误码而不是 errno
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §8.10 exec、§15.2 管道；man 3 posix_spawn；man 3 posix_spawn_file_actions_adddup2
// I AM NOT DONE
//
// 说明：
//   用法：proc4_posix_spawn cmd [args...]
//   实现 run_capture(argv, out, cap, &status)：运行 argv（按 PATH 查找），把子进程的 stdout
//   收集到 out（最多 cap-1 字节，以 '\0' 结尾，超出部分读出来丢掉），stderr 不管；
//   子进程结束后把 waitpid 的 status 写入 *status。
//   返回值：0 成功；失败时返回一个**错误码**（如 ENOENT），不是 -1。
//   main（已写好）打印 "exit=<code> output=<去掉结尾空白的输出>"；
//   启动失败时打印 "proc4_posix_spawn: <cmd>: <strerror>" 到 stderr 并以 127 退出。
//
//   注意 posix_spawn 家族的错误约定：**直接返回错误码，不设置 errno**（和 pthread_* 一样）。
//   写成 `if (posix_spawnp(...) == -1) perror(...)` 是经典 bug。
//   glibc 2.24+ 用 clone(CLONE_VM|CLONE_VFORK) 实现 posix_spawn，并能把子进程里 exec 的
//   失败原因（比如 ENOENT）传回给父进程 —— 这是 fork+exec 做不到的（fork 后只能靠退出码 127）。
//
//   还要当心死锁：子进程输出超过管道容量（Linux 默认 64KiB）时会阻塞在 write，
//   如果父进程先 waitpid 再 read，双方永远互等。必须先读到 EOF，再 waitpid。
//
//   为什么重要：fork 要复制页表，对几十 GB 的 JVM/Redis 进程很慢，而且多线程程序里
//   fork 后只能调用 async-signal-safe 函数。所以 Python subprocess（_posixsubprocess 在条件
//   允许时用 vfork/posix_spawn）、Rust std::process::Command、Java ProcessBuilder（jspawnhelper）
//   都优先用 posix_spawn / vfork 语义来启动子进程。

#include <errno.h>
#include <fcntl.h>
#include <spawn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

extern char **environ;

enum { OUT_CAP = 1 << 20 };

// TODO: 实现本函数。步骤：
//   1. pipe2(fds, O_CLOEXEC) 建管道
//   2. posix_spawn_file_actions_init + posix_spawn_file_actions_adddup2(&fa, fds[1], STDOUT_FILENO)
//   3. posix_spawnp(&pid, argv[0], &fa, nullptr, argv, environ) —— 注意它返回错误码
//   4. 父进程 close 写端，循环 read 到 EOF（EINTR 重试；超出 cap-1 的部分丢弃但继续读）
//   5. waitpid 得到 *status
//   所有路径都要 destroy file_actions、close 管道 fd。
[[nodiscard]] static int run_capture(char *const argv[], char *out, size_t cap, int *status) {
    if (cap > 0)
        out[0] = '\0';
    *status = 0;
    return ENOSYS; // TODO: 删掉这一行，按上面的步骤实现
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s cmd [args...]\n", argv[0]);
        return 2;
    }
    char *out = malloc(OUT_CAP);
    if (!out)
        return 1;
    out[0] = '\0';
    int status = 0;
    int err = run_capture(&argv[1], out, OUT_CAP, &status);
    if (err) {
        fprintf(stderr, "proc4_posix_spawn: %s: %s\n", argv[1], strerror(err));
        free(out);
        return 127;
    }
    size_t n = strlen(out);
    while (n > 0 && (out[n - 1] == '\n' || out[n - 1] == ' ' || out[n - 1] == '\t'))
        out[--n] = '\0';
    int code = WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
    printf("exit=%d output=%s\n", code, out);
    free(out);
    return 0;
}
