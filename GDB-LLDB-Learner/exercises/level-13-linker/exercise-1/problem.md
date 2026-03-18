# Exercise 1: 静态链接 vs 动态链接

## 学习目标

- 理解静态库 (.a) 和动态库 (.so) 的区别
- 掌握链接器的符号解析过程
- 学习使用 nm, ldd, readelf 等工具
- 对比静态链接和动态链接的优缺点
- 在调试器中观察符号来源

## 背景知识

### 静态链接

```
源代码 → 目标文件 (.o) → 静态库 (.a) → 可执行文件
                          ↓
                    所有代码都被复制到可执行文件中
```

**特点**:
- 库代码被完整复制到可执行文件
- 文件体积大
- 运行时无需库文件
- 升级库需要重新链接

### 动态链接

```
源代码 → 目标文件 (.o) → 动态库 (.so) → 可执行文件
                          ↓
                    仅记录符号引用，运行时加载
```

**特点**:
- 可执行文件只包含符号引用
- 文件体积小
- 运行时需要库文件
- 多个程序共享同一库副本
- 升级库不需要重新编译程序

### 链接过程

1. **符号解析**: 将每个符号引用与符号定义关联
2. **重定位**: 修改代码和数据段中的地址

## 任务

### 任务 1: 创建和比较两种链接方式

**目标**: 构建静态链接和动态链接版本

**步骤**:
1. 编译并构建两个版本：
   ```bash
   make both
   ```
2. 查看文件大小
3. 比较两者的差异

**问题**:
- 静态链接和动态链接的可执行文件大小差多少？
- 静态库 (.a) 和动态库 (.so) 的大小？
- 为什么会有这样的差异？

### 任务 2: 分析符号表

**目标**: 使用 nm 查看符号

**步骤**:
1. 查看库中的符号：
   ```bash
   nm libmath.a
   nm -D libmath.so
   ```
2. 查看可执行文件的符号：
   ```bash
   nm main_static | grep -E "(add|multiply|factorial)"
   nm main_dynamic | grep -E "(add|multiply|factorial)"
   ```
3. 查看未定义符号：
   ```bash
   nm -u main_dynamic
   ```

**问题**:
- `internal_helper` 符号的类型是什么？为什么？
- 静态链接版本中是否包含 `add` 符号？
- 动态链接版本中 `add` 是什么类型的符号？
- 为什么动态版本有 undefined 符号？

### 任务 3: 查看动态库依赖

**目标**: 使用 ldd 查看依赖

**步骤**:
1. 查看静态链接版本：
   ```bash
   ldd main_static
   ```
2. 查看动态链接版本：
   ```bash
   ldd main_dynamic
   ```
3. 设置 LD_LIBRARY_PATH 运行：
   ```bash
   LD_LIBRARY_PATH=. ./main_dynamic
   ```

**问题**:
- 静态版本依赖哪些库？
- 动态版本依赖 libmath.so 吗？
- 如果删除 libmath.so，动态版本还能运行吗？

### 任务 4: 在 GDB 中观察符号

**目标**: 使用调试器查看符号来源

**步骤**:
1. 调试静态链接版本：
   ```bash
   gdb main_static
   (gdb) break add
   (gdb) run
   (gdb) info symbol add
   (gdb) disassemble add
   ```
2. 调试动态链接版本：
   ```bash
   gdb main_dynamic
   (gdb) break add
   (gdb) run
   (gdb) info symbol add
   (gdb) info sharedlibrary
   ```

**问题**:
- `add` 函数的地址是什么？
- 静态版本和动态版本的地址有何不同？
- 动态版本从哪个库加载了 `add`？

### 任务 5: 使用 readelf 深入分析

**目标**: 查看 ELF 文件结构

**步骤**:
1. 查看文件头：
   ```bash
   readelf -h main_static
   readelf -h main_dynamic
   ```
2. 查看段头：
   ```bash
   readelf -S main_static
   readelf -S main_dynamic
   ```
3. 查看动态段：
   ```bash
   readelf -d main_dynamic
   ```

**问题**:
- 动态版本有 `.interp` 段吗？它是什么？
- 动态版本的 `DT_NEEDED` 项指向哪些库？
- 静态版本和动态版本的段数量差多少？

## 编译和运行

```bash
# 构建所有版本
make both

# 运行静态链接版本
./main_static

# 运行动态链接版本（需要库在当前目录或系统路径）
LD_LIBRARY_PATH=. ./main_dynamic

# 分析
make analyze

# 清理
make clean
```

## 预期输出

```bash
$ make both
静态库创建完成: libmath.a
静态链接可执行文件: main_static
   text    data     bss     dec     hex filename
   2156     608       8    2772     ad4 main_static

动态库创建完成: libmath.so
动态链接可执行文件: main_dynamic
   text    data     bss     dec     hex filename
   1543     608       8    2159     86f main_dynamic

=== 文件大小对比 ===
-rwxr-xr-x 1 user user 17K main_static
-rwxr-xr-x 1 user user 16K main_dynamic
-rw-r--r-- 1 user user 2.1K libmath.a
-rwxr-xr-x 1 user user 16K libmath.so
```

## 调试提示

### 查看符号类型

```bash
# T: 代码段全局符号
# t: 代码段局部符号（static）
# D: 数据段全局符号
# U: 未定义（需要链接）
nm main_dynamic
```

### 查看库依赖

```bash
# 查看所需的动态库
ldd main_dynamic

# 查看详细加载过程
LD_DEBUG=libs ./main_dynamic
```

### 查看重定位信息

```bash
# 查看重定位表
readelf -r main_dynamic

# 查看 PLT/GOT 相关
objdump -d -j .plt main_dynamic
```

## 常见问题

### Q: 为什么动态库需要 -fPIC？

A: **PIC** (Position Independent Code) 允许代码在任意内存地址执行，这是共享库必需的，因为：
- 多个进程共享同一库副本
- 库可能被加载到不同的内存地址
- 使用相对寻址而非绝对地址

### Q: 静态库和目标文件有何区别？

A: 静态库 (.a) 是**归档文件**，包含多个目标文件 (.o)：
```bash
ar t libmath.a   # 查看库中的文件
ar x libmath.a   # 提取文件
```

### Q: 如何查看库的版本信息？

A: 使用 `objdump` 或 `readelf`：
```bash
readelf -d libmath.so | grep SONAME
```

## 扩展练习

### 1. 创建自己的库

创建一个简单的字符串处理库：
```c
// strlib.h
char* str_reverse(const char* str);
int str_count_char(const char* str, char c);
```

同时提供静态和动态版本。

### 2. 符号可见性

修改 mathlib.c，使用 `__attribute__((visibility("hidden")))` 隐藏内部函数：
```c
__attribute__((visibility("hidden")))
void internal_helper(void) {
    // ...
}
```

重新编译并观察符号表变化。

### 3. 观察加载过程

使用 `LD_DEBUG` 观察动态链接过程：
```bash
LD_DEBUG=all ./main_dynamic 2>&1 | less
```

### 4. 符号冲突

创建两个库，都定义 `add` 函数，观察链接时的行为。

## 实用技巧

### 强制静态链接所有库

```bash
gcc -static main.c -lmath -o main_full_static
```

### 指定库搜索路径

```bash
gcc main.c -L/path/to/libs -lmath -o main
```

### 运行时库路径 (rpath)

```bash
gcc main.c -L. -lmath -Wl,-rpath,. -o main
```

## 关键概念

- **静态库**: 归档文件，包含 .o 文件，链接时复制代码
- **动态库**: 运行时加载，多个进程共享
- **符号表**: 记录所有符号（函数、变量）的名称和地址
- **PIC**: 位置无关代码，允许代码在任意地址执行
- **重定位**: 链接时或运行时修正地址引用

## 总结

完成本练习后，你应该掌握：

1. ✅ 静态链接和动态链接的区别
2. ✅ 使用 nm 查看符号表
3. ✅ 使用 ldd 查看动态库依赖
4. ✅ 创建静态库和动态库
5. ✅ 在调试器中观察符号解析
6. ✅ 理解 PIC 的必要性

下一步：学习符号表的深入分析！
