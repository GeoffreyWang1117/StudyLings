#include "mathlib.h"
#include <stdio.h>

// 内部辅助函数（不导出）
static void internal_helper(void) {
    printf("  [mathlib internal helper called]\n");
}

int add(int a, int b) {
    internal_helper();
    return a + b;
}

int multiply(int a, int b) {
    int result = 0;
    for (int i = 0; i < b; i++) {
        result += a;
    }
    return result;
}

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// 全局变量（在 .data 段）
int mathlib_version = 100;

// 未初始化全局变量（在 .bss 段）
int mathlib_counter;
