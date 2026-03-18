#include <stdio.h>

// ========== 强符号和弱符号 ==========

// 强符号（正常定义）
int strong_var = 100;

// 弱符号（可被覆盖）
__attribute__((weak)) int weak_var = 200;

// 弱函数
__attribute__((weak)) int weak_function(int x) {
    printf("  [默认 weak_function: x=%d]\n", x);
    return x * 2;
}

// ========== 符号可见性 ==========

// 默认可见性（external linkage）
int public_var = 1;

// 隐藏符号（仅库内可见）
__attribute__((visibility("hidden"))) int hidden_var = 2;

// 内部符号（仅本文件可见）
static int static_var = 3;

// 外部声明（定义在其他文件）
extern int external_var;

// ========== 不同存储类别 ==========

// .data 段（已初始化）
int global_initialized = 42;

// .bss 段（未初始化，自动清零）
int global_uninitialized;

// .rodata 段（只读）
const int const_value = 99;
const char *const_string = "Hello";

// ========== 函数符号 ==========

// 全局函数
void public_function(void) {
    printf("  [public_function called]\n");
}

// 隐藏函数
__attribute__((visibility("hidden")))
void hidden_function(void) {
    printf("  [hidden_function called]\n");
}

// 静态函数（局部符号）
static void static_function(void) {
    printf("  [static_function called]\n");
}

// ========== 符号别名 ==========

// 创建别名
int original_function(int x) __attribute__((alias("aliased_function")));
int aliased_function(int x) {
    return x + 10;
}

// ========== 主程序 ==========

void demonstrate_symbols(void) {
    printf("=== 符号类型演示 ===\n\n");

    printf("强符号和弱符号:\n");
    printf("  strong_var = %d\n", strong_var);
    printf("  weak_var = %d\n", weak_var);
    printf("  weak_function(5) = %d\n", weak_function(5));

    printf("\n符号可见性:\n");
    printf("  public_var = %d\n", public_var);
    printf("  hidden_var = %d\n", hidden_var);
    printf("  static_var = %d\n", static_var);

    printf("\n不同段的符号:\n");
    printf("  global_initialized (.data) = %d\n", global_initialized);
    printf("  global_uninitialized (.bss) = %d\n", global_uninitialized);
    printf("  const_value (.rodata) = %d\n", const_value);

    printf("\n函数调用:\n");
    public_function();
    hidden_function();
    static_function();

    printf("\n符号别名:\n");
    printf("  original_function(5) = %d\n", original_function(5));
}

int main() {
    demonstrate_symbols();

    printf("\n任务:\n");
    printf("1. 使用 'nm' 查看不同类型的符号\n");
    printf("2. 使用 'readelf -s' 查看符号表详情\n");
    printf("3. 观察隐藏符号和静态符号的区别\n");
    printf("4. 在 GDB 中查找符号\n");

    return 0;
}
