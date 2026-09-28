## 提示 1
timerfd 和 eventfd 的 read 都必须用一个 8 字节的缓冲区（`uint64_t`），少于 8 字节会得到 EINVAL。
- timerfd：读到的是"上次读取以来到期了几次"，读完清零
- eventfd：读到的是计数器的值（多次 write 会累加），读完清零（没有 EFD_SEMAPHORE 时）

## 提示 2
```c
for (;;) {
    ssize_t n = read(fd, out, sizeof *out);
    if (n == (ssize_t)sizeof *out) return true;
    if (n < 0 && errno == EINTR) continue;
    if (n < 0 && errno == EAGAIN) return false;
    sl_die("read counter");
}
```

## 提示 3
为什么 wakeup 的值可能是 2？工作线程两次 write 之间事件循环还没来得及 read，计数器就累加了。
这是特性不是 bug：libuv 的 uv_async_send 明确说明"多次调用可能合并成一次回调"。
试着把 WORKER_SLEEP_MS 改成 0 再跑，观察 wakeup 行的数量和值。
