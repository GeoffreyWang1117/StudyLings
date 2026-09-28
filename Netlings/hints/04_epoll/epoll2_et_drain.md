## 提示 1
ET 的铁律："就绪通知 = 状态从'没有'变成'有'的那一刻"。处理事件时必须一直做到 `EAGAIN`，
把状态重新变回"没有"，下一次变化才会再通知你。accept 和 read 都一样。

## 提示 2
drain accept：
```c
for (;;) {
    int cfd = accept4(lfd, nullptr, nullptr, SOCK_NONBLOCK | SOCK_CLOEXEC);
    if (cfd < 0) {
        if (errno == EINTR || errno == ECONNABORTED) continue;
        if (errno != EAGAIN) perror("accept4");
        return;
    }
    ... EPOLL_CTL_ADD ...
}
```
（ET 下所有 fd 必须是非阻塞的，否则最后那次"读到空"会直接阻塞整个事件循环。）

## 提示 3
drain read 同理：`for (;;) { n = read(...); ... EAGAIN → return; 0 → close_conn; 否则 write_back; }`。
对比：Redis 的 LT 读法是"每次事件最多读 16 KiB，读不完下次 epoll_wait 还会报告"；
nginx 的 ET 读法是 `ngx_unix_recv` 读到 EAGAIN 后清掉 `rev->ready`，等下一个边沿。
