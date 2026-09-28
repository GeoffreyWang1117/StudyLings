// EXERCISE: bpf1_xdp_count — XDP 按 L4 协议统计包数/字节数（PERCPU_ARRAY + 验证器边界检查）
// TOPIC: XDP / struct xdp_md / data·data_end 边界检查 / BPF_MAP_TYPE_PERCPU_ARRAY / libbpf 加载与挂载
// DIFFICULTY: ★★★☆☆
// BOOK: man 7 bpf-helpers；kernel Documentation/bpf/verifier.rst、Documentation/networking/xdp-*；libbpf API docs
// I AM NOT DONE
//
// 说明：
//   用法：bpf1_xdp_count IFACE SECONDS      （需要 root；SECONDS=0 表示一直跑到 Ctrl-C / SIGTERM）
//   本文件同时包含两部分，会被编译两次：
//     * #ifdef __BPF__ 分支：clang -target bpf 编译成 bin/bpf1_xdp_count.bpf.o，运行在内核里；
//     * #else 分支：gcc 编译的用户态 loader，用 libbpf 打开 SL_BPF_OBJ、加载（此时内核验证器检查程序）、
//       挂到 IFACE 的 XDP 钩子上。
//   XDP 程序在网卡驱动收包的最早时刻运行（还没分配 sk_buff），这里对每个包：
//     Ethernet → 若是 IPv4 → 看 ip->protocol，归到 TCP / UDP / ICMP / OTHER 四类之一，
//     在 PERCPU_ARRAY map "stats" 的对应槽里 packets++、bytes += 帧长，然后 XDP_PASS（放行）。
//   PERCPU map：每个 CPU 各有一份 value，内核侧无需原子操作；用户态 lookup 一次拿回 ncpu 份，
//   要自己加起来（libbpf_num_possible_cpus()）。
//   验证器（verifier）的经典一课：读包内容之前必须证明 "指针 + 长度 <= data_end"，
//   否则加载时就被拒绝（invalid access to packet），libbpf 会把验证器日志打印到 stderr。
//   输出：挂载后打印 "attached ..." 和 "ready"；到时间或收到 SIGINT/SIGTERM 后先卸载（关闭 bpf_link
//   即 detach），打印 "detached"，再打印四行 "TCP packets=N bytes=M" ……，exit 0。
//   环境变量 NETLINGS_XDP_MODE：skb（默认，generic XDP，任何网卡/veth 都能用）| drv（native，
//   驱动内执行，mlx5/ice/i40e 等支持，Mpps 级性能）| auto（让内核挑）。
//   探针（root + netns/veth）：对端 namespace 发 N 个 ping、M 个 UDP 包、K 个 TCP SYN（分散在各个 CPU
//   上发），检查 ICMP/UDP/TCP 计数与字节数精确相等；退出后网卡上不能残留 XDP 程序。
//   真实机器（可选）：设 NETLINGS_IFACE=<ConnectX 网卡> NETLINGS_PEER_IP=<对端 IP>，探针会以 drv 模式
//   挂到真网卡上 ping 对端，检查 ICMP 计数。
//
//   这些东西用在哪：Cloudflare 的 DDoS 防护（L4Drop）和 Meta 的 Katran L4 负载均衡都是 XDP 程序，
//   在驱动层每核处理上千万包/秒；Cilium 用 XDP 做 NodePort/LB 加速和预过滤；
//   Pixie、Parca、bpftrace 等可观测工具也是同一套 "BPF 程序 + map + 用户态 loader" 模式。

#include <linux/types.h>

// 内核与用户态共享的定义
enum { P_TCP, P_UDP, P_ICMP, P_OTHER, P_MAX };

struct counters {
    __u64 packets;
    __u64 bytes;
};

#ifdef __BPF__
// ============================== 内核侧：XDP 程序 ==============================
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/in.h>
#include <linux/ip.h>

#include <bpf/bpf_endian.h>
#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_PERCPU_ARRAY);
    __uint(max_entries, P_MAX);
    __type(key, __u32);
    __type(value, struct counters);
} stats SEC(".maps");

static __always_inline __u32 classify(void *data, void *data_end) {
    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end) // 帧比以太网头还短
        return P_OTHER;
    if (eth->h_proto != bpf_htons(ETH_P_IP))
        return P_OTHER;

    struct iphdr *ip = (void *)(eth + 1);
    // BUG: 直接读 ip->protocol —— 验证器无法证明这个 IP 头完整地落在包内，会拒绝加载。
    // TODO: 仿照上面以太网头的写法，读 ip 字段之前先检查 (void *)(ip + 1) 与 data_end

    switch (ip->protocol) {
    case IPPROTO_TCP:
        return P_TCP;
    case IPPROTO_UDP:
        return P_UDP;
    case IPPROTO_ICMP:
        return P_ICMP;
    default:
        return P_OTHER;
    }
}

SEC("xdp")
int xdp_count(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;

    __u32 key = classify(data, data_end);
    struct counters *c = bpf_map_lookup_elem(&stats, &key);
    if (c) { // 验证器要求判空，即使 ARRAY 的 key 一定在范围内
        c->packets++;
        c->bytes += (__u64)(data_end - data);
    }
    return XDP_PASS;
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

static const char *const proto_names[P_MAX] = {"TCP", "UDP", "ICMP", "OTHER"};

static volatile sig_atomic_t stop_flag;

static void on_signal(int sig) { stop_flag = sig; }

static void install_handlers(void) {
    struct sigaction sa = {.sa_handler = on_signal}; // 不设 SA_RESTART：让 nanosleep 被打断
    sigemptyset(&sa.sa_mask);
    if (sigaction(SIGINT, &sa, nullptr) < 0 || sigaction(SIGTERM, &sa, nullptr) < 0)
        sl_die("sigaction");
}

static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

// 睡到 seconds 秒过去（0 = 永远）或收到信号
static void wait_until_done(int seconds) {
    double deadline = now_s() + seconds;
    while (!stop_flag && (seconds == 0 || now_s() < deadline)) {
        struct timespec ts = {.tv_nsec = 100 * 1000 * 1000};
        nanosleep(&ts, nullptr);
    }
}

// NETLINGS_XDP_MODE → XDP_FLAGS_*（skb = generic，drv = native，auto = 让内核选）
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

// 读出 key 对应的 ncpu 份 value，加总到 *out
static int read_total(struct bpf_map *map, __u32 key, int ncpu, struct counters *out) {
    struct counters *vals = calloc((size_t)ncpu, sizeof *vals);
    if (!vals)
        return -ENOMEM;
    int err = bpf_map__lookup_elem(map, &key, sizeof key, vals, sizeof *vals * (size_t)ncpu, 0);
    if (err == 0) {
        // TODO: PERCPU map 返回 ncpu 份 value（每个 CPU 一份），要把它们全部加起来。
        //       现在只取了 CPU 0 的那一份。
        *out = vals[0];
    }
    free(vals);
    return err;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 3) {
        fprintf(stderr, "usage: %s IFACE SECONDS\n", argv[0]);
        return 2;
    }
    const char *ifname = argv[1];
    int seconds = atoi(argv[2]);
    unsigned ifindex = if_nametoindex(ifname);
    if (ifindex == 0)
        sl_die(ifname);
    install_handlers();

    struct bpf_object *obj = bpf_object__open_file(SL_BPF_OBJ, nullptr);
    if (!obj) {
        perror("bpf_object__open_file " SL_BPF_OBJ);
        return 1;
    }
    int err = bpf_object__load(obj);
    if (err) {
        fprintf(stderr,
                "bpf_object__load: %s\n"
                "hint: 内核验证器拒绝了程序，看上面 libbpf 打印的 verifier log（最后几行）："
                "\"invalid access to packet\" 说明读包之前缺少与 data_end 的边界检查\n",
                strerror(-err));
        bpf_object__close(obj);
        return 1;
    }
    struct bpf_program *prog = bpf_object__find_program_by_name(obj, "xdp_count");
    struct bpf_map *map = bpf_object__find_map_by_name(obj, "stats");
    if (!prog || !map) {
        fprintf(stderr, "program xdp_count / map stats not found in object\n");
        bpf_object__close(obj);
        return 1;
    }

    // bpf_link 方式挂载：link fd 关闭（包括进程被杀）时内核自动卸载，不会残留在网卡上。
    // bpf_program__attach_xdp(prog, ifindex) 也创建 link，但不能指定模式；这里用底层
    // bpf_link_create 以便传 XDP_FLAGS_SKB_MODE / XDP_FLAGS_DRV_MODE。
    const char *mode;
    LIBBPF_OPTS(bpf_link_create_opts, lopts, .flags = xdp_mode_flags(&mode));
    int link_fd = bpf_link_create(bpf_program__fd(prog), (int)ifindex, BPF_XDP, &lopts);
    if (link_fd < 0) {
        fprintf(stderr, "attach XDP to %s (%s): %s\n", ifname, mode, strerror(errno));
        bpf_object__close(obj);
        return 1;
    }
    printf("attached xdp_count to %s (%s mode)\n", ifname, mode);
    printf("ready\n");

    wait_until_done(seconds);

    close(link_fd); // detach
    printf("detached from %s\n", ifname);

    int ncpu = libbpf_num_possible_cpus();
    int rc = 0;
    if (ncpu <= 0) {
        fprintf(stderr, "libbpf_num_possible_cpus: %s\n", strerror(-ncpu));
        rc = 1;
    }
    for (__u32 k = 0; rc == 0 && k < P_MAX; k++) {
        struct counters total;
        err = read_total(map, k, ncpu, &total);
        if (err) {
            fprintf(stderr, "lookup %s: %s\n", proto_names[k], strerror(-err));
            rc = 1;
            break;
        }
        printf("%-5s packets=%llu bytes=%llu\n", proto_names[k], (unsigned long long)total.packets,
               (unsigned long long)total.bytes);
    }
    bpf_object__close(obj);
    return rc;
}
#endif
