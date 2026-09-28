// EXERCISE: uring1_read_batch — 用 io_uring 并发批量读文件（QD=8）
// TOPIC: io_uring_queue_init / io_uring_get_sqe / io_uring_prep_read / submit_and_wait / CQE 收割
// DIFFICULTY: ★★★☆☆
// BOOK: man 7 io_uring；man 3 io_uring_prep_read；man 3 io_uring_submit_and_wait；modern Linux notes（5.1+）
// I AM NOT DONE
//
// 说明：
//   用法：uring1_read_batch FILE      把 FILE 原样写到 stdout（像 cat，但读文件全部走 io_uring）
//   - 文件按固定 64 KiB 切块；同时最多 QD=8 个 IORING_OP_READ 在飞，各读各的 offset
//   - CQE 完成的顺序不保证等于提交顺序！每块读完后先放在自己的槽位里，
//     按块号顺序依次 write 到 stdout（"乱序完成、顺序输出"）
//   - 短读（cqe->res < 请求长度）：把剩下的部分重新提交（offset / buf 前移）
//   - 出错：io_uring 不设置 errno，而是把 -errno 放进 cqe->res（例如 -EIO、-EBADF）；
//     liburing 的函数也同样返回 -errno。-EAGAIN / -EINTR 重试，其它打印 strerror(-res) 退出 1
//   - 测试：0 字节、1 字节、64K-1、1 MiB+123 字节的文件内容必须一模一样；
//     strace 下不允许出现对该文件的 read/pread64，且 io_uring_enter 次数要远少于块数
//
//   io_uring 和 epoll（N04）的根本区别：
//   * epoll 是"就绪通知"（readiness）：内核告诉你"现在可以读了"，你还得自己调用 read，
//     每个 I/O 至少一次系统调用；而且普通文件永远"就绪"，epoll 对磁盘 I/O 毫无帮助。
//   * io_uring 是"完成通知"（completion）：你把"请帮我读 fd 的 [off, off+len) 到 buf"写进
//     提交队列 SQ（一个和内核共享的环形数组），内核做完后把结果写进完成队列 CQ。
//     一次 io_uring_enter 可以提交 N 个请求、顺便收割 M 个完成——系统调用次数大幅减少，
//     在 Spectre/Meltdown 缓解让系统调用变贵之后尤其明显。
//   * 两个 ring 都是 mmap 共享内存，用户态靠 head/tail 原子变量和内核交接（N06 的 SPSC ring！）。
//   谁在用：Rust 的 tokio-uring / monoio / glommio，TigerBeetle（全部 I/O 走 io_uring），
//   ScyllaDB/Seastar，Node.js 的 libuv 1.45+（文件操作），QEMU 块设备后端，RocksDB 的 MultiGet。
//   注意：Docker 默认 seccomp 配置拦截 io_uring，部分发行版用 sysctl kernel.io_uring_disabled
//   关掉它（它也是内核漏洞的重灾区）。本章所有程序在 io_uring_queue_init 返回 -EPERM/-ENOSYS 时
//   打印 "io_uring unavailable: ..." 并以 77 退出，测试据此 skip。

#include <errno.h>
#include <fcntl.h>
#include <liburing.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include "sl.h"

enum { QD = 8, CHUNK = 64 * 1024 };

struct slot {
    char *buf;
    off_t off;    // 本块在文件中的起点
    size_t len;   // 本块总长度
    size_t got;   // 已经读到的字节数
    bool done;    // 整块读完，等待按顺序输出
};

static void ring_init_or_skip(struct io_uring *ring, unsigned entries, unsigned flags) {
    int r = io_uring_queue_init(entries, ring, flags);
    if (r == -EPERM || r == -ENOSYS || r == -EACCES) {
        printf("io_uring unavailable: io_uring_queue_init: %s\n", strerror(-r));
        exit(77);
    }
    if (r < 0) {
        fprintf(stderr, "io_uring_queue_init: %s\n", strerror(-r));
        exit(1);
    }
}

static void write_all(int fd, const char *p, size_t n) {
    while (n > 0) {
        ssize_t w = write(fd, p, n);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            sl_die("write");
        }
        p += w;
        n -= (size_t)w;
    }
}

// 为 chunk 号为 idx 的块（槽位 s）准备一个 READ SQE：读 [off+got, off+len)。
// user_data 放块号，完成时靠它找回槽位。成功返回 true
static bool prep_chunk(struct io_uring *ring, int fd, struct slot *s, size_t idx) {
    // TODO: 1) io_uring_get_sqe 取一个空 SQE（返回 nullptr 表示 SQ 满了 → return false）
    //       2) io_uring_prep_read(sqe, fd, 目标地址, 长度, 文件偏移)：
    //          从 s->buf + s->got 开始，读 s->len - s->got 字节，文件偏移 s->off + s->got
    //          （这样短读后再调用本函数，就自动只读"剩下的部分"）
    //       3) io_uring_sqe_set_data64(sqe, idx)：完成时靠 user_data 找回是哪一块
    (void)ring, (void)fd, (void)s, (void)idx;
    return false;
}

// 处理一个 CQE。返回 false 表示致命错误
static bool complete_chunk(struct io_uring *ring, int fd, struct slot *slots,
                           const struct io_uring_cqe *cqe) {
    size_t idx = (size_t)io_uring_cqe_get_data64(cqe);
    struct slot *s = &slots[idx % QD];
    int res = cqe->res;
    // TODO: 这里假设每次都整块读满，而且从不出错。请补上：
    //   - res 是 -EAGAIN / -EINTR：原样重新提交（prep_chunk）
    //   - res < 0：io_uring 用 -errno 报错（不设置 errno！），打印 strerror(-res) 并 return false
    //   - res == 0：文件在读的过程中变短了（意外 EOF），return false
    //   - 0 < res：s->got += res；若 s->got < s->len 是短读 → 再 prep_chunk 提交剩下的部分
    //   - 只有整块读满才 s->done = true
    (void)ring, (void)fd;
    s->got = s->len;
    s->done = true;
    (void)res;
    return true;
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
    size_t size = (size_t)st.st_size;
    size_t nchunks = (size + CHUNK - 1) / CHUNK;

    struct io_uring ring;
    ring_init_or_skip(&ring, QD * 2, 0);

    struct slot slots[QD] = {};
    for (int i = 0; i < QD; i++) {
        slots[i].buf = malloc(CHUNK);
        if (slots[i].buf == nullptr)
            sl_die("malloc");
    }

    size_t next_submit = 0; // 下一个要提交的块号
    size_t next_write = 0;  // 下一个要输出的块号
    int status = 0;
    while (next_write < nchunks) {
        // 1) 窗口内还有空槽位就继续提交：块 k 占用槽位 k % QD，块 k 输出后槽位才能复用
        while (next_submit < nchunks && next_submit < next_write + QD) {
            struct slot *s = &slots[next_submit % QD];
            s->off = (off_t)(next_submit * CHUNK);
            s->len = next_submit + 1 < nchunks ? CHUNK : size - next_submit * CHUNK;
            s->got = 0;
            s->done = false;
            if (!prep_chunk(&ring, fd, s, next_submit)) {
                fprintf(stderr, "prep_chunk failed\n");
                status = 1;
                goto out;
            }
            next_submit++;
        }

        // 2) 一次系统调用：提交全部 SQE，并至少等 1 个完成
        int r = io_uring_submit_and_wait(&ring, 1);
        if (r < 0 && r != -EINTR) {
            fprintf(stderr, "io_uring_submit_and_wait: %s\n", strerror(-r));
            status = 1;
            goto out;
        }

        // 3) 把 CQ 里已有的完成全部收割掉，再一次性推进 CQ head
        struct io_uring_cqe *cqe;
        unsigned head, seen = 0;
        bool ok = true;
        io_uring_for_each_cqe(&ring, head, cqe) {
            seen++;
            if (!complete_chunk(&ring, fd, slots, cqe)) {
                ok = false;
                break;
            }
        }
        io_uring_cq_advance(&ring, seen);
        if (!ok) {
            status = 1;
            goto out;
        }

        // 4) 按块号顺序输出已经读完的块
        while (next_write < next_submit && slots[next_write % QD].done) {
            struct slot *s = &slots[next_write % QD];
            write_all(STDOUT_FILENO, s->buf, s->len);
            s->done = false;
            next_write++;
        }
    }

out:
    io_uring_queue_exit(&ring); // 正常路径上此时已无在飞请求；出错路径直接退出进程也无妨
    for (int i = 0; i < QD; i++)
        free(slots[i].buf);
    close(fd);
    return status;
}
