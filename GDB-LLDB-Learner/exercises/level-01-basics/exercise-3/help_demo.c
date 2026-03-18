#include <stdio.h>

/*
 * 帮助系统演示程序
 * 这个程序很简单，主要用于练习调试器的帮助系统
 */

void print_message(const char *msg) {
    printf("消息: %s\n", msg);
}

int main() {
    const char *message = "学习使用调试器帮助系统！";
    int counter = 0;

    printf("帮助系统演示程序\n");
    printf("=================\n\n");

    for (int i = 0; i < 3; i++) {
        counter++;
        print_message(message);
    }

    printf("\n循环执行了 %d 次\n", counter);

    return 0;
}
