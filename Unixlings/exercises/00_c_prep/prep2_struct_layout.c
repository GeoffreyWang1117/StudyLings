// EXERCISE: prep2_struct_layout — 结构体内存布局：对齐、填充、offsetof
// TOPIC: sizeof / alignof / offsetof / 字段重排
// DIFFICULTY: ★★☆☆☆
// BOOK: 预备章 —— struct stat、struct sockaddr_in6、协议头、共享内存里的结构都要求你"看得见"内存布局
// I AM NOT DONE
//
// 说明：
//   编译器会在字段之间插入填充（padding），让每个字段落在自己的对齐边界上，
//   整个结构体的大小也会补齐到最大对齐的整数倍。本题假设 LP64（x86-64 / aarch64 Linux）。
//   1. 不运行程序，先在纸上推算下面 enum 里的 6 个数字，填进去（这就是"预测"练习）
//   2. 重排 struct flow_record 的字段顺序（不许删字段、不许改类型、不许用 packed），
//      让 sizeof(struct flow_record) <= 16
//   调试技巧：gdb 里 `ptype /o struct record_a` 会直接打印每个字段的偏移和空洞。

#include "sl.h"

#include <stdalign.h>
#include <stddef.h>
#include <stdint.h>

struct record_a {
    char tag;
    int id;
    char flag;
    double score;
};

struct record_b {
    char tag;
    char flag;
    int id;
    double score;
};

// TODO: 推算并填写（不要写成 sizeof(...) —— 那就失去练习意义了）
enum {
    SIZEOF_A = 0,
    OFFSET_A_ID = 0,
    OFFSET_A_FLAG = 0,
    OFFSET_A_SCORE = 0,
    SIZEOF_B = 0,
    ALIGNOF_A = 0,
};

// TODO: 重排字段，使 sizeof <= 16（当前是 32）
struct flow_record {
    uint8_t proto;
    double timestamp;
    uint16_t port;
    int32_t bytes;
    uint8_t ttl;
};

// ---- 以下为自测，不要修改 ----
int main(void) {
    SL_CHECK_EQ(SIZEOF_A, sizeof(struct record_a));
    SL_CHECK_EQ(OFFSET_A_ID, offsetof(struct record_a, id));
    SL_CHECK_EQ(OFFSET_A_FLAG, offsetof(struct record_a, flag));
    SL_CHECK_EQ(OFFSET_A_SCORE, offsetof(struct record_a, score));
    SL_CHECK_EQ(SIZEOF_B, sizeof(struct record_b));
    SL_CHECK_EQ(ALIGNOF_A, alignof(struct record_a));

    struct flow_record r = {.proto = 6, .timestamp = 1.5, .port = 443, .bytes = 1500, .ttl = 64};
    SL_CHECK(r.proto == 6 && r.timestamp == 1.5 && r.port == 443 && r.bytes == 1500 && r.ttl == 64);
    printf("sizeof(struct flow_record) = %zu\n", sizeof(struct flow_record));
    SL_CHECK(sizeof(struct flow_record) <= 16);
    return sl_report();
}
