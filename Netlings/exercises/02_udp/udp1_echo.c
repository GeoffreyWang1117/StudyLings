// EXERCISE: udp1_echo — 双栈 UDP 回显：recvfrom/sendto、消息边界、空数据报与大数据报
// TOPIC: SOCK_DGRAM / recvfrom / sendto / sockaddr_storage / 数据报边界
// DIFFICULTY: ★★☆☆☆
// BOOK: UNP §8.1-8.6（UDP 回显服务器）、§8.12（UDP 没有流量控制）、§12.2；man 7 udp
// I AM NOT DONE
//
// 说明：
//   用法：udp1_echo PORT        启动后打印 "listening on port N"，然后永远循环：
//   收到一个数据报，就把它原样发回给【发送它的那个地址】。
//
//   和 TCP 的区别：
//   - UDP 保留消息边界：一次 recvfrom 恰好取走一个完整数据报（缓冲区太小时多余部分被静默丢弃，
//     flags 里会有 MSG_TRUNC）。所以缓冲区要按最大可能的数据报准备：UDP 负载最大 65507(v4)/65527(v6)
//     字节，用 64 KiB 就够了。按 MTU 1500 开缓冲区是经典 bug。
//   - 长度为 0 的数据报是合法的（recvfrom 返回 0 不是 EOF！UDP 根本没有连接和 EOF）。
//   - 没有连接：每个数据报都可能来自不同的客户端，回复地址必须取自这次 recvfrom 的 src_addr；
//     addrlen 是值-结果参数，每次调用前都要重置成缓冲区大小。用 sockaddr_storage 才能同时装下 v4/v6。
//   现代例子：DNS（CoreDNS、systemd-resolved、Go 的 net.ListenPacket）、QUIC/HTTP3（quiche、
//   quinn、nginx 的 `listen 443 quic`）、StatsD、WireGuard 都跑在这样的 recvfrom/sendto 循环上。
//
//   探针会检查：IPv4 与 IPv6 客户端（本机无 IPv6 时跳过）；多个客户端交替发送；
//   空数据报；60000 字节的数据报原样返回。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

// 脚手架：双栈 UDP socket（IPV6_V6ONLY=0 绑定 ::），内核不支持 IPv6 时退回 0.0.0.0。
static int make_udp_socket(unsigned short port) {
    int family = AF_INET6;
    int fd = socket(AF_INET6, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0 && errno == EAFNOSUPPORT) {
        family = AF_INET;
        fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    }
    if (fd < 0)
        sl_die("socket");
    int off = 0;
    if (family == AF_INET6 && setsockopt(fd, IPPROTO_IPV6, IPV6_V6ONLY, &off, sizeof off) < 0)
        sl_die("setsockopt IPV6_V6ONLY");
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
    return fd;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PORT\n", argv[0]);
        return 2;
    }
    unsigned short port = (unsigned short)atoi(argv[1]);
    int fd = make_udp_socket(port);
    printf("listening on port %u\n", port);

    static char buf[1500]; // BUG: 按以太网 MTU 开的缓冲区，大数据报会被截断
    for (;;) {
        // TODO: recvfrom 一个数据报，记下发送方地址（sockaddr_storage + 每次重置的 addrlen），
        //       然后 sendto 原样发回给这个地址。长度为 0 的数据报也要回。
        struct sockaddr_storage peer;
        socklen_t peer_len = sizeof peer;
        ssize_t n = recvfrom(fd, buf, sizeof buf, 0, (struct sockaddr *)&peer, &peer_len);
        if (n <= 0) // BUG: 把 0 当成"没数据/EOF"——但空数据报是合法消息
            continue;
        if (sendto(fd, buf, (size_t)n, 0, (struct sockaddr *)&peer, peer_len) < 0)
            perror("sendto"); // UDP 发送失败（对端不可达等）不应让服务器退出
    }
}
