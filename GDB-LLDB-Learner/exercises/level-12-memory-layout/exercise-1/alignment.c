#include <stdio.h>
#include <stddef.h>

// 未优化的结构体
struct Unoptimized {
    char a;     // 1 byte
    int b;      // 4 bytes (需要对齐)
    char c;     // 1 byte
    double d;   // 8 bytes (需要对齐)
};

// 优化后的结构体（重排序）
struct Optimized {
    double d;   // 8 bytes
    int b;      // 4 bytes
    char a;     // 1 byte
    char c;     // 1 byte
};

// Packed 结构体（禁用对齐）
struct __attribute__((packed)) Packed {
    char a;
    int b;
    char c;
    double d;
};

int main() {
    printf("=== 结构体内存布局分析 ===\n\n");
    
    printf("未优化结构体:\n");
    printf("  sizeof(Unoptimized) = %lu\n", sizeof(struct Unoptimized));
    printf("  offsetof(a) = %lu\n", offsetof(struct Unoptimized, a));
    printf("  offsetof(b) = %lu\n", offsetof(struct Unoptimized, b));
    printf("  offsetof(c) = %lu\n", offsetof(struct Unoptimized, c));
    printf("  offsetof(d) = %lu\n", offsetof(struct Unoptimized, d));
    
    printf("\n优化结构体:\n");
    printf("  sizeof(Optimized) = %lu\n", sizeof(struct Optimized));
    printf("  offsetof(d) = %lu\n", offsetof(struct Optimized, d));
    printf("  offsetof(b) = %lu\n", offsetof(struct Optimized, b));
    printf("  offsetof(a) = %lu\n", offsetof(struct Optimized, a));
    printf("  offsetof(c) = %lu\n", offsetof(struct Optimized, c));
    
    printf("\nPacked 结构体:\n");
    printf("  sizeof(Packed) = %lu\n", sizeof(struct Packed));
    
    // 创建实例
    struct Unoptimized u = {'A', 42, 'B', 3.14};
    struct Optimized o = {3.14, 42, 'A', 'B'};
    struct Packed p = {'A', 42, 'B', 3.14};
    
    printf("\n任务: 使用 GDB 查看实际内存布局\n");
    printf("1. ptype /o struct Unoptimized\n");
    printf("2. x/24xb &u  (查看内存，观察 padding)\n");
    printf("3. 比较三种结构体的内存使用\n");
    
    return 0;
}
