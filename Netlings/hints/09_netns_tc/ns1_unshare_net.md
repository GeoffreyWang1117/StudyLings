## 提示 1
自己先在 shell 里体验一下：`unshare -rn sh -c 'ip link; ping -c1 127.0.0.1'` —— 只有一个 DOWN 的 lo，
连 127.0.0.1 都 ping 不通。`-r` 就是"映射成 root"，`-n` 就是新的 netns，你要用 C 做同样的事。

## 提示 2
`enter_private_netns`：`uid_t uid = getuid(); gid_t gid = getgid();` 必须在 unshare **之前**取；
然后 `unshare(CLONE_NEWUSER | CLONE_NEWNET)`，再依次
`write_file("/proc/self/setgroups", "deny")`、`write_file("/proc/self/uid_map", "0 <uid> 1\n")`、
`write_file("/proc/self/gid_map", "0 <gid> 1\n")`（用 snprintf 拼字符串）。顺序不能错：setgroups 在 gid_map 之前。

## 提示 3
`link_up`：
```c
int fd = socket(AF_INET, SOCK_DGRAM | SOCK_CLOEXEC, 0);
struct ifreq ifr = {};
snprintf(ifr.ifr_name, sizeof ifr.ifr_name, "%s", ifname);
ioctl(fd, SIOCGIFFLAGS, &ifr);      // 读
ifr.ifr_flags |= IFF_UP;
ioctl(fd, SIOCSIFFLAGS, &ifr);      // 写
close(fd);
```
每一步都检查返回值。验证：`ls -l /proc/<pid>/ns/net` 与 `ls -l /proc/self/ns/net` 的 inode 号不同。
