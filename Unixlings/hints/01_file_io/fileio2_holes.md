## 提示 1
create 只差一行：`lseek(fd, offset, SEEK_SET)`。之后的 write 从 offset 处开始写，中间自然留下空洞。
用 `ls -ls` 或 `du -h` vs `du -h --apparent-size` 对比，就能看到空洞不占空间。

## 提示 2
map 的循环：`start = lseek(fd, pos, SEEK_DATA)`；`start < 0 && errno == ENXIO` 表示已经没有数据，跳出循环。
然后 `end = lseek(fd, start, SEEK_HOLE)`，打印后 `pos = end`。

## 提示 3
区间边界是文件系统的块大小（比如 4096），而不是你写入的 4 个字节 —— 文件系统按块分配存储。
