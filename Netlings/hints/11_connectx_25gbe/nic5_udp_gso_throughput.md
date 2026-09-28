## 提示 1
GSO 只需要一个 socket 选项：
```c
int seg = SEG;   // 每个数据报的负载大小
setsockopt(fd, IPPROTO_UDP, UDP_SEGMENT, &seg, sizeof seg);
```
之后每次 send 的数据只要大于 seg，内核就把它按 seg 切成多个数据报（最后一个可以更短）。
也可以用 cmsg（SOL_UDP, UDP_SEGMENT）逐条指定。

## 提示 2
接收端开了 `UDP_GRO` 后，一次 recvmsg 可能拿到"好几个数据报拼在一起"的 buffer，
每条消息的 cmsg 里有 `(SOL_UDP, UDP_GRO)` → 一个 int 段大小。`gro_size()` 已经取好了，
在 `account()` 里按它切：`step = gso`，`for (off = 0; off < len; off += step)`，
最后一段 `seglen = min(step, len - off)`。

## 提示 3
在真实 25G 网卡上比较：
`nic5_udp_gso_throughput send PEER 5201 10` 与加 `--gso`，同时在两边 `mpstat -P ALL 1` 看 CPU。
单流普通 sendmmsg 往往卡在 5~10 Gbit/s（一个核打满），GSO 能到 20+ Gbit/s；
`ethtool -k IFACE | grep udp-segmentation` 为 on 时切分由网卡硬件完成（mlx5 支持）。
