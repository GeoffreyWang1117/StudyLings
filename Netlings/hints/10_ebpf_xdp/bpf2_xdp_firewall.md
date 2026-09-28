## 提示 1
测试里被封的是 9000（0x2328），结果却是 10275（0x2823）收不到包 —— 两个数正好是字节交换关系。
在 x86/arm64（小端）上把包里的 2 字节大端端口直接当 `__u16` 读，得到的就是字节反过来的数。

## 提示 2
包头字段都是网络字节序。要么把包里的值转成主机序再查 map：
```c
__u16 port = bpf_ntohs(udp->dest);
```
要么让 loader 用 `htons(port)` 作 key 写 map、内核侧直接用 `udp->dest` 查 —— 两边约定一致即可。
本题约定 map key 是主机序（`bpftool map dump` 时更好读）。`bpf_ntohs` 对常量会在编译期折叠。

## 提示 3
丢弃计数：HASH map 的 value 被所有 CPU 共享，`(*drops)++` 在多核并发时会丢计数，
要用 `__sync_fetch_and_add(drops, 1)`（编译成 BPF 原子加指令）。高包率下更好的做法是
PERCPU_HASH 或者把计数放到一个 PERCPU_ARRAY 里，就像 bpf1。
