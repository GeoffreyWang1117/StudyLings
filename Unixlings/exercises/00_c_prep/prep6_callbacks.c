// EXERCISE: prep6_callbacks — 函数指针与 void *ctx：C 的"闭包"
// TOPIC: 函数指针 / 回调 / qsort 比较器 / void* 上下文
// DIFFICULTY: ★★★☆☆
// BOOK: 预备章 —— pthread_create(&t, NULL, fn, arg)、sigaction 的 sa_handler、qsort、
//       epoll 事件循环里的 handler 表，都靠"函数指针 + void *上下文"
// I AM NOT DONE
//
// 说明：
//   1. cmp_conn：qsort 比较器。先按 latency_us 升序，相同时按 id 升序。
//      经典错误：return a->latency_us - b->latency_us; —— 值域大时减法会溢出，排序结果错乱。
//      正确写法：(x > y) - (x < y)
//   2. for_each：对数组每个元素调用 fn(elem, ctx)。ctx 是调用者传进来的任意数据，
//      for_each 本身不知道它是什么 —— 这就是 C 没有闭包时的替代方案。
//   3. stats_cb：作为回调传给 for_each，把 sum/count/max 累加到 ctx 指向的 struct stats 里。

#include "sl.h"

#include <limits.h>

struct conn {
    int id;
    int latency_us;
};

struct stats {
    long sum;
    int count;
    int max;
};

typedef void (*visit_fn)(const struct conn *c, void *ctx);

// TODO: 不会溢出的比较器
static int cmp_conn(const void *pa, const void *pb) {
    const struct conn *a = pa, *b = pb;
    return a->latency_us - b->latency_us;
}

// TODO: 对每个元素调用 fn(&arr[i], ctx)
static void for_each(const struct conn *arr, size_t n, visit_fn fn, void *ctx) {
}

// TODO: 把 ctx 转回 struct stats * 并累加
static void stats_cb(const struct conn *c, void *ctx) {
}

// ---- 以下为自测，不要修改 ----
int main(void) {
    struct conn cs[] = {
        {1, 300}, {2, INT_MAX}, {3, -5}, {4, 300}, {5, INT_MIN}, {6, 0},
    };
    size_t n = sizeof cs / sizeof cs[0];
    qsort(cs, n, sizeof cs[0], cmp_conn);
    int expect_ids[] = {5, 3, 6, 1, 4, 2};
    for (size_t i = 0; i < n; i++)
        SL_CHECK_EQ(cs[i].id, expect_ids[i]);

    struct conn live[] = {{1, 120}, {2, 80}, {3, 400}};
    struct stats st = {.sum = 0, .count = 0, .max = INT_MIN};
    for_each(live, 3, stats_cb, &st);
    SL_CHECK_EQ(st.count, 3);
    SL_CHECK_EQ(st.sum, 600);
    SL_CHECK_EQ(st.max, 400);
    return sl_report();
}
