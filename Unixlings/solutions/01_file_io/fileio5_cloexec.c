// EXERCISE: fileio5_cloexec — 文件描述符泄漏到子进程：O_CLOEXEC
// TOPIC: FD_CLOEXEC / O_CLOEXEC / EFD_CLOEXEC / close_range
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §3.14（fcntl, FD_CLOEXEC）、§8.10（exec 时哪些属性被继承）；man 2 close_range（Linux 5.9+）
//
// 说明：
//   用法：fileio5_cloexec SECRET_FILE CMD [ARGS...]
//   程序模拟一个服务：打开一个"敏感"文件（数据库、私钥），创建一个 eventfd 做内部唤醒，
//   然后 fork + exec 一个外部命令（CGI、插件、git、ffmpeg……）并等待它结束。
//   fd 默认会跨 exec 继承 —— 外部命令能直接读你的私钥、握住你的 socket 不放（端口无法重新绑定）。
//   修复：创建 fd 时就带上 close-on-exec 标志（O_CLOEXEC / EFD_CLOEXEC / SOCK_CLOEXEC / pipe2 O_CLOEXEC）。
//   为什么不在 fork 后再 fcntl(fd, F_SETFD, FD_CLOEXEC)？多线程程序里别的线程可能恰好在两步之间 fork，
//   所以现代代码一律在创建时原子地设置。Go、Rust std、Python 3.4+ 默认所有 fd 都是 CLOEXEC。
//   测试会用 `ls -l /proc/self/fd` 作为 CMD，检查子进程里看不到这两个 fd。

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/eventfd.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s SECRET_FILE CMD [ARGS...]\n", argv[0]);
        return 2;
    }
    int secret = open(argv[1], O_RDONLY | O_CLOEXEC);
    int wakeup = eventfd(0, EFD_CLOEXEC);
    if (secret < 0 || wakeup < 0) {
        perror("open/eventfd");
        return 1;
    }
    char buf[256];
    ssize_t n = read(secret, buf, sizeof buf);
    printf("loaded %zd bytes of secret\n", n);
    fflush(stdout);

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return 1;
    }
    if (pid == 0) {
        execvp(argv[2], &argv[2]);
        perror("execvp");
        _exit(127);
    }
    int status;
    if (waitpid(pid, &status, 0) < 0) {
        perror("waitpid");
        return 1;
    }
    close(secret);
    close(wakeup);
    return WIFEXITED(status) ? WEXITSTATUS(status) : 1;
}
