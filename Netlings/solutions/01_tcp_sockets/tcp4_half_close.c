// EXERCISE: tcp4_half_close — 半关闭：shutdown(SHUT_WR) 发 FIN 表示"我说完了"，但继续读回复
// TOPIC: shutdown vs close / TCP 半关闭 / 用 EOF 作为请求结束标志
// DIFFICULTY: ★★☆☆☆
// BOOK: UNP §6.6（shutdown）、§5.12；TCP/IP Illustrated Vol.1 §13.6（半关闭）；man 2 shutdown
//
// 说明：
//   用法：tcp4_half_close HOST PORT < FILE
//   把 stdin 的全部内容上传给服务器；上传完后必须让服务器知道"没有更多数据了"（发 FIN），
//   但自己还要继续读服务器的回复，一直读到 EOF，把回复原样打印到 stdout，exit 0。
//   探针的服务器会一直读到 EOF，然后回复 "bytes=<n> sha256=<hex>\n" 再关闭。
//
//   close(fd) 同时关掉读和写两个方向（而且只是引用计数减一）；shutdown(fd, SHUT_WR) 只关写方向：
//   内核发送 FIN，对端 read 返回 0，而我们这边仍然能 read 回复。
//   - 不发 FIN：服务器永远等不到 EOF，客户端永远等不到回复 → 双方互等，挂死。
//   - 用 close 代替：回复到达时 socket 已经关了，内核回 RST，回复丢失。
//   现实中的例子：`nc -N`（stdin EOF 后 shutdown）、HTTP/1.0 没有 Content-Length 时用连接关闭
//   表示 body 结束、gRPC 客户端流的 CloseSend()（HTTP/2 的 END_STREAM 就是"流级半关闭"）、
//   Go 的 (*net.TCPConn).CloseWrite、tokio 的 AsyncWriteExt::shutdown、Node 的 socket.end()。

#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

// 脚手架：与 tcp1_client 相同的 getaddrinfo + 逐个地址尝试。
static int dial(const char *host, const char *port) {
    struct addrinfo hints = {.ai_family = AF_UNSPEC, .ai_socktype = SOCK_STREAM};
    struct addrinfo *res = nullptr;
    int rc = getaddrinfo(host, port, &hints, &res);
    if (rc != 0) {
        fprintf(stderr, "tcp4_half_close: getaddrinfo %s: %s\n", host, gai_strerror(rc));
        exit(1);
    }
    int fd = -1, last_err = EHOSTUNREACH;
    for (struct addrinfo *ai = res; ai != nullptr; ai = ai->ai_next) {
        fd = socket(ai->ai_family, ai->ai_socktype | SOCK_CLOEXEC, ai->ai_protocol);
        if (fd < 0) {
            last_err = errno;
            continue;
        }
        if (connect(fd, ai->ai_addr, ai->ai_addrlen) == 0)
            break;
        last_err = errno;
        close(fd);
        fd = -1;
    }
    freeaddrinfo(res);
    if (fd < 0)
        errno = last_err;
    return fd;
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

// 把 in 的内容全部拷贝到 out，直到 in 读到 EOF。成功返回 0，失败返回 -1。
static int pump(int in, int out) {
    char buf[64 * 1024];
    for (;;) {
        ssize_t r = read(in, buf, sizeof buf);
        if (r < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        if (r == 0)
            return 0;
        if (write_all(out, buf, (size_t)r) < 0)
            return -1;
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s HOST PORT < FILE\n", argv[0]);
        return 2;
    }
    int fd = dial(argv[1], argv[2]);
    if (fd < 0) {
        fprintf(stderr, "tcp4_half_close: connect %s:%s: %s\n", argv[1], argv[2], strerror(errno));
        return 1;
    }

    if (pump(STDIN_FILENO, fd) < 0)
        sl_die("upload");

    // TODO: 上传完毕 —— 只关闭写方向，让服务器 read 到 EOF，但我们还要读回复。
    //       （不要用 close：那样读方向也没了。）
    if (shutdown(fd, SHUT_WR) < 0)
        sl_die("shutdown");

    if (pump(fd, STDOUT_FILENO) < 0)
        sl_die("download");
    close(fd);
    return 0;
}
