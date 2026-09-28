// EXERCISE: prep7_bytes_endian — 字节序、未对齐访问与协议头解析
// TOPIC: 大端/小端 / memcpy / ntohs / Internet checksum
// DIFFICULTY: ★★★☆☆
// BOOK: UNP §3.4（字节序）；RFC 791（IPv4 头）、RFC 1071（校验和）—— Netlings 解析报文的基础
//
// 说明：
//   网络协议规定字节序为大端（network byte order）；x86-64 / 常见 aarch64 是小端。
//   从字节缓冲区读多字节整数时，把 uint8_t* 强转成 uint16_t* 再解引用有两个问题：
//     (a) 字节序错了；(b) 地址可能未对齐 —— 这是未定义行为，UBSan 会报 "misaligned address"。
//   正确做法：逐字节拼（本题要求），或 memcpy 到局部变量后再 ntohs/ntohl。
//   1. load_be16 / load_be32 / store_be16：大端读写
//   2. parse_ipv4：从原始字节解析 IPv4 头的若干字段
//   3. inet_checksum：RFC 1071 的 16 位反码和；对一个正确的 IPv4 头计算结果应为 0

#include "sl.h"

#include <arpa/inet.h>
#include <stdint.h>

// TODO: 以大端读 2 字节
static uint16_t load_be16(const uint8_t *p) {
    return (uint16_t)(p[0] << 8 | p[1]);
}

// TODO: 以大端读 4 字节
static uint32_t load_be32(const uint8_t *p) {
    return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 | (uint32_t)p[2] << 8 | p[3];
}

// TODO: 以大端写 2 字节
static void store_be16(uint8_t *p, uint16_t v) {
    p[0] = (uint8_t)(v >> 8);
    p[1] = (uint8_t)v;
}

struct ipv4_info {
    unsigned version;  // 高 4 位
    unsigned hdr_len;  // IHL（低 4 位）× 4 字节
    unsigned total_len;
    unsigned ttl;
    unsigned proto;
    char src[INET_ADDRSTRLEN];
    char dst[INET_ADDRSTRLEN];
};

// TODO: 解析 20 字节以上的 IPv4 头（src 在偏移 12，dst 在偏移 16；可用 inet_ntop 转字符串）
static void parse_ipv4(const uint8_t *p, struct ipv4_info *out) {
    out->version = p[0] >> 4;
    out->hdr_len = (p[0] & 0x0f) * 4u;
    out->total_len = load_be16(p + 2);
    out->ttl = p[8];
    out->proto = p[9];
    struct in_addr a;
    memcpy(&a.s_addr, p + 12, 4); // s_addr 本身就是网络字节序，直接拷贝
    inet_ntop(AF_INET, &a, out->src, sizeof out->src);
    memcpy(&a.s_addr, p + 16, 4);
    inet_ntop(AF_INET, &a, out->dst, sizeof out->dst);
}

// TODO: 16 位一组求和（奇数长度时最后一个字节作为高 8 位），把进位折回低 16 位，最后取反
static uint16_t inet_checksum(const uint8_t *p, size_t n) {
    uint32_t sum = 0;
    for (; n > 1; p += 2, n -= 2)
        sum += load_be16(p);
    if (n)
        sum += (uint32_t)p[0] << 8;
    while (sum >> 16)
        sum = (sum & 0xffff) + (sum >> 16);
    return (uint16_t)~sum;
}

// ---- 以下为自测，不要修改 ----
int main(void) {
    // 故意从奇数地址开始放报文，模拟收包缓冲区里任意偏移的协议头
    alignas(8) uint8_t storage[64];
    uint8_t *pkt = storage + 1;
    const uint8_t hdr[20] = {0x45, 0x00, 0x00, 0x54, 0x1c, 0x46, 0x40, 0x00, 0x40, 0x01,
                             0x9c, 0xa9, 0xc0, 0xa8, 0x00, 0x68, 0xc0, 0xa8, 0x00, 0x01};
    memcpy(pkt, hdr, sizeof hdr);

    SL_CHECK_EQ(load_be16(pkt + 2), 84);
    SL_CHECK_EQ(load_be32(pkt + 12), 0xc0a80068u);

    struct ipv4_info info = {};
    parse_ipv4(pkt, &info);
    SL_CHECK_EQ(info.version, 4);
    SL_CHECK_EQ(info.hdr_len, 20);
    SL_CHECK_EQ(info.total_len, 84);
    SL_CHECK_EQ(info.ttl, 64);
    SL_CHECK_EQ(info.proto, 1); // ICMP
    SL_CHECK(strcmp(info.src, "192.168.0.104") == 0);
    SL_CHECK(strcmp(info.dst, "192.168.0.1") == 0);

    SL_CHECK_EQ(inet_checksum(pkt, 20), 0); // 正确的头部校验和为 0
    store_be16(pkt + 10, 0);                // 清零校验和字段后重新计算
    SL_CHECK_EQ(inet_checksum(pkt, 20), 0x9ca9);
    store_be16(pkt + 10, inet_checksum(pkt, 20));
    SL_CHECK(pkt[10] == 0x9c && pkt[11] == 0xa9);
    const uint8_t odd[3] = {0x01, 0x02, 0x03};
    SL_CHECK_EQ(inet_checksum(odd, 3), (uint16_t)~(0x0102 + 0x0300));
    return sl_report();
}
