// EXERCISE: nic1_ethtool_info — 用 ioctl(SIOCETHTOOL) 读网卡驱动、固件与链路速率
// TOPIC: SIOCETHTOOL / ETHTOOL_GDRVINFO / ETHTOOL_GLINKSETTINGS（nwords 握手）/ SIOCGIFMTU / sysfs numa_node
// DIFFICULTY: ★★★☆☆
// BOOK: man 8 ethtool；include/uapi/linux/ethtool.h（struct ethtool_link_settings 注释）；modern Linux notes
//
// 说明：
//   用法：nic1_ethtool_info IFACE
//   输出（每行 key=value，测试按行解析）：
//     iface= driver= version= firmware= bus_info=
//     speed_mbps=（未知时 -1） duplex=full|half|unknown autoneg=on|off
//     port=tp|fibre|da|aui|bnc|mii|none|other  link_mode_nwords=N  mtu=  numa_node=（没有时 -1）
//
//   `ethtool -i eth0` / `ethtool eth0` 背后就是这几个 ioctl（新版 ethtool 优先走 genetlink，
//   但 ioctl 接口仍然完整可用，也更容易在 C 里直接看清数据结构）：
//   - ETHTOOL_GDRVINFO：驱动名（ConnectX 是 mlx5_core）、驱动版本、固件版本（fw 升级/排障必看）、
//     PCI 地址 bus-info（后面找 IRQ、NUMA 都靠它）
//   - ETHTOOL_GLINKSETTINGS：取代老的 ETHTOOL_GSET。老接口的 link mode 位图只有 32 位，
//     装不下 25G/50G/100G/200G 这些新模式，所以新接口的位图长度可变，用"握手"协商：
//       第 1 次调用 link_mode_masks_nwords = 0 → 内核**不填任何数据**，只把
//         link_mode_masks_nwords 改成 -N（负数！）返回，告诉你它需要 N 个 u32；
//       第 2 次调用分配 sizeof(struct) + 3*N*4 字节（supported/advertising/lp_advertising
//         三张位图），nwords 填 +N，这次内核才真正填 speed/duplex/autoneg/port。
//     只调一次就去读 speed，会读到 0 —— 这正是本题的坑。
//   - SIOCGIFMTU：MTU（25G 数据中心里常用 9000 jumbo frame，RoCE 的 active_mtu 也受它限制）
//   - /sys/class/net/IFACE/device/numa_node：网卡挂在哪个 NUMA 节点。跨 NUMA 收包要走
//     UPI/Infinity Fabric，25G 线速下能掉 20%+ 吞吐。虚拟网卡（veth/lo）没有 device → 打印 -1
//
//   测试：在 netns 里建一对 veth（驱动 "veth"，速率 10000，MTU 设成 1400），检查各字段；
//   不存在的网卡要报错退出（错误信息带 strerror）。
//   真实机器：export NETLINGS_IFACE=<ConnectX 网卡名>，额外检查 driver=mlx5_core、firmware 非空、
//   speed 与 /sys/class/net/IFACE/speed 一致（25GbE 应为 25000）、numa_node 与 sysfs 一致。

#include <errno.h>
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

// 对 IFACE 发一个 SIOCETHTOOL 请求。data 指向以 u32 cmd 开头的 ethtool 结构体
static int ethtool_ioctl(int fd, const char *iface, void *data) {
    struct ifreq ifr = {};
    snprintf(ifr.ifr_name, sizeof ifr.ifr_name, "%s", iface);
    ifr.ifr_data = data;
    return ioctl(fd, SIOCETHTOOL, &ifr);
}

static bool get_drvinfo(int fd, const char *iface, struct ethtool_drvinfo *info) {
    *info = (struct ethtool_drvinfo){.cmd = ETHTOOL_GDRVINFO};
    if (ethtool_ioctl(fd, iface, info) < 0) {
        fprintf(stderr, "ioctl(SIOCETHTOOL, ETHTOOL_GDRVINFO) on %s: %s\n", iface, strerror(errno));
        return false;
    }
    return true;
}

typedef struct {
    int64_t speed_mbps; // -1 = 未知
    uint8_t duplex;
    uint8_t autoneg;
    uint8_t port;
    int nwords;
} link_info;

// ETHTOOL_GLINKSETTINGS 的两步握手
static bool get_link_settings(int fd, const char *iface, link_info *out) {
    // 第 1 步：nwords = 0，内核回填 -N
    struct ethtool_link_settings probe = {.cmd = ETHTOOL_GLINKSETTINGS};
    if (ethtool_ioctl(fd, iface, &probe) < 0) {
        fprintf(stderr, "ioctl(SIOCETHTOOL, ETHTOOL_GLINKSETTINGS) on %s: %s\n", iface, strerror(errno));
        return false;
    }
    if (probe.link_mode_masks_nwords >= 0 || probe.cmd != ETHTOOL_GLINKSETTINGS) {
        fprintf(stderr, "%s: 内核没有按协议返回负的 link_mode_masks_nwords（%d）\n", iface,
                probe.link_mode_masks_nwords);
        return false;
    }
    int nwords = -probe.link_mode_masks_nwords;

    // 第 2 步：带上 3 张 nwords 长的位图再调一次
    size_t sz = sizeof(struct ethtool_link_settings) + 3 * (size_t)nwords * sizeof(uint32_t);
    struct ethtool_link_settings *req = calloc(1, sz);
    if (req == nullptr) {
        perror("calloc");
        return false;
    }
    req->cmd = ETHTOOL_GLINKSETTINGS;
    req->link_mode_masks_nwords = (int8_t)nwords;
    bool ok = false;
    if (ethtool_ioctl(fd, iface, req) < 0) {
        fprintf(stderr, "ioctl(SIOCETHTOOL, ETHTOOL_GLINKSETTINGS nwords=%d) on %s: %s\n", nwords, iface,
                strerror(errno));
    } else if (req->link_mode_masks_nwords != nwords) {
        fprintf(stderr, "%s: 第二次握手 nwords 不一致（%d != %d）\n", iface, req->link_mode_masks_nwords, nwords);
    } else {
        out->speed_mbps = req->speed == (uint32_t)SPEED_UNKNOWN ? -1 : (int64_t)req->speed;
        out->duplex = req->duplex;
        out->autoneg = req->autoneg;
        out->port = req->port;
        out->nwords = nwords;
        ok = true;
    }
    free(req);
    return ok;
}

static bool get_mtu(int fd, const char *iface, int *mtu) {
    struct ifreq ifr = {};
    snprintf(ifr.ifr_name, sizeof ifr.ifr_name, "%s", iface);
    if (ioctl(fd, SIOCGIFMTU, &ifr) < 0) {
        fprintf(stderr, "ioctl(SIOCGIFMTU) on %s: %s\n", iface, strerror(errno));
        return false;
    }
    *mtu = ifr.ifr_mtu;
    return true;
}

// /sys/class/net/IFACE/device/numa_node；文件不存在（虚拟设备）返回 -1
static int read_numa_node(const char *iface) {
    char path[256];
    snprintf(path, sizeof path, "/sys/class/net/%s/device/numa_node", iface);
    FILE *f = fopen(path, "r");
    if (f == nullptr) {
        if (errno != ENOENT)
            fprintf(stderr, "open %s: %s\n", path, strerror(errno));
        return -1;
    }
    int node = -1;
    if (fscanf(f, "%d", &node) != 1)
        node = -1;
    fclose(f);
    return node;
}

static const char *duplex_str(uint8_t d) {
    switch (d) {
    case DUPLEX_FULL: return "full";
    case DUPLEX_HALF: return "half";
    default: return "unknown";
    }
}

static const char *port_str(uint8_t p) {
    switch (p) {
    case PORT_TP: return "tp";
    case PORT_AUI: return "aui";
    case PORT_BNC: return "bnc";
    case PORT_MII: return "mii";
    case PORT_FIBRE: return "fibre";
    case PORT_DA: return "da";
    case PORT_NONE: return "none";
    default: return "other";
    }
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s IFACE\n", argv[0]);
        return 2;
    }
    const char *iface = argv[1];
    if (strlen(iface) >= IFNAMSIZ) {
        fprintf(stderr, "%s: 网卡名太长（最多 %d 字符）\n", iface, IFNAMSIZ - 1);
        return 2;
    }

    // 任意 socket 都能承载 SIOCETHTOOL；AF_INET/SOCK_DGRAM 不需要任何特权
    int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");

    struct ethtool_drvinfo info;
    link_info link = {};
    int mtu = 0;
    bool ok = get_drvinfo(fd, iface, &info) && get_link_settings(fd, iface, &link) && get_mtu(fd, iface, &mtu);
    close(fd);
    if (!ok)
        return 1;

    printf("iface=%s\n", iface);
    printf("driver=%.*s\n", (int)sizeof info.driver, info.driver);
    printf("version=%.*s\n", (int)sizeof info.version, info.version);
    printf("firmware=%.*s\n", (int)sizeof info.fw_version, info.fw_version);
    printf("bus_info=%.*s\n", (int)sizeof info.bus_info, info.bus_info);
    printf("speed_mbps=%lld\n", (long long)link.speed_mbps);
    printf("duplex=%s\n", duplex_str(link.duplex));
    printf("autoneg=%s\n", link.autoneg == AUTONEG_ENABLE ? "on" : "off");
    printf("port=%s\n", port_str(link.port));
    printf("link_mode_nwords=%d\n", link.nwords);
    printf("mtu=%d\n", mtu);
    printf("numa_node=%d\n", read_numa_node(iface));
    return 0;
}
