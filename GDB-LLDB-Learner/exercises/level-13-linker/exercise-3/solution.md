# Exercise 3: PLT/GOT 和延迟绑定 - 参考答案

## 关键答案总结

### 任务 1: PLT/GOT 结构

```bash
$ objdump -d -j .plt pltgot | grep "printf@plt" -A 3
0000000000001030 <printf@plt>:
    1030:	ff 25 ca 2f 00 00    	jmp    *0x2fca(%rip)  # 4000 <printf@GLIBC_2.2.5>
    1036:	68 00 00 00 00       	push   $0x0
    103b:	e9 e0 ff ff ff       	jmp    1020 <.plt>

# jmp *0x2fca(%rip) → 间接跳转到 GOT 表项
# push $0x0 → 压入符号索引
# jmp 1020 → 跳转到公共 PLT 解析代码
```

### 任务 2: GDB 观察

```gdb
(gdb) break printf@plt
Breakpoint 1 at 0x1030

(gdb) run
Breakpoint 1, 0x0000555555555030 in printf@plt ()

# 第一次调用前查看 GOT
(gdb) x/gx 0x555555558000  # printf@got.plt
0x555555558000: 0x0000555555555036

# GOT 初始值指向 PLT 中的 push 指令（延迟绑定）

(gdb) finish
# 执行完 printf

(gdb) x/gx 0x555555558000
0x555555558000: 0x00007ffff7e1e5f0

# GOT 已更新为 printf 的实际地址（libc 中）
```

### 任务 3: LD_DEBUG 输出

```bash
$ LD_DEBUG=bindings ./pltgot 2>&1 | grep printf
binding file ./pltgot [0] to /lib/x86_64-linux-gnu/libc.so.6 [0]: normal symbol `printf' [GLIBC_2.2.5]
```

### 任务 4: LD_PRELOAD 劫持

```bash
$ LD_PRELOAD=./hook.so ./pltgot
[HOOK] malloc(100) = 0x555555559260
[HOOK] free(0x555555559260)
```

## PLT/GOT 工作流程图

```
第一次调用 printf:
  call printf
    ↓
  printf@plt:
    jmp *GOT[printf]  → 指向 PLT+6 (push)
    ↓
  push $0             → 符号索引
    ↓
  jmp PLT0            → 动态链接器入口
    ↓
  _dl_runtime_resolve → 解析 printf 地址
    ↓
  GOT[printf] = 真实地址
    ↓
  跳转到 printf

第二次调用 printf:
  call printf
    ↓
  printf@plt:
    jmp *GOT[printf]  → 直接跳转到 printf (已解析)
    ↓
  printf              → 执行
```

## 性能对比

| 模式 | 启动时间 | 首次调用 | 后续调用 |
|------|---------|---------|---------|
| 延迟绑定 | 快 | 慢（需解析） | 快 |
| 立即绑定 | 慢 | 快 | 快 |

## LD_PRELOAD 实用示例

```c
// 内存泄漏检测
void* malloc(size_t size) {
    void *ptr = dlsym(RTLD_NEXT, "malloc")(size);
    记录分配(ptr, size);
    return ptr;
}

// 性能分析
int printf(const char *fmt, ...) {
    记录调用次数();
    return 真实的printf(fmt, ...);
}
```

完整详细调试会话请参考 problem.md 中的步骤。
