## 提示 1
单边操作需要**两把钥匙**：发起方用对端 MR 的 `rkey` + 虚拟地址（`wr.wr.rdma.remote_addr / rkey`）；
对端注册 MR 时必须授予 `IBV_ACCESS_REMOTE_WRITE`（别人能写进来）和/或 `IBV_ACCESS_REMOTE_READ`
（别人能读出去）。注意 REMOTE_WRITE 必须和 LOCAL_WRITE 一起给，否则 ibv_reg_mr 返回 EINVAL。

## 提示 2
```c
static unsigned mr_access_flags(bool remote) {
    unsigned f = IBV_ACCESS_LOCAL_WRITE;
    if (remote) f |= IBV_ACCESS_REMOTE_WRITE | IBV_ACCESS_REMOTE_READ;
    return f;
}
```
`fill_rdma_wr` 里：`wr->wr.rdma.remote_addr = rb->addr; wr->wr.rdma.rkey = rb->rkey;`

## 提示 3
权限错了会怎样？发起方的完成状态是 `IBV_WC_REM_ACCESS_ERR`，`ibv_wc_status_str()` 打印
"remote access error"，而且**两端的 QP 都进入 ERROR 状态**，之后所有未完成的 WR 都以
"Work Request Flushed Error" 完成 —— RC QP 出错后只能重建（或 RESET 后重新走状态机）。
用 `server PORT --no-remote-access` 亲眼看一次。
