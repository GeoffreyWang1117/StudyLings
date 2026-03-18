#include <stdio.h>

void print_array(int *arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int numbers[] = {10, 20, 30, 40, 50};
    int matrix[3][3] = {{1,2,3}, {4,5,6}, {7,8,9}};
    
    print_array(numbers, 5);
    printf("Matrix[1][1] = %d\n", matrix[1][1]);
    return 0;
}
