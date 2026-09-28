// EXERCISE: proc3_pipeline — 用 pipe/fork/dup2/execvp 实现 shell 的 `cmd1 | cmd2`
// TOPIC: pipe / dup2 / execvp / 关闭多余的管道端 / O_CLOEXEC / 退出状态传递
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §15.2 管道、§8.10 exec、§3.12 dup2、§8.6 waitpid；man 2 pipe2
// I AM NOT DONE
//
// 说明：
//   用法：proc3_pipeline cmd1 [args...] '|' cmd2 [args...]
//   例：  proc3_pipeline printf 'a\nb\n' '|' wc -l          → 输出 2
//   - cmd1 的 stdout 接到 cmd2 的 stdin；两者的 stderr 不变
//   - 父进程等待两个子进程，并像 sh 一样以 **cmd2** 的退出状态退出：
//     正常退出 → 它的退出码；被信号杀死 → 128+信号编号
//   - 命令不存在：子进程打印 "proc3_pipeline: <cmd>: <strerror>" 到 stderr 并 _exit(127)
//
//   两个经典 bug（测试都会抓）：
//   1. 读端永远等不到 EOF：只要**任何**进程还持有管道写端，read 就不会返回 0。
//      父进程、cmd2 自己都可能还拿着写端 → `wc` 永远挂着。父进程必须 close 两端。
//   2. fd 泄漏：原始的 pipe fd 被 exec 后的命令继承。用 pipe2(fds, O_CLOEXEC) 创建，
//      exec 时内核自动关闭它们；而 dup2 出来的 0/1 不带 CLOEXEC 标志，会正常保留。
//      反过来：cmd1 退出后如果还有人拿着读端，`yes | head -n 1` 里的 yes 就收不到 SIGPIPE。
//
//   为什么重要：这就是 bash/zsh 管道、Python subprocess.Popen(stdout=PIPE)、Node child_process、
//   Go os/exec 的底层实现。现代运行时（Go、Rust std、Python 3.4+）创建的所有 fd 默认都带
//   O_CLOEXEC，正是为了避免 fd 漏进子进程 —— 漏掉的 socket/管道会让对端永远等不到 EOF。

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

// 在子进程里把 in_fd/out_fd 接到 stdin/stdout 后 exec argv。返回子进程 pid，fork 失败返回 -1
static pid_t spawn_stage(char *argv[], int in_fd, int out_fd) {
    pid_t pid = fork();
    if (pid != 0)
        return pid; // 父进程（或 fork 失败的 -1）
    if (in_fd != STDIN_FILENO && dup2(in_fd, STDIN_FILENO) < 0) {
        perror("dup2");
        _exit(126);
    }
    if (out_fd != STDOUT_FILENO && dup2(out_fd, STDOUT_FILENO) < 0) {
        perror("dup2");
        _exit(126);
    }
    execvp(argv[0], argv);
    int err = errno;
    fprintf(stderr, "proc3_pipeline: %s: %s\n", argv[0], strerror(err));
    _exit(err == ENOENT ? 127 : 126);
}

// TODO: 把 waitpid 的 status 转成 shell 风格的退出码
static int status_to_code(int status) {
    return 0;
}

static int wait_child(pid_t pid, int *status) {
    while (waitpid(pid, status, 0) < 0) {
        if (errno != EINTR)
            return -1;
    }
    return 0;
}

// 运行 left | right，返回 right 的 shell 风格退出码；内部错误返回 -1
static int run_pipeline(char *left[], char *right[]) {
    int fds[2];
    // TODO: 创建管道。想一想：exec 之后，cmd1/cmd2 还需要原始的 fds[0]/fds[1] 吗？
    // BUG: 普通 pipe()：原始的两个 fd 会被 exec 出来的 cmd1、cmd2 继承
    if (pipe(fds) < 0) {
        perror("pipe");
        return -1;
    }

    pid_t p1 = spawn_stage(left, STDIN_FILENO, fds[1]);
    if (p1 < 0) {
        perror("fork");
        close(fds[0]);
        close(fds[1]);
        return -1;
    }
    pid_t p2 = spawn_stage(right, fds[0], STDOUT_FILENO);
    int saved = errno;

    // TODO: 父进程不读也不写这个管道 —— 关掉两端，否则 cmd2 永远等不到 EOF

    int st1, st2;
    if (wait_child(p1, &st1) < 0) {
        perror("waitpid");
        return -1;
    }
    if (p2 < 0) {
        errno = saved;
        perror("fork");
        return -1;
    }
    if (wait_child(p2, &st2) < 0) {
        perror("waitpid");
        return -1;
    }
    // TODO: 像 sh 一样返回 cmd2 的退出状态
    return status_to_code(st2);
}

int main(int argc, char *argv[]) {
    int bar = -1;
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "|") == 0) {
            bar = i;
            break;
        }
    }
    if (bar <= 1 || bar == argc - 1) {
        fprintf(stderr, "usage: %s cmd1 [args...] '|' cmd2 [args...]\n", argv[0]);
        return 2;
    }
    argv[bar] = nullptr; // 把 argv 切成两个以 nullptr 结尾的数组
    int code = run_pipeline(&argv[1], &argv[bar + 1]);
    return code < 0 ? 1 : code;
}
