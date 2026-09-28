import os
import signal
import socket
import threading
import time

import pytest

from studylings.probe import start


def _recv_exact(s, n, deadline):
    buf = bytearray()
    while len(buf) < n:
        s.settimeout(max(0.01, deadline - time.monotonic()))
        try:
            chunk = s.recv(min(65536, n - len(buf)))
        except (socket.timeout, TimeoutError):
            break
        if not chunk:
            break
        buf += chunk
    return bytes(buf)


def test_one_mib_burst_is_fully_echoed(exe, port):
    with start(exe, port) as p:
        p.expect(r"listening on port \d+", timeout=10)
        data = os.urandom(1 << 20)
        with socket.create_connection(("127.0.0.1", port), timeout=5) as s:
            send_err = []

            def sender():
                try:
                    s.sendall(data)
                except OSError as e:
                    send_err.append(e)

            t = threading.Thread(target=sender, daemon=True)
            t.start()
            got = _recv_exact(s, len(data), time.monotonic() + 15)
            if len(got) < len(data):
                pytest.fail(
                    f"发送了 1 MiB，15s 内只收到 {len(got)} 字节回显，然后就停了。\n"
                    "边沿触发下，一个 EPOLLIN 事件只通知一次：如果 read 没读到 EAGAIN，"
                    "剩下的数据再也不会产生事件 —— 连接永远卡住。on_readable 要循环读到 EAGAIN。\n"
                    + p.describe(), pytrace=False)
            assert got == data, "回显的 1 MiB 数据与发送的不一致"
            t.join(timeout=5)
            assert not send_err, f"发送出错：{send_err}"


def test_burst_of_50_queued_connections(exe, port):
    with start(exe, port) as p:
        p.expect(r"listening on port \d+", timeout=10)
        socks = []
        os.kill(p.pid, signal.SIGSTOP)  # 冻结服务器：50 个连接都在 accept 队列里排队
        try:
            for _ in range(50):
                socks.append(socket.create_connection(("127.0.0.1", port), timeout=5))
        finally:
            os.kill(p.pid, signal.SIGCONT)
        try:
            for i, s in enumerate(socks):
                s.sendall(f"ping {i}\n".encode())
            deadline = time.monotonic() + 10
            stuck = []
            for i, s in enumerate(socks):
                want = f"ping {i}\n".encode()
                if _recv_exact(s, len(want), deadline) != want:
                    stuck.append(i)
            if stuck:
                pytest.fail(
                    f"50 个同时排队的连接里有 {len(stuck)} 个没有得到回显。\n"
                    "它们在 accept 队列里只产生了【一次】边沿：监听 socket 就绪时必须循环 accept4 直到 EAGAIN，"
                    "否则剩下的连接永远不会被 accept。\n" + p.describe(), pytrace=False)
        finally:
            for s in socks:
                s.close()
