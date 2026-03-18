#include <stdio.h>
void calculate(int a, int b, int c, int d, int e) {
    int sum = a + b + c + d + e;
    printf("Sum = %d\n", sum);
}
int main() {
    calculate(10, 20, 30, 40, 50);
    return 0;
}
