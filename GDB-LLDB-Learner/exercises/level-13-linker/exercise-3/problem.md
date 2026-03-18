# Exercise 3: PLT/GOT 和延迟绑定

## 学习目标

- 理解 PLT (Procedure Linkage Table) 的作用
- 掌握 GOT (Global Offset Table) 的工作原理
- 学习延迟绑定（Lazy Binding）机制
- 使用 GDB 观察函数第一次调用的解析过程
- 掌握 LD_PRELOAD 劫持技巧

## 背景知识

### PLT/GOT 机制

**问题**: 动态链接的函数地址在编译时未知，运行时才能确定。

**解决方案**: PLT + GOT 间接跳转

```
程序调用 printf
    ↓
跳转到 printf@plt (PLT 条目)
    ↓
间接跳转 *GOT[printf] (GOT 表项)
    ↓
第一次: 跳转到动态链接器 → 解析 printf 地址 → 更新 GOT
第二次及以后: 直接跳转到 printf (已解析)
```

### PLT 条目结构

```asm
printf@plt:
    jmp    *printf@got      ; 间接跳转到 GOT 中的地址
    push   $index           ; 压入符号索引
    jmp    PLT0             ; 跳转到公共 PLT 解析代码
```

### 延迟绑定流程

**第一次调用 printf**:
```
1. 程序调用 printf@plt
2. jmp *GOT[printf] → 初始值指向 PLT 下一条指令
3. push 符号索引
4. 调用动态链接器 _dl_runtime_resolve
5. 解析 printf 地址，更新 GOT[printf]
6. 跳转到真正的 printf
```

**第二次调用 printf**:
```
1. 程序调用 printf@plt
2. jmp *GOT[printf] → 已解析的地址
3. 直接执行 printf（无需解析）
```

## 任务

### 任务 1: 查看 PLT 和 GOT

**目标**: 使用 objdump 查看 PLT/GOT 结构

**步骤**:
```bash
make all

# 查看 PLT
objdump -d -j .plt pltgot

# 查看 GOT
objdump -s -j .got.plt pltgot

# 查看重定位表
readelf -r pltgot | grep plt
```

**问题**:
- `printf@plt` 的地址是什么？
- `printf@plt` 的第一条指令是什么？
- GOT 表的初始值是什么？

### 任务 2: GDB 观察延迟绑定

**目标**: 在调试器中观察第一次函数调用

**步骤**:
```bash
gdb pltgot
(gdb) break printf@plt
(gdb) run
(gdb) disassemble
(gdb) x/gx printf@got.plt
(gdb) stepi  # 单步执行
(gdb) continue
(gdb) x/gx printf@got.plt  # 再次查看 GOT
```

**问题**:
- 第一次调用前，GOT 中的值是什么？
- 第一次调用后，GOT 中的值变成什么？
- 第二次调用时还会进入动态链接器吗？

### 任务 3: 使用 LD_DEBUG 查看绑定

**目标**: 观察符号绑定过程

**步骤**:
```bash
make run-debug
```

**问题**:
- 哪些符号被绑定了？
- 绑定到的地址是什么？
- 哪些库提供了这些符号？

### 任务 4: LD_PRELOAD 函数劫持

**目标**: 使用 LD_PRELOAD 替换库函数

**步骤**:
```bash
make run-hook
```

**问题**:
- `malloc` 被劫持了吗？
- Hook 库如何调用真正的 `malloc`？
- 这个技术有什么实际用途？

### 任务 5: 禁用延迟绑定

**目标**: 对比延迟绑定和立即绑定

**步骤**:
```bash
# 延迟绑定（默认）
./pltgot

# 立即绑定
LD_BIND_NOW=1 ./pltgot
```

在 GDB 中对比两种模式的行为。

## 编译和运行

```bash
make all          # 编译所有
make run-normal   # 正常运行
make run-eager    # 禁用延迟绑定
make run-hook     # 使用 Hook
make run-debug    # 显示绑定过程
make analyze      # 分析 PLT/GOT
```

## 调试提示

### GDB 命令

```gdb
# 在 PLT 条目设置断点
break printf@plt

# 查看 GOT 表项
x/gx &printf@got.plt

# 查看 PLT 代码
disassemble 'printf@plt'

# 单步进入动态链接器
stepi
```

### 环境变量

```bash
LD_DEBUG=bindings ./program    # 显示符号绑定
LD_DEBUG=libs ./program         # 显示库加载
LD_DEBUG=symbols ./program      # 显示符号查找
LD_DEBUG=all ./program          # 显示所有调试信息
LD_BIND_NOW=1 ./program         # 禁用延迟绑定
LD_PRELOAD=./hook.so ./program  # 预加载库
```

## 实际应用

### 1. 性能优化

```bash
# 对于启动时间敏感的程序，使用延迟绑定
# 对于实时性要求高的程序，使用立即绑定
LD_BIND_NOW=1 ./realtime_app
```

### 2. 函数劫持（调试/测试）

```c
// hook.c - 劫持 malloc 以检测内存泄漏
void* malloc(size_t size) {
    void *ptr = real_malloc(size);
    log_allocation(ptr, size);
    return ptr;
}
```

### 3. 安全审计

使用 `LD_PRELOAD` 监控系统调用。

## 关键概念

- **PLT**: 代码段中的跳转表，每个外部函数一个条目
- **GOT**: 数据段中的地址表，存储函数的实际地址
- **延迟绑定**: 首次调用时才解析地址（提高启动速度）
- **LD_PRELOAD**: 预加载库，可劫持函数调用

## 总结

完成本练习后，你应该掌握：

1. ✅ PLT/GOT 的工作原理
2. ✅ 延迟绑定的流程
3. ✅ 使用 GDB 观察动态解析
4. ✅ 使用 LD_DEBUG 调试动态链接
5. ✅ 使用 LD_PRELOAD 劫持函数

**你已经完成了链接器专题的学习！**
