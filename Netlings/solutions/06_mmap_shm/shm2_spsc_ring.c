// EXERCISE: shm2_spsc_ring — 跨进程单生产者/单消费者无锁环形队列
// TOPIC: MAP_SHARED|MAP_ANONYMOUS + fork / C11 atomics / acquire-release / 满与空的判定
// DIFFICULTY: ★★★★☆
// BOOK: man 2 mmap（MAP_SHARED）；man 3 stdatomic.h；C11 §7.17；Linux kernel Documentation/core-api/circular-buffers.rst
//
// 说明：
//   用法：shm2_spsc_ring N
//   父进程用 mmap(MAP_SHARED | MAP_ANONYMOUS) 创建一块共享内存放环形队列，然后 fork：
//     子进程 = 生产者：依次推入 1, 2, ..., N，然后 _exit(0)
//     父进程 = 消费者：弹出 N 个数求和，waitpid 子进程，打印 "sum=<总和>"
//   正确时 sum = N*(N+1)/2。探针会用几个不同的 N（包括很大的）运行，并设超时抓"卡死"。
//
//   环形队列（容量 CAP，是 2 的幂）：
//     head = 生产者已写入的总个数（只有生产者写），tail = 消费者已取走的总个数（只有消费者写）
//     两者都单调递增、不回绕取模，槽位下标 = 计数 % CAP。
//     空：head == tail        满：head - tail == CAP
//   内存序（这才是本题的核心）：
//     生产者：先写 slots[head % CAP]，再 store(head, release) —— 保证消费者看到新 head 时数据已经写好
//     消费者：load(head, acquire) 之后再读槽位；读完再 store(tail, release)，
//             生产者 load(tail, acquire) 看到新 tail 后才会覆盖这个槽位
//   x86 是强内存序，写错了也常常"看起来能跑"；ARM（Graviton、Apple M 系列）上就会读到脏数据。
//   另外 head/tail 放在不同的 cache line（alignas(64)），避免两个核心来回抢同一行（false sharing）。
//
//   为了稳定地测到"满"的情形，脚手架里消费者会先等生产者把环填满（head 50ms 不再前进）再开始消费。
//
//   现实中：DPDK rte_ring、LMAX Disruptor、io_uring 的 SQ/CQ（内核与用户态共享的环！）、
//   Chrome 的 Mojo 数据管道、音频/行情系统的共享内存队列，都是这个结构。
//   本章是 ASan 构建，不是 TSan —— 内存序错误要靠你自己推理，而不是工具。

#include <errno.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

enum { CAP = 256 };
static_assert((CAP & (CAP - 1)) == 0, "CAP must be a power of two");

struct ring {
    alignas(64) _Atomic size_t head; // 生产者写
    alignas(64) _Atomic size_t tail; // 消费者写
    alignas(64) uint64_t slots[CAP];
};
static_assert(ATOMIC_LONG_LOCK_FREE == 2, "need lock-free atomics for cross-process use");

static void backoff(unsigned *spins) {
    if (++*spins > 64) {
        sched_yield(); // 让出 CPU：测试机可能很忙，别空转
        *spins = 0;
    }
}

static void ring_push(struct ring *r, uint64_t v) {
    size_t h = atomic_load_explicit(&r->head, memory_order_relaxed); // 只有自己写 head
    unsigned spins = 0;
    // 满：等消费者取走至少一个
    while (h - atomic_load_explicit(&r->tail, memory_order_acquire) == CAP)
        backoff(&spins);
    r->slots[h % CAP] = v;
    atomic_store_explicit(&r->head, h + 1, memory_order_release); // 发布：数据先于 head 可见
}

static uint64_t ring_pop(struct ring *r) {
    size_t t = atomic_load_explicit(&r->tail, memory_order_relaxed); // 只有自己写 tail
    unsigned spins = 0;
    // 空：等生产者放入至少一个
    while (atomic_load_explicit(&r->head, memory_order_acquire) == t)
        backoff(&spins);
    uint64_t v = r->slots[t % CAP];
    atomic_store_explicit(&r->tail, t + 1, memory_order_release); // 读完才让出槽位
    return v;
}

static void sleep_ms(long ms) {
    struct timespec ts = {.tv_sec = ms / 1000, .tv_nsec = (ms % 1000) * 1000000L};
    while (nanosleep(&ts, &ts) < 0 && errno == EINTR) {
    }
}

// 脚手架：模拟"慢消费者"——等生产者把环填满、停下来（head 连续 50ms 不变）
static void wait_until_producer_stalls(struct ring *r, uint64_t n) {
    size_t last = (size_t)-1;
    int stable = 0;
    for (int i = 0; i < 400 && stable < 5; i++) { // 最多约 4 秒
        size_t h = atomic_load_explicit(&r->head, memory_order_acquire);
        if (h == n)
            return; // 生产者已经全部写完（N 小于容量）
        stable = (h == last) ? stable + 1 : 0;
        last = h;
        sleep_ms(10);
    }
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s N\n", argv[0]);
        return 2;
    }
    uint64_t n = strtoull(argv[1], nullptr, 10);

    struct ring *r = mmap(nullptr, sizeof *r, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (r == MAP_FAILED)
        sl_die("mmap");
    // MAP_ANONYMOUS 的内存已经清零；这里显式初始化，意图更清楚
    atomic_init(&r->head, 0);
    atomic_init(&r->tail, 0);

    pid_t pid = fork();
    if (pid < 0)
        sl_die("fork");
    if (pid == 0) {
        for (uint64_t v = 1; v <= n; v++)
            ring_push(r, v);
        _exit(0);
    }

    wait_until_producer_stalls(r, n);

    uint64_t sum = 0, out_of_order = 0;
    for (uint64_t i = 1; i <= n; i++) {
        uint64_t v = ring_pop(r);
        if (v != i && out_of_order++ < 5)
            fprintf(stderr, "pop #%llu got %llu\n", (unsigned long long)i, (unsigned long long)v);
        sum += v;
    }

    int status;
    if (waitpid(pid, &status, 0) < 0)
        sl_die("waitpid");
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        fprintf(stderr, "producer failed (status 0x%x)\n", status);
        return 1;
    }
    if (munmap(r, sizeof *r) < 0)
        sl_die("munmap");
    printf("sum=%llu\n", (unsigned long long)sum);
    return out_of_order ? 1 : 0;
}
