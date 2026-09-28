// EXERCISE: fileio6_walk — 用 openat/fstatat 递归遍历目录，不跟随符号链接
// TOPIC: openat / fdopendir / fstatat(AT_SYMLINK_NOFOLLOW) / 目录 fd
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §4.2-4.3（stat/lstat）、§4.22（读目录，图 4.22 的 ftw 实现）、§3.3（openat 系列）
// I AM NOT DONE
//
// 说明：
//   用法：fileio6_walk DIR
//   对 DIR 下的每个条目（递归，不含 DIR 本身）打印一行：
//       f <size> <相对路径>     普通文件
//       d - <相对路径>          目录
//       l <size> <相对路径>     符号链接（size 为链接自身的 lstat 大小，即目标路径长度）
//       o - <相对路径>          其他（FIFO、socket、设备）
//   输出顺序不限（测试会排序）。
//   要点：
//   1. 用 "目录 fd + 相对名字"（openat/fstatat/fdopendir），而不是每次拼出完整路径再 stat：
//      路径很深时不会超过 PATH_MAX，也避免了"检查后被替换成符号链接"的 TOCTOU 竞态。
//      这就是 find、rm -rf、Go 的 os.RemoveAll、Rust 的 remove_dir_all 修过的那类安全漏洞。
//   2. 必须用 AT_SYMLINK_NOFOLLOW：测试目录里有一个指向父目录的符号链接，跟随它就会无限递归。

#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

static int walk(int dirfd, const char *prefix) {
    DIR *d = fdopendir(dirfd); // 成功后 dirfd 归 DIR 所有，closedir 会关闭它
    if (!d) {
        perror("fdopendir");
        close(dirfd);
        return -1;
    }
    int rc = 0;
    struct dirent *e;
    while ((e = readdir(d)) != nullptr) {
        if (strcmp(e->d_name, ".") == 0 || strcmp(e->d_name, "..") == 0)
            continue;
        char path[4096];
        snprintf(path, sizeof path, "%s%s%s", prefix, *prefix ? "/" : "", e->d_name);

        struct stat st;
        // TODO: 查询条目本身的信息 —— 符号链接不能被跟随
        if (fstatat(dirfd, e->d_name, &st, 0) < 0) {
            perror(path);
            rc = -1;
            continue;
        }
        if (S_ISREG(st.st_mode)) {
            printf("f %lld %s\n", (long long)st.st_size, path);
        } else if (S_ISDIR(st.st_mode)) {
            printf("d - %s\n", path);
            // TODO: 用 openat(dirfd, 名字, O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC) 打开子目录，
            //       然后递归 walk(subfd, path)
        } else if (S_ISLNK(st.st_mode)) {
            printf("l %lld %s\n", (long long)st.st_size, path);
        } else {
            printf("o - %s\n", path);
        }
    }
    closedir(d);
    return rc;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s DIR\n", argv[0]);
        return 2;
    }
    int fd = open(argv[1], O_RDONLY | O_DIRECTORY | O_CLOEXEC);
    if (fd < 0) {
        perror(argv[1]);
        return 1;
    }
    return walk(fd, "") == 0 ? 0 : 1;
}
