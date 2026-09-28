// EXERCISE: fileio3_append — O_APPEND 的原子性：多个进程同时写同一个日志文件
// TOPIC: O_APPEND / 文件描述 (file description) / 竞态
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §3.11（原子操作）、§3.10（文件共享：进程表项 → 文件表 → v-node）
//
// 说明：
//   用法：fileio3_append FILE NPROC NLINES
//   启动 NPROC 个子进程，每个子进程独立 open 同一个日志文件，各写 NLINES 行 "worker <i> line <j>\n"。
//   现在的写法是 "lseek 到末尾，再 write"：两步之间另一个进程可能也 seek 到了同一个末尾，
//   结果两行写到同一个偏移上，互相覆盖 —— 日志丢行。
//   修复：用 O_APPEND 打开，内核保证 "移动到末尾 + 写入" 是一个原子操作。
//   这正是 nginx access_log、多 worker 的 Python/Node 服务共享日志文件时依赖的语义。
//   （注意：每行必须用一次 write 写完；O_APPEND 保证的是单次 write 的原子性。）

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

static void worker(const char *path, int id, int nlines) {
    int fd = open(path, O_WRONLY | O_CREAT | O_APPEND | O_CLOEXEC, 0644);
    if (fd < 0) {
        perror("open");
        _exit(1);
    }
    char line[64];
    for (int j = 0; j < nlines; j++) {
        int n = snprintf(line, sizeof line, "worker %d line %d\n", id, j);
        if (write(fd, line, (size_t)n) != n) {
            perror("write");
            _exit(1);
        }
    }
    close(fd);
    _exit(0);
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s FILE NPROC NLINES\n", argv[0]);
        return 2;
    }
    int nproc = atoi(argv[2]), nlines = atoi(argv[3]);
    for (int i = 0; i < nproc; i++) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            return 1;
        }
        if (pid == 0)
            worker(argv[1], i, nlines);
    }
    int status, failed = 0;
    while (wait(&status) > 0)
        if (!WIFEXITED(status) || WEXITSTATUS(status) != 0)
            failed = 1;
    return failed;
}
