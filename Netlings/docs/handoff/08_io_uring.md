# 08_io_uring — handoff notes

Validated on the authoring box (kernel 6.18, liburing 2.5 headers, root, GCC 13, ASan+UBSan):
all 5 solutions pass (25 tests, 0 skips, stable over 3 sequential + 3 parallel runs); all 5 starters fail.
Nothing in this chapter needs the ConnectX NIC; everything runs on loopback / local files.

## Exercises

| name | lesson | probe |
|---|---|---|
| uring1_read_batch | QD=8 IORING_OP_READ, out-of-order completion, short reads, `cqe->res = -errno` | content for 0/1/64K-1/1MiB+123 B; reading a directory → `-EISDIR` message; strace: no read/pread64 on the file, `io_uring_enter` ≤ chunks/2 |
| uring2_echo_server | accept/recv/send, user_data = op\|bidx\|fd, re-arm accept, short sends | 50 clients; 4×3 MiB payloads with slow readers (server sets SO_SNDBUF=16K so short sends always happen); abrupt RST clients; socket count back to baseline |
| uring3_multishot | multishot accept + multishot recv + provided buffer ring (16×4 KiB), `F_MORE`/`F_BUFFER`, `-ENOBUFS`, buffer recycling | 50 clients with large payloads; 3000 small msgs on one conn; burst of 200 connects; no fd leak |
| uring4_link_timeout | CONNECT →link RECV →link LINK_TIMEOUT in one submit | line reply (split in 2 sends); silent server → `timeout` exit 3 in [0.45 s, 8 s); half line then silence → timeout; closed port → `refused` exit 2 |
| uring5_fixed_sqpoll | register_files / register_buffers, IOSQE_FIXED_FILE, read_fixed/write_fixed, SQPOLL | copies of 0 B … 3 MiB+7 (also `--sqpoll`); strace shows IORING_REGISTER_FILES/BUFFERS, no direct read/write of SRC/DST; `--sqpoll` ≤ 8 `io_uring_enter` for 64 chunks |

## Skip contract

Every program prints `io_uring unavailable: <why>` and exits **77** when `io_uring_queue_init` returns
-EPERM/-ENOSYS/-EACCES (uring3 also when buffer rings / multishot return -EINVAL, i.e. kernel < 6.0).
`tests/08_io_uring/conftest.py` (`urun`, `userver` fixtures) turns that into `pytest.skip`.
Verified by LD_PRELOAD-ing a stub `io_uring_queue_init` returning -EPERM: 25/25 skip cleanly.

Tests that can skip for other reasons:
- strace-based tests (uring1 `test_uses_io_uring_not_read`, uring5 `test_registered_files_and_buffers`,
  `test_sqpoll_avoids_io_uring_enter`) skip if strace is missing or ptrace is forbidden.
- `test_sqpoll_avoids_io_uring_enter` skips if the program printed `note: SQPOLL unavailable`.
- uring1 `test_negative_res_is_errno` skips if the filesystem reports st_size == 0 for directories.

## Checklist for the real machine

- [ ] `sysctl kernel.io_uring_disabled` is 0 (1 = only group `kernel.io_uring_group` may use it; 2 = off).
      Not inside Docker with the default seccomp profile (use `--security-opt seccomp=unconfined`).
- [ ] `pkg-config --modversion liburing` ≥ 2.3 (needs `io_uring_setup_buf_ring`, `io_uring_prep_multishot_accept`,
      `io_uring_prep_recv_multishot`). With liburing < 2.4 check that `io_uring_setup_buf_ring` exists; if not,
      uring3 needs a manual `io_uring_register_buf_ring` + mmap fallback.
- [ ] `STUDYLINGS_PRESET=solutions python -m pytest -q tests/08_io_uring` → 25 passed, 0 skipped (on kernel ≥ 6.1).
- [ ] `python -m studylings.selfcheck Netlings uring1_read_batch uring2_echo_server uring3_multishot uring4_link_timeout uring5_fixed_sqpoll`
      → all "solution ok, exercise fails".
- [ ] As a non-root user: uring5 `--sqpoll` must still work on ≥ 5.11 (unprivileged SQPOLL). If `RLIMIT_MEMLOCK`
      is tiny (< 1 MiB) `io_uring_register_buffers` returns -ENOMEM → raise `ulimit -l`.

## Known risks / assumptions

- uring1's enter-count assertion (≤ chunks/2) assumes buffered reads of a page-cached file complete mostly
  inline. On a slow/NFS/FUSE filesystem the probe's tmp dir might produce more enters; the probe reads the
  file once first to warm the cache. If it fails there, set `TMPDIR` to a local fs.
- uring2 relies on SO_SNDBUF=16K making 64 KiB sends short; if a kernel ever retried partial stream sends
  internally without MSG_WAITALL, the starter's "ignores partial send" bug would stop being detected by
  `test_big_payload_slow_reader_partial_send` (the starter still fails via the missing accept re-arm).
- uring3 needs kernel ≥ 6.0 (multishot recv). With only 16 buffers, `-ENOBUFS` (which ends the multishot,
  F_MORE clear) shows up even on a single connection: the kernel can loop a multishot recv over many small
  segments, one buffer each, before user space gets to recycle. On 6.18 a starter variant with recycling fixed
  but no re-arm fails all three uring3 tests (149 `-ENOBUFS` terminations in one run). If a future kernel
  batches differently, the 200-connect burst is still the most reliable trigger.
- uring5 SQPOLL mode busy-polls the CQ (no `io_uring_wait_cqe`), burning one core for the copy's duration
  on purpose; the SQ thread idles after 2 s.

## Worth adding on newer kernels / liburing (not done here: box has liburing 2.5)

- `IORING_OP_SEND_ZC` / `io_uring_prep_send_zc` (6.0+) with registered buffers: two CQEs per send
  (result + `IORING_CQE_F_NOTIF` when the buffer can be reused). On 25GbE this is where io_uring beats epoll
  for large-message servers; on loopback it is usually slower (copy is cheap there). Exercise idea:
  uring6_send_zc with a probe that checks the NOTIF CQE arrives and buffers are not reused before it.
- Recv bundles (`IORING_RECVSEND_BUNDLE`, 6.10+, liburing 2.7): one CQE covering several provided buffers.
- Incremental buffer consumption (`IOU_PBUF_RING_INC`, 6.12+, liburing 2.8): large provided buffers
  consumed piecewise by successive recvs; `IORING_CQE_F_BUF_MORE`.
- `io_uring_register_ring_fd` (5.18+) and `IORING_SETUP_SINGLE_ISSUER | IORING_SETUP_DEFER_TASKRUN` (6.1+):
  the recommended setup flags for single-threaded servers like uring2/uring3; worth a benchmark column.
- Zero-copy receive (`IORING_OP_RECV_ZC`, 6.15+) needs NIC header/data split + flow steering — mlx5 supports it;
  a natural bridge to chapter 11.

## Benchmark suggestion (real machine)

Compare N04 `epoll1_lt_echo` / `epoll2_et_drain` vs `uring2_echo_server` vs `uring3_multishot` (Release build,
no sanitizers: `cmake -B build/rel -DCMAKE_BUILD_TYPE=Release -DSL_SANITIZE= -DSL_SOURCE_DIR=solutions`):

```bash
taskset -c 2 build/rel/bin/uring3_multishot 9000 &
# load generator on other cores (or on the peer host via NETLINGS_PEER_IP after changing the bind address):
#   rust_echo_bench:  cargo run --release -- --address 127.0.0.1:9000 --number 1000 --duration 30 --length 512
#   or tcpkali:       tcpkali -c 1000 -T 30s -m 'x' --message-rate 1000 127.0.0.1:9000
perf stat -e syscalls:sys_enter_io_uring_enter,syscalls:sys_enter_epoll_wait,context-switches -p $(pgrep -n uring3) -- sleep 10
```
Report: msgs/s, p99 latency, syscalls per message, CPU% of the server core; for 64 B, 512 B, 16 KiB messages and
100 / 1000 / 10000 connections. Expect uring3 < uring2 in memory (shared buffer ring) and syscalls/msg;
the epoll gap widens with connection count and with `DEFER_TASKRUN`. Note: the exercise servers bind 127.0.0.1;
for two-host runs change `INADDR_LOOPBACK` to `INADDR_ANY` in the Release copy only.
