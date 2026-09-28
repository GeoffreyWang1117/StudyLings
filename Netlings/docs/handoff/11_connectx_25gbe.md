# 11_connectx_25gbe — handoff for the real machine

Exercises: `nic1_ethtool_info`, `nic2_queues_rss`, `nic3_reuseport_cpu`, `nic4_irq_affinity_plan`,
`nic5_udp_gso_throughput`. All C, ioctl(SIOCETHTOOL) / sysfs / procfs / socket options, no extra libraries.

## What was validated on the authoring box (kernel 6.18, root, GCC 13, ASan+UBSan, no real NIC)

All 10 files (5 solutions + 5 starters) compile with zero warnings (`-Wall -Wextra -Wshadow`, also checked
with `gcc -O2` and clang 18). Solutions: 13 passed, 4 skipped; starters: every probe fails for the lesson's
reason. Stable over 3 sequential runs, 3 parallel runs and 3 runs with 4 busy-loop CPU hogs.

| Probe | Here | What it checks |
|---|---|---|
| nic1 `test_veth_fields` | PASS (netlab veth, MTU 1400) | driver=veth, speed == sysfs speed (10000), duplex full, mtu 1400, numa_node -1, nwords > 0 |
| nic1 `test_missing_iface` | PASS | ENODEV reported with strerror |
| nic1 `test_real_connectx` | **SKIP** (no NETLINGS_IFACE) | see checklist |
| nic2 `test_selftest` | PASS | indirection-table histogram, RXH_* formatting |
| nic2 `test_veth_channels` | PASS (`ethtool -L rx 2 tx 3` on veth) | channels == sysfs queue dirs; `rings/rxfh_tcp4/rss unsupported` (veth returns EOPNOTSUPP) |
| nic2 `test_real_connectx_rss` | **SKIP** | see checklist |
| nic3 `test_hash_spreads_over_all_workers` / `test_cbpf_steers_to_local_cpu` / `test_incoming_cpu_steers_to_local_cpu` | PASS (loopback, 4 CPUs) | every worker gets connections; with CBPF / SO_INCOMING_CPU a connection made from CPU k is accepted by the worker pinned to k (>= 90%, observed 100%) |
| nic4 `test_selftest` | PASS | cpulist parse/format, IRQ-name → queue, /proc/interrupts line parser (fmemopen), plan |
| nic4 `test_fake_machine_plan_and_apply` | PASS | full main path against a synthetic sysfs/procfs tree via `NETLINGS_NIC4_ROOT`, incl. `--apply` writes |
| nic4 `test_veth_has_no_irqs` | PASS | exit 2 + message about `device/msi_irqs` |
| nic4 `test_real_connectx_plan` | **SKIP** | see checklist |
| nic5 `test_plain_sendmmsg` / `test_gso` / `test_gso_gro` | PASS (loopback, 1.5 s each) | recv/sent ratio >= 20%, bad == 0, END count matches, batching visible, `gro_batches > 0` |
| nic5 `test_real_peer_throughput` | **SKIP** (no NETLINGS_PEER_IP) | report only |

Loopback reference numbers under ASan on the 4-vCPU box: plain sendmmsg ~4.5 Gbit/s (~390 kpps),
`--gso` ~14 Gbit/s, `--gso` + `--gro` ~50 Gbit/s (loopback never segments GSO skbs for a GRO socket).

## Environment

```bash
cd Netlings
cmake --preset dev && cmake --preset solutions
export NETLINGS_IFACE=enp65s0f0np0        # the ConnectX netdev (ip -br link)
export NETLINGS_PEER_IP=192.168.100.2     # optional, peer host on the same 25G link (nic5)
export NETLINGS_PEER_PORT=5201            # optional, default 5201
# netlab-based veth tests (nic1/nic2/nic4) need root; nic3/nic5 do not.
sudo -E STUDYLINGS_PRESET=solutions python -m pytest -q -rs -s tests/11_connectx_25gbe
sudo -E python -m studylings.selfcheck Netlings nic1_ethtool_info nic2_queues_rss nic3_reuseport_cpu nic4_irq_affinity_plan nic5_udp_gso_throughput
```

## Checklist (real machine)

- [ ] **nic1** `test_real_connectx`: pass = `driver=mlx5_core`, non-empty `firmware=` (e.g. `26.36.1010 (MT_0000000531)`),
      `speed_mbps` equal to `/sys/class/net/$IFACE/speed` (25000 with link up; test only *prints* a note if not 25000),
      `bus_info` equal to the basename of `readlink -f /sys/class/net/$IFACE/device`, `numa_node` equal to sysfs.
      Cross-check manually: `ethtool $IFACE`, `ethtool -i $IFACE`. Expect `port=da` (DAC) or `port=fibre` (optics).
- [ ] **nic2** `test_real_connectx_rss`: pass = `combined > 1`, `rss indir_size=N key_size=K` with N, K > 0
      (mlx5 default: 256 / 40, `hfunc=toeplitz`), `rss_queues_used == combined + rx`, `rss_out_of_range=0`,
      `rxfh_tcp4` contains `ip-src,ip-dst,l4-b-0-1,l4-b-2-3`. Cross-check with `ethtool -l/-g/-x $IFACE` and
      `ethtool -n $IFACE rx-flow-hash tcp4`.
- [ ] **nic3**: the automated probe is loopback-only and already passes here; re-run it once on the real box
      (needs >= 2 allowed CPUs; `test_incoming_cpu_*` skips on kernels < 6.1).
      Optional manual NIC experiment: the program binds 127.0.0.1 only (probe rule), so locally change
      `INADDR_LOOPBACK` to `INADDR_ANY`, pin the NIC IRQs with nic4, drive connections from the peer
      (e.g. `wrk -c 400`), then compare `cpu_mismatch` of `--mode hash` vs `--mode cbpf` in the SIGTERM summary.
- [ ] **nic4** `test_real_connectx_plan`: pass = number of `irq=` plan lines == number of
      `mlx5_comp<N>@pci:<bus>` lines in `/proc/interrupts`, each `plan=` CPU inside `device/local_cpulist`.
      Manual `--apply` check (root, changes the system!): `systemctl stop irqbalance`, run
      `sudo nic4_irq_affinity_plan $IFACE --apply` → `applied=N failed=0`, then
      `grep mlx5_comp /proc/interrupts` under load: each IRQ's counter grows only in its planned CPU column.
- [ ] **nic5** `test_real_peer_throughput` (report only): on the peer run
      `build/solutions/bin/nic5_udp_gso_throughput recv 5201 --gro`, then run the probe with `-s` to see output.
      The probe sends 5 s plain and 5 s `--gso`; it only asserts exit 0 and `refused=0`.
      Target numbers to record in the report (single flow, one core): plain sendmmsg ~5–10 Gbit/s, `--gso`
      >= 20 Gbit/s (line rate 25G ≈ 23.5 Gbit/s UDP payload at MTU 1500); receiver loss should drop sharply with `--gro`.
      Check `ethtool -k $IFACE | grep udp-segmentation` (mlx5: `tx-udp-segmentation: on`).

## Known assumptions / risks in the code

- nic1: relies on the GLINKSETTINGS handshake (first call returns `link_mode_masks_nwords = -N`). Any kernel since 4.9.
  Speed `SPEED_UNKNOWN` is printed as -1 (link down); the test compares with sysfs, which also reports -1.
- nic2: `nq = rx_count + combined_count` bounds the histogram; if RSS contexts or `ethtool -X ... equal M` with
  M < combined are configured, `rss_queues_used` will legitimately be < nq and the real-NIC test fails —
  reset with `ethtool -X $IFACE default`. Only the default RSS context (0) is read.
  `hfunc` bits are defined locally (`RSS_HASH_TOP=1<<0` etc.), the uapi header does not export `ETH_RSS_HASH_*`.
- nic3: the CBPF program is `ld cpu; jeq cpu_i → ret i; ...; ret n` (out-of-range → kernel falls back to hash).
  Group index == order of `listen()` calls, done sequentially in main. If `/sys/class/net/lo/queues/rx-0/rps_cpus`
  is non-zero on the real box, loopback softirq runs on other CPUs and the cbpf/incoming-cpu probes can fail —
  set it to 0 for the test.
- nic4: queue IRQs are recognised by name only (`mlx5_comp<N>` or `-TxRx-<N>`). If a newer mlx5 names IRQs
  differently (e.g. shared IRQ pools where the PF's `msi_irqs` holds IRQs named after another function), fix
  `queue_index_from_name()` in solution + starter and the regex in `test_real_connectx_plan`.
  `/proc/interrupts` is read with `getline` (long lines on many-core boxes are fine). Kernel-managed IRQs reject
  writes with EIO; `--apply` reports them and exits 1.
- nic5: segment size is fixed at 1472 B (MTU 1500). With MTU 9000 it still works (smaller than needed).
  `UDP_SEGMENT` needs checksum offload on the egress device; failure shows as `sendmmsg: Input/output error`
  with a hint. Loss tolerance on loopback is generous (>= 20% delivered) because the receiver shares CPUs.
  `SO_RCVBUFFORCE` (8 MiB) needs CAP_NET_ADMIN; without it the receiver silently falls back to `SO_RCVBUF`
  (capped by `net.core.rmem_max`) — raise `rmem_max` if non-root runs show heavy loss.

## Likely fixes if something fails there

- `bus_info` mismatch in nic1 real test on a VF/SF: compare against `ethtool -i` instead of the sysfs symlink.
- nic2 real test `rxfh_tcp4` order: the program prints fields in RXH bit order; adjust the regex, not the program.
- nic4 plan count mismatch: print `/proc/interrupts | grep $(basename $(readlink -f /sys/class/net/$IFACE/device))`
  and extend `queue_index_from_name()`.
