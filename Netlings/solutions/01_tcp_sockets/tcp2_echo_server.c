// EXERCISE: tcp2_echo_server — 双栈迭代回显服务器：IPV6_V6ONLY=0、SO_REUSEADDR 与 TIME_WAIT
// TOPIC: socket / bind / listen / accept4 / 主动关闭方与 TIME_WAIT
// DIFFICULTY: ★★☆☆☆
// BOOK: UNP §2.7（TIME_WAIT）、§4.5-4.6（listen/accept）、§5（回显服务器）、§7.5（SO_REUSEADDR）、§12.2（双栈）；man 7 ipv6
//
// 说明：
//   用法：tcp2_echo_server PORT        （PORT 为 0 时由内核挑一个）
//   启动后打印 "listening on port N"，然后一次服务一个连接：每读到一行就原样写回；
//   读到内容恰好是 "quit" 的一行时，先回显它，然后【服务器】主动 close 这个连接，继续 accept 下一个。
//
//   要点：
//   1. 双栈：一个 AF_INET6 socket 绑定 ::，并 setsockopt(IPV6_V6ONLY, 0)，IPv4 客户端会以
//      ::ffff:127.0.0.1 这种 v4-mapped 地址出现。默认值取决于 sysctl net.ipv6.bindv6only，
//      不要赌默认值——nginx 的 `listen [::]:80 ipv6only=off`、Go 的 net.Listen("tcp", ":80")
//      都是显式设置的。（本机内核没有 IPv6 时，脚手架会自动退回 AF_INET + 0.0.0.0。）
//   2. TIME_WAIT：谁先 close，谁进入 TIME_WAIT（2*MSL，Linux 上 60 秒）。本服务器在 "quit" 后
//      主动关闭，于是 TIME_WAIT 挂在服务器的端口上。此时 kill 掉服务器马上重启，没有
//      SO_REUSEADDR 的 bind 会得到 EADDRINUSE —— 这就是"改完配置重启 nginx/Redis 失败"
//      的经典原因。所有正经的服务器（nginx、Redis、Envoy、Go、tokio）监听前都设 SO_REUSEADDR。
//   3. listen 的 backlog 用 SOMAXCONN（内核再用 net.core.somaxconn 截断）；
//      accept4(..., SOCK_CLOEXEC) 与 socket(... | SOCK_CLOEXEC)：fork+exec 子进程时不泄漏 fd。
//
//   探针会检查：v4 / v6 客户端都能回显；一次 read 里多行、一行拆成多次发送都能正确处理；
//   "quit" 后服务器主动关闭（服务器端口上出现 TIME_WAIT）；kill 后立刻在同一端口重启必须成功；
//   监听 fd 与已连接 fd 都带 O_CLOEXEC。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

// 脚手架：优先创建 AF_INET6 socket；内核不支持 IPv6（EAFNOSUPPORT）时退回 AF_INET。
static int open_socket(int type, int *family) {
    int fd = socket(AF_INET6, type | SOCK_CLOEXEC, 0);
    if (fd >= 0) {
        *family = AF_INET6;
        return fd;
    }
    if (errno != EAFNOSUPPORT)
        return -1;
    *family = AF_INET;
    return socket(AF_INET, type | SOCK_CLOEXEC, 0);
}

// TODO: 创建监听 socket 并返回 fd，失败时 sl_die。
//   - AF_INET6 时 setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, 0)（双栈）
//   - setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)（必须在 bind 之前）
//   - bind 到 in6addr_any（或 INADDR_ANY）:port
//   - listen(fd, SOMAXCONN)
static int make_listener(unsigned short port) {
    int family;
    int fd = open_socket(SOCK_STREAM, &family);
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

static unsigned short bound_port(int fd) {
    struct sockaddr_storage ss;
    socklen_t len = sizeof ss;
    if (getsockname(fd, (struct sockaddr *)&ss, &len) < 0)
        sl_die("getsockname");
    if (ss.ss_family == AF_INET6)
        return ntohs(((struct sockaddr_in6 *)&ss)->sin6_port);
    return ntohs(((struct sockaddr_in *)&ss)->sin_port);
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

// 服务一个连接：逐行回显；对端 EOF、出错或收到 "quit" 行时返回（由调用者 close）。
static void serve(int cfd) {
    char buf[8192];
    size_t len = 0;
    for (;;) {
        if (len == sizeof buf) { // 一行太长：原样回显已有部分，腾出空间
            if (write_all(cfd, buf, len) < 0)
                return;
            len = 0;
        }
        ssize_t r = read(cfd, buf + len, sizeof buf - len);
        if (r < 0) {
            if (errno == EINTR)
                continue;
            return;
        }
        if (r == 0)
            return; // 客户端先关了：它进入 TIME_WAIT，我们不会
        len += (size_t)r;

        char *nl;
        while ((nl = memchr(buf, '\n', len)) != nullptr) {
            size_t line_len = (size_t)(nl - buf) + 1;
            if (write_all(cfd, buf, line_len) < 0)
                return;
            bool quit = line_len == 5 && memcmp(buf, "quit", 4) == 0;
            memmove(buf, buf + line_len, len - line_len);
            len -= line_len;
            if (quit)
                return;
        }
    }
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    int lfd = make_listener((unsigned short)atoi(argv[1]));
    printf("listening on port %u\n", bound_port(lfd));

    for (;;) {
        // TODO: 用 accept4(..., SOCK_CLOEXEC) 取代 accept，让已连接 fd 也带 close-on-exec
        int cfd = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
        if (cfd < 0) {
            if (errno == EINTR || errno == ECONNABORTED)
                continue;
            sl_die("accept4");
        }
        serve(cfd);
        close(cfd); // 在 "quit" 之后，这就是服务器的主动关闭 → TIME_WAIT
    }
}
