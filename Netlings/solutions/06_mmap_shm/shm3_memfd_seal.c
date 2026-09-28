// EXERCISE: shm3_memfd_seal — memfd_create + 文件封印：把一块共享内存变成"只读、不可变"再交给别人
// TOPIC: memfd_create / MFD_ALLOW_SEALING / fcntl(F_ADD_SEALS) / F_SEAL_WRITE|SHRINK|GROW|SEAL
// DIFFICULTY: ★★★☆☆
// BOOK: man 2 memfd_create；man 2 fcntl（File Sealing 一节）；APUE §14.8 / §15.9（共享存储）
//
// 说明：
//   用法：shm3_memfd_seal
//   1. memfd_create 创建一个匿名内存文件（没有路径，只有 fd），写入一段数据 PAYLOAD；
//   2. 用 fcntl(fd, F_ADD_SEALS, F_SEAL_WRITE | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_SEAL) 封印它；
//   3. fork：子进程继承 fd（模拟"把 fd 通过 SCM_RIGHTS 交给不信任的对端"），
//      mmap(PROT_READ, MAP_SHARED) 校验内容，然后故意尝试破坏它：
//        write(fd)、ftruncate(fd) 缩小/扩大、mmap(PROT_WRITE, MAP_SHARED)、再加/去掉封印
//      —— 这些都必须失败，errno == EPERM。子进程逐行打印结果，例如 "write: EPERM"。
//   4. 父进程 waitpid，打印 "child exit <code>"。
//
//   为什么需要封印：接收方拿到一块共享内存时，如果发送方还能随时改内容或者把文件截短，
//   接收方就会遇到 TOCTOU（先校验后使用之间被改）或者访问被截掉的页时 SIGBUS 崩溃。
//   封印之后，**任何人**（包括创建者自己）都不能再改，接收方可以放心地"校验一次、一直使用"。
//
//   谁在用：Wayland 合成器与客户端共享 wl_shm 缓冲区和 keymap（封印防止客户端让合成器 SIGBUS）；
//   Android ashmem 的替代品就是 memfd；systemd-journald 接收 memfd 传来的大日志；
//   Chrome / Firefox 沙箱在进程间传只读的共享数据；Flatpak / bubblewrap 传配置。

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>

#include "sl.h"

static const char PAYLOAD[] = "frame #42: immutable pixels, verified once, used forever\n";

// 打印一次"破坏尝试"的结果：期望失败且 errno == EPERM。符合期望返回 true
static bool report(const char *what, int rc) {
    if (rc >= 0) {
        printf("%s: succeeded (!)\n", what);
        return false;
    }
    printf("%s: %s\n", what, errno == EPERM ? "EPERM" : strerror(errno));
    return errno == EPERM;
}

static int child(int fd) {
    bool ok = true;
    size_t len = sizeof PAYLOAD - 1;

    // 只读映射并校验内容
    char *p = mmap(nullptr, len, PROT_READ, MAP_SHARED, fd, 0);
    if (p == MAP_FAILED) {
        perror("child mmap(PROT_READ)");
        return 1;
    }
    bool same = memcmp(p, PAYLOAD, len) == 0;
    printf("content: %s\n", same ? "ok" : "MISMATCH");
    ok = ok && same;

    // 逐一尝试破坏
    ok &= report("write", (int)pwrite(fd, "X", 1, 0));
    ok &= report("ftruncate-shrink", ftruncate(fd, 1));
    ok &= report("ftruncate-grow", ftruncate(fd, 1 << 20));
    void *w = mmap(nullptr, len, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    ok &= report("mmap-write", w == MAP_FAILED ? -1 : 0);
    if (w != MAP_FAILED)
        munmap(w, len);
    ok &= report("add-seal", fcntl(fd, F_ADD_SEALS, F_SEAL_SHRINK)); // F_SEAL_SEAL：封印集合也被冻结

    // 映射里看到的内容仍然完好
    bool still = memcmp(p, PAYLOAD, len) == 0;
    printf("after attacks: %s\n", still ? "intact" : "MODIFIED");
    ok = ok && still;
    munmap(p, len);
    return ok ? 0 : 1;
}

int main(void) {
    setvbuf(stdout, nullptr, _IOLBF, 0);

    // MFD_ALLOW_SEALING：不加这个标志，memfd 一创建就带着 F_SEAL_SEAL，之后什么封印都加不上
    int fd = memfd_create("netlings-frame", MFD_CLOEXEC | MFD_ALLOW_SEALING);
    if (fd < 0)
        sl_die("memfd_create");

    size_t len = sizeof PAYLOAD - 1;
    if (write(fd, PAYLOAD, len) != (ssize_t)len)
        sl_die("write");

    // 封印：之后谁都不能再写、缩小、扩大，也不能再改封印集合
    if (fcntl(fd, F_ADD_SEALS, F_SEAL_WRITE | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_SEAL) < 0)
        sl_die("F_ADD_SEALS");

    int seals = fcntl(fd, F_GET_SEALS);
    if (seals < 0)
        sl_die("F_GET_SEALS");
    printf("seals=0x%x\n", seals);

    pid_t pid = fork();
    if (pid < 0)
        sl_die("fork");
    if (pid == 0) {
        int rc = child(fd);
        fflush(stdout);
        _exit(rc);
    }

    int status;
    if (waitpid(pid, &status, 0) < 0)
        sl_die("waitpid");
    close(fd);
    int code = WIFEXITED(status) ? WEXITSTATUS(status) : 128 + WTERMSIG(status);
    printf("child exit %d\n", code);
    return code == 0 ? 0 : 1;
}
