## 提示 1
两步：创建时 `memfd_create(name, MFD_CLOEXEC | MFD_ALLOW_SEALING)`；写完数据后
`fcntl(fd, F_ADD_SEALS, F_SEAL_WRITE | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_SEAL)`。

## 提示 2
F_SEAL_WRITE 要求此刻没有任何可写的共享映射（否则 EBUSY）—— 所以这里用 write(2) 填数据，
或者先 munmap 掉可写映射再加封印。`F_GET_SEALS` 可以查看当前封印位（WRITE=0x8, SHRINK=0x2, GROW=0x4, SEAL=0x1）。

## 提示 3
接收方（比如 Wayland 合成器）拿到 fd 后会先 `fcntl(fd, F_GET_SEALS)` 检查封印齐全才敢用。
`ls -l /proc/<pid>/fd` 里 memfd 显示为 `/memfd:netlings-frame (deleted)`。
