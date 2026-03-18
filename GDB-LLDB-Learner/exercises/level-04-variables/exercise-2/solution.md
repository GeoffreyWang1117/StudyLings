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
