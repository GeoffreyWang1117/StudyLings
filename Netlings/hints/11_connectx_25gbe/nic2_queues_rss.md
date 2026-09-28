## 提示 1
`ETHTOOL_GCHANNELS` 最简单：`struct ethtool_channels ch = {.cmd = ETHTOOL_GCHANNELS};` 传给
`ethtool_ioctl`，内核填回 `max_*` 与 `*_count`。失败时把 `errno` 返回给调用者，由它决定是
"unsupported" 还是致命错误。

## 提示 2
`indir_distribution` 就是一个直方图：`counts[indir[i]]++`（先检查 `indir[i] < nq`，否则算
out_of_range，避免越界写）。返回值 = `counts` 里非 0 的格子数 —— 真实网卡上它应该等于 combined 通道数，
否则有队列（以及它的中断和 CPU）永远收不到包。

## 提示 3
`ETHTOOL_GRSSH` 和 nic1 的 link settings 一样是两步：
```c
struct ethtool_rxfh sizes = {.cmd = ETHTOOL_GRSSH};          // indir_size = key_size = 0
ethtool_ioctl(fd, iface, &sizes);                             // 内核只回填尺寸
size_t sz = sizeof(struct ethtool_rxfh) + sizes.indir_size * sizeof(uint32_t) + sizes.key_size;
struct ethtool_rxfh *rss = calloc(1, sz);
rss->cmd = ETHTOOL_GRSSH; rss->indir_size = sizes.indir_size; rss->key_size = sizes.key_size;
ethtool_ioctl(fd, iface, rss);                                // rss_config[] = 间接表 + key
```
对照 `ethtool -x IFACE` 的输出检查你的结果。
