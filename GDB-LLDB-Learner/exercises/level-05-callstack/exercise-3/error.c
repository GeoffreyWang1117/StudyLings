#include <stdio.h>
#include <stdlib.h>

void process(int *data) {
    if (!data) {
        fprintf(stderr, "Error: NULL pointer!\n");
        return;
    }
    *data = 42;
}

void caller() {
    int *ptr = NULL;
    process(ptr);  # Bug!
}

int main() {
    caller();
    return 0;
}
