# 10_ebpf_xdp — hand-off notes

Four exercises, each one `.c` file holding the BPF program (`#ifdef __BPF__`, built by clang into
`bin/<name>.bpf.o`) and a libbpf loader (gcc, ASan+UBSan). All need root.

| exercise | hook | lesson | validated here |
|---|---|---|---|
| bpf1_xdp_count | XDP (generic on veth) | data_end bounds checks, PERCPU_ARRAY summation | yes (netns/veth) |
| bpf2_xdp_firewall | XDP | HASH map from argv, XDP_DROP, `bpf_ntohs` | yes (netns/veth) |
| bpf3_tcp_state_trace | tracepoint sock/inet_sock_set_state | hand-written tp ctx, ringbuf, `.rodata` config | yes (loopback) |
| bpf4_tc_egress_stats | tc clsact egress (`SEC("tc")`) | `__sk_buff`, TC_ACT_*, bpf_tc_hook_create/attach | yes (netns/veth) |

Validation box: kernel 6.18, libbpf 1.3.0, clang 18, GCC 13, 4 CPUs, generic XDP only (veth).
Solutions pass 3x in a row and 3 parallel runs; starters fail for the lesson's reason.

## Tests that SKIP on the validation box (need the ConnectX machine)

Both need `NETLINGS_IFACE=<mlx5 netdev>` and `NETLINGS_PEER_IP=<peer on that link>`, run as root.

- [ ] `tests/10_ebpf_xdp/test_bpf1_xdp_count.py::test_real_nic_native_mode`
  - Runs the loader on `$NETLINGS_IFACE` with `NETLINGS_XDP_MODE=drv` (XDP_FLAGS_DRV_MODE; override
    with `NETLINGS_XDP_MODE=skb|auto`), pings the peer 20 times, expects `ICMP packets >= 20` and no
    `xdp` left in `ip link show`.
  - Pass: `ready`, then `attached xdp_count to <if> (native/drv mode)`, ICMP count >= 20.
  - Risks: native attach fails with `EOPNOTSUPP`/`EINVAL` if MTU is above the mlx5 XDP limit
    (non-multi-buffer programs need MTU <= ~3498 on mlx5; jumbo 9000 → set MTU 1500 or build the
    program as `SEC("xdp.frags")` and use `bpf_xdp_load_bytes`); attaching XDP resets mlx5 channels
    (link flaps for ~1 s; ping uses `-W 2`, should be fine). If another XDP prog is already attached
    (e.g. by a previous crashed run using netlink attach) → `EBUSY`; our loader uses bpf_link, which
    auto-detaches when the process dies. With LRO/HW-GRO on, mlx5 refuses XDP: `ethtool -K <if> lro off`.
- [ ] `tests/10_ebpf_xdp/test_bpf4_tc_egress_stats.py::test_real_nic_egress`
  - Attaches to `$NETLINGS_IFACE` egress, sends 200 × 1000-byte UDP datagrams to the peer (port 5555,
    nobody needs to listen), expects the peer IP in `top talkers` with >= 200 packets and no filter left.
  - Risks: if the NIC already has a `clsact` qdisc (e.g. Cilium/other tooling), the loader reuses it
    (`-EEXIST`) and does not delete it — correct, but check that handle 1 / prio 1 does not collide
    with an existing filter (`tc filter show dev $IF egress`). TSO/GSO: large TCP sends are counted
    per GSO skb (skb->len can be 64 KB), so per-packet counts are lower than wire packets; UDP 1000 B is fine.

## Manual checks worth doing on the real machine

- bpf2 on the real NIC (not automated — needs a UDP server on this host and a sender on the peer):
  `sudo NETLINGS_XDP_MODE=drv bin/bpf2_xdp_firewall $IF 9000` here; on the peer
  `for i in $(seq 100); do echo x | nc -u -w0 <this-ip> 9000; done`; `nc -ul 9000` here must see nothing,
  Ctrl-C the loader → `port 9000 dropped 100`.
- Mpps measurement (extension, not a probe): `xdp-bench drop $IF` (xdp-tools) on this host, and on the
  peer `pktgen` (`samples/pktgen/pktgen_sample03_burst_single_flow.sh -i <peer-if> -d <this-ip> -m <this-mac> -t 4`)
  or `trex`. Compare generic vs native: `NETLINGS_XDP_MODE=skb` vs `drv` with bpf1 while pktgen blasts;
  native on ConnectX-5/6 at 25GbE should drop line rate (~37 Mpps at 64 B) with a few cores.
- AF_XDP (extension idea): `xdp-tools`' `xdpsock`/`xdp-trafficgen`, zero-copy on mlx5 needs
  `XDP_ZEROCOPY` + dedicated channels (`ethtool -L $IF combined N`).
- Inspection: `bpftool prog show`, `bpftool prog dump xlated name xdp_count`, `bpftool map dump name stats`
  (per-CPU values), `bpftool net show dev $IF`, `bpftool link show`, `bpftool prog tracelog` for
  `bpf_printk`. (bpftool is not installed on the validation box: `apt install linux-tools-$(uname -r)`.)

## Assumptions / known risks in the code

- `SL_BPF_OBJ` is an absolute path to the build tree; moving the build dir requires a rebuild.
- bpf1/bpf2 attach with `bpf_link_create(prog_fd, ifindex, BPF_XDP, flags)` (flags = SKB/DRV mode) so
  XDP is detached even on SIGKILL. `bpf_program__attach_xdp` cannot pass mode flags in libbpf 1.3.
- bpf1 probe relies on each veth packet being processed on the sender's CPU (true for veth without RPS);
  it pins the sender to each CPU in turn so the "sum only CPU 0" bug is detected. On a 1-CPU box that bug
  is undetectable (probe still passes the solution).
- bpf1 exact byte counts assume the ICMP/UDP frames are not padded (veth doesn't pad) and IPv6 off
  in the netns (no stray v4 traffic besides ARP, which is counted as OTHER and not asserted).
- bpf3 hand-writes the tracepoint layout (offsets asserted with `_Static_assert` against the 6.x format:
  oldstate@16, sport@24, saddr@32, daddr_v6@56). Stable since 4.16, but if a future kernel changes the
  format the BPF compile still succeeds and events are garbage → compare against
  `/sys/kernel/tracing/events/sock/inet_sock_set_state/format`, or switch to vmlinux.h + CO-RE.
  `target_port` is set by patching `.rodata` at offset 0 via `bpf_map__initial_value` — it must remain
  the only `.rodata` variable (string literals go to `.rodata.str1.1`, fine).
- bpf3 probe mounts tracefs if `/sys/kernel/tracing/events` is missing; skips if the mount fails.
  Client-side final transition is `FIN_WAIT2 -> CLOSE` (TIME_WAIT is a separate timewait sock);
  the probe accepts `FIN_WAIT1 -> FIN_WAIT2|CLOSING` and any `-> CLOSE` for the client.
- bpf4 uses the legacy netlink tc API (`bpf_tc_*`); a SIGKILLed loader leaves the filter/qdisc
  (tests clean up via netns deletion). tcx (`bpf_program__attach_tcx`, kernel 6.6+) would give link semantics.

## Kernel lockdown / Secure Boot pitfalls

- With Secure Boot, many distro kernels enable lockdown=integrity; BPF still loads, but
  `bpf_probe_read_kernel` of arbitrary memory and kprobe writes are restricted; under
  lockdown=confidentiality, tracing helpers that read kernel memory are denied (EPERM) — bpf3 only
  reads the tracepoint context, so it should still work. Check `cat /sys/kernel/security/lockdown`.
- `kernel.unprivileged_bpf_disabled` doesn't matter (we run as root) but `sudo` must keep
  `CAP_SYS_ADMIN`/`CAP_BPF`/`CAP_NET_ADMIN`/`CAP_PERFMON`; run via `sudo -E` so the build dir env is kept.
- `ulimit -l` (memlock): libbpf 1.x uses memcg accounting on 5.11+; on older kernels raise RLIMIT_MEMLOCK.
