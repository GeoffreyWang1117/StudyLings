#include <stdio.h>

int calculate(int x, int y) {
    int a = x + y;
    int b = a * 2;
    int c = b - 10;
    return c;
}

int main() {
    int result = calculate(5, 10);
    printf("Result: %d\n", result);
    return 0;
}
