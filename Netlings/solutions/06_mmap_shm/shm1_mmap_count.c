// EXERCISE: shm1_mmap_count — 用 mmap 代替 read 统计文件的行数与字节数
// TOPIC: mmap(PROT_READ, MAP_PRIVATE) / madvise(MADV_SEQUENTIAL) / memchr / 空文件陷阱
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §14.8（存储映射 I/O）；UNP 卷2 §12；man 2 mmap, man 2 madvise
//
// 说明：
//   用法：shm1_mmap_count FILE
//   输出一行：lines=<换行符个数> bytes=<文件大小>（和 `wc -l -c` 的两个数一致）
//
//   要求：
//   - 不许 read(2) 这个文件：fstat 拿大小 → mmap 整个文件 → 在内存里用 memchr 数 '\n'。
//     探针会用 strace 检查没有对该文件的 read 调用。
//   - madvise(MADV_SEQUENTIAL)：告诉内核我们会顺序扫描，加大预读、读过的页可以尽早回收。
//   - 空文件：mmap 长度为 0 会失败（EINVAL）！大小为 0 时直接输出 lines=0 bytes=0。
//   - 用完 munmap + close（ASan/LSan 不管 mmap，但好习惯要有）。
//
//   现代用法：LMDB、SQLite（mmap_size）、MongoDB 早期的 MMAPv1、ripgrep 对大文件的搜索、
//   Prometheus TSDB 的 chunk、Kafka 的索引文件，都靠 mmap 把"读文件"变成"访问内存"，
//   省掉一次内核→用户态的拷贝，并由 page cache 统一管理缓存。

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#include "sl.h"

// 在 [p, p+n) 里数 '\n'
static size_t count_newlines(const char *p, size_t n) {
    size_t lines = 0;
    const char *end = p + n;
    while (p < end) {
        const char *nl = memchr(p, '\n', (size_t)(end - p));
        if (nl == nullptr)
            break;
        lines++;
        p = nl + 1;
    }
    return lines;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE\n", argv[0]);
        return 2;
    }
    int fd = open(argv[1], O_RDONLY | O_CLOEXEC);
    if (fd < 0)
        sl_die(argv[1]);
    struct stat st;
    if (fstat(fd, &st) < 0)
        sl_die("fstat");
    if (!S_ISREG(st.st_mode)) {
        fprintf(stderr, "shm1_mmap_count: %s: not a regular file\n", argv[1]);
        return 1;
    }
    size_t size = (size_t)st.st_size;

    size_t lines = 0;
    if (size > 0) { // mmap 长度 0 → EINVAL，空文件直接跳过
        char *p = mmap(nullptr, size, PROT_READ, MAP_PRIVATE, fd, 0);
        if (p == MAP_FAILED)
            sl_die("mmap");
        if (madvise(p, size, MADV_SEQUENTIAL) < 0)
            perror("madvise"); // 只是建议，失败不致命
        lines = count_newlines(p, size);
        if (munmap(p, size) < 0)
            sl_die("munmap");
    }
    close(fd);
    printf("lines=%zu bytes=%zu\n", lines, size);
    return 0;
}
