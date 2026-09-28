// EXERCISE: bpf2_xdp_firewall — XDP 丢弃发往黑名单 UDP 端口的包（HASH map + 字节序）
// TOPIC: XDP_DROP / XDP_PASS / BPF_MAP_TYPE_HASH / 用户态写 map / bpf_ntohs / __sync_fetch_and_add
// DIFFICULTY: ★★★☆☆
// BOOK: man 7 bpf-helpers；kernel Documentation/bpf/map_hash.rst；RFC 768 (UDP)；libbpf API docs
// I AM NOT DONE
//
// 说明：
//   用法：bpf2_xdp_firewall IFACE PORT...     （需要 root；运行到 SIGINT/SIGTERM 为止）
//   loader 加载程序后，把命令行上的每个 PORT 写进 HASH map "blocked_ports"
//   （key = __u16 端口号，**主机字节序**；value = __u64 该端口已丢弃的包数，初值 0），
//   然后以 generic 模式（NETLINGS_XDP_MODE=drv 可改 native）挂到 IFACE，打印 "ready"。
//   XDP 程序：Ethernet → IPv4 → UDP（每一层都要做 data_end 边界检查；IP 头长用 ihl*4；
//   非首片的 IP 分片没有 UDP 头，直接放行），若目的端口在 map 里 → 计数 +1 并 XDP_DROP，否则 XDP_PASS。
//   退出时（先 detach）打印每个端口 "port 9000 dropped N" 和 "total dropped N"。
//   字节序：包里的 udp->dest 是网络字节序（大端），map 的 key 是主机序；比较前必须 bpf_ntohs()。
//   探针（root + netns/veth）：防火墙所在 namespace 里有一个 UDP 服务器同时监听被封端口 9000 和
//   放行端口 10275（= 0x2823，恰好是 9000 = 0x2328 的字节交换！），对端各发 30 个包：
//   9000 一个都不能收到、10275 必须全部收到，loader 报告的丢弃数必须恰好等于 30；退出后不能残留 XDP。
//
//   这些东西用在哪：Cloudflare 的 L4Drop / "Gatebot" DDoS 缓解就是把攻击特征编译成 XDP 规则，
//   在驱动层 XDP_DROP，每核每秒丢上千万包而 CPU 几乎不涨；Meta 的 Katran 与 Cilium 也在 XDP 层做
//   过滤和负载均衡。规则放在 map 里、由用户态随时增删，程序本身无需重新加载 —— 这是 BPF "数据面程序 +
//   控制面写 map" 的标准分工（bpftool map update 也能手动改规则）。

#include <linux/types.h>

#ifdef __BPF__
// ============================== 内核侧：XDP 程序 ==============================
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <linux/ip.h>
#include <linux/udp.h>

#include <bpf/bpf_endian.h>
#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 1024);
    __type(key, __u16);   // 目的端口，主机字节序
    __type(value, __u64); // 丢弃计数
} blocked_ports SEC(".maps");

SEC("xdp")
int xdp_firewall(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end || eth->h_proto != bpf_htons(ETH_P_IP))
        return XDP_PASS;

    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end || ip->protocol != IPPROTO_UDP || ip->ihl < 5)
        return XDP_PASS;
    if (ip->frag_off & bpf_htons(0x1FFF)) // 非首片：没有 UDP 头
        return XDP_PASS;

    struct udphdr *udp = (void *)ip + ip->ihl * 4;
    if ((void *)(udp + 1) > data_end)
        return XDP_PASS;

    // BUG: udp->dest 是网络字节序（大端），而 loader 写入 map 的 key 是主机字节序。
    // TODO: 转换成主机序再查 map（提示：bpf_endian.h）
    __u16 port = udp->dest;
    __u64 *drops = bpf_map_lookup_elem(&blocked_ports, &port);
    if (!drops)
        return XDP_PASS;
    __sync_fetch_and_add(drops, 1); // HASH map 的 value 被所有 CPU 共享 → 原子加
    return XDP_DROP;
}

char LICENSE[] SEC("license") = "GPL";

#else
// ============================== 用户态：loader ==============================
#include <errno.h>
#include <linux/if_link.h>
#include <net/if.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <bpf/bpf.h>
#include <bpf/libbpf.h>

#include "sl.h"

#ifndef SL_BPF_OBJ
#error "SL_BPF_OBJ 应由 CMake 定义为 .bpf.o 的绝对路径"
#endif

static volatile sig_atomic_t stop_flag;

static void on_signal(int sig) { stop_flag = sig; }

static void install_handlers(void) {
    struct sigaction sa = {.sa_handler = on_signal};
    sigemptyset(&sa.sa_mask);
    if (sigaction(SIGINT, &sa, nullptr) < 0 || sigaction(SIGTERM, &sa, nullptr) < 0)
        sl_die("sigaction");
}

static __u32 xdp_mode_flags(const char **name) {
    const char *m = getenv("NETLINGS_XDP_MODE");
    if (m && strcmp(m, "drv") == 0) {
        *name = "native/drv";
        return XDP_FLAGS_DRV_MODE;
    }
    if (m && strcmp(m, "auto") == 0) {
        *name = "auto";
        return 0;
    }
    *name = "generic/skb";
    return XDP_FLAGS_SKB_MODE;
}

static bool parse_port(const char *s, __u16 *out) {
    char *end;
    errno = 0;
    long v = strtol(s, &end, 10);
    if (errno || *end || v < 1 || v > 65535)
        return false;
    *out = (__u16)v;
    return true;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc < 3) {
        fprintf(stderr, "usage: %s IFACE PORT...\n", argv[0]);
        return 2;
    }
    const char *ifname = argv[1];
    unsigned ifindex = if_nametoindex(ifname);
    if (ifindex == 0)
        sl_die(ifname);
    int nports = argc - 2;
    __u16 ports[nports > 0 ? nports : 1];
    for (int i = 0; i < nports; i++) {
        if (!parse_port(argv[i + 2], &ports[i])) {
            fprintf(stderr, "bad port: %s\n", argv[i + 2]);
            return 2;
        }
    }
    install_handlers();

    struct bpf_object *obj = bpf_object__open_file(SL_BPF_OBJ, nullptr);
    if (!obj) {
        perror("bpf_object__open_file " SL_BPF_OBJ);
        return 1;
    }
    int err = bpf_object__load(obj);
    if (err) {
        fprintf(stderr, "bpf_object__load: %s (verifier log above)\n", strerror(-err));
        bpf_object__close(obj);
        return 1;
    }
    struct bpf_program *prog = bpf_object__find_program_by_name(obj, "xdp_firewall");
    struct bpf_map *map = bpf_object__find_map_by_name(obj, "blocked_ports");
    if (!prog || !map) {
        fprintf(stderr, "program xdp_firewall / map blocked_ports not found in object\n");
        bpf_object__close(obj);
        return 1;
    }

    // 控制面：把规则写进 map（程序挂载前写好，第一个包就能被过滤）
    for (int i = 0; i < nports; i++) {
        __u64 zero = 0;
        err = bpf_map__update_elem(map, &ports[i], sizeof ports[i], &zero, sizeof zero, BPF_ANY);
        if (err) {
            fprintf(stderr, "map update port %u: %s\n", ports[i], strerror(-err));
            bpf_object__close(obj);
            return 1;
        }
        printf("blocking udp port %u\n", ports[i]);
    }

    const char *mode;
    LIBBPF_OPTS(bpf_link_create_opts, lopts, .flags = xdp_mode_flags(&mode));
    int link_fd = bpf_link_create(bpf_program__fd(prog), (int)ifindex, BPF_XDP, &lopts);
    if (link_fd < 0) {
        fprintf(stderr, "attach XDP to %s (%s): %s\n", ifname, mode, strerror(errno));
        bpf_object__close(obj);
        return 1;
    }
    printf("attached xdp_firewall to %s (%s mode)\n", ifname, mode);
    printf("ready\n");

    while (!stop_flag) { // 100ms 轮询标志（pause() 在检查与睡眠之间收到信号会永远睡下去）
        struct timespec ts = {.tv_nsec = 100 * 1000 * 1000};
        nanosleep(&ts, nullptr);
    }

    close(link_fd);
    printf("detached from %s\n", ifname);

    int rc = 0;
    unsigned long long total = 0;
    for (int i = 0; i < nports; i++) {
        __u64 n = 0;
        err = bpf_map__lookup_elem(map, &ports[i], sizeof ports[i], &n, sizeof n, 0);
        if (err) {
            fprintf(stderr, "map lookup port %u: %s\n", ports[i], strerror(-err));
            rc = 1;
            continue;
        }
        printf("port %u dropped %llu\n", ports[i], (unsigned long long)n);
        total += n;
    }
    printf("total dropped %llu\n", total);
    bpf_object__close(obj);
    return rc;
}
#endif
