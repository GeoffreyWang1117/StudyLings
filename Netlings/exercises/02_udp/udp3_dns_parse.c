// EXERCISE: udp3_dns_parse — 手工构造 DNS 查询并解析响应（含名字压缩指针）
// TOPIC: 二进制协议编解码 / 网络字节序 / DNS 报文格式 / 名字压缩 / 不信任对端输入
// DIFFICULTY: ★★★★☆
// BOOK: UNP §11.2（DNS 概述）、§8（UDP 客户端）；RFC 1035 §4.1（报文格式）、§4.1.4（压缩）；RFC 5452
// I AM NOT DONE
//
// 说明：
//   用法：udp3_dns_parse SERVER_PORT NAME
//   向 127.0.0.1:SERVER_PORT 发送一个 NAME 的 A 记录查询，打印答案里的每条 A 记录：
//       A <点分 IPv4> ttl=<秒>
//   出错（名字非法、超时、RCODE 非 0、报文畸形）时向 stderr 说明原因并 exit 1。
//
//   报文格式（全部大端）：
//     头部 12 字节：ID(2) FLAGS(2) QDCOUNT(2) ANCOUNT(2) NSCOUNT(2) ARCOUNT(2)
//       查询时 FLAGS = 0x0100（RD=1，期望递归），QDCOUNT = 1
//     问题：QNAME + QTYPE(2)=1(A) + QCLASS(2)=1(IN)
//       QNAME 编码："www.example.com" → 03 'w''w''w' 07 'e''x''a''m''p''l''e' 03 'c''o''m' 00
//       每个 label 1..63 字节，整个编码后的名字 ≤ 255 字节；末尾的 '.' 可有可无。
//     资源记录：NAME TYPE(2) CLASS(2) TTL(4) RDLENGTH(2) RDATA(RDLENGTH)
//   名字压缩：长度字节的最高两位为 11（>= 0xC0）时，它和下一个字节组成 14 位偏移，
//   表示"名字的剩余部分在报文的这个偏移处"。指针后面不再有 00 结尾；指针可以指向另一个
//   含指针的名字。响应里几乎所有名字都是压缩的（最常见的是 C0 0C，指向问题里的 QNAME）。
//
//   把对端当成敌人（现实中 DNS 解析器的 CVE 多数出在这里：glibc CVE-2015-7547、
//   dnsmasq "DNSpooq"、systemd-resolved ……）：
//   - 所有读取都要检查边界；指针可能构成环（A 指向 B，B 指回 A），要限制跳转次数；
//   - 响应 ID 必须与查询 ID 一致，否则丢弃并继续等待（防伪造响应，RFC 5452）；
//   - 只接受 owner 名字属于查询名字（或它的 CNAME 链）的 A 记录，其余一律忽略。
//   CNAME 记录（TYPE 5）：如果它的 owner 是当前期望的名字，就把期望名字换成它的目标名字；
//   然后跳过 RDLENGTH 字节继续。
//
//   现代关联：Go 的 golang.org/x/net/dns/dnsmessage、c-ares（Node.js、curl）、hickory-dns（Rust），
//   以及 CoreDNS / Kubernetes 集群 DNS。HTTP/2 的 HPACK、QUIC 的变长整数也是同一类"手写二进制解析"。
//
//   探针运行一个假的 DNS 服务器：检查你的查询报文（ID、FLAGS、QNAME 字节、QTYPE/QCLASS），
//   回复 CNAME + 2 条 A 记录（名字全部压缩、指针套指针），还会测试：伪造 ID 的响应、
//   不相干名字的 A 记录、指针环、超过 63 字节的 label。

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/random.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

enum {
    DNS_HDR = 12,
    MAX_NAME_WIRE = 255, // 编码后的名字最多 255 字节
    MAX_NAME_TEXT = 256, // 点分文本形式的缓冲区大小（含 '\0'）
    MAX_JUMPS = 64,      // 最多跟随多少个压缩指针（防环）
    TYPE_A = 1,
    TYPE_CNAME = 5,
    CLASS_IN = 1,
    TIMEOUT_MS = 2000,
};

static void put16(uint8_t *p, uint16_t v) {
    p[0] = (uint8_t)(v >> 8);
    p[1] = (uint8_t)v;
}
static uint16_t get16(const uint8_t *p) { return (uint16_t)(p[0] << 8 | p[1]); }
static uint32_t get32(const uint8_t *p) {
    return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | p[3];
}

// TODO: 把点分名字编码成 DNS wire 格式写到 out，返回写入的字节数；名字非法时返回 -1。
//   - 按 '.' 切分，每个 label 前面写 1 字节长度；最后写 0x00（根）
//   - label 长度必须在 1..63 之间（空 label 如 "a..b" 非法）；允许一个结尾的 '.'
//   - "" 或 "." 表示根，编码为单个 0x00
//   - 编码后总长度不能超过 MAX_NAME_WIRE，也不能超过 cap
static int encode_qname(const char *name, uint8_t *out, size_t cap) {
    return -1;
}

// TODO: 从报文 msg[0..len) 的偏移 off 处解析一个（可能压缩的）名字。
//   - 成功时把点分文本写到 out（根写成 "."），把"名字之后的下一个字节的偏移"写到 *next，返回 0
//   - 普通 label：长度字节 1..63，后跟 label 内容；0 表示结束
//   - 压缩指针：长度字节最高两位为 11，偏移 = ((b & 0x3F) << 8) | 下一字节，跳过去继续读。
//     *next 应该是【第一个】指针之后的位置（指针占 2 字节），而不是跳转后的位置。
//   - 最高两位为 01 或 10 是保留值，报错
//   - 任何越界读取、文本超出 outcap、跳转次数超过 MAX_JUMPS（指针环），都返回 -1
static int parse_name(const uint8_t *msg, size_t len, size_t off, char *out, size_t outcap,
                      size_t *next) {
    size_t out_len = 0;
    for (;;) {
        if (off >= len)
            return -1;
        uint8_t b = msg[off];
        if ((b & 0xC0) != 0) {
            // TODO: 支持压缩指针（最高两位 11），并限制跳转次数；01/10 是保留值
            return -1;
        }
        if (b == 0) {
            *next = off + 1;
            break;
        }
        if (off + 1 + b > len)
            return -1;
        size_t need = out_len + (out_len ? 1 : 0) + b;
        if (need + 1 > outcap)
            return -1;
        if (out_len)
            out[out_len++] = '.';
        memcpy(out + out_len, msg + off + 1, b);
        out_len += b;
        off += 1 + (size_t)b;
    }
    if (out_len == 0) {
        if (outcap < 2)
            return -1;
        out[out_len++] = '.';
    }
    out[out_len] = '\0';
    return 0;
}

// 去掉结尾的 '.'，便于比较名字（DNS 名字比较不区分大小写）。
static bool same_name(const char *a, const char *b) {
    size_t la = strlen(a), lb = strlen(b);
    if (la > 1 && a[la - 1] == '.')
        la--;
    if (lb > 1 && b[lb - 1] == '.')
        lb--;
    return la == lb && strncasecmp(a, b, la) == 0;
}

static double now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1e3 + (double)ts.tv_nsec / 1e6;
}

// 解析并打印响应。成功返回 0，报文有问题返回 -1（已向 stderr 说明原因）。
static int print_answers(const uint8_t *msg, size_t len, const char *qname) {
    uint16_t flags = get16(msg + 2);
    if (!(flags & 0x8000)) {
        fprintf(stderr, "udp3_dns_parse: reply is not a response (QR=0)\n");
        return -1;
    }
    if (flags & 0x0200) {
        fprintf(stderr, "udp3_dns_parse: reply truncated (TC=1), would need TCP\n");
        return -1;
    }
    if ((flags & 0x000F) != 0) {
        fprintf(stderr, "udp3_dns_parse: server returned RCODE %u\n", flags & 0x000F);
        return -1;
    }
    uint16_t qd = get16(msg + 4), an = get16(msg + 6);

    char name[MAX_NAME_TEXT];
    size_t off = DNS_HDR;
    for (uint16_t i = 0; i < qd; i++) {
        if (parse_name(msg, len, off, name, sizeof name, &off) < 0 || off + 4 > len) {
            fprintf(stderr, "udp3_dns_parse: malformed question section\n");
            return -1;
        }
        off += 4; // QTYPE + QCLASS
    }

    char expect[MAX_NAME_TEXT]; // 当前期望的 owner 名字：查询名，遇到 CNAME 后换成目标名
    snprintf(expect, sizeof expect, "%s", qname);
    for (uint16_t i = 0; i < an; i++) {
        if (parse_name(msg, len, off, name, sizeof name, &off) < 0 || off + 10 > len) {
            fprintf(stderr, "udp3_dns_parse: malformed answer #%u\n", i + 1);
            return -1;
        }
        uint16_t type = get16(msg + off), klass = get16(msg + off + 2);
        uint32_t ttl = get32(msg + off + 4);
        uint16_t rdlen = get16(msg + off + 8);
        off += 10;
        if (off + rdlen > len) {
            fprintf(stderr, "udp3_dns_parse: answer #%u RDATA out of bounds\n", i + 1);
            return -1;
        }
        bool ours = klass == CLASS_IN && same_name(name, expect);
        if (ours && type == TYPE_CNAME) {
            char target[MAX_NAME_TEXT];
            size_t after;
            if (parse_name(msg, off + rdlen, off, target, sizeof target, &after) < 0) {
                fprintf(stderr, "udp3_dns_parse: malformed CNAME target\n");
                return -1;
            }
            snprintf(expect, sizeof expect, "%s", target);
        } else if (ours && type == TYPE_A && rdlen == 4) {
            char ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, msg + off, ip, sizeof ip);
            printf("A %s ttl=%u\n", ip, ttl);
        }
        off += rdlen;
    }
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s SERVER_PORT NAME\n", argv[0]);
        return 2;
    }
    const char *qname = argv[2];

    // ---- 构造查询 ----
    uint8_t query[DNS_HDR + MAX_NAME_WIRE + 4];
    uint16_t id;
    if (getrandom(&id, sizeof id, 0) != (ssize_t)sizeof id)
        sl_die("getrandom");
    put16(query + 0, id);
    put16(query + 2, 0x0100); // RD
    put16(query + 4, 1);      // QDCOUNT
    put16(query + 6, 0);
    put16(query + 8, 0);
    put16(query + 10, 0);
    int qlen = encode_qname(qname, query + DNS_HDR, MAX_NAME_WIRE);
    if (qlen < 0) {
        fprintf(stderr, "udp3_dns_parse: invalid name '%s'\n", qname);
        return 1;
    }
    size_t len = DNS_HDR + (size_t)qlen;
    put16(query + len, TYPE_A);
    put16(query + len + 2, CLASS_IN);
    len += 4;

    // ---- 发送（已连接 UDP socket，见 udp2_retry_client） ----
    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    struct sockaddr_in sa = {.sin_family = AF_INET,
                             .sin_port = htons((uint16_t)atoi(argv[1])),
                             .sin_addr.s_addr = htonl(INADDR_LOOPBACK)};
    if (connect(fd, (struct sockaddr *)&sa, sizeof sa) < 0)
        sl_die("connect");
    if (send(fd, query, len, 0) < 0)
        sl_die("send");

    // ---- 等待 ID 匹配的响应 ----
    static uint8_t reply[65536];
    double deadline = now_ms() + TIMEOUT_MS;
    for (;;) {
        int left = (int)(deadline - now_ms());
        if (left <= 0) {
            fprintf(stderr, "udp3_dns_parse: timeout\n");
            close(fd);
            return 1;
        }
        struct pollfd pfd = {.fd = fd, .events = POLLIN};
        int n = poll(&pfd, 1, left);
        if (n < 0 && errno != EINTR)
            sl_die("poll");
        if (n <= 0)
            continue;
        ssize_t r = recv(fd, reply, sizeof reply, 0);
        if (r < 0)
            sl_die("recv");
        if (r < DNS_HDR || get16(reply) != id) {
            fprintf(stderr, "udp3_dns_parse: ignoring reply with wrong ID or size\n");
            continue;
        }
        int rc = print_answers(reply, (size_t)r, qname);
        close(fd);
        return rc == 0 ? 0 : 1;
    }
}
