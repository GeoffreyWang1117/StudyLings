// EXERCISE: fileio4_redirect — dup/dup2 重定向 stdout，以及 stdio 缓冲的陷阱
// TOPIC: dup / dup2 / 文件描述符表 / fflush
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §3.12（dup/dup2）、§5.4（标准 I/O 缓冲）
//
// 说明：
//   用法：fileio4_redirect FILE
//   程序依次打印三行：第 1 行到原来的 stdout，第 2 行临时重定向到 FILE，第 3 行恢复到原来的 stdout。
//   shell 的 `cmd > file`、Python 的 contextlib.redirect_stdout(对 fd 层面的版本)、
//   测试框架捕获子进程输出，底层都是 dup2。
//   两个坑：
//   1. dup2(fd, STDOUT_FILENO) 只换掉了 fd 1 指向的文件；printf 的数据还可能躺在 stdio 的用户态缓冲区里。
//      stdout 接到管道/文件时是"全缓冲"，不 fflush 就切换 fd，缓冲区里的旧数据会被写进新文件。
//   2. 恢复时需要事先用 dup(1) 保存原来的 stdout，否则原来的文件就再也找不回来了。
//   测试时 stdout 是管道（全缓冲），正好能暴露第 1 个坑。

#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

// TODO: 把 stdout 重定向到 path（创建/截断），返回保存下来的原 stdout fd；失败返回 -1
static int redirect_stdout(const char *path) {
    fflush(stdout); // 先把缓冲区里属于"旧 stdout"的数据写出去
    int saved = dup(STDOUT_FILENO);
    if (saved < 0)
        return -1;
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0644);
    if (fd < 0) {
        close(saved);
        return -1;
    }
    if (dup2(fd, STDOUT_FILENO) < 0) { // dup2 产生的新 fd 不带 FD_CLOEXEC
        close(fd);
        close(saved);
        return -1;
    }
    close(fd);
    return saved;
}

// TODO: 恢复原来的 stdout，并关闭 saved
static void restore_stdout(int saved) {
    if (saved < 0)
        return;
    fflush(stdout); // 属于文件的数据必须在切回之前写进文件
    dup2(saved, STDOUT_FILENO);
    close(saved);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE\n", argv[0]);
        return 2;
    }
    printf("line 1: original stdout\n");
    int saved = redirect_stdout(argv[1]);
    printf("line 2: redirected into file\n");
    restore_stdout(saved);
    printf("line 3: original stdout again\n");
    return 0;
}
