// EXERCISE: rdma2_rc_pingpong — RC QP 的 SEND/RECV 乒乓：PD/MR/CQ/QP 与 RESET→INIT→RTR→RTS
// TOPIC: ibv_alloc_pd / ibv_reg_mr / ibv_create_cq / ibv_create_qp / ibv_modify_qp / ibv_post_send / ibv_poll_cq
// DIFFICULTY: ★★★★★
// BOOK: man 3 ibv_modify_qp（每个状态迁移必需/可选的 attr_mask 表）；man 3 ibv_post_send；rdma-core 的 libibverbs/examples/rc_pingpong.c；RDMA Aware Networks Programming User Manual
//
// 说明：
//   用法：rdma2_rc_pingpong server PORT      [--iters N] [--size S] [--events]
//         rdma2_rc_pingpong client HOST PORT [--iters N] [--size S] [--events]
//         rdma2_rc_pingpong --selftest       纯函数自测（不需要设备）
//   设备：NETLINGS_RDMA_DEV（缺省第一个设备），端口 1；GID 下标：NETLINGS_RDMA_GID_INDEX，
//   缺省从 sysfs 自动挑 RoCE v2 + IPv4 的表项（rdma1 的逻辑）。
//
//   步骤（两端相同，除了谁先发）：
//   1. ibv_open_device → ibv_alloc_pd（保护域：MR 和 QP 必须属于同一个 PD 才能互相使用）
//   2. ibv_reg_mr 注册 2*S 字节（前半收、后半发），拿到 lkey
//   3. [--events] ibv_create_comp_channel；ibv_create_cq；ibv_create_qp(IBV_QPT_RC)
//   4. QP 状态机（每一步的 attr_mask 必须**恰好**包含该迁移要求的字段，多了少了都 EINVAL）：
//      RESET→INIT：STATE | PKEY_INDEX | PORT | ACCESS_FLAGS
//      INIT→RTR  ：STATE | AV | PATH_MTU | DEST_QPN | RQ_PSN | MAX_DEST_RD_ATOMIC | MIN_RNR_TIMER
//                  RoCE 没有 LID 路由，地址向量必须带 GRH：ah_attr.is_global = 1、grh.dgid = 对端 GID、
//                  grh.sgid_index = 本端 RoCE v2 GID 下标；path_mtu 取两端 active_mtu 的较小者
//      RTR→RTS   ：STATE | TIMEOUT | RETRY_CNT | RNR_RETRY | SQ_PSN | MAX_QP_RD_ATOMIC
//   5. 连接信息 {qpn, psn, lid, gid, mtu} 通过一条 TCP 连接交换（带外 OOB）——
//      RDMA 自己没法在 QP 建好之前通信。librdmacm 把这一步标准化了（见 rdma4）
//   6. 在进入 RTR 之前先 ibv_post_recv：RC 的 SEND 到达时接收方必须已经有 RECV WQE，
//      否则对端收到 RNR NAK，重试 rnr_retry 次后报错
//   7. client 发 ping（带序号）→ server 收到后先补一个 RECV 再回 pong → client 等 SEND 与 RECV 两个完成。
//      打印 "iters=N size=S avg_rtt_us=X avg_lat_us=Y"（Y = X/2，单程延迟）
//   完成事件：默认忙轮询 ibv_poll_cq（最低延迟，占满一个核）；--events 用完成通道：
//   ibv_req_notify_cq → poll(channel->fd) → ibv_get_cq_event → ibv_ack_cq_events → 再 poll_cq。
//
//   为什么：这是所有 RDMA 应用的地基 —— NCCL 的 IB transport、UCX、Ceph 的 RDMA messenger、
//   SPDK NVMe-oF、各种 RDMA KV 存储都是这几十行 verbs 调用。建连的状态机和 attr_mask 是最容易出错的地方
//   （ibv_modify_qp 只会返回一个 EINVAL，不告诉你缺了哪个位），所以本题把它们写成纯函数单独测。
//
//   测试：--selftest 检查三个状态迁移的 attr/mask 和连接信息的序列化；本机没有设备时检查提示信息。
//   有设备时（rxe 或 mlx5，同一主机上 server + client 走网卡 loopback）：1000 次乒乓数据正确，
//   忙轮询和 --events 两种模式都要通过。

#include <arpa/inet.h>
#include <endian.h>
#include <errno.h>
#include <fcntl.h>
#include <infiniband/verbs.h>
#include <netdb.h>
#include <netinet/in.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

enum { WIRE_LEN = 27, CQ_DEPTH = 16, WR_DEPTH = 16, TIMEOUT_MS = 10000 };
enum { WRID_RECV = 1, WRID_SEND = 2 };

typedef struct {
    uint32_t qpn;
    uint32_t psn; // 24 位
    uint16_t lid;
    uint8_t mtu; // enum ibv_mtu
    uint8_t gid[16];
} conn_info;

// ---------- 纯函数（--selftest 覆盖） ----------

// 连接信息 → 27 字节大端格式（两端可能是不同架构，不能直接发结构体）
static void pack_info(const conn_info *c, uint8_t out[WIRE_LEN]) {
    uint32_t qpn = htonl(c->qpn), psn = htonl(c->psn);
    uint16_t lid = htons(c->lid);
    memcpy(out, &qpn, 4);
    memcpy(out + 4, &psn, 4);
    memcpy(out + 8, &lid, 2);
    out[10] = c->mtu;
    memcpy(out + 11, c->gid, 16);
}

static void unpack_info(const uint8_t in[WIRE_LEN], conn_info *c) {
    uint32_t qpn, psn;
    uint16_t lid;
    memcpy(&qpn, in, 4);
    memcpy(&psn, in + 4, 4);
    memcpy(&lid, in + 8, 2);
    c->qpn = ntohl(qpn);
    c->psn = ntohl(psn) & 0xffffff;
    c->lid = ntohs(lid);
    c->mtu = in[10];
    memcpy(c->gid, in + 11, 16);
}

static enum ibv_mtu min_mtu(enum ibv_mtu a, enum ibv_mtu b) { return a < b ? a : b; }

static void init_attr(uint8_t port, unsigned access, struct ibv_qp_attr *a, int *mask) {
    *a = (struct ibv_qp_attr){
        .qp_state = IBV_QPS_INIT,
        .pkey_index = 0,
        .port_num = port,
        .qp_access_flags = access,
    };
    *mask = IBV_QP_STATE | IBV_QP_PKEY_INDEX | IBV_QP_PORT | IBV_QP_ACCESS_FLAGS;
}

// global = 是否带 GRH（RoCE 必须；IB 子网内可以只用 LID）
static void rtr_attr(const conn_info *remote, uint8_t port, int sgid_index, enum ibv_mtu mtu, bool global,
                     struct ibv_qp_attr *a, int *mask) {
    *a = (struct ibv_qp_attr){
        .qp_state = IBV_QPS_RTR,
        .path_mtu = mtu,
        .dest_qp_num = remote->qpn,
        .rq_psn = remote->psn,
        .max_dest_rd_atomic = 1, // 允许对端同时发起的 RDMA READ/原子操作数（rdma3 要用 READ）
        .min_rnr_timer = 12,     // 对端没有 RECV WQE 时让它等 ~0.64ms 再重试
        .ah_attr = {
            .dlid = remote->lid,
            .sl = 0,
            .src_path_bits = 0,
            .port_num = port,
        },
    };
    if (global) {
        a->ah_attr.is_global = 1;
        memcpy(a->ah_attr.grh.dgid.raw, remote->gid, 16);
        a->ah_attr.grh.sgid_index = (uint8_t)sgid_index;
        a->ah_attr.grh.hop_limit = 64; // RoCE v2 经过三层路由时就是 IP TTL
        a->ah_attr.grh.traffic_class = 0;
        a->ah_attr.grh.flow_label = 0;
    }
    *mask = IBV_QP_STATE | IBV_QP_AV | IBV_QP_PATH_MTU | IBV_QP_DEST_QPN | IBV_QP_RQ_PSN |
            IBV_QP_MAX_DEST_RD_ATOMIC | IBV_QP_MIN_RNR_TIMER;
}

static void rts_attr(uint32_t my_psn, struct ibv_qp_attr *a, int *mask) {
    *a = (struct ibv_qp_attr){
        .qp_state = IBV_QPS_RTS,
        .timeout = 14,  // 本地 ACK 超时 4.096us * 2^14 ≈ 67ms
        .retry_cnt = 7, // 传输错误重试次数
        .rnr_retry = 7, // 7 = 无限重试 RNR
        .sq_psn = my_psn,
        .max_rd_atomic = 1,
    };
    *mask = IBV_QP_STATE | IBV_QP_TIMEOUT | IBV_QP_RETRY_CNT | IBV_QP_RNR_RETRY | IBV_QP_SQ_PSN |
            IBV_QP_MAX_QP_RD_ATOMIC;
}

static int selftest(void) {
    conn_info c = {.qpn = 0x123456, .psn = 0xabcdef, .lid = 7, .mtu = IBV_MTU_1024}, d = {};
    for (int i = 0; i < 16; i++)
        c.gid[i] = (uint8_t)(i * 17);
    uint8_t wire[WIRE_LEN];
    pack_info(&c, wire);
    SL_CHECK_EQ(wire[0], 0x00);
    SL_CHECK_EQ(wire[1], 0x12); // 大端
    unpack_info(wire, &d);
    SL_CHECK_EQ(d.qpn, c.qpn);
    SL_CHECK_EQ(d.psn, c.psn);
    SL_CHECK_EQ(d.lid, 7);
    SL_CHECK_EQ(d.mtu, IBV_MTU_1024);
    SL_CHECK(memcmp(d.gid, c.gid, 16) == 0);
    SL_CHECK_EQ(min_mtu(IBV_MTU_4096, IBV_MTU_1024), IBV_MTU_1024);

    struct ibv_qp_attr a;
    int mask = 0;
    init_attr(1, 0, &a, &mask);
    SL_CHECK_EQ(mask, IBV_QP_STATE | IBV_QP_PKEY_INDEX | IBV_QP_PORT | IBV_QP_ACCESS_FLAGS);
    SL_CHECK_EQ(a.qp_state, IBV_QPS_INIT);
    SL_CHECK_EQ(a.port_num, 1);

    rtr_attr(&c, 1, 3, IBV_MTU_1024, true, &a, &mask);
    SL_CHECK_EQ(mask, IBV_QP_STATE | IBV_QP_AV | IBV_QP_PATH_MTU | IBV_QP_DEST_QPN | IBV_QP_RQ_PSN |
                          IBV_QP_MAX_DEST_RD_ATOMIC | IBV_QP_MIN_RNR_TIMER);
    SL_CHECK_EQ(a.qp_state, IBV_QPS_RTR);
    SL_CHECK_EQ(a.dest_qp_num, 0x123456);
    SL_CHECK_EQ(a.rq_psn, 0xabcdef);
    SL_CHECK_EQ(a.path_mtu, IBV_MTU_1024);
    SL_CHECK_EQ(a.ah_attr.is_global, 1);
    SL_CHECK_EQ(a.ah_attr.grh.sgid_index, 3);
    SL_CHECK(a.ah_attr.grh.hop_limit > 0);
    SL_CHECK(memcmp(a.ah_attr.grh.dgid.raw, c.gid, 16) == 0);
    SL_CHECK_EQ(a.ah_attr.port_num, 1);
    SL_CHECK(a.max_dest_rd_atomic >= 1);
    rtr_attr(&c, 1, -1, IBV_MTU_1024, false, &a, &mask);
    SL_CHECK_EQ(a.ah_attr.is_global, 0);
    SL_CHECK_EQ(a.ah_attr.dlid, 7);

    rts_attr(0x42, &a, &mask);
    SL_CHECK_EQ(mask, IBV_QP_STATE | IBV_QP_TIMEOUT | IBV_QP_RETRY_CNT | IBV_QP_RNR_RETRY | IBV_QP_SQ_PSN |
                          IBV_QP_MAX_QP_RD_ATOMIC);
    SL_CHECK_EQ(a.qp_state, IBV_QPS_RTS);
    SL_CHECK_EQ(a.sq_psn, 0x42);
    SL_CHECK(a.timeout > 0 && a.retry_cnt > 0 && a.rnr_retry > 0);
    return sl_report();
}

// ---------- TCP 带外通道 ----------

static bool write_full(int fd, const void *buf, size_t n) {
    const uint8_t *p = buf;
    while (n > 0) {
        ssize_t w = send(fd, p, n, MSG_NOSIGNAL);
        if (w < 0) {
            if (errno == EINTR)
                continue;
            perror("oob send");
            return false;
        }
        p += w;
        n -= (size_t)w;
    }
    return true;
}

static bool read_full(int fd, void *buf, size_t n) {
    uint8_t *p = buf;
    while (n > 0) {
        ssize_t r = recv(fd, p, n, 0);
        if (r < 0) {
            if (errno == EINTR)
                continue;
            perror("oob recv");
            return false;
        }
        if (r == 0) {
            fprintf(stderr, "oob recv: 对端提前关闭了 TCP 连接\n");
            return false;
        }
        p += r;
        n -= (size_t)r;
    }
    return true;
}

static void set_oob_timeout(int fd) {
    struct timeval tv = {.tv_sec = 30};
    if (setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof tv) < 0)
        perror("setsockopt(SO_RCVTIMEO)");
}

static int oob_listen(int port) {
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    int one = 1;
    if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one) < 0)
        sl_die("setsockopt(SO_REUSEADDR)");
    struct sockaddr_in addr = {.sin_family = AF_INET, .sin_port = htons((uint16_t)port)};
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    if (bind(fd, (struct sockaddr *)&addr, sizeof addr) < 0)
        sl_die("bind");
    if (listen(fd, 1) < 0)
        sl_die("listen");
    return fd;
}

static int oob_connect(const char *host, const char *port) {
    struct addrinfo hints = {.ai_family = AF_INET, .ai_socktype = SOCK_STREAM}, *ai;
    int gai = getaddrinfo(host, port, &hints, &ai);
    if (gai != 0) {
        fprintf(stderr, "getaddrinfo(%s, %s): %s\n", host, port, gai_strerror(gai));
        return -1;
    }
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (fd < 0)
        sl_die("socket");
    // server 可能还在初始化：重试几秒
    for (int attempt = 0;; attempt++) {
        if (connect(fd, ai->ai_addr, ai->ai_addrlen) == 0)
            break;
        if (errno != ECONNREFUSED || attempt >= 50) {
            fprintf(stderr, "connect %s:%s: %s\n", host, port, strerror(errno));
            close(fd);
            freeaddrinfo(ai);
            return -1;
        }
        nanosleep(&(struct timespec){.tv_nsec = 100 * 1000 * 1000}, nullptr);
    }
    freeaddrinfo(ai);
    return fd;
}

// 两端互相发一个字节再等对方的：确保双方都走到了同一步
static bool oob_barrier(int fd, char tag) {
    char got = 0;
    if (!write_full(fd, &tag, 1) || !read_full(fd, &got, 1))
        return false;
    if (got != tag) {
        fprintf(stderr, "oob barrier: 期望 '%c'，收到 '%c'\n", tag, got);
        return false;
    }
    return true;
}

// ---------- RDMA 资源 ----------

typedef struct {
    struct ibv_context *ctx;
    struct ibv_pd *pd;
    struct ibv_comp_channel *ch;
    struct ibv_cq *cq;
    struct ibv_qp *qp;
    struct ibv_mr *mr;
    uint8_t *buf; // [0,size) 接收；[size,2size) 发送
    size_t size;
    uint8_t port;
    int gid_index; // -1 = 不用 GRH（IB 子网内）
    bool global;
    struct ibv_port_attr pattr;
    union ibv_gid gid;
    uint32_t psn;
} rdma_res;

// sysfs 里找第一个 RoCE v2 + IPv4 映射的 GID 下标（rdma1 的逻辑精简版）
static int auto_gid_index(const char *dev, uint8_t port, int tbl_len) {
    for (int i = 0; i < tbl_len; i++) {
        char path[256], type[32] = "", gid[64] = "";
        snprintf(path, sizeof path, "/sys/class/infiniband/%s/ports/%u/gid_attrs/types/%d", dev, port, i);
        FILE *f = fopen(path, "r");
        if (f == nullptr)
            continue;
        bool ok = fgets(type, sizeof type, f) != nullptr; // 空表项读出 EINVAL
        fclose(f);
        if (!ok || strncmp(type, "RoCE v2", 7) != 0)
            continue;
        snprintf(path, sizeof path, "/sys/class/infiniband/%s/ports/%u/gids/%d", dev, port, i);
        f = fopen(path, "r");
        if (f == nullptr)
            continue;
        ok = fgets(gid, sizeof gid, f) != nullptr;
        fclose(f);
        if (ok && strncmp(gid, "0000:0000:0000:0000:0000:ffff:", 30) == 0)
            return i;
    }
    return -1;
}

static struct ibv_context *open_device(const char *want) {
    int num = 0;
    errno = 0;
    struct ibv_device **list = ibv_get_device_list(&num);
    if (list == nullptr || num == 0) {
        fprintf(stderr, "no RDMA device: load rdma_rxe or use ConnectX（ibv_get_device_list: %s）\n",
                list == nullptr ? strerror(errno) : "0 devices");
        if (list)
            ibv_free_device_list(list);
        return nullptr;
    }
    struct ibv_device *dev = nullptr;
    for (int i = 0; i < num; i++)
        if (want == nullptr || strcmp(ibv_get_device_name(list[i]), want) == 0) {
            dev = list[i];
            break;
        }
    struct ibv_context *ctx = nullptr;
    if (dev == nullptr) {
        fprintf(stderr, "RDMA device %s not found\n", want);
    } else {
        ctx = ibv_open_device(dev);
        if (ctx == nullptr)
            fprintf(stderr, "ibv_open_device(%s): %s\n", ibv_get_device_name(dev), strerror(errno));
    }
    ibv_free_device_list(list);
    return ctx;
}

static void destroy_res(rdma_res *r) {
    int err;
    if (r->qp && (err = ibv_destroy_qp(r->qp)))
        fprintf(stderr, "ibv_destroy_qp: %s\n", strerror(err));
    if (r->mr && (err = ibv_dereg_mr(r->mr)))
        fprintf(stderr, "ibv_dereg_mr: %s\n", strerror(err));
    if (r->cq && (err = ibv_destroy_cq(r->cq)))
        fprintf(stderr, "ibv_destroy_cq: %s\n", strerror(err));
    if (r->ch && (err = ibv_destroy_comp_channel(r->ch)))
        fprintf(stderr, "ibv_destroy_comp_channel: %s\n", strerror(err));
    if (r->pd && (err = ibv_dealloc_pd(r->pd)))
        fprintf(stderr, "ibv_dealloc_pd: %s\n", strerror(err));
    if (r->ctx && ibv_close_device(r->ctx))
        fprintf(stderr, "ibv_close_device: %s\n", strerror(errno));
    free(r->buf);
    *r = (rdma_res){};
}

static bool create_res(rdma_res *r, size_t size, bool events) {
    const char *want = getenv("NETLINGS_RDMA_DEV");
    r->ctx = open_device(want && *want ? want : nullptr);
    if (r->ctx == nullptr)
        return false;
    const char *dev = ibv_get_device_name(r->ctx->device);
    r->port = 1;
    int err = ibv_query_port(r->ctx, r->port, &r->pattr);
    if (err) {
        fprintf(stderr, "ibv_query_port(%s, 1): %s\n", dev, strerror(err));
        return false;
    }
    if (r->pattr.state != IBV_PORT_ACTIVE)
        fprintf(stderr, "警告：%s 端口 1 状态为 %s（不是 ACTIVE，QP 建连会失败）\n", dev, ibv_port_state_str(r->pattr.state));

    const char *gi = getenv("NETLINGS_RDMA_GID_INDEX");
    r->gid_index = gi && *gi ? atoi(gi) : auto_gid_index(dev, r->port, r->pattr.gid_tbl_len);
    r->global = r->pattr.link_layer == IBV_LINK_LAYER_ETHERNET || (gi && *gi);
    if (r->global) {
        if (r->gid_index < 0 || r->gid_index >= r->pattr.gid_tbl_len) {
            fprintf(stderr, "%s: 没有可用的 RoCE v2 IPv4 GID（给网卡配 IPv4，或设置 NETLINGS_RDMA_GID_INDEX）\n", dev);
            return false;
        }
        err = ibv_query_gid(r->ctx, r->port, r->gid_index, &r->gid);
        if (err) {
            fprintf(stderr, "ibv_query_gid(%s, idx %d): %s\n", dev, r->gid_index, strerror(errno));
            return false;
        }
    }

    r->pd = ibv_alloc_pd(r->ctx);
    if (r->pd == nullptr) {
        fprintf(stderr, "ibv_alloc_pd: %s\n", strerror(errno));
        return false;
    }
    r->size = size;
    long page = sysconf(_SC_PAGESIZE);
    void *mem = nullptr;
    int merr = posix_memalign(&mem, page > 0 ? (size_t)page : 4096, 2 * size);
    if (merr != 0) {
        fprintf(stderr, "posix_memalign: %s\n", strerror(merr));
        return false;
    }
    r->buf = mem;
    memset(r->buf, 0, 2 * size);
    r->mr = ibv_reg_mr(r->pd, r->buf, 2 * size, IBV_ACCESS_LOCAL_WRITE);
    if (r->mr == nullptr) {
        fprintf(stderr, "ibv_reg_mr(%zu bytes): %s（非 root 时检查 ulimit -l）\n", 2 * size, strerror(errno));
        return false;
    }
    if (events) {
        r->ch = ibv_create_comp_channel(r->ctx);
        if (r->ch == nullptr) {
            fprintf(stderr, "ibv_create_comp_channel: %s\n", strerror(errno));
            return false;
        }
        int fl = fcntl(r->ch->fd, F_GETFL);
        if (fl < 0 || fcntl(r->ch->fd, F_SETFL, fl | O_NONBLOCK) < 0) {
            perror("fcntl(comp channel, O_NONBLOCK)");
            return false;
        }
    }
    r->cq = ibv_create_cq(r->ctx, CQ_DEPTH, nullptr, r->ch, 0);
    if (r->cq == nullptr) {
        fprintf(stderr, "ibv_create_cq: %s\n", strerror(errno));
        return false;
    }
    struct ibv_qp_init_attr qia = {
        .send_cq = r->cq,
        .recv_cq = r->cq,
        .cap = {.max_send_wr = WR_DEPTH, .max_recv_wr = WR_DEPTH, .max_send_sge = 1, .max_recv_sge = 1},
        .qp_type = IBV_QPT_RC,
        .sq_sig_all = 0,
    };
    r->qp = ibv_create_qp(r->pd, &qia);
    if (r->qp == nullptr) {
        fprintf(stderr, "ibv_create_qp: %s\n", strerror(errno));
        return false;
    }
    r->psn = (uint32_t)lrand48() & 0xffffff;

    struct ibv_qp_attr a;
    int mask;
    init_attr(r->port, 0, &a, &mask);
    err = ibv_modify_qp(r->qp, &a, mask);
    if (err) {
        fprintf(stderr, "ibv_modify_qp(RESET→INIT): %s\n", strerror(err));
        return false;
    }
    return true;
}

static bool connect_qp(rdma_res *r, const conn_info *remote) {
    struct ibv_qp_attr a;
    int mask;
    enum ibv_mtu mtu = r->pattr.active_mtu;
    if (remote->mtu >= IBV_MTU_256 && remote->mtu <= IBV_MTU_4096)
        mtu = min_mtu(mtu, (enum ibv_mtu)remote->mtu);
    rtr_attr(remote, r->port, r->gid_index, mtu, r->global, &a, &mask);
    int err = ibv_modify_qp(r->qp, &a, mask);
    if (err) {
        fprintf(stderr, "ibv_modify_qp(INIT→RTR): %s（检查 attr_mask、GID 下标、path_mtu）\n", strerror(err));
        return false;
    }
    rts_attr(r->psn, &a, &mask);
    err = ibv_modify_qp(r->qp, &a, mask);
    if (err) {
        fprintf(stderr, "ibv_modify_qp(RTR→RTS): %s\n", strerror(err));
        return false;
    }
    return true;
}

static bool post_recv(rdma_res *r) {
    struct ibv_sge sge = {.addr = (uintptr_t)r->buf, .length = (uint32_t)r->size, .lkey = r->mr->lkey};
    struct ibv_recv_wr wr = {.wr_id = WRID_RECV, .sg_list = &sge, .num_sge = 1}, *bad = nullptr;
    int err = ibv_post_recv(r->qp, &wr, &bad);
    if (err)
        fprintf(stderr, "ibv_post_recv: %s\n", strerror(err));
    return err == 0;
}

static bool post_send(rdma_res *r) {
    struct ibv_sge sge = {.addr = (uintptr_t)(r->buf + r->size), .length = (uint32_t)r->size, .lkey = r->mr->lkey};
    struct ibv_send_wr wr = {
        .wr_id = WRID_SEND, .sg_list = &sge, .num_sge = 1, .opcode = IBV_WR_SEND, .send_flags = IBV_SEND_SIGNALED};
    struct ibv_send_wr *bad = nullptr;
    int err = ibv_post_send(r->qp, &wr, &bad);
    if (err)
        fprintf(stderr, "ibv_post_send: %s\n", strerror(err));
    return err == 0;
}

static double now_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1e6 + (double)ts.tv_nsec / 1e3;
}

// 等一个完成：忙轮询或完成通道。超时/出错返回 false
static bool wait_wc(rdma_res *r, struct ibv_wc *wc) {
    double deadline = now_us() + TIMEOUT_MS * 1000.0;
    for (;;) {
        int n = ibv_poll_cq(r->cq, 1, wc);
        if (n < 0) {
            fprintf(stderr, "ibv_poll_cq 失败\n");
            return false;
        }
        if (n == 1)
            break;
        if (now_us() > deadline) {
            fprintf(stderr, "等待完成超时（%d ms）：对端 QP 状态不对？GID/MTU 配错时包会被静默丢弃\n", TIMEOUT_MS);
            return false;
        }
        if (r->ch == nullptr)
            continue; // 忙轮询
        // 事件模式：先武装通知，再 poll 一次防止"武装之前就到了"的完成被漏掉
        int err = ibv_req_notify_cq(r->cq, 0);
        if (err) {
            fprintf(stderr, "ibv_req_notify_cq: %s\n", strerror(err));
            return false;
        }
        n = ibv_poll_cq(r->cq, 1, wc);
        if (n < 0) {
            fprintf(stderr, "ibv_poll_cq 失败\n");
            return false;
        }
        if (n == 1)
            break;
        struct pollfd pfd = {.fd = r->ch->fd, .events = POLLIN};
        int pr = poll(&pfd, 1, 100);
        if (pr < 0 && errno != EINTR) {
            perror("poll(comp channel)");
            return false;
        }
        if (pr > 0) {
            struct ibv_cq *ev_cq;
            void *ev_ctx;
            if (ibv_get_cq_event(r->ch, &ev_cq, &ev_ctx) == 0)
                ibv_ack_cq_events(ev_cq, 1); // 每个事件都必须 ack，否则 destroy_cq 会卡住
            else if (errno != EAGAIN)
                perror("ibv_get_cq_event");
        }
    }
    if (wc->status != IBV_WC_SUCCESS) {
        fprintf(stderr, "wc error: %s (status=%d) wr_id=%llu opcode=%d vendor_err=0x%x\n", ibv_wc_status_str(wc->status),
                wc->status, (unsigned long long)wc->wr_id, wc->opcode, wc->vendor_err);
        return false;
    }
    return true;
}

// 等到 SEND 和 RECV 各完成一次（顺序不定）
static bool wait_send_and_recv(rdma_res *r, bool need_send, bool need_recv) {
    while (need_send || need_recv) {
        struct ibv_wc wc;
        if (!wait_wc(r, &wc))
            return false;
        if (wc.wr_id == WRID_SEND)
            need_send = false;
        else if (wc.wr_id == WRID_RECV)
            need_recv = false;
    }
    return true;
}

static void put_seq(uint8_t *p, size_t size, uint32_t seq) {
    for (size_t i = 0; i < size; i++)
        p[i] = (uint8_t)(seq + i);
}

static bool check_seq(const uint8_t *p, size_t size, uint32_t seq) {
    for (size_t i = 0; i < size; i++)
        if (p[i] != (uint8_t)(seq + i)) {
            fprintf(stderr, "数据错误：第 %u 轮 offset %zu 期望 %u 实际 %u\n", seq, i, (uint8_t)(seq + i), p[i]);
            return false;
        }
    return true;
}

static bool pingpong(rdma_res *r, bool is_client, int iters) {
    double t0 = now_us();
    for (int i = 0; i < iters; i++) {
        uint32_t seq = (uint32_t)i;
        if (is_client) {
            put_seq(r->buf + r->size, r->size, seq);
            if (!post_send(r) || !wait_send_and_recv(r, true, true))
                return false;
            if (!check_seq(r->buf, r->size, seq) || !post_recv(r))
                return false;
        } else {
            if (!wait_send_and_recv(r, false, true) || !check_seq(r->buf, r->size, seq))
                return false;
            if (!post_recv(r)) // 先补 RECV 再回复：client 的下一个 ping 到达时一定有 WQE
                return false;
            memcpy(r->buf + r->size, r->buf, r->size);
            if (!post_send(r) || !wait_send_and_recv(r, true, false))
                return false;
        }
    }
    double us = now_us() - t0;
    if (is_client)
        printf("iters=%d size=%zu avg_rtt_us=%.2f avg_lat_us=%.2f\n", iters, r->size, us / iters, us / iters / 2);
    else
        printf("server done iters=%d\n", iters);
    return true;
}

// 建 OOB 连接 → 交换连接信息 → RTR/RTS → 乒乓。host == nullptr 表示 server
static bool session(rdma_res *r, bool is_client, const char *host, const char *port, int iters) {
    // 在进入 RTR（以及告诉对端自己的 QPN）之前先放好接收 WQE
    if (!post_recv(r))
        return false;
    int fd;
    if (!is_client) {
        int lfd = oob_listen(atoi(port));
        printf("listening on port %s\n", port);
        fd = accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC);
        if (fd < 0)
            perror("accept4");
        close(lfd);
    } else {
        fd = oob_connect(host, port);
    }
    if (fd < 0)
        return false;
    set_oob_timeout(fd);

    conn_info me = {.qpn = r->qp->qp_num, .psn = r->psn, .lid = r->pattr.lid, .mtu = (uint8_t)r->pattr.active_mtu};
    memcpy(me.gid, r->gid.raw, 16);
    uint8_t wire[WIRE_LEN];
    pack_info(&me, wire);
    conn_info peer;
    bool ok = write_full(fd, wire, sizeof wire) && read_full(fd, wire, sizeof wire);
    if (ok) {
        unpack_info(wire, &peer);
        char g[INET6_ADDRSTRLEN] = "-";
        inet_ntop(AF_INET6, me.gid, g, sizeof g);
        printf("local qpn=0x%06x psn=0x%06x gid_index=%d gid=%s | remote qpn=0x%06x psn=0x%06x\n", me.qpn, me.psn,
               r->gid_index, g, peer.qpn, peer.psn);
        // 双方都 RTS 了再开始发；双方都结束了再销毁 QP（避免对端还在等 ACK）
        ok = connect_qp(r, &peer) && oob_barrier(fd, 'R') && pingpong(r, is_client, iters) && oob_barrier(fd, 'D');
    }
    close(fd);
    return ok;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 2 && strcmp(argv[1], "--selftest") == 0)
        return selftest();
    bool is_client = argc >= 4 && strcmp(argv[1], "client") == 0;
    bool is_server = argc >= 3 && strcmp(argv[1], "server") == 0;
    if (!is_client && !is_server) {
        fprintf(stderr, "usage: %s server PORT [--iters N] [--size S] [--events]\n"
                        "       %s client HOST PORT [--iters N] [--size S] [--events]\n"
                        "       %s --selftest\n",
                argv[0], argv[0], argv[0]);
        return 2;
    }
    int iters = 1000;
    long size = 64;
    bool events = false;
    for (int i = is_client ? 4 : 3; i < argc; i++) {
        if (strcmp(argv[i], "--iters") == 0 && i + 1 < argc)
            iters = atoi(argv[++i]);
        else if (strcmp(argv[i], "--size") == 0 && i + 1 < argc)
            size = atol(argv[++i]);
        else if (strcmp(argv[i], "--events") == 0)
            events = true;
        else {
            fprintf(stderr, "unknown option %s\n", argv[i]);
            return 2;
        }
    }
    if (iters <= 0 || size <= 0 || size > (1 << 20)) {
        fprintf(stderr, "--iters 应 > 0，--size 应在 1..1048576\n");
        return 2;
    }
    srand48((long)getpid() ^ (long)time(nullptr));

    rdma_res r = {};
    if (!create_res(&r, (size_t)size, events)) {
        destroy_res(&r);
        return 2;
    }
    bool ok = is_server ? session(&r, false, nullptr, argv[2], iters) : session(&r, true, argv[2], argv[3], iters);
    destroy_res(&r);
    return ok ? 0 : 1;
}
