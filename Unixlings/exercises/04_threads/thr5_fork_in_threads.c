// EXERCISE: thr5_fork_in_threads — 多线程程序里 fork：被复制的锁与 pthread_atfork
// TOPIC: fork 与线程、异步信号安全、pthread_atfork
// DIFFICULTY: ★★★★☆
// BOOK: APUE §12.9（线程和 fork）、§10.6（可重入函数）；man 3 pthread_atfork, man 7 signal-safety
// I AM NOT DONE
//
// 说明：
//   用法：thr5_fork_in_threads
//   程序里有一个后台"日志刷盘"线程，它大部分时间都拿着日志锁 g_log_lock（在锁里 sleep 模拟慢 I/O）。
//   main 在这个锁被持有期间 fork 一个子进程，子进程先调用 log_msg 记一行日志，再 exec `echo child-ok`；
//   父进程 waitpid 等子进程成功退出后打印 parent-ok。
//
//   问题：fork 只复制调用 fork 的那一个线程，但会复制整个地址空间 —— 包括"已上锁"状态的 g_log_lock。
//   子进程里持锁的那个后台线程根本不存在，没人会解锁；子进程一调用 log_msg 就永远卡住（死锁）。
//   malloc 的内部锁、stdio 的 FILE 锁也有同样问题，所以 POSIX 规定：多线程进程 fork 后、exec 前，
//   子进程只能调用异步信号安全（async-signal-safe）的函数。
//
//   两种修法（任选其一，也可以都做）：
//   A. 子进程在 exec 之前什么"库函数"都不碰：只用 write(2)、dup2、execvp、_exit 等异步信号安全函数；
//      或者干脆用 posix_spawn 一步到位。
//   B. pthread_atfork(prepare, parent, child)：prepare 在 fork 前拿到锁（等后台线程释放），
//      parent/child 在 fork 后各自解锁 —— 子进程拿到的是一把"干净"的锁。
//
//   测试：必须在超时内输出 child-ok 和 parent-ok，退出码 0。卡住 = 子进程死锁在复制来的锁上。
//
//   现代意义：Python multiprocessing 在 Linux 上默认 fork 导致的各种神秘卡死（3.14 起默认改为 forkserver）、
//   Go 运行时根本不提供裸 fork、Redis 的 BGSAVE fork 后子进程只做只读快照、
//   glibc/jemalloc 用 pthread_atfork 保护 malloc 的锁 —— 都源于这一节。

#include "sl.h"

#include <errno.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdarg.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static pthread_mutex_t g_log_lock = PTHREAD_MUTEX_INITIALIZER;
static atomic_bool g_stop;
static sem_t g_lock_held; // 后台线程每次拿到锁后 post，让 main 确定"锁正被持有"再 fork

static void sleep_ms(long ms) {
    struct timespec ts = {.tv_sec = ms / 1000, .tv_nsec = (ms % 1000) * 1000000L};
    while (nanosleep(&ts, &ts) != 0 && errno == EINTR) {
    }
}

static void log_msg(const char *fmt, ...) {
    pthread_mutex_lock(&g_log_lock);
    va_list ap;
    va_start(ap, fmt);
    fprintf(stderr, "[log pid=%d] ", (int)getpid());
    vfprintf(stderr, fmt, ap);
    fputc('\n', stderr);
    va_end(ap);
    pthread_mutex_unlock(&g_log_lock);
}

// 后台刷盘线程：拿着锁"慢慢写"，偶尔松开一下
static void *flusher(void *arg) {
    while (!atomic_load(&g_stop)) {
        pthread_mutex_lock(&g_log_lock);
        sem_post(&g_lock_held);
        sleep_ms(200); // 持锁期间的慢 I/O
        pthread_mutex_unlock(&g_log_lock);
        sleep_ms(1);
    }
    return nullptr;
}

// TODO（修法 B）：写 fork 前/后的处理函数 —— prepare 里加锁，parent/child 里解锁，
//       然后在 main 开头用 pthread_atfork 注册它们。

int main(void) {
    setvbuf(stdout, nullptr, _IOLBF, 0);

    int rc;
    // TODO（修法 B）：在创建任何线程之前 pthread_atfork(...)，检查返回值

    if (sem_init(&g_lock_held, 0, 0) != 0)
        sl_die("sem_init");
    log_msg("parent: starting flusher thread");
    pthread_t tid;
    rc = pthread_create(&tid, nullptr, flusher, nullptr);
    if (rc != 0) {
        fprintf(stderr, "pthread_create: %s\n", strerror(rc));
        return 1;
    }
    while (sem_wait(&g_lock_held) != 0) {
    } // 此刻后台线程正持有 g_log_lock（它会持有 200ms）

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return 1;
    }
    if (pid == 0) {
        // 子进程
        // BUG: 这把锁是在"已上锁"状态下被复制过来的，持锁线程在子进程里不存在 → 永远等下去。
        // TODO: 修法 A —— exec 之前只用异步信号安全函数（删掉/替换这行）；或者用修法 B 让锁在 fork 时是干净的
        log_msg("child: about to exec echo");
        execlp("echo", "echo", "child-ok", (char *)nullptr);
        static const char msg[] = "thr5_fork_in_threads: exec echo failed\n";
        (void)!write(STDERR_FILENO, msg, sizeof msg - 1);
        _exit(127);
    }

    int status;
    while (waitpid(pid, &status, 0) < 0) {
        if (errno != EINTR) {
            perror("waitpid");
            return 1;
        }
    }
    log_msg("parent: child exited");
    atomic_store(&g_stop, true);
    rc = pthread_join(tid, nullptr);
    if (rc != 0) {
        fprintf(stderr, "pthread_join: %s\n", strerror(rc));
        return 1;
    }
    sem_destroy(&g_lock_held);

    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0) {
        fprintf(stderr, "child failed (status 0x%x)\n", (unsigned)status);
        return 1;
    }
    puts("parent-ok");
    return 0;
}
