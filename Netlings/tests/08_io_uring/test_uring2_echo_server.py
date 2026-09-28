import os
import socket
import struct
import threading
import time

import pytest

from studylings.probe import fd_targets

N_CLIENTS = 50


def _socket_count(pid) -> int:
    return sum(1 for t in fd_targets(pid).values() if t.startswith("socket:"))


def _echo_roundtrip(port, payload: bytes, *, rcvbuf=None, read_delay=0.0, timeout=60) -> bytes:
    """一个线程发送 payload，同时（可选延迟后）读回同样多的字节。"""
    s = socket.socket()
    if rcvbuf:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rcvbuf)
    s.settimeout(timeout)
    s.connect(("127.0.0.1", port))
    send_err = []

    def sender():
        try:
            s.sendall(payload)
        except OSError as e:
            send_err.append(e)

    t = threading.Thread(target=sender, daemon=True)
    t.start()
    if read_delay:
        time.sleep(read_delay)
    buf = bytearray()
    deadline = time.monotonic() + timeout
    try:
        while len(buf) < len(payload) and time.monotonic() < deadline:
            chunk = s.recv(min(1 << 20, len(payload) - len(buf)))
            if not chunk:
                break
            buf += chunk
    except OSError:
        pass
    t.join(timeout=5)
    s.close()
    return bytes(buf)


def _wait_sockets(pid, want, timeout=10) -> int:
    deadline = time.monotonic() + timeout
    n = _socket_count(pid)
    while time.monotonic() < deadline and n > want:
        time.sleep(0.05)
        n = _socket_count(pid)
    return n


def test_fifty_concurrent_clients(exe, port, userver):
    with userver(exe, port) as p:
        base = _socket_count(p.pid)
        errors: list[str] = []
        start_gate = threading.Barrier(N_CLIENTS)

        def client(i):
            try:
                start_gate.wait(timeout=30)
                with socket.create_connection(("127.0.0.1", port), timeout=10) as s:
                    for r in range(4):
                        msg = f"[{i}:{r}]".encode() * (1 + (i * 13 + r * 7) % 400)
                        s.sendall(msg)
                        got = bytearray()
                        while len(got) < len(msg):
                            chunk = s.recv(len(msg) - len(got))
                            if not chunk:
                                break
                            got += chunk
                        if bytes(got) != msg:
                            errors.append(f"客户端 {i} 第 {r} 轮：收到 {len(got)}/{len(msg)} 字节，内容不符")
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
                        "\n（只有第一个客户端能连上？ACCEPT 完成后要重新提交一个 ACCEPT）\n" + p.describe(),
                        pytrace=False)
        left = _wait_sockets(p.pid, base)
        assert left == base, (f"所有客户端断开后服务器还持有 {left} 个 socket（开始时 {base} 个）："
                              "recv 返回 0 / 负数时要 close(fd) 并归还缓冲区")
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()


def test_big_payload_slow_reader_partial_send(exe, port, userver):
    """客户端接收窗口很小、而且先不读：服务器的 send 会只发出一部分（短写）。"""
    with userver(exe, port) as p:
        results: dict[int, bytes] = {}
        payloads = {i: os.urandom((3 << 20) + i * 4099) for i in range(4)}

        def worker(i):
            results[i] = _echo_roundtrip(port, payloads[i], rcvbuf=16 * 1024, read_delay=0.5, timeout=20)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)
        for i, data in payloads.items():
            got = results.get(i, b"")
            if got != data:
                bad = next((k for k, (a, b) in enumerate(zip(got, data)) if a != b), min(len(got), len(data)))
                pytest.fail(f"客户端 {i}：发送 {len(data)} 字节，收回 {len(got)} 字节，从偏移 {bad} 起不一致。\n"
                            "SEND 的 cqe->res 可能小于请求长度（短写），要把剩余部分重新提交，"
                            "全部发完才能再提交 RECV\n" + p.describe(), pytrace=False)
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()


def test_clients_disconnect_midstream_no_fd_leak(exe, port, userver):
    with userver(exe, port) as p:
        base = _socket_count(p.pid)
        # 30 个客户端：发一大块然后不读就直接关（服务器 send 会遇到 EPIPE/ECONNRESET），
        # 另 20 个客户端：连上就立刻关（recv 返回 0）
        socks = []
        for i in range(30):
            s = socket.create_connection(("127.0.0.1", port), timeout=10)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))  # close → RST
            try:
                s.sendall(os.urandom(100_000))
            except OSError:
                pass
            socks.append(s)
        for i in range(20):
            socket.create_connection(("127.0.0.1", port), timeout=10).close()
        time.sleep(0.2)
        for s in socks:
            s.close()
        left = _wait_sockets(p.pid, base)
        assert left == base, (f"50 个客户端都断开后服务器还持有 {left} 个 socket（开始时 {base} 个）：\n"
                              "recv 返回 0、recv/send 返回 -ECONNRESET/-EPIPE 时都要 close(fd)")
        assert p.p.poll() is None, "客户端异常断开不应导致服务器退出（SIGPIPE？MSG_NOSIGNAL）\n" + p.describe()
        # 服务器仍然正常工作
        assert _echo_roundtrip(port, b"still alive\n", timeout=10) == b"still alive\n", \
            "客户端断开之后服务器不再响应新连接\n" + p.describe()
