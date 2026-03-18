#include <stdio.h>
#include <stdlib.h>

void demonstrate_pointers() {
    // 一级指针
    int value = 42;
    int *p1 = &value;
    
    // 二级指针
    int **p2 = &p1;
    
    // 三级指针
    int ***p3 = &p2;
    
    printf("=== 指针层次演示 ===\n\n");
    
    // 打印地址和值
    printf("value 的地址: %p, 值: %d\n", (void*)&value, value);
    printf("p1 的地址: %p, p1 的值(指向 value): %p, *p1: %d\n", 
           (void*)&p1, (void*)p1, *p1);
    printf("p2 的地址: %p, p2 的值(指向 p1): %p, *p2: %p, **p2: %d\n",
           (void*)&p2, (void*)p2, (void*)*p2, **p2);
    printf("p3 的地址: %p, p3 的值(指向 p2): %p, *p3: %p, **p3: %p, ***p3: %d\n",
           (void*)&p3, (void*)p3, (void*)*p3, (void*)**p3, ***p3);
    
    // 通过不同层次修改 value
    printf("\n=== 通过指针修改值 ===\n");
    *p1 = 100;
    printf("通过 *p1 修改后, value = %d\n", value);
    
    **p2 = 200;
    printf("通过 **p2 修改后, value = %d\n", value);
    
    ***p3 = 300;
    printf("通过 ***p3 修改后, value = %d\n", value);
}

// 动态分配的多级指针
void dynamic_multilevel() {
    printf("\n=== 动态分配的多级指针 ===\n");
    
    // 分配并初始化一级指针
    int *p1 = malloc(sizeof(int));
    *p1 = 42;
    
    // 分配二级指针
    int **p2 = malloc(sizeof(int*));
    *p2 = p1;
    
    // 分配三级指针
    int ***p3 = malloc(sizeof(int**));
    *p3 = p2;
    
    printf("动态分配的值: %d\n", ***p3);
    printf("p1 地址: %p\n", (void*)p1);
    printf("p2 地址: %p, 指向: %p\n", (void*)p2, (void*)*p2);
    printf("p3 地址: %p, 指向: %p, 再指向: %p\n", 
           (void*)p3, (void*)*p3, (void*)**p3);
    
    // 清理（在调试器中检查释放过程）
    free(p1);
    free(p2);
    free(p3);
}

int main() {
    demonstrate_pointers();
    dynamic_multilevel();
    
    printf("\n=== 调试任务 ===\n");
    printf("1. 使用 GDB 查看每个指针的内存地址\n");
    printf("2. 使用 x/gx 命令查看指针链的内存布局\n");
    printf("3. 逐层解引用指针并验证值\n");
    printf("4. 在不同层次设置 watchpoint\n");
    
    return 0;
}
