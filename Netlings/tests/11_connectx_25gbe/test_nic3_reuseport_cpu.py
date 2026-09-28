import collections
import os
import platform
import re
import signal
import socket
import threading

import pytest

from studylings.probe import start

CONNS_PER_CPU = 50


def _cpus(n_max=4) -> list[int]:
    cpus = sorted(os.sched_getaffinity(0))[:n_max]
    if len(cpus) < 2:
        pytest.skip("本机只有 1 个可用 CPU，无法验证连接在多个 CPU 间的分配（至少需要 2 个）")
    return cpus


def _connect_from_cpus(port: int, cpus: list[int]) -> tuple[dict[int, list[tuple[int, int, int]]], list[str]]:
    """每个 CPU 一个客户端线程（绑到该 CPU），各发起 CONNS_PER_CPU 个连接，收集服务器回的那一行。"""
    results: dict[int, list[tuple[int, int, int]]] = collections.defaultdict(list)
    errors: list[str] = []

    def client(cpu: int):
        try:
            os.sched_setaffinity(0, {cpu})  # 0 = 当前线程：loopback 的收包软中断就在这个 CPU 上跑
            for _ in range(CONNS_PER_CPU):
                with socket.create_connection(("127.0.0.1", port), timeout=10) as s:
                    line = s.makefile("r").readline()
                m = re.match(r"worker=(\d+) cpu=(-?\d+) incoming_cpu=(-?\d+)", line)
                if not m:
                    errors.append(f"CPU {cpu} 上的客户端收到 {line!r}，期望 'worker=I cpu=C incoming_cpu=X'")
                    return
                results[cpu].append(tuple(map(int, m.groups())))
        except OSError as e:
            errors.append(f"CPU {cpu} 上的客户端：{e!r}")

    threads = [threading.Thread(target=client, args=(c,)) for c in cpus]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=120)
    return results, errors


def _stop_and_summary(p, n: int) -> str:
    p.signal(signal.SIGTERM)
    rc = p.wait(timeout=10)
    assert rc == 0, f"收到 SIGTERM 后应正常退出（exit 0），实际 {rc}\n" + p.describe()
    total = CONNS_PER_CPU * n
    m = re.search(r"^total accepted=(\d+) cpu_mismatch=(\d+)$", p.stdout, re.M)
    assert m, "退出时应打印 'total accepted=T cpu_mismatch=M'\n" + p.describe()
    assert int(m.group(1)) == total, f"total accepted={m.group(1)}，客户端一共连接了 {total} 次\n" + p.describe()
    return p.stdout


def _run_mode(exe, port, mode):
    cpus = _cpus()
    n = len(cpus)
    with start(exe, port, n, "--mode", mode) as p:
        m = p.expect(r"listening on port \d+ workers=(\d+) mode=(\S+) cpus=([\d,]+)", timeout=10)
        assert [int(c) for c in m.group(3).split(",")] == cpus, (
            f"worker 应依次绑到可用 CPU {cpus}，程序报告 cpus={m.group(3)}")
        results, errors = _connect_from_cpus(port, cpus)
        if errors:
            pytest.fail("\n".join(errors[:5]) + "\n" + p.describe(), pytrace=False)
        out = _stop_and_summary(p, n)
    return cpus, results, out


def test_hash_spreads_over_all_workers(exe, port):
    cpus, results, out = _run_mode(exe, port, "hash")
    per_worker = collections.Counter(w for rs in results.values() for (w, _, _) in rs)
    for i, cpu in enumerate(cpus):
        assert per_worker[i] > 0, (
            f"worker {i} 一个连接都没分到（分布 {dict(per_worker)}）。每个 worker 都要有自己的 SO_REUSEPORT "
            "监听 socket，内核按 4 元组哈希把连接分散到组内各 socket")
    for rs in results.values():
        for w, cpu, _ in rs:
            assert cpu == cpus[w], (f"worker {w} 报告自己在 CPU {cpu} 上运行，应该绑在 CPU {cpus[w]} 上"
                                    "（pthread_setaffinity_np）")


def _assert_cpu_local(cpus, results, how):
    for k, rs in results.items():
        want = cpus.index(k)
        wrong = [r for r in rs if r[0] != want]
        # 允许极少量例外（例如被迁移到 ksoftirqd 的边界情况），但 90% 以上必须命中
        assert len(wrong) <= len(rs) // 10, (
            f"从 CPU {k} 发起的 {len(rs)} 个连接中有 {len(wrong)} 个没有交给绑在 CPU {k} 上的 worker {want}，"
            f"例如 {wrong[:3]}（{how}）")
        for w, cpu, incoming in rs:
            if w == want:
                assert cpu == k, f"worker {w} 在 CPU {cpu} 上处理连接，应在 CPU {k}（没绑核？）"
                assert incoming == k, f"SO_INCOMING_CPU={incoming}，应为收包 CPU {k}"


def test_cbpf_steers_to_local_cpu(exe, port):
    cpus, results, _ = _run_mode(exe, port, "cbpf")
    _assert_cpu_local(cpus, results,
                      "SO_ATTACH_REUSEPORT_CBPF：A = SKF_AD_OFF + SKF_AD_CPU，A == cpus[i] 时返回下标 i")


def test_incoming_cpu_steers_to_local_cpu(exe, port):
    major, minor = (int(x) for x in re.match(r"(\d+)\.(\d+)", platform.release()).groups())
    if (major, minor) < (6, 1):
        pytest.skip(f"内核 {platform.release()} < 6.1：reuseport 的哈希选择还不考虑 SO_INCOMING_CPU")
    cpus, results, _ = _run_mode(exe, port, "incoming-cpu")
    _assert_cpu_local(cpus, results, "每个监听 socket 设 SO_INCOMING_CPU = 它所在的 CPU")
