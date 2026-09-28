## 提示 1
先在有设备的机器上看原始数据：
`ls /sys/class/infiniband/mlx5_0/ports/1/gids/`、`cat .../gids/3`、`cat .../gid_attrs/types/3`。
GID 文件是 8 组 4 位十六进制，用 ':' 分隔；`show_gids`（mlx5 的 ofed 脚本）和 `rdma link` 能对照。

## 提示 2
解析一组：
```c
unsigned v = 0;
for (int k = 0; k < 4; k++) { 取一个字符 c → 0..15 的 d，非法就 return false; v = v << 4 | d; }
raw[2*g] = v >> 8;  raw[2*g + 1] = v & 0xff;
```
前 7 组后面必须跟 ':'，第 8 组后面只能是 '\0' 或 '\n'。

## 提示 3
IPv4 映射的 IPv6 地址 = 80 位 0 + 16 位 1 + 32 位 IPv4：`raw[0..9] == 0 && raw[10] == 0xff && raw[11] == 0xff`。
`pick_roce_v2_ipv4` 返回的是 `e[i].index`（GID 表下标）。拿到下标后可以用
`ibv_query_gid(ctx, port, idx, &gid)` 对照，后面几题建 QP 时 `ah_attr.grh.sgid_index` 就填它。
