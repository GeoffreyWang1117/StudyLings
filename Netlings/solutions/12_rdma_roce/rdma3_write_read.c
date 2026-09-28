// EXERCISE: rdma3_write_read — 单边操作：RDMA WRITE（带立即数）与 RDMA READ
// TOPIC: IBV_ACCESS_REMOTE_WRITE/READ / rkey / IBV_WR_RDMA_WRITE_WITH_IMM / IBV_WR_RDMA_READ / ibv_wc_status_str
// DIFFICULTY: ★★★★★
// BOOK: man 3 ibv_reg_mr（access 标志）；man 3 ibv_post_send（wr.rdma.remote_addr / rkey、imm_data）；man 3 ibv_poll_cq（IBV_WC_RECV_RDMA_WITH_IMM）；RDMA Aware Networks Programming User Manual
//
// 说明：
//   用法：rdma3_write_read server PORT [--size S] [--no-remote-access]
//         rdma3_write_read client HOST PORT [--size S] [--bulk N]
//         rdma3_write_read --selftest
//   设备/GID 的选择同 rdma2（NETLINGS_RDMA_DEV、NETLINGS_RDMA_GID_INDEX）。QP 建连代码与 rdma2 相同。
//
//   SEND/RECV 是"双边"操作：对端必须预先 post RECV 并处理完成。RDMA WRITE/READ 是"单边"的：
//   发起方直接读写对端**已注册**内存的某个虚拟地址，对端 CPU 完全不参与（连完成都没有）。
//   前提是对端把 {addr, rkey} 告诉你，并在注册 MR 时授予远端权限：
//     IBV_ACCESS_REMOTE_WRITE —— 允许别人 WRITE 进来（要求同时有 LOCAL_WRITE）
//     IBV_ACCESS_REMOTE_READ  —— 允许别人 READ 出去
//   QP 在 INIT 时也要打开 qp_access_flags 里对应的位。缺了 MR 的权限，发起方会收到
//   IBV_WC_REM_ACCESS_ERR —— ibv_wc_status_str 打印为 "remote access error"，而且 QP 进入错误状态。
//
//   流程：
//   1. 两端建好 RC QP（同 rdma2）；server 的 MR 大小 S，client 的 MR 大小 2S（前半发、后半收 READ 结果）；
//      server 的 MR 用 mr_access_flags(true)，QP 用 qp_access_flags()；带外交换 {qpn,psn,gid,mtu} + {addr,rkey,len}
//   2. client：前半填图案 → IBV_WR_RDMA_WRITE_WITH_IMM 写到 server 的 addr（imm_data = 0x4e4c3132）。
//      普通 RDMA WRITE 对端无感知；WITH_IMM 会在写完后消耗对端一个 RECV、产生
//      IBV_WC_RECV_RDMA_WITH_IMM 完成 —— 常用来"写完数据再通知"（NCCL 的 IB transport 就这么做）
//   3. server：等到这个完成，检查 imm 和缓冲区图案，把每个字节取反，通过 TCP 告诉 client "V"
//   4. client：IBV_WR_RDMA_READ 把 server 缓冲区读回后半，检查是取反后的图案
//   5. client：批量 N 次 RDMA WRITE（窗口 8 个未完成），算带宽。
//      打印 "write ok read ok bw_gbps=X"；server 打印 "server verified imm=0x4e4c3132" 与 "server done"
//   任何完成出错都打印 "wc error: <ibv_wc_status_str> (status=N) ..." 并以 1 退出。
//   --no-remote-access：server 故意用 mr_access_flags(false) 注册（只有 LOCAL_WRITE），
//   用来观察 client 端的 "remote access error"。
//
//   为什么：分布式训练的 AllReduce（NCCL）、分布式存储的数据面（Ceph/DAOS/3FS）、
//   远程内存/KV（FaRM、Pilaf）都靠单边操作把 CPU 从数据路径上拿掉。rkey 就是"内存能力凭证"：
//   泄露 rkey 等于把那段内存交给了对方，所以生产系统按需注册、用完即注销，或者用 Memory Window。
//
//   测试：--selftest 检查访问标志、WR 构造、{addr,rkey} 序列化；本机没有设备时检查提示信息。
//   有设备时：正常流程输出 "write ok read ok"；--no-remote-access 时 client 必须报告 WC 状态字符串。

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

enum { WIRE_LEN = 27, BUF_WIRE_LEN = 16, CQ_DEPTH = 16, WR_DEPTH = 16, TIMEOUT_MS = 10000, WINDOW = 8 };
enum { WRID_RECV = 1, WRID_WRITE_IMM = 2, WRID_READ = 3, WRID_BULK = 4 };
static const uint32_t IMM = 0x4e4c3132; // "NL12"

typedef struct {
    uint32_t qpn;
    uint32_t psn; // 24 位
    uint16_t lid;
    uint8_t mtu; // enum ibv_mtu
    uint8_t gid[16];
} conn_info;

typedef struct {
    uint64_t addr; // 对端 MR 里的虚拟地址
    uint32_t rkey;
    uint32_t len;
} remote_buf;

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

// MR 的访问权限。remote = true：允许对端 RDMA WRITE 和 READ 这块内存
static unsigned mr_access_flags(bool remote) {
    unsigned f = IBV_ACCESS_LOCAL_WRITE; // 网卡写本地内存（RECV、READ 结果）总是需要
    if (remote)
        f |= IBV_ACCESS_REMOTE_WRITE | IBV_ACCESS_REMOTE_READ;
    return f;
}

// QP 的访问权限（INIT 时设置）：允许对端在这个 QP 上发起 WRITE/READ
static unsigned qp_access_flags(void) { return IBV_ACCESS_REMOTE_WRITE | IBV_ACCESS_REMOTE_READ; }

static void pack_buf(const remote_buf *b, uint8_t out[BUF_WIRE_LEN]) {
    uint64_t addr = htobe64(b->addr);
    uint32_t rkey = htonl(b->rkey), len = htonl(b->len);
    memcpy(out, &addr, 8);
    memcpy(out + 8, &rkey, 4);
    memcpy(out + 12, &len, 4);
}

static void unpack_buf(const uint8_t in[BUF_WIRE_LEN], remote_buf *b) {
    uint64_t addr;
    uint32_t rkey, len;
    memcpy(&addr, in, 8);
    memcpy(&rkey, in + 8, 4);
    memcpy(&len, in + 12, 4);
    b->addr = be64toh(addr);
    b->rkey = ntohl(rkey);
    b->len = ntohl(len);
}

// 构造一个单边 WR：本地 [laddr, laddr+len)（lkey）↔ 对端 rb->addr（rb->rkey）
static void fill_rdma_wr(struct ibv_send_wr *wr, struct ibv_sge *sge, enum ibv_wr_opcode op, uint64_t wr_id,
                         uint64_t laddr, uint32_t len, uint32_t lkey, const remote_buf *rb, bool signaled) {
    *sge = (struct ibv_sge){.addr = laddr, .length = len, .lkey = lkey};
    *wr = (struct ibv_send_wr){
        .wr_id = wr_id,
        .sg_list = sge,
        .num_sge = 1,
        .opcode = op,
        .send_flags = signaled ? IBV_SEND_SIGNALED : 0,
    };
    wr->wr.rdma.remote_addr = rb->addr;
    wr->wr.rdma.rkey = rb->rkey;
    if (op == IBV_WR_RDMA_WRITE_WITH_IMM)
        wr->imm_data = htonl(IMM); // imm_data 按网络字节序传输
}

static void fill_pattern(uint8_t *p, size_t n, bool inverted) {
    for (size_t i = 0; i < n; i++) {
        uint8_t v = (uint8_t)(i * 7 + (i >> 8));
        p[i] = inverted ? (uint8_t)~v : v;
    }
}

static bool check_pattern(const uint8_t *p, size_t n, bool inverted) {
    for (size_t i = 0; i < n; i++) {
        uint8_t v = (uint8_t)(i * 7 + (i >> 8));
        if (p[i] != (inverted ? (uint8_t)~v : v)) {
            fprintf(stderr, "数据错误：offset %zu 期望 0x%02x 实际 0x%02x\n", i, inverted ? (uint8_t)~v : v, p[i]);
            return false;
        }
    }
    return true;
}

static int selftest(void) {
    SL_CHECK_EQ(mr_access_flags(true), IBV_ACCESS_LOCAL_WRITE | IBV_ACCESS_REMOTE_WRITE | IBV_ACCESS_REMOTE_READ);
    SL_CHECK_EQ(mr_access_flags(false), IBV_ACCESS_LOCAL_WRITE);
    SL_CHECK_EQ(qp_access_flags(), IBV_ACCESS_REMOTE_WRITE | IBV_ACCESS_REMOTE_READ);

    remote_buf rb = {.addr = 0x00007f1234567000ull, .rkey = 0xdeadbeef, .len = 65536}, back = {};
    uint8_t wire[BUF_WIRE_LEN];
    pack_buf(&rb, wire);
    SL_CHECK_EQ(wire[0], 0x00);
    SL_CHECK_EQ(wire[2], 0x7f);
    unpack_buf(wire, &back);
    SL_CHECK(back.addr == rb.addr);
    SL_CHECK_EQ(back.rkey, 0xdeadbeef);
    SL_CHECK_EQ(back.len, 65536);

    struct ibv_send_wr wr;
    struct ibv_sge sge;
    fill_rdma_wr(&wr, &sge, IBV_WR_RDMA_WRITE_WITH_IMM, 9, 0x1000, 4096, 0x77, &rb, true);
    SL_CHECK_EQ(wr.opcode, IBV_WR_RDMA_WRITE_WITH_IMM);
    SL_CHECK(wr.wr.rdma.remote_addr == rb.addr);
    SL_CHECK_EQ(wr.wr.rdma.rkey, 0xdeadbeef);
    SL_CHECK_EQ(ntohl(wr.imm_data), IMM);
    SL_CHECK_EQ(wr.send_flags, IBV_SEND_SIGNALED);
    SL_CHECK(wr.sg_list == &sge && wr.num_sge == 1);
    SL_CHECK_EQ(sge.lkey, 0x77);
    SL_CHECK_EQ(sge.length, 4096);
    fill_rdma_wr(&wr, &sge, IBV_WR_RDMA_READ, 3, 0x2000, 64, 0x77, &rb, false);
    SL_CHECK_EQ(wr.opcode, IBV_WR_RDMA_READ);
    SL_CHECK_EQ(wr.send_flags, 0);
    SL_CHECK(wr.wr.rdma.remote_addr == rb.addr);

    uint8_t buf[1024];
    fill_pattern(buf, sizeof buf, false);
    SL_CHECK(check_pattern(buf, sizeof buf, false));
    for (size_t i = 0; i < sizeof buf; i++)
        buf[i] = (uint8_t)~buf[i];
    SL_CHECK(check_pattern(buf, sizeof buf, true));
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
    uint8_t *buf; // 2*size 字节：server 只用前半；client 前半是 WRITE 的源，后半是 READ 的目的
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

static bool create_res(rdma_res *r, size_t size, unsigned mr_access, unsigned qp_access) {
    const bool events = false; // 本题只用忙轮询
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
    r->mr = ibv_reg_mr(r->pd, r->buf, 2 * size, (int)mr_access);
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
    init_attr(r->port, qp_access, &a, &mask);
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

// WRITE_WITH_IMM 会消耗对端一个 RECV WQE（数据写进 MR，不进 RECV 缓冲区），所以 RECV 可以没有 SGE
static bool post_recv_empty(rdma_res *r) {
    struct ibv_recv_wr wr = {.wr_id = WRID_RECV, .sg_list = nullptr, .num_sge = 0}, *bad = nullptr;
    int err = ibv_post_recv(r->qp, &wr, &bad);
    if (err)
        fprintf(stderr, "ibv_post_recv: %s\n", strerror(err));
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

static bool post_one(rdma_res *r, struct ibv_send_wr *wr) {
    struct ibv_send_wr *bad = nullptr;
    int err = ibv_post_send(r->qp, wr, &bad);
    if (err)
        fprintf(stderr, "ibv_post_send(opcode %d): %s\n", wr->opcode, strerror(err));
    return err == 0;
}

static bool server_flow(rdma_res *r, int fd) {
    struct ibv_wc wc;
    if (!wait_wc(r, &wc))
        return false;
    if (wc.opcode != IBV_WC_RECV_RDMA_WITH_IMM || !(wc.wc_flags & IBV_WC_WITH_IMM)) {
        fprintf(stderr, "期望 IBV_WC_RECV_RDMA_WITH_IMM 完成，实际 opcode=%d wc_flags=0x%x\n", wc.opcode, wc.wc_flags);
        return false;
    }
    uint32_t imm = ntohl(wc.imm_data);
    if (imm != IMM) {
        fprintf(stderr, "imm_data=0x%08x，期望 0x%08x\n", imm, IMM);
        return false;
    }
    if (!check_pattern(r->buf, r->size, false))
        return false;
    printf("server verified imm=0x%08x\n", imm);
    for (size_t i = 0; i < r->size; i++) // 取反：client 读回来时能证明读到的是远端的新数据
        r->buf[i] = (uint8_t)~r->buf[i];
    // 批量 WRITE 阶段 server 什么都不用做 —— 这就是"单边"
    if (!oob_barrier(fd, 'V') || !oob_barrier(fd, 'D'))
        return false;
    printf("server done\n");
    return true;
}

static bool client_flow(rdma_res *r, int fd, const remote_buf *rb, int bulk) {
    uint8_t *src = r->buf, *dst = r->buf + r->size;
    uint32_t len = (uint32_t)r->size;
    struct ibv_send_wr wr;
    struct ibv_sge sge;
    struct ibv_wc wc;

    fill_pattern(src, r->size, false);
    fill_rdma_wr(&wr, &sge, IBV_WR_RDMA_WRITE_WITH_IMM, WRID_WRITE_IMM, (uintptr_t)src, len, r->mr->lkey, rb, true);
    if (!post_one(r, &wr) || !wait_wc(r, &wc))
        return false;
    if (!oob_barrier(fd, 'V')) // 等 server 校验并取反
        return false;

    memset(dst, 0, r->size);
    fill_rdma_wr(&wr, &sge, IBV_WR_RDMA_READ, WRID_READ, (uintptr_t)dst, len, r->mr->lkey, rb, true);
    if (!post_one(r, &wr) || !wait_wc(r, &wc) || !check_pattern(dst, r->size, true))
        return false;

    // 批量写：最多 WINDOW 个未完成的 WR（每个都 signaled，简单起见）
    double t0 = now_us();
    int posted = 0, done = 0;
    while (done < bulk) {
        while (posted < bulk && posted - done < WINDOW) {
            fill_rdma_wr(&wr, &sge, IBV_WR_RDMA_WRITE, WRID_BULK, (uintptr_t)src, len, r->mr->lkey, rb, true);
            if (!post_one(r, &wr))
                return false;
            posted++;
        }
        if (!wait_wc(r, &wc))
            return false;
        done++;
    }
    double us = now_us() - t0;
    double gbps = us > 0 ? (double)bulk * (double)len * 8 / (us * 1e3) : 0;
    printf("write ok read ok bw_gbps=%.2f size=%u bulk=%d\n", gbps, len, bulk);
    return oob_barrier(fd, 'D');
}

// host == nullptr 表示 server
static bool session(rdma_res *r, bool is_client, const char *host, const char *port, int bulk) {
    if (!is_client && !post_recv_empty(r)) // 给 WRITE_WITH_IMM 准备的 RECV
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
    remote_buf mine = {.addr = (uintptr_t)r->buf, .rkey = r->mr->rkey, .len = (uint32_t)r->size};
    uint8_t wire[WIRE_LEN + BUF_WIRE_LEN];
    pack_info(&me, wire);
    pack_buf(&mine, wire + WIRE_LEN);
    bool ok = write_full(fd, wire, sizeof wire) && read_full(fd, wire, sizeof wire);
    if (ok) {
        conn_info peer;
        remote_buf rb;
        unpack_info(wire, &peer);
        unpack_buf(wire + WIRE_LEN, &rb);
        printf("local qpn=0x%06x rkey=0x%08x | remote qpn=0x%06x addr=0x%llx rkey=0x%08x len=%u\n", me.qpn,
               mine.rkey, peer.qpn, (unsigned long long)rb.addr, rb.rkey, rb.len);
        if (is_client && rb.len < r->size) {
            fprintf(stderr, "server 的缓冲区只有 %u 字节，小于 --size %zu\n", rb.len, r->size);
            ok = false;
        } else {
            ok = connect_qp(r, &peer) && oob_barrier(fd, 'R') &&
                 (is_client ? client_flow(r, fd, &rb, bulk) : server_flow(r, fd));
        }
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
        fprintf(stderr, "usage: %s server PORT [--size S] [--no-remote-access]\n"
                        "       %s client HOST PORT [--size S] [--bulk N]\n"
                        "       %s --selftest\n",
                argv[0], argv[0], argv[0]);
        return 2;
    }
    long size = 65536;
    int bulk = 2000;
    bool remote_access = true;
    for (int i = is_client ? 4 : 3; i < argc; i++) {
        if (strcmp(argv[i], "--size") == 0 && i + 1 < argc)
            size = atol(argv[++i]);
        else if (strcmp(argv[i], "--bulk") == 0 && i + 1 < argc && is_client)
            bulk = atoi(argv[++i]);
        else if (strcmp(argv[i], "--no-remote-access") == 0 && is_server)
            remote_access = false;
        else {
            fprintf(stderr, "unknown option %s\n", argv[i]);
            return 2;
        }
    }
    if (size <= 0 || size > (4 << 20) || bulk <= 0) {
        fprintf(stderr, "--size 应在 1..4194304，--bulk 应 > 0\n");
        return 2;
    }
    srand48((long)getpid() ^ (long)time(nullptr));

    rdma_res r = {};
    // client 的 MR 只被本地网卡读写（WRITE 的源、READ 的目的），不需要远端权限
    unsigned mr_access = is_server ? mr_access_flags(remote_access) : mr_access_flags(false);
    if (!create_res(&r, (size_t)size, mr_access, qp_access_flags())) {
        destroy_res(&r);
        return 2;
    }
    bool ok = is_server ? session(&r, false, nullptr, argv[2], bulk) : session(&r, true, argv[2], argv[3], bulk);
    destroy_res(&r);
    return ok ? 0 : 1;
}
