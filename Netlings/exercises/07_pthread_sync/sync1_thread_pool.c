// EXERCISE: sync1_thread_pool — 固定大小线程池：互斥量 + 条件变量任务队列 + 优雅关闭
// TOPIC: pthread_mutex / pthread_cond_wait / 虚假唤醒 / broadcast / 先排空队列再 join
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §11.6（互斥量、条件变量）；man 3 pthread_cond_wait；UNP §26.8（线程池服务器）
// I AM NOT DONE
//
// 说明：
//   用法：sync1_thread_pool NTHREADS MTASKS [IDLE_MS]
//   创建 NTHREADS 个 worker 的线程池，提交 MTASKS 个任务；第 i 个任务（i = 1..M）睡 200µs 后把 i
//   原子地加到 total。可选 IDLE_MS：提交完之后主线程先睡这么久再关闭（此时所有 worker 都在
//   条件变量上睡着）。最后 pool_shutdown：**先执行完队列里剩下的所有任务**，再 join 所有 worker。
//   打印 "done=<执行了的任务数> total=<总和>"，应为 done=M total=M*(M+1)/2。
//
//   关键点：
//   - 等待条件必须写在 while 里：pthread_cond_wait 可能虚假唤醒，被唤醒时条件也可能已被别人抢走。
//   - worker 的退出条件是"队列空 **并且** 正在关闭"，而不是"一看到关闭就走"——否则排队的请求被丢掉。
//   - 关闭时要 pthread_cond_broadcast：所有睡着的 worker 都得醒来看到 shutdown 标志；
//     只 signal 一个的话，其余 worker 永远睡下去，join 卡死。
//   - 这一章用 ThreadSanitizer 构建：任何数据竞争都会让程序以 exit 66 结束。
//
//   现实中：几乎每个服务器都有线程池 —— nginx 的 thread_pool（aio threads）、libuv 的
//   threadpool（Node.js 的 fs/dns 都跑在上面，UV_THREADPOOL_SIZE）、PostgreSQL 的 I/O workers、
//   MySQL/Percona thread pool、Redis 6+ 的 I/O threads、tokio 的 blocking pool。优雅关闭
//   （drain 后再退出）正是 Kubernetes 发 SIGTERM 后服务器应该做的事。

#include <errno.h>
#include <stdatomic.h>
#include <stdint.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "sl.h"

typedef void (*task_fn)(void *arg);

struct task {
    task_fn fn;
    void *arg;
    struct task *next;
};

struct pool {
    pthread_mutex_t mu;
    pthread_cond_t cv;   // "队列里有活了" 或 "要关闭了"
    struct task *head;   // 队首（FIFO）
    struct task *tail;
    bool shutdown;
    size_t nthreads;
    pthread_t *threads;
};

static void *worker(void *arg) {
    struct pool *p = arg;
    for (;;) {
        pthread_mutex_lock(&p->mu);
        while (p->head == nullptr && !p->shutdown)
            pthread_cond_wait(&p->cv, &p->mu);
        // BUG: 一看到 shutdown 就退出，队列里还没执行的任务全被丢掉了。
        // TODO: 只有"队列空并且正在关闭"时才退出；队列里还有任务就继续取
        if (p->shutdown) {
            pthread_mutex_unlock(&p->mu);
            return nullptr;
        }
        struct task *t = p->head;
        p->head = t->next;
        if (p->head == nullptr)
            p->tail = nullptr;
        pthread_mutex_unlock(&p->mu);

        t->fn(t->arg); // 在锁外执行任务
        free(t);
    }
}

static struct pool *pool_create(size_t n) {
    struct pool *p = calloc(1, sizeof *p);
    if (!p)
        return nullptr;
    p->threads = calloc(n, sizeof *p->threads);
    if (!p->threads) {
        free(p);
        return nullptr;
    }
    pthread_mutex_init(&p->mu, nullptr);
    pthread_cond_init(&p->cv, nullptr);
    for (size_t i = 0; i < n; i++) {
        int rc = pthread_create(&p->threads[i], nullptr, worker, p);
        if (rc != 0) {
            errno = rc;
            sl_die("pthread_create");
        }
        p->nthreads++;
    }
    return p;
}

// 提交任务。关闭之后提交返回 false
static bool pool_submit(struct pool *p, task_fn fn, void *arg) {
    struct task *t = malloc(sizeof *t);
    if (!t)
        return false;
    *t = (struct task){.fn = fn, .arg = arg};
    pthread_mutex_lock(&p->mu);
    if (p->shutdown) {
        pthread_mutex_unlock(&p->mu);
        free(t);
        return false;
    }
    if (p->tail)
        p->tail->next = t;
    else
        p->head = t;
    p->tail = t;
    pthread_cond_signal(&p->cv); // 一个新任务只需要叫醒一个 worker
    pthread_mutex_unlock(&p->mu);
    return true;
}

// 优雅关闭：不再接收新任务，排空队列，join 所有 worker，释放资源
static void pool_shutdown(struct pool *p) {
    pthread_mutex_lock(&p->mu);
    p->shutdown = true;
    // BUG: signal 只叫醒一个 worker，其余在条件变量上睡着的 worker 永远醒不来，下面的 join 卡死。
    // TODO: 叫醒**所有**睡着的 worker
    pthread_cond_signal(&p->cv);
    pthread_mutex_unlock(&p->mu);

    for (size_t i = 0; i < p->nthreads; i++)
        pthread_join(p->threads[i], nullptr);

    // 正常情况下队列已经空了；防御性地释放残留任务
    for (struct task *t = p->head; t;) {
        struct task *next = t->next;
        free(t);
        t = next;
    }
    pthread_cond_destroy(&p->cv);
    pthread_mutex_destroy(&p->mu);
    free(p->threads);
    free(p);
}

// ---- 脚手架：任务与主程序 ----

static atomic_ullong g_total;
static atomic_ullong g_done;

static void sleep_us(long us) {
    struct timespec ts = {.tv_sec = us / 1000000, .tv_nsec = (us % 1000000) * 1000L};
    while (nanosleep(&ts, &ts) < 0 && errno == EINTR) {
    }
}

static void add_task(void *arg) {
    sleep_us(200); // 模拟一次阻塞 I/O
    atomic_fetch_add_explicit(&g_total, (unsigned long long)(uintptr_t)arg, memory_order_relaxed);
    atomic_fetch_add_explicit(&g_done, 1, memory_order_relaxed);
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 3 && argc != 4) {
        fprintf(stderr, "usage: %s NTHREADS MTASKS [IDLE_MS]\n", argv[0]);
        return 2;
    }
    long n = strtol(argv[1], nullptr, 10), m = strtol(argv[2], nullptr, 10);
    long idle_ms = argc == 4 ? strtol(argv[3], nullptr, 10) : 0;
    if (n <= 0 || m < 0 || idle_ms < 0) {
        fprintf(stderr, "bad arguments\n");
        return 2;
    }

    struct pool *p = pool_create((size_t)n);
    if (!p)
        sl_die("pool_create");
    for (long i = 1; i <= m; i++) {
        if (!pool_submit(p, add_task, (void *)(uintptr_t)i))
            sl_die("pool_submit");
    }
    if (idle_ms > 0)
        sleep_us(idle_ms * 1000); // 让所有 worker 做完并在条件变量上睡着
    pool_shutdown(p);

    printf("done=%llu total=%llu\n", atomic_load(&g_done), atomic_load(&g_total));
    return 0;
}
