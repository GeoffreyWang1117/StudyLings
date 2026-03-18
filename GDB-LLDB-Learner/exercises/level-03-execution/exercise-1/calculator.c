#include <stdio.h>

/*
 * 简单计算器程序
 * 用于练习 step 和 next 命令
 */

int add(int a, int b) {
    int result = a + b;
    return result;
}

int multiply(int a, int b) {
    int result = a * b;
    return result;
}

int calculate(int x, int y) {
    int sum = add(x, y);
    int product = multiply(x, y);
    return sum + product;
}

int main() {
    printf("开始计算...\n");

    int num1 = 5;
    int num2 = 3;

    int sum = add(num1, num2);
    printf("加法: %d + %d = %d\n", num1, num2, sum);

    int product = multiply(num1, num2);
    printf("乘法: %d * %d = %d\n", num1, num2, product);

    int final = calculate(num1, num2);
    printf("综合计算结果: %d\n", final);

    return 0;
}
