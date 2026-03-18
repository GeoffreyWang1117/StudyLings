# Exercise 3: 函数指针与回调机制 - 参考答案

## 完整调试会话

### GDB 调试会话

```bash
$ gdb ./funcptr
(gdb) break main
Breakpoint 1 at 0x40118d: file funcptr.c, line 14.

(gdb) run
Starting program: ./funcptr

Breakpoint 1, main () at funcptr.c:14

# ========== 任务 1: 检查函数指针的值 ==========

(gdb) n
17          Operation op = add;

# 查看函数地址
(gdb) p add
$1 = {int (int, int)} 0x401146 <add>

(gdb) p &add
$2 = (int (*)(int, int)) 0x401146 <add>

(gdb) p sub
$3 = {int (int, int)} 0x401155 <sub>

(gdb) p mul
$4 = {int (int, int)} 0x401164 <mul>

# 函数地址在代码段（低地址）

# 执行赋值
(gdb) n
18          printf("函数指针 op 指向: %p (add 函数)\n", (void*)op);

# 检查函数指针 op
(gdb) p op
$5 = (Operation) 0x401146 <add>

(gdb) ptype op
type = int (*)(int, int)

# op 存储的值就是 add 函数的地址

# 查看 op 本身的地址（在栈上）
(gdb) p &op
$6 = (Operation *) 0x7fffffffe058

# op 变量在栈上，值是代码段地址

# 查看函数入口的指令
(gdb) x/5i add
   0x401146 <add>:      endbr64
   0x40114a <add+4>:    push   %rbp
   0x40114b <add+5>:    mov    %rsp,%rbp
   0x40114e <add+8>:    mov    %edi,-0x4(%rbp)
   0x401151 <add+11>:   mov    %esi,-0x8(%rbp)

# 通过函数指针调用
(gdb) n
19          printf("调用 op(5, 3) = %d\n\n", op(5, 3));

(gdb) p op(5, 3)
$7 = 8

# ========== 任务 2: 查看函数指针数组 ==========

(gdb) n
...
23          const char *names[] = {"add", "sub", "mul"};

(gdb) n
25          printf("函数指针数组:\n");

# 查看函数指针数组
(gdb) p ops
$8 = {0x401146 <add>, 0x401155 <sub>, 0x401164 <mul>}

(gdb) p sizeof(ops)
$9 = 24
# 3 个函数指针 * 8 字节 = 24

(gdb) p ops[0]
$10 = (Operation) 0x401146 <add>

(gdb) p ops[1]
$11 = (Operation) 0x401155 <sub>

(gdb) p ops[2]
$12 = (Operation) 0x401164 <mul>

# 查看数组的内存布局
(gdb) x/3xg ops
0x7fffffffe030: 0x0000000000401146  0x0000000000401155
0x7fffffffe040: 0x0000000000401164

# 数组存储的是函数的地址

# 通过数组调用函数
(gdb) p ops[1](10, 5)
$13 = 5
# ops[1] 是 sub，10 - 5 = 5

# 查看每个函数的地址差
(gdb) p (void*)ops[1] - (void*)ops[0]
$14 = 15
# sub 和 add 之间相差 15 字节

(gdb) p (void*)ops[2] - (void*)ops[1]
$15 = 15
# mul 和 sub 之间相差 15 字节

# ========== 任务 3: 追踪回调函数调用 ==========

(gdb) break callback_example
Breakpoint 2 at 0x401173: file funcptr.c, line 10.

(gdb) continue
函数指针 op 指向: 0x401146 (add 函数)
调用 op(5, 3) = 8

函数指针数组:
ops[0] = 0x401146 (add)
ops[1] = 0x401155 (sub)
ops[2] = 0x401164 (mul)

使用回调函数:

Breakpoint 2, callback_example (x=10, y=5, op=0x401146 <add>, name=0x402004 "add")

(gdb) info args
x = 10
y = 5
op = 0x401146 <add>
name = 0x402004 "add"

# op 参数存储的是 add 函数的地址

(gdb) p op
$16 = (Operation) 0x401146 <add>

# 查看栈帧信息
(gdb) info frame
Stack level 0, frame at 0x7fffffffe020:
 rip = 0x401173 in callback_example (funcptr.c:10);
    saved rip = 0x401207
 called by frame at 0x7fffffffe060
 source language c.
 Arglist at 0x7fffffffe010, args: x=10, y=5, op=0x401146 <add>, name=0x402004 "add"
 Locals at 0x7fffffffe010, Previous frame's sp is 0x7fffffffe020

# 单步到调用点
(gdb) n
10          printf("%s(%d, %d) = %d\n", name, x, y, op(x, y));

# 使用 step 进入回调函数
(gdb) step
add (a=10, b=5) at funcptr.c:3

# 成功进入 add 函数！

(gdb) backtrace
#0  add (a=10, b=5) at funcptr.c:3
#1  0x0000000000401189 in callback_example (x=10, y=5, op=0x401146 <add>,
    name=0x402004 "add") at funcptr.c:10
#2  0x0000000000401207 in main () at funcptr.c:32

# 可以看到完整的调用链

(gdb) finish
Run till exit from #0  add (a=10, b=5) at funcptr.c:3
0x0000000000401189 in callback_example (x=10, y=5, op=0x401146 <add>,
    name=0x402004 "add") at funcptr.c:10

Value returned is $17 = 15

# add(10, 5) 返回 15

# ========== 任务 4: 反汇编分析 ==========

# 查看 add 函数的汇编
(gdb) disassemble add
Dump of assembler code for function add:
   0x0000000000401146 <+0>:     endbr64
   0x000000000040114a <+4>:     push   %rbp
   0x000000000040114b <+5>:     mov    %rsp,%rbp
   0x000000000040114e <+8>:     mov    %edi,-0x4(%rbp)
   0x0000000000401151 <+11>:    mov    %esi,-0x8(%rbp)
   0x0000000000401154 <+14>:    mov    -0x4(%rbp),%edx
   0x0000000000401157 <+17>:    mov    -0x8(%rbp),%eax
   0x000000000040115a <+20>:    add    %edx,%eax
   0x000000000040115c <+22>:    pop    %rbp
   0x000000000040115d <+23>:    ret
End of assembler dump.

# 查看 callback_example 的汇编
(gdb) disassemble callback_example
Dump of assembler code for function callback_example:
   0x0000000000401165 <+0>:     endbr64
   0x0000000000401169 <+4>:     push   %rbp
   0x000000000040116a <+5>:     mov    %rsp,%rbp
   0x000000000040116d <+8>:     sub    $0x20,%rsp
   0x0000000000401171 <+12>:    mov    %edi,-0x4(%rbp)
   0x0000000000401174 <+15>:    mov    %esi,-0x8(%rbp)
   0x0000000000401177 <+18>:    mov    %rdx,-0x10(%rbp)    # op 参数
   0x000000000040117b <+22>:    mov    %rcx,-0x18(%rbp)    # name 参数
   0x000000000040117f <+26>:    mov    -0x8(%rbp),%edx     # y
   0x0000000000401182 <+29>:    mov    -0x4(%rbp),%eax     # x
   0x0000000000401185 <+32>:    mov    %edx,%esi
   0x0000000000401187 <+34>:    mov    %eax,%edi
   0x0000000000401189 <+36>:    call   *-0x10(%rbp)        # ← 间接调用！
   0x000000000040118c <+39>:    mov    %eax,%ecx
   ...
End of assembler dump.

# 关键指令：call *-0x10(%rbp)
# * 表示间接调用，地址从 -0x10(%rbp) 加载

# 对比直接调用（在 main 中）
(gdb) disassemble main
...
   0x00000000004011e5 <+88>:    mov    $0x3,%esi
   0x00000000004011ea <+93>:    mov    $0x5,%edi
   0x00000000004011ef <+98>:    call   0x401146 <add>      # ← 直接调用
...

# 直接调用：call 0x401146（地址是立即数）
# 间接调用：call *(%rax)（地址从寄存器/内存读取）

# 性能分析
(gdb) set disassemble-next-line on
(gdb) stepi
# 可以看到每条指令的执行

# ========== 扩展：查看类型信息 ==========

(gdb) ptype Operation
type = int (*)(int, int)

(gdb) ptype ops
type = int (*[3])(int, int)
# 3个函数指针的数组

(gdb) ptype callback_example
type = void (int, int, Operation, const char *)

# ========== 测试 NULL 检查 ==========

(gdb) set var op = 0

(gdb) p op
$18 = (Operation) 0x0

(gdb) call op(5, 3)
Program received signal SIGSEGV, Segmentation fault.
# 调用 NULL 函数指针会崩溃！

(gdb) quit
```

### LLDB 调试会话

```bash
$ lldb ./funcptr
(lldb) target create "./funcptr"

(lldb) b main
Breakpoint 1: where = funcptr`main + 13

(lldb) run
Process 1234 launched: './funcptr'

Process 1234 stopped

# ========== 任务 1: 检查函数指针的值 ==========

(lldb) n
(lldb) n

# 查看函数地址
(lldb) expr add
(int (*)(int, int)) $0 = 0x0000000000401146

(lldb) expr &add
(int (*)(int, int)) $1 = 0x0000000000401146

(lldb) expr sub
(int (*)(int, int)) $2 = 0x0000000000401155

(lldb) expr mul
(int (*)(int, int)) $3 = 0x0000000000401164

# 执行到 op 赋值之后
(lldb) n

(lldb) frame variable op
(Operation) op = 0x0000000000401146

(lldb) expr op
(Operation) $4 = 0x0000000000401146

# 查看函数入口指令
(lldb) memory read --format instruction --count 5 `add`
0x401146: endbr64
0x40114a: pushq  %rbp
0x40114b: movq   %rsp, %rbp
0x40114e: movl   %edi, -0x4(%rbp)
0x401151: movl   %esi, -0x8(%rbp)

# 调用函数指针
(lldb) expr op(5, 3)
(int) $5 = 8

# ========== 任务 2: 查看函数指针数组 ==========

(lldb) n
...

(lldb) frame variable ops
(Operation [3]) ops = {
  [0] = 0x0000000000401146
  [1] = 0x0000000000401155
  [2] = 0x0000000000401164
}

(lldb) expr sizeof(ops)
(unsigned long) $6 = 24

(lldb) memory read --size 8 --count 3 --format x `ops`
0x7fffffffe030: 0x0000000000401146 0x0000000000401155
0x7fffffffe040: 0x0000000000401164

# 通过数组调用
(lldb) expr ops[1](10, 5)
(int) $7 = 5

# ========== 任务 3: 追踪回调函数调用 ==========

(lldb) b callback_example
Breakpoint 2: where = funcptr`callback_example + 12

(lldb) continue
Process 1234 resuming
...

Process 1234 stopped
* thread #1, stop reason = breakpoint 2.1
    frame #0: funcptr`callback_example(x=10, y=5, op=0x401146, name="add")

(lldb) frame variable
(int) x = 10
(int) y = 5
(Operation) op = 0x0000000000401146
(const char *) name = 0x0000000000402004 "add"

(lldb) expr op
(Operation) $8 = 0x0000000000401146

# 单步进入回调
(lldb) n
(lldb) step
Process 1234 stopped
* thread #1, stop reason = step in
    frame #0: funcptr`add(a=10, b=5)

# 成功进入 add 函数

(lldb) thread backtrace
* thread #1, stop reason = step in
  * frame #0: funcptr`add(a=10, b=5)
    frame #1: funcptr`callback_example(x=10, y=5, op=0x401146, name="add")
    frame #2: funcptr`main

# ========== 任务 4: 反汇编分析 ==========

(lldb) disassemble --name add
funcptr`add:
    0x401146 <+0>:  endbr64
    0x40114a <+4>:  pushq  %rbp
    0x40114b <+5>:  movq   %rsp, %rbp
    0x40114e <+8>:  movl   %edi, -0x4(%rbp)
    0x401151 <+11>: movl   %esi, -0x8(%rbp)
    0x401154 <+14>: movl   -0x4(%rbp), %edx
    0x401157 <+17>: movl   -0x8(%rbp), %eax
    0x40115a <+20>: addl   %edx, %eax
    0x40115c <+22>: popq   %rbp
    0x40115d <+23>: retq

(lldb) disassemble --name callback_example
funcptr`callback_example:
    ...
    0x401189 <+36>: callq  *-0x10(%rbp)    ; 间接调用
    ...

# 对比直接调用
(lldb) disassemble --name main
funcptr`main:
    ...
    0x4011ef <+98>: callq  0x401146        ; 直接调用 add
    ...

# 关键差异：
# 直接：callq 0x401146（立即数地址）
# 间接：callq *-0x10(%rbp)（从内存加载地址）

(lldb) quit
```

## 答案总结

### 任务 1: 函数指针的值

| 问题 | 答案 |
|------|------|
| add 函数的地址 | 0x401146 (代码段) |
| op 存储的值 | 0x401146 (add 的地址) |
| op 本身存储在哪里 | 栈 (0x7fffffffe058) |
| op 指向的函数在哪里 | 代码段 (.text) |

**内存布局**:
```
栈 (0x7fffffffe058):
  op: [0x401146] ─────┐
                      │
代码段 (0x401146):     │
  add: [endbr64]  <───┘
       [push %rbp]
       [mov %rsp,%rbp]
       ...
```

### 任务 2: 函数指针数组

| 问题 | 答案 |
|------|------|
| ops 数组占用字节 | 24 (3 × 8) |
| ops[0] 指向 | 0x401146 (add) |
| ops[1] 指向 | 0x401155 (sub) |
| ops[2] 指向 | 0x401164 (mul) |
| 调用方式 | ops[1](10, 5) |
| 存储内容 | 函数地址（指针） |

**跳转表**:
```
ops @ 0x7fffffffe030:
  [0]: 0x401146 → add
  [1]: 0x401155 → sub
  [2]: 0x401164 → mul
```

**使用示例**:
```c
for (int i = 0; i < 3; i++) {
    ops[i](10, 5);  // 依次调用 add, sub, mul
}
```

### 任务 3: 回调函数调用

#### 参数传递

```
main 调用 callback_example(10, 5, add, "add"):
  寄存器/栈传参:
    rdi = 10
    rsi = 5
    rdx = 0x401146 (add 的地址)
    rcx = 0x402004 ("add" 字符串)

callback_example 栈帧:
  [rbp-0x4]:  x = 10
  [rbp-0x8]:  y = 5
  [rbp-0x10]: op = 0x401146
  [rbp-0x18]: name = 0x402004
```

#### 调用流程

1. **准备参数**: x, y 加载到 edi, esi
2. **加载函数地址**: `mov -0x10(%rbp), %rax` (op → rax)
3. **间接调用**: `call *%rax`
4. **跳转到 add**: CPU 跳转到 0x401146
5. **执行 add 函数**
6. **返回**: ret 指令返回到 callback_example

#### 回调 vs 直接调用

| 特性 | 直接调用 | 回调调用 |
|------|---------|---------|
| 地址确定时间 | 编译时 | 运行时 |
| 汇编指令 | `call 0x401146` | `call *%rax` |
| 灵活性 | 固定 | 可变 |
| 性能 | 快 | 稍慢 |

### 任务 4: 反汇编分析

#### 直接调用 (main 中)

```asm
mov    $0x3,%esi          ; 参数 b = 3
mov    $0x5,%edi          ; 参数 a = 5
call   0x401146 <add>     ; 直接调用，地址是常量
```

#### 间接调用 (callback_example 中)

```asm
mov    -0x8(%rbp),%edx    ; y
mov    -0x4(%rbp),%eax    ; x
mov    %edx,%esi          ; 参数 b
mov    %eax,%edi          ; 参数 a
call   *-0x10(%rbp)       ; 间接调用，地址从栈读取
```

**关键差异**:
- **直接调用**: `call <地址>` - 地址是立即数
- **间接调用**: `call *<地址>` - 地址从寄存器/内存加载

#### 性能影响

| 操作 | 直接调用 | 间接调用 |
|------|---------|---------|
| 指令数 | 1 (call) | 2 (load + call) |
| 内存访问 | 0 | 1 |
| 分支预测 | 容易 | 困难 |
| 额外开销 | 0 | ~2-5 周期 |

## 扩展练习答案

### 1. 函数指针表（计算器）

```c
#include <stdio.h>

typedef int (*Operation)(int, int);

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }
int divide(int a, int b) { return b != 0 ? a / b : 0; }

typedef struct {
    char op;
    Operation func;
    const char *name;
} OpEntry;

OpEntry table[] = {
    {'+', add, "加法"},
    {'-', sub, "减法"},
    {'*', mul, "乘法"},
    {'/', divide, "除法"}
};

int calculate(int a, char op, int b) {
    for (int i = 0; i < 4; i++) {
        if (table[i].op == op) {
            printf("%d %c %d = ", a, op, b);
            int result = table[i].func(a, b);
            printf("%d (%s)\n", result, table[i].name);
            return result;
        }
    }
    printf("未知操作符: %c\n", op);
    return 0;
}

int main() {
    calculate(10, '+', 5);   // 15
    calculate(10, '-', 5);   // 5
    calculate(10, '*', 5);   // 50
    calculate(10, '/', 5);   // 2
    return 0;
}
```

**调试要点**:
```bash
(gdb) p table
$1 = {{op = 43 '+', func = 0x401146 <add>, name = 0x402008 "加法"},
      {op = 45 '-', func = 0x401155 <sub>, name = 0x402010 "减法"},
      ...}

(gdb) p table[0].func(10, 5)
$2 = 15
```

### 2. 虚函数表（vtable 模拟）

```c
#include <stdio.h>
#include <stdlib.h>

// 虚函数表
typedef struct {
    void (*draw)(void *self);
    void (*move)(void *self, int dx, int dy);
} ShapeVTable;

// 基类
typedef struct {
    ShapeVTable *vtable;
    int x, y;
} Shape;

// 圆形
typedef struct {
    Shape base;
    int radius;
} Circle;

void circle_draw(void *self) {
    Circle *c = (Circle*)self;
    printf("绘制圆形 @ (%d, %d), 半径 = %d\n",
           c->base.x, c->base.y, c->radius);
}

void circle_move(void *self, int dx, int dy) {
    Shape *s = (Shape*)self;
    s->x += dx;
    s->y += dy;
    printf("圆形移动到 (%d, %d)\n", s->x, s->y);
}

ShapeVTable circle_vtable = {
    .draw = circle_draw,
    .move = circle_move
};

// 矩形
typedef struct {
    Shape base;
    int width, height;
} Rectangle;

void rect_draw(void *self) {
    Rectangle *r = (Rectangle*)self;
    printf("绘制矩形 @ (%d, %d), %dx%d\n",
           r->base.x, r->base.y, r->width, r->height);
}

void rect_move(void *self, int dx, int dy) {
    Shape *s = (Shape*)self;
    s->x += dx;
    s->y += dy;
    printf("矩形移动到 (%d, %d)\n", s->x, s->y);
}

ShapeVTable rect_vtable = {
    .draw = rect_draw,
    .move = rect_move
};

// 多态调用
void draw_shape(Shape *s) {
    s->vtable->draw(s);  // 虚函数调用
}

void move_shape(Shape *s, int dx, int dy) {
    s->vtable->move(s, dx, dy);
}

int main() {
    Circle c = {{&circle_vtable, 10, 20}, 5};
    Rectangle r = {{&rect_vtable, 30, 40}, 10, 20};

    Shape *shapes[] = {(Shape*)&c, (Shape*)&r};

    for (int i = 0; i < 2; i++) {
        draw_shape(shapes[i]);   // 多态！
        move_shape(shapes[i], 5, 5);
    }

    return 0;
}
```

**调试要点**:
```bash
(gdb) p c
$1 = {base = {vtable = 0x404040 <circle_vtable>, x = 10, y = 20}, radius = 5}

(gdb) p c.base.vtable
$2 = (ShapeVTable *) 0x404040 <circle_vtable>

(gdb) p *c.base.vtable
$3 = {draw = 0x401165 <circle_draw>, move = 0x4011a5 <circle_move>}

(gdb) call c.base.vtable->draw(&c)
绘制圆形 @ (10, 20), 半径 = 5

# 这就是 C++ 虚函数的底层实现！
```

### 3. qsort 回调

```c
#include <stdio.h>
#include <stdlib.h>

int compare_asc(const void *a, const void *b) {
    return *(int*)a - *(int*)b;
}

int compare_desc(const void *a, const void *b) {
    return *(int*)b - *(int*)a;
}

void print_array(int *arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int arr[] = {5, 2, 8, 1, 9, 3};
    int size = sizeof(arr) / sizeof(arr[0]);

    printf("原始数组: ");
    print_array(arr, size);

    qsort(arr, size, sizeof(int), compare_asc);
    printf("升序排序: ");
    print_array(arr, size);

    qsort(arr, size, sizeof(int), compare_desc);
    printf("降序排序: ");
    print_array(arr, size);

    return 0;
}
```

**调试 qsort 回调**:
```bash
(gdb) break compare_asc
(gdb) run
Breakpoint 1, compare_asc (a=0x7fffffffe050, b=0x7fffffffe054)

(gdb) p *(int*)a
$1 = 5

(gdb) p *(int*)b
$2 = 2

(gdb) finish
Value returned is $3 = 3

# qsort 多次调用 compare_asc 来排序

(gdb) continue
# 断点会多次命中

(gdb) backtrace
#0  compare_asc (a=0x7fffffffe050, b=0x7fffffffe054)
#1  0x00007ffff7a5e2a3 in msort_with_tmp.part ()
   from /lib/x86_64-linux-gnu/libc.so.6
#2  0x00007ffff7a5e1f0 in qsort () from /lib/x86_64-linux-gnu/libc.so.6
#3  0x000000000040123f in main ()

# 可以看到 qsort 的内部调用栈
```

## 核心概念总结

### 1. 函数指针的本质

```c
int add(int a, int b);   // 函数
int (*fp)(int, int);     // 函数指针

fp = add;                // 赋值（add 自动转换为地址）
fp = &add;               // 显式取地址（等价）
fp(2, 3);                // 调用（推荐）
(*fp)(2, 3);             // 显式解引用调用（传统）
```

**内存模型**:
- 函数代码存储在代码段 (.text)
- 函数指针存储函数的起始地址
- 调用时 CPU 跳转到该地址

### 2. typedef 简化

```c
// 原始声明（难读）
int (*fp)(int, int);
int (*ops[3])(int, int);

// 使用 typedef（清晰）
typedef int (*Operation)(int, int);
Operation fp;
Operation ops[3];
```

### 3. 函数指针数组（跳转表）

```c
Operation ops[] = {add, sub, mul, divide};

// 选择策略
int choice = get_user_choice();
int result = ops[choice](a, b);
```

**应用**:
- 策略模式
- 状态机
- 命令分发

### 4. 回调函数

```c
void process(int data, void (*callback)(int)) {
    // ... 处理数据 ...
    callback(result);  // 回调
}
```

**应用**:
- 事件处理
- 异步编程
- 插件系统

### 5. 虚函数表

```c
struct vtable {
    void (*func1)();
    void (*func2)();
};

struct object {
    struct vtable *vptr;  // 虚函数表指针
    // ... 数据成员 ...
};

obj->vptr->func1();  // 虚函数调用
```

## 性能优化建议

1. **尽量使用直接调用**: 编译器可以内联优化
2. **避免循环中的间接调用**: 分支预测失效
3. **考虑使用 switch**: 比函数指针数组快
4. **Profile 后再优化**: 现代 CPU 优化很好

## 常见错误

### 1. 声明错误

```c
int *fp(int);       // ✗ 这是函数，返回 int*
int (*fp)(int);     // ✓ 这是函数指针
```

### 2. 类型不匹配

```c
int add(int, int);
void (*fp)(int, int) = add;  // ✗ 返回类型不匹配

int (*fp)(int, int) = add;   // ✓ 正确
```

### 3. 忘记 NULL 检查

```c
void (*callback)() = get_callback();
callback();  // ✗ 可能崩溃

if (callback != NULL) {
    callback();  // ✓ 安全
}
```

## 总结

完成本练习后，你应该理解：

1. ✅ 函数指针存储函数的地址
2. ✅ typedef 简化复杂声明
3. ✅ 函数指针数组实现跳转表
4. ✅ 回调函数的传递和调用机制
5. ✅ 间接调用 vs 直接调用的汇编差异
6. ✅ 虚函数表是函数指针数组的应用
7. ✅ 函数指针是实现多态的基础

**关键要点**:
- 函数名即地址
- 函数指针像其他指针一样使用
- 间接调用牺牲小部分性能换取灵活性
- C++ 虚函数就是用函数指针实现的

掌握函数指针是成为 C 语言高手的必经之路！
