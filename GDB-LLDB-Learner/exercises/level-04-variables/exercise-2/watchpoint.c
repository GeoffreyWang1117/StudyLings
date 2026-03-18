#include <stdio.h>

int global_var = 0;

void modify_value(int *ptr) {
    *ptr = 100;
}

int main() {
    int local_var = 10;
    printf("初始值: %d\n", local_var);

    local_var = 20;
    modify_value(&local_var);
    global_var = 50;

    printf("最终值: local=%d, global=%d\n", local_var, global_var);
    return 0;
}
