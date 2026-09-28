// EXERCISE: thr3_bounded_queue — 互斥量 + 两个条件变量实现有界阻塞队列
// TOPIC: 条件变量、while 等待、关闭时 broadcast
// DIFFICULTY: ★★★★☆
// BOOK: APUE §11.6.6（条件变量）；man 3 pthread_cond_wait, pthread_cond_broadcast
//
// 说明：
//   用法：thr3_bounded_queue PRODUCERS CONSUMERS ITEMS_PER_PRODUCER
//   容量为 8 的环形队列，一把 mutex + 两个条件变量：
//     not_full  —— 队列满时生产者在这里睡，消费者取走一个后通知它
//     not_empty —— 队列空时消费者在这里睡，生产者放入一个后通知它
//   生产者 p 依次放入 p*ITEMS+1 .. p*ITEMS+ITEMS；main 等所有生产者 join 后调用 queue_close，
//   消费者把队列取空且看到 closed 后退出。最后打印：consumed=<取到的个数> sum=<所有取到数之和>
//
//   三条铁律：
//   1. pthread_cond_wait 必须放在 while 循环里重新检查条件：被唤醒 ≠ 条件成立
//      （虚假唤醒；或者别的线程抢先一步把刚放进来的元素取走了）
//   2. 放入后通知 not_empty，取出后通知 not_full —— 别发错条件变量
//   3. 关闭队列时要 broadcast：所有睡着的消费者都得醒来看到 closed，signal 只叫醒一个，其余永远睡下去
//
//   测试：若干 (P, C) 组合，检查 consumed/sum 精确正确，并且程序能在超时前结束（卡住 = 有线程没被唤醒）。
//
//   现代意义：这就是每一个线程池任务队列、Go 的带缓冲 channel（make(chan T, 8) + close(ch)）、
//   Java 的 ArrayBlockingQueue、tokio::sync::mpsc 的核心 —— 背压（满了就阻塞生产者）+ 关闭语义。

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { CAP = 8, MAX_THREADS = 64 };

struct queue {
    long buf[CAP];
    int head;  // 下一个要取的位置
    int count; // 当前元素个数
    bool closed;
    pthread_mutex_t mu;
    pthread_cond_t not_full;
    pthread_cond_t not_empty;
};

static struct queue g_q = {
    .mu = PTHREAD_MUTEX_INITIALIZER,
    .not_full = PTHREAD_COND_INITIALIZER,
    .not_empty = PTHREAD_COND_INITIALIZER,
};

// 放入 v；队列满时阻塞
static void queue_push(struct queue *q, long v) {
    pthread_mutex_lock(&q->mu);
    while (q->count == CAP)
        pthread_cond_wait(&q->not_full, &q->mu);
    q->buf[(q->head + q->count) % CAP] = v;
    q->count++;
    pthread_cond_signal(&q->not_empty);
    pthread_mutex_unlock(&q->mu);
}

// 取出一个元素写入 *out 并返回 true；队列已关闭且取空时返回 false
static bool queue_pop(struct queue *q, long *out) {
    pthread_mutex_lock(&q->mu);
    while (q->count == 0 && !q->closed)
        pthread_cond_wait(&q->not_empty, &q->mu);
    if (q->count == 0) { // 只可能是 closed 且已取空
        pthread_mutex_unlock(&q->mu);
        return false;
    }
    *out = q->buf[q->head];
    q->head = (q->head + 1) % CAP;
    q->count--;
    pthread_cond_signal(&q->not_full);
    pthread_mutex_unlock(&q->mu);
    return true;
}

// 关闭队列：之后不再有 push；唤醒所有等待者
static void queue_close(struct queue *q) {
    pthread_mutex_lock(&q->mu);
    q->closed = true;
    pthread_cond_broadcast(&q->not_empty);
    pthread_cond_broadcast(&q->not_full);
    pthread_mutex_unlock(&q->mu);
}

// ---- 以下为脚手架 ----

struct producer_arg {
    long first;
    long n;
};

struct consumer_arg {
    long count;
    long long sum;
};

static void *producer(void *arg) {
    const struct producer_arg *a = arg;
    for (long i = 0; i < a->n; i++)
        queue_push(&g_q, a->first + i);
    return nullptr;
}

static void *consumer(void *arg) {
    struct consumer_arg *a = arg;
    long v;
    while (queue_pop(&g_q, &v)) {
        a->count++;
        a->sum += v;
    }
    return nullptr;
}

static void check(int rc, const char *what) {
    if (rc != 0) {
        fprintf(stderr, "%s: %s\n", what, strerror(rc));
        exit(1);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s PRODUCERS CONSUMERS ITEMS_PER_PRODUCER\n", argv[0]);
        return 2;
    }
    int np = atoi(argv[1]), nc = atoi(argv[2]);
    long items = atol(argv[3]);
    if (np < 0 || np > MAX_THREADS || nc < 1 || nc > MAX_THREADS || items < 0) {
        fprintf(stderr, "thr3_bounded_queue: bad arguments\n");
        return 2;
    }

    pthread_t ptid[MAX_THREADS], ctid[MAX_THREADS];
    struct producer_arg pa[MAX_THREADS];
    struct consumer_arg ca[MAX_THREADS] = {};

    for (int i = 0; i < nc; i++)
        check(pthread_create(&ctid[i], nullptr, consumer, &ca[i]), "pthread_create");
    for (int i = 0; i < np; i++) {
        pa[i] = (struct producer_arg){.first = i * items + 1, .n = items};
        check(pthread_create(&ptid[i], nullptr, producer, &pa[i]), "pthread_create");
    }
    for (int i = 0; i < np; i++)
        check(pthread_join(ptid[i], nullptr), "pthread_join");
    queue_close(&g_q);

    long count = 0;
    long long sum = 0;
    for (int i = 0; i < nc; i++) {
        check(pthread_join(ctid[i], nullptr), "pthread_join");
        count += ca[i].count;
        sum += ca[i].sum;
    }
    printf("consumed=%ld sum=%lld\n", count, sum);
    return 0;
}
