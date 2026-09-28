# 12_rdma_roce — handoff for the real machine

Exercises: `rdma1_devices`, `rdma2_rc_pingpong`, `rdma3_write_read`, `rdma4_cm_connect`
(link libibverbs + librdmacm via pkg-config).

## What was validated on the authoring box (no RDMA device, no rdma_rxe, rdma-core 50 headers)

**None of the verbs/CM data paths has ever run.** Everything device-related is compile-only
(0 warnings with the CMake flags, `gcc -O2 -Wall -Wextra -Wshadow -Wjump-misses-init`, and clang 18).
What did run:

| Probe | Here | What it checks |
|---|---|---|
| rdma1 `test_selftest` | PASS | sysfs GID text parse, IPv4-mapped check, inet_ntop, gid type strings, RoCE v2 pick |
| rdma1 `test_fake_sysfs_pick` | PASS | `--sysfs-root` scan of a synthetic `ports/1/{gids,gid_attrs/types,gid_attrs/ndevs}` tree → `roce_v2_gid_index=6`; no v2 IPv4 → `-1`, exit 1 |
| rdma1..4 `test_no_device_message` | PASS | `ibv_get_device_list` returns NULL/ENOSYS here → stderr `no RDMA device: load rdma_rxe or use ConnectX`, exit 2 |
| rdma2 `test_selftest` | PASS | INIT/RTR/RTS `ibv_qp_attr` + exact attr_mask, GRH fields, 27-byte OOB wire format |
| rdma3 `test_selftest` | PASS | MR/QP access flags, `fill_rdma_wr` (remote_addr, rkey, imm_data in network order), {addr,rkey,len} wire format |
| rdma4 `test_selftest` | PASS | CM event → next step (client/server), private data encode/parse (zero-padded to 56 B) |
| rdma1 `test_real_device`, rdma2 `test_pingpong_busy_poll`/`test_pingpong_events`, rdma3 `test_write_imm_read_bulk`/`test_remote_access_error_is_reported`, rdma4 `test_cm_pingpong` | **SKIP** | need a device |

On a machine WITH a device, `test_no_device_message` skips instead (by design).

## Environment

```bash
cd Netlings
cmake --preset dev && cmake --preset solutions
rdma link; ibv_devices; ibv_devinfo -d mlx5_0        # sanity: port state PORT_ACTIVE, link_layer Ethernet
export NETLINGS_RDMA_DEV=mlx5_0                      # or rxe0
# export NETLINGS_RDMA_GID_INDEX=3                   # optional; default = auto-pick RoCE v2 + IPv4-mapped GID
# export NETLINGS_RDMA_IP=192.168.100.1              # optional (rdma4); default = IPv4 inside that GID
STUDYLINGS_PRESET=solutions python -m pytest -q -rs -s tests/12_rdma_roce
python -m studylings.selfcheck Netlings rdma1_devices rdma2_rc_pingpong rdma3_write_read rdma4_cm_connect
```

Soft-RoCE alternative (no ConnectX): `sudo modprobe rdma_rxe && sudo rdma link add rxe0 type rxe netdev <iface>`
where `<iface>` has an IPv4 address (a veth with an address works; `lo` does not).
Also load `rdma_ucm` (rdma4) if `rdma_create_event_channel` fails with ENODEV.
Non-root: `ulimit -l` must allow ~1 MiB of pinned memory (rdma3 registers 2×64 KiB per side by default).

## Checklist (real machine) — all tests run server + client on the same host through the NIC loopback

- [ ] **rdma1** `test_real_device`: pass = `device=mlx5_0 ... ports=1`, first `port=` line `state=PORT_ACTIVE`,
      `link_layer=Ethernet`, and `roce_v2_gid_index=<i>` with `/sys/class/infiniband/mlx5_0/ports/1/gid_attrs/types/<i>`
      == `RoCE v2`. Cross-check with `show_gids` / `ibv_devinfo -v`. Expected for 25GbE: `speed=25.0Gbps width=1x`
      (active_speed 32 = EDR decode) — printed only, not asserted.
- [ ] **rdma2** `test_pingpong_busy_poll` (1000 iters) and `test_pingpong_events` (200 iters, completion channel):
      pass = client prints `iters=N size=64 avg_rtt_us=X avg_lat_us=Y`, server prints `server done iters=N`, both exit 0.
      Record latency: mlx5 local loopback typically ~2–4 µs RTT busy-poll (rxe: tens of µs); `--events` is higher.
      Reference tool for comparison: `ibv_rc_pingpong -d mlx5_0 -g <gid_idx>` (server) / `... 127.0.0.1` (client).
- [ ] **rdma3** `test_write_imm_read_bulk`: pass = client `write ok read ok bw_gbps=X size=65536 bulk=2000`,
      server `server verified imm=0x4e4c3132` + `server done`. Record bw (loopback on a 25G port should approach
      ~20+ Gbit/s; it is PCIe-bound, not wire-bound, when looped inside the NIC).
- [ ] **rdma3** `test_remote_access_error_is_reported`: server started with `--no-remote-access` (MR = LOCAL_WRITE only).
      pass = client exits != 0 and stderr matches `wc error: remote access error (status=10)`
      (test also accepts `remote invalid request error`), server exits != 0 (flushed RECV or 10 s timeout).
- [ ] **rdma4** `test_cm_pingpong`: pass = client `connected: server hello version=1 msg_size=64`, `iters=500 ...`;
      server `connect request: client hello version=1 ...` and `server done iters=500`, both exit 0.
      Needs the device's IPv4 (`rdma_ipv4` fixture: NETLINGS_RDMA_IP, else parsed from the RoCE v2 GID in sysfs).
- [ ] Starters: `python -m studylings.selfcheck ...` must show each exercise "exercise fails"
      (they already fail their selftests here; on hardware rdma2's starter would also fail at INIT→RTR with EINVAL,
      rdma3's with `remote access error`, rdma4's client with a CM-event timeout).

## Known assumptions / risks in the code (please verify first)

1. **LeakSanitizer and rdma-core**: providers (libmlx5, librxe) and libnl may keep allocations that LSan reports
   (exit code 23). `tests/12_rdma_roce/lsan.supp` suppresses `libibverbs.so`, `librdmacm.so`, `libmlx5.so`,
   `librxe`, `libnl-*`; tests pass it through `LSAN_OPTIONS`. If a leak report names another library frame,
   add it there. If a leak points into the exercise code, it is a real bug.
2. **Port 1 only**; device = NETLINGS_RDMA_DEV or the first device. Dual-port ConnectX shows up as two devices
   (mlx5_0, mlx5_1), each port 1 — fine.
3. **GID auto-pick** (rdma2/rdma3): first index whose `gid_attrs/types/<i>` is `RoCE v2` and whose `gids/<i>` starts with
   `0000:0000:0000:0000:0000:ffff:`. Both server and client use the same device+GID, so this is a loopback through the
   same port (mlx5 enables HW loopback when there are >= 2 user contexts; if the ping-pong times out with
   `retry exceeded`, check `ethtool --show-priv-flags` / try two different ports or two hosts).
4. **RTR attrs**: `hop_limit=64`, `sl=0`, `traffic_class=0`, `path_mtu = min(local active_mtu, peer active_mtu)`,
   `min_rnr_timer=12`, `max_dest_rd_atomic=1`; RTS: `timeout=14`, `retry_cnt=7`, `rnr_retry=7`, `max_rd_atomic=1`.
   If the lab uses PFC on a non-zero priority/DSCP, set `traffic_class` (DSCP<<2) — not needed for loopback.
5. `ibv_query_gid`/`ibv_close_device`/`rdma_*` are treated as "-1 + errno"; `ibv_query_port`, `ibv_modify_qp`,
   `ibv_post_*`, `ibv_destroy_*`, `ibv_dereg_mr`, `ibv_dealloc_pd`, `ibv_req_notify_cq` as "return errno".
   This matches rdma-core man pages; double-check if an error message prints "Success".
6. Completion waits time out after 10 s (rdma2/3) / 15 s (rdma4) and CM events after 15 s, so a broken setup fails
   instead of hanging. `--events` sets the completion-channel fd O_NONBLOCK and polls it.
7. rdma3 `imm_data` is sent as `htonl(0x4e4c3132)` and checked with `ntohl(wc.imm_data)` on the receiver.
   The WRITE_WITH_IMM consumes a zero-SGE RECV on the server.
8. rdma4 private data: 12 bytes (`"NL12"`, version 1, msg_size); parse accepts any length >= 12 because the IB CM
   pads REQ/REP private data. `rdma_accept` passes `responder_resources=1, initiator_depth=1, rnr_retry_count=7`.
   The server serves exactly one connection, rejects and destroys extra CONNECT_REQUEST ids.
9. `active_speed_ex` (rdma-core >= 42 only) is intentionally not used, for portability with older distro headers;
   XDR speeds would print 0.0Gbps.

## Likely fixes if something fails there

- rdma2 `ibv_modify_qp(INIT→RTR): Invalid argument` with the solution → print the chosen GID index / active_mtu;
  a stale `NETLINGS_RDMA_GID_INDEX` or a GID of type RoCE v1 is the usual cause.
- Ping-pong hangs → `wait_wc` timeout message; check `rdma resource show qp` (state), `ethtool -S $IFACE | grep -i
  -E 'out_of_seq|rnr|ack_timeout'`, and that the netdev behind the GID is up (`gid_attrs/ndevs/<i>`).
- rdma4 `rdma_resolve_addr` error / `ADDR_ERROR` → wrong IP: must be the IPv4 on the RDMA netdev.
- rdma3 remote-access test reports a different status on rxe → extend the regex in
  `tests/12_rdma_roce/test_rdma3_write_read.py`, keep the requirement that the status string is printed.
