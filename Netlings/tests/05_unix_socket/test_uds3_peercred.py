import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile

import pytest

from studylings.probe import start


@pytest.fixture
def sock_dir(tmp_path):
    """sun_path 只有 108 字节：tmp_path 太长时换一个短目录。"""
    if len(str(tmp_path)) < 80:
        yield tmp_path
        return
    d = tempfile.mkdtemp(prefix="sl-uds-")
    try:
        yield d
    finally:
        shutil.rmtree(d, ignore_errors=True)


def ask(path: str) -> str:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as c:
        c.settimeout(5)
        c.connect(path)
        data = b""
        while chunk := c.recv(256):
            data += chunk
    return data.decode()


def parse(line: str) -> tuple[int, int, int]:
    m = re.fullmatch(r"pid=(-?\d+) uid=(-?\d+) gid=(-?\d+)\n", line)
    if not m:
        pytest.fail(f"回复格式应为 'pid=<p> uid=<u> gid=<g>\\n'，实际 {line!r}", pytrace=False)
    return tuple(map(int, m.groups()))


def test_reports_peer_credentials(exe, sock_dir):
    path = os.path.join(sock_dir, "cred.sock")
    with start(exe, path) as p:
        p.expect(r"listening", timeout=10)
        pid, uid, gid = parse(ask(path))
        assert pid != p.pid, "回复的是服务器自己的 pid —— 要查的是对端（客户端）的凭证"
        assert (pid, uid, gid) == (os.getpid(), os.getuid(), os.getgid()), (
            f"应当回复客户端的 pid/uid/gid = {(os.getpid(), os.getuid(), os.getgid())}，实际 {(pid, uid, gid)}")


def test_distinguishes_different_clients(exe, sock_dir):
    """再从另一个进程连一次：pid 必须跟着客户端变。"""
    path = os.path.join(sock_dir, "cred2.sock")
    code = (
        "import os,socket,sys\n"
        "c=socket.socket(socket.AF_UNIX); c.settimeout(5); c.connect(sys.argv[1])\n"
        "d=b''\n"
        "while (x:=c.recv(256)): d+=x\n"
        "print(os.getpid()); print(d.decode(), end='')\n"
    )
    with start(exe, path) as p:
        p.expect(r"listening", timeout=10)
        r = subprocess.run([sys.executable, "-c", code, path], capture_output=True, text=True, timeout=20)
        assert r.returncode == 0, f"子进程客户端失败：{r.stderr}"
        child_pid_line, reply = r.stdout.split("\n", 1)
        pid, _, _ = parse(reply)
        assert pid == int(child_pid_line), f"另一个客户端进程 pid={child_pid_line}，服务器却回复 pid={pid}"
