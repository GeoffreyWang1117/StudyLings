# Level 4: 变量检查与修改

## 学习目标

- 打印和检查变量
- 修改变量值
- 使用监视点（watchpoints）
- 查看复杂数据结构

## 核心命令

### GDB 命令
```bash
print var               # 打印变量（简写：p）
print/x var             # 以十六进制打印
print/d var             # 以十进制打印
ptype var               # 显示变量类型
whatis var              # 显示变量类型（简短）
info locals             # 显示所有局部变量
info args               # 显示函数参数
set var x = 10          # 修改变量值
display var             # 每次停止时自动显示变量
watch var               # 设置监视点（变量改变时中断）
```

### LLDB 命令
```bash
print var / p var       # 打印变量
print/x var             # 以十六进制打印
expr var = 10           # 修改变量值
frame variable          # 显示所有局部变量（简写：fr v）
frame variable -a       # 显示参数
type lookup var         # 显示变量类型
watchpoint set variable var  # 设置监视点
```

## 练习列表

### Exercise 1: 变量检查
学习打印和检查各种类型的变量。

### Exercise 2: 修改变量
学习在运行时修改变量值来改变程序行为。

### Exercise 3: 监视点
学习使用 watchpoints 监控变量变化。

## 快速参考

| 功能 | GDB | LLDB |
|------|-----|------|
| 打印变量 | `print var` | `p var` |
| 修改变量 | `set var x=10` | `expr x=10` |
| 查看类型 | `ptype var` | `type lookup` |
| 局部变量 | `info locals` | `fr v` |
| 监视点 | `watch var` | `wa s v var` |
