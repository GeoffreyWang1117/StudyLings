## 提示 1
先用 `ss -tin` 观察一条正在传输的连接：rtt、cwnd、retrans、delivery_rate、pacing_rate 都在那里。
ss 就是通过 netlink (INET_DIAG) 拿到同一个 struct tcp_info 的；你用 getsockopt(TCP_INFO) 拿自己的。

## 提示 2
```c
struct tcp_info ti = {};
socklen_t len = sizeof ti;
if (getsockopt(fd, IPPROTO_TCP, TCP_INFO, &ti, &len) < 0) return -1;
s->rtt_us = ti.tcpi_rtt;           // 微秒
s->cwnd = ti.tcpi_snd_cwnd;        // 段数
s->total_retrans = ti.tcpi_total_retrans;
```
速率字段 tcpi_delivery_rate / tcpi_pacing_rate 是 **字节/秒**，用 bps_to_mbps 换算。

## 提示 3
goodput = tcpi_bytes_acked × 8 / 秒 / 1e6。write() 返回只说明数据进了本机发送缓冲区
（net.ipv4.tcp_wmem 上限可到 4MB+，在 50Mbit 链路上相当于半秒多的数据），不代表对方收到了。
