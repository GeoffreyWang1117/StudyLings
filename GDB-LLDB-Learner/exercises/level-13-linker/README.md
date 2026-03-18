# Level 13: 链接器与符号解析

本级别深入探讨链接器（Linker）的工作原理，帮助你理解程序从源代码到可执行文件的完整过程。

## 学习目标

- 理解编译和链接的区别
- 掌握静态链接和动态链接的原理
- 学习符号表的结构和符号解析过程
- 理解 PLT/GOT 机制
- 使用调试器观察链接过程

## 为什么学习链接器？

链接器是编译工具链中容易被忽视但非常重要的一环：

1. **理解错误信息**: "undefined reference" 是什么意思？
2. **优化程序**: 静态链接 vs 动态链接的性能差异
3. **调试技巧**: 符号冲突、版本问题的排查
4. **逆向工程**: 理解二进制文件的结构
5. **系统编程**: 共享库、插件系统的实现

## 编译链接流程

```
源代码 (.c)
    ↓ [编译器 gcc -c]
目标文件 (.o)
    ↓ [链接器 ld / gcc]
可执行文件 或 共享库 (.so)
    ↓ [加载器 ld.so]
运行时内存
```

## 练习列表

### Exercise 1: 静态链接 vs 动态链接

**学习内容**:
- `.o` (目标文件)、`.a` (静态库)、`.so` (共享库) 的区别
- 静态链接和动态链接的过程
- 使用 `ldd` 查看依赖
- 使用 `nm` 查看符号

**关键命令**:
```bash
gcc -c file.c           # 编译不链接
ar rcs libfoo.a foo.o   # 创建静态库
gcc -shared -fPIC -o libfoo.so foo.c  # 创建共享库
ldd ./program           # 查看动态库依赖
nm program              # 查看符号表
```

### Exercise 2: 符号表和符号解析

**学习内容**:
- 符号的类型（T, D, B, U, W等）
- 强符号和弱符号
- 符号可见性（static, extern, __attribute__((visibility))）
- 符号冲突的解决
- 使用 `readelf` 深入分析

**关键命令**:
```bash
nm -C program           # 查看符号（C++ demangle）
readelf -s program      # 查看符号表详情
objdump -t program      # 查看符号表
c++filt _Z3foov         # C++ 符号还原
```

### Exercise 3: PLT/GOT 和延迟绑定

**学习内容**:
- PLT (Procedure Linkage Table) 的作用
- GOT (Global Offset Table) 的作用
- 延迟绑定（Lazy Binding）机制
- 使用 GDB 观察函数第一次调用
- `LD_PRELOAD` 劫持技巧

**关键命令**:
```bash
objdump -d -j .plt program      # 查看 PLT
readelf -r program              # 查看重定位表
LD_DEBUG=bindings ./program     # 显示绑定过程
LD_PRELOAD=./my.so ./program    # 预加载库
```

## 内存布局（链接视角）

### 目标文件（.o）

```
┌─────────────────────┐
│   ELF Header        │
├─────────────────────┤
│   .text (代码)      │  未解析的外部引用
├─────────────────────┤
│   .data (数据)      │  初始化数据
├─────────────────────┤
│   .bss (BSS)        │  未初始化数据
├─────────────────────┤
│   .symtab (符号表)  │  所有符号
├─────────────────────┤
│   .rel.text (重定位)│  需要重定位的位置
└─────────────────────┘
```

### 可执行文件（静态链接）

```
┌─────────────────────┐
│   ELF Header        │
├─────────────────────┤
│   .text (代码)      │  所有符号已解析
├─────────────────────┤
│   .rodata           │  只读数据
├─────────────────────┤
│   .data             │  初始化数据
├─────────────────────┤
│   .bss              │  未初始化数据
├─────────────────────┤
│   .symtab           │  符号表（调试用）
└─────────────────────┘
```

### 可执行文件（动态链接）

```
┌─────────────────────┐
│   ELF Header        │
├─────────────────────┤
│   .interp           │  动态链接器路径
├─────────────────────┤
│   .plt              │  过程链接表
├─────────────────────┤
│   .got.plt          │  全局偏移表
├─────────────────────┤
│   .text (代码)      │  部分符号待运行时解析
├─────────────────────┤
│   .dynamic          │  动态链接信息
├─────────────────────┤
│   .dynsym           │  动态符号表
└─────────────────────┘
```

## 符号类型速查表

| 符号 | 类型 | 说明 | 示例 |
|------|------|------|------|
| T | Text | 全局函数（代码段） | `main`, `printf` |
| t | text | 局部函数（static） | `static void helper()` |
| D | Data | 全局变量（.data） | `int global = 42;` |
| d | data | 局部变量（static .data） | `static int var = 10;` |
| B | BSS | 全局未初始化变量 | `int uninit;` |
| b | bss | 局部未初始化变量 | `static int uninit;` |
| U | Undefined | 未定义（外部引用） | `extern int foo;` |
| W | Weak | 弱符号 | `__attribute__((weak))` |
| R | Read-only | 只读数据（.rodata） | `const char *str = "hi";` |

## 调试链接问题

### 常见链接错误

1. **undefined reference to 'xxx'**
   - 符号未定义
   - 缺少库文件
   - 链接顺序错误

2. **multiple definition of 'xxx'**
   - 符号重复定义
   - 头文件包含了定义（而非声明）

3. **cannot find -lxxx**
   - 找不到库文件
   - 库文件路径未指定

### 调试方法

```bash
# 1. 检查未定义的符号
nm -u program

# 2. 检查库中的符号
nm -D /usr/lib/libxxx.so

# 3. 查看链接的详细过程
gcc -Wl,--verbose main.c

# 4. 查看运行时库加载
LD_DEBUG=libs ./program
LD_DEBUG=symbols ./program
```

## 学习路径

### 前置知识
- Level 7: 内存段（.text, .data, .bss）
- Level 12: 内存布局

### 本级别
- Exercise 1: 理解静态和动态链接的区别
- Exercise 2: 掌握符号表的分析
- Exercise 3: 深入 PLT/GOT 机制

### 后续学习
- 操作系统加载器（Loader）
- 共享库版本管理
- 位置无关代码（PIC）

## 实用工具

### 分析工具

| 工具 | 用途 | 示例 |
|------|------|------|
| `nm` | 查看符号表 | `nm program` |
| `ldd` | 查看动态库依赖 | `ldd program` |
| `readelf` | 查看 ELF 文件结构 | `readelf -h program` |
| `objdump` | 反汇编和查看段 | `objdump -d program` |
| `file` | 查看文件类型 | `file program` |
| `strings` | 提取字符串 | `strings program` |
| `size` | 查看段大小 | `size program` |
| `ar` | 操作静态库 | `ar t libfoo.a` |
| `ld` | 链接器 | `ld -o program obj.o` |

### 环境变量

| 变量 | 作用 | 示例 |
|------|------|------|
| `LD_LIBRARY_PATH` | 共享库搜索路径 | `LD_LIBRARY_PATH=/opt/lib` |
| `LD_PRELOAD` | 预加载库 | `LD_PRELOAD=./hook.so` |
| `LD_DEBUG` | 调试动态链接 | `LD_DEBUG=all` |
| `LD_BIND_NOW` | 禁用延迟绑定 | `LD_BIND_NOW=1` |

## 最佳实践

### 编译时
1. 使用 `-fPIC` 编译共享库
2. 使用 `-fvisibility=hidden` 隐藏内部符号
3. 使用版本脚本控制导出符号

### 链接时
1. 静态库放在命令行最后
2. 注意链接顺序（被依赖的在后）
3. 使用 `-Wl,--as-needed` 避免不必要的依赖

### 运行时
1. 使用 `rpath` 而非 `LD_LIBRARY_PATH`
2. 避免全局符号污染
3. 正确处理符号版本

## 总结

完成本级别后，你将掌握：

1. ✅ 编译和链接的完整流程
2. ✅ 静态链接和动态链接的原理
3. ✅ 符号表的结构和符号解析
4. ✅ PLT/GOT 延迟绑定机制
5. ✅ 使用工具分析链接问题
6. ✅ 调试器中观察链接过程

**链接器知识是系统级编程的基石！**
