// EXERCISE: rdma4_cm_connect — 用 librdmacm 建立 RC 连接（生产代码的做法）
// TOPIC: rdma_create_event_channel / rdma_resolve_addr / rdma_resolve_route / rdma_connect / rdma_accept / private data
// DIFFICULTY: ★★★★☆
// BOOK: man 7 rdma_cm；man 3 rdma_resolve_addr / rdma_connect / rdma_accept / rdma_get_cm_event；rdma-core 的 librdmacm/examples/rping.c
// I AM NOT DONE
//
// 说明：
//   用法：rdma4_cm_connect server PORT [--iters N]
//         rdma4_cm_connect client IP PORT [--iters N]     IP 必须是 RDMA 网卡上配置的 IPv4 地址
//         rdma4_cm_connect --selftest
//   rdma2 里我们自己用 TCP 交换 {qpn, psn, gid}、自己调 ibv_modify_qp 走状态机。
//   RDMA CM（Connection Manager）把这些都标准化了，接口刻意模仿 socket：
//     client：rdma_create_id → rdma_resolve_addr(IP)   → 事件 ADDR_RESOLVED（IP→GID、选定本地设备/端口）
//             → rdma_resolve_route                      → 事件 ROUTE_RESOLVED（RoCE 上是邻居/路由解析）
//             → 在 id->verbs 上建 PD/CQ/MR，rdma_create_qp（QP 自动进入 INIT），post RECV
//             → rdma_connect(私有数据)                   → 事件 ESTABLISHED（QP 已被 CM 迁移到 RTS）
//     server：rdma_bind_addr(0.0.0.0:PORT) → rdma_listen → 事件 CONNECT_REQUEST（event->id 是新连接的 id，
//             类似 accept 返回的新 fd）→ 建资源、post RECV → rdma_accept(私有数据) → 事件 ESTABLISHED
//     结束：一方 rdma_disconnect → 两端都收到 DISCONNECTED
//   私有数据（private data）随 CM 的 REQ/REP 报文捎带（REQ 最多 56 字节），常用来交换协议版本、
//   缓冲区大小、{addr, rkey} 之类的应用参数；接收方看到的长度可能被**补零到最大值**，解析时只能要求 >=。
//   所有事件都通过 rdma_get_cm_event 取出，**必须 rdma_ack_cm_event**，而且 ack 之后
//   event->param 里的私有数据指针就失效了 —— 要先拷贝。
//   连接建立后的数据面和 rdma2 一样（SEND/RECV 乒乓），打印 "iters=N avg_rtt_us=X avg_lat_us=Y"。
//
//   为什么：NCCL（net_ib 用 verbs + 自己的 OOB，但 UCX/libfabric 路径走 rdma_cm）、SPDK/内核的 NVMe-oF RDMA、
//   iSER、SMB Direct、Ceph 的 RDMA 都用 RDMA CM 建连：它按 IP 寻址（能用 DNS/现有 IP 配置），
//   自动处理 GID 选择、路径 MTU、端口故障切换（bonding），还能跑在 iWARP 上（iWARP 只能用 CM 建连）。
//
//   测试：--selftest 检查 client/server 的事件→动作映射（尤其是 ROUTE_RESOLVED → connect）和私有数据编解码；
//   本机没有设备时检查提示信息。有设备时：server + client 在同一主机上通过网卡 IP（RoCE v2 GID 里的 IPv4，
//   或 NETLINGS_RDMA_IP）建连并乒乓 500 次。

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <infiniband/verbs.h>
#include <netdb.h>
#include <netinet/in.h>
#include <poll.h>
#include <rdma/rdma_cma.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include "sl.h"

enum { MSG_SIZE = 64, CQ_DEPTH = 16, WR_DEPTH = 16, TIMEOUT_MS = 15000, RESOLVE_MS = 2000, PRIV_LEN = 12 };
enum { WRID_RECV = 1, WRID_SEND = 2 };

enum step { STEP_IGNORE, STEP_RESOLVE_ROUTE, STEP_CONNECT, STEP_ACCEPT, STEP_RUN, STEP_DONE, STEP_FAIL };

typedef struct {
    char magic[4]; // "NL12"
    uint32_t version;
    uint32_t msg_size;
} hello;

// ---------- 纯函数（--selftest 覆盖） ----------

// client 状态机：收到某个 CM 事件后下一步做什么
static enum step client_next_step(enum rdma_cm_event_type ev) {
    switch (ev) {
    case RDMA_CM_EVENT_ADDR_RESOLVED: return STEP_RESOLVE_ROUTE;
    // TODO: 路由解析完成（RDMA_CM_EVENT_ROUTE_RESOLVED）之后就可以建 QP 并 rdma_connect 了 → STEP_CONNECT。
    //       现在它落进 default 被忽略，client 会一直等下去直到超时
    case RDMA_CM_EVENT_ESTABLISHED: return STEP_RUN;
    case RDMA_CM_EVENT_DISCONNECTED: return STEP_DONE;
    case RDMA_CM_EVENT_ADDR_ERROR:
    case RDMA_CM_EVENT_ROUTE_ERROR:
    case RDMA_CM_EVENT_CONNECT_ERROR:
    case RDMA_CM_EVENT_UNREACHABLE:
    case RDMA_CM_EVENT_REJECTED:
    case RDMA_CM_EVENT_DEVICE_REMOVAL: return STEP_FAIL;
    default: return STEP_IGNORE; // 例如 ADDR_CHANGE、TIMEWAIT_EXIT
    }
}

static enum step server_next_step(enum rdma_cm_event_type ev) {
    switch (ev) {
    case RDMA_CM_EVENT_CONNECT_REQUEST: return STEP_ACCEPT;
    case RDMA_CM_EVENT_ESTABLISHED: return STEP_RUN;
    case RDMA_CM_EVENT_DISCONNECTED: return STEP_DONE;
    case RDMA_CM_EVENT_CONNECT_ERROR:
    case RDMA_CM_EVENT_UNREACHABLE:
    case RDMA_CM_EVENT_REJECTED:
    case RDMA_CM_EVENT_DEVICE_REMOVAL: return STEP_FAIL;
    default: return STEP_IGNORE;
    }
}

static void pack_hello(uint32_t msg_size, uint8_t out[PRIV_LEN]) {
    uint32_t v = htonl(1), sz = htonl(msg_size);
    memcpy(out, "NL12", 4);
    memcpy(out + 4, &v, 4);
    memcpy(out + 8, &sz, 4);
}

// 对端的私有数据可能被补零到协议最大长度：只要求 len >= PRIV_LEN
static bool parse_hello(const void *data, size_t len, hello *h) {
    if (data == nullptr || len < PRIV_LEN)
        return false;
    const uint8_t *p = data;
    uint32_t v, sz;
    memcpy(h->magic, p, 4);
    memcpy(&v, p + 4, 4);
    memcpy(&sz, p + 8, 4);
    h->version = ntohl(v);
    h->msg_size = ntohl(sz);
    return memcmp(h->magic, "NL12", 4) == 0 && h->version == 1;
}

static int selftest(void) {
    SL_CHECK_EQ(client_next_step(RDMA_CM_EVENT_ADDR_RESOLVED), STEP_RESOLVE_ROUTE);
    SL_CHECK_EQ(client_next_step(RDMA_CM_EVENT_ROUTE_RESOLVED), STEP_CONNECT);
    SL_CHECK_EQ(client_next_step(RDMA_CM_EVENT_ESTABLISHED), STEP_RUN);
    SL_CHECK_EQ(client_next_step(RDMA_CM_EVENT_DISCONNECTED), STEP_DONE);
    SL_CHECK_EQ(client_next_step(RDMA_CM_EVENT_ROUTE_ERROR), STEP_FAIL);
    SL_CHECK_EQ(client_next_step(RDMA_CM_EVENT_REJECTED), STEP_FAIL);
    SL_CHECK_EQ(client_next_step(RDMA_CM_EVENT_ADDR_ERROR), STEP_FAIL);
    SL_CHECK_EQ(client_next_step(RDMA_CM_EVENT_TIMEWAIT_EXIT), STEP_IGNORE);
    SL_CHECK_EQ(server_next_step(RDMA_CM_EVENT_CONNECT_REQUEST), STEP_ACCEPT);
    SL_CHECK_EQ(server_next_step(RDMA_CM_EVENT_ESTABLISHED), STEP_RUN);
    SL_CHECK_EQ(server_next_step(RDMA_CM_EVENT_DISCONNECTED), STEP_DONE);

    uint8_t buf[56] = {}; // 模拟被补零到 56 字节的 REQ 私有数据
    pack_hello(4096, buf);
    hello h;
    SL_CHECK(parse_hello(buf, sizeof buf, &h));
    SL_CHECK_EQ(h.version, 1);
    SL_CHECK_EQ(h.msg_size, 4096);
    SL_CHECK(parse_hello(buf, PRIV_LEN, &h));
    SL_CHECK(!parse_hello(buf, PRIV_LEN - 1, &h));
    SL_CHECK(!parse_hello(nullptr, 0, &h));
    buf[0] = 'X';
    SL_CHECK(!parse_hello(buf, sizeof buf, &h));
    return sl_report();
}

// ---------- 连接资源 ----------

typedef struct {
    struct rdma_cm_id *id;
    struct ibv_pd *pd;
    struct ibv_cq *cq;
    struct ibv_mr *mr;
    uint8_t *buf; // [0,MSG_SIZE) 接收；[MSG_SIZE,2*MSG_SIZE) 发送
    bool qp_created;
} cm_res;

static void destroy_res(cm_res *r) {
    int err;
    if (r->qp_created)
        rdma_destroy_qp(r->id);
    if (r->mr && (err = ibv_dereg_mr(r->mr)))
        fprintf(stderr, "ibv_dereg_mr: %s\n", strerror(err));
    if (r->cq && (err = ibv_destroy_cq(r->cq)))
        fprintf(stderr, "ibv_destroy_cq: %s\n", strerror(err));
    if (r->pd && (err = ibv_dealloc_pd(r->pd)))
        fprintf(stderr, "ibv_dealloc_pd: %s\n", strerror(err));
    free(r->buf);
    struct rdma_cm_id *id = r->id;
    *r = (cm_res){.id = id};
}

// 在 id 绑定的设备（id->verbs，地址解析之后才有）上建 PD/CQ/MR/QP，并先放一个 RECV
static bool post_recv(cm_res *r);

static bool create_res(cm_res *r) {
    struct ibv_context *verbs = r->id->verbs;
    if (verbs == nullptr) {
        fprintf(stderr, "id->verbs 为空：地址还没解析到 RDMA 设备\n");
        return false;
    }
    r->pd = ibv_alloc_pd(verbs);
    if (r->pd == nullptr) {
        fprintf(stderr, "ibv_alloc_pd: %s\n", strerror(errno));
        return false;
    }
    r->cq = ibv_create_cq(verbs, CQ_DEPTH, nullptr, nullptr, 0);
    if (r->cq == nullptr) {
        fprintf(stderr, "ibv_create_cq: %s\n", strerror(errno));
        return false;
    }
    r->buf = calloc(2, MSG_SIZE);
    if (r->buf == nullptr) {
        perror("calloc");
        return false;
    }
    r->mr = ibv_reg_mr(r->pd, r->buf, 2 * MSG_SIZE, IBV_ACCESS_LOCAL_WRITE);
    if (r->mr == nullptr) {
        fprintf(stderr, "ibv_reg_mr: %s（非 root 时检查 ulimit -l）\n", strerror(errno));
        return false;
    }
    struct ibv_qp_init_attr qia = {
        .send_cq = r->cq,
        .recv_cq = r->cq,
        .cap = {.max_send_wr = WR_DEPTH, .max_recv_wr = WR_DEPTH, .max_send_sge = 1, .max_recv_sge = 1},
        .qp_type = IBV_QPT_RC,
    };
    // rdma_create_qp 建 QP 并把它迁移到 INIT；RTR/RTS 由 rdma_connect/rdma_accept 完成
    if (rdma_create_qp(r->id, r->pd, &qia) < 0) {
        fprintf(stderr, "rdma_create_qp: %s\n", strerror(errno));
        return false;
    }
    r->qp_created = true;
    return post_recv(r);
}

static bool post_recv(cm_res *r) {
    struct ibv_sge sge = {.addr = (uintptr_t)r->buf, .length = MSG_SIZE, .lkey = r->mr->lkey};
    struct ibv_recv_wr wr = {.wr_id = WRID_RECV, .sg_list = &sge, .num_sge = 1}, *bad = nullptr;
    int err = ibv_post_recv(r->id->qp, &wr, &bad);
    if (err)
        fprintf(stderr, "ibv_post_recv: %s\n", strerror(err));
    return err == 0;
}

static bool post_send(cm_res *r) {
    struct ibv_sge sge = {.addr = (uintptr_t)(r->buf + MSG_SIZE), .length = MSG_SIZE, .lkey = r->mr->lkey};
    struct ibv_send_wr wr = {
        .wr_id = WRID_SEND, .sg_list = &sge, .num_sge = 1, .opcode = IBV_WR_SEND, .send_flags = IBV_SEND_SIGNALED};
    struct ibv_send_wr *bad = nullptr;
    int err = ibv_post_send(r->id->qp, &wr, &bad);
    if (err)
        fprintf(stderr, "ibv_post_send: %s\n", strerror(err));
    return err == 0;
}

static double now_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1e6 + (double)ts.tv_nsec / 1e3;
}

// 忙轮询等 SEND / RECV 各若干个完成
static bool wait_completions(cm_res *r, bool need_send, bool need_recv) {
    double deadline = now_us() + TIMEOUT_MS * 1000.0;
    while (need_send || need_recv) {
        struct ibv_wc wc;
        int n = ibv_poll_cq(r->cq, 1, &wc);
        if (n < 0) {
            fprintf(stderr, "ibv_poll_cq 失败\n");
            return false;
        }
        if (n == 0) {
            if (now_us() > deadline) {
                fprintf(stderr, "等待完成超时（%d ms）\n", TIMEOUT_MS);
                return false;
            }
            continue;
        }
        if (wc.status != IBV_WC_SUCCESS) {
            fprintf(stderr, "wc error: %s (status=%d) wr_id=%llu vendor_err=0x%x\n", ibv_wc_status_str(wc.status),
                    wc.status, (unsigned long long)wc.wr_id, wc.vendor_err);
            return false;
        }
        if (wc.wr_id == WRID_SEND)
            need_send = false;
        else if (wc.wr_id == WRID_RECV)
            need_recv = false;
    }
    return true;
}

static bool pingpong(cm_res *r, bool is_client, int iters) {
    double t0 = now_us();
    for (int i = 0; i < iters; i++) {
        uint32_t seq = (uint32_t)i, got;
        if (is_client) {
            memcpy(r->buf + MSG_SIZE, &seq, sizeof seq);
            if (!post_send(r) || !wait_completions(r, true, true))
                return false;
            memcpy(&got, r->buf, sizeof got);
            if (got != seq) {
                fprintf(stderr, "第 %d 轮收到序号 %u\n", i, got);
                return false;
            }
            if (!post_recv(r))
                return false;
        } else {
            if (!wait_completions(r, false, true))
                return false;
            memcpy(&got, r->buf, sizeof got);
            if (got != seq) {
                fprintf(stderr, "第 %d 轮收到序号 %u\n", i, got);
                return false;
            }
            if (!post_recv(r))
                return false;
            memcpy(r->buf + MSG_SIZE, r->buf, MSG_SIZE);
            if (!post_send(r) || !wait_completions(r, true, false))
                return false;
        }
    }
    double us = now_us() - t0;
    if (is_client)
        printf("iters=%d size=%d avg_rtt_us=%.2f avg_lat_us=%.2f\n", iters, MSG_SIZE, us / iters, us / iters / 2);
    else
        printf("server done iters=%d\n", iters);
    return true;
}

// ---------- 事件循环 ----------

// 带超时地取一个 CM 事件（通道 fd 设成了非阻塞）
static struct rdma_cm_event *next_event(struct rdma_event_channel *ch) {
    double deadline = now_us() + TIMEOUT_MS * 1000.0;
    for (;;) {
        struct rdma_cm_event *ev = nullptr;
        if (rdma_get_cm_event(ch, &ev) == 0)
            return ev;
        if (errno != EAGAIN && errno != EWOULDBLOCK && errno != EINTR) {
            fprintf(stderr, "rdma_get_cm_event: %s\n", strerror(errno));
            return nullptr;
        }
        double left_ms = (deadline - now_us()) / 1000.0;
        if (left_ms <= 0) {
            fprintf(stderr, "等待 CM 事件超时（%d ms）\n", TIMEOUT_MS);
            return nullptr;
        }
        struct pollfd pfd = {.fd = ch->fd, .events = POLLIN};
        if (poll(&pfd, 1, (int)left_ms + 1) < 0 && errno != EINTR) {
            perror("poll(cm channel)");
            return nullptr;
        }
    }
}

static struct rdma_event_channel *make_channel(void) {
    struct rdma_event_channel *ch = rdma_create_event_channel();
    if (ch == nullptr) {
        // 没有 rdma_cm 内核模块 / 没有设备时 errno 通常是 ENODEV 或 ENOENT
        fprintf(stderr, "rdma_create_event_channel: %s\n", strerror(errno));
        return nullptr;
    }
    int fl = fcntl(ch->fd, F_GETFL);
    if (fl < 0 || fcntl(ch->fd, F_SETFL, fl | O_NONBLOCK) < 0) {
        perror("fcntl(cm channel, O_NONBLOCK)");
        rdma_destroy_event_channel(ch);
        return nullptr;
    }
    return ch;
}

static void report_fail(const struct rdma_cm_event *ev) {
    // status：错误事件里是负的 errno；REJECTED 时是对端 CM 的拒绝原因码
    fprintf(stderr, "CM 事件 %s status=%d%s%s\n", rdma_event_str(ev->event), ev->status, ev->status < 0 ? " " : "",
            ev->status < 0 ? strerror(-ev->status) : "");
}

static bool run_client(struct rdma_event_channel *ch, const char *ip, const char *port, int iters) {
    struct addrinfo hints = {.ai_family = AF_INET, .ai_socktype = SOCK_STREAM, .ai_flags = AI_NUMERICHOST}, *ai;
    int gai = getaddrinfo(ip, port, &hints, &ai);
    if (gai != 0) {
        fprintf(stderr, "getaddrinfo(%s, %s): %s（需要数字 IPv4 地址）\n", ip, port, gai_strerror(gai));
        return false;
    }
    cm_res r = {};
    bool ok = false, done = false;
    if (rdma_create_id(ch, &r.id, nullptr, RDMA_PS_TCP) < 0) {
        fprintf(stderr, "rdma_create_id: %s\n", strerror(errno));
        freeaddrinfo(ai);
        return false;
    }
    if (rdma_resolve_addr(r.id, nullptr, ai->ai_addr, RESOLVE_MS) < 0) {
        fprintf(stderr, "rdma_resolve_addr(%s): %s\n", ip, strerror(errno));
        done = true;
    }
    freeaddrinfo(ai);

    while (!done) {
        struct rdma_cm_event *ev = next_event(ch);
        if (ev == nullptr)
            break;
        enum rdma_cm_event_type type = ev->event;
        enum step step = client_next_step(type);
        hello peer = {};
        bool have_hello = false;
        if (step == STEP_RUN) // 私有数据在 ack 之后失效：先拷贝
            have_hello = parse_hello(ev->param.conn.private_data, ev->param.conn.private_data_len, &peer);
        if (step == STEP_FAIL)
            report_fail(ev);
        if (rdma_ack_cm_event(ev) < 0)
            perror("rdma_ack_cm_event");

        switch (step) {
        case STEP_RESOLVE_ROUTE:
            // TODO: 地址解析完成后调用 rdma_resolve_route(r.id, RESOLVE_MS) 发起路由解析；
            //       失败（返回 -1）时打印 strerror(errno) 并结束循环（done = true）。
            //       成功后等待下一个事件 RDMA_CM_EVENT_ROUTE_RESOLVED
            break;
        case STEP_CONNECT: {
            if (!create_res(&r)) {
                done = true;
                break;
            }
            uint8_t priv[PRIV_LEN];
            pack_hello(MSG_SIZE, priv);
            struct rdma_conn_param cp = {
                .private_data = priv,
                .private_data_len = sizeof priv,
                .responder_resources = 1,
                .initiator_depth = 1,
                .retry_count = 7,
                .rnr_retry_count = 7,
            };
            if (rdma_connect(r.id, &cp) < 0) {
                fprintf(stderr, "rdma_connect: %s\n", strerror(errno));
                done = true;
            }
            break;
        }
        case STEP_RUN:
            if (!have_hello) {
                fprintf(stderr, "server 的私有数据无法解析\n");
                done = true;
                break;
            }
            printf("connected: server hello version=%u msg_size=%u\n", peer.version, peer.msg_size);
            ok = pingpong(&r, true, iters);
            if (rdma_disconnect(r.id) < 0) { // 两端随后都会收到 DISCONNECTED
                fprintf(stderr, "rdma_disconnect: %s\n", strerror(errno));
                ok = false;
                done = true;
            }
            break;
        case STEP_DONE:
            done = true;
            break;
        case STEP_FAIL:
            ok = false;
            done = true;
            break;
        default:
            fprintf(stderr, "忽略 CM 事件 %s\n", rdma_event_str(type));
            break;
        }
    }
    destroy_res(&r);
    if (rdma_destroy_id(r.id) < 0)
        perror("rdma_destroy_id");
    return ok;
}

static bool run_server(struct rdma_event_channel *ch, const char *port, int iters) {
    struct rdma_cm_id *listen_id = nullptr;
    if (rdma_create_id(ch, &listen_id, nullptr, RDMA_PS_TCP) < 0) {
        fprintf(stderr, "rdma_create_id: %s\n", strerror(errno));
        return false;
    }
    struct sockaddr_in addr = {.sin_family = AF_INET, .sin_port = htons((uint16_t)atoi(port))};
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    cm_res r = {};
    bool ok = false, done = false;
    if (rdma_bind_addr(listen_id, (struct sockaddr *)&addr) < 0) {
        fprintf(stderr, "rdma_bind_addr(0.0.0.0:%s): %s\n", port, strerror(errno));
        done = true;
    } else if (rdma_listen(listen_id, 1) < 0) {
        fprintf(stderr, "rdma_listen: %s\n", strerror(errno));
        done = true;
    } else {
        printf("listening on port %s\n", port);
    }

    while (!done) {
        struct rdma_cm_event *ev = next_event(ch);
        if (ev == nullptr)
            break;
        enum rdma_cm_event_type type = ev->event;
        enum step step = server_next_step(type);
        hello peer = {};
        bool have_hello = false;
        struct rdma_cm_id *conn_id = ev->id;
        if (step == STEP_ACCEPT)
            have_hello = parse_hello(ev->param.conn.private_data, ev->param.conn.private_data_len, &peer);
        if (step == STEP_FAIL)
            report_fail(ev);
        if (rdma_ack_cm_event(ev) < 0)
            perror("rdma_ack_cm_event");

        switch (step) {
        case STEP_ACCEPT: {
            if (r.id != nullptr) { // 只服务一个连接：拒绝并销毁多出来的 id（它归应用所有）
                if (rdma_reject(conn_id, nullptr, 0) < 0)
                    perror("rdma_reject");
                if (rdma_destroy_id(conn_id) < 0)
                    perror("rdma_destroy_id(rejected)");
                break;
            }
            r.id = conn_id;
            if (!have_hello) {
                fprintf(stderr, "client 的私有数据无法解析，拒绝连接\n");
                if (rdma_reject(conn_id, nullptr, 0) < 0)
                    perror("rdma_reject");
                done = true;
                break;
            }
            printf("connect request: client hello version=%u msg_size=%u\n", peer.version, peer.msg_size);
            if (!create_res(&r)) {
                done = true;
                break;
            }
            uint8_t priv[PRIV_LEN];
            pack_hello(MSG_SIZE, priv);
            struct rdma_conn_param cp = {
                .private_data = priv,
                .private_data_len = sizeof priv,
                .responder_resources = 1,
                .initiator_depth = 1,
                .rnr_retry_count = 7,
            };
            if (rdma_accept(conn_id, &cp) < 0) {
                fprintf(stderr, "rdma_accept: %s\n", strerror(errno));
                done = true;
            }
            break;
        }
        case STEP_RUN:
            ok = pingpong(&r, false, iters);
            if (!ok)
                done = true;
            break;
        case STEP_DONE:
            done = true;
            break;
        case STEP_FAIL:
            ok = false;
            done = true;
            break;
        default:
            fprintf(stderr, "忽略 CM 事件 %s\n", rdma_event_str(type));
            break;
        }
    }
    destroy_res(&r);
    if (r.id && rdma_destroy_id(r.id) < 0)
        perror("rdma_destroy_id(conn)");
    if (rdma_destroy_id(listen_id) < 0)
        perror("rdma_destroy_id(listen)");
    return ok;
}

// 在做任何 CM 操作之前先确认有 verbs 设备，给出统一的提示
static bool have_rdma_device(void) {
    int num = 0;
    errno = 0;
    struct ibv_device **list = ibv_get_device_list(&num);
    if (list == nullptr || num == 0) {
        fprintf(stderr, "no RDMA device: load rdma_rxe or use ConnectX（ibv_get_device_list: %s）\n",
                list == nullptr ? strerror(errno) : "0 devices");
        if (list)
            ibv_free_device_list(list);
        return false;
    }
    ibv_free_device_list(list);
    return true;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 2 && strcmp(argv[1], "--selftest") == 0)
        return selftest();
    bool is_client = argc >= 4 && strcmp(argv[1], "client") == 0;
    bool is_server = argc >= 3 && strcmp(argv[1], "server") == 0;
    if (!is_client && !is_server) {
        fprintf(stderr, "usage: %s server PORT [--iters N]\n       %s client IP PORT [--iters N]\n       %s --selftest\n",
                argv[0], argv[0], argv[0]);
        return 2;
    }
    int iters = 500;
    int first_opt = is_client ? 4 : 3;
    if (argc == first_opt + 2 && strcmp(argv[first_opt], "--iters") == 0)
        iters = atoi(argv[first_opt + 1]);
    else if (argc != first_opt) {
        fprintf(stderr, "unknown option %s\n", argv[first_opt]);
        return 2;
    }
    int port = atoi(is_client ? argv[3] : argv[2]);
    if (iters <= 0 || port <= 0 || port > 65535) {
        fprintf(stderr, "--iters 应 > 0，PORT 应在 1..65535\n");
        return 2;
    }
    if (!have_rdma_device())
        return 2;
    struct rdma_event_channel *ch = make_channel();
    if (ch == nullptr)
        return 2;
    bool ok = is_client ? run_client(ch, argv[2], argv[3], iters) : run_server(ch, argv[2], iters);
    rdma_destroy_event_channel(ch);
    return ok ? 0 : 1;
}
