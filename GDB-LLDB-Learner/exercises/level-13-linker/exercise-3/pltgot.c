#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>

// 外部库函数（libc）
// 这些函数会通过 PLT/GOT 调用

void demonstrate_plt_got() {
    printf("=== PLT/GOT 延迟绑定演示 ===\n\n");

    // 第一次调用 printf - 会触发 PLT 解析
    printf("第一次调用 printf\n");

    // 第二次调用 - 直接使用 GOT 中的地址
    printf("第二次调用 printf (已解析)\n");

    // 调用其他 libc 函数
    void *ptr = malloc(100);
    printf("malloc 分配: %p\n", ptr);
    free(ptr);

    printf("所有函数调用完成\n");
}

int main(int argc, char *argv[]) {
    int disable_lazy = 0;

    if (argc > 1 && argv[1][0] == '1') {
        disable_lazy = 1;
    }

    if (disable_lazy) {
        printf("延迟绑定已禁用 (LD_BIND_NOW=1)\n\n");
    } else {
        printf("延迟绑定已启用 (默认)\n\n");
    }

    demonstrate_plt_got();

    printf("\n任务:\n");
    printf("1. 使用 GDB 在 PLT 条目上设置断点\n");
    printf("2. 观察第一次调用时的动态解析过程\n");
    printf("3. 查看 GOT 表在调用前后的变化\n");
    printf("4. 使用 LD_DEBUG=bindings 查看绑定过程\n");
    printf("5. 使用 LD_PRELOAD 劫持函数调用\n");

    return 0;
}
