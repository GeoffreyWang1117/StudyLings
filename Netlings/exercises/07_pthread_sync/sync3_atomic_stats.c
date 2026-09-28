// EXERCISE: sync3_atomic_stats — 无锁统计计数器 + release/acquire 发布配置指针
// TOPIC: <stdatomic.h> / atomic_fetch_add(relaxed) / 指针发布(release-acquire) / happens-before
// DIFFICULTY: ★★★☆☆
// BOOK: C11 §7.17（stdatomic.h）；man 3 stdatomic.h；APUE §11.6（为什么需要同步）
// I AM NOT DONE
//
// 说明：
//   用法：sync3_atomic_stats THREADS REQUESTS
//   模拟服务器的统计模块：
//   1. 主线程先启动 THREADS 个 worker，然后才构造配置 struct config（直方图桶宽、名字）并**发布**
//      它的指针；worker 自旋等到指针非空，之后读取配置里的字段。
//   2. 每个 worker 处理 REQUESTS 个"请求"：第 i 个请求（线程 t）的字节数 = i % 1000 + 1，
//      延迟 = (i * 7919 + t * 104729) % 5000 µs；更新全局计数 requests、bytes 和
//      延迟直方图 hist[min(延迟 / 桶宽, NBUCKETS-1)]。
//   3. 全部 join 后打印 "requests=<n> bytes=<n> hist=<h0,h1,...> config=<名字>"，数值必须精确。
//
//   两种原子用法：
//   - 统计计数器：只要求"最终总数正确"，不用它同步别的数据 → atomic_fetch_add_explicit(...,
//     memory_order_relaxed)，最便宜（x86 上就是一条 lock xadd）。
//   - 发布指针：worker 看到指针后要读它指向的字段 → 主线程 atomic_store_explicit(release)，
//     worker atomic_load_explicit(acquire)。release 之前的写（填配置字段）对 acquire 之后的读可见。
//     用 relaxed 发布的话，worker 可能看到新指针却读到还没写好的字段（ARM 上真的会发生）；
//     TSan 会把它报告为数据竞争（exit 66）。
//
//   现实中：Prometheus client 的 Counter/Histogram、nginx 的 stub_status 计数器（ngx_atomic_fetch_add）、
//   Envoy stats、Linux 内核的 percpu counter；配置热加载 —— nginx reload 之外，Envoy xDS、
//   HAProxy runtime API 都是"构造新配置 → 原子地替换指针"（RCU 风格），读者永不加锁。

#include <errno.h>
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sl.h"

enum { NBUCKETS = 10 };

struct config {
    unsigned bucket_width_us;
    char name[32];
};

// 统计计数器：多个线程并发累加
// TODO: 普通 unsigned long 的并发 ++ 是数据竞争（读-改-写不是原子的，还会丢计数）。
//       改成 atomic_ulong
static unsigned long g_requests;
static unsigned long g_bytes;
static unsigned long g_hist[NBUCKETS];

// 发布出来的配置指针：nullptr 表示还没准备好
static struct config *_Atomic g_config;

static void record(const struct config *cfg, unsigned long bytes, unsigned latency_us) {
    unsigned b = latency_us / cfg->bucket_width_us;
    if (b >= NBUCKETS)
        b = NBUCKETS - 1;
    // TODO: 改成 atomic_fetch_add_explicit(..., memory_order_relaxed)
    g_requests++;
    g_bytes += bytes;
    g_hist[b]++;
}

// BUG: relaxed 只保证指针本身读写是原子的，不保证"填配置字段"先于"指针可见"。
// TODO: 发布用 memory_order_release，读取用 memory_order_acquire
static void publish_config(struct config *cfg) {
    atomic_store_explicit(&g_config, cfg, memory_order_relaxed);
}

static const struct config *wait_config(void) {
    const struct config *cfg;
    while ((cfg = atomic_load_explicit(&g_config, memory_order_relaxed)) == nullptr)
        sched_yield();
    return cfg;
}

// ---- 脚手架 ----

struct worker_arg {
    unsigned id;
    long requests;
};

static void *worker(void *p) {
    const struct worker_arg *w = p;
    const struct config *cfg = wait_config();
    for (long i = 0; i < w->requests; i++) {
        unsigned long bytes = (unsigned long)(i % 1000) + 1;
        unsigned latency = (unsigned)(((unsigned long)i * 7919u + w->id * 104729u) % 5000u);
        record(cfg, bytes, latency);
    }
    return nullptr;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 3) {
        fprintf(stderr, "usage: %s THREADS REQUESTS\n", argv[0]);
        return 2;
    }
    long nt = strtol(argv[1], nullptr, 10), nreq = strtol(argv[2], nullptr, 10);
    if (nt <= 0 || nt > 128 || nreq < 0) {
        fprintf(stderr, "bad arguments\n");
        return 2;
    }

    pthread_t tids[128];
    struct worker_arg args[128];
    for (long i = 0; i < nt; i++) {
        args[i] = (struct worker_arg){.id = (unsigned)i, .requests = nreq};
        int rc = pthread_create(&tids[i], nullptr, worker, &args[i]);
        if (rc != 0) {
            errno = rc;
            sl_die("pthread_create");
        }
    }

    // worker 已经在跑了，现在才构造配置并发布
    struct config *cfg = malloc(sizeof *cfg);
    if (!cfg)
        sl_die("malloc");
    cfg->bucket_width_us = 500;
    snprintf(cfg->name, sizeof cfg->name, "latency-v%d", 2);
    publish_config(cfg);

    for (long i = 0; i < nt; i++)
        pthread_join(tids[i], nullptr);

    // TODO: 计数器改成原子类型后，这里用 atomic_load 读取
    printf("requests=%lu bytes=%lu hist=", g_requests, g_bytes);
    for (int b = 0; b < NBUCKETS; b++)
        printf("%s%lu", b ? "," : "", g_hist[b]);
    printf(" config=%s\n", cfg->name);
    free(cfg);
    return 0;
}
