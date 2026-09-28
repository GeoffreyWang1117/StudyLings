// EXERCISE: thr4_once_tls — pthread_once 惰性初始化 + thread_local 线程私有数据
// TOPIC: 一次性初始化、线程局部存储
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §12.6（线程特定数据）、§12.5 pthread_once；C23 thread_local
//
// 说明：
//   用法：thr4_once_tls
//   8 个"请求处理线程"同时启动（用 barrier 让它们尽量同一时刻冲进来），每个线程：
//     1. 设置自己的请求 id：set_request_id(100 + 线程号)
//     2. 计算字符串 "request-<线程号>" 的 CRC-32 —— CRC 查找表很大，惰性构建：第一次用到时才建，且只能建一次
//     3. 调用 handle()，它通过 current_request_id() 读"当前请求 id"，并设置 errno 风格的 g_last_error
//   输出：
//     thread <t> req=<id> crc=<8 位十六进制> last_error=<e>     （每个线程一行）
//     init_count=<CRC 表被构建的次数>
//
//   起步代码的两个问题：
//   - "if (!initialized) { build(); initialized = true; }" 在多线程下既是数据竞争，又可能构建多次，
//     甚至让别的线程看到"initialized = true 但表还没填完"。用 pthread_once 解决（C11 也有 call_once）。
//   - 请求 id 和 last_error 是普通全局变量，8 个线程互相覆盖。每个线程需要自己的一份：
//     C23 的 thread_local（APUE 里的 pthread_key_create/pthread_getspecific 是它的"手动版"）。
//     errno 本身就是这样实现的：glibc 里 errno 是一个 thread_local 变量。
//
//   测试：检查 init_count=1、每个线程的 req/crc/last_error 都是它自己的，且 TSan 无报告（退出码 0）。
//
//   现代意义：日志库的"当前 trace id"、OpenSSL 的 per-thread error queue、Go/tokio 的 task-local、
//   单例/全局配置的惰性加载（Rust 的 std::sync::OnceLock、Go 的 sync.Once）都是这两个机制。

#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { NTHREADS = 8 };

// ---------- 惰性构建的 CRC-32 查找表 ----------
static uint32_t g_crc_table[256];
static int g_init_count; // 构建次数，应当恰好为 1

static void build_crc_table(void) {
    g_init_count++;
    for (uint32_t i = 0; i < 256; i++) {
        uint32_t c = i;
        for (int k = 0; k < 8; k++)
            c = (c & 1) ? 0xEDB88320u ^ (c >> 1) : c >> 1;
        g_crc_table[i] = c;
    }
}

static pthread_once_t g_crc_once = PTHREAD_ONCE_INIT;

static void ensure_crc_table(void) {
    int rc = pthread_once(&g_crc_once, build_crc_table);
    if (rc != 0) {
        fprintf(stderr, "pthread_once: %s\n", strerror(rc));
        exit(1);
    }
}

static uint32_t crc32_str(const char *s) {
    ensure_crc_table();
    uint32_t c = 0xFFFFFFFFu;
    for (; *s; s++)
        c = g_crc_table[(c ^ (uint8_t)*s) & 0xFF] ^ (c >> 8);
    return c ^ 0xFFFFFFFFu;
}

// ---------- 每线程的"当前请求" ----------
static thread_local int g_request_id;
static thread_local int g_last_error;

static void set_request_id(int id) { g_request_id = id; }
static int current_request_id(void) { return g_request_id; }

// 模拟一个处理函数：像系统调用设置 errno 一样设置 g_last_error
static void handle(void) { g_last_error = current_request_id() % 7; }

// ---------- 脚手架 ----------
static pthread_barrier_t g_barrier;

struct result {
    int req;
    uint32_t crc;
    int last_error;
};

static struct result g_results[NTHREADS];

static void *worker(void *arg) {
    int t = (int)(intptr_t)arg;
    set_request_id(100 + t);
    pthread_barrier_wait(&g_barrier); // 所有线程都设置完 id，再同时去用 CRC 表

    char name[32];
    snprintf(name, sizeof name, "request-%d", t);
    uint32_t crc = crc32_str(name);
    handle();

    pthread_barrier_wait(&g_barrier); // 所有线程都 handle 完，再读回"自己的"值
    g_results[t] = (struct result){
        .req = current_request_id(), .crc = crc, .last_error = g_last_error};
    return nullptr;
}

int main(void) {
    int rc = pthread_barrier_init(&g_barrier, nullptr, NTHREADS);
    if (rc != 0) {
        fprintf(stderr, "pthread_barrier_init: %s\n", strerror(rc));
        return 1;
    }
    pthread_t tids[NTHREADS];
    for (int t = 0; t < NTHREADS; t++) {
        rc = pthread_create(&tids[t], nullptr, worker, (void *)(intptr_t)t);
        if (rc != 0) {
            fprintf(stderr, "pthread_create: %s\n", strerror(rc));
            return 1;
        }
    }
    for (int t = 0; t < NTHREADS; t++) {
        rc = pthread_join(tids[t], nullptr);
        if (rc != 0) {
            fprintf(stderr, "pthread_join: %s\n", strerror(rc));
            return 1;
        }
    }
    pthread_barrier_destroy(&g_barrier);

    for (int t = 0; t < NTHREADS; t++)
        printf("thread %d req=%d crc=%08x last_error=%d\n", t, g_results[t].req,
               (unsigned)g_results[t].crc, g_results[t].last_error);
    printf("init_count=%d\n", g_init_count);
    return 0;
}
