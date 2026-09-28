// EXERCISE: tcp3_length_prefix — TCP 是字节流：用"4 字节长度 + 负载"分帧，处理短读短写
// TOPIC: 消息分帧（framing）/ read_full / write_full / 最大帧长度
// DIFFICULTY: ★★★☆☆
// BOOK: UNP §3.9（readn/writen）、§5.18（二进制数据与字节序）；RFC 9113 §4.1（HTTP/2 帧头）
//
// 说明：
//   用法：tcp3_length_prefix PORT        启动后打印 "listening on port N"
//   协议：每条消息 = 4 字节大端（网络字节序）长度 L + L 字节负载。服务器对每条消息回复一条
//   同样格式的消息，负载是原负载的字节逆序。客户端关闭连接后服务器继续 accept 下一个。
//   L 超过 16 MiB 视为非法：直接关闭这个连接（不许崩溃、不许去 malloc 4GB）。
//
//   TCP 没有"消息边界"：发送方的一次 send 可能被接收方分成好几次 read 读到（分片），
//   发送方的好几次 send 也可能被一次 read 全读到（合并）。所以所有跑在 TCP 上的协议都
//   自己分帧：HTTP/2 帧头 3 字节长度、gRPC 消息 1+4 字节前缀、Kafka 4 字节长度、
//   Redis RESP 的 "$<len>\r\n"、PostgreSQL 协议的 4 字节长度……
//   接收方必须"读满 N 字节"才能继续：read 返回的字节数可能少于请求数，要循环。
//   同理 write 在非阻塞 socket 或被信号打断时也可能短写。
//   最大帧长度检查也很重要：gRPC 默认 max_receive_message_length = 4 MiB，
//   不检查的话对方发个 0xFFFFFFFF 你就去分配 4GB 内存。
//
//   探针会检查：逐字节发送（每字节间隔几毫秒，制造分片）；一次 sendall 发出多帧（合并），
//   其中包括空负载帧；1 MiB 的大帧；非法长度后服务器仍然活着、能服务下一个连接。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_FRAME = 16 * 1024 * 1024 };

// TODO: 从 fd 读满 n 字节到 buf。
//   返回 1 表示读满；返回 0 表示在读到任何字节之前就遇到 EOF（对端正常关闭）；
//   返回 -1 表示出错或读到一半遇到 EOF（帧被截断）。EINTR 要重试。
static int read_full(int fd, void *buf, size_t n) {
    char *p = buf;
    size_t got = 0;
    while (got < n) {
        ssize_t r = read(fd, p + got, n - got);
        if (r < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        if (r == 0)
            return got == 0 ? 0 : -1;
        got += (size_t)r;
    }
    return 1;
}

// TODO: 把 buf[0..n) 全部写到 fd，处理短写与 EINTR。成功返回 0，失败返回 -1。
static int write_full(int fd, const void *buf, size_t n) {
    const char *p = buf;
    while (n > 0) {
        ssize_t w = write(fd, p, n);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        p += w;
        n -= (size_t)w;
    }
    return 0;
}

// 服务一个连接直到对端关闭或出错。
static void serve(int cfd) {
    for (;;) {
        uint32_t be_len;
        int rc = read_full(cfd, &be_len, sizeof be_len);
        if (rc <= 0)
            return;
        uint32_t len = ntohl(be_len);
        if (len > MAX_FRAME) {
            fprintf(stderr, "tcp3_length_prefix: frame too large (%u bytes), dropping client\n", len);
            return;
        }
        unsigned char *payload = malloc(len ? len : 1);
        if (!payload)
            sl_die("malloc");
        if (len > 0 && read_full(cfd, payload, len) != 1) {
            free(payload);
            return;
        }
        for (uint32_t i = 0, j = len; i + 1 < j; i++, j--) {
            unsigned char t = payload[i];
            payload[i] = payload[j - 1];
            payload[j - 1] = t;
        }
        int wrc = write_full(cfd, &be_len, sizeof be_len);
        if (wrc == 0 && len > 0)
            wrc = write_full(cfd, payload, len);
        free(payload);
        if (wrc < 0)
            return;
    }
}

// 脚手架：双栈监听 socket（内核不支持 IPv6 时退回 IPv4），细节见 tcp2_echo_server。
static int make_listener(unsigned short port) {
    int family = AF_INET6;
    int fd = socket(AF_INET6, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (fd < 0 && errno == EAFNOSUPPORT) {
        family = AF_INET;
        fd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    }
    if (fd < 0)
        sl_die("socket");
    int on = 1, off = 0;
    if (family == AF_INET6 && setsockopt(fd, IPPROTO_IPV6, IPV6_V6ONLY, &off, sizeof off) < 0)
        sl_die("setsockopt IPV6_V6ONLY");
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof on) < 0)
        sl_die("setsockopt SO_REUSEADDR");
    int rc;
    if (family == AF_INET6) {
        struct sockaddr_in6 sa = {
            .sin6_family = AF_INET6, .sin6_port = htons(port), .sin6_addr = in6addr_any};
        rc = bind(fd, (struct sockaddr *)&sa, sizeof sa);
    } else {
        struct sockaddr_in sa = {
            .sin_family = AF_INET, .sin_port = htons(port), .sin_addr.s_addr = htonl(INADDR_ANY)};
        rc = bind(fd, (struct sockaddr *)&sa, sizeof sa);
    }
    if (rc < 0)
        sl_die("bind");
    if (listen(fd, SOMAXCONN) < 0)
        sl_die("listen");
    return fd;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    unsigned short port = (unsigned short)atoi(argv[1]);
    int lfd = make_listener(port);
    printf("listening on port %u\n", port);

    for (;;) {
        int cfd = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
        if (cfd < 0) {
            if (errno == EINTR || errno == ECONNABORTED)
                continue;
            sl_die("accept4");
        }
        serve(cfd);
        close(cfd);
    }
}
