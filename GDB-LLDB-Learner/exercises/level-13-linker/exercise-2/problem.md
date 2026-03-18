# Exercise 2: 符号表和符号解析

## 学习目标

- 理解符号表的结构
- 掌握不同类型的符号（T, D, B, U, W等）
- 学习强符号和弱符号
- 理解符号可见性（visibility）
- 解决符号冲突问题

## 背景知识

### 符号表

符号表记录程序中所有符号（函数、变量）的信息：
- 符号名称
- 符号类型
- 符号地址
- 符号大小
- 符号绑定（binding）

### 符号类型速查

| 类型 | 说明 | 示例 |
|------|------|------|
| **T** | 全局函数 (Text) | `void foo() {}` |
| **t** | 局部函数 | `static void bar() {}` |
| **D** | 全局已初始化数据 (Data) | `int x = 1;` |
| **d** | 局部已初始化数据 | `static int y = 2;` |
| **B** | 全局未初始化数据 (BSS) | `int z;` |
| **b** | 局部未初始化数据 | `static int w;` |
| **R** | 只读数据 (Rodata) | `const int c = 3;` |
| **U** | 未定义 (Undefined) | `extern int ext;` |
| **W** | 弱符号 (Weak) | `__attribute__((weak))` |

### 强符号 vs 弱符号

**强符号** (Strong Symbol):
- 普通的全局符号
- 多重定义会导致链接错误
- 总是优先于弱符号

**弱符号** (Weak Symbol):
- 使用 `__attribute__((weak))` 声明
- 可以被强符号覆盖
- 用于提供默认实现

```c
// 弱符号（可被覆盖的默认实现）
__attribute__((weak))
void optional_function() {
    printf("默认实现\n");
}

// 强符号（如果存在，会覆盖弱符号）
void optional_function() {
    printf("自定义实现\n");
}
```

### 符号可见性

```c
// 默认：外部可见
int public_var;

// 隐藏：仅库内可见
__attribute__((visibility("hidden")))
int hidden_var;

// 静态：仅文件内可见
static int file_local_var;
```

## 任务

### 任务 1: 查看符号表

**目标**: 使用 nm 和 readelf 分析符号

**步骤**:
1. 编译程序：
   ```bash
   make all
   ```
2. 查看所有符号：
   ```bash
   nm symbols
   ```
3. 查看特定类型的符号：
   ```bash
   nm symbols | grep " T "  # 全局函数
   nm symbols | grep " D "  # 全局数据
   nm symbols | grep " W "  # 弱符号
   ```

**问题**:
- `weak_var` 的符号类型是什么？
- `static_function` 能在符号表中找到吗？
- `hidden_var` 和 `public_var` 有何不同？

### 任务 2: 强符号覆盖弱符号

**目标**: 观察符号覆盖机制

**步骤**:
1. 运行基本版本：
   ```bash
   ./symbols
   ```
   观察 `weak_var` 和 `weak_function` 的值

2. 运行覆盖版本：
   ```bash
   ./symbols_override
   ```
   观察变化

3. 对比符号表：
   ```bash
   nm symbols | grep weak
   nm symbols_override | grep weak
   ```

**问题**:
- 覆盖版本中 `weak_var` 的值是多少？
- `weak_function` 被哪个实现覆盖了？
- 弱符号在符号表中还存在吗？

### 任务 3: 使用 readelf 深入分析

**目标**: 查看符号表的详细信息

**步骤**:
1. 查看符号表：
   ```bash
   readelf -s symbols
   ```
2. 查看特定符号：
   ```bash
   readelf -s symbols | grep weak_var
   ```
3. 查看符号绑定和可见性：
   ```bash
   readelf -s symbols | grep hidden
   ```

**问题**:
- `hidden_var` 的 `Vis` 列是什么？
- `weak_var` 的 `Bind` 列是什么？
- `static_var` 是否出现在动态符号表中？

### 任务 4: 在 GDB 中查找符号

**目标**: 使用调试器查看符号

**步骤**:
1. 启动 GDB：
   ```bash
   gdb symbols
   ```
2. 查找符号：
   ```gdb
   (gdb) info variables weak
   (gdb) info functions static
   (gdb) print weak_var
   (gdb) print 'hidden_var'
   ```

**问题**:
- 能否直接访问 `hidden_var`？
- `static_function` 能否被调用？
- 弱符号的地址是多少？

### 任务 5: 符号冲突实验

**目标**: 理解符号冲突的解决

**步骤**:
1. 尝试定义两个强符号（编辑代码）
2. 观察链接器报错
3. 使用弱符号解决冲突

**问题**:
- 多重定义错误的信息是什么？
- 如何使用弱符号避免冲突？

## 编译和运行

```bash
# 构建两个版本
make all

# 运行基本版本
./symbols

# 运行覆盖版本
./symbols_override

# 分析符号
make analyze

# 符号统计
make symbols
```

## 预期输出

```bash
$ ./symbols
=== 符号类型演示 ===

强符号和弱符号:
  strong_var = 100
  weak_var = 200
  [默认 weak_function: x=5]
  weak_function(5) = 10

$ ./symbols_override
=== 符号类型演示 ===

强符号和弱符号:
  strong_var = 100
  weak_var = 300          # 被覆盖了！
  [覆盖的 weak_function: x=5]
  weak_function(5) = 15   # 被覆盖了！
```

## 调试提示

### nm 常用选项

```bash
nm -C program         # C++ 符号 demangle
nm -D libfoo.so       # 仅显示动态符号
nm -u program         # 仅显示未定义符号
nm --size-sort program # 按大小排序
```

### readelf 查看符号

```bash
readelf -s program    # 符号表
readelf -W -s program # 宽格式（不截断）
readelf -sW program | grep WEAK  # 查找弱符号
```

### 符号绑定类型

| Bind | 说明 |
|------|------|
| GLOBAL | 全局符号 |
| LOCAL | 局部符号 |
| WEAK | 弱符号 |

### 符号可见性

| Vis | 说明 |
|-----|------|
| DEFAULT | 默认可见 |
| HIDDEN | 隐藏（库内部） |
| PROTECTED | 受保护 |

## 实际应用

### 1. 可选功能实现

```c
// 库提供默认实现
__attribute__((weak))
void log_message(const char *msg) {
    // 默认不做任何事
}

// 用户可以提供自己的实现
void log_message(const char *msg) {
    fprintf(stderr, "LOG: %s\n", msg);
}
```

### 2. 测试桩（Test Stub）

```c
// 生产代码
extern int database_query(const char *sql);

// 测试代码提供弱符号实现
__attribute__((weak))
int database_query(const char *sql) {
    return 42;  // 测试时返回模拟数据
}
```

### 3. 插件系统

```c
// 主程序定义弱符号
__attribute__((weak))
void plugin_init(void) {
    // 默认什么都不做
}

// 插件提供强符号实现
void plugin_init(void) {
    // 插件初始化代码
}
```

## 常见问题

### Q: 什么时候使用弱符号？

A:
- 提供可选功能的默认实现
- 允许用户覆盖库函数
- 实现插件机制
- 编写测试代码

### Q: hidden 符号的优势？

A:
- 避免符号污染
- 加快动态链接速度
- 减小符号表大小
- 防止符号冲突

### Q: 如何导出特定符号？

A: 使用版本脚本：
```
# version.map
{
  global:
    public_function;
    public_var;
  local:
    *;
};
```

编译时：`gcc -Wl,--version-script=version.map ...`

## 扩展练习

### 1. 创建符号版本

研究符号版本控制（symbol versioning）

### 2. 分析大型项目

使用 nm 分析真实项目的符号：
```bash
nm /usr/lib/libc.so.6 | less
```

### 3. 符号冲突调试

创建两个库，都定义相同符号，观察链接行为

## 总结

完成本练习后，你应该掌握：

1. ✅ 符号表的结构和类型
2. ✅ 强符号和弱符号的区别
3. ✅ 符号可见性控制
4. ✅ 使用 nm 和 readelf 分析符号
5. ✅ 在调试器中查找符号
6. ✅ 解决符号冲突

下一步：学习 PLT/GOT 机制！
