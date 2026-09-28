// EXERCISE: thr2_mutex_counter — 用 pthread_mutex 保护共享账户
// TOPIC: 数据竞争、互斥量、最小临界区
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §11.6.1（互斥量）、§11.6.2（避免死锁）；man 3 pthread_mutex_lock
// I AM NOT DONE
//
// 说明：
//   用法：thr2_mutex_counter NTHREADS ITERS
//   4 个账户各有 1000 元。NTHREADS 个线程各做 ITERS 次"转账"：从一个账户转 1 元到另一个账户
//   （余额不足就跳过，但也算一次尝试）。每次尝试都把全局计数 g_attempts 加 1。
//   结束后打印：total=<四个账户余额之和> attempts=<尝试次数> min=<最小余额>
//
//   "balance -= 1" 看起来是一条语句，其实是 load → sub → store 三步；两个线程交错执行就会丢更新，
//   总额不再守恒。本章用 ThreadSanitizer 编译，第一次竞争就会以退出码 66 结束。
//
//   要求：
//   - 用一个 PTHREAD_MUTEX_INITIALIZER 静态初始化的互斥量保护账户和计数器
//   - 临界区尽量小：挑选账户、模拟"风控计算"等不碰共享数据的工作放在锁外面
//
//   测试：多组 NTHREADS/ITERS，检查退出码 0、total=4000、attempts=NTHREADS*ITERS、min>=0。
//
//   现代意义：Redis 6 的 I/O 线程、nginx 的共享内存 slab、数据库连接池计数……凡是共享的可变状态
//   都要么加锁、要么用原子操作、要么干脆不共享（每线程一份，最后合并）。

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { NACCOUNTS = 4, INITIAL = 1000 };

static long g_balance[NACCOUNTS] = {INITIAL, INITIAL, INITIAL, INITIAL};
static long g_attempts;

// TODO: 定义一个静态初始化的互斥量（PTHREAD_MUTEX_INITIALIZER）

// 模拟一些不需要共享数据的"风控计算"——它不该待在锁里
static unsigned risk_score(unsigned seed) {
    unsigned h = seed * 2654435761u;
    for (int k = 0; k < 20; k++)
        h ^= h << 13, h ^= h >> 17, h ^= h << 5;
    return h;
}

// TODO: 用互斥量保护下面对 g_balance / g_attempts 的读-改-写。
//       BUG: 现在完全没加锁，多个线程同时转账会丢更新（TSan 会报 data race）
static void transfer(int from, int to, long amount) {
    if (g_balance[from] >= amount) {
        g_balance[from] -= amount;
        g_balance[to] += amount;
    }
    g_attempts++;
}

struct worker_arg {
    int id;
    long iters;
};

static void *worker(void *arg) {
    const struct worker_arg *w = arg;
    unsigned sink = 0;
    for (long j = 0; j < w->iters; j++) {
        int from = (int)((w->id + j) % NACCOUNTS);
        int to = (from + 1 + (int)(j % (NACCOUNTS - 1))) % NACCOUNTS;
        sink += risk_score((unsigned)j); // 锁外
        transfer(from, to, 1);
    }
    return (void *)(unsigned long)sink;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s NTHREADS ITERS\n", argv[0]);
        return 2;
    }
    int n = atoi(argv[1]);
    long iters = atol(argv[2]);
    if (n < 1 || n > 64 || iters < 0) {
        fprintf(stderr, "thr2_mutex_counter: bad arguments\n");
        return 2;
    }

    pthread_t tids[64];
    struct worker_arg args[64];
    for (int i = 0; i < n; i++) {
        args[i] = (struct worker_arg){.id = i, .iters = iters};
        int rc = pthread_create(&tids[i], nullptr, worker, &args[i]);
        if (rc != 0) {
            fprintf(stderr, "pthread_create: %s\n", strerror(rc));
            return 1;
        }
    }
    for (int i = 0; i < n; i++) {
        int rc = pthread_join(tids[i], nullptr);
        if (rc != 0) {
            fprintf(stderr, "pthread_join: %s\n", strerror(rc));
            return 1;
        }
    }

    // 所有线程都已 join，这里单线程读，不需要锁
    long total = 0, min = g_balance[0];
    for (int i = 0; i < NACCOUNTS; i++) {
        total += g_balance[i];
        if (g_balance[i] < min)
            min = g_balance[i];
    }
    printf("total=%ld attempts=%ld min=%ld\n", total, g_attempts, min);
    return 0;
}
