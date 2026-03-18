#include <stdio.h>

void func_c(int x) {
    printf("In func_c: x = %d\n", x);
}

void func_b(int y) {
    int b = y * 2;
    func_c(b);
}

void func_a(int z) {
    int a = z + 1;
    func_b(a);
}

int main() {
    printf("调用栈演示\n");
    func_a(10);
    return 0;
}
