// EXERCISE: uring3_multishot — multishot accept + multishot recv + provided buffer ring
// TOPIC: io_uring_prep_multishot_accept / recv_multishot / io_uring_setup_buf_ring / IORING_CQE_F_MORE / F_BUFFER
// DIFFICULTY: ★★★★★
// BOOK: man 3 io_uring_prep_multishot_accept；man 3 io_uring_prep_recv_multishot；man 3 io_uring_setup_buf_ring；man 3 io_uring_buf_ring_add
//
// 说明：
//   用法：uring3_multishot PORT      监听 127.0.0.1:PORT，打印 "listening on port N"，echo 服务器
//   uring2 的两个浪费：每次 accept/recv 完成都要重新提交一个请求；每个连接都要预先占着一块
//   recv 缓冲区（1 万个空闲连接 × 64 KiB = 640 MiB 的内存什么也不干）。本题把两者都去掉：
//   - multishot accept（5.19+）：挂一次，每来一个连接就产生一个 CQE
//   - multishot recv（6.0+）+ provided buffer ring（5.19+）：recv 不指定缓冲区，
//     而是带 IOSQE_BUFFER_SELECT 和缓冲区组号 BGID；数据到达时内核才从"缓冲区环"里
//     挑一块空闲缓冲区，把编号放在 cqe->flags >> IORING_CQE_BUFFER_SHIFT（并置 IORING_CQE_F_BUFFER）。
//     所有连接共享这 16 块缓冲区——内存和"正在收数据的连接数"成正比，而非和连接总数成正比
//   - 用完的缓冲区要**还给环**：io_uring_buf_ring_add(br, addr, len, bid, mask, 0) +
//     io_uring_buf_ring_advance(br, 1)。忘了还，16 块用光之后 recv 以 -ENOBUFS 结束，服务器卡死
//   - IORING_CQE_F_MORE：这个 multishot 请求还会继续产生 CQE。**没有 F_MORE 就说明它已经终止**
//     （-ENOBUFS、出错、EOF、内核内部原因……），若连接还活着就要重新提交
//   - 本题收到数据后把它拷进连接自己的发送队列、立刻归还缓冲区，每个连接同时只有一个 SEND 在飞
//     （两个 SEND 同时在飞可能乱序）；连接关闭时若还有 SEND 在飞，先等它完成再 close
//   - 测试：50 个并发客户端大数据回显；单连接连续发几千条小消息（远超 16 块缓冲区）；
//     200 个连接同时涌入各发一条消息（缓冲区环必然被耗尽 → -ENOBUFS → 需要重新提交）；
//     全部断开后 socket fd 回落到只剩监听 socket
//
//   这正是现代 io_uring 运行时的主流形态：monoio / glommio / tokio-uring 的 TCP 读、
//   Seastar 的网络栈都用 provided buffers；新内核还有 recv bundle（一个 CQE 拿多块缓冲区）
//   和 incremental buffer consumption（6.12+，一块大缓冲区被多次 recv 分段消费），见 docs/handoff。
//   不支持时（内核 < 6.0）程序打印 "io_uring unavailable: ..." 并以 77 退出，测试 skip。

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

enum { RING_ENTRIES = 512, MAX_FD = 4096, NBUFS = 16, BUF_SZ = 4096, BGID = 7 };
enum op : uint8_t { OP_ACCEPT = 1, OP_RECV = 2, OP_SEND = 3 };
static_assert((NBUFS & (NBUFS - 1)) == 0, "buffer ring size must be a power of two");

struct conn {
    bool eof;        // 不会再收到数据了（对端关闭 / 出错）
    bool recv_armed; // multishot recv 还在内核里挂着
    bool sending;    // 有一个 SEND 在飞，缓冲区 out 正被内核读取
    char *out;       // 正在发送的数据
    size_t out_len, out_off, out_cap;
    char *pend;      // 发送期间新收到的数据先攒在这里
    size_t pend_len, pend_cap;
};

static struct conn *conns[MAX_FD];
static struct io_uring_buf_ring *br;
static char *bufs; // NBUFS × BUF_SZ 的一整块内存

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

[[noreturn]] static void unsupported(const char *what, int res) {
    printf("io_uring unavailable: %s: %s (need Linux 6.0+)\n", what, strerror(-res));
    exit(77);
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

static inline uint64_t pack(enum op op, int fd) { return (uint64_t)op << 56 | (uint32_t)fd; }
static inline enum op ud_op(uint64_t ud) { return (enum op)(ud >> 56); }
static inline int ud_fd(uint64_t ud) { return (int)(uint32_t)ud; }

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

static void arm_accept(struct io_uring *ring, int lfd) {
    struct io_uring_sqe *sqe = get_sqe(ring);
    io_uring_prep_multishot_accept(sqe, lfd, nullptr, nullptr, SOCK_CLOEXEC);
    io_uring_sqe_set_data64(sqe, pack(OP_ACCEPT, lfd));
}

static void arm_recv(struct io_uring *ring, int fd) {
    struct io_uring_sqe *sqe = get_sqe(ring);
    io_uring_prep_recv_multishot(sqe, fd, nullptr, 0, 0); // 不给缓冲区：由内核从 BGID 组里挑
    sqe->flags |= IOSQE_BUFFER_SELECT;
    sqe->buf_group = BGID;
    io_uring_sqe_set_data64(sqe, pack(OP_RECV, fd));
    conns[fd]->recv_armed = true;
}

static void submit_send(struct io_uring *ring, int fd) {
    struct conn *c = conns[fd];
    struct io_uring_sqe *sqe = get_sqe(ring);
    io_uring_prep_send(sqe, fd, c->out + c->out_off, c->out_len - c->out_off, MSG_NOSIGNAL);
    io_uring_sqe_set_data64(sqe, pack(OP_SEND, fd));
    c->sending = true;
}

// 把编号为 bid 的缓冲区还给缓冲区环，内核之后又可以把它分给任何连接的 recv
static void recycle_buffer(unsigned bid) {
    io_uring_buf_ring_add(br, bufs + (size_t)bid * BUF_SZ, BUF_SZ, (unsigned short)bid,
                          io_uring_buf_ring_mask(NBUFS), 0);
    io_uring_buf_ring_advance(br, 1);
}

static void append(struct conn *c, const char *p, size_t n) {
    if (c->pend_len + n > c->pend_cap) {
        size_t cap = c->pend_cap ? c->pend_cap : 4096;
        while (cap < c->pend_len + n)
            cap *= 2;
        char *np = realloc(c->pend, cap);
        if (np == nullptr)
            sl_die("realloc");
        c->pend = np;
        c->pend_cap = cap;
    }
    memcpy(c->pend + c->pend_len, p, n);
    c->pend_len += n;
}

// 没有 SEND 在飞时：把攒下的数据和 out 交换，发出去（旧 out 缓冲区复用为新的 pend）
static void kick_send(struct io_uring *ring, int fd) {
    struct conn *c = conns[fd];
    if (c->sending || c->pend_len == 0)
        return;
    char *old = c->out;
    size_t old_cap = c->out_cap;
    c->out = c->pend;
    c->out_cap = c->pend_cap;
    c->out_len = c->pend_len;
    c->out_off = 0;
    c->pend = old;
    c->pend_cap = old_cap;
    c->pend_len = 0;
    submit_send(ring, fd);
}

// 既不会再收到数据、也没有请求在飞时才能 close：否则内核还拿着这个 fd 的请求
static void maybe_close(int fd) {
    struct conn *c = conns[fd];
    if (!c->eof || c->recv_armed || c->sending || c->pend_len > 0)
        return;
    if (close(fd) < 0)
        perror("close");
    free(c->out);
    free(c->pend);
    free(c);
    conns[fd] = nullptr;
}

static void on_accept(struct io_uring *ring, int lfd, int res, unsigned flags) {
    if (!(flags & IORING_CQE_F_MORE)) {
        if (res == -EINVAL)
            unsupported("multishot accept", res);
        arm_accept(ring, lfd); // multishot accept 终止了：重新挂上
    }
    if (res < 0) {
        fprintf(stderr, "accept: %s\n", strerror(-res));
        return;
    }
    if (res >= MAX_FD) {
        fprintf(stderr, "fd %d too large, rejecting\n", res);
        close(res);
        return;
    }
    conns[res] = calloc(1, sizeof(struct conn));
    if (conns[res] == nullptr)
        sl_die("calloc");
    arm_recv(ring, res);
}

static void on_recv(struct io_uring *ring, int fd, int res, unsigned flags) {
    struct conn *c = conns[fd];
    if (res > 0) {
        // 数据在内核挑的那块缓冲区里：拷走，然后立刻把缓冲区还给环
        unsigned bid = flags >> IORING_CQE_BUFFER_SHIFT;
        append(c, bufs + (size_t)bid * BUF_SZ, (size_t)res);
        recycle_buffer(bid);
        kick_send(ring, fd);
    } else if (res == 0) {
        c->eof = true; // 对端关闭
    } else if (res == -EINVAL) {
        unsupported("multishot recv", res);
    } else if (res != -ENOBUFS) { // -ENOBUFS：16 块缓冲区暂时全被占用，不是连接的错
        if (res != -ECONNRESET)
            fprintf(stderr, "recv fd %d: %s\n", fd, strerror(-res));
        c->eof = true;
    }
    if (!(flags & IORING_CQE_F_MORE)) { // 这个 multishot recv 已经终止
        c->recv_armed = false;
        if (!c->eof)
            arm_recv(ring, fd); // 连接还活着（例如 -ENOBUFS 之后）：重新挂上
    }
    maybe_close(fd);
}

static void on_send(struct io_uring *ring, int fd, int res) {
    struct conn *c = conns[fd];
    c->sending = false;
    if (res < 0) { // 对端走了：丢掉没发的数据，shutdown 让挂着的 multishot recv 以 EOF 结束
        if (res != -EPIPE && res != -ECONNRESET)
            fprintf(stderr, "send fd %d: %s\n", fd, strerror(-res));
        c->pend_len = 0;
        c->eof = true;
        if (c->recv_armed)
            shutdown(fd, SHUT_RDWR);
        maybe_close(fd);
        return;
    }
    c->out_off += (size_t)res;
    if (c->out_off < c->out_len)
        submit_send(ring, fd); // 短写
    else
        kick_send(ring, fd);
    maybe_close(fd);
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

    // 注册缓冲区环（组号 BGID），并把 NBUFS 块缓冲区全部放进去
    int ret = 0;
    br = io_uring_setup_buf_ring(&ring, NBUFS, BGID, 0, &ret);
    if (br == nullptr) {
        if (ret == -EINVAL || ret == -ENOSYS || ret == -EOPNOTSUPP)
            unsupported("io_uring_setup_buf_ring", ret);
        fprintf(stderr, "io_uring_setup_buf_ring: %s\n", strerror(-ret));
        return 1;
    }
    bufs = malloc((size_t)NBUFS * BUF_SZ);
    if (bufs == nullptr)
        sl_die("malloc");
    for (unsigned i = 0; i < NBUFS; i++)
        recycle_buffer(i);

    int lfd = listen_on(atoi(argv[1]));
    arm_accept(&ring, lfd);
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
            case OP_ACCEPT: on_accept(&ring, ud_fd(ud), cqe->res, cqe->flags); break;
            case OP_RECV: on_recv(&ring, ud_fd(ud), cqe->res, cqe->flags); break;
            case OP_SEND: on_send(&ring, ud_fd(ud), cqe->res); break;
            default: fprintf(stderr, "unknown user_data %#llx\n", (unsigned long long)ud);
            }
        }
        io_uring_cq_advance(&ring, seen);
    }
}
