// EXERCISE: bpf3_tcp_state_trace — 用 tracepoint + ringbuf 追踪 TCP 状态机
// TOPIC: tracepoint sock/inet_sock_set_state / 手写 tracepoint 上下文结构 / BPF_MAP_TYPE_RINGBUF / const volatile 配置
// DIFFICULTY: ★★★☆☆
// BOOK: UNP §2.6（TCP 状态转换图）；kernel include/trace/events/sock.h；Documentation/bpf/ringbuf.rst；libbpf API docs
//
// 说明：
//   用法：bpf3_tcp_state_trace PORT SECONDS     （需要 root；SECONDS=0 表示跑到 Ctrl-C / SIGTERM）
//   内核每次改变一个 TCP socket 的状态都会触发 tracepoint sock/inet_sock_set_state。
//   BPF 程序挂在上面：只关心 AF_INET + IPPROTO_TCP、且本端或对端端口等于 PORT 的事件，
//   把 (旧状态, 新状态, saddr:sport, daddr:dport) 写进 BPF ringbuf；loader 用 ring_buffer__poll
//   取出来，每个事件打印一行：
//       127.0.0.1:43512 -> 127.0.0.1:PORT SYN_SENT -> ESTABLISHED
//   启动时打印 "tracing tcp port PORT" 和 "ready"；到时或收到 SIGINT/SIGTERM 时 detach 并退出 0。
//
//   tracepoint 的参数怎么知道？读 /sys/kernel/tracing/events/sock/inet_sock_set_state/format：
//   前 8 字节是所有 tracepoint 共有的 common_* 字段，后面依次是 skaddr、oldstate、newstate、
//   sport、dport、family、protocol、saddr[4]、daddr[4]、saddr_v6[16]、daddr_v6[16]。
//   本题照着这个 format 手写 struct（用 static_assert 钉住偏移量）。注意 format 里的 sport/dport
//   已经是**主机字节序**（内核在 TP_fast_assign 里做了 ntohs），saddr/daddr 是网络序的 4 个字节。
//   更现代的写法是 CO-RE：`bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h`，
//   然后用内核自带的 `struct trace_event_raw_inet_sock_set_state`，或者挂 SEC("tp_btf/...")/fentry，
//   配合 BPF_CORE_READ 在不同内核版本间自动重定位字段 —— bcc 的 tcpstates、bpftrace 的
//   `tracepoint:sock:inet_sock_set_state { ... }` 做的就是同一件事。
//   要追踪的端口通过 `const volatile __u16 target_port` 传进去：它在 .rodata 里，loader 在
//   bpf_object__load 之前改好初值，加载后对验证器是常量（libbpf skeleton 的 skel->rodata->x 就是这个机制）。
//   探针（root）：若 tracefs 没挂载会先 mount（失败则 skip）；启动追踪器，在 127.0.0.1:PORT 上 listen、
//   connect、accept、客户端先 close、服务端再 close，检查输出里有这些关键转换且地址端口正确：
//     CLOSE -> LISTEN；客户端 CLOSE -> SYN_SENT、SYN_SENT -> ESTABLISHED、ESTABLISHED -> FIN_WAIT1、
//     FIN_WAIT1 -> FIN_WAIT2；服务端 SYN_RECV -> ESTABLISHED、ESTABLISHED -> CLOSE_WAIT、
//     CLOSE_WAIT -> LAST_ACK、LAST_ACK -> CLOSE。
//
//   这些东西用在哪：Pixie、Parca、Cilium Hubble、Datadog/New Relic 的 eBPF agent 用同类 tracepoint/kprobe
//   无侵入地统计连接生命周期、重传与延迟；bpftrace 一行就能写出本题；ringbuf（5.8+）取代了
//   perf buffer，是内核 → 用户态事件流的标准通道（多 CPU 共享一个缓冲区、保序、可 reserve/commit 零拷贝）。

#include <linux/types.h>

// 内核 → 用户态的事件
struct event {
    __u8 saddr[4]; // 网络序
    __u8 daddr[4];
    __u16 sport; // 主机序
    __u16 dport;
    __s32 oldstate;
    __s32 newstate;
};

#ifdef __BPF__
// ============================== 内核侧：tracepoint 程序 ==============================
#include <linux/bpf.h>
#include <linux/in.h>

#include <bpf/bpf_endian.h>
#include <bpf/bpf_helpers.h>

// 照 /sys/kernel/tracing/events/sock/inet_sock_set_state/format 手写
struct inet_sock_set_state_args {
    __u64 common; // common_type(2) common_flags(1) common_preempt_count(1) common_pid(4)
    const void *skaddr;
    int oldstate;
    int newstate;
    __u16 sport;
    __u16 dport;
    __u16 family;
    __u16 protocol;
    __u8 saddr[4];
    __u8 daddr[4];
    __u8 saddr_v6[16];
    __u8 daddr_v6[16];
};
_Static_assert(__builtin_offsetof(struct inet_sock_set_state_args, oldstate) == 16, "format: oldstate");
_Static_assert(__builtin_offsetof(struct inet_sock_set_state_args, sport) == 24, "format: sport");
_Static_assert(__builtin_offsetof(struct inet_sock_set_state_args, saddr) == 32, "format: saddr");
_Static_assert(__builtin_offsetof(struct inet_sock_set_state_args, daddr_v6) == 56, "format: daddr_v6");

#define SL_AF_INET 2

const volatile __u16 target_port = 0; // loader 在加载前写入（主机序）

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024);
} events SEC(".maps");

SEC("tracepoint/sock/inet_sock_set_state")
int trace_tcp_state(struct inet_sock_set_state_args *ctx) {
    if (ctx->family != SL_AF_INET || ctx->protocol != IPPROTO_TCP)
        return 0;
    // tracepoint 里的端口已是主机序，直接与主机序的 target_port 比较
    if (ctx->sport != target_port && ctx->dport != target_port)
        return 0;

    struct event *e = bpf_ringbuf_reserve(&events, sizeof *e, 0);
    if (!e) // ringbuf 满了：丢弃这个事件
        return 0;
    __builtin_memcpy(e->saddr, ctx->saddr, 4);
    __builtin_memcpy(e->daddr, ctx->daddr, 4);
    e->sport = ctx->sport;
    e->dport = ctx->dport;
    e->oldstate = ctx->oldstate;
    e->newstate = ctx->newstate;
    bpf_ringbuf_submit(e, 0);
    return 0;
}

char LICENSE[] SEC("license") = "GPL";

#else
// ============================== 用户态：loader ==============================
#include <arpa/inet.h>
#include <errno.h>
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

// include/net/tcp_states.h 的编号
static const char *state_name(int s) {
    static const char *const names[] = {
        [1] = "ESTABLISHED", [2] = "SYN_SENT",   [3] = "SYN_RECV",  [4] = "FIN_WAIT1",
        [5] = "FIN_WAIT2",   [6] = "TIME_WAIT",  [7] = "CLOSE",     [8] = "CLOSE_WAIT",
        [9] = "LAST_ACK",    [10] = "LISTEN",    [11] = "CLOSING",  [12] = "NEW_SYN_RECV",
    };
    if (s > 0 && s < (int)(sizeof names / sizeof names[0]) && names[s])
        return names[s];
    return "UNKNOWN";
}

static int on_event(void *ctx, void *data, size_t len) {
    if (len < sizeof(struct event))
        return 0;
    const struct event *e = data;
    char src[INET_ADDRSTRLEN], dst[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, e->saddr, src, sizeof src);
    inet_ntop(AF_INET, e->daddr, dst, sizeof dst);
    printf("%s:%u -> %s:%u %s -> %s\n", src, e->sport, dst, e->dport, state_name(e->oldstate),
           state_name(e->newstate));
    return 0;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 3) {
        fprintf(stderr, "usage: %s PORT SECONDS\n", argv[0]);
        return 2;
    }
    int port = atoi(argv[1]);
    int seconds = atoi(argv[2]);
    if (port < 1 || port > 65535) {
        fprintf(stderr, "bad port: %s\n", argv[1]);
        return 2;
    }
    install_handlers();

    struct bpf_object *obj = bpf_object__open_file(SL_BPF_OBJ, nullptr);
    if (!obj) {
        perror("bpf_object__open_file " SL_BPF_OBJ);
        return 1;
    }
    int rc = 1;
    struct bpf_link *link = nullptr;
    struct ring_buffer *rb = nullptr;

    // 加载前改 .rodata 里的 target_port（libbpf 把 .rodata 段做成一个 map，名字可用 ".rodata" 查找）
    struct bpf_map *rodata = bpf_object__find_map_by_name(obj, ".rodata");
    size_t rosz = 0;
    __u16 *cfg = rodata ? bpf_map__initial_value(rodata, &rosz) : nullptr;
    if (!cfg || rosz < sizeof *cfg) {
        fprintf(stderr, ".rodata (target_port) not found in object\n");
        goto out;
    }
    *cfg = (__u16)port; // .rodata 里只有 target_port 一个变量，偏移 0

    int err = bpf_object__load(obj);
    if (err) {
        fprintf(stderr, "bpf_object__load: %s (verifier log above)\n", strerror(-err));
        goto out;
    }
    struct bpf_program *prog = bpf_object__find_program_by_name(obj, "trace_tcp_state");
    struct bpf_map *events = bpf_object__find_map_by_name(obj, "events");
    if (!prog || !events) {
        fprintf(stderr, "program trace_tcp_state / map events not found\n");
        goto out;
    }
    link = bpf_program__attach_tracepoint(prog, "sock", "inet_sock_set_state");
    if (!link) {
        fprintf(stderr,
                "attach tracepoint sock/inet_sock_set_state: %s\n"
                "hint: 需要 tracefs：mount -t tracefs tracefs /sys/kernel/tracing\n",
                strerror(errno));
        goto out;
    }
    rb = ring_buffer__new(bpf_map__fd(events), on_event, nullptr, nullptr);
    if (!rb) {
        fprintf(stderr, "ring_buffer__new: %s\n", strerror(errno));
        goto out;
    }
    printf("tracing tcp port %d\n", port);
    printf("ready\n");

    double deadline = now_s() + seconds;
    while (!stop_flag && (seconds == 0 || now_s() < deadline)) {
        int n = ring_buffer__poll(rb, 100 /* ms */);
        if (n < 0 && n != -EINTR) {
            fprintf(stderr, "ring_buffer__poll: %s\n", strerror(-n));
            goto out;
        }
    }
    ring_buffer__consume(rb); // 退出前把剩下的事件取完
    rc = 0;
out:
    ring_buffer__free(rb);
    bpf_link__destroy(link); // detach
    bpf_object__close(obj);
    if (rc == 0)
        printf("detached\n");
    return rc;
}
#endif
