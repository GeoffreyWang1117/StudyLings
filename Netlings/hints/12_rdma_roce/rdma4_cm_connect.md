## 提示 1
client 的事件顺序固定：`ADDR_RESOLVED` → 你调 `rdma_resolve_route` → `ROUTE_RESOLVED` →
你建 PD/CQ/QP 并 `rdma_connect` → `ESTABLISHED`。每一步都是"发起异步操作，然后等下一个事件"，
和非阻塞 `connect()` + epoll 的思路一样。

## 提示 2
`client_next_step` 里加上 `case RDMA_CM_EVENT_ROUTE_RESOLVED: return STEP_CONNECT;`。
`STEP_RESOLVE_ROUTE` 分支：
```c
if (rdma_resolve_route(r.id, RESOLVE_MS) < 0) {
    fprintf(stderr, "rdma_resolve_route: %s\n", strerror(errno));
    done = true;
}
```

## 提示 3
为什么建 QP 要等到 ROUTE_RESOLVED（至少 ADDR_RESOLVED）之后？因为在那之前 `id->verbs` 还是 NULL ——
CM 要先根据目的 IP 查路由，才知道该用哪块 RDMA 设备、哪个端口、哪个 GID。
真实设备上排错：`rdma resource show cm_id` 查看 CM 状态；`rping -s` / `rping -c -a <ip> -v` 是官方示例。
