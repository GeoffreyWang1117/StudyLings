// EXERCISE: uring5_fixed_sqpoll — 注册文件 + 注册缓冲区做文件拷贝，可选 SQPOLL（零系统调用提交）
// TOPIC: io_uring_register_files / io_uring_register_buffers / IOSQE_FIXED_FILE / read_fixed / write_fixed / IORING_SETUP_SQPOLL
// DIFFICULTY: ★★★★☆
// BOOK: man 3 io_uring_register_files；man 3 io_uring_register_buffers；man 3 io_uring_prep_read_fixed；man 2 io_uring_setup（IORING_SETUP_SQPOLL）
//
// 说明：
//   用法：uring5_fixed_sqpoll [--sqpoll] SRC DST     把 SRC 拷贝到 DST（覆盖）
//   - 每个 I/O 请求内核都要做两件"查表"的事：fd → struct file（fdget/fdput，多线程进程里还有原子引用计数），
//     以及把用户缓冲区 pin 住（get_user_pages）。高频 I/O 时这两步很显眼。
//   - io_uring_register_files([src, dst])：一次性把文件登记进 ring 的"固定文件表"，
//     之后 SQE 里的 fd 字段填**表下标**（0 = src，1 = dst），并设置 IOSQE_FIXED_FILE
//   - io_uring_register_buffers(iovecs)：一次性 pin 住 QD 块缓冲区；之后用
//     io_uring_prep_read_fixed / write_fixed，最后一个参数是**缓冲区下标** buf_index
//     （地址必须落在那块已注册缓冲区之内）
//   - 流水线：QD=4 个槽位，每个槽位负责一段 128 KiB：READ_FIXED → WRITE_FIXED → 空闲 → 下一段；
//     读和写都要处理短读/短写（res < 请求长度 → 把剩下的再提交）；res < 0 是 -errno
//   - --sqpoll：IORING_SETUP_SQPOLL 让内核起一个线程（iou-sqp-PID）不停地轮询 SQ，
//     用户态只要把 SQE 写进共享内存、推进 tail——提交**不需要任何系统调用**；
//     完成也不用 io_uring_enter 去等，直接轮询 CQ（io_uring_peek_cqe）。
//     SQPOLL 线程空闲 sq_thread_idle 毫秒后睡眠，liburing 看到 IORING_SQ_NEED_WAKEUP 才会 enter 叫醒它。
//     不允许 SQPOLL（老内核要 CAP_SYS_ADMIN，或被策略禁止，返回 -EPERM）时打印
//     "note: SQPOLL unavailable ..." 并退回普通模式
//   - 测试：多种大小的拷贝结果逐字节相同；strace 里能看到 IORING_REGISTER_FILES / IORING_REGISTER_BUFFERS，
//     看不到对 SRC/DST 的 read/write；--sqpoll 模式下 io_uring_enter 几乎为 0
//
//   谁在用：SPDK 风格的存储引擎、TigerBeetle（注册文件）、ScyllaDB/Seastar；SQPOLL 在"一个核专门跑 I/O"
//   的场景（数据库、存储网关）里用 CPU 换延迟。代价：多占一个内核线程的 CPU；
//   注册缓冲区计入 RLIMIT_MEMLOCK。网络侧的对应物是 IORING_OP_SEND_ZC + 注册缓冲区（见 docs/handoff）。

#include <errno.h>
#include <fcntl.h>
#include <liburing.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/uio.h>
#include <unistd.h>

#include "sl.h"

enum { QD = 4, CHUNK = 128 * 1024, FIX_SRC = 0, FIX_DST = 1 };
enum phase { IDLE, READING, WRITING };

struct slot {
    enum phase phase;
    off_t off;  // 本段在文件中的起点
    size_t len; // 本段长度
    size_t pos; // 当前阶段（读或写）已完成的字节数
};

static struct iovec iov[QD]; // QD 块缓冲区，注册后按下标使用
static struct slot slots[QD];
static bool sqpoll;

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

// 建 ring：想要 SQPOLL 就先试 SQPOLL，不行退回普通模式
static void setup_ring(struct io_uring *ring) {
    if (sqpoll) {
        struct io_uring_params p = {.flags = IORING_SETUP_SQPOLL, .sq_thread_idle = 2000};
        int r = io_uring_queue_init_params(QD * 2, ring, &p);
        if (r == 0)
            return;
        printf("note: SQPOLL unavailable (%s), falling back to normal mode\n", strerror(-r));
        sqpoll = false;
    }
    ring_init_or_skip(ring, QD * 2, 0);
}

// 把 src/dst 登记为固定文件 0/1，把 QD 块缓冲区登记为固定缓冲区 0..QD-1
static bool register_resources(struct io_uring *ring, int src, int dst) {
    int fds[2] = {[FIX_SRC] = src, [FIX_DST] = dst};
    int r = io_uring_register_files(ring, fds, 2);
    if (r < 0) {
        fprintf(stderr, "io_uring_register_files: %s\n", strerror(-r));
        return false;
    }
    r = io_uring_register_buffers(ring, iov, QD);
    if (r < 0) { // -ENOMEM 常见于 RLIMIT_MEMLOCK 太小
        fprintf(stderr, "io_uring_register_buffers: %s\n", strerror(-r));
        return false;
    }
    return true;
}

// 按槽位 i 当前阶段准备 READ_FIXED 或 WRITE_FIXED（从 pos 继续）
static void prep_io(struct io_uring *ring, int i) {
    struct slot *s = &slots[i];
    struct io_uring_sqe *sqe = io_uring_get_sqe(ring); // ring 有 2*QD 项，每槽位最多 1 个在飞
    char *buf = (char *)iov[i].iov_base + s->pos;
    unsigned n = (unsigned)(s->len - s->pos);
    __u64 off = (__u64)(s->off + (off_t)s->pos);
    if (s->phase == READING) {
        io_uring_prep_read_fixed(sqe, FIX_SRC, buf, n, off, i);
    } else {
        io_uring_prep_write_fixed(sqe, FIX_DST, buf, n, off, i);
    }
    sqe->flags |= IOSQE_FIXED_FILE; // fd 字段是固定文件表下标，不是真正的 fd
    io_uring_sqe_set_data64(sqe, (__u64)i);
}

static inline void cpu_relax(void) {
#if defined(__x86_64__) || defined(__i386__)
    __builtin_ia32_pause();
#elif defined(__aarch64__)
    __asm__ volatile("yield");
#endif
}

// 等至少一个 CQE：普通模式 enter 等待；SQPOLL 模式直接轮询共享内存里的 CQ
static int wait_one(struct io_uring *ring, struct io_uring_cqe **cqe) {
    int r = io_uring_submit(ring); // SQPOLL 下通常不进内核：只推进 SQ tail
    if (r < 0)
        return r;
    if (!sqpoll)
        return io_uring_wait_cqe(ring, cqe);
    for (;;) {
        r = io_uring_peek_cqe(ring, cqe);
        if (r != -EAGAIN)
            return r;
        cpu_relax();
    }
}

// 处理一个 CQE；返回 false 表示致命错误
static bool on_cqe(struct io_uring *ring, const struct io_uring_cqe *cqe) {
    int i = (int)io_uring_cqe_get_data64(cqe);
    struct slot *s = &slots[i];
    int res = cqe->res;
    const char *what = s->phase == READING ? "read" : "write";
    if (res == -EAGAIN || res == -EINTR) {
        prep_io(ring, i);
        return true;
    }
    if (res < 0) {
        fprintf(stderr, "%s at %lld: %s\n", what, (long long)(s->off + (off_t)s->pos), strerror(-res));
        return false;
    }
    if (res == 0) {
        fprintf(stderr, "%s at %lld returned 0 (unexpected EOF?)\n", what,
                (long long)(s->off + (off_t)s->pos));
        return false;
    }
    s->pos += (size_t)res;
    if (s->pos < s->len) { // 短读 / 短写：继续本阶段
        prep_io(ring, i);
    } else if (s->phase == READING) { // 读满了 → 同一块缓冲区写出去
        s->phase = WRITING;
        s->pos = 0;
        prep_io(ring, i);
    } else {
        s->phase = IDLE;
    }
    return true;
}

int main(int argc, char *argv[]) {
    int a = 1;
    if (argc > 1 && strcmp(argv[1], "--sqpoll") == 0) {
        sqpoll = true;
        a++;
    }
    if (argc - a != 2) {
        fprintf(stderr, "usage: %s [--sqpoll] SRC DST\n", argv[0]);
        return 2;
    }
    int src = open(argv[a], O_RDONLY | O_CLOEXEC);
    if (src < 0)
        sl_die(argv[a]);
    int dst = open(argv[a + 1], O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0644);
    if (dst < 0)
        sl_die(argv[a + 1]);
    struct stat st;
    if (fstat(src, &st) < 0)
        sl_die("fstat");
    off_t size = st.st_size;

    for (int i = 0; i < QD; i++) {
        iov[i].iov_base = malloc(CHUNK);
        if (iov[i].iov_base == nullptr)
            sl_die("malloc");
        iov[i].iov_len = CHUNK;
    }

    struct io_uring ring;
    setup_ring(&ring);
    if (sqpoll)
        printf("mode: sqpoll\n");
    int status = 0;
    if (!register_resources(&ring, src, dst)) {
        status = 1;
        goto out;
    }

    off_t next = 0; // 下一段的起点
    for (;;) {
        for (int i = 0; i < QD && next < size; i++) {
            if (slots[i].phase != IDLE)
                continue;
            slots[i] = (struct slot){.phase = READING, .off = next,
                                     .len = (size_t)(size - next < CHUNK ? size - next : CHUNK)};
            next += (off_t)slots[i].len;
            prep_io(&ring, i);
        }
        int busy = 0; // 非 IDLE 的槽位数
        for (int i = 0; i < QD; i++)
            busy += slots[i].phase != IDLE;
        if (busy == 0)
            break; // 全部拷完

        struct io_uring_cqe *cqe;
        int r = wait_one(&ring, &cqe);
        if (r == -EINTR)
            continue;
        if (r < 0) {
            fprintf(stderr, "wait: %s\n", strerror(-r));
            status = 1;
            break;
        }
        bool ok = on_cqe(&ring, cqe);
        io_uring_cqe_seen(&ring, cqe);
        if (!ok) {
            status = 1;
            break;
        }
    }

out:
    io_uring_queue_exit(&ring); // 同时注销固定文件/缓冲区
    for (int i = 0; i < QD; i++)
        free(iov[i].iov_base);
    close(src);
    if (close(dst) < 0) {
        perror("close dst");
        status = 1;
    }
    return status;
}
