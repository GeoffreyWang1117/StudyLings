#include <stdio.h>
#include <string.h>

int main() {
    char buffer[20] = "Hello";
    int numbers[] = {1, 2, 3, 4, 5};
    char *ptr = "World";
    
    printf("Buffer: %s\n", buffer);
    printf("Numbers[0]: %d\n", numbers[0]);
    return 0;
}
