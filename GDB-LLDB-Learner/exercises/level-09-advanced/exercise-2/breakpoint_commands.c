#include <stdio.h>

int process_item(int item) {
    int result = item * 2;
    return result;
}

int main() {
    printf("自动化断点命令演示\n\n");

    for (int i = 1; i <= 10; i++) {
        int result = process_item(i);
        printf("Item %d -> %d\n", i, result);
    }

    return 0;
}
