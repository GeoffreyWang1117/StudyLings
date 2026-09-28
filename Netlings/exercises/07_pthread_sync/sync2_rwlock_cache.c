// EXERCISE: sync2_rwlock_cache — 读多写少的缓存：pthread_rwlock_t 保护多字段值
// TOPIC: pthread_rwlock_rdlock / wrlock / 撕裂读（torn read）/ 写者饥饿
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §11.6.4（读写锁）；man 3 pthread_rwlock_rdlock；man 3 pthread_rwlockattr_setkind_np
// I AM NOT DONE
//
// 说明：
//   用法：sync2_rwlock_cache READERS ITERS
//   一个 key → value 缓存（NKEYS 个槽位），value 是两个字段的结构体 {a, b}，不变式：b == a * 3 + 7。
//   READERS 个读线程各做 ITERS 次 cache_get（随机 key）并检查不变式；
//   1 个写线程做 ITERS / 10 次 cache_put（随机 key，新 a 值），与读者同时运行。
//   结束时打印 "reads=<总读数> writes=<总写数> torn=<看到不一致值的次数>"，torn 必须为 0，
//   而且在 ThreadSanitizer 下不能有任何数据竞争报告（exit 66）。
//
//   为什么需要锁：value 有两个 8 字节字段，写者分两步写；没有锁的读者可能读到"新 a + 旧 b"
//   —— 撕裂读。就算只有一个字段，C 语言里非原子的并发读写本身就是未定义行为。
//   为什么是读写锁：读远多于写时，读锁允许多个读者并行，只有写者需要独占。
//   注意 glibc 默认"读者优先"，读者源源不断时写者可能永远拿不到锁（写者饥饿）；
//   脚手架里用 pthread_rwlockattr_setkind_np(PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP) 避免。
//
//   现实中：nginx 的共享内存 zone（ngx_rwlock）、PostgreSQL 的 LWLock（共享/独占模式）、
//   RocksDB/LevelDB 的 memtable 与版本信息、Envoy 的 thread-local 配置快照、
//   Go 的 sync.RWMutex、Rust 的 RwLock —— 路由表、配置、DNS 缓存这类"很少改、到处读"的数据都这么保护。
//   （读极多时更进一步用 RCU / 引用计数快照，见 sync3 的指针发布。）

#include <errno.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sl.h"

enum { NKEYS = 64 };

struct value {
    uint64_t a;
    uint64_t b; // 不变式：b == a * 3 + 7
};

struct cache {
    pthread_rwlock_t lock;
    struct value slots[NKEYS];
};

static struct cache g_cache;

static struct value make_value(uint64_t a) {
    return (struct value){.a = a, .b = a * 3 + 7};
}

// 读：返回 key 对应 value 的一份拷贝
static struct value cache_get(struct cache *c, unsigned key) {
    // BUG: 没有加锁就读，写者可能正写到一半 —— 撕裂读 + 数据竞争
    // TODO: 拷贝前 pthread_rwlock_rdlock，拷贝后 pthread_rwlock_unlock（读锁：多个读者可以同时持有）
    struct value v = c->slots[key % NKEYS];
    return v;
}

// 写：两个字段必须在同一个临界区里更新
static void cache_put(struct cache *c, unsigned key, uint64_t a) {
    // BUG: 写者也没有加锁
    // TODO: 两个字段的更新放进同一个 pthread_rwlock_wrlock / unlock 临界区（写锁：独占）
    struct value *slot = &c->slots[key % NKEYS];
    slot->a = a;
    slot->b = a * 3 + 7;
}

// ---- 脚手架 ----

struct worker_arg {
    unsigned seed;
    long iters;
    long done;
    long torn;
};

static pthread_barrier_t g_start;

static unsigned next_rand(unsigned *s) { // xorshift32，每个线程自己的状态
    unsigned x = *s;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    return *s = x;
}

static void *reader(void *p) {
    struct worker_arg *w = p;
    pthread_barrier_wait(&g_start);
    for (long i = 0; i < w->iters; i++) {
        struct value v = cache_get(&g_cache, next_rand(&w->seed));
        if (v.b != v.a * 3 + 7)
            w->torn++;
        w->done++;
    }
    return nullptr;
}

static void *writer(void *p) {
    struct worker_arg *w = p;
    pthread_barrier_wait(&g_start);
    for (long i = 0; i < w->iters; i++) {
        cache_put(&g_cache, next_rand(&w->seed), (uint64_t)i * 1000003u + 1);
        w->done++;
    }
    return nullptr;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 3) {
        fprintf(stderr, "usage: %s READERS ITERS\n", argv[0]);
        return 2;
    }
    long nr = strtol(argv[1], nullptr, 10), iters = strtol(argv[2], nullptr, 10);
    if (nr <= 0 || nr > 256 || iters <= 0) {
        fprintf(stderr, "bad arguments\n");
        return 2;
    }

    pthread_rwlockattr_t attr;
    pthread_rwlockattr_init(&attr);
    pthread_rwlockattr_setkind_np(&attr, PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP);
    int rc = pthread_rwlock_init(&g_cache.lock, &attr);
    pthread_rwlockattr_destroy(&attr);
    if (rc != 0) {
        errno = rc;
        sl_die("pthread_rwlock_init");
    }
    for (unsigned k = 0; k < NKEYS; k++)
        g_cache.slots[k] = make_value(k);

    pthread_barrier_init(&g_start, nullptr, (unsigned)nr + 1);
    pthread_t tids[257];
    struct worker_arg args[257];
    for (long i = 0; i <= nr; i++) {
        args[i] = (struct worker_arg){.seed = 2463534242u + (unsigned)i * 7919u,
                                      .iters = i == nr ? iters / 10 + 1 : iters};
        rc = pthread_create(&tids[i], nullptr, i == nr ? writer : reader, &args[i]);
        if (rc != 0) {
            errno = rc;
            sl_die("pthread_create");
        }
    }
    long reads = 0, torn = 0;
    for (long i = 0; i <= nr; i++) {
        pthread_join(tids[i], nullptr);
        if (i < nr) {
            reads += args[i].done;
            torn += args[i].torn;
        }
    }
    pthread_barrier_destroy(&g_start);
    pthread_rwlock_destroy(&g_cache.lock);

    printf("reads=%ld writes=%ld torn=%ld\n", reads, args[nr].done, torn);
    return torn == 0 ? 0 : 1;
}
