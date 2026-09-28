# Netlings hardware hand-off — start here

You are Claude Code running on the learner's own machine: a Linux box with a **25GbE NVIDIA/Mellanox
ConnectX NIC (mlx5_core)** that supports **RDMA / RoCE v2**. Your job is to validate and fix the Netlings
chapters that could not be fully tested where they were written, **without weakening what they teach**.

Read `../../CLAUDE.md` (Netlings conventions) first, then this file, then the chapter file you are working on.

## 1. What was validated where

All 55 + 23 exercises were authored on a cloud VM: kernel 6.18, root with full capabilities, GCC 13,
Clang 18, CMake 3.28, liburing 2.5, libbpf 1.3, rdma-core 50. That box had **no IPv6, no netem/fq qdisc,
no real NIC, no RDMA device and no rdma_rxe**. On it, `python -m studylings.selfcheck Netlings` shows every
exercise healthy: each solution passes every test that could run, and each starter fails.

| Chapter | Ran on the VM | Still needs this machine | Details |
|---|---|---|---|
| N01–N07 sockets … pthread sync | everything except IPv6 cases | 4 IPv6 test cases (need `::1`) | — |
| N08 io_uring | everything | newer-kernel extras, benchmark | [08_io_uring.md](08_io_uring.md) |
| N09 netns / tc | everything except netem | 3 netem tests (`modprobe sch_netem`) | [09_netns_tc.md](09_netns_tc.md) |
| N10 eBPF / XDP | everything on veth (generic XDP) | native XDP + tc on the ConnectX | [10_ebpf_xdp.md](10_ebpf_xdp.md) |
| N11 25GbE ConnectX | veth/loopback/selftest paths | every `test_real_*` (ethtool, RSS, IRQs, 25G throughput) | [11_connectx_25gbe.md](11_connectx_25gbe.md) |
| N12 RDMA / RoCE | selftests + "no device" path only | **all verbs / rdma_cm traffic — never executed** | [12_rdma_roce.md](12_rdma_roce.md) |

N12's QP setup, WRITE/READ and rdma_cm code has only been compiled and unit-tested against synthetic
inputs, so expect to fix real bugs there. Start with N12 once the easier chapters are green.

## 2. Setup

```bash
# Ubuntu 24.04/26.04 packages (see .devcontainer/systems/Dockerfile for the full list)
sudo apt install build-essential clang cmake ninja-build pkg-config python3-venv strace ethtool iproute2 \
     iperf3 tcpdump liburing-dev libbpf-dev linux-tools-common bpftrace \
     rdma-core ibverbs-utils ibverbs-providers libibverbs-dev librdmacm-dev perftest

cd StudyLings
python3 -m venv .venv && . .venv/bin/activate && pip install -e .
sudo modprobe sch_netem sch_fq          # N09 netem tests
sudo mount -t tracefs tracefs /sys/kernel/tracing 2>/dev/null || true   # N10 bpf3

sudo -E Netlings/tools/hwcheck.sh       # read-only report; paste it into your notes
export NETLINGS_IFACE=<mlx5 netdev from the report>        # e.g. enp65s0f0np0
export NETLINGS_RDMA_DEV=<rdma dev from the report>        # e.g. mlx5_0
export NETLINGS_PEER_IP=<peer host on the 25G link>        # optional, two-host tests
# optional: NETLINGS_RDMA_GID_INDEX, NETLINGS_RDMA_IP, NETLINGS_PEER_PORT, NETLINGS_XDP_MODE=drv|skb|auto
```

Most N09+ tests need root. Run them with the venv's interpreter and your env vars:

```bash
sudo -E env "PATH=$PATH" python -m studylings.selfcheck Netlings -j 2          # whole project
sudo -E env "PATH=$PATH" python -m studylings.selfcheck Netlings rdma2_rc_pingpong
cd Netlings && sudo -E env "PATH=$PATH" STUDYLINGS_PRESET=solutions python -m pytest -q -rs tests/12_rdma_roce
```

Without RDMA hardware support available, Soft-RoCE still exercises all of N12's code paths:
`sudo modprobe rdma_rxe && sudo rdma link add rxe0 type rxe netdev $NETLINGS_IFACE` and `NETLINGS_RDMA_DEV=rxe0`.

## 3. Work order

1. `sudo -E env "PATH=$PATH" python -m studylings.selfcheck Unixlings -j 4` and the same for `Netlings`.
   Nothing that was green on the VM should go red here. If something does, it is a portability bug
   (compiler version, kernel, distro): fix it first.
2. Re-run with the env vars set. The summary line counts SKIPs; use `pytest -rs` to see each skip reason.
   Goal: **0 skips** except tests that truly need a second host you don't have.
3. Work chapter by chapter in this order: N09 (netem), N10 (native XDP), N11, N12. Each chapter file has
   a checklist of commands, what "pass" looks like, the assumptions baked into the code, and likely fixes.
4. Record measured numbers (25G throughput, RDMA latency/bandwidth, XDP Mpps) in `results.md` next to this
   file. Include kernel, firmware (`ethtool -i`), MTU, CPU and NUMA placement, so they can be reproduced.

## 4. Rules for fixes

- **Solution and starter stay in sync.** Apply a fix to both files unless it touches the TODO/BUG spot
  itself. The starter must still fail its probe, for the lesson's reason.
- **Verify both directions** with `python -m studylings.selfcheck Netlings <name>`: the solution passes and
  the starter fails.
- **Do not turn a real assertion into a skip or a looser bound** just to go green. If the hardware really
  behaves differently, change the assumption, explain it in a code comment and in the chapter file, and keep
  the check meaningful. Example: a throughput floor should come from measured numbers, not be removed.
- **Missing capabilities still skip,** with a Chinese reason that says how to enable them.
- **Learner-facing text stays Chinese.** This includes the exercise header, 说明, hints and probe messages.
- **Commit per chapter** on the working branch, with a message that says what was wrong on real hardware.
  Update the chapter's hand-off file: tick what passed, and note what you changed.

## 5. Known high-risk spots (from the authors' reports)

- **N12:**
  - QP attribute masks, GID index auto-pick, and whether the path MTU is taken from the port's active MTU.
  - mlx5 loopback between server and client on the same port.
  - LeakSanitizer reports inside rdma-core: extend `tests/12_rdma_roce/lsan.supp`, and do not disable ASan.
- **N11:**
  - nic4 recognises queue IRQs only by the name `mlx5_comp<N>@pci:<bus>` (or `-TxRx-<N>`); newer drivers may differ.
  - nic3's loopback test assumes RPS is disabled on `lo`.
  - nic5's peer throughput is report-only and needs a receiver started on the peer.
- **N10:**
  - Native-mode XDP needs an MTU within the mlx5 XDP limit and LRO off. Attaching XDP flaps the link.
  - An existing clsact/tc filter on the NIC can collide with bpf4's handle and priority.
- **N09:**
  - The BBR-vs-CUBIC ratio under netem loss is the only test with some flake risk. The chapter file says how to tune it.
- **N08:**
  - uring1's `io_uring_enter` limit assumes page-cache reads complete inline. Keep `TMPDIR` on a local filesystem.
- **Everywhere:** Ubuntu's AppArmor restriction on unprivileged user namespaces makes N09 ns1/ns2 skip for non-root users.

## 6. When you are done

Once all of the following hold, the Netlings README can drop "needs hardware validation" for N11/N12:
- the self-check is green with the hardware env vars set;
- the remaining skips are listed with reasons;
- `results.md` holds the measured baselines;
- every chapter hand-off file is updated.
