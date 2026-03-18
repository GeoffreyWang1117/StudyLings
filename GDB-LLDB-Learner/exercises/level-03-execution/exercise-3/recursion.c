#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

int main() {
    printf("斐波那契数列\n");
    for (int i = 0; i <= 6; i++) {
        printf("fib(%d) = %d\n", i, fibonacci(i));
    }
    return 0;
}
