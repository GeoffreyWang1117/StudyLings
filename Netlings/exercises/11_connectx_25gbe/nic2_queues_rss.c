// EXERCISE: nic2_queues_rss — 队列数、ring 大小与 RSS 间接表
// TOPIC: ETHTOOL_GCHANNELS / ETHTOOL_GRINGPARAM / ETHTOOL_GRXFH / ETHTOOL_GRSSH
// DIFFICULTY: ★★★☆☆
// BOOK: man 8 ethtool（-l / -g / -n rx-flow-hash / -x）；Documentation/networking/scaling.rst（RSS）
// I AM NOT DONE
//
// 说明：
//   用法：nic2_queues_rss IFACE        打印队列/ring/RSS 概况
//         nic2_queues_rss --selftest   只跑纯函数自测（不需要网卡）
//   输出（测试按行解析）：
//     channels_max rx=R tx=T other=O combined=C      （ETHTOOL_GCHANNELS 的 max_*）
//     channels rx=R tx=T other=O combined=C          （当前值 *_count）
//     rings rx=CUR/MAX tx=CUR/MAX     或  rings unsupported
//     rxfh_tcp4 ip-src,ip-dst,l4-b-0-1,l4-b-2-3   或  rxfh_tcp4 unsupported
//     rss indir_size=N key_size=K hfunc=toeplitz|xor|crc32|other key=<hex>   或  rss unsupported
//     rss_dist 0:32 1:32 ...       间接表里每个队列出现的次数
//     rss_queues_used=Q            间接表实际覆盖了多少个队列
//     rss_out_of_range=X           指向 >= 队列总数的表项数（正常为 0）
//
//   多队列网卡的收包路径：网卡对每个包的 (src ip, dst ip, src port, dst port) 算 Toeplitz 哈希，
//   用哈希值低几位查"间接表"（indirection table，mlx5 默认 256 项），表项就是 RX 队列号；
//   每个队列有自己的 MSI-X 中断（nic4），中断绑在哪个 CPU，这个流的软中断/协议栈处理就在哪个 CPU。
//   - ETHTOOL_GCHANNELS：mlx5 用 "combined" 通道（一对 RX+TX 队列共用一个中断/完成向量），
//     默认等于本 NUMA 节点的核数左右；`ethtool -L IFACE combined N` 可以改
//   - ETHTOOL_GRINGPARAM：每个队列的描述符数。ring 太小 → 突发流量时 rx_out_of_buffer 丢包；
//     太大 → 缓存命中下降、延迟上升。25G 常见调优：rx 4096/8192
//   - ETHTOOL_GRXFH（flow_type = TCP_V4_FLOW）：哈希用哪些字段。UDP 默认可能只哈希 IP，
//     同一对主机的所有 UDP 流落在同一个队列 —— 这是 QUIC/视频服务器单核打满的经典原因
//   - ETHTOOL_GRSSH：间接表和哈希 key，也是"两步"协议：先 indir_size = key_size = 0 调一次拿到尺寸，
//     再分配 sizeof(struct ethtool_rxfh) + indir_size*4 + key_size 字节调第二次。
//     rss_config[] 前 indir_size 个 u32 是间接表，紧接着 key_size 字节是 key。
//   veth 支持 channels（ethtool -L 可改 rx/tx 数），但不支持 ring/RSS → 打印 unsupported 并正常退出。
//
//   测试：--selftest 验证间接表分布统计和哈希字段格式化；在 netns 的 veth 上把通道设成 rx 2 tx 3
//   （需要 ethtool 命令，否则对照 /sys/class/net/DEV/queues），检查 channels 行和 unsupported 行。
//   真实机器（NETLINGS_IFACE=ConnectX）：combined > 1、间接表非空且覆盖所有 combined 队列。
//   这就是 nginx/Envoy 多 worker 能线性扩展的前提：流被均匀撒到多个队列 → 多个 CPU。

#include <errno.h>
#include <inttypes.h>
#include <linux/ethtool.h>
#include <linux/sockios.h>
#include <net/if.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

// hfunc 位（内核 include/linux/ethtool.h 里的 ETH_RSS_HASH_*，uapi 头文件没有导出，只导出了位序号的含义）
enum { RSS_HASH_TOP = 1u << 0, RSS_HASH_XOR = 1u << 1, RSS_HASH_CRC32 = 1u << 2 };

static int ethtool_ioctl(int fd, const char *iface, void *data) {
    struct ifreq ifr = {};
    snprintf(ifr.ifr_name, sizeof ifr.ifr_name, "%s", iface);
    ifr.ifr_data = data;
    return ioctl(fd, SIOCETHTOOL, &ifr);
}

static bool is_unsupported(int err) {
    return err == EOPNOTSUPP || err == ENOTSUP || err == EINVAL;
}

// ---------- 纯函数（--selftest 覆盖） ----------

// 统计间接表 indir[0..n) 中每个队列出现的次数，写入 counts[0..nq)（>= nq 的表项计入 *out_of_range）。
// 返回被至少一个表项指向的队列个数。
static size_t indir_distribution(const uint32_t *indir, size_t n, uint32_t *counts, size_t nq,
                                 size_t *out_of_range) {
    memset(counts, 0, nq * sizeof *counts);
    *out_of_range = 0;
    // TODO: 遍历 indir[0..n)：表项 < nq 时 counts[表项]++，否则 (*out_of_range)++；
    //       然后返回 counts 里非 0 的队列个数
    return 0;
}

// 把 RXH_* 位图格式化成 "ip-src,ip-dst,..."；0 → "none"
static void rxh_fields_str(uint64_t data, char *buf, size_t len) {
    static const struct {
        uint64_t bit;
        const char *name;
    } names[] = {
        {RXH_L2DA, "l2da"},       {RXH_VLAN, "vlan"},           {RXH_L3_PROTO, "l3proto"},
        {RXH_IP_SRC, "ip-src"},   {RXH_IP_DST, "ip-dst"},       {RXH_L4_B_0_1, "l4-b-0-1"},
        {RXH_L4_B_2_3, "l4-b-2-3"}, {RXH_DISCARD, "discard"},
    };
    size_t off = 0;
    buf[0] = '\0';
    for (size_t i = 0; i < sizeof names / sizeof names[0]; i++) {
        if (!(data & names[i].bit))
            continue;
        int w = snprintf(buf + off, len - off, "%s%s", off ? "," : "", names[i].name);
        if (w < 0 || (size_t)w >= len - off)
            return; // 截断：buf 仍以 '\0' 结尾
        off += (size_t)w;
    }
    if (off == 0)
        snprintf(buf, len, "none");
}

static const char *hfunc_str(uint8_t hfunc) {
    if (hfunc & RSS_HASH_TOP)
        return "toeplitz";
    if (hfunc & RSS_HASH_XOR)
        return "xor";
    if (hfunc & RSS_HASH_CRC32)
        return "crc32";
    return hfunc ? "other" : "unknown";
}

static int selftest(void) {
    uint32_t indir[128];
    for (size_t i = 0; i < 128; i++)
        indir[i] = (uint32_t)(i % 4);
    uint32_t counts[8];
    size_t oor = 99;
    SL_CHECK_EQ(indir_distribution(indir, 128, counts, 8, &oor), 4);
    SL_CHECK_EQ(counts[0], 32);
    SL_CHECK_EQ(counts[3], 32);
    SL_CHECK_EQ(counts[4], 0);
    SL_CHECK_EQ(oor, 0);

    for (size_t i = 0; i < 128; i++)
        indir[i] = 0;
    indir[5] = 9; // 超出 nq 的表项
    SL_CHECK_EQ(indir_distribution(indir, 128, counts, 8, &oor), 1);
    SL_CHECK_EQ(counts[0], 127);
    SL_CHECK_EQ(oor, 1);
    SL_CHECK_EQ(indir_distribution(indir, 0, counts, 8, &oor), 0);

    char buf[128];
    rxh_fields_str(RXH_IP_SRC | RXH_IP_DST | RXH_L4_B_0_1 | RXH_L4_B_2_3, buf, sizeof buf);
    SL_CHECK(strcmp(buf, "ip-src,ip-dst,l4-b-0-1,l4-b-2-3") == 0);
    rxh_fields_str(RXH_IP_SRC | RXH_IP_DST, buf, sizeof buf);
    SL_CHECK(strcmp(buf, "ip-src,ip-dst") == 0);
    rxh_fields_str(0, buf, sizeof buf);
    SL_CHECK(strcmp(buf, "none") == 0);
    char tiny[8];
    rxh_fields_str(RXH_IP_SRC | RXH_IP_DST, tiny, sizeof tiny);
    SL_CHECK(strlen(tiny) < sizeof tiny);
    SL_CHECK(strcmp(hfunc_str(RSS_HASH_TOP), "toeplitz") == 0);
    return sl_report();
}

// ---------- ioctl 查询 ----------

// 返回 0 成功；否则返回 errno
static int get_channels(int fd, const char *iface, struct ethtool_channels *ch) {
    *ch = (struct ethtool_channels){.cmd = ETHTOOL_GCHANNELS};
    // TODO: 用 ethtool_ioctl 发出 ETHTOOL_GCHANNELS 请求；失败返回 errno，成功返回 0
    return 0;
}

static int get_rings(int fd, const char *iface, struct ethtool_ringparam *ring) {
    *ring = (struct ethtool_ringparam){.cmd = ETHTOOL_GRINGPARAM};
    return ethtool_ioctl(fd, iface, ring) < 0 ? errno : 0;
}

static int get_rxfh_fields(int fd, const char *iface, uint32_t flow_type, uint64_t *fields) {
    struct ethtool_rxnfc nfc = {.cmd = ETHTOOL_GRXFH, .flow_type = flow_type};
    if (ethtool_ioctl(fd, iface, &nfc) < 0)
        return errno;
    *fields = nfc.data;
    return 0;
}

// ETHTOOL_GRSSH 两步：成功时 *out 指向 calloc 的结构（调用者 free），返回 0；否则返回 errno
static int get_rss(int fd, const char *iface, struct ethtool_rxfh **out) {
    // TODO: 第 1 步：struct ethtool_rxfh sizes = {.cmd = ETHTOOL_GRSSH}（indir_size = key_size = 0），
    //       ioctl 后内核填回 indir_size / key_size；失败返回 errno（veth 上是 EOPNOTSUPP）
    // TODO: 第 2 步：calloc(sizeof(struct ethtool_rxfh) + indir_size * 4 + key_size)，填好 cmd 和
    //       两个尺寸再 ioctl 一次；成功时 *out = 该指针并返回 0，失败记得 free
    *out = nullptr;
    return EOPNOTSUPP;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 2 && strcmp(argv[1], "--selftest") == 0)
        return selftest();
    if (argc != 2) {
        fprintf(stderr, "usage: %s IFACE | --selftest\n", argv[0]);
        return 2;
    }
    const char *iface = argv[1];
    if (strlen(iface) >= IFNAMSIZ) {
        fprintf(stderr, "%s: 网卡名太长\n", iface);
        return 2;
    }
    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    printf("iface=%s\n", iface);

    struct ethtool_channels ch;
    int err = get_channels(fd, iface, &ch);
    if (err) {
        fprintf(stderr, "ioctl(SIOCETHTOOL, ETHTOOL_GCHANNELS) on %s: %s\n", iface, strerror(err));
        close(fd);
        return 1;
    }
    printf("channels_max rx=%u tx=%u other=%u combined=%u\n", ch.max_rx, ch.max_tx, ch.max_other,
           ch.max_combined);
    printf("channels rx=%u tx=%u other=%u combined=%u\n", ch.rx_count, ch.tx_count, ch.other_count,
           ch.combined_count);

    struct ethtool_ringparam ring;
    err = get_rings(fd, iface, &ring);
    if (err == 0)
        printf("rings rx=%u/%u tx=%u/%u\n", ring.rx_pending, ring.rx_max_pending, ring.tx_pending,
               ring.tx_max_pending);
    else if (is_unsupported(err))
        printf("rings unsupported\n");
    else
        fprintf(stderr, "ioctl(ETHTOOL_GRINGPARAM) on %s: %s\n", iface, strerror(err));

    uint64_t fields = 0;
    err = get_rxfh_fields(fd, iface, TCP_V4_FLOW, &fields);
    if (err == 0) {
        char buf[128];
        rxh_fields_str(fields, buf, sizeof buf);
        printf("rxfh_tcp4 %s\n", buf);
    } else if (is_unsupported(err)) {
        printf("rxfh_tcp4 unsupported\n");
    } else {
        fprintf(stderr, "ioctl(ETHTOOL_GRXFH, TCP_V4_FLOW) on %s: %s\n", iface, strerror(err));
    }

    int rc = 0;
    struct ethtool_rxfh *rss = nullptr;
    err = get_rss(fd, iface, &rss);
    if (err == 0 && rss->indir_size == 0) {
        printf("rss unsupported\n"); // 驱动实现了 get_rxfh 但没有间接表
    } else if (err == 0) {
        const uint32_t *indir = rss->rss_config;
        const uint8_t *key = (const uint8_t *)(rss->rss_config + rss->indir_size);
        printf("rss indir_size=%u key_size=%u hfunc=%s key=", rss->indir_size, rss->key_size,
               hfunc_str(rss->hfunc));
        for (uint32_t i = 0; i < rss->key_size; i++)
            printf("%02x", key[i]);
        printf("\n");

        // 队列号的上界：RX 队列总数（mlx5 全是 combined）；越界表项说明配置异常，单独报告
        size_t nq = (size_t)ch.rx_count + ch.combined_count;
        if (nq == 0)
            nq = 1;
        uint32_t *counts = calloc(nq, sizeof *counts);
        if (counts == nullptr) {
            perror("calloc");
            rc = 1;
        } else {
            size_t oor = 0;
            size_t used = indir_distribution(indir, rss->indir_size, counts, nq, &oor);
            printf("rss_dist");
            for (size_t q = 0; q < nq; q++)
                printf(" %zu:%" PRIu32, q, counts[q]);
            printf("\n");
            printf("rss_queues_used=%zu\n", used);
            printf("rss_out_of_range=%zu\n", oor);
            free(counts);
        }
    } else if (is_unsupported(err)) {
        printf("rss unsupported\n");
    } else {
        fprintf(stderr, "ioctl(ETHTOOL_GRSSH) on %s: %s\n", iface, strerror(err));
        rc = 1;
    }
    free(rss);
    close(fd);
    return rc;
}
