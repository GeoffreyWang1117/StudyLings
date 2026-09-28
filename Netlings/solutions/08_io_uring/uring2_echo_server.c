// EXERCISE: uring2_echo_server — 单线程 io_uring echo 服务器（accept / recv / send 全异步）
// TOPIC: io_uring_prep_accept / prep_recv / prep_send / user_data 编码 / 短写 / 连接生命周期
// DIFFICULTY: ★★★★☆
// BOOK: man 3 io_uring_prep_accept；man 3 io_uring_prep_recv；man 3 io_uring_prep_send；UNP §5（echo 模型）
//
// 说明：
//   用法：uring2_echo_server PORT      监听 127.0.0.1:PORT，打印 "listening on port N"
//   - 没有 epoll_wait、没有非阻塞 read/write：所有 I/O 都是提交给内核的"请求"，
//     主循环只做一件事：io_uring_submit_and_wait → 按 CQE 的 user_data 分派
//   - user_data（64 位）编码三样东西：操作类型 op（高 8 位）| 缓冲区下标 bidx（16 位）| fd（低 32 位），
//     完成时解码就知道"哪个连接的哪种操作完成了、数据在哪块缓冲区"——不用任何查表
//   - ACCEPT 完成：res 是新连接 fd（或 -errno）。无论成败都要**重新提交一个 ACCEPT**，
//     否则只能接受一个连接（单次 accept 请求只完成一次；多次触发的写法见 uring3）
//   - RECV 完成：res > 0 → 把这些字节 SEND 回去；res == 0 → 对端关闭；res < 0 → -errno。
//     后两种都要 close(fd) 并归还缓冲区
//   - SEND 完成：res 可能小于请求长度（短写！对端读得慢、发送缓冲区快满时很常见），
//     要把剩下的部分再提交一次；全部发完才能再提交下一个 RECV
//   - 每个连接同一时刻只有一个请求在飞（recv → send → recv …），所以缓冲区不会被两个请求共享
//   - 测试：50 个并发客户端、大块数据（几 MiB，客户端故意读得慢）、客户端中途断开；
//     全部断开后服务器持有的 socket 要回落到只剩监听 socket（/proc/PID/fd 检查）
//
//   对比 N04 的 epoll 服务器："就绪 → 我来 read"变成"我先把 recv 交给内核，数据到了内核直接
//   拷进我的缓冲区再通知我"。好处是系统调用少（一次 io_uring_enter 批量提交/收割），
//   代价是缓冲区必须在请求完成前一直有效——这就是 tokio-uring / monoio 要求 "owned buffer"
//   （把缓冲区所有权交给运行时）的原因，也是 uring3 引入"内核挑选缓冲区"（provided buffers）的动机。

#include <arpa/inet.h>
#include <errno.h>
#include <liburing.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { RING_ENTRIES = 256, MAX_CONN = 512, BUF_SIZE = 64 * 1024 };
enum op : uint8_t { OP_ACCEPT = 1, OP_RECV = 2, OP_SEND = 3 };

struct conn {
    char buf[BUF_SIZE];
    size_t len;  // buf 中待发送的总字节数
    size_t sent; // 已经发出的字节数
};

static struct conn *conns;        // 缓冲区池：MAX_CONN 个
static uint16_t free_list[MAX_CONN];
static int n_free;

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

static int listen_on(int port) {
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    int one = 1;
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one) < 0)
        sl_die("setsockopt");
    struct sockaddr_in addr = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(fd, (struct sockaddr *)&addr, sizeof addr) < 0)
        sl_die("bind");
    if (listen(fd, SOMAXCONN) < 0)
        sl_die("listen");
    return fd;
}

// ---- user_data 编码：| op:8 | 0:8 | bidx:16 | fd:32 | ----
static inline uint64_t pack(enum op op, uint16_t bidx, int fd) {
    return (uint64_t)op << 56 | (uint64_t)bidx << 32 | (uint32_t)fd;
}
static inline enum op ud_op(uint64_t ud) { return (enum op)(ud >> 56); }
static inline uint16_t ud_bidx(uint64_t ud) { return (uint16_t)(ud >> 32); }
static inline int ud_fd(uint64_t ud) { return (int)(uint32_t)ud; }

// 取一个 SQE；SQ 满了就先把已有的提交掉再取（不会等待任何完成）
static struct io_uring_sqe *get_sqe(struct io_uring *ring) {
    struct io_uring_sqe *sqe = io_uring_get_sqe(ring);
    while (sqe == nullptr) {
        int r = io_uring_submit(ring);
        if (r < 0 && r != -EINTR && r != -EAGAIN && r != -EBUSY) {
            fprintf(stderr, "io_uring_submit: %s\n", strerror(-r));
            exit(1);
        }
        sqe = io_uring_get_sqe(ring);
    }
    return sqe;
}

static void submit_accept(struct io_uring *ring, int lfd) {
    struct io_uring_sqe *sqe = get_sqe(ring);
    io_uring_prep_accept(sqe, lfd, nullptr, nullptr, SOCK_CLOEXEC);
    io_uring_sqe_set_data64(sqe, pack(OP_ACCEPT, 0, lfd));
}

static void submit_recv(struct io_uring *ring, int fd, uint16_t bidx) {
    struct io_uring_sqe *sqe = get_sqe(ring);
    io_uring_prep_recv(sqe, fd, conns[bidx].buf, BUF_SIZE, 0);
    io_uring_sqe_set_data64(sqe, pack(OP_RECV, bidx, fd));
}

// 发送 buf[sent, len)
static void submit_send(struct io_uring *ring, int fd, uint16_t bidx) {
    struct conn *c = &conns[bidx];
    struct io_uring_sqe *sqe = get_sqe(ring);
    io_uring_prep_send(sqe, fd, c->buf + c->sent, c->len - c->sent, MSG_NOSIGNAL);
    io_uring_sqe_set_data64(sqe, pack(OP_SEND, bidx, fd));
}

static void close_conn(int fd, uint16_t bidx) {
    if (close(fd) < 0)
        perror("close");
    free_list[n_free++] = bidx;
}

static void on_accept(struct io_uring *ring, int lfd, int res) {
    // 单次 ACCEPT 只完成一次：无论成败，先把下一个 ACCEPT 挂上
    submit_accept(ring, lfd);
    if (res < 0) {
        fprintf(stderr, "accept: %s\n", strerror(-res)); // EMFILE 等：下一个 accept 已经挂上了
        return;
    }
    if (n_free == 0) {
        fprintf(stderr, "too many connections, rejecting fd %d\n", res);
        close(res);
        return;
    }
    // 把发送缓冲区设小（内核实际会翻倍）：一次 64 KiB 的 SEND 基本总会只发出一部分——
    // 大量连接的服务器为了省内存也常这么做。短写因此一定会出现，而不是"偶尔"
    int sndbuf = 16 * 1024;
    if (setsockopt(res, SOL_SOCKET, SO_SNDBUF, &sndbuf, sizeof sndbuf) < 0)
        perror("setsockopt SO_SNDBUF");
    uint16_t bidx = free_list[--n_free];
    conns[bidx].len = conns[bidx].sent = 0;
    submit_recv(ring, res, bidx);
}

static void on_recv(struct io_uring *ring, int fd, uint16_t bidx, int res) {
    if (res <= 0) { // 0 = 对端关闭；<0 = -errno（如 -ECONNRESET）
        if (res < 0 && res != -ECONNRESET)
            fprintf(stderr, "recv fd %d: %s\n", fd, strerror(-res));
        close_conn(fd, bidx);
        return;
    }
    conns[bidx].len = (size_t)res;
    conns[bidx].sent = 0;
    submit_send(ring, fd, bidx);
}

static void on_send(struct io_uring *ring, int fd, uint16_t bidx, int res) {
    if (res < 0) { // -EPIPE / -ECONNRESET：对端没读完就走了
        if (res != -EPIPE && res != -ECONNRESET)
            fprintf(stderr, "send fd %d: %s\n", fd, strerror(-res));
        close_conn(fd, bidx);
        return;
    }
    struct conn *c = &conns[bidx];
    c->sent += (size_t)res;
    if (c->sent < c->len) { // 短写：把剩下的再发一次
        submit_send(ring, fd, bidx);
        return;
    }
    submit_recv(ring, fd, bidx);
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    signal(SIGPIPE, SIG_IGN);

    struct io_uring ring;
    ring_init_or_skip(&ring, RING_ENTRIES, 0);
    conns = calloc(MAX_CONN, sizeof *conns);
    if (conns == nullptr)
        sl_die("calloc");
    for (int i = MAX_CONN - 1; i >= 0; i--)
        free_list[n_free++] = (uint16_t)i;

    int lfd = listen_on(atoi(argv[1]));
    submit_accept(&ring, lfd);
    printf("listening on port %s\n", argv[1]);

    for (;;) {
        int r = io_uring_submit_and_wait(&ring, 1);
        if (r < 0 && r != -EINTR) {
            fprintf(stderr, "io_uring_submit_and_wait: %s\n", strerror(-r));
            return 1;
        }
        struct io_uring_cqe *cqe;
        unsigned head, seen = 0;
        io_uring_for_each_cqe(&ring, head, cqe) {
            seen++;
            uint64_t ud = io_uring_cqe_get_data64(cqe);
            switch (ud_op(ud)) {
            case OP_ACCEPT: on_accept(&ring, ud_fd(ud), cqe->res); break;
            case OP_RECV: on_recv(&ring, ud_fd(ud), ud_bidx(ud), cqe->res); break;
            case OP_SEND: on_send(&ring, ud_fd(ud), ud_bidx(ud), cqe->res); break;
            default: fprintf(stderr, "unknown user_data %#llx\n", (unsigned long long)ud);
            }
        }
        io_uring_cq_advance(&ring, seen);
    }
}
