#include <stdio.h>

/*
 * 计算阶乘的程序
 * 用于练习断点设置
 */

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int number = 5;
    int result;

    printf("计算 %d 的阶乘\n", number);
    result = factorial(number);
    printf("%d! = %d\n", number, result);

    return 0;
}
