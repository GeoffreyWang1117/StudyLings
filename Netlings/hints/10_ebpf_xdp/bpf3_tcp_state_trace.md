## 提示 1
一行事件都没有，先怀疑过滤条件。`cat /sys/kernel/tracing/events/sock/inet_sock_set_state/format`
的 `print fmt` 里 sport/dport 直接按 `%hu` 打印 —— 内核在填 tracepoint 时已经做过 `ntohs`，
它们是**主机字节序**。loader 写进 `target_port` 的也是主机序，两边直接比较即可，不需要 `bpf_htons`。
（对比 bpf2：那里读的是包里的原始 UDP 头，才是网络序。）

## 提示 2
`bpf_ringbuf_reserve` 拿到的内存不会自动清零，所有字段都要填：
```c
__builtin_memcpy(e->saddr, ctx->saddr, 4);
__builtin_memcpy(e->daddr, ctx->daddr, 4);
e->sport = ctx->sport;   e->dport = ctx->dport;
e->oldstate = ctx->oldstate;   e->newstate = ctx->newstate;
```
BPF 里没有 libc，`memcpy` 要写成 `__builtin_memcpy`（长度是常量时 clang 会展开成几条 load/store）。

## 提示 3
观察输出会发现：客户端 `CLOSE -> SYN_SENT` 那一行 sport 是 0 —— connect() 时源端口在状态切换之后才分配；
客户端最后是 `FIN_WAIT2 -> CLOSE` 而不是进入 TIME_WAIT：原 socket 被关闭，TIME_WAIT 由一个轻量的
inet_timewait_sock 接管（`ss -tan state time-wait` 能看到它）。
用 bpftrace 一行实现同样的功能：
`bpftrace -e 'tracepoint:sock:inet_sock_set_state /args->dport == 8080/ { printf("%d -> %d\n", args->oldstate, args->newstate); }'`
