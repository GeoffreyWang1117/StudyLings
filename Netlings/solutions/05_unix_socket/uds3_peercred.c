// EXERCISE: uds3_peercred — 用 SO_PEERCRED 查出"是谁连上了我"
// TOPIC: 凭证传递 / getsockopt(SO_PEERCRED) / struct ucred
// DIFFICULTY: ★★☆☆☆
// BOOK: UNP §15.8（接收发送者凭证）；man 7 unix（SO_PEERCRED）；man 7 socket
//
// 说明：
//   用法：uds3_peercred PATH
//   在 PATH 上监听（AF_UNIX SOCK_STREAM），打印 "listening on PATH"，
//   对每个连进来的客户端回一行 "pid=<p> uid=<u> gid=<g>\n" 然后关闭连接。
//   这三个数字必须是**对端（客户端）**的，由内核在 connect() 那一刻记录下来，客户端无法伪造。
//   探针用 Python 连进来，和客户端自己的 os.getpid()/getuid()/getgid() 比较。
//
//   谁在用：
//   - dockerd：/var/run/docker.sock 靠文件权限 + 对端凭证判断调用者；
//   - PostgreSQL 的 peer 认证（pg_hba.conf: local all all peer）：用 SO_PEERCRED 取 uid，
//     映射成操作系统用户名，免密码登录（`sudo -u postgres psql` 就是这么进去的）；
//   - D-Bus、systemd-journald、polkit、containerd 的 ttrpc 都据此做权限判断。
//   注意 pid 可能在你检查之后就被复用 —— 较新的内核提供 SO_PEERPIDFD 拿一个 pidfd，更安全。

#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#include "sl.h"

// 查询 fd 对端的凭证。成功返回 0，失败返回 -1
static int peer_cred(int fd, struct ucred *out) {
    socklen_t len = sizeof(*out);
    if (getsockopt(fd, SOL_SOCKET, SO_PEERCRED, out, &len) < 0)
        return -1;
    if (len != sizeof(*out)) {
        errno = EINVAL;
        return -1;
    }
    return 0;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc != 2) {
        fprintf(stderr, "usage: %s PATH\n", argv[0]);
        return 2;
    }
    const char *path = argv[1];
    struct sockaddr_un sa = {.sun_family = AF_UNIX};
    size_t n = strlen(path);
    if (n + 1 > sizeof(sa.sun_path)) {
        fprintf(stderr, "uds3_peercred: path too long\n");
        return 2;
    }
    memcpy(sa.sun_path, path, n + 1);
    socklen_t salen = (socklen_t)(offsetof(struct sockaddr_un, sun_path) + n + 1);

    int lfd = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (lfd < 0)
        sl_die("socket");
    if (unlink(path) < 0 && errno != ENOENT)
        sl_die("unlink");
    if (bind(lfd, (struct sockaddr *)&sa, salen) < 0)
        sl_die("bind");
    if (listen(lfd, 64) < 0)
        sl_die("listen");
    printf("listening on %s\n", path);

    for (;;) {
        int c = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
        if (c < 0) {
            if (errno == EINTR || errno == ECONNABORTED)
                continue;
            sl_die("accept4");
        }
        struct ucred cred;
        if (peer_cred(c, &cred) < 0) {
            perror("SO_PEERCRED");
            close(c);
            continue;
        }
        char line[128];
        int len = snprintf(line, sizeof line, "pid=%ld uid=%ld gid=%ld\n", (long)cred.pid,
                           (long)cred.uid, (long)cred.gid);
        if (send(c, line, (size_t)len, MSG_NOSIGNAL) < 0)
            perror("send");
        printf("served %s", line);
        close(c);
    }
}
