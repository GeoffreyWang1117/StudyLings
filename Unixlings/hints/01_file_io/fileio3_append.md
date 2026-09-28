## 提示 1
在 open 的 flags 里加上 `O_APPEND`，然后删掉 `lseek(fd, 0, SEEK_END)` 那一行。

## 提示 2
为什么 lseek + write 会丢行：进程 A lseek 得到末尾 1000，还没 write 就被调度走；
进程 B 也 lseek 到 1000 并写入；A 回来后仍然写在 1000 —— 覆盖了 B 的那一行。
O_APPEND 让内核在每次 write 时（持有 inode 锁）把偏移设到当前末尾再写。
