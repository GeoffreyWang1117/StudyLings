# Exercise 2: 解决方案

## GDB 完整操作

```bash
# 编译
make

# 启动 GDB
gdb ./prime_finder

# 1. 设置条件断点：只在 num > 10 时停止
(gdb) break check_prime if num > 10
Breakpoint 1 at 0x1149: file prime_finder.c, line 4.

(gdb) info breakpoints
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x0000000000001149 in check_prime at prime_finder.c:4
        stop only if num > 10

(gdb) run
Starting program: ./prime_finder
质数查找程序
=============

查找 1 到 30 之间的质数:
2 是质数
3 是质数
5 是质数
7 是质数

Breakpoint 1, check_prime (num=11) at prime_finder.c:4
4	    if (num <= 1) return false;

(gdb) print num
$1 = 11

(gdb) continue
11 是质数

Breakpoint 1, check_prime (num=13) at prime_finder.c:4
...

# 2. 修改条件
(gdb) condition 1 num == 17
(gdb) continue
Continuing.

Breakpoint 1, check_prime (num=17) at prime_finder.c:4
(gdb) print num
$2 = 17

# 3. 删除条件（变为普通断点）
(gdb) condition 1
Breakpoint 1 now unconditional.

# 4. 在循环中设置条件断点
(gdb) delete 1
(gdb) break find_primes if i == 15
Breakpoint 2 at 0x11c5: file prime_finder.c, line 21.
(gdb) run
...
Breakpoint 2, find_primes (start=1, end=30) at prime_finder.c:21
21	        if (check_prime(i)) {
(gdb) print i
$3 = 15
```

## LLDB 完整操作

```bash
# 启动 LLDB
lldb ./prime_finder

# 1. 设置条件断点
(lldb) breakpoint set -n check_prime -c 'num > 10'
Breakpoint 1: where = prime_finder`check_prime + 13 at prime_finder.c:4

(lldb) breakpoint list
Current breakpoints:
1: name = 'check_prime', locations = 1
  Condition: num > 10
    1.1: where = prime_finder`check_prime + 13 at prime_finder.c:4

(lldb) run
质数查找程序
=============

查找 1 到 30 之间的质数:
2 是质数
3 是质数
5 是质数
7 是质数
Process 12345 stopped
* thread #1, stop reason = breakpoint 1.1
    frame #0: 0x0000000100003f30 prime_finder`check_prime(num=11)

(lldb) p num
(int) $0 = 11

# 2. 修改条件
(lldb) breakpoint modify 1 -c 'num == 17'
(lldb) continue

Process 12345 stopped
* thread #1, stop reason = breakpoint 1.1
    frame #0: prime_finder`check_prime(num=17)

(lldb) p num
(int) $1 = 17

# 3. 删除条件
(lldb) breakpoint modify 1 -c ''
# 或完全删除断点
(lldb) breakpoint delete 1

# 4. 复杂条件
(lldb) breakpoint set -n find_primes -c 'i == 15'
(lldb) run
```

## 关键命令对照

| 操作 | GDB | LLDB |
|------|-----|------|
| 设置条件断点 | `break func if cond` | `b func -c 'cond'` |
| 修改条件 | `condition N cond` | `br modify N -c 'cond'` |
| 删除条件 | `condition N` | `br modify N -c ''` |
| 查看条件 | `info breakpoints` | `br list` |

## 常用条件示例

```c
// 数值比较
i == 100
x > 10 && x < 20
count >= limit

// 指针检查
ptr != NULL
*ptr == 42

// 字符串比较（使用函数）
strcmp(str, "target") == 0

// 复杂逻辑
(flag == 1 || flag == 2) && value > threshold
```

## 技巧总结

1. **循环调试**: 使用条件断点避免手动点击数百次
2. **性能**: 条件断点可能影响性能，条件会在每次执行时求值
3. **表达式**: 条件可以是任何有效的 C 表达式
4. **调试条件**: 如果断点没有触发，检查条件表达式是否正确

## 问题答案

**1. 为什么使用条件断点？**
避免在不关心的情况下反复停止，特别是在循环中。

**2. 条件断点的性能影响？**
每次执行到断点时都会求值条件，可能较慢。对于热点代码考虑使用其他方法。

**3. 如何调试条件断点不工作的情况？**
- 检查变量名拼写
- 确保变量在作用域内
- 使用 `info locals` 检查变量值
- 简化条件进行测试
