## 提示 1
先看 stderr 里 libbpf 打印的 verifier log，最后几行形如
`invalid access to packet, off=23 size=1, R7(id=0,off=23,r=14)`：
off=23 是 `ip->protocol`（14 字节以太网头 + 9），`r=14` 表示验证器目前只"证明过"前 14 字节可读。
验证器对每个包指针跟踪"已证明安全的范围"，只有 `if (ptr + len > data_end) return ...;` 这样的比较能扩大它。

## 提示 2
```c
struct iphdr *ip = (void *)(eth + 1);
if ((void *)(ip + 1) > data_end)
    return P_OTHER;
```
注意比较的是 `ip + 1`（整个 20 字节的 IP 头的末尾），而不是 `ip`。
（带 IP 选项时真正的头长是 `ip->ihl * 4`，访问 L4 头前还得再做一次检查。）

## 提示 3
程序能加载以后，如果计数偏少：`BPF_MAP_TYPE_PERCPU_ARRAY` 每个 CPU 一份 value，
`bpf_map__lookup_elem` 一次返回 `libbpf_num_possible_cpus()` 份（每份按 8 字节对齐），
用户态要循环把 `vals[cpu].packets` / `.bytes` 全部加起来。
这就是 per-CPU map 的取舍：内核侧无锁、无原子操作、不抢 cache line，代价是读的时候要求和。
用 `bpftool map dump name stats` 可以直接看到每个 CPU 的值。
