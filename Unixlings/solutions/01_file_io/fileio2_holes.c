// EXERCISE: fileio2_holes — lseek 与文件空洞（sparse file），SEEK_DATA / SEEK_HOLE
// TOPIC: lseek / 稀疏文件 / st_size vs st_blocks
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §3.6 图 3.2（带空洞的文件）；man 2 lseek 的 SEEK_DATA/SEEK_HOLE（Linux 3.1+）
//
// 说明：
//   用法：fileio2_holes create PATH OFFSET    在偏移 0 写 "head"，在偏移 OFFSET 写 "tail"
//         fileio2_holes map PATH              打印文件里所有"有数据"的区间
//   lseek 越过文件末尾再写，中间的区域就是"空洞"：读出来是 0，但不占磁盘块。
//   虚拟机磁盘镜像（qcow2/raw）、数据库预分配文件、`truncate -s 10G` 都依赖这一点；
//   `cp --sparse`、`tar -S`、rsync 用 SEEK_DATA/SEEK_HOLE 跳过空洞，只拷贝真实数据。
//   map 的输出格式（每个数据区间一行，end 不含）：
//       data <start> <end>
//   最后一行：size <文件大小>
//   区间边界由文件系统的块大小决定（不一定是 4 或 OFFSET），测试会用同样的 SEEK_DATA/SEEK_HOLE
//   在 Python 里算出期望值来对比。

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static int do_create(const char *path, off_t offset) {
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0644);
    if (fd < 0) {
        perror("open");
        return 1;
    }
    if (write(fd, "head", 4) != 4) {
        perror("write");
        return 1;
    }
    if (lseek(fd, offset, SEEK_SET) < 0) {
        perror("lseek");
        return 1;
    }

    if (write(fd, "tail", 4) != 4) {
        perror("write");
        return 1;
    }
    close(fd);
    return 0;
}

static int do_map(const char *path) {
    int fd = open(path, O_RDONLY | O_CLOEXEC);
    if (fd < 0) {
        perror("open");
        return 1;
    }
    struct stat st;
    if (fstat(fd, &st) < 0) {
        perror("fstat");
        return 1;
    }
    off_t pos = 0;
    for (;;) {
        off_t start = lseek(fd, pos, SEEK_DATA);
        if (start < 0) {
            if (errno == ENXIO)
                break;
            perror("lseek SEEK_DATA");
            return 1;
        }
        off_t end = lseek(fd, start, SEEK_HOLE);
        if (end < 0) {
            perror("lseek SEEK_HOLE");
            return 1;
        }
        printf("data %lld %lld\n", (long long)start, (long long)end);
        pos = end;
    }

    printf("size %lld\n", (long long)st.st_size);
    close(fd);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc == 4 && strcmp(argv[1], "create") == 0)
        return do_create(argv[2], (off_t)strtoll(argv[3], nullptr, 10));
    if (argc == 3 && strcmp(argv[1], "map") == 0)
        return do_map(argv[2]);
    fprintf(stderr, "usage: %s create PATH OFFSET | map PATH\n", argv[0]);
    return 2;
}
