# Exercise 2: 符号表和符号解析 - 参考答案

## 快速答案总结

### 任务 1: 符号类型

```bash
$ nm symbols | grep -E "(weak_|hidden_|static_)"
0000000000404014 W weak_var
0000000000401186 W weak_function
0000000000404018 V hidden_var
0000000000401229 t static_function
```

- `weak_var`: **W** (弱数据符号)
- `static_function`: **t** (局部函数，小写表示 static)
- `hidden_var`: **V** (隐藏符号)

### 任务 2: 符号覆盖

**基本版本**:
```
weak_var = 200 (默认值)
weak_function(5) = 10 (x * 2)
```

**覆盖版本**:
```
weak_var = 300 (external.c 中的强符号覆盖)
weak_function(5) = 15 (x * 3, external.c 中的实现)
```

### 任务 3: readelf 分析

```bash
$ readelf -s symbols | grep weak_var
    58: 0000000000404014     4 OBJECT  WEAK   DEFAULT   24 weak_var

# Bind列：WEAK（弱绑定）
# Vis列：DEFAULT（默认可见性）

$ readelf -s symbols | grep hidden_var
    59: 0000000000404018     4 OBJECT  GLOBAL HIDDEN    24 hidden_var

# Vis列：HIDDEN（隐藏可见性）
```

### 任务 4: GDB 中的符号

```bash
(gdb) info variables weak
All variables matching regular expression "weak":

File symbols.c:
int weak_var;
8:      int weak_var;

(gdb) print weak_var
$1 = 200

(gdb) print hidden_var
$2 = 2

(gdb) info functions static
All functions matching regular expression "static":

File symbols.c:
static void static_function(void);

# static_function 可见但标记为 static
```

## 完整输出示例

```bash
$ make all
gcc -g -Wall -Wextra -O0 symbols.c -o symbols
基本版本构建完成: symbols
gcc -g -Wall -Wextra -O0 symbols.c external.c -o symbols_override
覆盖版本构建完成: symbols_override

$ ./symbols
=== 符号类型演示 ===

强符号和弱符号:
  strong_var = 100
  weak_var = 200
  [默认 weak_function: x=5]
  weak_function(5) = 10

符号可见性:
  public_var = 1
  hidden_var = 2
  static_var = 3

$ ./symbols_override
=== 符号类型演示 ===

强符号和弱符号:
  strong_var = 100
  weak_var = 300
  [覆盖的 weak_function: x=5]
  weak_function(5) = 15

$ make analyze
=== 基本版本符号分析 ===
所有全局符号:
0000000000401050 T _start
0000000000401186 W weak_function
00000000004011d6 T public_function
...

弱符号:
0000000000404014 W weak_var
0000000000401186 W weak_function

静态符号:
0000000000401229 t static_function
0000000000404010 d static_var
```

## 关键概念

### 符号覆盖规则

| 情况 | 结果 |
|------|------|
| 强符号 + 强符号 | ❌ 链接错误 |
| 强符号 + 弱符号 | ✅ 使用强符号 |
| 弱符号 + 弱符号 | ✅ 使用第一个 |

### 可见性层级

```
static (文件内) < hidden (库内) < default (全局)
```

### 符号表分析总结

```bash
# 统计符号类型
$ make symbols
T (全局函数):      8
t (局部函数):      3
D (全局数据):      6
W (弱符号):        2
```

完整详细分析请参考 problem.md 中的步骤说明。
