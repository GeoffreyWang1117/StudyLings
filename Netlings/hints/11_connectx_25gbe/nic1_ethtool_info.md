## 提示 1
`struct ethtool_link_settings` 末尾是柔性数组 `__u32 link_mode_masks[]`，长度由
`link_mode_masks_nwords` 决定。第一次用 `nwords = 0` 调用时内核**不填数据**，只把
`link_mode_masks_nwords` 设成 `-N` 返回——这是在告诉你"请准备 N 个 u32 再来"。

## 提示 2
```c
int nwords = -probe.link_mode_masks_nwords;
size_t sz = sizeof(struct ethtool_link_settings) + 3 * (size_t)nwords * sizeof(uint32_t);
struct ethtool_link_settings *req = calloc(1, sz);
req->cmd = ETHTOOL_GLINKSETTINGS;
req->link_mode_masks_nwords = (int8_t)nwords;
ethtool_ioctl(fd, iface, req);   // 这次 speed/duplex/port 才有值
```
3 张位图依次是 supported / advertising / lp_advertising。

## 提示 3
`speed` 是 `__u32`，链路没起来时是 `SPEED_UNKNOWN`（-1 转成无符号），打印前换成 -1。
用 `ethtool IFACE` 和 `cat /sys/class/net/IFACE/speed` 对照你的输出；ConnectX-4 Lx/5/6 Lx 的
25G 口正常应是 `speed_mbps=25000`，`port=da`（DAC 铜缆）或 `port=fibre`（光模块）。
