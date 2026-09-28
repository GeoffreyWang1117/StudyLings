// EXERCISE: uring4_link_timeout — connect → recv 链式提交，并给 recv 挂上 LINK_TIMEOUT
// TOPIC: IORING_OP_CONNECT / IOSQE_IO_LINK / IORING_OP_LINK_TIMEOUT / -ECANCELED / -ETIME
// DIFFICULTY: ★★★★☆
// BOOK: man 3 io_uring_prep_connect；man 3 io_uring_prep_link_timeout；man 2 io_uring_enter（IOSQE_IO_LINK）；UNP §16.3（connect 超时）
// I AM NOT DONE
//
// 说明：
//   用法：uring4_link_timeout HOST PORT TIMEOUT_MS
//   连接 HOST:PORT，读一行并打印；服务器 TIMEOUT_MS 毫秒内一个字节都不发 → 打印 "timeout"，退出 3；
//   连接被拒绝 → 打印 "refused"，退出 2；读到一行 → 打印这一行，退出 0
//   - 三个 SQE 一次提交（一次 io_uring_enter）：
//       CONNECT  ─(IOSQE_IO_LINK)→  RECV  ─(IOSQE_IO_LINK)→  LINK_TIMEOUT
//     IOSQE_IO_LINK 表示"下一个 SQE 要等我成功完成才开始"；我失败了，后面的全部以 -ECANCELED 完成
//   - LINK_TIMEOUT 不是独立的定时器：它只作用于**紧挨在它前面**、带 IOSQE_IO_LINK 的那个请求。
//     RECV 开始时计时开始；RECV 先完成 → 定时器被取消（timeout CQE 的 res = -ECANCELED）；
//     定时器先到 → RECV 被取消（recv CQE res = -ECANCELED），timeout CQE 的 res = -ETIME
//   - 忘了在 RECV 上加 IOSQE_IO_LINK：LINK_TIMEOUT 前面没有可挂的请求 → 它自己以 -EINVAL 完成，
//     RECV 则没有任何期限，对着一个沉默的服务器永远挂着
//   - 一行没读完就继续提交 RECV + LINK_TIMEOUT，直到读到 '\n' 或 EOF
//   - 测试：会回话的服务器 → 打印那一行；只 accept 不说话的服务器 → 在超时附近打印 timeout 退出 3；
//     没人监听的端口 → refused 退出 2
//
//   为什么要这样做：epoll 世界里超时靠 epoll_wait 的 timeout 参数 + 自己维护的定时器堆（N04 epoll3），
//   每个连接的期限都要自己算；io_uring 把"这个操作最多等多久"直接附在操作上，由内核负责取消。
//   Rust 的 monoio / glommio 的 IO 超时、TigerBeetle 的消息总线超时都是这种写法。
//   （UNP 里 connect 超时要靠 alarm/select + 非阻塞 connect，现在一个链就够了。）

#include <errno.h>
#include <liburing.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { LINE_MAX_LEN = 4096 };
enum : uint64_t { UD_CONNECT = 1, UD_RECV = 2, UD_TIMEOUT = 3 };

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

// 准备 RECV（读到 buf+len）+ 紧随其后的 LINK_TIMEOUT。ts 必须在请求完成前一直有效
static void prep_recv_with_timeout(struct io_uring *ring, int fd, char *buf, size_t cap,
                                   struct __kernel_timespec *ts) {
    struct io_uring_sqe *sqe = io_uring_get_sqe(ring);
    io_uring_prep_recv(sqe, fd, buf, cap, 0);
    io_uring_sqe_set_data64(sqe, UD_RECV);
    // TODO: 现在 RECV 和下面的 LINK_TIMEOUT 之间没有链接：LINK_TIMEOUT 找不到要限时的请求，
    //       自己以 -EINVAL 完成，而 RECV 永远等下去（服务器不说话时程序就挂死）。
    //       给这个 SQE 的 flags 加上 IOSQE_IO_LINK，让紧随其后的 LINK_TIMEOUT 作用于它

    sqe = io_uring_get_sqe(ring);
    io_uring_prep_link_timeout(sqe, ts, 0);
    io_uring_sqe_set_data64(sqe, UD_TIMEOUT);
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 4) {
        fprintf(stderr, "usage: %s HOST PORT TIMEOUT_MS\n", argv[0]);
        return 1;
    }
    long ms = atol(argv[3]);
    if (ms <= 0) {
        fprintf(stderr, "TIMEOUT_MS must be > 0\n");
        return 1;
    }

    struct addrinfo hints = {.ai_family = AF_UNSPEC, .ai_socktype = SOCK_STREAM,
                             .ai_flags = AI_NUMERICSERV};
    struct addrinfo *ai;
    int gai = getaddrinfo(argv[1], argv[2], &hints, &ai);
    if (gai != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(gai));
        return 1;
    }
    int fd = socket(ai->ai_family, ai->ai_socktype | SOCK_CLOEXEC, ai->ai_protocol);
    if (fd < 0)
        sl_die("socket");

    struct io_uring ring;
    ring_init_or_skip(&ring, 8, 0);

    struct __kernel_timespec ts = {.tv_sec = ms / 1000, .tv_nsec = (ms % 1000) * 1000000};
    char line[LINE_MAX_LEN + 1];
    size_t len = 0;

    // 第一轮：CONNECT →(link) RECV →(link) LINK_TIMEOUT，一次提交
    struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
    io_uring_prep_connect(sqe, fd, ai->ai_addr, ai->ai_addrlen);
    io_uring_sqe_set_data64(sqe, UD_CONNECT);
    sqe->flags |= IOSQE_IO_LINK; // CONNECT 失败 → 后面的 RECV/TIMEOUT 都以 -ECANCELED 结束
    prep_recv_with_timeout(&ring, fd, line, LINE_MAX_LEN, &ts);
    unsigned expect = 3;

    int status = -1;
    while (status < 0) {
        int r = io_uring_submit_and_wait(&ring, expect);
        if (r < 0 && r != -EINTR) {
            fprintf(stderr, "io_uring_submit_and_wait: %s\n", strerror(-r));
            status = 1;
            break;
        }
        // 收齐本轮所有 CQE（链上每个 SQE 都一定会产生一个 CQE，包括被取消的）
        int connect_res = 0, recv_res = 0, timeout_res = 0;
        unsigned got = 0;
        while (got < expect) {
            struct io_uring_cqe *cqe;
            r = io_uring_wait_cqe(&ring, &cqe);
            if (r == -EINTR)
                continue;
            if (r < 0) {
                fprintf(stderr, "io_uring_wait_cqe: %s\n", strerror(-r));
                return 1;
            }
            switch (io_uring_cqe_get_data64(cqe)) {
            case UD_CONNECT: connect_res = cqe->res; break;
            case UD_RECV: recv_res = cqe->res; break;
            case UD_TIMEOUT: timeout_res = cqe->res; break;
            }
            io_uring_cqe_seen(&ring, cqe);
            got++;
        }

        if (connect_res == -ECONNREFUSED) {
            puts("refused");
            status = 2;
        } else if (connect_res < 0) {
            fprintf(stderr, "connect: %s\n", strerror(-connect_res));
            status = 1;
        } else if (recv_res == -ECANCELED && timeout_res == -ETIME) {
            puts("timeout");
            status = 3;
        } else if (recv_res < 0) {
            fprintf(stderr, "recv: %s (timeout cqe: %d)\n", strerror(-recv_res), timeout_res);
            status = 1;
        } else if (recv_res == 0) { // EOF：输出已有的部分
            if (len > 0)
                printf("%.*s\n", (int)len, line);
            status = len > 0 ? 0 : 1;
        } else {
            len += (size_t)recv_res;
            char *nl = memchr(line, '\n', len);
            if (nl != nullptr || len == LINE_MAX_LEN) {
                size_t n = nl ? (size_t)(nl - line) : len;
                printf("%.*s\n", (int)n, line);
                status = 0;
            } else { // 一行还没收完：再来一轮 RECV + LINK_TIMEOUT
                prep_recv_with_timeout(&ring, fd, line + len, LINE_MAX_LEN - len, &ts);
                expect = 2;
            }
        }
    }

    io_uring_queue_exit(&ring);
    close(fd);
    freeaddrinfo(ai);
    return status;
}
