## 提示 1
read 的三种返回值：`> 0` 读到的字节数（可能少于请求的）、`0` EOF、`-1` 出错（看 errno）。
典型循环：`for (;;) { ssize_t r = read(...); if (r == 0) break; if (r < 0) {...} write_all(...); }`

## 提示 2
write_all：`while (n > 0) { ssize_t w = write(fd, buf, n); ... buf += w; n -= w; }`，
`w < 0 && errno == EINTR` 时 `continue`。

## 提示 3
strace 看看你的程序做了什么：`strace -e trace=openat,read,write,close ./build/dev/bin/fileio1_cat -b 16 /etc/hostname`
（ASan 自身也会调用 read，所以测试用 `strace -y` 只统计对 data.bin 的 read。）
