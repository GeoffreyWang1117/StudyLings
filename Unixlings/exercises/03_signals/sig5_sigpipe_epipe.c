// EXERCISE: sig5_sigpipe_epipe — 读端关闭时不要被 SIGPIPE 悄悄杀死
// TOPIC: SIGPIPE、EPIPE、忽略信号
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §10.2（SIGPIPE）, §15.2（管道：写一个读端已关闭的管道）；man 7 pipe
// I AM NOT DONE
//
// 说明：
//   用法：sig5_sigpipe_epipe
//   程序不停地往 stdout 写编号行 "line 1"、"line 2"……
//   当读者走掉（管道读端被关闭，例如 `sig5_sigpipe_epipe | head -n 3`）时，下一次 write(2)：
//     - 默认情况下内核给进程发 SIGPIPE，默认动作是 **终止进程**，不打印任何东西
//     - 如果 SIGPIPE 被忽略（SIG_IGN），write 改为返回 -1，errno == EPIPE
//   要求：忽略 SIGPIPE，在 write 失败且 errno == EPIPE 时向 stderr 打印 "peer closed"，退出码 0。
//   测试会：从管道读几行后关闭读端，要求进程以 0 退出且 stderr 含 peer closed。
//
//   为什么重要：往一个对端已关闭的 TCP socket 写数据，同样会触发 SIGPIPE。一个客户端突然断线
//   就能让整个服务器进程"无声无息"地消失。所以 nginx、Redis、Go runtime（对非 stdout/stderr
//   的 fd）、Node.js 启动时都会忽略 SIGPIPE；Linux 上还可以对单次 send(2) 用 MSG_NOSIGNAL，
//   macOS/BSD 上用 SO_NOSIGPIPE。

#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "sl.h"

// 把 buf[0..n) 全部写出。成功返回 0，失败返回 -1（errno 保持）
static int write_all(int fd, const char *buf, size_t n) {
    while (n > 0) {
        ssize_t w = write(fd, buf, n);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        buf += w;
        n -= (size_t)w;
    }
    return 0;
}

int main(void) {
    // TODO: 忽略 SIGPIPE（用 sigaction 把处理方式设为 SIG_IGN）

    char line[64];
    for (unsigned long i = 1;; i++) {
        int len = snprintf(line, sizeof line, "line %lu\n", i);
        if (write_all(STDOUT_FILENO, line, (size_t)len) < 0) {
            // TODO: errno == EPIPE 表示读者已经走了：向 stderr 打印 peer closed，正常退出（0）
            sl_die("write");
        }
    }
}
