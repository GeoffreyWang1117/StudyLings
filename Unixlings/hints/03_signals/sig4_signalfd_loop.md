## 提示 1
signalfd 只是"读取待决信号"的接口，**不会**改变信号的递送。信号必须先被阻塞才会停留在待决状态：
`sigprocmask(SIG_BLOCK, &mask, nullptr)`，而且要在 `signalfd` 之前（也在任何可能收到信号之前）。

## 提示 2
handle_signal：`struct signalfd_siginfo si; ssize_t r = read(sfd, &si, sizeof si);`
每次 read 至少要给 `sizeof si` 字节的缓冲区，否则返回 EINVAL。然后 `switch (si.ssi_signo)`。

## 提示 3
多线程程序里要用 `pthread_sigmask`，并且在创建其他线程之前阻塞，否则信号可能被递送给别的线程。
fork+exec 子进程前记得恢复信号掩码——被阻塞的信号掩码会被 exec 继承（systemd、nginx 都会这样做）。
