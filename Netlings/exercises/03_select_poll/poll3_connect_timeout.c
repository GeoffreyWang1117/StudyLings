// EXERCISE: poll3_connect_timeout — 带超时的非阻塞 connect
// TOPIC: O_NONBLOCK / EINPROGRESS / poll(POLLOUT) / getsockopt(SO_ERROR)
// DIFFICULTY: ★★★☆☆
// BOOK: UNP §16.3-16.4 (nonblocking connect)；man 2 connect（EINPROGRESS 一段）
// I AM NOT DONE
//
// 说明：
//   用法：poll3_connect_timeout HOST PORT TIMEOUT_MS
//   - 连接成功：打印 "connected"，退出码 0
//   - 对端拒绝（端口没人监听，收到 RST）：打印 "refused"，退出码 2
//   - TIMEOUT_MS 毫秒内既没连上也没被拒绝：打印 "timeout"，退出码 3
//   - 其他错误：打印原因到 stderr，退出码 1
//
//   阻塞的 connect(2) 没有超时参数：对一个"黑洞"地址（SYN 被丢弃、没有任何回应），
//   Linux 会按 tcp_syn_retries=6 重传 SYN，要等 2 分钟多才返回 ETIMEDOUT。
//   所有正经的客户端库都自己实现连接超时：
//     1. socket 设成非阻塞（SOCK_NONBLOCK 或 fcntl O_NONBLOCK）
//     2. connect 立即返回 -1 / EINPROGRESS（本机回环也可能直接成功，返回 0）
//     3. poll 等 POLLOUT，带超时；超时 → 放弃
//     4. 可写之后用 getsockopt(SO_ERROR) 取出真正的结果：0 成功，ECONNREFUSED 等为失败
//   Go 的 net.DialTimeout、libuv 的 uv_tcp_connect + timer、tokio::time::timeout(TcpStream::connect)、
//   nginx 的 proxy_connect_timeout、Redis 客户端 hiredis 的 connect timeout 都是这个套路。
//   测试会用"accept 队列已满的监听 socket"在本机制造一个确定性的黑洞。

#include <errno.h>
#include <netdb.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

enum result { R_CONNECTED = 0, R_ERROR = 1, R_REFUSED = 2, R_TIMEOUT = 3 };

[[maybe_unused]] static long long now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

static enum result classify(int err) {
    if (err == 0)
        return R_CONNECTED;
    if (err == ECONNREFUSED)
        return R_REFUSED;
    if (err == ETIMEDOUT)
        return R_TIMEOUT;
    fprintf(stderr, "connect: %s\n", strerror(err));
    return R_ERROR;
}

// 在 timeout_ms 内连接 ai 描述的地址
static enum result connect_with_timeout(const struct addrinfo *ai, int timeout_ms) {
    // BUG: 阻塞 socket + 阻塞 connect：timeout_ms 根本没用上。
    //      对黑洞地址，这里会卡 2 分钟多（内核重传 SYN）才返回。
    // TODO: 1. socket 类型再或上 SOCK_NONBLOCK
    //       2. connect 返回 0 → 已连接；返回 -1 且 errno != EINPROGRESS → classify(errno)
    //       3. EINPROGRESS：poll 等 POLLOUT，超时 timeout_ms（EINTR 时用剩余时间重试，now_ms() 可用）
    //          poll 返回 0 → R_TIMEOUT
    //       4. 否则 getsockopt(fd, SOL_SOCKET, SO_ERROR, &err, &len) 取结果，classify(err)
    //       别忘了每条路径都要 close(fd)
    int fd = socket(ai->ai_family, ai->ai_socktype | SOCK_CLOEXEC, ai->ai_protocol);
    if (fd < 0) {
        perror("socket");
        return R_ERROR;
    }
    (void)timeout_ms;
    enum result res = R_CONNECTED;
    if (connect(fd, ai->ai_addr, ai->ai_addrlen) < 0)
        res = classify(errno);
    close(fd);
    return res;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 4) {
        fprintf(stderr, "usage: %s HOST PORT TIMEOUT_MS\n", argv[0]);
        return 1;
    }
    int timeout_ms = atoi(argv[3]);
    if (timeout_ms <= 0) {
        fprintf(stderr, "bad timeout: %s\n", argv[3]);
        return 1;
    }

    struct addrinfo hints = {.ai_socktype = SOCK_STREAM, .ai_flags = AI_NUMERICSERV};
    struct addrinfo *ai;
    int gai = getaddrinfo(argv[1], argv[2], &hints, &ai);
    if (gai != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(gai));
        return 1;
    }
    enum result res = connect_with_timeout(ai, timeout_ms); // 为简单起见只试第一个地址
    freeaddrinfo(ai);

    static const char *const names[] = {"connected", "error", "refused", "timeout"};
    if (res != R_ERROR)
        puts(names[res]);
    return (int)res;
}
