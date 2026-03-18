# Level 11: 多级指针调试专题

## 学习目标

- 深入理解一级、二级、三级指针的内存布局
- 掌握指针数组 vs 数组指针的区别
- 学习调试函数指针和函数指针数组
- 理解指针在编译器视角下的实现
- 掌握复杂指针声明的解读

## 为什么要学习多级指针？

多级指针在系统编程中无处不在：
- **二级指针**: 动态二维数组、字符串数组（`char **argv`）、链表节点的修改
- **三级指针**: 复杂数据结构、动态三维数组、指针数组的指针
- **函数指针**: 回调函数、策略模式、虚函数表

## 指针层次解析

### 一级指针 (T *)

```c
int value = 42;
int *ptr = &value;

内存布局:
┌─────────────┐
│   value     │  0x1000: [42]
└─────────────┘
      ↑
      │
┌─────────────┐
│    ptr      │  0x2000: [0x1000]
└─────────────┘
```

### 二级指针 (T **)

```c
int value = 42;
int *ptr = &value;
int **ptr_ptr = &ptr;

内存布局:
┌─────────────┐
│   value     │  0x1000: [42]
└─────────────┘
      ↑
┌─────────────┐
│    ptr      │  0x2000: [0x1000]
└─────────────┘
      ↑
┌─────────────┐
│  ptr_ptr    │  0x3000: [0x2000]
└─────────────┘
```

### 三级指针 (T ***)

```c
int value = 42;
int *p1 = &value;
int **p2 = &p1;
int ***p3 = &p2;

内存布局:
┌─────────────┐
│   value     │  0x1000: [42]
└─────────────┘
      ↑
┌─────────────┐
│     p1      │  0x2000: [0x1000]
└─────────────┘
      ↑
┌─────────────┐
│     p2      │  0x3000: [0x2000]
└─────────────┘
      ↑
┌─────────────┐
│     p3      │  0x4000: [0x3000]
└─────────────┘
```

## 指针数组 vs 数组指针

### 指针数组 (Array of Pointers)

```c
int *arr[5];  // 5 个 int* 的数组

┌──────┬──────┬──────┬──────┬──────┐
│ ptr0 │ ptr1 │ ptr2 │ ptr3 │ ptr4 │
└──┬───┴──┬───┴──┬───┴──┬───┴──┬───┘
   │      │      │      │      │
   ↓      ↓      ↓      ↓      ↓
  int    int    int    int    int
```

### 数组指针 (Pointer to Array)

```c
int (*ptr)[5];  // 指向 int[5] 数组的指针

        ┌──────────────────────────┐
  ptr ──┤                          │
        ↓                          │
┌──────┬──────┬──────┬──────┬──────┐
│ int  │ int  │ int  │ int  │ int  │
└──────┴──────┴──────┴──────┴──────┘
```

## GDB/LLDB 调试技巧

### 1. 查看指针链

**GDB:**
```c
int value = 42;
int *p1 = &value;
int **p2 = &p1;
int ***p3 = &p2;

(gdb) print value
$1 = 42

(gdb) print p1
$2 = (int *) 0x7fffffffddf4  # 指向 value 的地址

(gdb) print *p1
$3 = 42  # 解引用得到 value

(gdb) print p2
$4 = (int **) 0x7fffffffddf8  # 指向 p1 的地址

(gdb) print *p2
$5 = (int *) 0x7fffffffddf4  # 解引用得到 p1 的值（value 的地址）

(gdb) print **p2
$6 = 42  # 二次解引用得到 value

(gdb) print p3
$7 = (int ***) 0x7fffffffe000

(gdb) print ***p3
$8 = 42  # 三次解引用
```

### 2. 查看内存布局

```bash
# 查看整个指针链的内存
(gdb) x/gx &value   # value 的内存
0x7fffffffddf4: 0x000000000000002a  # 42 (0x2a)

(gdb) x/gx &p1      # p1 的内存（存储 value 的地址）
0x7fffffffddf8: 0x00007fffffffddf4

(gdb) x/gx &p2      # p2 的内存（存储 p1 的地址）
0x7fffffffe000: 0x00007fffffffddf8

(gdb) x/gx &p3      # p3 的内存（存储 p2 的地址）
0x7fffffffe008: 0x00007fffffffe000
```

### 3. 指针数组调试

```c
char *names[] = {"Alice", "Bob", "Charlie"};

(gdb) print names
$1 = {0x555555556004 "Alice", 0x55555555600a "Bob", 0x55555555600e "Charlie"}

(gdb) print names[0]
$2 = 0x555555556004 "Alice"

(gdb) print *names[0]
$3 = 65 'A'

(gdb) x/s names[0]
0x555555556004: "Alice"

# 查看整个数组的内存布局
(gdb) x/3gx names  # 3 个指针
0x7fffffffdde0: 0x0000555555556004  0x000055555555600a
0x7fffffffddf0: 0x000055555555600e
```

### 4. 函数指针调试

```c
int add(int a, int b) { return a + b; }
int (*func_ptr)(int, int) = add;

(gdb) print func_ptr
$1 = (int (*)(int, int)) 0x555555555149 <add>

(gdb) print func_ptr(5, 3)
$2 = 8

# 查看函数指针数组
int (*ops[])(int, int) = {add, sub, mul};

(gdb) print ops
$3 = {0x555555555149 <add>, 0x555555555160 <sub>, 0x555555555177 <mul>}

(gdb) print ops[0](10, 5)
$4 = 15
```

## 练习列表

### Exercise 1: 一级、二级、三级指针
**难度**: ⭐⭐⭐

深入理解多级指针的内存布局，学习如何在调试器中追踪指针链。

**技能点**:
- 打印各级指针的地址和值
- 查看连续的内存布局
- 理解解引用的层次
- 修改深层指针指向的值

### Exercise 2: 指针数组与数组指针
**难度**: ⭐⭐⭐⭐

区分两种容易混淆的指针类型，理解它们在内存中的不同表现。

**技能点**:
- `char *arr[]` vs `char (*arr)[]`
- 动态二维数组的两种实现
- `argv` 的内存布局
- 矩阵的指针访问

### Exercise 3: 函数指针与回调
**难度**: ⭐⭐⭐⭐

学习调试函数指针、函数指针数组和回调函数。

**技能点**:
- 函数指针的声明和使用
- 函数指针数组（跳转表）
- 回调函数的调试
- 虚函数表的原理

## 常见陷阱

### 1. 指针声明陷阱

```c
int* p1, p2;  // p1 是指针，p2 是 int!
int *p1, *p2; // 正确：都是指针

int *arr[10];   // 指针数组：10 个 int*
int (*arr)[10]; // 数组指针：指向 int[10]
```

### 2. 二级指针与动态数组

```c
// 错误示例
int **matrix = malloc(rows * sizeof(int*));  // 只分配了指针数组
// 忘记为每一行分配内存！

// 正确示例
int **matrix = malloc(rows * sizeof(int*));
for (int i = 0; i < rows; i++) {
    matrix[i] = malloc(cols * sizeof(int));
}
```

### 3. 函数指针声明

```c
int (*func)(int, int);    // 函数指针
int *func(int, int);      // 返回 int* 的函数
int *(func(int, int));    // 同上（多余括号）
int (*func[10])(int);     // 函数指针数组
```

## 调试技巧总结

1. **逐层解引用**: 使用多个 `print *` 或 `print **`
2. **查看地址**: 使用 `print &variable`
3. **内存可视化**: 使用 `x` 命令查看连续内存
4. **类型信息**: 使用 `ptype` 查看复杂类型
5. **追踪指针链**: 手动或脚本化遍历多级指针

## 快速参考

| 类型 | 声明 | 含义 | 示例 |
|------|------|------|------|
| 一级指针 | `int *p` | 指向 int | `p` 存储 int 的地址 |
| 二级指针 | `int **p` | 指向 int* | `p` 存储指针的地址 |
| 三级指针 | `int ***p` | 指向 int** | 三层间接引用 |
| 指针数组 | `int *arr[N]` | N 个指针 | `argv` 是 `char *[]` |
| 数组指针 | `int (*p)[N]` | 指向数组 | `p` 指向 int[N] |
| 函数指针 | `int (*f)(int)` | 指向函数 | 回调函数 |

## 实战应用

1. **命令行参数**: `int main(int argc, char **argv)`
2. **动态二维数组**: `int **matrix`
3. **链表修改**: `void insert(Node **head)`
4. **回调机制**: `void qsort(..., int (*cmp)(...))`
5. **虚函数表**: C++ 对象的 vtable

完成这个级别后，你将能够：
- ✅ 快速理解任何复杂的指针声明
- ✅ 在调试器中追踪多级指针
- ✅ 调试动态多维数组
- ✅ 理解函数指针的工作原理
- ✅ 掌握指针在内存中的实际布局
