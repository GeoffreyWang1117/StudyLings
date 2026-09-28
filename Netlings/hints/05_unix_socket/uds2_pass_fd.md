## 提示 1
消息 = 普通数据（iov，至少 1 字节）+ 控制数据（msg_control）。控制缓冲区大小用
`CMSG_SPACE(sizeof(int))`（含对齐填充），单条 cmsghdr 的 `cmsg_len` 用 `CMSG_LEN(sizeof(int))`（不含尾部填充）。

## 提示 2
发送：`cm = CMSG_FIRSTHDR(&msg); cm->cmsg_level = SOL_SOCKET; cm->cmsg_type = SCM_RIGHTS;
cm->cmsg_len = CMSG_LEN(sizeof(int)); memcpy(CMSG_DATA(cm), &fd, sizeof fd);`
接收：`recvmsg(sock, &msg, MSG_CMSG_CLOEXEC)`，然后
`for (cm = CMSG_FIRSTHDR(&msg); cm; cm = CMSG_NXTHDR(&msg, cm))` 里判断 level/type/len。

## 提示 3
收到的 fd 号一般和发送方的不同（接收方分配最小可用的号），但 `ls -l /proc/<pid>/fd` 会显示同一个文件，
被 unlink 的文件会显示成 `... (deleted)`。`strace -e trace=sendmsg,recvmsg` 可以看到 `SCM_RIGHTS`。
