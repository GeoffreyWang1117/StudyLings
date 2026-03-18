# Exercise 3: 函数指针与回调机制

## 学习目标

- 理解函数指针的声明和使用
- 掌握 typedef 简化函数指针
- 学习函数指针数组（跳转表）
- 理解回调函数机制
- 探索虚函数表的原理

## 背景知识

### 函数指针基础

```c
// 函数
int add(int a, int b) {
    return a + b;
}

// 函数指针声明
int (*fp)(int, int);        // fp 是函数指针

// 赋值和调用
fp = add;                    // 或 fp = &add;
int result = fp(2, 3);      // 或 (*fp)(2, 3);
```

### 声明解析

```c
int (*fp)(int, int);
// 读法：fp 是指针，指向一个函数
//       该函数接受两个 int 参数，返回 int

int *fp(int, int);
// 读法：fp 是函数，接受两个 int 参数，返回 int*
//       (完全不同的含义！)
```

### typedef 简化

```c
typedef int (*Operation)(int, int);

// 现在可以这样使用
Operation op1 = add;
Operation op2 = sub;
Operation ops[3] = {add, sub, mul};
```

### 内存模型

```
代码段(.text):
  add:  [指令...]  @ 0x401146
  sub:  [指令...]  @ 0x401155
  mul:  [指令...]  @ 0x401164

栈:
  op:   [0x401146]  // 指向 add 函数
  ops:  [0x401146][0x401155][0x401164]  // 函数指针数组
```

## 任务

### 任务 1: 检查函数指针的值

**目标**: 理解函数指针存储的是什么

**步骤**:
1. 在 `main()` 函数中设置断点
2. 查看函数 `add`, `sub`, `mul` 的地址
3. 检查函数指针 `op` 的值
4. 验证函数指针指向代码段

**问题**:
- `add` 函数的地址是多少？
- 函数指针 `op` 存储的值是什么？
- 函数指针本身存储在哪里（栈/堆/代码段）？
- 函数指针指向的函数在哪里？

### 任务 2: 查看函数指针数组

**目标**: 理解跳转表的实现

**步骤**:
1. 断点在函数指针数组初始化之后
2. 打印 `ops` 数组
3. 查看每个元素的值
4. 使用 disassemble 查看函数代码

**问题**:
- `ops` 数组占用多少字节？
- `ops[0]`, `ops[1]`, `ops[2]` 分别指向哪里？
- 如何通过 `ops[1](10, 5)` 调用 `sub` 函数？
- 数组中存储的是函数地址还是函数本身？

### 任务 3: 追踪回调函数调用

**目标**: 理解回调机制

**步骤**:
1. 在 `callback_example()` 函数上设置断点
2. 查看参数 `op` 的值
3. 单步进入 `op(x, y)` 调用
4. 观察程序如何跳转到实际函数

**问题**:
- 回调函数的地址是如何传递的？
- `op` 参数在栈帧中的位置？
- 调用 `op(x, y)` 时，CPU 如何知道跳转到哪里？
- 回调和直接函数调用有什么不同？

### 任务 4: 反汇编分析

**目标**: 理解函数指针调用的底层机制

**步骤**:
1. 使用 `disassemble` 查看 `callback_example` 的汇编
2. 找到 `op(x, y)` 的调用指令
3. 比较直接调用和间接调用的汇编差异

**问题**:
- 直接调用（如 `add(5, 3)`）使用什么指令？
- 间接调用（如 `op(x, y)`）使用什么指令？
- 为什么间接调用更慢？

## 编译和运行

```bash
make
./funcptr

# GDB
gdb ./funcptr

# LLDB
lldb ./funcptr
```

## 预期输出

```
=== 函数指针演示 ===

函数指针 op 指向: 0x401146 (add 函数)
调用 op(5, 3) = 8

函数指针数组:
ops[0] = 0x401146 (add)
ops[1] = 0x401155 (sub)
ops[2] = 0x401164 (mul)

使用回调函数:
add(10, 5) = 15
sub(10, 5) = 5
mul(10, 5) = 50

任务: 使用调试器查看函数指针的地址和类型
```

## 调试提示

### 查看函数地址

```bash
# GDB
(gdb) p add
(gdb) p &add
(gdb) p sub
(gdb) p mul

# LLDB
(lldb) expr add
(lldb) expr &add
```

### 查看函数指针

```bash
# GDB
(gdb) p op
(gdb) ptype op
(gdb) x/i op       # 查看函数入口的指令

# LLDB
(lldb) frame variable op
(lldb) memory read --format i `op`
```

### 查看函数指针数组

```bash
# GDB
(gdb) p ops
(gdb) p ops[0]
(gdb) x/3xg ops    # 查看3个指针

# LLDB
(lldb) expr ops
(lldb) memory read --size 8 --count 3 --format x `ops`
```

### 反汇编函数

```bash
# GDB
(gdb) disassemble add
(gdb) disassemble callback_example

# LLDB
(lldb) disassemble --name add
(lldb) disassemble --name callback_example
```

### 单步进入回调

```bash
# GDB
(gdb) break callback_example
(gdb) run
(gdb) p op
(gdb) step        # 进入 op(x, y)

# LLDB
(lldb) b callback_example
(lldb) run
(lldb) step
```

## 扩展练习

### 1. 构造函数指针表

创建一个计算器，使用函数指针数组实现操作符查找：

```c
typedef struct {
    char op;
    Operation func;
} OpEntry;

OpEntry table[] = {
    {'+', add},
    {'-', sub},
    {'*', mul}
};

// 查找并调用
for (int i = 0; i < 3; i++) {
    if (table[i].op == user_input) {
        result = table[i].func(a, b);
    }
}
```

### 2. 实现虚函数表（C++ vtable 原理）

```c
typedef struct {
    void (*draw)();
    void (*move)();
} ShapeVTable;

typedef struct {
    ShapeVTable *vtable;
    int x, y;
} Shape;

// 模拟多态调用
void draw_shape(Shape *s) {
    s->vtable->draw();  // 虚函数调用
}
```

### 3. qsort 比较函数

```c
int compare(const void *a, const void *b) {
    return *(int*)a - *(int*)b;
}

int arr[] = {3, 1, 4, 1, 5};
qsort(arr, 5, sizeof(int), compare);
// 使用调试器观察 compare 如何被回调
```

## 应用场景

### 1. 策略模式

```c
typedef int (*SortStrategy)(int[], int);

SortStrategy strategies[] = {
    bubble_sort,
    quick_sort,
    merge_sort
};

// 运行时选择算法
strategies[user_choice](array, size);
```

### 2. 事件处理

```c
typedef void (*EventHandler)(Event*);

void register_handler(EventType type, EventHandler handler) {
    handlers[type] = handler;
}

void dispatch_event(Event *e) {
    handlers[e->type](e);  // 回调注册的处理函数
}
```

### 3. 状态机

```c
typedef void (*StateFunc)(void);

StateFunc states[] = {
    state_idle,
    state_running,
    state_stopped
};

StateFunc current_state = states[0];
current_state();  // 调用当前状态的处理函数
```

## 常见陷阱

### 1. 声明混淆

```c
int (*fp)(int);      // ✓ 函数指针
int *fp(int);        // ✗ 返回 int* 的函数

typedef int (*FP)(int);   // ✓ 简化声明
FP fp;
```

### 2. 调用语法

```c
int (*fp)(int, int) = add;

fp(2, 3);        // ✓ 推荐
(*fp)(2, 3);     // ✓ 显式解引用（传统写法）
```

### 3. NULL 检查

```c
Operation op = NULL;

if (op != NULL) {
    op(5, 3);    // ✓ 安全
}

op(5, 3);        // ✗ 如果 op 为 NULL，崩溃！
```

## 性能考虑

### 直接调用 vs 间接调用

**直接调用**:
```asm
call 0x401146 <add>     # 地址在编译时确定
```

**间接调用**:
```asm
mov    rax, QWORD PTR [rbp-0x8]   # 从变量加载地址
call   rax                         # 间接跳转
```

**性能影响**:
- 间接调用需要额外的内存读取
- CPU 分支预测更困难
- 现代 CPU 的影响较小（~2-3个周期）

## 相关概念

- **Level 7** (内存): 函数在代码段的存储
- **Level 11 Exercise 2**: 指针数组（函数指针数组也是指针数组）
- **C++ vtable**: 虚函数表就是函数指针数组

## 调试检查清单

- [ ] 查看函数的地址
- [ ] 验证函数指针存储的值
- [ ] 检查函数指针数组的布局
- [ ] 追踪回调函数的调用
- [ ] 反汇编查看间接调用
- [ ] 理解 typedef 的作用

## 关键概念总结

1. **函数指针**: 存储函数地址的指针
2. **跳转表**: 函数指针数组，用于实现策略选择
3. **回调**: 将函数作为参数传递，稍后调用
4. **间接调用**: 通过指针调用函数，地址在运行时确定
5. **虚函数表**: C++ 多态的底层实现（函数指针数组）

## 总结

完成本练习后，你应该掌握：

1. ✅ 函数指针的声明和使用
2. ✅ typedef 简化复杂声明
3. ✅ 函数指针数组（跳转表）
4. ✅ 回调机制的实现
5. ✅ 间接调用的汇编表示
6. ✅ 虚函数表的原理

函数指针是 C 语言中实现高级设计模式的关键工具！
