import os
import selectors
import socket
import threading
import time

import pytest

from studylings.probe import fd_targets

N_CLIENTS = 50
BURST = 200


def _socket_count(pid) -> int:
    return sum(1 for t in fd_targets(pid).values() if t.startswith("socket:"))


def _wait_sockets(pid, want, timeout=10) -> int:
    deadline = time.monotonic() + timeout
    n = _socket_count(pid)
    while time.monotonic() < deadline and n > want:
        time.sleep(0.05)
        n = _socket_count(pid)
    return n


def _recv_exact(s, n, timeout) -> bytes:
    buf = bytearray()
    deadline = time.monotonic() + timeout
    while len(buf) < n:
        s.settimeout(max(0.01, deadline - time.monotonic()))
        try:
            chunk = s.recv(min(1 << 20, n - len(buf)))
        except (socket.timeout, TimeoutError, OSError):
            break
        if not chunk:
            break
        buf += chunk
    return bytes(buf)


def test_fifty_concurrent_clients(exe, port, userver):
    with userver(exe, port) as p:
        base = _socket_count(p.pid)
        errors: list[str] = []
        gate = threading.Barrier(N_CLIENTS)

        def client(i):
            try:
                gate.wait(timeout=30)
                with socket.create_connection(("127.0.0.1", port), timeout=10) as s:
                    for r in range(3):
                        msg = os.urandom(1000 + (i * 7919 + r * 104729) % 200_000)
                        t = threading.Thread(target=s.sendall, args=(msg,), daemon=True)
                        t.start()
                        got = _recv_exact(s, len(msg), 10)
                        t.join(timeout=10)
                        if got != msg:
                            errors.append(f"客户端 {i} 第 {r} 轮：{len(msg)} 字节只收回 {len(got)} 字节或内容不符")
                            return
            except (OSError, threading.BrokenBarrierError) as e:
                errors.append(f"客户端 {i}：{e!r}")

        threads = [threading.Thread(target=client, args=(i,)) for i in range(N_CLIENTS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)
        if errors:
            pytest.fail(f"{len(errors)}/{N_CLIENTS} 个客户端出错，例如：\n" + "\n".join(errors[:5]) +
                        "\n用过的缓冲区要 io_uring_buf_ring_add + advance 还给环；"
                        "CQE 没有 IORING_CQE_F_MORE 时要重新提交 multishot recv\n" + p.describe(), pytrace=False)
        left = _wait_sockets(p.pid, base)
        assert left == base, f"所有客户端断开后服务器还持有 {left} 个 socket（开始时 {base} 个）"
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()


def test_many_small_messages_one_connection(exe, port, userver):
    """一个连接上 3000 条小消息：recv 次数远超 16 块缓冲区，不归还缓冲区就会卡住。"""
    with userver(exe, port) as p:
        with socket.create_connection(("127.0.0.1", port), timeout=10) as s:
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            total = bytearray()
            for k in range(3000):
                line = f"msg {k:05d}\n".encode()
                s.sendall(line)
                total += line
                if k % 100 == 99:  # 每 100 条等一次回显，保证服务器真的做了很多次 recv
                    got = _recv_exact(s, 100 * len(line), 10)
                    want = bytes(total[-100 * len(line):])
                    if got != want:
                        pytest.fail(f"第 {k + 1} 条消息附近回显卡住/出错：期望 {len(want)} 字节，收到 {len(got)}。\n"
                                    "缓冲区环只有 16 块：每个 recv CQE 用掉一块（编号在 cqe->flags >> "
                                    "IORING_CQE_BUFFER_SHIFT），处理完必须还回去；"
                                    "用光时 recv 以 -ENOBUFS 结束且没有 F_MORE → 要重新提交\n" + p.describe(),
                                    pytrace=False)
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()


def test_burst_of_200_connects(exe, port, userver):
    """200 个连接几乎同时涌入并各发一条消息：multishot accept 要全部接住；
    16 块缓冲区必然被耗尽（-ENOBUFS），multishot recv 终止后要重新挂上。"""
    with userver(exe, port) as p:
        base = _socket_count(p.pid)
        socks = []
        try:
            for i in range(BURST):
                s = socket.socket()
                s.settimeout(10)
                s.connect(("127.0.0.1", port))
                socks.append(s)
            msgs = {}
            for i, s in enumerate(socks):
                msgs[i] = f"hello from {i} ".encode() * 20
                s.sendall(msgs[i])
            # 并发地收：用 selectors 同时等 200 个 socket
            got = {i: bytearray() for i in range(BURST)}
            sel = selectors.DefaultSelector()
            for i, s in enumerate(socks):
                s.setblocking(False)
                sel.register(s, selectors.EVENT_READ, i)
            deadline = time.monotonic() + 20
            pending = set(range(BURST))
            while pending and time.monotonic() < deadline:
                for key, _ in sel.select(timeout=0.5):
                    i = key.data
                    try:
                        chunk = key.fileobj.recv(65536)
                    except BlockingIOError:
                        continue
                    except OSError:
                        chunk = b""
                    if not chunk:
                        sel.unregister(key.fileobj)
                        pending.discard(i)
                        continue
                    got[i] += chunk
                    if len(got[i]) >= len(msgs[i]):
                        sel.unregister(key.fileobj)
                        pending.discard(i)
            sel.close()
            bad = [i for i in range(BURST) if bytes(got[i]) != msgs[i]]
            if bad:
                pytest.fail(f"{len(bad)}/{BURST} 个连接没有收到完整回显（例如 #{bad[:5]}）。\n"
                            "突发连接下 16 块缓冲区会被耗尽：recv CQE 为 -ENOBUFS 且没有 IORING_CQE_F_MORE，"
                            "要重新提交 multishot recv；multishot accept 没有 F_MORE 时也要重新提交\n"
                            + p.describe(), pytrace=False)
        finally:
            for s in socks:
                s.close()
        left = _wait_sockets(p.pid, base)
        assert left == base, (f"{BURST} 个连接都断开后服务器还持有 {left} 个 socket（开始时 {base} 个）："
                              "recv 返回 0 且没有请求在飞时要 close(fd)")
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()
