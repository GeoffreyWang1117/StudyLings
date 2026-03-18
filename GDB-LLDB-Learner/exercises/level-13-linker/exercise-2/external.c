#include <stdio.h>

// 定义在 symbols.c 中声明为 extern 的变量
int external_var = 999;

// 强符号覆盖弱符号
int weak_var = 300;  // 覆盖 symbols.c 中的弱符号

// 强函数覆盖弱函数
int weak_function(int x) {
    printf("  [覆盖的 weak_function: x=%d]\n", x);
    return x * 3;
}
