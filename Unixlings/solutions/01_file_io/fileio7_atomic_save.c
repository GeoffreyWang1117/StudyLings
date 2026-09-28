// EXERCISE: fileio7_atomic_save — 原子地替换文件：写临时文件 + fsync + rename
// TOPIC: mkstemp / fsync / rename 原子性 / 崩溃一致性
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §4.16（rename）、§3.13（fsync/fdatasync）；man 2 rename "atomically replaced"
//
// 说明：
//   用法：fileio7_atomic_save PATH < new_content
//   用 stdin 的全部内容替换 PATH。现在的实现 open(O_TRUNC) 然后写：
//   写到一半进程崩溃/断电，或者另一个进程恰好此时读取，就会看到一个空的/只有一半的文件。
//   配置热加载、etcd/Consul 落盘、SQLite 的日志、编辑器保存文件、Kubernetes ConfigMap 更新，都用这个套路：
//     1. 在同一个目录下创建临时文件（rename 只在同一文件系统内是原子的）：mkstemp("PATH.tmpXXXXXX")
//     2. 写入全部内容，fsync(tmpfd) —— 保证数据先落盘
//     3. rename(tmp, PATH) —— 读者要么看到完整的旧文件，要么看到完整的新文件
//     4. fsync 所在目录的 fd —— 保证 "rename 这件事" 也落盘
//     5. 任何一步失败都要 unlink 临时文件，不留垃圾
//   测试会用 strace 检查：从未以 O_TRUNC 打开 PATH；fsync 发生在 rename 之前；最终内容正确、没有残留临时文件。

#include <errno.h>
#include <fcntl.h>
#include <libgen.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

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

// 读完 stdin，返回 malloc 出来的缓冲区（调用者 free）
static char *slurp_stdin(size_t *len) {
    size_t cap = 65536, n = 0;
    char *buf = malloc(cap);
    for (;;) {
        if (!buf)
            return nullptr;
        if (n == cap) {
            char *p = realloc(buf, cap *= 2);
            if (!p) {
                free(buf);
                return nullptr;
            }
            buf = p;
        }
        ssize_t r = read(STDIN_FILENO, buf + n, cap - n);
        if (r < 0 && errno == EINTR)
            continue;
        if (r < 0) {
            free(buf);
            return nullptr;
        }
        if (r == 0)
            break;
        n += (size_t)r;
    }
    *len = n;
    return buf;
}

// TODO: 按说明中的 5 步原子地替换 path。成功返回 0，失败返回 -1
static int atomic_save(const char *path, const char *data, size_t len) {
    char tmp[4096];
    if (snprintf(tmp, sizeof tmp, "%s.tmpXXXXXX", path) >= (int)sizeof tmp) {
        errno = ENAMETOOLONG;
        return -1;
    }
    int fd = mkostemp(tmp, O_CLOEXEC); // 同目录、唯一名字、O_EXCL 创建，权限 0600
    if (fd < 0)
        return -1;
    if (fchmod(fd, 0644) < 0 || write_all(fd, data, len) < 0 || fsync(fd) < 0) {
        int saved = errno;
        close(fd);
        unlink(tmp);
        errno = saved;
        return -1;
    }
    if (close(fd) < 0 || rename(tmp, path) < 0) {
        int saved = errno;
        unlink(tmp);
        errno = saved;
        return -1;
    }

    // 让目录项的变化（rename）也持久化
    char dirbuf[4096];
    snprintf(dirbuf, sizeof dirbuf, "%s", path);
    int dfd = open(dirname(dirbuf), O_RDONLY | O_DIRECTORY | O_CLOEXEC);
    if (dfd < 0)
        return -1;
    int rc = fsync(dfd);
    close(dfd);
    return rc;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s PATH < content\n", argv[0]);
        return 2;
    }
    size_t len;
    char *data = slurp_stdin(&len);
    if (!data) {
        perror("read stdin");
        return 1;
    }
    int rc = atomic_save(argv[1], data, len);
    if (rc < 0)
        perror(argv[1]);
    free(data);
    return rc < 0 ? 1 : 0;
}
