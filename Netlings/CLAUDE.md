# Netlings — notes for Claude Code

Netlings is a rustlings-style C23 course (UNP sockets → epoll → io_uring → netns/tc → eBPF/XDP →
25GbE ConnectX → RDMA/RoCE) built on the shared `studylings` framework in the repo root.
Learner-facing text (exercise headers, hints, probe messages) is Chinese; code identifiers and these
maintainer docs are English.

**If you are running on the ConnectX / RDMA hardware machine, read `docs/handoff/README.md` first.**
It describes what was validated where, what still needs real hardware, and the order to work in.

## Layout (one exercise = four files)

```
exercises/<chapter>/<name>.c      starter the learner edits (compiles, must FAIL its probe; has "// I AM NOT DONE")
solutions/<chapter>/<name>.c      same file completed (must PASS its probe)
tests/<chapter>/test_<name>.py    pytest behaviour probe (drives the binary from outside)
hints/<chapter>/<name>.md         progressive hints, one "## 提示 N" section per level
```

- Each `.c` becomes its own executable `build/<preset>/bin/<name>`; stems are globally unique.
- `10_ebpf_xdp`: one file holds the BPF program (`#ifdef __BPF__`) and its loader; CMake also builds
  `bin/<name>.bpf.o` with clang and passes its path as `SL_BPF_OBJ`.
- Chapter libraries: `08_io_uring` → liburing, `10_ebpf_xdp` → libbpf, `12_rdma_roce` → libibverbs + librdmacm.
- Sanitizers: ASan+UBSan everywhere, TSan for `07_pthread_sync`. Exit code 23 = ASan/LSan, 66 = TSan.
- Probe helpers: `studylings/probe.py` (`exe`, `run`, `start`, `free_port`, `strace_run`, `assert_ok`, ...)
  and `studylings/netlab.py` (`netlab` fixture: netns + veth + tc, root only).

## Commands

```bash
pip install -e ..                               # framework (click, rich, watchdog, pytest)
cmake --preset dev && cmake --preset solutions
python -m studylings.selfcheck Netlings -j 4    # run from repo root; root needed for N09+ (see handoff)
python -m studylings.selfcheck Netlings nic1_ethtool_info rdma2_rc_pingpong   # selected exercises
STUDYLINGS_PRESET=solutions python -m pytest -q tests/11_connectx_25gbe      # probes against solutions
```

## Rules when changing exercises

- Keep starter and solution in sync: only the TODO / BUG spots differ, plus the removed `I AM NOT DONE` line.
- A starter must keep failing for the *lesson's* reason; a solution must pass. Verify both with selfcheck.
- Missing hardware/privilege/kernel feature → `pytest.skip("<中文原因 + 如何满足>")`, never a silent pass.
- Do not loosen an assertion just to go green; if hardware behaves differently than assumed, fix the
  assumption and document it in the chapter's `docs/handoff/<chapter>.md`.
- Hardware env vars: `NETLINGS_IFACE`, `NETLINGS_PEER_IP`, `NETLINGS_RDMA_DEV`, `NETLINGS_RDMA_GID_INDEX`.
