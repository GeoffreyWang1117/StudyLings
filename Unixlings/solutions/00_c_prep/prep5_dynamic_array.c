// EXERCISE: prep5_dynamic_array — malloc/realloc/free 与"所有权"
// TOPIC: 堆内存 / 扩容 / 泄漏检测
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §7.8；这就是 Rust Vec<T>、Go slice、C++ std::vector 在底层做的事
//
// 说明：
//   实现一个 int 动态数组 struct vec：
//   1. vec_push：容量不够时按 2 倍扩容（初始容量 4）。realloc 可能失败返回 NULL ——
//      如果写成 v->data = realloc(v->data, ...)，失败时原指针就丢了（泄漏）。先存到临时变量。
//   2. vec_free：释放并把结构体恢复成空状态（防止 double free / use-after-free）。
//   3. join_ints：把数组格式化为 "1,2,3" 返回一个 malloc 出来的字符串 —— 调用者负责 free。
//      这就是 C 里的"所有权转移"，在函数注释里写清楚谁负责释放是 C 程序员的基本素养。
//   本题用 AddressSanitizer + LeakSanitizer 编译：越界写和内存泄漏都会让程序以非 0 退出。

#include "sl.h"

#include <stdint.h>

struct vec {
    int *data;
    size_t len;
    size_t cap;
};

// TODO: 追加一个元素，必要时扩容。成功返回 0，内存不足返回 -1（原数组保持不变）
static int vec_push(struct vec *v, int x) {
    if (v->len == v->cap) {
        size_t ncap = v->cap ? v->cap * 2 : 4;
        if (ncap > SIZE_MAX / sizeof *v->data)
            return -1;
        int *p = realloc(v->data, ncap * sizeof *v->data);
        if (!p)
            return -1; // v->data 仍然有效，没有泄漏
        v->data = p;
        v->cap = ncap;
    }
    v->data[v->len++] = x;
    return 0;
}

// TODO: 释放内存并重置为 {nullptr, 0, 0}
static void vec_free(struct vec *v) {
    free(v->data);
    *v = (struct vec){};
}

// TODO: 返回新分配的字符串 "a,b,c"（空数组返回 ""），调用者负责 free；内存不足返回 nullptr
// 提示：snprintf(nullptr, 0, ...) 可以先算出需要的长度
static char *join_ints(const struct vec *v) {
    size_t need = 1; // '\0'
    for (size_t i = 0; i < v->len; i++)
        need += (size_t)snprintf(nullptr, 0, "%s%d", i ? "," : "", v->data[i]);
    char *s = malloc(need);
    if (!s)
        return nullptr;
    size_t off = 0;
    s[0] = '\0';
    for (size_t i = 0; i < v->len; i++)
        off += (size_t)snprintf(s + off, need - off, "%s%d", i ? "," : "", v->data[i]);
    return s;
}

// ---- 以下为自测，不要修改 ----
int main(void) {
    struct vec v = {};
    for (int i = 1; i <= 10000; i++)
        SL_CHECK_EQ(vec_push(&v, i), 0);
    SL_CHECK_EQ(v.len, 10000);
    SL_CHECK(v.cap >= v.len && (v.cap & (v.cap - 1)) == 0); // 容量是 2 的幂
    long sum = 0;
    for (size_t i = 0; i < v.len; i++)
        sum += v.data[i];
    SL_CHECK_EQ(sum, 50005000L);
    vec_free(&v);
    SL_CHECK(v.data == nullptr && v.len == 0 && v.cap == 0);

    struct vec w = {};
    char *s = join_ints(&w);
    SL_CHECK(s && strcmp(s, "") == 0);
    free(s);
    vec_push(&w, 1);
    vec_push(&w, -20);
    vec_push(&w, 300);
    s = join_ints(&w);
    SL_CHECK(s && strcmp(s, "1,-20,300") == 0);
    free(s);
    vec_free(&w);
    return sl_report();
}
