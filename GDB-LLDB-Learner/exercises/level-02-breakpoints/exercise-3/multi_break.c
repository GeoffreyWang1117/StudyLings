#include <stdio.h>

int calculate(int a, int b) {
    return a + b;
}

void process_data(int *arr, int size) {
    printf("处理数组...\n");
    for (int i = 0; i < size; i++) {
        arr[i] = calculate(arr[i], i);
    }
}

void display_results(int *arr, int size) {
    printf("结果: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int data[] = {1, 2, 3, 4, 5};
    int size = 5;

    printf("断点管理演示\n");
    printf("============\n\n");

    process_data(data, size);
    display_results(data, size);

    return 0;
}
