// EXERCISE: nic3_reuseport_cpu — SO_REUSEPORT + CPU 绑定 + CBPF：连接在收到它的 CPU 上处理
// TOPIC: SO_REUSEPORT / pthread_setaffinity_np / SO_INCOMING_CPU / SO_ATTACH_REUSEPORT_CBPF（SKF_AD_CPU）
// DIFFICULTY: ★★★★☆
// BOOK: man 7 socket（SO_REUSEPORT、SO_INCOMING_CPU、SO_ATTACH_REUSEPORT_CBPF）；man 3 pthread_setaffinity_np；Documentation/networking/filter.rst（classic BPF 与 SKF_AD_* 扩展）
//
// 说明：
//   用法：nic3_reuseport_cpu PORT NWORKERS [--mode hash|cbpf|incoming-cpu]   （默认 cbpf）
//   - 取本进程允许运行的 CPU 列表（sched_getaffinity），worker i 绑到第 i 个 CPU（NWORKERS 不能超过它）
//   - 每个 worker 一个**自己的**监听 socket：都设 SO_REUSEPORT、都 bind 127.0.0.1:PORT，
//     内核把它们放进同一个 reuseport 组，每个新连接只会进入其中一个 socket 的 accept 队列
//     （没有 SO_REUSEPORT 时第二个 bind 会 EADDRINUSE）
//   - mode=hash：内核按 4 元组哈希挑 socket —— 连接均匀分散，但"网卡队列/软中断所在 CPU"和
//     "accept 它的 worker 所在 CPU"无关，包要在 CPU 之间搬运（cache miss、跨核唤醒）
//   - mode=cbpf：给组挂一个 classic BPF 程序：A = 当前 CPU 号（SKF_AD_OFF + SKF_AD_CPU），
//     返回"绑在这个 CPU 上的 worker 的下标"。下标 = socket 调 listen() 加入组的顺序，
//     所以 main 里按 worker 顺序依次创建/listen。返回值越界时内核退回哈希选择。
//   - mode=incoming-cpu：每个监听 socket 设 SO_INCOMING_CPU = 它的 CPU；Linux 6.1+ 的
//     reuseport 哈希选择会优先挑 incoming_cpu 等于当前 CPU 的 socket（不用 BPF）
//   - 每个 accept 到的连接：回一行 "worker=I cpu=C incoming_cpu=X\n" 然后关闭。
//     cpu 是 sched_getcpu()，incoming_cpu 是 getsockopt(conn, SO_INCOMING_CPU)：最后处理这个
//     连接收包软中断的 CPU。两者不同计为一次 cpu_mismatch
//   - 就绪后打印 "listening on port P workers=N mode=M cpus=0,1,..."；
//     收到 SIGTERM/SIGINT：所有 worker 退出，打印每个 worker 的
//     "worker I cpu=C accepted=N cpu_mismatch=M" 和 "total accepted=T cpu_mismatch=M"，exit 0
//
//   这就是 nginx `listen ... reuseport`、Envoy 的每 worker 监听、Seastar/ScyllaDB/Redpanda
//   "shared-nothing" 的核心：网卡 RSS 把流撒到各队列（nic2）→ 队列中断绑到各 CPU（nic4）→
//   包在哪个 CPU 上收，连接就在哪个 CPU 上 accept 和处理，全程不跨核。
//
//   测试（本机 loopback 即可）：lo 上包的软中断在发送方 CPU 上处理，所以测试把客户端线程分别
//   绑到各个 CPU 上发起连接：hash 模式下每个 worker 都分到连接；cbpf / incoming-cpu 模式下，
//   从 CPU k 发起的连接必须由绑在 CPU k 上的 worker 处理（cpu == incoming_cpu == k）。
//   真实机器上可以用 NETLINGS_PEER_IP 所在主机做客户端、网卡 RSS + nic4 的 IRQ 绑定来重复实验。

#include <arpa/inet.h>
#include <errno.h>
#include <linux/filter.h>
#include <netinet/in.h>
#include <pthread.h>
#include <sched.h>
#include <signal.h>
#include <poll.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_WORKERS = 64 };
enum mode { MODE_HASH, MODE_CBPF, MODE_INCOMING_CPU };

typedef struct {
    int id;
    int cpu; // 绑定的 CPU
    int lfd; // 自己的监听 socket
    pthread_barrier_t *ready;
    int pin_err;       // pthread_setaffinity_np 的返回值（0 = 成功）
    unsigned long accepted;
    unsigned long mismatch;
    int fatal_err; // worker 因错误退出时的 errno
} worker;

static atomic_bool g_stop;

// 创建一个加入 reuseport 组的监听 socket（非阻塞，worker 用 poll 等待）
static int make_listener(int port, enum mode mode, int cpu) {
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    int one = 1;
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one) < 0)
        sl_die("setsockopt(SO_REUSEADDR)");
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEPORT, &one, sizeof one) < 0)
        sl_die("setsockopt(SO_REUSEPORT)");
    if (mode == MODE_INCOMING_CPU && setsockopt(fd, SOL_SOCKET, SO_INCOMING_CPU, &cpu, sizeof cpu) < 0)
        sl_die("setsockopt(SO_INCOMING_CPU)");
    struct sockaddr_in addr = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(fd, (struct sockaddr *)&addr, sizeof addr) < 0)
        sl_die("bind");
    if (listen(fd, SOMAXCONN) < 0) // 加入 reuseport 组：组内下标 = listen 的先后顺序
        sl_die("listen");
    return fd;
}

// 生成 classic BPF：A = 当前 CPU；A == cpus[i] → 返回 i；都不匹配 → 返回 n（越界 → 内核退回哈希）
// 返回指令条数；cap 不够返回 0
static size_t build_cpu_filter(const int *cpus, size_t n, struct sock_filter *out, size_t cap) {
    size_t need = 2 * n + 2;
    if (cap < need)
        return 0;
    size_t k = 0;
    out[k++] = (struct sock_filter)BPF_STMT(BPF_LD | BPF_W | BPF_ABS, (uint32_t)(SKF_AD_OFF + SKF_AD_CPU));
    for (size_t i = 0; i < n; i++) {
        // 相等 → 不跳（执行下一条 RET i）；不等 → 跳过 1 条
        out[k++] = (struct sock_filter)BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, (uint32_t)cpus[i], 0, 1);
        out[k++] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, (uint32_t)i);
    }
    out[k++] = (struct sock_filter)BPF_STMT(BPF_RET | BPF_K, (uint32_t)n);
    return k;
}

static void attach_cpu_filter(int fd, const int *cpus, size_t n) {
    struct sock_filter code[2 * MAX_WORKERS + 2];
    size_t len = build_cpu_filter(cpus, n, code, sizeof code / sizeof code[0]);
    if (len == 0) {
        fprintf(stderr, "build_cpu_filter: 指令缓冲区不够\n");
        exit(1);
    }
    struct sock_fprog prog = {.len = (unsigned short)len, .filter = code};
    // 挂在组内任意一个 socket 上即作用于整个组
    if (setsockopt(fd, SOL_SOCKET, SO_ATTACH_REUSEPORT_CBPF, &prog, sizeof prog) < 0)
        sl_die("setsockopt(SO_ATTACH_REUSEPORT_CBPF)");
}

static void serve_one(worker *w, int cfd) {
    int incoming = -1;
    socklen_t len = sizeof incoming;
    if (getsockopt(cfd, SOL_SOCKET, SO_INCOMING_CPU, &incoming, &len) < 0) {
        perror("getsockopt(SO_INCOMING_CPU)");
        incoming = -1;
    }
    int now = sched_getcpu();
    w->accepted++;
    if (incoming != w->cpu)
        w->mismatch++;
    char line[96];
    int n = snprintf(line, sizeof line, "worker=%d cpu=%d incoming_cpu=%d\n", w->id, now, incoming);
    // 短回复 + 阻塞 socket：一次 send 基本总能写完；对端提前关闭（EPIPE/ECONNRESET）不算服务器错误
    if (send(cfd, line, (size_t)n, MSG_NOSIGNAL) < 0 && errno != EPIPE && errno != ECONNRESET)
        perror("send");
    close(cfd);
}

static void *worker_main(void *arg) {
    worker *w = arg;
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(w->cpu, &set);
    w->pin_err = pthread_setaffinity_np(pthread_self(), sizeof set, &set);
    pthread_barrier_wait(w->ready);
    if (w->pin_err)
        return nullptr;

    while (!atomic_load_explicit(&g_stop, memory_order_relaxed)) {
        struct pollfd pfd = {.fd = w->lfd, .events = POLLIN};
        int r = poll(&pfd, 1, 100); // 100ms 醒一次检查 g_stop
        if (r < 0) {
            if (errno == EINTR)
                continue;
            w->fatal_err = errno;
            break;
        }
        if (r == 0)
            continue;
        int cfd = accept4(w->lfd, nullptr, nullptr, SOCK_CLOEXEC); // 连接 socket 用阻塞模式
        if (cfd < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK || errno == EINTR || errno == ECONNABORTED)
                continue;
            w->fatal_err = errno;
            break;
        }
        serve_one(w, cfd);
    }
    return nullptr;
}

static bool parse_mode(const char *s, enum mode *m) {
    if (strcmp(s, "hash") == 0)
        *m = MODE_HASH;
    else if (strcmp(s, "cbpf") == 0)
        *m = MODE_CBPF;
    else if (strcmp(s, "incoming-cpu") == 0)
        *m = MODE_INCOMING_CPU;
    else
        return false;
    return true;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    enum mode mode = MODE_CBPF;
    if (argc == 5 && strcmp(argv[3], "--mode") == 0) {
        if (!parse_mode(argv[4], &mode)) {
            fprintf(stderr, "unknown mode %s (hash|cbpf|incoming-cpu)\n", argv[4]);
            return 2;
        }
    } else if (argc != 3) {
        fprintf(stderr, "usage: %s PORT NWORKERS [--mode hash|cbpf|incoming-cpu]\n", argv[0]);
        return 2;
    }
    int port = atoi(argv[1]);
    int n = atoi(argv[2]);
    if (port <= 0 || port > 65535 || n <= 0 || n > MAX_WORKERS) {
        fprintf(stderr, "PORT 应在 1..65535，NWORKERS 应在 1..%d\n", MAX_WORKERS);
        return 2;
    }

    // 允许运行的 CPU（容器/cgroup/taskset 可能只给了一部分）
    cpu_set_t allowed;
    if (sched_getaffinity(0, sizeof allowed, &allowed) < 0)
        sl_die("sched_getaffinity");
    int cpus[MAX_WORKERS];
    int ncpu = 0;
    for (int c = 0; c < CPU_SETSIZE && ncpu < n; c++)
        if (CPU_ISSET(c, &allowed))
            cpus[ncpu++] = c;
    if (ncpu < n) {
        fprintf(stderr, "NWORKERS=%d 超过了可用 CPU 数 %d（每个 worker 独占一个 CPU）\n", n, ncpu);
        return 2;
    }

    // SIGTERM/SIGINT 由 main 用 sigwait 同步接收；先屏蔽，新线程继承屏蔽字
    sigset_t sigs;
    sigemptyset(&sigs);
    sigaddset(&sigs, SIGTERM);
    sigaddset(&sigs, SIGINT);
    int err = pthread_sigmask(SIG_BLOCK, &sigs, nullptr);
    if (err) {
        errno = err;
        sl_die("pthread_sigmask");
    }

    // 按 worker 顺序创建并 listen：组内下标 i ↔ worker i ↔ cpus[i]
    worker workers[MAX_WORKERS] = {};
    for (int i = 0; i < n; i++)
        workers[i] = (worker){.id = i, .cpu = cpus[i], .lfd = make_listener(port, mode, cpus[i])};
    if (mode == MODE_CBPF)
        attach_cpu_filter(workers[0].lfd, cpus, (size_t)n);

    pthread_barrier_t ready;
    err = pthread_barrier_init(&ready, nullptr, (unsigned)n + 1);
    if (err) {
        errno = err;
        sl_die("pthread_barrier_init");
    }
    pthread_t tids[MAX_WORKERS];
    for (int i = 0; i < n; i++) {
        workers[i].ready = &ready;
        err = pthread_create(&tids[i], nullptr, worker_main, &workers[i]);
        if (err) {
            errno = err;
            sl_die("pthread_create");
        }
    }
    pthread_barrier_wait(&ready); // 所有 worker 都已绑好 CPU
    bool pinned = true;
    for (int i = 0; i < n; i++) {
        if (workers[i].pin_err) {
            fprintf(stderr, "pthread_setaffinity_np(worker %d → CPU %d): %s\n", i, workers[i].cpu,
                    strerror(workers[i].pin_err));
            pinned = false;
        }
    }

    int rc = 0;
    if (pinned) {
        printf("listening on port %d workers=%d mode=%s cpus=", port, n,
               mode == MODE_HASH ? "hash" : mode == MODE_CBPF ? "cbpf" : "incoming-cpu");
        for (int i = 0; i < n; i++)
            printf("%s%d", i ? "," : "", cpus[i]);
        printf("\n");
        int sig = 0;
        err = sigwait(&sigs, &sig);
        if (err) {
            fprintf(stderr, "sigwait: %s\n", strerror(err));
            rc = 1;
        }
    } else {
        rc = 1;
    }

    atomic_store(&g_stop, true);
    unsigned long total = 0, mismatch = 0;
    for (int i = 0; i < n; i++) {
        err = pthread_join(tids[i], nullptr);
        if (err) {
            fprintf(stderr, "pthread_join: %s\n", strerror(err));
            rc = 1;
        }
        if (workers[i].fatal_err) {
            fprintf(stderr, "worker %d: %s\n", i, strerror(workers[i].fatal_err));
            rc = 1;
        }
        if (pinned)
            printf("worker %d cpu=%d accepted=%lu cpu_mismatch=%lu\n", i, workers[i].cpu, workers[i].accepted,
                   workers[i].mismatch);
        total += workers[i].accepted;
        mismatch += workers[i].mismatch;
        close(workers[i].lfd);
    }
    if (pinned)
        printf("total accepted=%lu cpu_mismatch=%lu\n", total, mismatch);
    pthread_barrier_destroy(&ready);
    return rc;
}
