// EXERCISE: epoll3_timer_eventfd — 把定时器和跨线程唤醒接进同一个 epoll 循环
// TOPIC: timerfd_create / timerfd_settime / eventfd / 事件循环的 wakeup 机制
// DIFFICULTY: ★★★☆☆
// BOOK: man 2 timerfd_create；man 2 eventfd；man 7 epoll；modern Linux notes
//
// 说明：
//   用法：epoll3_timer_eventfd      （无参数）
//   - 一个 epoll 实例里注册两个 fd：
//       timerfd：每 50ms 到期一次（CLOCK_MONOTONIC，周期定时器）
//       eventfd：工作线程每隔 ~120ms 往里 write 一个 uint64_t 1，共 5 次，用来"叫醒"事件循环
//   - timerfd 可读 → read 出一个 uint64_t = 自上次读取以来到期的次数，打印 "tick <次数>"
//   - eventfd 可读 → read 出一个 uint64_t = 计数器当前值（读完清零；多次 write 可能合并成
//     一次读，所以值可能 > 1），打印 "wakeup <值>"
//   - 所有 wakeup 值累加到 5 后：退出循环，pthread_join 工作线程，关闭 fd，exit 0
//   - 注意：不读 timerfd/eventfd 的话它们一直可读，LT 模式的 epoll_wait 会立即返回 → busy loop
//   - 测试：退出码 0；wakeup 值之和恰好为 5；至少有一行 tick；几秒内结束
//
//   这正是现代运行时唤醒事件循环的方式：
//     libuv  —— uv_async_send() 写 eventfd（uv__async_send），定时器堆决定 epoll_wait 的 timeout
//     tokio/mio —— mio::Waker 在 Linux 上就是一个 eventfd；spawn 到别的线程的任务完成后靠它唤醒
//     Go runtime —— netpollBreak 写一个 eventfd 打断阻塞在 epoll_pwait 里的 M
//     systemd/sd-event —— 定时器直接用 timerfd
//   "一切皆 fd"让定时器、信号（signalfd）、跨线程通知都能和 socket 放进同一个 epoll_wait。

#include <errno.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <sys/eventfd.h>
#include <sys/timerfd.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

enum { N_WAKEUPS = 5, TICK_MS = 50, WORKER_SLEEP_MS = 120 };

// 工作线程：模拟"别的线程完成了一件事，通知事件循环"
static void *worker(void *arg) {
    int efd = *(int *)arg;
    for (int i = 0; i < N_WAKEUPS; i++) {
        struct timespec ts = {.tv_sec = 0, .tv_nsec = WORKER_SLEEP_MS * 1000000L};
        nanosleep(&ts, nullptr);
        uint64_t one = 1;
        if (write(efd, &one, sizeof one) != sizeof one)
            perror("worker: write eventfd");
    }
    return nullptr;
}

// 从 timerfd / eventfd 读出一个 8 字节计数器。成功返回 true 并写入 *out；
// 非阻塞 fd 暂时没数据（EAGAIN）返回 false
[[nodiscard]] static bool read_counter(int fd, uint64_t *out) {
    for (;;) {
        ssize_t n = read(fd, out, sizeof *out);
        if (n == (ssize_t)sizeof *out)
            return true;
        if (n < 0 && errno == EINTR)
            continue;
        if (n < 0 && errno == EAGAIN)
            return false;
        sl_die("read counter"); // timerfd/eventfd 的 read 要么 8 字节要么失败
    }
}

static int make_timer(int period_ms) {
    int tfd = timerfd_create(CLOCK_MONOTONIC, TFD_NONBLOCK | TFD_CLOEXEC);
    if (tfd < 0)
        sl_die("timerfd_create");
    struct timespec period = {.tv_sec = period_ms / 1000, .tv_nsec = (period_ms % 1000) * 1000000L};
    struct itimerspec its = {.it_interval = period, .it_value = period};
    if (timerfd_settime(tfd, 0, &its, nullptr) < 0)
        sl_die("timerfd_settime");
    return tfd;
}

static void watch(int epfd, int fd) {
    struct epoll_event ev = {.events = EPOLLIN, .data.fd = fd};
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &ev) < 0)
        sl_die("epoll_ctl ADD");
}

int main(void) {
    setvbuf(stdout, nullptr, _IOLBF, 0);

    int epfd = epoll_create1(EPOLL_CLOEXEC);
    if (epfd < 0)
        sl_die("epoll_create1");
    int tfd = make_timer(TICK_MS);
    int efd = eventfd(0, EFD_NONBLOCK | EFD_CLOEXEC);
    if (efd < 0)
        sl_die("eventfd");
    watch(epfd, tfd);
    watch(epfd, efd);

    pthread_t th;
    int rc = pthread_create(&th, nullptr, worker, &efd);
    if (rc != 0) {
        errno = rc;
        sl_die("pthread_create");
    }

    uint64_t total = 0;
    while (total < N_WAKEUPS) {
        struct epoll_event events[4];
        int n = epoll_wait(epfd, events, 4, -1);
        if (n < 0) {
            if (errno == EINTR)
                continue;
            sl_die("epoll_wait");
        }
        for (int i = 0; i < n; i++) {
            uint64_t v;
            if (events[i].data.fd == tfd) {
                if (read_counter(tfd, &v))
                    printf("tick %llu\n", (unsigned long long)v);
            } else if (events[i].data.fd == efd) {
                if (read_counter(efd, &v)) {
                    printf("wakeup %llu\n", (unsigned long long)v);
                    total += v;
                }
            }
        }
    }

    rc = pthread_join(th, nullptr);
    if (rc != 0) {
        errno = rc;
        sl_die("pthread_join");
    }
    close(tfd);
    close(efd);
    close(epfd);
    printf("done: %llu wakeups\n", (unsigned long long)total);
    return 0;
}
