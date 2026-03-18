# Exercise 3: 内存段和栈帧布局 - 参考答案

## 完整调试会话

### GDB 调试会话

```bash
$ gdb ./segments
(gdb) break main
Breakpoint 1 at 0x4012e5: file segments.c, line 100.

(gdb) run
Starting program: ./segments

Breakpoint 1, main () at segments.c:100

# ========== 任务 1: 识别内存段 ==========

(gdb) continue
=== 内存段布局 ===

代码段 (.text):
  main 函数: 0x4012dd
  func_level1: 0x4011e6

只读数据段 (.rodata):
  const_value: 0x404030 (值: 100)
  const_string ptr: 0x404038
  const_string 内容: 0x402064

数据段 (.data):
  global_initialized: 0x404040 (值: 42)
  global_string: 0x404044 (内容: "Hello, World!")

BSS 段 (.bss):
  global_uninitialized: 0x404060 (值: 0)
  global_buffer: 0x404480

堆 (heap):
  heap_var: 0x4052a0 (值: 20)

栈 (stack):
  stack_var: 0x7fffffffe05c (值: 10)
  static_var: 0x404058 (值: 30)

# 使用 info proc mappings 查看详细映射
(gdb) info proc mappings
process 1234
Mapped address spaces:

          Start Addr           End Addr       Size     Offset objfile
      0x400000           0x401000     0x1000        0x0 /path/to/segments
      0x401000           0x402000     0x1000     0x1000 /path/to/segments  ← .text
      0x402000           0x403000     0x1000     0x2000 /path/to/segments  ← .rodata
      0x403000           0x404000     0x1000     0x2000 /path/to/segments
      0x404000           0x405000     0x1000     0x3000 /path/to/segments  ← .data + .bss
      0x405000           0x426000    0x21000        0x0 [heap]            ← heap
      ...
      0x7ffff7dd5000     0x7ffff7e00000    0x2b000        0x0 [libc.so...]
      ...
      0x7ffffffde000     0x7ffffffff000    0x21000        0x0 [stack]      ← stack

# 分析地址范围
(gdb) p/x main
$1 = 0x4012dd    # 在 0x401000-0x402000 范围内 → .text

(gdb) p/x &const_value
$2 = 0x404030    # 在 0x404000-0x405000 范围内 → .data/.bss

(gdb) p/x &global_initialized
$3 = 0x404040    # .data

(gdb) p/x &global_uninitialized
$4 = 0x404060    # .bss

# ========== 任务 2: 验证栈的增长方向 ==========

(gdb) break show_stack_growth
Breakpoint 2 at 0x401276: file segments.c, line 34.

(gdb) continue
Breakpoint 2, show_stack_growth () at segments.c:34

(gdb) n
...
38          printf("var1 @ %p\n", (void*)&var1);

# 查看三个变量的地址
(gdb) p &var1
$5 = (int *) 0x7fffffffe04c

(gdb) p &var2
$6 = (int *) 0x7fffffffe048

(gdb) p &var3
$7 = (int *) 0x7fffffffe044

# 地址递减：0x04c → 0x048 → 0x044
# 后声明的变量地址更低

(gdb) p (void*)&var1 - (void*)&var2
$8 = 4
# var2 的地址比 var1 低 4 字节

# 结论：栈向下增长（高地址 → 低地址）

(gdb) continue
=== 栈增长方向 ===
var1 @ 0x7fffffffe04c
var2 @ 0x7fffffffe048
var3 @ 0x7fffffffe044
栈向下增长（高地址 → 低地址）

# ========== 任务 3: 分析栈帧 ==========

(gdb) break func_level1
Breakpoint 3 at 0x4011fa: file segments.c, line 28.

(gdb) break func_level2
Breakpoint 4 at 0x40122f: file segments.c, line 22.

(gdb) break func_level3
Breakpoint 5 at 0x401264: file segments.c, line 16.

(gdb) continue
=== 栈帧布局 ===

Breakpoint 3, func_level1 () at segments.c:28

# 第一层
(gdb) backtrace
#0  func_level1 () at segments.c:28
#1  0x00000000004013a5 in show_stack_frame () at segments.c:98
#2  0x00000000004013bb in main () at segments.c:102

(gdb) info frame
Stack level 0, frame at 0x7fffffffe050:
 rip = 0x4011fa in func_level1 (segments.c:28); saved rip = 0x4013a5
 called by frame at 0x7fffffffe060
 source language c.
 Arglist at 0x7fffffffe040, args:
 Locals at 0x7fffffffe040, Previous frame's sp is 0x7fffffffe050
 Saved registers:
  rbp at 0x7fffffffe040, rip at 0x7fffffffe048

# 栈帧分析：
# - 当前帧起始: 0x7fffffffe050
# - saved rbp: 0x7fffffffe040
# - 返回地址: 0x7fffffffe048 (存储 0x4013a5)

(gdb) p &local1
$9 = (int *) 0x7fffffffe04c

(gdb) continue
Breakpoint 4, func_level2 () at segments.c:22

# 第二层
(gdb) backtrace
#0  func_level2 () at segments.c:22
#1  0x0000000000401210 in func_level1 () at segments.c:30
#2  0x00000000004013a5 in show_stack_frame () at segments.c:98
#3  0x00000000004013bb in main () at segments.c:102

(gdb) info frame
Stack level 0, frame at 0x7fffffffe040:
 rip = 0x40122f in func_level2 (segments.c:22); saved rip = 0x401210
 called by frame at 0x7fffffffe050
 ...

(gdb) p &local2
$10 = (int *) 0x7fffffffe03c

(gdb) continue
Breakpoint 5, func_level3 () at segments.c:16

# 第三层
(gdb) backtrace
#0  func_level3 () at segments.c:16
#1  0x0000000000401245 in func_level2 () at segments.c:24
#2  0x0000000000401210 in func_level1 () at segments.c:30
#3  0x00000000004013a5 in show_stack_frame () at segments.c:98
#4  0x00000000004013bb in main () at segments.c:102

(gdb) p &local3
$11 = (int *) 0x7fffffffe02c

# 栈帧地址对比：
# local1: 0x7fffffffe04c (最高)
# local2: 0x7fffffffe03c
# local3: 0x7fffffffe02c (最低，当前栈顶附近)
# 越深的调用，局部变量地址越低

# 查看所有帧
(gdb) backtrace full
#0  func_level3 () at segments.c:16
        local3 = 3
#1  0x0000000000401245 in func_level2 () at segments.c:24
        local2 = 2
#2  0x0000000000401210 in func_level1 () at segments.c:30
        local1 = 1
#3  0x00000000004013a5 in show_stack_frame () at segments.c:98
#4  0x00000000004013bb in main () at segments.c:102

# 查看返回地址
(gdb) info frame
...
 saved rip = 0x401245

(gdb) x/i 0x401245
   0x401245 <func_level2+22>: nop

# 这是 func_level2 中调用 func_level3 之后的下一条指令

# ========== 任务 4: 查看内存映射 ==========

# 使用 maintenance info sections 查看段详情
(gdb) maintenance info sections
Exec file: `/path/to/segments', file type elf64-x86-64.
...
  [13] 0x0000000000401000->0x0000000000401351 at 0x00001000: .text ALLOC LOAD READONLY CODE HAS_CONTENTS
  [14] 0x0000000000402000->0x0000000000402074 at 0x00002000: .rodata ALLOC LOAD READONLY DATA HAS_CONTENTS
  [23] 0x0000000000404000->0x0000000000404052 at 0x00003000: .data ALLOC LOAD DATA HAS_CONTENTS
  [24] 0x0000000000404060->0x0000000000404890 at 0x00003060: .bss ALLOC
...

# 段权限：
# .text:   READONLY CODE  (r-x)
# .rodata: READONLY DATA  (r--)
# .data:   DATA           (rw-)
# .bss:    (同 .data)     (rw-)

# 查看特定地址属于哪个段
(gdb) info symbol 0x4012dd
main in section .text of /path/to/segments

(gdb) info symbol 0x404040
global_initialized in section .data of /path/to/segments

# 使用 info files 查看所有段
(gdb) info files
Symbols from "/path/to/segments".
Local exec file:
        `/path/to/segments', file type elf64-x86-64.
        Entry point: 0x401050
        0x00000000004002a8 - 0x00000000004002c4 is .note.gnu.property
        0x00000000004002c4 - 0x00000000004002e8 is .note.gnu.build-id
        ...

# ========== 扩展：汇编分析 ==========

(gdb) disassemble func_level1
Dump of assembler code for function func_level1:
   0x00000000004011e6 <+0>:     endbr64
   0x00000000004011ea <+4>:     push   %rbp          # 保存 caller 的 rbp
   0x00000000004011eb <+5>:     mov    %rsp,%rbp     # 设置新的 rbp
   0x00000000004011ee <+8>:     sub    $0x10,%rsp    # 分配栈空间
   0x00000000004011f2 <+12>:    movl   $0x1,-0x4(%rbp)  # local1 = 1
   ...
   0x000000000040120b <+37>:    call   0x40121c <func_level2>
   ...
   0x0000000000401210 <+42>:    nop
   0x0000000000401211 <+43>:    leave               # 恢复 rbp, rsp
   0x0000000000401212 <+44>:    ret                 # 返回

# 栈帧创建：
# 1. push %rbp        - 保存老的栈底
# 2. mov %rsp,%rbp    - 设置新的栈底
# 3. sub $0x10,%rsp   - 分配局部变量空间

# 栈帧销毁：
# 1. leave            - 相当于 mov %rbp,%rsp; pop %rbp
# 2. ret              - 弹出返回地址并跳转

(gdb) quit
```

### LLDB 调试会话

```bash
$ lldb ./segments
(lldb) target create "./segments"

(lldb) b main
Breakpoint 1: where = segments`main + 13

(lldb) run
Process 1234 launched: './segments'

# ========== 任务 1: 识别内存段 ==========

(lldb) continue
Process 1234 resuming
[输出内存段信息...]

# 查看内存区域
(lldb) memory region `main`
[0x0000000000401000-0x0000000000402000) r-x /path/to/segments

(lldb) memory region `&global_initialized`
[0x0000000000404000-0x0000000000405000) rw- /path/to/segments

# ========== 任务 2: 栈增长 ==========

(lldb) b show_stack_growth
Breakpoint 2: where = segments`show_stack_growth + 22

(lldb) continue
Process 1234 resuming

(lldb) n
...

(lldb) frame variable &var1 &var2 &var3
(int *) &var1 = 0x00007fffffffe04c
(int *) &var2 = 0x00007fffffffe048
(int *) &var3 = 0x00007fffffffe044

# 地址递减 → 栈向下增长

# ========== 任务 3: 栈帧 ==========

(lldb) b func_level1
(lldb) b func_level2
(lldb) b func_level3

(lldb) continue
...

(lldb) bt
* thread #1, stop reason = breakpoint 3.1
  * frame #0: segments`func_level1
    frame #1: segments`show_stack_frame
    frame #2: segments`main

(lldb) frame info
frame #0: segments`func_level1 at segments.c:28

(lldb) frame variable
(int) local1 = 1

(lldb) continue
...

(lldb) bt
* thread #1, stop reason = breakpoint 4.1
  * frame #0: segments`func_level2
    frame #1: segments`func_level1 + 42
    frame #2: segments`show_stack_frame
    frame #3: segments`main

# 查看所有帧的变量
(lldb) bt all
...
frame #0: local2 = 2
frame #1: local1 = 1
frame #2: (无局部变量)
frame #3: (main 的变量)

(lldb) quit
```

## 答案总结

### 任务 1: 内存段识别

| 变量/函数 | 地址示例 | 所在段 | 说明 |
|-----------|----------|--------|------|
| `main` | 0x4012dd | .text | 代码段 |
| `func_level1` | 0x4011e6 | .text | 代码段 |
| `const_value` | 0x404030 | .rodata | 只读数据段 |
| `const_string` 内容 | 0x402064 | .rodata | 字符串字面量 |
| `global_initialized` | 0x404040 | .data | 初始化全局变量 |
| `global_string` | 0x404044 | .data | 初始化全局数组 |
| `global_uninitialized` | 0x404060 | .bss | 未初始化全局变量 |
| `global_buffer` | 0x404480 | .bss | 未初始化数组 |
| `heap_var` | 0x4052a0 | heap | malloc 分配 |
| `stack_var` | 0x7fffffffe05c | stack | 局部变量 |
| `static_var` | 0x404058 | .data | 静态局部变量 |

**观察**:
- 代码段地址最低 (0x401xxx)
- 数据段/BSS 段紧随其后 (0x404xxx)
- 堆地址稍高 (0x405xxx)
- 栈地址最高 (0x7ffxxx)

### 任务 2: 栈增长方向

**结果**: 栈向下增长（从高地址到低地址）

**证据**:
```
var1 @ 0x7fffffffe04c  (先声明)
var2 @ 0x7fffffffe048  (后声明，地址更低)
var3 @ 0x7fffffffe044  (最后声明，地址最低)
```

**原因**:
1. 历史原因：早期架构如此设计
2. 向上增长的堆不会冲突
3. 便于函数调用（参数压栈）

### 任务 3: 栈帧分析

**调用链**:
```
main() @ 0x7fffffffe0??
  └─ show_stack_frame() @ 0x7fffffffe0??
       └─ func_level1() @ 0x7fffffffe050
            └─ func_level2() @ 0x7fffffffe040
                 └─ func_level3() @ 0x7fffffffe030
```

**局部变量地址**:
```
local1 @ 0x7fffffffe04c  (level 1)
local2 @ 0x7fffffffe03c  (level 2)
local3 @ 0x7fffffffe02c  (level 3, 最深)
```

**栈帧结构** (func_level1):
```
高地址
┌─────────────────────┐ 0x7fffffffe050
│   返回地址          │ 0x7fffffffe048 (0x4013a5)
├─────────────────────┤
│   saved rbp         │ 0x7fffffffe040
├─────────────────────┤
│   local1            │ 0x7fffffffe04c
├─────────────────────┤
│   (对齐/其他)       │
└─────────────────────┘ ← rsp
低地址
```

**如何找到返回地址**:
```bash
(gdb) info frame
 saved rip = 0x4013a5  # 返回地址

(gdb) x/xg $rbp+8
0x7fffffffe048: 0x00000000004013a5  # 存储在 rbp+8
```

**如何找到上一层栈帧**:
```bash
(gdb) x/xg $rbp
0x7fffffffe040: 0x00007fffffffe060  # 上一层的 rbp
```

### 任务 4: 内存映射

**典型内存布局** (64位Linux):
```
地址范围                    大小    权限  内容
----------------------------------------
0x400000-0x401000          4KB     r--   ELF header
0x401000-0x402000          4KB     r-x   .text
0x402000-0x403000          4KB     r--   .rodata
0x403000-0x404000          4KB     r--   其他只读段
0x404000-0x405000          4KB     rw-   .data + .bss
0x405000-0x426000        132KB     rw-   heap
...
0x7ffff7xxx-0x7ffff7xxx    ...     r-x   libc.so (代码)
0x7ffff7xxx-0x7ffff7xxx    ...     r--   libc.so (数据)
...
0x7ffffffde000-0x7ffffffff000  132KB  rw-   stack
```

**段权限说明**:
- `r-x`: 只读可执行 (.text)
- `r--`: 只读 (.rodata)
- `rw-`: 可读写 (.data, .bss, heap, stack)

**堆和栈之间的空间**:
- 通常有 GB 级别的未映射空间
- 用于检测栈溢出和堆溢出
- 允许堆和栈动态增长

## 扩展练习答案

### 1. 验证 BSS 段清零

```c
#include <stdio.h>

int bss_array[100];  // 未初始化

int main() {
    for (int i = 0; i < 100; i++) {
        if (bss_array[i] != 0) {
            printf("BSS not zeroed at index %d\n", i);
            return 1;
        }
    }
    printf("BSS is properly zeroed\n");
    return 0;
}
```

**调试验证**:
```bash
(gdb) p bss_array[0]@100
$1 = {0 <repeats 100 times>}
```

### 2. 观察堆的增长

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *p1 = malloc(100);
    int *p2 = malloc(100);
    int *p3 = malloc(100);

    printf("p1: %p\n", (void*)p1);
    printf("p2: %p\n", (void*)p2);
    printf("p3: %p\n", (void*)p3);

    printf("p2 - p1 = %ld\n", (char*)p2 - (char*)p1);
    printf("p3 - p2 = %ld\n", (char*)p3 - (char*)p2);

    free(p1);
    free(p2);
    free(p3);
}
```

**结果**:
```
p1: 0x4052a0
p2: 0x405310  (差约 112 字节，包含元数据)
p3: 0x405380
```

### 3. 栈溢出实验

```c
#include <stdio.h>

void deep_recursion(int depth) {
    char buffer[1024];  // 每次调用消耗 1KB+ 栈空间
    printf("Depth: %d, buffer @ %p\n", depth, (void*)buffer);

    if (depth < 10000) {
        deep_recursion(depth + 1);
    }
}

int main() {
    deep_recursion(0);
    return 0;
}
```

**会导致**:
```
...
Segmentation fault (core dumped)  # 栈溢出
```

## 核心概念总结

### 内存段一览

```c
// .text (代码段)
void my_function() {
    // 函数代码存储在这里
}

// .rodata (只读数据)
const char *str = "literal";  // 字符串字面量
const int val = 42;           // 常量

// .data (已初始化数据)
int global = 100;             // 全局变量

// .bss (未初始化数据)
int uninit;                   // 自动清零
char buffer[1024];            // 大数组

// heap (堆)
int *p = malloc(sizeof(int)); // 动态分配

// stack (栈)
void func() {
    int local = 10;           // 局部变量
}
```

### 栈帧生命周期

**创建** (函数调用时):
```asm
push   %rbp          # 保存旧的栈底
mov    %rsp,%rbp     # 建立新的栈底
sub    $N,%rsp       # 分配局部变量空间
```

**使用** (函数执行中):
```asm
mov    %edi,-0x4(%rbp)   # 访问局部变量
call   other_func         # 调用其他函数
```

**销毁** (函数返回时):
```asm
leave                # mov %rbp,%rsp; pop %rbp
ret                  # pop %rip; jmp %rip
```

## 调试技巧总结

### 查看内存段

1. **GDB**:
```bash
info proc mappings        # 所有映射
info files                # 段信息
maintenance info sections # 详细段信息
```

2. **Shell**:
```bash
readelf -S ./program      # 段头表
objdump -h ./program      # 段概要
size ./program            # 段大小
```

### 查看栈帧

```bash
backtrace              # 调用栈
info frame             # 当前帧详情
info args              # 参数
info locals            # 局部变量
frame N                # 切换到第N帧
```

### 查看汇编

```bash
disassemble func       # 反汇编函数
layout asm             # 汇编视图
stepi                  # 单步执行指令
```

完成本练习后，你已经彻底理解了程序的内存布局！
