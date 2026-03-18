#include <stdio.h>

int main() {
    int value = 42;
    int *ptr = &value;
    int **ptr_ptr = &ptr;
    
    printf("Value: %d\n", **ptr_ptr);
    return 0;
}
