## 提示 1
select 的 fd_set 是"值-结果"参数：传进去的是"我关心哪些 fd"，返回时只剩"哪些 fd 就绪了"。
所以 `FD_ZERO` + `FD_SET` 必须放在 `for (;;)` 循环**里面**，每轮重建一次；
第一个参数是"最大 fd + 1"，不是 fd 的个数。

## 提示 2
骨架：
```c
fd_set rset; FD_ZERO(&rset); FD_SET(lfd, &rset); int maxfd = lfd;
for (...) if (clients[i] >= 0) { FD_SET(clients[i], &rset); maxfd = max(maxfd, clients[i]); }
if (select(maxfd + 1, &rset, nullptr, nullptr, nullptr) < 0) { if (errno == EINTR) continue; ... }
if (FD_ISSET(lfd, &rset)) { accept4 → add_client }
for (...) if (clients[i] >= 0 && FD_ISSET(clients[i], &rset) && !echo_once(clients[i])) { close; clients[i] = -1; }
```

## 提示 3
select 返回"可读"只保证下一次 read 不阻塞，所以每个就绪 fd 只 read **一次**，然后回到 select。
想看它在做什么：`strace -e trace=select,accept4,read,write ./build/dev/bin/poll1_select_echo 9000`，
另开终端 `nc 127.0.0.1 9000` 开两三个。
