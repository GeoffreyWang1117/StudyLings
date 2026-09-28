import os
import socket
import threading
import time
from pathlib import Path

import pytest

from studylings.probe import fd_targets, start

O_NONBLOCK = 0o4000
O_CLOEXEC = 0o2000000
N_CLIENTS = 100
ROUNDS = 5


def _recv_exact(s, n):
    buf = b""
    while len(buf) < n:
        chunk = s.recv(n - len(buf))
        if not chunk:
            break
        buf += chunk
    return buf


def _fd_flags(pid, fd) -> int:
    for line in Path(f"/proc/{pid}/fdinfo/{fd}").read_text().splitlines():
        if line.startswith("flags:"):
            return int(line.split()[1], 8)
    return 0


def _socket_fds(pid):
    return {fd: t for fd, t in fd_targets(pid).items() if t.startswith("socket:")}


def test_hundred_concurrent_clients(exe, port):
    with start(exe, port) as p:
        p.expect(r"listening on port \d+", timeout=10)
        errors: list[str] = []
        phase = threading.Barrier(N_CLIENTS + 1)
        release = threading.Barrier(N_CLIENTS + 1)

        def client(i):
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=5) as s:
                    for r in range(ROUNDS):
                        msg = f"<{i}:{r}>".encode() * (1 + (i * 7 + r) % 50)
                        s.sendall(msg)
                        got = _recv_exact(s, len(msg))
                        if got != msg:
                            errors.append(f"客户端 {i} 第 {r} 轮：收到 {got[:60]!r}... 期望 {msg[:60]!r}...")
                            break
                        if r == 0:
                            phase.wait(timeout=30)
                            release.wait(timeout=30)
            except (OSError, threading.BrokenBarrierError) as e:
                errors.append(f"客户端 {i}：{e!r}（5s 内没收到回显？新连接加入 epoll 了吗？）")
                phase.abort()
                release.abort()

        threads = [threading.Thread(target=client, args=(i,)) for i in range(N_CLIENTS)]
        for t in threads:
            t.start()
        try:
            phase.wait(timeout=40)
        except threading.BrokenBarrierError:
            pass
        # 此刻 100 个连接都已建立并回显过一次：检查 fd 标志
        flag_errors = []
        if not errors:
            socks = _socket_fds(p.pid)
            if len(socks) < N_CLIENTS + 1:
                flag_errors.append(f"服务器只持有 {len(socks)} 个 socket，应至少 {N_CLIENTS + 1} 个")
            for fd, target in fd_targets(p.pid).items():
                if fd <= 2:
                    continue
                flags = _fd_flags(p.pid, fd)
                if (target.startswith("socket:") or "eventpoll" in target) and not flags & O_CLOEXEC:
                    flag_errors.append(f"fd {fd} ({target}) 没有 CLOEXEC（accept4/epoll_create1 的 flags）")
            nonblock = [fd for fd in socks if _fd_flags(p.pid, fd) & O_NONBLOCK]
            if len(nonblock) < N_CLIENTS:
                flag_errors.append(f"只有 {len(nonblock)} 个 socket 是 O_NONBLOCK，连接 socket 都应该是非阻塞的"
                                   "（accept4 的 SOCK_NONBLOCK）")
        try:
            release.wait(timeout=10)
        except threading.BrokenBarrierError:
            pass
        for t in threads:
            t.join(timeout=60)
        if errors:
            pytest.fail(f"{len(errors)} 个客户端出错，例如：\n" + "\n".join(errors[:5]) + "\n" + p.describe(),
                        pytrace=False)
        if flag_errors:
            pytest.fail("\n".join(flag_errors[:5]), pytrace=False)

        # 所有客户端都断开了：服务器应只剩监听 socket
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline and len(_socket_fds(p.pid)) > 1:
            time.sleep(0.1)
        left = len(_socket_fds(p.pid))
        assert left == 1, (f"所有客户端都断开后服务器还持有 {left} 个 socket fd（应只剩监听 socket）："
                           "read 返回 0 时要 EPOLL_CTL_DEL 并 close")
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()
