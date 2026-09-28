// EXERCISE: tcp1_client — 协议无关的 TCP 客户端：getaddrinfo + 逐个地址尝试 connect
// TOPIC: getaddrinfo(AF_UNSPEC) / 双栈 / "Happy Eyeballs" 的朴素版
// DIFFICULTY: ★★☆☆☆
// BOOK: UNP §4.3-4.4（connect）、§11.6-11.12（getaddrinfo、tcp_connect）；RFC 8305；man 3 getaddrinfo
// I AM NOT DONE
//
// 说明：
//   用法：tcp1_client HOST PORT MESSAGE
//   连接 HOST:PORT，发送 "MESSAGE\n"，读回一行响应，原样打印到 stdout，exit 0。
//   连接失败时向 stderr 打印 "tcp1_client: connect HOST:PORT: <原因>"，exit 1。
//
//   为什么不能 hard-code AF_INET、也不能只试第一个地址？
//   - "localhost" 在大多数现代发行版上会同时解析出 ::1 和 127.0.0.1，而且 ::1 排在前面
//     （RFC 6724 地址选择规则）。服务只监听 127.0.0.1 时，只试第一个地址就会 ECONNREFUSED。
//   - 一个域名通常有多条 A/AAAA 记录（负载均衡、多机房）。其中一台挂了，客户端应该试下一台。
//   Go 的 net.Dialer、curl、Python 的 socket.create_connection、libuv 的 uv_getaddrinfo +
//   uv_tcp_connect 都是这个套路：getaddrinfo(AF_UNSPEC, SOCK_STREAM) 拿到列表，按顺序逐个
//   socket()+connect()，第一个成功的就用；全部失败才报错（报最后一个错误）。
//   Happy Eyeballs（RFC 8305）在此基础上把 v6/v4 并发竞速，本练习只要求顺序尝试。
//
//   探针会检查：数字地址 127.0.0.1 / ::1；服务只监听 127.0.0.1 但给你 "localhost"；
//   服务只监听 ::1 时给你 "localhost"（本机没有 IPv6 时这些 v6 用例会被跳过）；无人监听时报错退出。

#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

// TODO: 解析 host:port 并返回一个已连接的 TCP socket fd；失败返回 -1（errno 为最后一次失败的原因）。
//   1. hints: ai_family = AF_UNSPEC（v4/v6 都要）、ai_socktype = SOCK_STREAM
//   2. getaddrinfo 失败时向 stderr 打印 gai_strerror(rc)，返回 -1
//   3. 遍历链表：socket(ai_family, ai_socktype | SOCK_CLOEXEC, ai_protocol) + connect，
//      失败就 close 掉、记住 errno、试下一个
//   4. 别忘了 freeaddrinfo
static int dial(const char *host, const char *port) {
    struct addrinfo hints = {
        .ai_family = AF_INET, // BUG: 只要 IPv4，"::1" 和只监听 ::1 的服务就连不上
        .ai_socktype = SOCK_STREAM,
    };
    struct addrinfo *res = nullptr;
    int rc = getaddrinfo(host, port, &hints, &res);
    if (rc != 0) {
        fprintf(stderr, "tcp1_client: getaddrinfo %s: %s\n", host, gai_strerror(rc));
        errno = EHOSTUNREACH;
        return -1;
    }

    // TODO: 遍历 res 链表，逐个 socket() + connect()，第一个成功的就返回它的 fd。
    //       失败的 fd 要 close；全部失败时让 errno 等于最后一次失败的原因。
    freeaddrinfo(res);
    errno = ENOSYS;
    return -1;
}

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

// 读到 '\n'（包含）或 EOF 为止；返回读到的字节数，出错返回 -1。
static ssize_t read_line(int fd, char *buf, size_t cap) {
    size_t len = 0;
    while (len + 1 < cap) {
        ssize_t r = read(fd, buf + len, 1);
        if (r < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        if (r == 0)
            break;
        len += (size_t)r;
        if (buf[len - 1] == '\n')
            break;
    }
    buf[len] = '\0';
    return (ssize_t)len;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s HOST PORT MESSAGE\n", argv[0]);
        return 2;
    }
    const char *host = argv[1], *port = argv[2], *msg = argv[3];

    int fd = dial(host, port);
    if (fd < 0) {
        fprintf(stderr, "tcp1_client: connect %s:%s: %s\n", host, port, strerror(errno));
        return 1;
    }

    size_t mlen = strlen(msg);
    char *out = malloc(mlen + 2);
    if (!out)
        sl_die("malloc");
    memcpy(out, msg, mlen);
    out[mlen] = '\n';
    if (write_all(fd, out, mlen + 1) < 0)
        sl_die("write");
    free(out);

    char line[4096];
    ssize_t n = read_line(fd, line, sizeof line);
    if (n < 0)
        sl_die("read");
    if (n == 0) {
        fprintf(stderr, "tcp1_client: server closed the connection without a reply\n");
        close(fd);
        return 1;
    }
    fputs(line, stdout);
    close(fd);
    return 0;
}
