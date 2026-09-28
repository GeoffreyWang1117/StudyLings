## 提示 1
`man 3 ibv_modify_qp` 末尾有一张表：每个状态迁移"必需"和"可选"的 attr_mask 位。
RC QP 的 INIT→RTR 必需：`IBV_QP_STATE | IBV_QP_AV | IBV_QP_PATH_MTU | IBV_QP_DEST_QPN |
IBV_QP_RQ_PSN | IBV_QP_MAX_DEST_RD_ATOMIC | IBV_QP_MIN_RNR_TIMER`。
填了 `ah_attr` 却不在 mask 里放 `IBV_QP_AV`，内核根本不会看它。

## 提示 2
RoCE 没有子网管理器分配的 LID，路由完全靠 GRH 里的 GID：
```c
a->ah_attr.is_global = 1;
memcpy(a->ah_attr.grh.dgid.raw, remote->gid, 16);
a->ah_attr.grh.sgid_index = (uint8_t)sgid_index;   // 本端 RoCE v2 GID 下标（rdma1）
a->ah_attr.grh.hop_limit = 64;
```
sgid_index 选错（比如选了 RoCE v1 的表项），modify 能成功，但包会以 v1（以太类型 0x8915）发出，
对端 v2 QP 收不到 —— 表现为 client 等完成超时（`retry exceeded`）。

## 提示 3
RTR→RTS 必需：`IBV_QP_STATE | IBV_QP_TIMEOUT | IBV_QP_RETRY_CNT | IBV_QP_RNR_RETRY |
IBV_QP_SQ_PSN | IBV_QP_MAX_QP_RD_ATOMIC`。sq_psn 必须等于你告诉对端的 psn（对端把它填进 rq_psn）。
在真实设备上排错：`rdma resource show qp` 看 QP 状态；`ibv_rc_pingpong -d mlx5_0 -g <idx>` 是官方参考实现。
