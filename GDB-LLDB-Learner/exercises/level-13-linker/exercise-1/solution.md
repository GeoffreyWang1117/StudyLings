# Exercise 1: 静态链接 vs 动态链接 - 参考答案

## 完整调试会话

### 构建和分析

```bash
$ make both
gcc -g -Wall -Wextra -O0 -c mathlib.c -o mathlib.o
ar rcs libmath.a mathlib.o
静态库创建完成: libmath.a
gcc -g -Wall -Wextra -O0 -fPIC -c mathlib.c -o mathlib_pic.o
gcc -shared -o libmath.so mathlib_pic.o
动态库创建完成: libmath.so
gcc -g -Wall -Wextra -O0 main.c -L. -lmath -o main_static
静态链接可执行文件: main_static
   text    data     bss     dec     hex filename
   2156     608       8    2772     ad4 main_static
gcc -g -Wall -Wextra -O0 main.c -L. -lmath -o main_dynamic
动态链接可执行文件: main_dynamic
   text    data     bss     dec     hex filename
   1543     608       8    2159     86f main_dynamic

=== 文件大小对比 ===
-rwxr-xr-x 1 user user 17K Nov 18 10:00 main_static
-rwxr-xr-x 1 user user 16K Nov 18 10:00 main_dynamic
-rw-r--r-- 1 user user 2.1K Nov 18 10:00 libmath.a
-rwxr-xr-x 1 user user 16K Nov 18 10:00 libmath.so

=== 符号对比 ===
静态链接符号数:
65
动态链接符号数:
62

# ========== 任务 1: 文件大小对比 ==========

$ ls -lh
total 68K
-rw-r--r-- 1 user user  16K libmath.a       # 静态库
-rwxr-xr-x 1 user user  16K libmath.so      # 动态库
-rwxr-xr-x 1 user user  17K main_dynamic    # 动态链接
-rwxr-xr-x 1 user user  17K main_static     # 静态链接

# 详细大小分析
$ size main_static main_dynamic
   text    data     bss     dec     hex filename
   2156     608       8    2772     ad4 main_static
   1543     608       8    2159     86f main_dynamic

# text 段差异：2156 - 1543 = 613 字节
# 静态版本包含了库代码

# ========== 任务 2: 符号表分析 ==========

# 查看静态库内容
$ ar t libmath.a
mathlib.o

# 查看静态库中的符号
$ nm libmath.a

mathlib.o:
0000000000000000 T add
0000000000000000 B mathlib_counter
0000000000000000 D mathlib_version
0000000000000036 T multiply
0000000000000058 T factorial
0000000000000012 t internal_helper

# 符号类型说明：
# T: 全局函数（.text 段）
# t: 局部函数（static）
# D: 初始化全局变量（.data 段）
# B: 未初始化全局变量（.bss 段）

# 查看动态库中的符号（导出符号）
$ nm -D libmath.so
0000000000001169 T add
0000000000004024 B mathlib_counter
0000000000004020 D mathlib_version
000000000000119f T multiply
00000000000011c1 T factorial

# 注意：internal_helper 没有出现！
# 因为它是 static 函数，不会被导出

# 查看静态链接版本的符号
$ nm main_static | grep -E "(add|multiply|factorial|internal_helper)"
0000000000401196 T add
00000000004011f6 T factorial
00000000004011cc T multiply
00000000004011a8 t internal_helper

# add, multiply, factorial 都在可执行文件中
# 地址已经确定（绝对地址）

# 查看动态链接版本的符号
$ nm main_dynamic | grep -E "(add|multiply|factorial)"
                 U add
                 U factorial
                 U multiply

# U: Undefined（未定义）
# 这些符号在运行时才会从 libmath.so 中解析

# 查看动态链接版本的所有未定义符号
$ nm -u main_dynamic
                 U add
                 U factorial
                 U __libc_start_main@@GLIBC_2.2.5
                 U mathlib_version
                 U multiply
                 U printf@@GLIBC_2.2.5

# ========== 任务 3: 动态库依赖 ==========

# 静态链接版本的依赖
$ ldd main_static
	linux-vdso.so.1 (0x00007ffc8e9fe000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f4a2e400000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f4a2e61c000)

# 只依赖系统库（libc），不依赖 libmath

# 动态链接版本的依赖
$ ldd main_dynamic
	linux-vdso.so.1 (0x00007ffc93bfe000)
	libmath.so => not found
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f9c4e200000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f9c4e41c000)

# libmath.so => not found
# 因为库不在标准路径中

# 设置 LD_LIBRARY_PATH 后
$ LD_LIBRARY_PATH=. ldd main_dynamic
	linux-vdso.so.1 (0x00007ffc0e1fe000)
	libmath.so => ./libmath.so (0x00007f2a9e000000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f2a9dc00000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f2a9e20c000)

# 现在找到了！

# 运行动态版本
$ LD_LIBRARY_PATH=. ./main_dynamic
=== 静态链接 vs 动态链接演示 ===

mathlib_version: 100
  [mathlib internal helper called]
add(10, 20) = 30
multiply(10, 20) = 200
factorial(5) = 120

# 如果删除 libmath.so
$ mv libmath.so libmath.so.bak
$ ./main_dynamic
./main_dynamic: error while loading shared libraries: libmath.so: cannot open shared object file: No such file or directory

# 运行时找不到库！

# ========== 任务 4: GDB 调试会话 ==========

# 调试静态链接版本
$ gdb -q main_static
(gdb) break add
Breakpoint 1 at 0x401196: file mathlib.c, line 9.

(gdb) run
Starting program: ./main_static
=== 静态链接 vs 动态链接演示 ===

mathlib_version: 100

Breakpoint 1, add (a=10, b=20) at mathlib.c:9

(gdb) info symbol add
add in section .text of /path/to/main_static

# add 在可执行文件的 .text 段中

(gdb) print add
$1 = {int (int, int)} 0x401196 <add>

# 地址是绝对地址 0x401196

(gdb) disassemble add
Dump of assembler code for function add:
=> 0x0000000000401196 <+0>:     endbr64
   0x000000000040119a <+4>:     push   %rbp
   0x000000000040119b <+5>:     mov    %rsp,%rbp
   0x000000000040119e <+8>:     sub    $0x10,%rsp
   0x00000000004011a2 <+12>:    mov    %edi,-0x4(%rbp)
   0x00000000004011a5 <+15>:    mov    %esi,-0x8(%rbp)
   0x00000000004011a8 <+18>:    call   0x4011a8 <internal_helper>
   ...

# 完整的函数代码都在这里

(gdb) quit

# 调试动态链接版本
$ LD_LIBRARY_PATH=. gdb -q main_dynamic
(gdb) break add
Function "add" not defined.
Make breakpoint pending on future shared library load? (y or [n]) y
Breakpoint 1 (add) pending.

# 注意：add 尚未加载，设置为 pending 断点

(gdb) run
Starting program: ./main_dynamic
=== 静态链接 vs 动态链接演示 ===

mathlib_version: 100

Breakpoint 1, add (a=10, b=20) at mathlib.c:9

(gdb) info symbol add
add in section .text of ./libmath.so

# add 在 libmath.so 的 .text 段中

(gdb) print add
$1 = {int (int, int)} 0x7ffff7fc5169 <add>

# 地址是运行时分配的 0x7ffff7fc5169（高地址）

(gdb) info sharedlibrary
From                To                  Syms Read   Shared Object Library
0x00007ffff7fc5000  0x00007ffff7fc51e7  Yes         ./libmath.so
0x00007ffff7fc3000  0x00007ffff7fc4000  Yes (*)     /lib64/ld-linux-x86-64.so.2
0x00007ffff7c00000  0x00007ffff7d91000  Yes         /lib/x86_64-linux-gnu/libc.so.6

# 显示所有加载的共享库
# libmath.so 被加载到 0x7ffff7fc5000

(gdb) disassemble add
Dump of assembler code for function add:
=> 0x00007ffff7fc5169 <+0>:     endbr64
   0x00007ffff7fc516d <+4>:     push   %rbp
   ...

# 函数代码在共享库中

(gdb) quit

# ========== 任务 5: readelf 深入分析 ==========

# 查看静态链接版本的文件头
$ readelf -h main_static
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           Advanced Micro Devices X86-64
  Entry point address:               0x401050

# 查看动态链接版本的文件头
$ readelf -h main_dynamic
ELF Header:
  ...
  Type:                              DYN (Shared object file)
  Entry point address:               0x1050

# 注意：Type 是 DYN（位置无关）

# 查看段头（静态版本）
$ readelf -S main_static | head -20
There are 29 section headers, starting at offset 0x39c8:

Section Headers:
  [Nr] Name              Type             Address           Offset
       Size              EntSize          Flags  Link  Info  Align
  [ 0]                   NULL             0000000000000000  00000000
       0000000000000000  0000000000000000           0     0     0
  [13] .text             PROGBITS         0000000000401050  00001050
       0000000000000301  0000000000000000  AX       0     0     16
  [15] .rodata           PROGBITS         0000000000402000  00002000
       0000000000000074  0000000000000000   A       0     0     8
  [23] .data             PROGBITS         0000000000404000  00003000
       0000000000000018  0000000000000000  WA       0     0     8
  [24] .bss              NOBITS           0000000000404018  00003018
       0000000000000008  0000000000000000  WA       0     0     4

# 查看段头（动态版本）
$ readelf -S main_dynamic | grep -E "(\.interp|\.plt|\.got)"
  [ 1] .interp           PROGBITS         0000000000000318  00000318
  [11] .plt              PROGBITS         0000000000001020  00001020
  [12] .plt.got          PROGBITS         0000000000001070  00001070
  [21] .got              PROGBITS         0000000000003fb0  00002fb0
  [22] .got.plt          PROGBITS         0000000000003fd8  00002fd8

# 动态版本有 .interp（动态链接器路径）、.plt、.got

# 查看 .interp 段内容
$ readelf -p .interp main_dynamic

String dump of section '.interp':
  [     0]  /lib64/ld-linux-x86-64.so.2

# 这是动态链接器的路径

# 查看动态段
$ readelf -d main_dynamic

Dynamic section at offset 0x2dd8 contains 27 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libmath.so]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
 0x000000000000000c (INIT)               0x1000
 0x000000000000000d (FINI)               0x12d4
 0x0000000000000019 (INIT_ARRAY)         0x3dc8
 0x000000000000001b (INIT_ARRAYSZ)       8 (bytes)
 ...

# NEEDED 项列出了所需的动态库

# 查看重定位表
$ readelf -r main_dynamic

Relocation section '.rela.dyn' at offset 0x520 contains 8 entries:
  Offset          Info           Type           Sym. Value    Sym. Name + Addend
000000003fb0  000000000008 R_X86_64_RELATIVE                    1180
000000003fb8  000000000008 R_X86_64_RELATIVE                    1140
000000004008  000000000008 R_X86_64_RELATIVE                    4008
000000003fd8  000100000006 R_X86_64_GLOB_DAT 0000000000000000 __libc_start_main@GLIBC_2.2.5 + 0
000000003fe0  000300000006 R_X86_64_GLOB_DAT 0000000000000000 __gmon_start__ + 0
000000004000  000600000006 R_X86_64_GLOB_DAT 0000000000000000 mathlib_version + 0

Relocation section '.rela.plt' at offset 0x5e0 contains 4 entries:
  Offset          Info           Type           Sym. Value    Sym. Name + Addend
000000003ff0  000200000007 R_X86_64_JUMP_SLO 0000000000000000 printf@GLIBC_2.2.5 + 0
000000003ff8  000400000007 R_X86_64_JUMP_SLO 0000000000000000 add + 0
000000004000  000500000007 R_X86_64_JUMP_SLO 0000000000000000 multiply + 0
000000004008  000700000007 R_X86_64_JUMP_SLO 0000000000000000 factorial + 0

# .rela.plt 包含了需要通过 PLT 调用的函数
# add, multiply, factorial 都在其中

# ========== 扩展：使用 objdump 查看 PLT ==========

$ objdump -d -j .plt main_dynamic

main_dynamic:     file format elf64-x86-64

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	ff 35 b2 2f 00 00    	push   0x2fb2(%rip)        # 3fd8 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	ff 25 b4 2f 00 00    	jmp    *0x2fb4(%rip)        # 3fe0 <_GLOBAL_OFFSET_TABLE_+0x10>
    102c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000000001030 <printf@plt>:
    1030:	ff 25 b2 2f 00 00    	jmp    *0x2fb2(%rip)        # 3fe8 <printf@GLIBC_2.2.5>
    1036:	68 00 00 00 00       	push   $0x0
    103b:	e9 e0 ff ff ff       	jmp    1020 <.plt>

0000000000001040 <add@plt>:
    1040:	ff 25 aa 2f 00 00    	jmp    *0x2faa(%rip)        # 3ff0 <add>
    1046:	68 01 00 00 00       	push   $0x1
    104b:	e9 d0 ff ff ff       	jmp    1020 <.plt>

# PLT 条目：每个外部函数都有一个 PLT 条目
# 第一次调用会触发动态链接器解析地址
```

## 答案总结

### 任务 1: 文件大小对比

| 文件 | 大小 | 说明 |
|------|------|------|
| libmath.a | 2.1KB | 静态库（归档文件） |
| libmath.so | 16KB | 动态库（包含调试信息） |
| main_static | 17KB | 静态链接（包含库代码） |
| main_dynamic | 16KB | 动态链接（不包含库代码） |

**text 段对比**:
- 静态版本: 2156 字节（包含 add, multiply, factorial 代码）
- 动态版本: 1543 字节（不包含库代码）
- 差异: 613 字节（库代码大小）

### 任务 2: 符号表分析

**internal_helper 符号**:
```
静态库: 000000000012 t internal_helper
动态库: (不出现)
```
- 类型 `t` 表示局部函数（static）
- 动态库不导出 static 符号

**add 符号**:
```
静态版本: 0000000000401196 T add    (已解析)
动态版本:                  U add    (未定义)
```
- 静态版本：符号已解析，地址确定
- 动态版本：符号未定义，运行时解析

### 任务 3: 动态库依赖

**静态版本**:
```
只依赖 libc.so.6（系统 C 库）
不依赖 libmath（已静态链接）
```

**动态版本**:
```
依赖 libmath.so（我们的库）
依赖 libc.so.6（系统 C 库）
```

**如果删除 libmath.so**:
```
动态版本无法运行：
error while loading shared libraries: libmath.so: cannot open shared object file
```

### 任务 4: GDB 观察符号

**静态版本**:
- `add` 地址: `0x401196` (低地址，代码段)
- 来源: 可执行文件本身
- 符号: `add in section .text of main_static`

**动态版本**:
- `add` 地址: `0x7ffff7fc5169` (高地址，共享库)
- 来源: `libmath.so`
- 符号: `add in section .text of ./libmath.so`

**关键差异**:
- 静态：绝对地址，编译时确定
- 动态：运行时地址，加载时分配

### 任务 5: ELF 结构分析

**动态版本特有的段**:

| 段名 | 作用 |
|------|------|
| `.interp` | 动态链接器路径 `/lib64/ld-linux-x86-64.so.2` |
| `.plt` | 过程链接表（函数调用跳转） |
| `.got.plt` | 全局偏移表（存储函数地址） |
| `.dynamic` | 动态链接信息 |
| `.dynsym` | 动态符号表 |

**DT_NEEDED 项**:
```
(NEEDED) Shared library: [libmath.so]
(NEEDED) Shared library: [libc.so.6]
```

## 关键概念总结

### 静态链接优缺点

**优点**:
- ✅ 无运行时依赖
- ✅ 加载速度快（无需解析符号）
- ✅ 部署简单（单个文件）

**缺点**:
- ❌ 文件体积大
- ❌ 内存浪费（每个进程独立副本）
- ❌ 升级困难（需重新链接）

### 动态链接优缺点

**优点**:
- ✅ 文件体积小
- ✅ 内存共享（多进程共用一份）
- ✅ 易于升级（只需替换 .so）

**缺点**:
- ❌ 运行时依赖
- ❌ 启动稍慢（需解析符号）
- ❌ "DLL Hell"（版本冲突）

### 符号解析时机

| 链接方式 | 解析时机 | 地址类型 |
|----------|----------|----------|
| 静态链接 | 链接时 | 绝对地址 |
| 动态链接 | 运行时 | 相对地址（PIC） |

## 实用技巧

### 查看库的导出符号

```bash
nm -D libmath.so | grep " T "    # 导出的函数
nm -D libmath.so | grep " D "    # 导出的数据
```

### 强制动态链接特定库

```bash
gcc -Wl,-Bdynamic -lmath -o main  # 动态链接 libmath
gcc -Wl,-Bstatic -lmath -o main   # 静态链接 libmath
```

### 查看链接器的详细过程

```bash
gcc -Wl,--verbose main.c -lmath -o main 2>&1 | less
```

### 检查符号冲突

```bash
nm main | sort
nm libmath.so | sort
```

完成本练习后，你已经掌握了链接的基础知识！下一步：深入符号表分析。
