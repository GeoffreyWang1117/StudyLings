## 提示 1
`read(fd, buf, n)` 返回 `r` 且 `0 < r < n` 完全正常——只是"目前到了这么多"。
read_full 要用一个 `got` 计数循环，每次读 `n - got` 字节到 `buf + got`。

## 提示 2
区分两种 EOF：一个字节都还没读到就 `read` 返回 0 → 对端在帧边界正常关闭（返回 0）；
读了一半返回 0 → 帧被截断（返回 -1）。`r < 0 && errno == EINTR` 时 `continue`。

## 提示 3
write_full 是同样的循环：`while (n > 0) { w = write(...); ... p += w; n -= w; }`。
`void *` 不能做指针运算，先转成 `char *`。
