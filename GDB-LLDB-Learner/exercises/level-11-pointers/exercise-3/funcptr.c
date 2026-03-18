#include <stdio.h>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }

typedef int (*Operation)(int, int);

void callback_example(int x, int y, Operation op, const char *name) {
    printf("%s(%d, %d) = %d\n", name, x, y, op(x, y));
}

int main() {
    printf("=== 函数指针演示 ===\n\n");
    
    // 1. 基本函数指针
    Operation op = add;
    printf("函数指针 op 指向: %p (add 函数)\n", (void*)op);
    printf("调用 op(5, 3) = %d\n\n", op(5, 3));
    
    // 2. 函数指针数组（跳转表）
    Operation ops[] = {add, sub, mul};
    const char *names[] = {"add", "sub", "mul"};
    
    printf("函数指针数组:\n");
    for (int i = 0; i < 3; i++) {
        printf("ops[%d] = %p (%s)\n", i, (void*)ops[i], names[i]);
    }
    
    // 3. 使用回调
    printf("\n使用回调函数:\n");
    callback_example(10, 5, add, "add");
    callback_example(10, 5, sub, "sub");
    callback_example(10, 5, mul, "mul");
    
    printf("\n任务: 使用调试器查看函数指针的地址和类型\n");
    
    return 0;
}
