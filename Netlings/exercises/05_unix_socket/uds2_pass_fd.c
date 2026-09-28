// EXERCISE: uds2_pass_fd — 用 SCM_RIGHTS 在进程之间传递打开的文件描述符
// TOPIC: sendmsg / recvmsg / 辅助数据 cmsg / SCM_RIGHTS / MSG_CMSG_CLOEXEC
// DIFFICULTY: ★★★☆☆
// BOOK: UNP §15.7（传递描述符）；APUE §17.4；man 7 unix, man 3 cmsg
// I AM NOT DONE
//
// 说明：
//   用法：uds2_pass_fd recv SOCKPATH       监听 SOCKPATH，打印 "listening on SOCKPATH"，
//                                          accept 一个连接，收到 fd 后把它指向的文件内容拷贝到 stdout
//         uds2_pass_fd send SOCKPATH FILE  打开 FILE（只读），connect 到 SOCKPATH，
//                                          用 sendmsg 把这个 fd（外加 1 字节普通数据）发过去
//
//   通过 UDS 传过去的不是"文件名"也不是"数字 3"，而是内核里的打开文件表项（struct file）本身：
//   接收方拿到一个新的 fd 号，指向同一个打开的文件（共享文件偏移量）。所以即使发送方 open 之后
//   文件就被 unlink 了，接收方照样能读 —— 探针就是这样检查你是否真的收到了 fd。
//
//   要点：
//   - fd 放在"辅助数据"（control message）里：cmsg_level = SOL_SOCKET, cmsg_type = SCM_RIGHTS，
//     用 CMSG_SPACE / CMSG_LEN / CMSG_FIRSTHDR / CMSG_DATA 这些宏构造和解析，别自己算偏移。
//   - 至少要带 1 字节普通数据：stream socket 上 0 字节的 sendmsg 可能什么也不发送。
//   - 接收方 recvmsg 要加 MSG_CMSG_CLOEXEC：收到的 fd 直接带 O_CLOEXEC，
//     避免在多线程程序里 fork+exec 时把它泄漏给子进程（和 SOCK_CLOEXEC / O_CLOEXEC 同一个道理）。
//   - 检查 MSG_CTRUNC：控制缓冲区太小时内核会丢掉 fd（并且被丢的 fd 会被内核关掉）。
//
//   现实中的用法：
//   - nginx 二进制热升级（kill -USR2）：新 master 通过继承拿到监听 socket；
//     Envoy hot restart、HAProxy 的 seamless reload（expose-fd listeners）则是用 SCM_RIGHTS 把
//     监听 socket 从旧进程"递"给新进程，一个连接都不丢。
//   - systemd socket activation / sd_pid_notify_with_fds(FDSTORE=1)：服务把 fd 存到 systemd，
//     重启后再拿回来。
//   - Chrome / Wayland：GPU 进程与渲染进程之间传递 dmabuf / memfd 共享内存 fd。

#include <errno.h>
#include <fcntl.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#include "sl.h"

static socklen_t make_addr(const char *path, struct sockaddr_un *sa) {
    memset(sa, 0, sizeof(*sa));
    sa->sun_family = AF_UNIX;
    size_t n = strlen(path);
    if (n + 1 > sizeof(sa->sun_path)) {
        fprintf(stderr, "uds2_pass_fd: path too long: %s\n", path);
        exit(2);
    }
    memcpy(sa->sun_path, path, n + 1);
    return (socklen_t)(offsetof(struct sockaddr_un, sun_path) + n + 1);
}

// 通过 sock 发送 fd_to_send，外加 1 字节普通数据。成功返回 0，失败返回 -1（errno 已设置）
static int send_fd(int sock, int fd_to_send) {
    char byte = 'F';
    struct iovec iov = {.iov_base = &byte, .iov_len = 1};

    // 控制缓冲区用 union 保证 struct cmsghdr 的对齐
    union {
        char buf[CMSG_SPACE(sizeof(int))];
        struct cmsghdr align;
    } ctrl;
    memset(&ctrl, 0, sizeof ctrl);

    struct msghdr msg = {
        .msg_iov = &iov,
        .msg_iovlen = 1,
        // TODO: 挂上控制缓冲区：.msg_control = ctrl.buf, .msg_controllen = sizeof ctrl.buf
    };
    // TODO: 用 CMSG_FIRSTHDR 取得第一个 cmsghdr，填 cmsg_level = SOL_SOCKET、
    //       cmsg_type = SCM_RIGHTS、cmsg_len = CMSG_LEN(sizeof(int))，
    //       再把 fd_to_send memcpy 到 CMSG_DATA(cm)（CMSG_DATA 不保证对齐，别直接 *(int *) 赋值）
    (void)fd_to_send;

    for (;;) {
        ssize_t n = sendmsg(sock, &msg, MSG_NOSIGNAL);
        if (n == 1)
            return 0;
        if (n < 0 && errno == EINTR)
            continue;
        if (n >= 0)
            errno = EIO;
        return -1;
    }
}

// 从 sock 接收一个 fd。成功返回收到的 fd（已带 FD_CLOEXEC），失败返回 -1
static int recv_fd(int sock) {
    char byte;
    struct iovec iov = {.iov_base = &byte, .iov_len = 1};
    union {
        char buf[CMSG_SPACE(sizeof(int))];
        struct cmsghdr align;
    } ctrl;
    struct msghdr msg = {
        .msg_iov = &iov,
        .msg_iovlen = 1,
        // TODO: 同样挂上控制缓冲区，否则内核没地方放 fd
    };
    (void)ctrl;

    ssize_t n;
    do {
        // TODO: flags 加上 MSG_CMSG_CLOEXEC
        n = recvmsg(sock, &msg, 0);
    } while (n < 0 && errno == EINTR);
    if (n < 0)
        return -1;
    if (n == 0) {
        fprintf(stderr, "uds2_pass_fd: peer closed without sending anything\n");
        errno = ENOMSG;
        return -1;
    }
    if (msg.msg_flags & MSG_CTRUNC) {
        fprintf(stderr, "uds2_pass_fd: control data truncated\n");
        errno = EMSGSIZE;
        return -1;
    }
    // TODO: 用 CMSG_FIRSTHDR / CMSG_NXTHDR 遍历控制消息，找到
    //       cmsg_level == SOL_SOCKET && cmsg_type == SCM_RIGHTS && cmsg_len == CMSG_LEN(sizeof(int))
    //       的那一条，从 CMSG_DATA 里 memcpy 出 fd 并返回
    fprintf(stderr, "uds2_pass_fd: message carried no SCM_RIGHTS fd\n");
    errno = ENOMSG;
    return -1;
}

static int copy_to_stdout(int fd) {
    char buf[65536];
    for (;;) {
        ssize_t r = read(fd, buf, sizeof buf);
        if (r == 0)
            return 0;
        if (r < 0) {
            if (errno == EINTR)
                continue;
            return -1;
        }
        if (fwrite(buf, 1, (size_t)r, stdout) != (size_t)r)
            return -1;
    }
}

static int do_send(const char *sockpath, const char *file) {
    int fd = open(file, O_RDONLY | O_CLOEXEC);
    if (fd < 0)
        sl_die(file);
    struct sockaddr_un sa;
    socklen_t len = make_addr(sockpath, &sa);
    int s = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (s < 0)
        sl_die("socket");
    if (connect(s, (struct sockaddr *)&sa, len) < 0)
        sl_die("connect");
    if (send_fd(s, fd) < 0)
        sl_die("send_fd");
    // 发送完就可以关掉自己的副本：内核里的 struct file 由接收方的引用继续保持
    close(fd);
    close(s);
    return 0;
}

static int do_recv(const char *sockpath) {
    struct sockaddr_un sa;
    socklen_t len = make_addr(sockpath, &sa);
    int lfd = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (lfd < 0)
        sl_die("socket");
    if (unlink(sockpath) < 0 && errno != ENOENT)
        sl_die("unlink");
    if (bind(lfd, (struct sockaddr *)&sa, len) < 0)
        sl_die("bind");
    if (listen(lfd, 8) < 0)
        sl_die("listen");
    printf("listening on %s\n", sockpath);
    fflush(stdout);

    int c;
    do {
        c = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
    } while (c < 0 && (errno == EINTR || errno == ECONNABORTED));
    if (c < 0)
        sl_die("accept4");

    int fd = recv_fd(c);
    if (fd < 0)
        sl_die("recv_fd");
    int fdflags = fcntl(fd, F_GETFD);
    if (fdflags < 0)
        sl_die("fcntl");
    fprintf(stderr, "received fd %d (cloexec=%d)\n", fd, (fdflags & FD_CLOEXEC) ? 1 : 0);

    int status = 0;
    if (copy_to_stdout(fd) < 0) {
        perror("copy");
        status = 1;
    }
    close(fd);
    close(c);
    close(lfd);
    unlink(sockpath);
    return status;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 3 && strcmp(argv[1], "recv") == 0)
        return do_recv(argv[2]);
    if (argc == 4 && strcmp(argv[1], "send") == 0)
        return do_send(argv[2], argv[3]);
    fprintf(stderr, "usage: %s recv SOCKPATH | send SOCKPATH FILE\n", argv[0]);
    return 2;
}
