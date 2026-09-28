// EXERCISE: prep1_pointers — 指针、数组退化与"输出参数"
// TOPIC: 指针 / 数组 / 输出参数
// DIFFICULTY: ★☆☆☆☆
// BOOK: 预备章 —— APUE 里几乎每个 API 都这样返回结果：read(fd, buf, n)、waitpid(pid, &status, 0)
// I AM NOT DONE
//
// 说明：
//   系统调用的通用风格是"调用者提供内存，函数通过指针写回结果"，返回值只报告成功/失败。
//   1. swap_int：交换两个 int
//   2. sum：数组求和 —— 数组传参时会"退化"为指针，函数内 sizeof(a) 拿不到长度，所以要显式传 n
//   3. max_index：通过输出参数 *out 返回最大值下标；n == 0 时返回 false 且不能写 *out
//   4. reverse：原地反转
//   完成 TODO 让自测全部通过，然后删除 "I AM NOT DONE" 这一行。

#include "sl.h"

#include <stddef.h>

// TODO: 交换 *a 和 *b
static void swap_int(int *a, int *b) {
}

// TODO: 返回 a[0..n) 之和（用 long 防止溢出）
static long sum(const int *a, size_t n) {
    return 0;
}

// TODO: 找最大值的下标写入 *out 并返回 true；n == 0 时返回 false
static bool max_index(const int *a, size_t n, size_t *out) {
    return false;
}

// TODO: 原地反转 a[0..n)（可以复用 swap_int）
static void reverse(int *a, size_t n) {
}

// ---- 以下为自测，不要修改 ----
int main(void) {
    int x = 1, y = 2;
    swap_int(&x, &y);
    SL_CHECK_EQ(x, 2);
    SL_CHECK_EQ(y, 1);

    int a[] = {3, 1, 4, 1, 5, 9, 2, 6};
    size_t n = sizeof a / sizeof a[0]; // 这里 a 还是数组，sizeof 得到整个数组的字节数
    SL_CHECK_EQ(sum(a, n), 31);
    SL_CHECK_EQ(sum(a, 0), 0);

    size_t idx = 12345;
    SL_CHECK(max_index(a, n, &idx));
    SL_CHECK_EQ(idx, 5);
    idx = 12345;
    SL_CHECK(!max_index(a, 0, &idx));
    SL_CHECK_EQ(idx, 12345); // n == 0 时不许写输出参数

    reverse(a, n);
    int expect[] = {6, 2, 9, 5, 1, 4, 1, 3};
    for (size_t i = 0; i < n; i++)
        SL_CHECK_EQ(a[i], expect[i]);
    reverse(a, 0);
    return sl_report();
}
