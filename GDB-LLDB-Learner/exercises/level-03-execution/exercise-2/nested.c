#include <stdio.h>

int level3(int x) {
    printf("Level 3: x = %d\n", x);
    return x * 3;
}

int level2(int x) {
    printf("Level 2: x = %d\n", x);
    int result = level3(x + 1);
    return result * 2;
}

int level1(int x) {
    printf("Level 1: x = %d\n", x);
    int result = level2(x + 1);
    return result + 10;
}

int main() {
    printf("嵌套函数调用演示\n\n");
    int result = level1(5);
    printf("最终结果: %d\n", result);
    return 0;
}
