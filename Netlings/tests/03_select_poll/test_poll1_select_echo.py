import socket
import threading

import pytest

from studylings.probe import start


def _connect(port, timeout=5.0):
    s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
    return s


def _recv_exact(s, n):
    buf = b""
    while len(buf) < n:
        chunk = s.recv(n - len(buf))
        if not chunk:
            break
        buf += chunk
    return buf


def _echo(s, msg: bytes) -> bytes:
    s.sendall(msg)
    return _recv_exact(s, len(msg))


def _start_server(exe, port):
    p = start(exe, port)
    p.expect(r"listening on port \d+", timeout=10)
    return p, port


def test_silent_client_does_not_block_others(exe, port):
    p, port = _start_server(exe, port)
    with p:
        silent = _connect(port)  # 连上但一个字节都不发
        try:
            other = _connect(port)
            try:
                got = _echo(other, b"hello select\n")
            except socket.timeout:
                pytest.fail("第二个客户端 5s 内没有收到回显：服务器卡在第一个（沉默）客户端的 read 上了。"
                            "只有 select 报告可读的 fd 才能去 read。\n" + p.describe(), pytrace=False)
            assert got == b"hello select\n", f"回显内容不对：{got!r}"
            other.close()
        finally:
            silent.close()


def test_twenty_clients_interleaved(exe, port):
    p, port = _start_server(exe, port)
    with p:
        silent = _connect(port)
        n_clients, rounds = 20, 10
        socks = [_connect(port) for _ in range(n_clients)]
        errors: list[str] = []
        barrier = threading.Barrier(n_clients)

        def worker(i, s):
            try:
                barrier.wait(timeout=10)
                for r in range(rounds):
                    msg = f"client {i} round {r} ".encode() * (1 + (i + r) % 7) + b"\n"
                    got = _echo(s, msg)
                    if got != msg:
                        errors.append(f"客户端 {i} 第 {r} 轮：发送 {msg!r}，收到 {got!r}")
                        return
            except (OSError, threading.BrokenBarrierError) as e:
                errors.append(f"客户端 {i}：{e!r}（5s 内没收到回显？）")

        threads = [threading.Thread(target=worker, args=(i, s)) for i, s in enumerate(socks)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)
        for s in socks:
            s.close()
        silent.close()
        if errors:
            pytest.fail(f"{len(errors)} 个客户端出错，例如：\n" + "\n".join(errors[:5]) + "\n" + p.describe(),
                        pytrace=False)

        # 所有人断开后，服务器必须还活着并能服务新客户端（断开的 fd 要被清理掉）
        for _ in range(3):
            s = _connect(port)
            try:
                assert _echo(s, b"still alive\n") == b"still alive\n", "客户端断开后，新客户端的回显不对"
            except socket.timeout:
                pytest.fail("旧客户端断开后，新客户端得不到回显（没有把关闭的 fd 从集合中移除？）\n" + p.describe(),
                            pytrace=False)
            finally:
                s.close()
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()
