#include <stdio.h>
#include "mathlib.h"

// 外部符号（链接时解析）
extern int mathlib_version;

int main() {
    printf("=== 静态链接 vs 动态链接演示 ===\n\n");

    printf("mathlib_version: %d\n", mathlib_version);

    int a = 10, b = 20;
    printf("add(%d, %d) = %d\n", a, b, add(a, b));
    printf("multiply(%d, %d) = %d\n", a, b, multiply(a, b));
    printf("factorial(%d) = %d\n", 5, factorial(5));

    printf("\n任务:\n");
    printf("1. 使用 nm 查看符号表\n");
    printf("2. 使用 ldd 查看动态库依赖\n");
    printf("3. 比较静态链接和动态链接的可执行文件大小\n");
    printf("4. 使用 GDB 查看符号来源\n");

    return 0;
}
