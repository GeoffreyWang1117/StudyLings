## 提示 1
在探针的拓扑里（或自己用 `ip netns` 搭一个）抓包：`ip netns exec <router> tcpdump -ni any icmp`
能看到 "need to frag (mtu 1400)"。之后客户端 `ip route get 10.2.0.2` 会显示 `cache ... mtu 1400`。

## 提示 2
`path_mtu`：`getsockopt(fd, IPPROTO_IP, IP_MTU, &mtu, &len)`，socket 必须已 connect（脚手架已做）。
EMSGSIZE 可能从两个地方冒出来：下一次 send（数据报超过了已缓存的 PMTU）或者等 ACK 时的 recv
（ICMP 带来的异步 socket 错误）。脚手架在两处都调用了 on_emsgsize。

## 提示 3
`on_emsgsize`：`int c = mtu - IP_UDP_OVERHEAD - HDR;`，若 `c <= 0 || c >= *chunk` 返回 -1（防止死循环），
否则 `*chunk = c; return 0;`。返回 0 后主循环会立刻用新大小重发当前这一片 —— 它之前那一份已经被 router 丢了，
而停等协议里 offset 没前进，所以不会有重复数据。
