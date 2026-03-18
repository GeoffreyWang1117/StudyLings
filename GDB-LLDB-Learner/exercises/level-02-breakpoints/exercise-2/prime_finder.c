#include <stdio.h>
#include <stdbool.h>

bool check_prime(int num) {
    if (num <= 1) return false;
    if (num == 2) return true;
    if (num % 2 == 0) return false;

    for (int i = 3; i * i <= num; i += 2) {
        if (num % i == 0) {
            return false;
        }
    }
    return true;
}

void find_primes(int start, int end) {
    printf("查找 %d 到 %d 之间的质数:\n", start, end);

    for (int i = start; i <= end; i++) {
        if (check_prime(i)) {
            printf("%d 是质数\n", i);
        }
    }
}

int main() {
    printf("质数查找程序\n");
    printf("=============\n\n");

    find_primes(1, 30);

    return 0;
}
