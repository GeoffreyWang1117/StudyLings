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
N08 io_uring                                  tokio-uring、Seastar、TigerBeetle
        ↓
N09 network namespace / tc                    容器网络、CNI、流量整形、TCP 行为实验
        ↓
N10 eBPF / XDP                                Cilium、Katran、Cloudflare DDoS 防护
        ↓
N11 25GbE ConnectX                            网卡队列、RSS、IRQ 绑核、GSO/GRO
        ↓
N12 RDMA / RoCE                               内核旁路：verbs、RC QP、rdma_cm
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

## 章节

| 章 | 内容 | 环境 |
|---|---|---|
| **N01 TCP socket** | 多地址回退的客户端、双栈监听与 TIME_WAIT、长度前缀分帧、shutdown 半关闭、复现 Nagle + 延迟 ACK 卡顿 | 普通用户 |
| **N02 UDP** | 双栈 echo 与消息边界、connected UDP + 超时重传、手写 DNS 报文与名字压缩 | 普通用户 |
| **N03 select / poll** | select 多客户端、poll 聊天室、非阻塞 connect + 超时 | 普通用户 |
| **N04 epoll** | 水平触发、边沿触发（读空到 EAGAIN）、timerfd + eventfd 反应堆、EPOLLOUT 背压 | 普通用户 |
| **N05 Unix domain socket** | 路径与抽象命名空间、SCM_RIGHTS 传递 fd、SO_PEERCRED | 普通用户 |
| **N06 mmap / 共享内存** | mmap 扫描文件、跨进程 SPSC ring、memfd + seals | 普通用户 |
| **N07 pthread 同步** | 线程池、读写锁、原子统计与发布、robust mutex | 普通用户 |
| **N08 io_uring** | QD=8 批量读、accept/recv/send 服务器、multishot + provided buffer ring、linked timeout、registered files + SQPOLL | 普通用户（容器需放开 seccomp） |
| **N09 netns / tc** | 无特权 unshare、手写 rtnetlink 创建 veth、TCP_INFO（C 版 `ss -ti`）、按 socket 切换 BBR/CUBIC、经过路由器的 PMTU 发现 | root；netem 实验需 `sch_netem` |
| **N10 eBPF / XDP** | XDP 按协议计数（校验器边界检查）、XDP UDP 防火墙、tracepoint + ringbuf 追踪 TCP 状态机、tc egress 流量统计 | root |
| **N11 25GbE ConnectX** | ETHTOOL_GLINKSETTINGS、队列/ring/RSS 间接表、SO_REUSEPORT + CBPF 按 CPU 分发、IRQ 绑核计划、UDP GSO/GRO + sendmmsg 吞吐 | 部分可在 veth/lo 上做；完整需要 ConnectX |
| **N12 RDMA / RoCE** | 设备与 RoCE v2 GID、RC QP 状态机 ping-pong、RDMA WRITE_WITH_IMM / READ、rdma_cm 建连 | ConnectX 或 Soft-RoCE（`rdma_rxe`） |

N08–N12 在需要的环境不满足时会自动跳过，并说明如何满足。
真实网卡相关的环境变量：`NETLINGS_IFACE`（ConnectX 网卡名）、`NETLINGS_PEER_IP`（对端主机）、
`NETLINGS_RDMA_DEV`（如 `mlx5_0`、`rxe0`）、`NETLINGS_RDMA_GID_INDEX`。
`tools/hwcheck.sh` 会检查本机环境，并告诉你该 export 什么。

> **硬件验证状态**：N11/N12 里依赖真实网卡的部分（尤其是 RDMA 的收发路径）只在无网卡的机器上编译过、
> 用合成输入做过单元自测，还需要在 ConnectX 机器上验证。交接说明见 [docs/handoff/README.md](docs/handoff/README.md)。

## 维护者

```bash
python -m studylings.selfcheck Netlings -j 4
```
