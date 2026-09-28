// EXERCISE: bpf4_tc_egress_stats — tc clsact egress 上的 BPF 程序：按目的 IPv4 统计出站流量
// TOPIC: SEC("tc") / struct __sk_buff / TC_ACT_OK·TC_ACT_SHOT / clsact / bpf_tc_hook_create·bpf_tc_attach / HASH map 遍历
// DIFFICULTY: ★★★☆☆
// BOOK: man 8 tc-bpf；man 8 tc（clsact）；man 7 bpf-helpers；libbpf API docs（bpf_tc_*）
// I AM NOT DONE
//
// 说明：
//   用法：bpf4_tc_egress_stats IFACE SECONDS     （需要 root；SECONDS=0 表示跑到 Ctrl-C / SIGTERM）
//   XDP 只能看到**收**方向的包；要看**发**出去的包，就挂到 tc 的 clsact qdisc 的 egress 钩子上
//   （direct-action 模式的 cls_bpf 分类器，libbpf 里写 SEC("tc")）。程序拿到的是 struct __sk_buff，
//   skb->len 是整帧长度（egress 时含以太网头）。对每个 IPv4 包，以**目的地址**（ip->daddr，
//   网络序 __u32）为 key，在 HASH map "egress_bytes" 里累加 bytes/packets，然后返回 TC_ACT_OK 放行。
//   返回值很关键：TC_ACT_OK 放行、TC_ACT_SHOT 丢弃、TC_ACT_REDIRECT 转发（bpf_redirect）……
//   loader：bpf_tc_hook_create（建 clsact qdisc；已存在返回 -EEXIST，此时不是我们建的，退出时也不删）
//   → bpf_tc_attach（handle=1, priority=1）→ 打印 "ready" → 到时或 SIGINT/SIGTERM →
//   bpf_tc_detach（+ 若 qdisc 是自己建的就 bpf_tc_hook_destroy）→ 打印 "detached" →
//   用 bpf_map_get_next_key 遍历 map，按字节数降序打印 "top talkers:" 和每行
//   "10.0.0.2 bytes=N packets=M"。
//   注意：tc 过滤器不像 bpf_link 那样随进程退出自动卸载（进程被 SIGKILL 会残留，需要
//   `tc filter del dev IFACE egress` 或 `tc qdisc del dev IFACE clsact`）；6.6+ 内核的 tcx
//   （bpf_program__attach_tcx）改成了 link 语义。
//   扩展：同一个钩子里还能改写包 —— 设 skb->mark 给 iptables/路由策略用、设 skb->priority 选
//   mq/prio 的队列、bpf_skb_store_bytes 改 DSCP，Cilium 的带宽管理器（EDT）就是在 egress 设 skb->tstamp。
//   探针（root + netns/veth）：对端 namespace 在同一条 veth 上有两个地址 .2 和 .3，本端向 .2 发 300 个、
//   向 .3 发 100 个 1000 字节的 UDP 包，检查排名（.2 在前）和字节/包数精确相等；包必须真的发出去
//   （对端能收到）；退出后 IFACE 上不能残留 bpf 过滤器。
//   真实机器（可选）：NETLINGS_IFACE + NETLINGS_PEER_IP 时，向对端发 UDP 并检查对端地址的计数。
//
//   这些东西用在哪：Cilium 的数据面主体就是挂在 tc ingress/egress（新内核是 tcx）上的 BPF 程序，
//   做 Pod 间策略、NAT、负载均衡；Pixie/Parca 等可观测工具在这里做按连接的流量统计；
//   Android 用 tc BPF 统计每个 App 的流量（netd）。

#include <linux/types.h>

struct talker {
    __u64 bytes;
    __u64 packets;
};

#ifdef __BPF__
// ============================== 内核侧：tc 程序 ==============================
#include <linux/bpf.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/pkt_cls.h>

#include <bpf/bpf_endian.h>
#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 4096);
    __type(key, __u32); // 目的 IPv4 地址，网络序
    __type(value, struct talker);
} egress_bytes SEC(".maps");

SEC("tc")
int tc_egress(struct __sk_buff *skb) {
    void *data = (void *)(long)skb->data;
    void *data_end = (void *)(long)skb->data_end;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end || eth->h_proto != bpf_htons(ETH_P_IP))
        return TC_ACT_OK;
    struct iphdr *ip = (void *)(eth + 1);
    if ((void *)(ip + 1) > data_end)
        return TC_ACT_OK;

    // BUG: 题目要求按目的地址统计
    __u32 key = ip->saddr;
    struct talker *t = bpf_map_lookup_elem(&egress_bytes, &key);
    if (t) {
        __sync_fetch_and_add(&t->bytes, skb->len);
        __sync_fetch_and_add(&t->packets, 1);
    } else {
        struct talker init = {.bytes = skb->len, .packets = 1};
        // 两个 CPU 同时第一次见到这个地址：只有一个 NOEXIST 插入成功，另一个退回原子加
        if (bpf_map_update_elem(&egress_bytes, &key, &init, BPF_NOEXIST) != 0) {
            t = bpf_map_lookup_elem(&egress_bytes, &key);
            if (t) {
                __sync_fetch_and_add(&t->bytes, skb->len);
                __sync_fetch_and_add(&t->packets, 1);
            }
        }
    }
    // TODO: 选对返回值 —— 本程序只统计、不拦截（看 linux/pkt_cls.h 里的 TC_ACT_*）
    return TC_ACT_SHOT;
}

char LICENSE[] SEC("license") = "GPL";

#else
// ============================== 用户态：loader ==============================
#include <arpa/inet.h>
#include <errno.h>
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

static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

static void wait_until_done(int seconds) {
    double deadline = now_s() + seconds;
    while (!stop_flag && (seconds == 0 || now_s() < deadline)) {
        struct timespec ts = {.tv_nsec = 100 * 1000 * 1000};
        nanosleep(&ts, nullptr);
    }
}

struct row {
    __u32 addr;
    struct talker t;
};

static int by_bytes_desc(const void *a, const void *b) {
    const struct row *x = a, *y = b;
    return (x->t.bytes < y->t.bytes) - (x->t.bytes > y->t.bytes);
}

static int print_top_talkers(int map_fd) {
    size_t cap = 16, n = 0;
    struct row *rows = malloc(cap * sizeof *rows);
    if (!rows)
        return -ENOMEM;
    __u32 key, next;
    __u32 *prev = nullptr; // nullptr → 取第一个 key
    while (bpf_map_get_next_key(map_fd, prev, &next) == 0) {
        if (n == cap) {
            struct row *bigger = realloc(rows, 2 * cap * sizeof *rows);
            if (!bigger) {
                free(rows);
                return -ENOMEM;
            }
            rows = bigger;
            cap *= 2;
        }
        if (bpf_map_lookup_elem(map_fd, &next, &rows[n].t) == 0) {
            rows[n].addr = next;
            n++;
        }
        key = next;
        prev = &key;
    }
    qsort(rows, n, sizeof *rows, by_bytes_desc);
    printf("top talkers:\n");
    for (size_t i = 0; i < n; i++) {
        char buf[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &rows[i].addr, buf, sizeof buf);
        printf("%s bytes=%llu packets=%llu\n", buf, (unsigned long long)rows[i].t.bytes,
               (unsigned long long)rows[i].t.packets);
    }
    free(rows);
    return 0;
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
        fprintf(stderr, "bpf_object__load: %s (verifier log above)\n", strerror(-err));
        bpf_object__close(obj);
        return 1;
    }
    struct bpf_program *prog = bpf_object__find_program_by_name(obj, "tc_egress");
    struct bpf_map *map = bpf_object__find_map_by_name(obj, "egress_bytes");
    if (!prog || !map) {
        fprintf(stderr, "program tc_egress / map egress_bytes not found\n");
        bpf_object__close(obj);
        return 1;
    }

    LIBBPF_OPTS(bpf_tc_hook, hook, .ifindex = (int)ifindex, .attach_point = BPF_TC_EGRESS);
    err = bpf_tc_hook_create(&hook); // = tc qdisc add dev IFACE clsact
    bool created_qdisc = err == 0;
    if (err && err != -EEXIST) {
        fprintf(stderr, "bpf_tc_hook_create: %s\n", strerror(-err));
        bpf_object__close(obj);
        return 1;
    }
    // = tc filter add dev IFACE egress prio 1 handle 1 bpf direct-action obj ...
    LIBBPF_OPTS(bpf_tc_opts, topts, .handle = 1, .priority = 1, .prog_fd = bpf_program__fd(prog));
    err = bpf_tc_attach(&hook, &topts);
    if (err) {
        fprintf(stderr, "bpf_tc_attach: %s\n", strerror(-err));
        if (created_qdisc) {
            hook.attach_point = BPF_TC_INGRESS | BPF_TC_EGRESS;
            bpf_tc_hook_destroy(&hook);
        }
        bpf_object__close(obj);
        return 1;
    }
    printf("attached tc_egress to %s egress (prog id %u)\n", ifname, topts.prog_id);
    printf("ready\n");

    wait_until_done(seconds);

    int rc = 0;
    // bpf_tc_detach 要求 prog_fd/prog_id/flags 为 0，只按 handle+priority 定位
    topts.flags = topts.prog_fd = topts.prog_id = 0;
    err = bpf_tc_detach(&hook, &topts);
    if (err) {
        fprintf(stderr, "bpf_tc_detach: %s\n", strerror(-err));
        rc = 1;
    }
    if (created_qdisc) {
        hook.attach_point = BPF_TC_INGRESS | BPF_TC_EGRESS; // 两个方向都给 → 删除整个 clsact
        err = bpf_tc_hook_destroy(&hook);
        if (err) {
            fprintf(stderr, "bpf_tc_hook_destroy: %s\n", strerror(-err));
            rc = 1;
        }
    }
    printf("detached from %s\n", ifname);

    err = print_top_talkers(bpf_map__fd(map));
    if (err) {
        fprintf(stderr, "reading map: %s\n", strerror(-err));
        rc = 1;
    }
    bpf_object__close(obj);
    return rc;
}
#endif
