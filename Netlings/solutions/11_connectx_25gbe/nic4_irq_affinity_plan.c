// EXERCISE: nic4_irq_affinity_plan — 找出网卡队列中断，按 NUMA 本地 CPU 生成绑核方案
// TOPIC: /sys/class/net/IFACE/device/{msi_irqs,numa_node,local_cpulist} / /proc/interrupts / /proc/irq/N/smp_affinity_list
// DIFFICULTY: ★★★☆☆
// BOOK: Documentation/core-api/irq/irq-affinity.rst；Documentation/networking/scaling.rst；man 5 proc（interrupts）
//
// 说明：
//   用法：nic4_irq_affinity_plan IFACE [--apply]    打印方案（只读）；--apply 真正写入（需要 root）
//         nic4_irq_affinity_plan --selftest         用合成输入测试纯函数（不需要网卡）
//   步骤：
//   1. /sys/class/net/IFACE/device/msi_irqs/ 目录下每个文件名就是这块 PCI 设备的一个 MSI-X 中断号。
//      虚拟网卡（veth/lo/bridge）没有 device/ 或没有 msi_irqs → 报错退出（exit 2）
//   2. 在 /proc/interrupts 里找到这些中断的名字。mlx5 的完成向量叫
//      "mlx5_comp<N>@pci:0000:41:00.0"，N 就是队列（通道）号；mlx5_async / mlx5_ctrl 等不是数据队列。
//      Intel 网卡是 "<iface>-TxRx-<N>"。认不出队列号的中断不进方案
//   3. numa_node + local_cpulist：网卡所在 NUMA 节点的 CPU（例如 "0-15,32-47"）
//   4. 方案：按队列号排序，队列 i → local_cpus[i % n]；同时显示当前的 /proc/irq/N/smp_affinity_list
//   输出：
//     iface=IFACE numa_node=K local_cpus=0-15 nlocal=16
//     irq=150 name=mlx5_comp0@pci:0000:41:00.0 queue=0 current=0-63 plan=0
//     ...
//     plan_irqs=N
//     echo 0 > /proc/irq/150/smp_affinity_list      （可以直接复制执行的命令）
//
//   为什么：每个 RX 队列的中断触发哪个 CPU，那个 CPU 就跑这个队列的 NAPI 轮询和协议栈。
//   队列中断落到远端 NUMA 节点 → 每个包的 DMA 缓冲区都要跨 socket 访问；多个队列挤在一个 CPU 上 →
//   这个 CPU 的 softirq 打满（top 里 si 100%）而其他核闲着。25G 线速 ≈ 2 Mpps（1500B），
//   单核扛不住，必须"一个队列一个本地核"。irqbalance 会定期改写 smp_affinity，
//   手工绑核前要 systemctl stop irqbalance（或用 IRQBALANCE_BANNED_CPULIST 把这些核排除）。
//   DPDK/SPDK、Seastar、ScyllaDB 的部署脚本（perftune.py）做的就是这件事；mlx5 自带的
//   set_irq_affinity_cpulist.sh 也是。
//
//   环境变量 NETLINGS_NIC4_ROOT=DIR：把 DIR 当作文件系统根（读 DIR/sys/...、DIR/proc/...），
//   测试用它在没有真网卡的机器上跑通主流程（包括 --apply 写文件）。
//
//   测试：--selftest 用合成的 /proc/interrupts 文本和 cpulist 验证解析与方案；veth 上应报错退出。
//   真实机器（NETLINGS_IFACE=ConnectX）：方案要覆盖该 PCI 设备的所有 mlx5_comp 中断，且都绑到本地 CPU。

#include <ctype.h>
#include <dirent.h>
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "sl.h"

enum { MAX_CPUS = 4096, MAX_IRQS = 1024, NAME_LEN = 96, LIST_LEN = 512 };

static const char *g_root = ""; // NETLINGS_NIC4_ROOT：测试用的假根目录

typedef struct {
    int irq;
    int queue; // -1 = 不是数据队列
    char name[NAME_LEN];
} irq_entry;

// ---------- 纯函数（--selftest 覆盖） ----------

// 解析 "0-3,8,10-11\n" 这样的 cpulist；返回 CPU 个数，格式错误或超过 cap 返回 -1。空串 → 0
static int parse_cpulist(const char *s, int *out, int cap) {
    int n = 0;
    const char *p = s;
    while (*p && isspace((unsigned char)*p))
        p++;
    while (*p && *p != '\n') {
        char *end;
        errno = 0;
        long lo = strtol(p, &end, 10);
        if (end == p || errno || lo < 0 || lo >= MAX_CPUS)
            return -1;
        long hi = lo;
        p = end;
        if (*p == '-') {
            p++;
            hi = strtol(p, &end, 10);
            if (end == p || errno || hi < lo || hi >= MAX_CPUS)
                return -1;
            p = end;
        }
        for (long c = lo; c <= hi; c++) {
            if (n >= cap)
                return -1;
            out[n++] = (int)c;
        }
        if (*p == ',')
            p++;
        else if (*p && *p != '\n' && !isspace((unsigned char)*p))
            return -1;
        while (*p == ' ' || *p == '\t')
            p++;
    }
    return n;
}

// 把 CPU 数组（升序）压缩回 "0-3,8,10-11"
static void format_cpulist(const int *cpus, int n, char *buf, size_t len) {
    size_t off = 0;
    buf[0] = '\0';
    for (int i = 0; i < n;) {
        int j = i;
        while (j + 1 < n && cpus[j + 1] == cpus[j] + 1)
            j++;
        int w = j > i ? snprintf(buf + off, len - off, "%s%d-%d", off ? "," : "", cpus[i], cpus[j])
                      : snprintf(buf + off, len - off, "%s%d", off ? "," : "", cpus[i]);
        if (w < 0 || (size_t)w >= len - off)
            return;
        off += (size_t)w;
        i = j + 1;
    }
}

// 从中断名里取队列号："mlx5_comp7@pci:..." → 7，"eth0-TxRx-3" → 3；其他 → -1
static int queue_index_from_name(const char *name) {
    static const char *const markers[] = {"mlx5_comp", "-TxRx-"};
    for (size_t i = 0; i < sizeof markers / sizeof markers[0]; i++) {
        const char *m = strstr(name, markers[i]);
        if (m == nullptr)
            continue;
        const char *d = m + strlen(markers[i]);
        if (!isdigit((unsigned char)*d))
            return -1;
        long q = strtol(d, nullptr, 10);
        return q > 100000 ? -1 : (int)q;
    }
    return -1;
}

// 解析 /proc/interrupts 的一行：" 150:   0   5 ...  IR-PCI-MSIX-0000:41:00.0  1-edge  mlx5_comp0@pci:..."
// 中断号取行首数字，名字取最后一个空白分隔的字段。非数字行（CPU0 表头、NMI、LOC…）返回 false
static bool parse_interrupt_line(const char *line, int *irq, char *name, size_t len) {
    const char *p = line;
    while (*p == ' ')
        p++;
    if (!isdigit((unsigned char)*p))
        return false;
    char *end;
    long v = strtol(p, &end, 10);
    if (*end != ':' || v < 0 || v > INT32_MAX)
        return false;
    const char *e = line + strlen(line);
    while (e > end && isspace((unsigned char)e[-1]))
        e--;
    const char *b = e;
    while (b > end + 1 && !isspace((unsigned char)b[-1]))
        b--;
    if (b >= e)
        return false;
    snprintf(name, len, "%.*s", (int)(e - b), b);
    *irq = (int)v;
    return true;
}

static bool contains(const int *a, int n, int v) {
    for (int i = 0; i < n; i++)
        if (a[i] == v)
            return true;
    return false;
}

static int cmp_entry(const void *x, const void *y) {
    const irq_entry *a = x, *b = y;
    if (a->queue != b->queue)
        return a->queue < b->queue ? -1 : 1;
    return (a->irq > b->irq) - (a->irq < b->irq);
}

// 从 /proc/interrupts 流里挑出属于 msi[] 的队列中断，按队列号排序；返回个数
static int collect_queue_irqs(FILE *f, const int *msi, int nmsi, irq_entry *out, int cap) {
    // getline：几百个 CPU 的机器上一行可能有好几 KB，固定大小的 fgets 会把行截断
    char *line = nullptr;
    size_t cap_line = 0;
    int n = 0;
    while (getline(&line, &cap_line, f) >= 0) {
        irq_entry e = {};
        if (!parse_interrupt_line(line, &e.irq, e.name, sizeof e.name) || !contains(msi, nmsi, e.irq))
            continue;
        e.queue = queue_index_from_name(e.name);
        if (e.queue < 0 || n >= cap)
            continue;
        out[n++] = e;
    }
    free(line);
    qsort(out, (size_t)n, sizeof *out, cmp_entry);
    return n;
}

// 队列 i → local[i % nlocal]
static void build_plan(int nq, const int *local, int nlocal, int *plan) {
    for (int i = 0; i < nq; i++)
        plan[i] = local[i % nlocal];
}

static int selftest(void) {
    int cpus[64] = {};
    SL_CHECK_EQ(parse_cpulist("0-3,8,10-11\n", cpus, 64), 7);
    SL_CHECK_EQ(cpus[3], 3);
    SL_CHECK_EQ(cpus[4], 8);
    SL_CHECK_EQ(cpus[6], 11);
    SL_CHECK_EQ(parse_cpulist("5", cpus, 64), 1);
    SL_CHECK_EQ(cpus[0], 5);
    SL_CHECK_EQ(parse_cpulist("\n", cpus, 64), 0);
    SL_CHECK_EQ(parse_cpulist("3-1", cpus, 64), -1);
    SL_CHECK_EQ(parse_cpulist("0-99", cpus, 64), -1); // 超过 cap
    SL_CHECK_EQ(parse_cpulist("a", cpus, 64), -1);

    char buf[128];
    int list[] = {0, 1, 2, 3, 8, 10, 11};
    format_cpulist(list, 7, buf, sizeof buf);
    SL_CHECK(strcmp(buf, "0-3,8,10-11") == 0);

    SL_CHECK_EQ(queue_index_from_name("mlx5_comp7@pci:0000:41:00.0"), 7);
    SL_CHECK_EQ(queue_index_from_name("mlx5_comp12@pci:0000:41:00.1"), 12);
    SL_CHECK_EQ(queue_index_from_name("mlx5_async0@pci:0000:41:00.0"), -1);
    SL_CHECK_EQ(queue_index_from_name("i40e-eth0-TxRx-3"), 3);
    SL_CHECK_EQ(queue_index_from_name("virtio1-input.0"), -1);

    int irq = -1;
    char name[NAME_LEN];
    SL_CHECK(parse_interrupt_line(" 150:  0  5  0  0  IR-PCI-MSIX-0000:41:00.0  1-edge  mlx5_comp0@pci:0000:41:00.0\n",
                                  &irq, name, sizeof name));
    SL_CHECK_EQ(irq, 150);
    SL_CHECK(strcmp(name, "mlx5_comp0@pci:0000:41:00.0") == 0);
    SL_CHECK(!parse_interrupt_line("           CPU0       CPU1\n", &irq, name, sizeof name));
    SL_CHECK(!parse_interrupt_line("NMI:  0  0  Non-maskable interrupts\n", &irq, name, sizeof name));

    // 合成的 /proc/interrupts：两块卡的中断混在一起，只取 msi[] 里的、有队列号的，按队列号排序
    static const char fake[] =
        "            CPU0       CPU1       CPU2       CPU3\n"
        "  24:          0          0          0          0  IR-PCI-MSIX-0000:41:00.0    0-edge      mlx5_async0@pci:0000:41:00.0\n"
        "  27:          9          0          0          0  IR-PCI-MSIX-0000:41:00.0    3-edge      mlx5_comp2@pci:0000:41:00.0\n"
        "  25:          1          0          0          0  IR-PCI-MSIX-0000:41:00.0    1-edge      mlx5_comp0@pci:0000:41:00.0\n"
        "  26:          0          7          0          0  IR-PCI-MSIX-0000:41:00.0    2-edge      mlx5_comp1@pci:0000:41:00.0\n"
        "  40:          0          0          0          3  IR-PCI-MSIX-0000:41:00.1    1-edge      mlx5_comp0@pci:0000:41:00.1\n"
        " NMI:          0          0          0          0   Non-maskable interrupts\n";
    int msi[] = {24, 25, 26, 27};
    FILE *f = fmemopen((void *)fake, sizeof fake - 1, "r");
    SL_CHECK(f != nullptr);
    if (f) {
        irq_entry e[8];
        int n = collect_queue_irqs(f, msi, 4, e, 8);
        fclose(f);
        SL_CHECK_EQ(n, 3);
        if (n == 3) {
            SL_CHECK_EQ(e[0].irq, 25);
            SL_CHECK_EQ(e[1].irq, 26);
            SL_CHECK_EQ(e[2].irq, 27);
            SL_CHECK_EQ(e[2].queue, 2);
        }
    }

    int local[] = {2, 3, 6};
    int plan[8];
    build_plan(8, local, 3, plan);
    SL_CHECK_EQ(plan[0], 2);
    SL_CHECK_EQ(plan[2], 6);
    SL_CHECK_EQ(plan[3], 2);
    SL_CHECK_EQ(plan[7], 3);
    return sl_report();
}

// ---------- 读 sysfs / procfs ----------

// 读一个小文本文件的第一行到 buf；失败返回 false（errno 保留）
static bool read_line(const char *path, char *buf, size_t len) {
    FILE *f = fopen(path, "r");
    if (f == nullptr)
        return false;
    bool ok = fgets(buf, (int)len, f) != nullptr;
    int saved = errno;
    fclose(f);
    if (!ok) {
        errno = saved ? saved : EIO;
        return false;
    }
    buf[strcspn(buf, "\n")] = '\0';
    return true;
}

// 读 msi_irqs 目录；返回中断个数，目录不存在返回 -1
static int read_msi_irqs(const char *iface, int *out, int cap) {
    char path[512];
    snprintf(path, sizeof path, "%s/sys/class/net/%s/device/msi_irqs", g_root, iface);
    DIR *d = opendir(path);
    if (d == nullptr)
        return -1;
    int n = 0;
    struct dirent *de;
    while ((de = readdir(d)) != nullptr) {
        char *end;
        long v = strtol(de->d_name, &end, 10);
        if (end == de->d_name || *end != '\0' || v < 0 || v > INT32_MAX)
            continue; // "." ".."
        if (n < cap)
            out[n++] = (int)v;
    }
    closedir(d);
    return n;
}

static bool apply_one(int irq, int cpu) {
    char path[512];
    snprintf(path, sizeof path, "%s/proc/irq/%d/smp_affinity_list", g_root, irq);
    FILE *f = fopen(path, "w");
    if (f == nullptr) {
        fprintf(stderr, "open %s: %s\n", path, strerror(errno));
        return false;
    }
    // 写入错误（例如内核托管的中断返回 EIO）在 fclose 刷新缓冲时才出现
    bool ok = fprintf(f, "%d\n", cpu) > 0;
    if (fclose(f) != 0)
        ok = false;
    if (!ok)
        fprintf(stderr, "write %s: %s（managed IRQ 不允许改亲和性时是 EIO）\n", path, strerror(errno));
    return ok;
}

int main(int argc, char **argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc == 2 && strcmp(argv[1], "--selftest") == 0)
        return selftest();
    bool apply = argc == 3 && strcmp(argv[2], "--apply") == 0;
    if (argc != 2 && !apply) {
        fprintf(stderr, "usage: %s IFACE [--apply] | --selftest\n", argv[0]);
        return 2;
    }
    const char *iface = argv[1];
    if (strchr(iface, '/') || strlen(iface) > 15) {
        fprintf(stderr, "非法网卡名 %s\n", iface);
        return 2;
    }

    const char *root = getenv("NETLINGS_NIC4_ROOT");
    if (root != nullptr && strlen(root) < 256)
        g_root = root;
    char path[512];
    snprintf(path, sizeof path, "%s/sys/class/net/%s", g_root, iface);
    if (access(path, F_OK) < 0) {
        fprintf(stderr, "%s: %s\n", path, strerror(errno));
        return 1;
    }
    static int msi[MAX_IRQS];
    int nmsi = read_msi_irqs(iface, msi, MAX_IRQS);
    if (nmsi <= 0) {
        fprintf(stderr, "%s 没有 PCI MSI-X 中断（/sys/class/net/%s/device/msi_irqs 不存在或为空）："
                        "虚拟网卡（veth/lo/bridge）没有硬件队列中断，请用真实网卡（NETLINGS_IFACE）\n",
                iface, iface);
        return 2;
    }

    char buf[LIST_LEN];
    int numa = -1;
    snprintf(path, sizeof path, "%s/sys/class/net/%s/device/numa_node", g_root, iface);
    if (read_line(path, buf, sizeof buf))
        numa = atoi(buf);
    static int local[MAX_CPUS];
    snprintf(path, sizeof path, "%s/sys/class/net/%s/device/local_cpulist", g_root, iface);
    if (!read_line(path, buf, sizeof buf)) {
        fprintf(stderr, "读 %s 失败（%s），退回到所有在线 CPU\n", path, strerror(errno));
        snprintf(path, sizeof path, "%s/sys/devices/system/cpu/online", g_root);
        if (!read_line(path, buf, sizeof buf)) {
            perror(path);
            return 1;
        }
    }
    int nlocal = parse_cpulist(buf, local, MAX_CPUS);
    if (nlocal <= 0) {
        fprintf(stderr, "无法解析 cpulist %s\n", buf);
        return 1;
    }

    snprintf(path, sizeof path, "%s/proc/interrupts", g_root);
    FILE *f = fopen(path, "r");
    if (f == nullptr)
        sl_die(path);
    static irq_entry ents[MAX_IRQS];
    int nq = collect_queue_irqs(f, msi, nmsi, ents, MAX_IRQS);
    fclose(f);
    if (nq == 0) {
        fprintf(stderr, "%s 的 %d 个 MSI-X 中断里没有认出队列中断（名字不含 mlx5_comp<N> / -TxRx-<N>）\n", iface,
                nmsi);
        return 1;
    }

    static int plan[MAX_IRQS];
    build_plan(nq, local, nlocal, plan);

    char cl[LIST_LEN];
    format_cpulist(local, nlocal, cl, sizeof cl);
    printf("iface=%s numa_node=%d local_cpus=%s nlocal=%d msi_irqs=%d\n", iface, numa, cl, nlocal, nmsi);
    for (int i = 0; i < nq; i++) {
        char cur[LIST_LEN] = "?";
        snprintf(path, sizeof path, "%s/proc/irq/%d/smp_affinity_list", g_root, ents[i].irq);
        if (!read_line(path, cur, sizeof cur))
            snprintf(cur, sizeof cur, "?(%s)", strerror(errno));
        printf("irq=%d name=%s queue=%d current=%s plan=%d\n", ents[i].irq, ents[i].name, ents[i].queue, cur,
               plan[i]);
    }
    printf("plan_irqs=%d\n", nq);
    if (nq > nlocal)
        printf("# 注意：%d 个队列 > %d 个本地 CPU，部分 CPU 会分到多个队列（考虑 ethtool -L %s combined %d）\n", nq,
               nlocal, iface, nlocal);
    printf("# 先停掉 irqbalance（systemctl stop irqbalance），再以 root 执行：\n");
    for (int i = 0; i < nq; i++)
        printf("echo %d > /proc/irq/%d/smp_affinity_list\n", plan[i], ents[i].irq);

    if (!apply)
        return 0;
    if (geteuid() != 0 && g_root[0] == '\0') {
        fprintf(stderr, "--apply 需要 root\n");
        return 1;
    }
    int failed = 0;
    for (int i = 0; i < nq; i++)
        failed += !apply_one(ents[i].irq, plan[i]);
    printf("applied=%d failed=%d\n", nq - failed, failed);
    return failed ? 1 : 0;
}
