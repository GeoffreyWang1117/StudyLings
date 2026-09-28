import hashlib
import os
import socket
import threading

import pytest

from studylings.probe import assert_ok, run


class DigestServer:
    """读到 EOF 为止，然后回复 "bytes=<n> sha256=<hex>\\n" 并关闭。"""

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(4)
        self.sock.settimeout(15)
        self.port = self.sock.getsockname()[1]
        self.saw_eof = False
        self.reply_error = None
        self.t = threading.Thread(target=self._serve, daemon=True)
        self.t.start()

    def _serve(self):
        try:
            c, _ = self.sock.accept()
        except OSError:
            return
        with c:
            c.settimeout(8)
            h, n = hashlib.sha256(), 0
            try:
                while True:
                    d = c.recv(1 << 16)
                    if not d:
                        self.saw_eof = True
                        break
                    h.update(d)
                    n += len(d)
                c.sendall(f"bytes={n} sha256={h.hexdigest()}\n".encode())
            except OSError as e:
                self.reply_error = e

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()
        self.t.join(timeout=10)


def _upload(exe, data: bytes):
    srv = DigestServer()
    try:
        failed = None
        try:
            r = run(exe, "127.0.0.1", srv.port, input=data, timeout=5)
        except pytest.fail.Exception as e:
            failed = str(e)
    finally:
        srv.close()
    if failed is not None:
        pytest.fail("客户端 5 秒内没有结束：服务器在等 EOF，客户端在等回复，双方互等。\n"
                    "上传完后要 shutdown(fd, SHUT_WR) 发出 FIN。\n" + failed, pytrace=False)
    assert srv.saw_eof, "服务器没有读到 EOF（没发 FIN？）"
    return r


def test_uploads_file_and_prints_reply(exe):
    data = os.urandom(3 * 1024 * 1024 + 123)
    r = _upload(exe, data)
    assert_ok(r, what="上传 3 MiB")
    want = f"bytes={len(data)} sha256={hashlib.sha256(data).hexdigest()}\n"
    assert r.stdout == want.encode(), (
        f"应打印服务器回复 {want!r}，实际 {r.stdout[:200]!r}"
        "（用 close 代替 shutdown 的话，回复会丢失）")


def test_empty_upload(exe):
    r = _upload(exe, b"")
    assert_ok(r, what="空上传")
    want = f"bytes=0 sha256={hashlib.sha256(b'').hexdigest()}\n"
    assert r.stdout == want.encode(), f"空输入也要发 FIN 并读回复，实际 {r.stdout!r}"
