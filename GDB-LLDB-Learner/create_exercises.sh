#!/bin/bash

# 批量创建练习的辅助脚本

# Level 3 Exercise 3
cat > exercises/level-03-execution/exercise-3/recursion.c << 'EOF'
#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

int main() {
    printf("斐波那契数列\n");
    for (int i = 0; i <= 6; i++) {
        printf("fib(%d) = %d\n", i, fibonacci(i));
    }
    return 0;
}
EOF

cat > exercises/level-03-execution/exercise-3/Makefile << 'EOF'
CC = gcc
CFLAGS = -g -Wall -Wextra
TARGET = recursion
SRC = recursion.c

all: $(TARGET)
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
EOF

cat > exercises/level-03-execution/exercise-3/problem.md << 'EOF'
# Exercise 3: 调试递归函数

## 目标
学习如何调试递归函数，理解调用栈深度。

## 任务
使用调试器：
1. 在递归函数设置断点
2. 使用 backtrace 查看调用栈
3. 在不同深度查看变量值
4. 使用 finish 快速返回

## 提示
- 使用条件断点避免停太多次：`break fibonacci if n == 3`
- 使用 `backtrace` 查看递归深度
- 使用 `frame N` 切换到不同调用层
EOF

cat > exercises/level-03-execution/exercise-3/solution.md << 'EOF'
# Exercise 3: 解决方案

## 调试递归函数

```bash
gdb ./recursion
(gdb) break fibonacci if n == 3
(gdb) run
(gdb) backtrace
#0  fibonacci (n=3) at recursion.c:4
#1  fibonacci (n=4) at recursion.c:5
#2  fibonacci (n=5) at recursion.c:5
#3  main () at recursion.c:11

(gdb) frame 1
(gdb) print n
$1 = 4

(gdb) finish  # 返回到上一层
```

## 技巧
- 递归深度可能很大，使用条件断点
- 使用 `bt` 理解调用关系
- 使用 `finish` 快速返回上层
EOF

# Level 4 Exercises
mkdir -p exercises/level-04-variables/exercise-{2,3}

cat > exercises/level-04-variables/exercise-2/watchpoint.c << 'EOF'
#include <stdio.h>

int global_var = 0;

void modify_value(int *ptr) {
    *ptr = 100;
}

int main() {
    int local_var = 10;
    printf("初始值: %d\n", local_var);

    local_var = 20;
    modify_value(&local_var);
    global_var = 50;

    printf("最终值: local=%d, global=%d\n", local_var, global_var);
    return 0;
}
EOF

cat > exercises/level-04-variables/exercise-2/Makefile << 'EOF'
CC = gcc
CFLAGS = -g -Wall -Wextra
TARGET = watchpoint
SRC = watchpoint.c

all: $(TARGET)
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)
clean:
	rm -f $(TARGET)
.PHONY: all clean
EOF

cat > exercises/level-04-variables/exercise-2/problem.md << 'EOF'
# Exercise 2: 使用监视点(Watchpoints)

## 目标
学习使用 watchpoints 监控变量何时被修改。

## 任务
设置监视点，找出变量在何处被修改。

## 命令
**GDB:**
```
(gdb) watch local_var
(gdb) watch global_var
(gdb) info watchpoints
```

**LLDB:**
```
(lldb) watchpoint set variable local_var
(lldb) watchpoint list
```
EOF

cat > exercises/level-04-variables/exercise-2/solution.md << 'EOF'
# Exercise 2: 解决方案

## GDB 完整会话

```bash
gdb ./watchpoint
(gdb) break main
(gdb) run
(gdb) next  # 执行到 local_var 定义后
(gdb) watch local_var
Hardware watchpoint 2: local_var

(gdb) continue
Hardware watchpoint 2: local_var
Old value = 10
New value = 20

(gdb) backtrace  # 查看在哪里修改的

(gdb) continue
Hardware watchpoint 2: local_var
Old value = 20
New value = 100
```

## 监视点类型
- `watch`: 写监视点（变量被修改时停止）
- `rwatch`: 读监视点（GDB，变量被读取时停止）
- `awatch`: 访问监视点（读或写时都停止）

## 注意事项
- 监视点会降低程序速度
- 局部变量离开作用域后监视点自动删除
- 硬件监视点数量有限（通常 4 个）
EOF

echo "练习文件创建完成！"
