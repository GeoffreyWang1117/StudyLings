#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void array_of_pointers() {
    printf("=== 指针数组 (Array of Pointers) ===\n");
    
    // 方式1: 字符串字面量
    char *names1[] = {"Alice", "Bob", "Charlie", "David"};
    
    printf("names1 是指针数组，包含 %lu 个指针\n", sizeof(names1)/sizeof(names1[0]));
    printf("names1 的大小: %lu 字节 (%lu 个指针 * %lu 字节/指针)\n",
           sizeof(names1), sizeof(names1)/sizeof(char*), sizeof(char*));
    
    for (int i = 0; i < 4; i++) {
        printf("names1[%d] = %p, 指向: \"%s\"\n", i, (void*)names1[i], names1[i]);
    }
    
    // 方式2: 动态分配的字符串数组(类似 argv)
    char **names2 = malloc(3 * sizeof(char*));
    names2[0] = strdup("Apple");
    names2[1] = strdup("Banana");
    names2[2] = strdup("Cherry");
    
    printf("\nnames2 也是指针数组（动态分配）\n");
    for (int i = 0; i < 3; i++) {
        printf("names2[%d] = %p, 指向: \"%s\"\n", i, (void*)names2[i], names2[i]);
    }
    
    // 清理
    for (int i = 0; i < 3; i++) free(names2[i]);
    free(names2);
}

void pointer_to_array() {
    printf("\n=== 数组指针 (Pointer to Array) ===\n");
    
    int matrix[3][4] = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12}
    };
    
    // ptr 是指向 int[4] 的指针
    int (*ptr)[4] = matrix;
    
    printf("matrix 的大小: %lu 字节\n", sizeof(matrix));
    printf("ptr 指向整行（4个int）\n");
    printf("ptr 的地址: %p\n", (void*)ptr);
    printf("ptr+1 的地址: %p (+%lu 字节)\n", 
           (void*)(ptr+1), (char*)(ptr+1) - (char*)ptr);
    
    for (int i = 0; i < 3; i++) {
        printf("行 %d: ", i);
        for (int j = 0; j < 4; j++) {
            printf("%d ", ptr[i][j]);
        }
        printf("\n");
    }
}

void compare_types() {
    printf("\n=== 类型对比 ===\n");
    
    char *arr1[5];      // 指针数组: 5个 char*
    char (*arr2)[5];    // 数组指针: 指向 char[5]
    
    printf("char *arr1[5]:\n");
    printf("  类型: 数组，元素类型是 char*\n");
    printf("  大小: %lu 字节 (5 * %lu)\n", sizeof(arr1), sizeof(char*));
    printf("  arr1+1 跳过: %lu 字节 (一个指针)\n", sizeof(char*));
    
    printf("\nchar (*arr2)[5]:\n");
    printf("  类型: 指针，指向 char[5]\n");
    printf("  大小: %lu 字节 (一个指针)\n", sizeof(arr2));
    printf("  arr2+1 跳过: 5 字节 (整个数组)\n");
}

int main() {
    array_of_pointers();
    pointer_to_array();
    compare_types();
    
    printf("\n=== 调试任务 ===\n");
    printf("1. 查看 names1 数组的内存布局\n");
    printf("2. 比较指针数组和数组指针的地址跳转\n");
    printf("3. 理解 argv (char **) 的内存结构\n");
    printf("4. 调试动态二维数组的两种实现\n");
    
    return 0;
}
