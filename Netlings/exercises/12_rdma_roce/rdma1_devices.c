// EXERCISE: rdma1_devices — 枚举 RDMA 设备、端口与 GID 表，挑出 RoCE v2 的 GID 下标
// TOPIC: ibv_get_device_list / ibv_query_device / ibv_query_port / sysfs gids 与 gid_attrs/types
// DIFFICULTY: ★★☆☆☆
// BOOK: man 3 ibv_get_device_list；man 3 ibv_query_port；man 3 ibv_query_gid；RDMA Aware Networks Programming User Manual（NVIDIA）；InfiniBand Architecture Spec Annex A17（RoCE v2）
// I AM NOT DONE
//
// 说明：
//   用法：rdma1_devices [DEV]                      列出所有（或指定的）RDMA 设备
//         rdma1_devices --selftest                 纯函数自测（不需要设备）
//         rdma1_devices --sysfs-root DIR DEV PORT  只扫描 DIR/DEV/ports/PORT/ 下的 GID 表（测试用假 sysfs）
//   DEV 缺省时读环境变量 NETLINGS_RDMA_DEV，再没有就列出全部设备。
//   输出：
//     device=mlx5_0 node_guid=0c42:a103:0012:3456 fw=16.35.2000 ports=1
//     port=1 state=PORT_ACTIVE active_mtu=1024 max_mtu=4096 link_layer=Ethernet speed=25.0Gbps width=1x lid=0
//     gid index=3 gid=::ffff:192.168.1.10 type=roce_v2 ndev=enp65s0f0np0
//     roce_v2_gid_index=3      （以太网端口上找不到时打印 -1 并说明原因）
//   没有设备：打印 "no RDMA device: load rdma_rxe or use ConnectX" 到 stderr，exit 2。
//
//   ── 本章背景 ──────────────────────────────────────────────────────────────────────────
//   * Kernel bypass：socket 的每次 send/recv 都要陷入内核、拷贝数据、走协议栈。RDMA 把传输层做进网卡：
//     应用在用户态直接往网卡的门铃寄存器写 WQE（工作请求），网卡自己 DMA 读写应用内存、自己做
//     可靠传输（重传/确认），完成后在 CQ 里放一个 CQE；数据路径上既没有系统调用也没有拷贝。
//     单边操作（RDMA WRITE/READ，见 rdma3）连对端 CPU 都不打扰。端到端延迟 ~2 µs，TCP 通常 10~50 µs。
//   * 内存注册（ibv_reg_mr）：网卡用物理地址做 DMA，所以缓冲区必须提前"注册"：内核把这些页
//     pin 住（不能被换出/迁移）并把虚拟→物理映射装进网卡的 MTT，返回 lkey（本地访问）/ rkey（授权远端访问）。
//     注册很慢（毫秒级），所以真实系统（NCCL、UCX、SPDK、Redis-RDMA）都会预先注册一大块内存池复用。
//     非 root 用户受 RLIMIT_MEMLOCK（ulimit -l）限制，注册失败时先看它。
//   * RC vs UD：RC（Reliable Connected）一对一连接、网卡保证可靠有序，支持 RDMA WRITE/READ/原子操作，
//     但每个对端一个 QP，大规模集群 QP 数量会爆（网卡缓存装不下 QP 上下文 → 性能下降）；
//     UD（Unreliable Datagram）一个 QP 可以对任意多个对端收发，只支持 SEND/RECV、单个 MTU 大小的消息、
//     不保证送达 —— 类似 UDP。DC（Dynamically Connected，mlx5 私有）是两者的折中。
//   * RoCE v2 = InfiniBand 传输层封装在 UDP（目的端口 4791）/IP 里，可以跨三层路由。
//     GID 就是 RoCE 里的"地址"：v2 的 GID 是 IPv4 映射地址 ::ffff:a.b.c.d 或 IPv6 地址。
//     同一块网卡上每个 IP 会同时生成 RoCE v1 和 v2 两个 GID 表项，所以要看 gid_attrs/types/<i>
//     挑出 "RoCE v2" 且是 IPv4 映射的那个下标 —— 后面几题建 QP 时的 sgid_index 就用它。
//   * 为什么要无损以太网：IB 的可靠传输假设链路基本不丢包。mlx5 丢一个包要走 go-back-N 重传，
//     吞吐会断崖式下跌。所以 RoCE 部署通常配 PFC（802.1Qbb，按优先级暂停帧，让交换机缓冲快满时
//     让上游"停一下"）+ ECN 标记 + DCQCN（网卡根据 ECN 回传的 CNP 降速的拥塞控制）。
//     没有 PFC 时（"Resilient RoCE"）靠 ECN/DCQCN 和网卡的选择性重传也能跑，但拥塞时尾延迟和吞吐
//     都会变差；PFC 本身又有 head-of-line blocking、PFC storm/死锁的风险 —— 这是 RoCE 运维的核心难题。
//   * 没有 RDMA 网卡时可以用 Soft-RoCE（rdma_rxe，内核用软件实现 RoCE v2，跑在任意以太网卡上）：
//       sudo modprobe rdma_rxe && sudo rdma link add rxe0 type rxe netdev <iface>
//     功能完整、性能一般，足以学习 verbs 编程。
//
//   测试：--selftest 验证 GID 字符串解析 / IPv4 映射判断 / 类型解析；--sysfs-root 用假 sysfs 目录验证
//   扫描与挑选逻辑；本机没有设备时验证 "no RDMA device" 提示。有设备时（NETLINGS_RDMA_DEV）
//   检查端口信息并与 sysfs 对照 roce_v2_gid_index。

#include <arpa/inet.h>
#include <endian.h>
#include <errno.h>
#include <infiniband/verbs.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sl.h"

enum { MAX_GIDS = 1024 };
enum gid_type { GID_TYPE_UNKNOWN, GID_TYPE_IB_ROCE_V1, GID_TYPE_ROCE_V2 };

typedef struct {
    int index;
    uint8_t raw[16];
    enum gid_type type;
    char ndev[32];
} gid_entry;

#define SYSFS_IB "/sys/class/infiniband"

// ---------- 纯函数（--selftest 覆盖） ----------

// sysfs 的 GID 文本："0000:0000:0000:0000:0000:ffff:c0a8:010a"（8 组 4 位十六进制）
static bool parse_sysfs_gid(const char *s, uint8_t raw[16]) {
    // TODO: 依次解析 8 组、每组恰好 4 个十六进制字符（大小写都可能），组间是 ':'；
    //       每组的 16 位值按大端写入 raw[2g]（高字节）和 raw[2g+1]（低字节）。
    //       任何非法字符、组数不对、结尾多出东西（除了一个 '\n'）都返回 false
    memset(raw, 0, 16);
    return false;
}

static bool gid_is_zero(const uint8_t raw[16]) {
    for (int i = 0; i < 16; i++)
        if (raw[i])
            return false;
    return true;
}

// ::ffff:a.b.c.d —— 前 10 字节 0，接着 2 字节 0xff
static bool gid_is_ipv4_mapped(const uint8_t raw[16]) {
    // TODO: raw[0..9] 全为 0 且 raw[10] == raw[11] == 0xff
    return false;
}

static void gid_to_str(const uint8_t raw[16], char *buf, size_t len) {
    if (inet_ntop(AF_INET6, raw, buf, (socklen_t)len) == nullptr)
        snprintf(buf, len, "?");
}

static enum gid_type parse_gid_type(const char *s) {
    size_t n = strcspn(s, "\n");
    if (n == 7 && strncmp(s, "RoCE v2", 7) == 0)
        return GID_TYPE_ROCE_V2;
    if (n == 10 && strncmp(s, "IB/RoCE v1", 10) == 0)
        return GID_TYPE_IB_ROCE_V1;
    return GID_TYPE_UNKNOWN;
}

static const char *gid_type_name(enum gid_type t) {
    switch (t) {
    case GID_TYPE_ROCE_V2: return "roce_v2";
    case GID_TYPE_IB_ROCE_V1: return "ib_roce_v1";
    default: return "unknown";
    }
}

// 第一个 RoCE v2 + IPv4 映射的表项下标（gid_entry.index），没有返回 -1
static int pick_roce_v2_ipv4(const gid_entry *e, int n) {
    // TODO: 返回第一个 type == GID_TYPE_ROCE_V2 且 GID 是 IPv4 映射地址的表项的 .index
    //       （注意是 GID 表里的下标 e[i].index，不是数组下标 i —— 空表项被跳过了）
    return -1;
}

// ---------- sysfs 扫描 ----------

static bool read_small(const char *path, char *buf, size_t len) {
    FILE *f = fopen(path, "r");
    if (f == nullptr)
        return false;
    bool ok = fgets(buf, (int)len, f) != nullptr;
    fclose(f);
    if (ok)
        buf[strcspn(buf, "\n")] = '\0';
    return ok;
}

// 扫描 root/dev/ports/port/gids/0..tbl_len-1（tbl_len < 0：扫到第一个不存在的文件为止），
// 跳过全 0 的空表项。类型文件对空表项会返回 EINVAL —— 读不到就记为 unknown。返回表项数
static int scan_gid_table(const char *root, const char *dev, int port, int tbl_len, gid_entry *out, int cap) {
    int n = 0;
    int limit = tbl_len < 0 ? MAX_GIDS : tbl_len;
    for (int i = 0; i < limit && n < cap; i++) {
        char path[512], buf[128];
        snprintf(path, sizeof path, "%s/%s/ports/%d/gids/%d", root, dev, port, i);
        if (!read_small(path, buf, sizeof buf)) {
            if (errno == ENOENT && tbl_len < 0)
                break;
            continue;
        }
        gid_entry e = {.index = i};
        if (!parse_sysfs_gid(buf, e.raw) || gid_is_zero(e.raw))
            continue;
        snprintf(path, sizeof path, "%s/%s/ports/%d/gid_attrs/types/%d", root, dev, port, i);
        e.type = read_small(path, buf, sizeof buf) ? parse_gid_type(buf) : GID_TYPE_UNKNOWN;
        snprintf(path, sizeof path, "%s/%s/ports/%d/gid_attrs/ndevs/%d", root, dev, port, i);
        if (!read_small(path, e.ndev, sizeof e.ndev))
            snprintf(e.ndev, sizeof e.ndev, "-");
        out[n++] = e;
    }
    return n;
}

static int print_gids(const char *root, const char *dev, int port, int tbl_len, bool ethernet) {
    static gid_entry gids[MAX_GIDS];
    int n = scan_gid_table(root, dev, port, tbl_len, gids, MAX_GIDS);
    for (int i = 0; i < n; i++) {
        char s[INET6_ADDRSTRLEN];
        gid_to_str(gids[i].raw, s, sizeof s);
        printf("gid index=%d gid=%s type=%s ndev=%s\n", gids[i].index, s, gid_type_name(gids[i].type), gids[i].ndev);
    }
    if (!ethernet)
        return -1;
    int idx = pick_roce_v2_ipv4(gids, n);
    printf("roce_v2_gid_index=%d\n", idx);
    if (idx < 0)
        fprintf(stderr, "%s port %d: 没有 RoCE v2 IPv4 GID —— 对应的网卡（ndev）配置 IPv4 地址并 up 了吗？\n", dev, port);
    return idx;
}

static int selftest(void) {
    uint8_t raw[16];
    SL_CHECK(parse_sysfs_gid("0000:0000:0000:0000:0000:ffff:c0a8:010a\n", raw));
    SL_CHECK_EQ(raw[10], 0xff);
    SL_CHECK_EQ(raw[12], 192);
    SL_CHECK_EQ(raw[15], 10);
    SL_CHECK(gid_is_ipv4_mapped(raw));
    char s[INET6_ADDRSTRLEN];
    gid_to_str(raw, s, sizeof s);
    SL_CHECK(strcmp(s, "::ffff:192.168.1.10") == 0);

    SL_CHECK(parse_sysfs_gid("fe80:0000:0000:0000:0e42:a1ff:fe12:3456", raw));
    SL_CHECK_EQ(raw[0], 0xfe);
    SL_CHECK_EQ(raw[1], 0x80);
    SL_CHECK(!gid_is_ipv4_mapped(raw));
    SL_CHECK(!gid_is_zero(raw));
    SL_CHECK(parse_sysfs_gid("0000:0000:0000:0000:0000:0000:0000:0000", raw));
    SL_CHECK(gid_is_zero(raw));
    SL_CHECK(!gid_is_ipv4_mapped(raw));
    SL_CHECK(!parse_sysfs_gid("0000:0000", raw));
    SL_CHECK(!parse_sysfs_gid("zz00:0000:0000:0000:0000:ffff:c0a8:010a", raw));
    SL_CHECK(!parse_sysfs_gid("0000:0000:0000:0000:0000:ffff:c0a8:010a:ffff", raw));

    SL_CHECK_EQ(parse_gid_type("RoCE v2\n"), GID_TYPE_ROCE_V2);
    SL_CHECK_EQ(parse_gid_type("IB/RoCE v1\n"), GID_TYPE_IB_ROCE_V1);
    SL_CHECK_EQ(parse_gid_type("RoCE v22"), GID_TYPE_UNKNOWN);

    gid_entry e[4] = {};
    e[0] = (gid_entry){.index = 0, .raw = {0xfe, 0x80, [15] = 1}, .type = GID_TYPE_ROCE_V2}; // v2 但不是 IPv4
    e[1] = (gid_entry){.index = 2, .raw = {[10] = 0xff, [11] = 0xff, 10, 0, 0, 1}, .type = GID_TYPE_IB_ROCE_V1};
    e[2] = (gid_entry){.index = 3, .raw = {[10] = 0xff, [11] = 0xff, 10, 0, 0, 1}, .type = GID_TYPE_ROCE_V2};
    SL_CHECK_EQ(pick_roce_v2_ipv4(e, 3), 3);
    SL_CHECK_EQ(pick_roce_v2_ipv4(e, 2), -1);
    return sl_report();
}

// ---------- 设备查询 ----------

static const char *mtu_str(enum ibv_mtu m) {
    switch (m) {
    case IBV_MTU_256: return "256";
    case IBV_MTU_512: return "512";
    case IBV_MTU_1024: return "1024";
    case IBV_MTU_2048: return "2048";
    case IBV_MTU_4096: return "4096";
    default: return "?";
    }
}

// ibv_port_attr.active_speed 编码 → 每 lane Gbps
static double lane_gbps(uint8_t speed) {
    switch (speed) {
    case 1: return 2.5;   // SDR
    case 2: return 5.0;   // DDR
    case 4: return 10.0;  // QDR
    case 8: return 10.0;  // FDR10
    case 16: return 14.0; // FDR
    case 32: return 25.0; // EDR（25GbE 的 RoCE 端口报告为 EDR 1x）
    case 64: return 50.0; // HDR
    case 128: return 100.0; // NDR
    default: return 0.0;
    }
}

static int width_lanes(uint8_t w) {
    switch (w) {
    case 1: return 1;
    case 2: return 4;
    case 4: return 8;
    case 8: return 12;
    case 16: return 2;
    default: return 0;
    }
}

static const char *link_layer_str(uint8_t ll) {
    switch (ll) {
    case IBV_LINK_LAYER_ETHERNET: return "Ethernet";
    case IBV_LINK_LAYER_INFINIBAND: return "InfiniBand";
    default: return "unspecified";
    }
}

static bool show_device(struct ibv_device *dev) {
    const char *name = ibv_get_device_name(dev);
    struct ibv_context *ctx = ibv_open_device(dev);
    if (ctx == nullptr) {
        fprintf(stderr, "ibv_open_device(%s): %s\n", name, strerror(errno));
        return false;
    }
    struct ibv_device_attr attr;
    int err = ibv_query_device(ctx, &attr);
    if (err) {
        fprintf(stderr, "ibv_query_device(%s): %s\n", name, strerror(err));
        ibv_close_device(ctx);
        return false;
    }
    uint64_t guid = be64toh(ibv_get_device_guid(dev));
    printf("device=%s node_guid=%04x:%04x:%04x:%04x fw=%s ports=%u\n", name, (unsigned)(guid >> 48) & 0xffff,
           (unsigned)(guid >> 32) & 0xffff, (unsigned)(guid >> 16) & 0xffff, (unsigned)guid & 0xffff,
           attr.fw_ver[0] ? attr.fw_ver : "-", attr.phys_port_cnt);

    bool ok = true;
    for (uint8_t p = 1; p <= attr.phys_port_cnt; p++) {
        struct ibv_port_attr pa;
        err = ibv_query_port(ctx, p, &pa);
        if (err) {
            fprintf(stderr, "ibv_query_port(%s, %u): %s\n", name, p, strerror(err));
            ok = false;
            continue;
        }
        int lanes = width_lanes(pa.active_width);
        printf("port=%u state=%s active_mtu=%s max_mtu=%s link_layer=%s speed=%.1fGbps width=%dx lid=%u "
               "gid_tbl_len=%d\n",
               p, ibv_port_state_str(pa.state), mtu_str(pa.active_mtu), mtu_str(pa.max_mtu),
               link_layer_str(pa.link_layer), lane_gbps(pa.active_speed) * lanes, lanes, pa.lid, pa.gid_tbl_len);
        print_gids(SYSFS_IB, name, p, pa.gid_tbl_len, pa.link_layer == IBV_LINK_LAYER_ETHERNET);
    }
    err = ibv_close_device(ctx);
    if (err) {
        fprintf(stderr, "ibv_close_device(%s): %s\n", name, strerror(errno));
        ok = false;
    }
    return ok;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 2 && strcmp(argv[1], "--selftest") == 0)
        return selftest();
    if (argc == 5 && strcmp(argv[1], "--sysfs-root") == 0) {
        int port = atoi(argv[4]);
        if (port <= 0) {
            fprintf(stderr, "bad port %s\n", argv[4]);
            return 2;
        }
        return print_gids(argv[2], argv[3], port, -1, true) >= 0 ? 0 : 1;
    }
    if (argc > 2) {
        fprintf(stderr, "usage: %s [DEV] | --selftest | --sysfs-root DIR DEV PORT\n", argv[0]);
        return 2;
    }
    const char *want = argc == 2 ? argv[1] : getenv("NETLINGS_RDMA_DEV");
    if (want && !*want)
        want = nullptr;

    int num = 0;
    errno = 0;
    struct ibv_device **list = ibv_get_device_list(&num);
    if (list == nullptr || num == 0) {
        // 没有 ib_uverbs 时返回 NULL + ENOSYS；有内核支持但没有设备时返回空列表
        fprintf(stderr, "no RDMA device: load rdma_rxe or use ConnectX（ibv_get_device_list: %s）\n",
                list == nullptr ? strerror(errno) : "0 devices");
        if (list)
            ibv_free_device_list(list);
        return 2;
    }
    bool found = false, ok = true;
    for (int i = 0; i < num; i++) {
        if (want && strcmp(ibv_get_device_name(list[i]), want) != 0)
            continue;
        found = true;
        ok = show_device(list[i]) && ok;
    }
    ibv_free_device_list(list);
    if (!found) {
        fprintf(stderr, "RDMA device %s not found（rdma link / ibv_devices 查看设备名）\n", want);
        return 2;
    }
    return ok ? 0 : 1;
}
