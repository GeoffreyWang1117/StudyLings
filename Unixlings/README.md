# Unixlings — APUE 现代版

**用 C23 和 2026 年的工具链，从零重走《UNIX 环境高级编程》(APUE 3e) 的核心：文件、进程、信号、线程。**

Unixlings 是 StudyLings 系统编程路线的第一站，下一站是 [Netlings](../Netlings/)（UNP socket → epoll → io_uring → eBPF → RDMA）。

```
A00 C 预备 → A01 文件 I/O → A02 进程 → A03 信号 → A04 线程 ──→ Netlings
```

## 为什么用 C，而不是 Rust / Rust Web

APUE 讲的是**系统调用这一层的语义**：fd 归属、fork/exec/wait、信号的异步安全、线程与 fork 的交互。
这一层的"母语"是 C —— `man 2`、`<unistd.h>`、`strace` 的输出、内核源码都是 C。
用 C 写，你写下的每一行和 `strace` 看到的几乎一一对应；tokio/axum 这类框架在它上面还隔着四层。
学完这里再看 Rust 的 `OwnedFd`、`unsafe fn fork`、`Send`/`Sync`，会明白它们究竟在防什么。

## 快速开始

```bash
# 推荐：用仓库里的 Dev Container（.devcontainer/systems），工具链版本固定
pip install -e ..                 # 在 StudyLings 根目录安装框架（click / rich / watchdog / pytest）
cd Unixlings
cmake --preset dev                # 生成 build/dev 与 compile_commands.json（给 clangd 用）
python -m unixlings               # 进度 + 下一题
python -m unixlings watch         # 保存即编译、即测试，通过后自动进入下一题
python -m unixlings hint fileio1_cat --level 1
```

需要：Linux、GCC ≥ 13（推荐 GCC 15）或 Clang、CMake ≥ 3.28、Ninja、Python ≥ 3.9、strace。

## 一道题是怎么被判定的

每道题是 `exercises/<章>/<名字>.c` 一个文件，编译成同名可执行文件。`run`/`verify`/`watch` 会：

1. `cmake --build --preset dev --target <名字>` —— 带 **AddressSanitizer + UBSan**（线程章换成 **ThreadSanitizer**），
   越界、泄漏、未定义行为、数据竞争都会让程序以非 0 退出；
2. 运行 `tests/<章>/test_<名字>.py` —— 一个 pytest **行为探针**，像 shell、对端进程或网络客户端那样从外部驱动你的程序：
   发信号、数僵尸进程、看 `/proc/<pid>/fd`、用 `strace` 检查你到底调用了哪些系统调用；
3. 测试全部通过后，删除文件里的 `// I AM NOT DONE`，进入下一题。

题目有三种：**填空实现**、**修 Bug**（fork 后输出两遍、fd 泄漏、僵尸、竞态……）、**复现实验**（例如用 `strace` 复现 APUE 图 3.6 的 read 次数）。

## 章节

| 章 | 对应 | 练习 |
|---|---|---|
| **A00 C 预备** | —— | 指针与输出参数、结构体对齐、有界字符串、errno 与 strtol、malloc/realloc 所有权、函数指针与 `void *ctx`、字节序与校验和 |
| **A01 文件 I/O** | APUE 3-4 | read/write 短写与缓冲区实验、文件空洞与 SEEK_DATA、O_APPEND 原子性、dup2 与 stdio 缓冲、O_CLOEXEC、openat/fstatat 安全遍历、write-fsync-rename 原子替换 |
| **A02 进程** | APUE 7-9 | fork/waitpid、fork 与 stdio 缓冲、pipe 流水线、posix_spawn、pidfd 超时控制、exit vs _exit |
| **A03 信号** | APUE 10 | sigaction 优雅退出、EINTR 超时、SIGCHLD 回收僵尸、signalfd 事件循环、SIGPIPE/EPIPE |
| **A04 线程** | APUE 11-12 | create/join 参数传递、互斥锁、条件变量有界队列、pthread_once 与 thread_local、多线程程序里的 fork |

每题的 BOOK 行标注了对应的 APUE 章节；题目和代码均为原创，不搬运原书内容。
书之外的现代补充（pidfd、signalfd、close_range、SEEK_DATA、posix_spawn……）直接写在题目说明里。

## 工具链

| 用途 | 工具 |
|---|---|
| 编译 | GCC 15 / Clang 20+，`-std=gnu23`（老编译器自动退到 gnu2x） |
| 构建 | CMake 4.x + Ninja + `CMakePresets.json`（`dev` / `nosan` / `solutions`） |
| 运行时检查 | ASan、UBSan、LSan、TSan；`nosan` 预设留给 valgrind / perf |
| 静态检查 | `clang-tidy -p build/dev`（`.clang-tidy` 已开启 `concurrency-mt-unsafe` 等），`gcc -fanalyzer` |
| 观测 | strace、ltrace、gdb/lldb（见 [Debuglings](../GDB-LLDB-Learner/)）、perf、bpftrace、`/proc` |

## 维护者

```bash
python -m studylings.selfcheck Unixlings -j 4   # 每个参考答案必须通过，每个原始练习必须失败
```
CI 在 `.github/workflows/systems-lings.yml` 里做同样的检查。
