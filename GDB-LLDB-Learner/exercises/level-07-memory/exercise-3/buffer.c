#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];
    strcpy(buffer, "Hello");  // OK
    strcpy(buffer, "This is too long!");  // Buffer overflow!

    printf("Buffer: %s\n", buffer);
    return 0;
}
