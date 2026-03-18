#include <stdio.h>
#include <assert.h>

int divide(int a, int b) {
    assert(b != 0 && "除数不能为零");
    return a / b;
}

int main() {
    int result1 = divide(10, 2);
    printf("10 / 2 = %d\n", result1);

    int result2 = divide(10, 0);  // 触发 assertion
    printf("10 / 0 = %d\n", result2);

    return 0;
}
