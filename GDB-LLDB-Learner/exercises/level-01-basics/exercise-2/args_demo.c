#include <stdio.h>
#include <stdlib.h>

/*
 * 命令行参数演示程序
 * 用法: ./args_demo <num1> <num2>
 * 示例: ./args_demo 10 20
 */

int main(int argc, char *argv[]) {
    printf("程序名: %s\n", argv[0]);
    printf("参数数量: %d\n", argc - 1);

    // 检查参数数量
    if (argc != 3) {
        printf("用法: %s <num1> <num2>\n", argv[0]);
        printf("示例: %s 10 20\n", argv[0]);
        return 1;
    }

    // 打印参数
    printf("参数 1: %s\n", argv[1]);
    printf("参数 2: %s\n", argv[2]);

    // 转换为整数
    int num1 = atoi(argv[1]);
    int num2 = atoi(argv[2]);

    // 计算结果
    int result = num1 + num2;
    printf("结果: %d + %d = %d\n", num1, num2, result);

    return 0;
}
