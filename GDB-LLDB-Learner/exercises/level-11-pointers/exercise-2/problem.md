# Exercise 2: 指针数组 vs 数组指针

## 学习目标

- 理解 `char *arr[]` (指针数组) 和 `char (*arr)[]` (数组指针) 的区别
- 掌握 `char **argv` 的内存结构
- 学习二维数组的两种实现方式
- 理解指针运算和 sizeof 的差异

## 背景知识

### 核心区别

```c
char *arr1[5];      // 指针数组：5个元素，每个元素是 char*
char (*arr2)[5];    // 数组指针：1个指针，指向 char[5]
```

### 优先级规则

```c
char *arr[5];       // [] 优先级高于 *
                    // 读法：arr 是数组，元素类型是 char*

char (*arr)[5];     // () 改变优先级
                    // 读法：arr 是指针，指向 char[5]
```

### 内存布局对比

**指针数组** (`char *arr[5]`):
```
栈上:
arr:    [ptr1][ptr2][ptr3][ptr4][ptr5]  // 5个指针，每个8字节(64位)
         |     |     |     |     |
堆/常量区: "A"  "B"  "C"  "D"  "E"
```

**数组指针** (`char (*arr)[5]`):
```
栈上:
arr: [ptr] → [c1][c2][c3][c4][c5]  // 1个指针，指向5个char
```

## 任务

### 任务 1: 检查指针数组的内存布局

**目标**: 理解指针数组的实际存储方式

**步骤**:
1. 在 `array_of_pointers()` 函数中设置断点
2. 检查 `names1` 的地址和大小
3. 查看每个元素的地址和内容
4. 验证 `sizeof(names1)` 的值

**问题**:
- `names1` 占用多少字节？
- `names1[0]` 的地址是什么？它指向什么？
- `names1[1]` 的地址与 `names1[0]` 相差多少字节？
- 字符串 "Alice" 存储在哪里？

### 任务 2: 理解数组指针

**目标**: 掌握数组指针的地址跳转

**步骤**:
1. 在 `pointer_to_array()` 函数中设置断点
2. 检查 `matrix` 的内存布局
3. 查看 `ptr` 和 `ptr+1` 的地址差
4. 理解为什么 `ptr+1` 跳过 16 字节

**问题**:
- `matrix` 占用多少字节？
- `ptr` 指向什么？
- `ptr+1` 相对于 `ptr` 跳过多少字节？为什么？
- `ptr[1][2]` 如何访问到正确的元素？

### 任务 3: 对比两种类型

**目标**: 深入理解类型差异

**步骤**:
1. 在 `compare_types()` 函数中设置断点
2. 比较 `sizeof(arr1)` 和 `sizeof(arr2)`
3. 理解指针运算的差异

**问题**:
- `arr1` 和 `arr2` 的 sizeof 分别是多少？
- `arr1+1` 跳过多少字节？
- `arr2+1` 跳过多少字节？
- 为什么会有这个差异？

### 任务 4: 调试动态分配的指针数组

**目标**: 理解 `char **argv` 类似的结构

**步骤**:
1. 断点在 `names2` 分配之后
2. 查看 `names2` 的二级指针结构
3. 遍历每个字符串
4. 检查内存分配情况

**问题**:
- `names2` 本身存储在哪里？
- `names2[0]`, `names2[1]`, `names2[2]` 存储在哪里？
- 字符串 "Apple", "Banana", "Cherry" 存储在哪里？
- 这与 `main(int argc, char **argv)` 的 argv 有何相似之处？

## 编译和运行

```bash
make
./arrays

# GDB
gdb ./arrays

# LLDB
lldb ./arrays
```

## 预期输出

```
=== 指针数组 (Array of Pointers) ===
names1 是指针数组，包含 4 个指针
names1 的大小: 32 字节 (4 个指针 * 8 字节/指针)
names1[0] = 0x..., 指向: "Alice"
names1[1] = 0x..., 指向: "Bob"
...

=== 数组指针 (Pointer to Array) ===
matrix 的大小: 48 字节
ptr 指向整行（4个int）
ptr 的地址: 0x...
ptr+1 的地址: 0x... (+16 字节)
...

=== 类型对比 ===
char *arr1[5]:
  类型: 数组，元素类型是 char*
  大小: 40 字节 (5 * 8)

char (*arr2)[5]:
  类型: 指针，指向 char[5]
  大小: 8 字节 (一个指针)
```

## 调试提示

### 查看指针数组

```bash
# GDB
(gdb) p names1
(gdb) p &names1[0]
(gdb) p names1[0]
(gdb) p *names1[0]@5    # 查看前5个字符
(gdb) x/4xg names1      # 查看4个指针（8字节每个）
```

### 查看数组指针

```bash
# GDB
(gdb) p matrix
(gdb) p ptr
(gdb) p ptr+1
(gdb) p (char*)(ptr+1) - (char*)ptr    # 地址差
(gdb) p ptr[0]          # 第一行
(gdb) p ptr[1][2]       # 第二行第三个元素
```

### 比较 sizeof

```bash
# GDB
(gdb) p sizeof(arr1)    # 数组的大小
(gdb) p sizeof(arr2)    # 指针的大小
(gdb) ptype arr1        # 查看类型
(gdb) ptype arr2
```

### 查看动态分配

```bash
# GDB
(gdb) p names2
(gdb) x/3xg names2      # 查看3个指针
(gdb) x/s names2[0]     # 查看第一个字符串
(gdb) x/s names2[1]
(gdb) x/s names2[2]
```

## 常见混淆点

### 1. 声明的读法

| 声明 | 读法 | 含义 |
|------|------|------|
| `char *arr[5]` | arr is an array of 5 pointers to char | 5个 char* |
| `char (*arr)[5]` | arr is a pointer to an array of 5 chars | 指向 char[5] 的指针 |
| `char **arr` | arr is a pointer to pointer to char | 二级指针 |

### 2. sizeof 的差异

```c
char *arr1[5];        // sizeof(arr1) = 5 * 8 = 40 (64位系统)
char (*arr2)[5];      // sizeof(arr2) = 8 (一个指针)
char **arr3;          // sizeof(arr3) = 8 (一个指针)
```

### 3. 指针运算

```c
char *arr1[5];
arr1 + 1;             // 跳过 sizeof(char*) = 8 字节

char (*arr2)[5];
arr2 + 1;             // 跳过 sizeof(char[5]) = 5 字节
```

## 实际应用场景

### 1. main 函数的 argv

```c
int main(int argc, char **argv) {
    // argv 是指针数组（严格来说是指向指针的指针）
    // argv[0], argv[1], ... 每个都是 char*
    // 类似于 names2 的结构
}
```

### 2. 动态二维数组

**方法1: 指针数组** (不连续)
```c
char **matrix = malloc(rows * sizeof(char*));
for (int i = 0; i < rows; i++) {
    matrix[i] = malloc(cols * sizeof(char));
}
```

**方法2: 数组指针** (连续)
```c
char (*matrix)[cols] = malloc(rows * sizeof(*matrix));
```

### 3. 字符串数组

```c
char *days[] = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};
// 指针数组，存储7个字符串字面量的地址
```

## 扩展挑战

1. **模拟 argv**: 创建一个类似 `char **argv` 的结构，手动填充命令行参数
2. **二维数组访问**: 用两种方法实现矩阵访问，比较性能
3. **内存可视化**: 画出完整的内存布局图
4. **指针转换**: 尝试在两种类型之间转换（理解为什么不能）

## 相关知识点

- **Level 7** (内存): 查看内存布局
- **Level 11 Exercise 1**: 多级指针（理解 char **）
- **Level 12**: 数组的内存对齐

## 调试检查清单

- [ ] 验证指针数组中每个指针的地址
- [ ] 计算数组指针的地址跳转
- [ ] 比较 sizeof 的不同结果
- [ ] 画出动态分配的内存图
- [ ] 理解 argv 的实际结构
- [ ] 掌握两种二维数组的差异

## 总结

完成本练习后，你应该能够：

1. ✅ 正确读出复杂指针声明
2. ✅ 区分指针数组和数组指针
3. ✅ 理解指针运算的步长
4. ✅ 掌握 argv 的内存结构
5. ✅ 选择合适的二维数组实现方式

记住：**[] 的优先级高于 \***，括号可以改变优先级！
