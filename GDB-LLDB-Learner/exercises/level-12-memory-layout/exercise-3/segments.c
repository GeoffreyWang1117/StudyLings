#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 全局变量（初始化）→ .data 段
int global_initialized = 42;
char global_string[] = "Hello, World!";

// 全局变量（未初始化）→ .bss 段
int global_uninitialized;
char global_buffer[1024];

// 常量 → .rodata 段
const int const_value = 100;
const char *const_string = "Constant String";

// 函数 → .text 段
void func_level3() {
    int local3 = 3;
    printf("Level 3: local3 @ %p\n", (void*)&local3);
}

void func_level2() {
    int local2 = 2;
    printf("Level 2: local2 @ %p\n", (void*)&local2);
    func_level3();
}

void func_level1() {
    int local1 = 1;
    printf("Level 1: local1 @ %p\n", (void*)&local1);
    func_level2();
}

void show_stack_growth() {
    printf("\n=== 栈增长方向 ===\n");

    int var1 = 1;
    int var2 = 2;
    int var3 = 3;

    printf("var1 @ %p\n", (void*)&var1);
    printf("var2 @ %p\n", (void*)&var2);
    printf("var3 @ %p\n", (void*)&var3);

    if ((void*)&var2 < (void*)&var1) {
        printf("栈向下增长（高地址 → 低地址）\n");
    } else {
        printf("栈向上增长（低地址 → 高地址）\n");
    }
}

void show_memory_layout() {
    printf("=== 内存段布局 ===\n\n");

    // 栈变量
    int stack_var = 10;

    // 堆分配
    int *heap_var = malloc(sizeof(int));
    *heap_var = 20;

    // 静态变量
    static int static_var = 30;

    printf("代码段 (.text):\n");
    printf("  main 函数: %p\n", (void*)main);
    printf("  func_level1: %p\n", (void*)func_level1);

    printf("\n只读数据段 (.rodata):\n");
    printf("  const_value: %p (值: %d)\n", (void*)&const_value, const_value);
    printf("  const_string ptr: %p\n", (void*)&const_string);
    printf("  const_string 内容: %p\n", (void*)const_string);

    printf("\n数据段 (.data):\n");
    printf("  global_initialized: %p (值: %d)\n",
           (void*)&global_initialized, global_initialized);
    printf("  global_string: %p (内容: \"%s\")\n",
           (void*)global_string, global_string);

    printf("\nBSS 段 (.bss):\n");
    printf("  global_uninitialized: %p (值: %d)\n",
           (void*)&global_uninitialized, global_uninitialized);
    printf("  global_buffer: %p\n", (void*)global_buffer);

    printf("\n堆 (heap):\n");
    printf("  heap_var: %p (值: %d)\n", (void*)heap_var, *heap_var);

    printf("\n栈 (stack):\n");
    printf("  stack_var: %p (值: %d)\n", (void*)&stack_var, stack_var);
    printf("  static_var: %p (值: %d)\n", (void*)&static_var, static_var);

    // 清理
    free(heap_var);
}

void show_stack_frame() {
    printf("\n=== 栈帧布局 ===\n");
    func_level1();
}

int main() {
    show_memory_layout();
    show_stack_growth();
    show_stack_frame();

    printf("\n任务:\n");
    printf("1. 使用 'info proc mappings' 查看完整内存映射\n");
    printf("2. 比较不同段的地址范围\n");
    printf("3. 观察栈帧的创建和销毁\n");
    printf("4. 查看调用栈和局部变量的位置\n");

    return 0;
}
