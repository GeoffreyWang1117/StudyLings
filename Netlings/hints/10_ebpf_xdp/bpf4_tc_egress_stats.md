## 提示 1
对端一个包都收不到？看程序的返回值。tc 分类器在 direct-action 模式下，返回值就是动作：
`TC_ACT_OK`（0，放行）、`TC_ACT_SHOT`（2，丢弃）、`TC_ACT_REDIRECT`（7）……
egress 上返回 SHOT 连 ARP 请求都发不出去，于是邻居解析失败，所有 IPv4 包也卡在邻居队列里被丢掉。

## 提示 2
排行里只有本机地址 10.79.0.1？在 egress 方向，`ip->saddr` 是自己，`ip->daddr` 才是"发给谁"。
key 用网络序的 `ip->daddr` 就好，用户态 `inet_ntop(AF_INET, &addr, ...)` 直接能打印，不用转换。

## 提示 3
HASH map 的 value 被所有 CPU 共享：已有条目用 `__sync_fetch_and_add` 累加；第一次见到的地址用
`bpf_map_update_elem(..., BPF_NOEXIST)` 插入，失败（别的 CPU 抢先插入了）再退回 lookup + 原子加。
手动检查挂载状态：`tc filter show dev IFACE egress`、`tc qdisc show dev IFACE`；
等价的命令行做法是 `tc qdisc add dev IFACE clsact` + `tc filter add dev IFACE egress bpf da obj x.bpf.o sec tc`。
