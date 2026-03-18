#include <stdio.h>

void buggy_function(int *ptr) {
    *ptr = 100;  # 如果 ptr 是 NULL 会崩溃
}

int main() {
    int *bad_ptr = NULL;
    buggy_function(bad_ptr);
    return 0;
}
