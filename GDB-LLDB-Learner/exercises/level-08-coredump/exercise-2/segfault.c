#include <stdio.h>

typedef struct {
    int id;
    char name[50];
} User;

void process_user(User *user) {
    printf("Processing user: %s\n", user->name);
    user->id = 42;  // 如果 user 为 NULL 崩溃
}

int main(int argc, char *argv[]) {
    User *u = NULL;

    if (argc > 1) {
        User temp = {1, "Test User"};
        u = &temp;
    }

    process_user(u);  // 可能崩溃
    return 0;
}
