// EXERCISE: sync4_robust_mutex — 跨进程健壮互斥量：持锁进程崩溃后如何恢复
// TOPIC: PTHREAD_PROCESS_SHARED / PTHREAD_MUTEX_ROBUST / EOWNERDEAD / pthread_mutex_consistent
// DIFFICULTY: ★★★☆☆
// BOOK: APUE §12.4.1（互斥量属性：进程共享、健壮性）；man 3 pthread_mutexattr_setrobust；
//       man 3 pthread_mutex_consistent
// I AM NOT DONE
//
// 说明：
//   用法：sync4_robust_mutex
//   1. 在 mmap(MAP_SHARED | MAP_ANONYMOUS) 的共享内存里放一个 pthread_mutex_t 和它保护的数据
//      （一个"账本"：balance_a + balance_b 必须恒等于 1000）。
//   2. 互斥量属性：PTHREAD_PROCESS_SHARED（可以跨进程使用）+ PTHREAD_MUTEX_ROBUST（持有者死亡可被发现）。
//   3. fork 一个子进程：加锁，从 a 转 100 到 b 只做了一半（a 已扣、b 未加），然后 _exit —— 模拟
//      worker 进程在临界区里崩溃（段错误、OOM killer、kill -9）。
//   4. 父进程 waitpid 子进程之后加锁：
//      - 普通互斥量：锁的主人已经死了，永远不会解锁 → 父进程**永远卡住**；
//      - 健壮互斥量：pthread_mutex_lock 返回 EOWNERDEAD，调用者获得锁，但必须修复被保护的数据，
//        然后调用 pthread_mutex_consistent 标记"已修复"，再 unlock。之后这把锁就能正常使用。
//        （如果不调用 consistent 就 unlock，锁会变成永久不可用：之后 lock 返回 ENOTRECOVERABLE。）
//   5. 修复后再 lock/unlock 一次确认正常，打印 "recovered balance=<a+b>"。
//
//   现实中：PostgreSQL、Oracle 等多进程数据库的共享内存锁需要处理 backend 崩溃；
//   LMDB（MDB_ROBUST）、Boost.Interprocess、Chrome/Android 的共享内存 IPC，以及
//   nginx 共享内存 zone 的锁（它用自己的 ngx_shmtx，在 worker 崩溃后由 master 强制解锁）。
//   这个问题的本质：锁的状态存在共享内存里，内核只在 robust futex list 上替你兜底。

#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <unistd.h>

#include "sl.h"

struct shared {
    pthread_mutex_t mu;
    long balance_a; // 不变式：balance_a + balance_b == 1000
    long balance_b;
};

static void init_mutex(pthread_mutex_t *mu) {
    pthread_mutexattr_t attr;
    int rc = pthread_mutexattr_init(&attr);
    if (rc == 0)
        rc = pthread_mutexattr_setpshared(&attr, PTHREAD_PROCESS_SHARED);
    // TODO: 设置 PTHREAD_MUTEX_ROBUST（pthread_mutexattr_setrobust）。
    //       默认是 PTHREAD_MUTEX_STALLED：持有者死掉后，其他人 lock 会永远阻塞
    if (rc == 0)
        rc = pthread_mutex_init(mu, &attr);
    pthread_mutexattr_destroy(&attr);
    if (rc != 0) {
        errno = rc;
        sl_die("mutex init");
    }
}

// 修复被中断的转账：以 a 为准，把 b 补齐到不变式成立
static void repair(struct shared *s) {
    fprintf(stderr, "repairing: a=%ld b=%ld\n", s->balance_a, s->balance_b);
    s->balance_b = 1000 - s->balance_a;
}

// 加锁；若上一个持有者死在临界区里，修复数据并把锁标记为一致。成功返回 0
static int lock_and_recover(struct shared *s) {
    int rc = pthread_mutex_lock(&s->mu);
    // TODO: rc == EOWNERDEAD 时：我们已经拿到了锁，但数据可能是半成品。
    //       打印 "lock: EOWNERDEAD (previous owner died)"，调用 repair(s) 修复数据，
    //       再 pthread_mutex_consistent(&s->mu) 把锁标记为一致（失败则 unlock 并返回错误码），
    //       最后返回 0 表示成功持锁
    (void)repair;
    return rc;
}

int main(void) {
    setvbuf(stdout, nullptr, _IOLBF, 0);

    struct shared *s = mmap(nullptr, sizeof *s, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (s == MAP_FAILED)
        sl_die("mmap");
    init_mutex(&s->mu);
    s->balance_a = 1000;
    s->balance_b = 0;

    pid_t pid = fork();
    if (pid < 0)
        sl_die("fork");
    if (pid == 0) {
        // 子进程：拿锁，转账做到一半就"崩溃"
        if (pthread_mutex_lock(&s->mu) != 0)
            _exit(2);
        s->balance_a -= 100;
        printf("child: locked, a=%ld, dying before crediting b\n", s->balance_a);
        fflush(stdout);
        _exit(0); // 不 unlock 就死掉
    }

    int status;
    if (waitpid(pid, &status, 0) < 0)
        sl_die("waitpid");
    printf("child exited, parent locking...\n");

    int rc = lock_and_recover(s);
    if (rc != 0) {
        errno = rc;
        sl_die("lock_and_recover");
    }
    pthread_mutex_unlock(&s->mu);

    // 再用一次，确认锁已恢复正常
    rc = pthread_mutex_lock(&s->mu);
    if (rc != 0) {
        errno = rc;
        sl_die("second lock");
    }
    long sum = s->balance_a + s->balance_b;
    pthread_mutex_unlock(&s->mu);

    printf("recovered balance=%ld\n", sum);
    pthread_mutex_destroy(&s->mu);
    if (munmap(s, sizeof *s) < 0)
        sl_die("munmap");
    return sum == 1000 ? 0 : 1;
}
