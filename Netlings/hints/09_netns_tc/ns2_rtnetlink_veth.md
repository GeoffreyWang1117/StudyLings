## 提示 1
先用现成工具看一眼消息长什么样：`ip -d link add a type veth peer name b` 背后就是一条 RTM_NEWLINK。
`strace -e trace=sendmsg -s 300 -xx ip link add a type veth peer name b` 能看到原始字节；
`ip monitor link` 能看到内核广播的结果。netlink 属性就是 TLV：`struct rtattr {len, type}` + 数据，按 4 字节对齐。

## 提示 2
nl_create_veth 的骨架：
```c
nlreq r;
struct ifinfomsg *ifi = nl_init(&r, RTM_NEWLINK, NLM_F_CREATE | NLM_F_EXCL, sizeof *ifi);
ifi->ifi_family = AF_UNSPEC;
nla_put_str(&r, IFLA_IFNAME, name);
struct rtattr *li = nla_nest_start(&r, IFLA_LINKINFO);
nla_put_str(&r, IFLA_INFO_KIND, "veth");
struct rtattr *data = nla_nest_start(&r, IFLA_INFO_DATA);
struct rtattr *peer_nest = nla_nest_start(&r, VETH_INFO_PEER);
/* 这里放 peer 的 struct ifinfomsg（nla_put_raw）和它的 IFLA_IFNAME、IFLA_NET_NS_PID */
nla_nest_end(&r, peer_nest); nla_nest_end(&r, data); nla_nest_end(&r, li);
return nl_talk(fd, &r);
```
内核回 EINVAL/ERANGE 通常是长度或嵌套没闭合；EEXIST 是名字已存在。

## 提示 3
地址：`struct ifaddrmsg *ifa = nl_init(&r, RTM_NEWADDR, NLM_F_CREATE | NLM_F_EXCL, sizeof *ifa);`
填 family/prefixlen/scope/index，然后 `nla_put(&r, IFA_LOCAL, &in, 4)` 和 `IFA_ADDRESS` 同值。
up：`RTM_NEWLINK`、flags 0，`ifi_index = ifindex; ifi_flags = IFF_UP; ifi_change = IFF_UP;`。
veth 两端都 up 之后 carrier 才会就绪，脚手架里的发送循环会自动重试。
