# Netlings — UNP 现代版，一路走到 RDMA

**接着 [Unixlings](../Unixlings/)，用 C23 从 socket 一路做到内核旁路：只学今天的 Web 和基础设施里还在用的东西。**

```
Unixlings: file / process / signal / thread
        ↓
N01 TCP socket ─ N02 UDP                      UNP Vol.1 仍然活着的部分
        ↓
N03 select / poll
        ↓
N04 epoll                                     nginx、Redis、libuv、tokio/mio、Go netpoller
        ↓
N05 Unix domain socket                        docker.sock、systemd、PostgreSQL、fd 传递
        ↓
N06 mmap / 共享内存                           数据库、零拷贝、跨进程 ring buffer
        ↓
N07 pthread 同步（服务器视角）                 线程池、读写锁、原子操作、robust mutex
        ↓
N08 io_uring                                  ─┐
        ↓                                        │
N09 network namespace / tc                       │  路线图（下一批）
        ↓                                        │
N10 eBPF / XDP                                   │
        ↓                                        │
N11 25GbE ConnectX                               │
        ↓                                        │
N12 RDMA / RoCE                               ─┘
```

## 选材原则

UNP 卷一里**今天仍在各个 Web 生态里活着**的内容才会进来：getaddrinfo 与 IPv4/IPv6 双栈、TIME_WAIT 与 SO_REUSEADDR、
字节流分帧（HTTP/2、gRPC、Kafka、Redis 都是长度前缀）、半关闭、Nagle 与 TCP_NODELAY、非阻塞 connect、UDP 重传、
I/O 多路复用、SCM_RIGHTS、SO_PEERCRED……

不做：XTI/TLI、STREAMS、SIGIO 驱动 I/O、T/TCP、rsh/rlogin、`gethostbyname` 这类遗留 API。

每道题的说明都会写它在今天的系统里对应什么（nginx、Envoy、Redis、Node/libuv、Go、tokio、systemd、Kubernetes……）。

## 快速开始

```bash
pip install -e ..            # StudyLings 根目录
cd Netlings
cmake --preset dev
python -m netlings           # 进度 + 下一题
python -m netlings watch
```

所有 N01–N07 的练习只用 `127.0.0.1` / `::1` / AF_UNIX，不需要 root，也不需要外网。
判定方式与 Unixlings 相同：ASan/UBSan（N07 用 TSan）编译，再由 `tests/` 里的 pytest 探针从外部驱动。
探针扮演客户端或对端：比如一个字节一个字节地发包来测试分帧，或者故意不读数据来测试背压，
还会把 accept 队列塞满、造出本地"黑洞"来测试 connect 超时。

## 已完成章节

| 章 | 内容 |
|---|---|
| **N01 TCP socket** | 多地址回退的客户端、双栈监听与 TIME_WAIT、长度前缀分帧、shutdown 半关闭、复现 Nagle + 延迟 ACK 卡顿 |
| **N02 UDP** | 双栈 echo 与消息边界、connected UDP + 超时重传（DNS 客户端的做法）、手写 DNS 报文与名字压缩 |
| **N03 select / poll** | select 多客户端、poll 聊天室、非阻塞 connect + 超时 |
| **N04 epoll** | 水平触发、边沿触发（读空到 EAGAIN）、timerfd + eventfd 反应堆、写缓冲与 EPOLLOUT 背压 |
| **N05 Unix domain socket** | 路径与抽象命名空间、SCM_RIGHTS 传递 fd、SO_PEERCRED 认证 |
| **N06 mmap / 共享内存** | mmap 扫描文件、跨进程 SPSC ring（acquire/release）、memfd + seals |
| **N07 pthread 同步** | 线程池与优雅关闭、读写锁缓存、原子统计与发布、进程间 robust mutex |

## 路线图：N08–N12

这几章会用到特权、专用内核特性和真实硬件。探针会先检测环境，条件不满足时 `skip` 并说明原因。

### N08 io_uring
liburing；用 multishot accept/recv 和 provided buffer ring 写 echo 服务器；registered files/buffers；
SQPOLL；`IORING_OP_SEND_ZC` 零拷贝发送；与 N04 的 epoll 版本做同机压测对比。
（Docker 默认的 seccomp 会拦截 io_uring，Dev Container 已设置 `seccomp=unconfined`。）

### N09 network namespace / tc
不需要 root：用 `unshare -Urn` 搭拓扑，包括 veth 对、bridge、`client — router — server` 三节点；
`tc netem` 注入延迟、丢包、乱序；`tc fq`/`tbf` 做整形；用 `ss -ti` 观察 RTO 和 cwnd；
iperf3 对比 CUBIC 与 BBR；在丢包链路上复现 TCP 重传退避。

### N10 eBPF / XDP
libbpf + CO-RE + `bpftool gen skeleton`；用 bpftrace 追踪 `tcp:tcp_retransmit_skb`；
在 veth 上跑 XDP 程序（先 generic 模式，再用 BPF map 统计 / 丢弃 / 重定向）；tc-bpf 出向过滤；
最后配合 N11，在 mlx5 上跑 native XDP。

### N11 25GbE ConnectX
`ethtool -l/-L`（队列）、`-X`（RSS 间接表）、`-K`（TSO/GRO/LRO）、`-C`（中断合并）、`-G`（ring 大小）；
IRQ 亲和与 NUMA 绑核；RPS/RFS/XPS；`SO_REUSEPORT` + `SO_INCOMING_CPU`；`SO_BUSY_POLL`；
用 iperf3 / sockperf / `perf` 找瓶颈，目标是单流和多流跑满 25 Gbit/s。
网卡名通过环境变量 `NETLINGS_IFACE` 指定。

### N12 RDMA / RoCE
rdma-core / libibverbs：查询设备和 GID，建立 PD / MR / CQ / QP，走完 QP 状态机 RESET→INIT→RTR→RTS；
RC 上的 SEND/RECV、RDMA WRITE/READ；用 rdma_cm 建连；perftest（`ib_write_bw` / `ib_send_lat`）做基线。
没有硬件时，先在 veth 上用 **Soft-RoCE（rdma_rxe）** 完成所有功能题；有 ConnectX 时再做 RoCE v2 的
GID 选择、PFC/ECN 无损配置与 DCQCN 观察。

## 维护者

```bash
python -m studylings.selfcheck Netlings -j 4
```
