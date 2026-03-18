# Exercise 2: 指针数组 vs 数组指针 - 参考答案

## 完整调试会话

### GDB 调试会话

```bash
$ gdb ./arrays
(gdb) break array_of_pointers
Breakpoint 1 at 0x401169: file arrays.c, line 6.

(gdb) run
Starting program: ./arrays

Breakpoint 1, array_of_pointers () at arrays.c:6

# ========== 任务 1: 检查指针数组的内存布局 ==========

(gdb) n
9           char *names1[] = {"Alice", "Bob", "Charlie", "David"};

(gdb) n
11          printf("names1 是指针数组，包含 %lu 个指针\n", ...);

# 查看 names1 的地址和大小
(gdb) p names1
$1 = {0x402004 "Alice", 0x40200a "Bob", 0x40200e "Charlie", 0x402016 "David"}

(gdb) p &names1
$2 = (char *(*)[4]) 0x7fffffffe060

(gdb) p sizeof(names1)
$3 = 32

# names1 是数组，占 32 字节 = 4个指针 * 8字节/指针

# 查看每个元素
(gdb) p names1[0]
$4 = 0x402004 "Alice"

(gdb) p &names1[0]
$5 = (char **) 0x7fffffffe060

(gdb) p names1[1]
$6 = 0x40200a "Bob"

(gdb) p &names1[1]
$7 = (char **) 0x7fffffffe068

# 地址差 = 0x68 - 0x60 = 8 字节（一个指针的大小）

(gdb) p (char*)&names1[1] - (char*)&names1[0]
$8 = 8

# 查看内存布局（4个指针）
(gdb) x/4xg &names1[0]
0x7fffffffe060: 0x0000000000402004  0x000000000040200a
0x7fffffffe070: 0x000000000040200e  0x0000000000402016

# 这4个值就是指向字符串的指针

# 查看字符串实际存储位置
(gdb) x/s 0x402004
0x402004: "Alice"

(gdb) x/s 0x40200a
0x40200a: "Bob"

# 字符串存储在只读数据段（常量区）

# 检查类型
(gdb) ptype names1
type = char *[4]
# 读作：names1 是一个包含4个 char* 的数组

# 动态分配的指针数组 (names2)
(gdb) n
...
20          char **names2 = malloc(3 * sizeof(char*));

(gdb) until 24
array_of_pointers () at arrays.c:25

(gdb) p names2
$9 = (char **) 0x405260

(gdb) p sizeof(names2)
$10 = 8
# names2 本身是指针，大小是8字节

# 查看 names2 指向的内存（3个指针）
(gdb) x/3xg names2
0x405260: 0x0000000000405280  0x00000000004052a0  0x00000000004052c0

# 查看每个字符串
(gdb) x/s 0x405280
0x405280: "Apple"

(gdb) x/s 0x4052a0
0x4052a0: "Banana"

(gdb) x/s 0x4052c0
0x4052c0: "Cherry"

# 内存布局：
# 栈: names2 → 0x405260 (堆)
# 堆: [ptr1][ptr2][ptr3]
#      |     |     |
#     "Apple" "Banana" "Cherry"

# ========== 任务 2: 理解数组指针 ==========

(gdb) break pointer_to_array
Breakpoint 2 at 0x4012e9: file arrays.c, line 36.

(gdb) continue
=== 指针数组 (Array of Pointers) ===
names1 是指针数组，包含 4 个指针
...

Breakpoint 2, pointer_to_array () at arrays.c:36

(gdb) n
...
45          int (*ptr)[4] = matrix;

(gdb) n
47          printf("matrix 的大小: %lu 字节\n", sizeof(matrix));

# 查看 matrix
(gdb) p matrix
$11 = {{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}}

(gdb) p &matrix
$12 = (int (*)[3][4]) 0x7fffffffe040

(gdb) p sizeof(matrix)
$13 = 48
# 3行 * 4列 * 4字节/int = 48 字节

# 查看内存（连续存储）
(gdb) x/12dw &matrix[0][0]
0x7fffffffe040: 1  2  3  4  5  6  7  8  9  10 11 12

# 检查 ptr
(gdb) p ptr
$14 = (int (*)[4]) 0x7fffffffe040

(gdb) ptype ptr
type = int (*)[4]
# ptr 是指向 int[4] 的指针

(gdb) p ptr+0
$15 = (int (*)[4]) 0x7fffffffe040

(gdb) p ptr+1
$16 = (int (*)[4]) 0x7fffffffe050

# 地址差
(gdb) p (char*)(ptr+1) - (char*)ptr
$17 = 16
# 跳过 16 字节 = 4个int * 4字节 = sizeof(int[4])

(gdb) p ptr+2
$18 = (int (*)[4]) 0x7fffffffe060

(gdb) p (char*)(ptr+2) - (char*)ptr
$19 = 32

# 访问元素
(gdb) p ptr[0]
$20 = {1, 2, 3, 4}
# ptr[0] 是第一行

(gdb) p ptr[1]
$21 = {5, 6, 7, 8}

(gdb) p ptr[1][2]
$22 = 7
# 第二行第三个元素

# ptr[1][2] 等价于 *((ptr+1)[0] + 2)
# 等价于 *(*(ptr+1) + 2)

# ========== 任务 3: 对比两种类型 ==========

(gdb) break compare_types
Breakpoint 3 at 0x4013e9: file arrays.c, line 63.

(gdb) continue
...

Breakpoint 3, compare_types () at arrays.c:63

(gdb) n
...
66          char (*arr2)[5];

(gdb) n
68          printf("char *arr1[5]:\n");

# 比较大小
(gdb) p sizeof(arr1)
$23 = 40
# 5 个指针 * 8 字节 = 40

(gdb) p sizeof(arr2)
$24 = 8
# 1 个指针 = 8 字节

# 检查类型
(gdb) ptype arr1
type = char *[5]
# arr1 是数组，元素是 char*

(gdb) ptype arr2
type = char (*)[5]
# arr2 是指针，指向 char[5]

# 指针运算
(gdb) p &arr1[0]
$25 = (char **) 0x7fffffffe010

(gdb) p &arr1[1]
$26 = (char **) 0x7fffffffe018

(gdb) p (char*)&arr1[1] - (char*)&arr1[0]
$27 = 8
# arr1+1 跳过 8 字节（一个 char* 指针）

# 如果 arr2 指向某个数组
(gdb) set arr2 = &"hello"
(gdb) p arr2
$28 = (char (*)[5]) 0x402020

(gdb) p arr2+1
$29 = (char (*)[5]) 0x402025

(gdb) p (char*)(arr2+1) - (char*)arr2
$30 = 5
# arr2+1 跳过 5 字节（整个 char[5] 数组）

# 关键差异：
# arr1 是数组，arr1+1 跳过一个元素（char*）
# arr2 是指针，arr2+1 跳过它指向的类型（char[5]）

# ========== 任务 4: 深入理解 argv 结构 ==========

# 返回到 names2 的分析
(gdb) break 25
Breakpoint 4 at 0x4012af: file arrays.c, line 25.

(gdb) run
...
Breakpoint 4, array_of_pointers () at arrays.c:25

(gdb) p names2
$31 = (char **) 0x405260

# names2 本身存储在栈上
(gdb) p &names2
$32 = (char ***) 0x7fffffffe038
# 栈地址

# names2 指向的数组在堆上
(gdb) p names2
$33 = (char **) 0x405260
# 堆地址

# 画出内存图
(gdb) define show_argv
    set $i = 0
    while $i < $argc
        printf "argv[%d] @ %p → %p → \"%s\"\n", $i, &$arg0[$i], $arg0[$i], $arg0[$i]
        set $i = $i + 1
    end
end

# 模拟 argv
(gdb) set $argc = 3
(gdb) show_argv names2
argv[0] @ 0x405260 → 0x405280 → "Apple"
argv[1] @ 0x405268 → 0x4052a0 → "Banana"
argv[2] @ 0x405270 → 0x4052c0 → "Cherry"

# 内存可视化：
# 栈:
#   names2 @ 0x7fffffffe038: [0x405260]
#                              |
# 堆:                          v
#   @ 0x405260: [0x405280][0x4052a0][0x4052c0]
#                  |        |        |
#                  v        v        v
#   @ 0x405280: "Apple\0"
#   @ 0x4052a0: "Banana\0"
#   @ 0x4052c0: "Cherry\0"

# 这与 main(int argc, char **argv) 完全相同！
```

### LLDB 调试会话

```bash
$ lldb ./arrays
(lldb) target create "./arrays"

(lldb) b array_of_pointers
Breakpoint 1: where = arrays`array_of_pointers + 13

(lldb) run
Process 1234 launched: './arrays'

Process 1234 stopped

# ========== 任务 1: 检查指针数组 ==========

(lldb) n
(lldb) n
# 到达 names1 定义之后

(lldb) frame variable names1
(char *[4]) names1 = {
  [0] = 0x0000000000402004 "Alice"
  [1] = 0x000000000040200a "Bob"
  [2] = 0x000000000040200e "Charlie"
  [3] = 0x0000000000402016 "David"
}

(lldb) expr sizeof(names1)
(unsigned long) $0 = 32

(lldb) memory read --size 8 --count 4 --format x `&names1`
0x7fffffffe060: 0x0000000000402004 0x000000000040200a
0x7fffffffe070: 0x000000000040200e 0x0000000000402016

(lldb) memory read --format s 0x402004
0x00402004: "Alice"

(lldb) type lookup char *[4]
# (未支持，使用 frame variable)

# 动态分配的 names2
(lldb) n
...
(lldb) until 25

(lldb) expr names2
(char **) $1 = 0x0000000000405260

(lldb) memory read --size 8 --count 3 --format x `names2`
0x00405260: 0x0000000000405280 0x00000000004052a0
0x00405270: 0x00000000004052c0

(lldb) memory read --format s 0x405280
0x00405280: "Apple"

# ========== 任务 2: 理解数组指针 ==========

(lldb) b pointer_to_array
Breakpoint 2: where = arrays`pointer_to_array + 13

(lldb) continue
Process 1234 resuming
...

Process 1234 stopped

(lldb) n
...
# 到达 ptr 定义之后

(lldb) expr matrix
(int [3][4]) $2 = {
  [0] = ([0] = 1, [1] = 2, [2] = 3, [3] = 4)
  [1] = ([0] = 5, [1] = 6, [2] = 7, [3] = 8)
  [2] = ([0] = 9, [1] = 10, [2] = 11, [3] = 12)
}

(lldb) expr sizeof(matrix)
(unsigned long) $3 = 48

(lldb) expr ptr
(int (*)[4]) $4 = 0x00007fffffffe040

(lldb) expr ptr+1
(int (*)[4]) $5 = 0x00007fffffffe050

(lldb) expr (char*)(ptr+1) - (char*)ptr
(long) $6 = 16

# 跳过16字节 = sizeof(int[4])

(lldb) expr ptr[1][2]
(int) $7 = 7

# ========== 任务 3: 对比类型 ==========

(lldb) b compare_types
Breakpoint 3: where = arrays`compare_types + 13

(lldb) continue
...

(lldb) n
...

(lldb) expr sizeof(arr1)
(unsigned long) $8 = 40
# 5个指针

(lldb) expr sizeof(arr2)
(unsigned long) $9 = 8
# 1个指针

(lldb) type lookup -- 'char *[5]'
# arr1 的类型

(lldb) type lookup -- 'char (*)[5]'
# arr2 的类型

# ========== 内存可视化脚本 ==========

(lldb) script
>>> # 可视化 argv 类似结构
>>> def show_string_array(debugger, command, result, internal_dict):
...     frame = debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame()
...     arr = frame.FindVariable(command)
...     count = 3  # 假设3个元素
...     for i in range(count):
...         ptr = arr.GetChildAtIndex(i)
...         addr = ptr.GetValueAsUnsigned()
...         cmd_result = lldb.SBCommandReturnObject()
...         debugger.GetCommandInterpreter().HandleCommand(
...             f"memory read --format s {addr}", cmd_result)
...         print(f"[{i}] @ {hex(addr)}: {cmd_result.GetOutput().strip()}")
...
>>> lldb.debugger.HandleCommand('command script add -f __main__.show_string_array show_strings')
>>> quit()

(lldb) show_strings names2
[0] @ 0x405280: 0x00405280: "Apple"
[1] @ 0x4052a0: 0x004052a0: "Banana"
[2] @ 0x4052c0: 0x004052c0: "Cherry"

(lldb) quit
```

## 答案总结

### 任务 1: 指针数组的内存布局

#### names1 (静态指针数组)

| 问题 | 答案 |
|------|------|
| 占用多少字节？ | 32 字节 (4 × 8) |
| names1[0] 的地址 | 0x7fffffffe060 (栈上) |
| names1[0] 指向什么 | 0x402004 → "Alice" (常量区) |
| 相邻指针地址差 | 8 字节 |
| 字符串存储位置 | 只读数据段(.rodata) |

**内存图**:
```
栈 (0x7fffffffe060):
names1: [0x402004][0x40200a][0x40200e][0x402016]
           |         |         |         |
常量区:    "Alice"  "Bob"  "Charlie"  "David"
```

#### names2 (动态指针数组)

| 组件 | 地址 | 位置 |
|------|------|------|
| names2 变量 | 0x7fffffffe038 | 栈 |
| 指针数组 | 0x405260 | 堆 |
| "Apple" | 0x405280 | 堆 |
| "Banana" | 0x4052a0 | 堆 |
| "Cherry" | 0x4052c0 | 堆 |

**内存图**:
```
栈:
  names2: [0x405260] ----+
                         |
堆:                      v
  0x405260: [0x405280][0x4052a0][0x4052c0]
               |         |         |
               v         v         v
            "Apple"  "Banana"  "Cherry"
```

**与 argv 的相似性**:
```c
int main(int argc, char **argv) {
    // argv 的结构与 names2 完全相同
    // argv[0], argv[1], ... 都是 char*
    // argv 本身是 char**
}
```

### 任务 2: 数组指针

| 问题 | 答案 |
|------|------|
| matrix 占用字节 | 48 字节 (3×4×4) |
| ptr 指向什么 | 第一行 (int[4]) |
| ptr+1 地址差 | 16 字节 = sizeof(int[4]) |
| ptr[1][2] 访问 | *(*(ptr+1)+2) = 7 |

**指针运算解释**:
```c
ptr       → matrix[0] → {1, 2, 3, 4}
ptr + 1   → matrix[1] → {5, 6, 7, 8}   // 跳过 16 字节
ptr + 2   → matrix[2] → {9, 10, 11, 12}
```

**元素访问**:
```c
ptr[1][2]
= (*(ptr+1))[2]
= *((*(ptr+1)) + 2)
= *(matrix[1] + 2)
= matrix[1][2]
= 7
```

### 任务 3: 类型对比

| 特性 | `char *arr1[5]` | `char (*arr2)[5]` |
|------|-----------------|-------------------|
| 类型 | 数组 | 指针 |
| 元素类型 | char* | 指向 char[5] |
| sizeof | 40 字节 (5×8) | 8 字节 |
| arr+1 跳过 | 8 字节 | 5 字节 |
| 读法 | 5个char指针的数组 | 指向5个char数组的指针 |

**优先级规则**:
```c
char *arr[5];     // [] 优先级高，先看 arr[5]，再看 *
                  // arr 是数组，元素是 char*

char (*arr)[5];   // () 改变优先级，先看 *arr
                  // arr 是指针，指向 char[5]
```

### 任务 4: argv 结构

**完整内存布局**:
```
main() 栈帧:
  argc: 3
  argv: [ptr] @ 0x7fffffffe0a8
          |
          v
  堆/其他内存段: [ptr0][ptr1][ptr2][NULL] @ 0x405260
                   |     |     |
                   v     v     v
                "Apple" "Banana" "Cherry"
```

**三层结构**:
1. `argv` 本身 (char***): 指向指针数组
2. `argv[i]` (char**): 指向字符串
3. `argv[i][j]` (char): 字符串中的字符

**访问方式**:
```c
argv        // char** (指向指针数组)
argv[0]     // char*  (第一个字符串的地址)
argv[0][0]  // char   ('A')
*argv[0]    // char   ('A')
**argv      // char   ('A')
```

## 核心调试技巧

### 1. 查看多级指针结构

```bash
# GDB
(gdb) p argv                 # 第一层：char**
(gdb) p argv[0]              # 第二层：char*
(gdb) p argv[0][0]           # 第三层：char
(gdb) x/3xg argv             # 查看3个指针
(gdb) x/s argv[0]            # 查看字符串

# LLDB
(lldb) expr argv
(lldb) expr argv[0]
(lldb) memory read --size 8 --count 3 --format x `argv`
(lldb) memory read --format s `argv[0]`
```

### 2. 计算地址差

```bash
# GDB
(gdb) p (char*)&arr[1] - (char*)&arr[0]
(gdb) p (char*)(ptr+1) - (char*)ptr

# LLDB
(lldb) expr (char*)&arr[1] - (char*)&arr[0]
```

### 3. 查看类型信息

```bash
# GDB
(gdb) ptype arr1
(gdb) whatis arr1

# LLDB
(lldb) frame variable --show-types arr1
```

### 4. 遍历字符串数组

```bash
# GDB
set $i = 0
while $i < 3
    printf "argv[%d] = %s\n", $i, argv[$i]
    set $i = $i + 1
end

# LLDB (使用 Python)
script
for i in range(3):
    print(f"argv[{i}] = {lldb.frame.FindVariable('argv').GetChildAtIndex(i).GetSummary()}")
```

## 实际应用示例

### 1. 解析命令行参数

```c
int main(int argc, char **argv) {
    // argv 是指针数组
    printf("Program: %s\n", argv[0]);
    for (int i = 1; i < argc; i++) {
        printf("Arg %d: %s\n", i, argv[i]);
    }
    return 0;
}
```

### 2. 动态二维数组 (方法对比)

**方法1: 指针数组 (灵活，不连续)**
```c
char **matrix = malloc(rows * sizeof(char*));
for (int i = 0; i < rows; i++) {
    matrix[i] = malloc(cols * sizeof(char));
}
// 优点：每行可以有不同长度
// 缺点：内存不连续，两次分配
```

**方法2: 数组指针 (高效，连续)**
```c
char (*matrix)[cols] = malloc(rows * sizeof(*matrix));
// 优点：一次分配，内存连续，缓存友好
// 缺点：cols 必须是编译时常量（或使用 VLA）
```

### 3. 字符串列表

```c
char *fruits[] = {
    "Apple",
    "Banana",
    "Cherry",
    NULL  // 结束标记
};

// 遍历
for (char **p = fruits; *p != NULL; p++) {
    printf("%s\n", *p);
}
```

## 常见陷阱

### 1. 混淆指针数组和数组指针

```c
char *arr1[5];    // ✓ 正确：5个指针
char (*arr2)[5];  // ✓ 正确：1个指针，指向5个char

char* arr3[5];    // ✓ 同 arr1（风格不同）
char *[5]arr4;    // ✗ 错误：语法错误
```

### 2. sizeof 陷阱

```c
void func(char *arr[]) {
    // arr 在这里退化为 char**
    printf("%lu\n", sizeof(arr));  // 输出 8，不是数组大小！
}

char *arr[10];
func(arr);  // 传递的是指针，不是数组
```

### 3. 指针运算错误

```c
char *arr[5];
arr + 1;      // ✓ 跳过 sizeof(char*) = 8 字节

char (*ptr)[5];
ptr + 1;      // ✓ 跳过 sizeof(char[5]) = 5 字节

char **p;
p + 1;        // ✓ 跳过 sizeof(char*) = 8 字节
```

## 总结检查清单

完成本练习后，你应该能够回答：

- [x] `char *arr[]` 和 `char (*arr)[]` 的区别是什么？
  - **答**: 前者是指针数组，后者是数组指针

- [x] `sizeof` 对两种类型返回什么？
  - **答**: 指针数组返回数组大小，数组指针返回指针大小(8字节)

- [x] 指针运算 `+1` 跳过多少字节？
  - **答**: 取决于指针指向的类型大小

- [x] `argv` 的实际内存结构是什么？
  - **答**: 三层结构：argv → 指针数组 → 字符串

- [x] 如何在调试器中可视化多级指针？
  - **答**: 逐层解引用，使用 x/xg 查看指针，x/s 查看字符串

- [x] 两种二维数组实现的优缺点是什么？
  - **答**: 指针数组灵活但不连续；数组指针连续但大小固定

**关键要点**:
1. **优先级**: `[]` > `*`，括号改变优先级
2. **sizeof**: 数组是整体大小，指针是8字节
3. **指针运算**: 步长是指向类型的大小
4. **argv**: 理解三层间接访问
5. **内存布局**: 栈vs堆，连续vs分散

掌握这些概念后，复杂指针声明将不再是难题！
