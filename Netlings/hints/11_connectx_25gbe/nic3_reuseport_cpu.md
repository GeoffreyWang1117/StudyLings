## 提示 1
每个 worker 自己的监听 socket 在 `bind` **之前**必须
`setsockopt(fd, SOL_SOCKET, SO_REUSEPORT, &one, sizeof one)`。同一个端口上所有 socket 都设了它
（并且属于同一个有效 UID），内核才允许它们一起 bind，并把它们组成一个 reuseport 组。

## 提示 2
绑核：
```c
cpu_set_t set; CPU_ZERO(&set); CPU_SET(w->cpu, &set);
w->pin_err = pthread_setaffinity_np(pthread_self(), sizeof set, &set);  // 返回错误码，不设 errno
```
在线程**开始 accept 之前**绑好（本题用 barrier 保证 main 打印 listening 时所有 worker 都已绑定）。

## 提示 3
Classic BPF 的 reuseport 程序返回值 = 组内 socket 下标。完整程序（n 个 worker）：
```
ld  [SKF_AD_OFF + SKF_AD_CPU]     ; A = 当前 CPU
jeq #cpus[0], 0, 1  ;  ret #0
jeq #cpus[1], 0, 1  ;  ret #1
...
ret #n                            ; 越界 → 内核用哈希兜底
```
`BPF_JUMP(code, k, jt, jf)`：jt/jf 是"相等/不等时再跳过几条指令"。
