// EXERCISE: thr1_create_join — pthread_create / pthread_join 并行求和
// TOPIC: 线程创建、参数传递、join 取回结果
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §11.4-11.5（线程创建、线程终止）；man 3 pthread_create, pthread_join
// I AM NOT DONE
//
// 说明：
//   用法：thr1_create_join NTHREADS
//   把 1..10000000 的求和平均切成 NTHREADS 段，每个线程算一段，main 用 pthread_join 等所有线程结束，
//   再把各段结果加起来，打印一行：sum=<总和>
//
//   经典坑：pthread_create(&tid, nullptr, worker, &i) —— 把循环变量 i 的地址传给每个线程。
//   所有线程拿到的是"同一个地址"，线程真正读取 *arg 时 main 早已把 i 改掉了（数据竞争 + 分段错乱）。
//   正确做法：每个线程一个独立的参数结构体（放在数组/堆上，生命周期覆盖到 join 之后），
//   结构体里既有输入（区间 lo..hi）也有输出槽（partial sum），线程写自己的槽，join 之后 main 再读。
//
//   测试：NTHREADS = 1 / 4 / 7（7 不能整除，最后一段要把余数收掉），检查 sum 正确且退出码为 0。
//   本章用 ThreadSanitizer 编译：一旦有数据竞争，程序以退出码 66 结束。
//
//   现代意义：Go 1.22 之前 `for i := ... { go func(){ use(i) }() }` 是同一个坑；
//   Rust 的 thread::spawn 要求 move + 'static 就是为了在编译期禁止它。
//   Redis 的 bio 线程、nginx 的 thread_pool 都用"每任务一个结构体"传参。

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { LIMIT = 10000000 };

// 每个线程独享一个：输入区间 [lo, hi]，输出 partial
struct task {
    long lo;
    long hi;
    long long partial;
};

// 起步代码：线程只拿到一个"下标"，再从全局数组里找自己的 task。
static struct task *g_tasks;

// TODO: 改成直接接收 struct task *（arg 就是它自己的那个结构体），不要再经过 int 下标。
static void *worker(void *arg) {
    int idx = *(const int *)arg; // BUG: arg 指向 main 的循环变量 i，读到时 i 可能早就变了
    struct task *t = &g_tasks[idx];
    long long s = 0;
    for (long v = t->lo; v <= t->hi; v++)
        s += v;
    t->partial = s;
    return nullptr;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s NTHREADS\n", argv[0]);
        return 2;
    }
    int n = atoi(argv[1]);
    if (n < 1 || n > 256) {
        fprintf(stderr, "thr1_create_join: NTHREADS must be 1..256\n");
        return 2;
    }

    pthread_t *tids = calloc((size_t)n, sizeof *tids);
    struct task *tasks = calloc((size_t)n, sizeof *tasks);
    if (!tids || !tasks) {
        fprintf(stderr, "thr1_create_join: out of memory\n");
        return 1;
    }
    g_tasks = tasks;

    long chunk = LIMIT / n;
    for (int i = 0; i < n; i++) {
        tasks[i].lo = (long)i * chunk + 1;
        tasks[i].hi = (i == n - 1) ? LIMIT : (long)(i + 1) * chunk;
        // TODO: 每个线程传它自己的 &tasks[i]
        int rc = pthread_create(&tids[i], nullptr, worker, &i); // BUG: 所有线程共享同一个 &i
        if (rc != 0) {
            fprintf(stderr, "pthread_create: %s\n", strerror(rc));
            return 1;
        }
    }

    long long sum = 0;
    for (int i = 0; i < n; i++) {
        int rc = pthread_join(tids[i], nullptr);
        if (rc != 0) {
            fprintf(stderr, "pthread_join: %s\n", strerror(rc));
            return 1;
        }
        sum += tasks[i].partial;
    }

    printf("sum=%lld\n", sum);
    free(tasks);
    free(tids);
    return 0;
}
