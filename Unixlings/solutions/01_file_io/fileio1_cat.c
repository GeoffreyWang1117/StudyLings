// EXERCISE: fileio1_cat — 只用 read(2)/write(2) 实现 cat，并复现 APUE 图 3.6
// TOPIC: 无缓冲 I/O：read / write / 短写
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §3.6-3.9；图 3.6（缓冲区大小对 read 次数与耗时的影响）
//
// 说明：
//   用法：fileio1_cat [-b BUFSIZE] [FILE...]      没有 FILE 时读 stdin
//   - 不许用 stdio（fopen/fread/printf 写数据），只用 open/read/write/close
//   - 每次 read 最多 BUFSIZE 字节（默认 4096）—— 测试会用 strace 数你的 read 次数
//   - write(2) 可能"短写"：写入字节数少于请求数（管道、socket、被信号打断时都会发生）。
//     必须循环写完，这就是 write_all 的作用
//   - read 返回 -1 且 errno == EINTR 时应当重试
//   - 出错时向 stderr 打印 "fileio1_cat: <文件名>: <错误原因>"，继续处理下一个文件，最后以 1 退出
//
// 实验（选做）：cmake --build --preset nosan --target fileio1_cat 后，
//   对一个 1GB 文件用 hyperfine 比较 -b 1 / 64 / 4096 / 131072，对照 APUE 图 3.6 的 2013 年数据。

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// TODO: 把 buf[0..n) 全部写到 fd，处理短写和 EINTR。成功返回 0，失败返回 -1（errno 保持）
static int write_all(int fd, const char *buf, size_t n) {
    while (n > 0) {
        ssize_t w = write(fd, buf, n);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        buf += w;
        n -= (size_t)w;
    }
    return 0;
}

// TODO: 把 in_fd 的内容全部拷贝到 out_fd，每次 read 最多 bufsize 字节。
//       read 返回 0 表示 EOF。成功返回 0，失败返回 -1
static int copy_fd(int in_fd, int out_fd, char *buf, size_t bufsize) {
    for (;;) {
        ssize_t r = read(in_fd, buf, bufsize);
        if (r == 0)
            return 0;
        if (r < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        if (write_all(out_fd, buf, (size_t)r) < 0)
            return -1;
    }
}

int main(int argc, char *argv[]) {
    size_t bufsize = 4096;
    int opt;
    while ((opt = getopt(argc, argv, "b:")) != -1) {
        if (opt == 'b') {
            bufsize = strtoul(optarg, nullptr, 10);
        } else {
            fprintf(stderr, "usage: %s [-b BUFSIZE] [FILE...]\n", argv[0]);
            return 2;
        }
    }
    if (bufsize == 0) {
        fprintf(stderr, "fileio1_cat: bad buffer size\n");
        return 2;
    }
    char *buf = malloc(bufsize);
    if (!buf)
        return 1;

    int status = 0;
    if (optind == argc) {
        if (copy_fd(STDIN_FILENO, STDOUT_FILENO, buf, bufsize) < 0) {
            fprintf(stderr, "fileio1_cat: -: %s\n", strerror(errno));
            status = 1;
        }
    }
    for (int i = optind; i < argc; i++) {
        int fd = open(argv[i], O_RDONLY | O_CLOEXEC);
        if (fd < 0) {
            fprintf(stderr, "fileio1_cat: %s: %s\n", argv[i], strerror(errno));
            status = 1;
            continue;
        }
        if (copy_fd(fd, STDOUT_FILENO, buf, bufsize) < 0) {
            fprintf(stderr, "fileio1_cat: %s: %s\n", argv[i], strerror(errno));
            status = 1;
        }
        close(fd);
    }
    free(buf);
    return status;
}
