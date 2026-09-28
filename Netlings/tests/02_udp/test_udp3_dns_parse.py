import socket
import struct
import threading
import time

import pytest

from studylings.probe import run


def wire(name: str) -> bytes:
    """参考实现：点分名字 → DNS wire 格式。"""
    out = b""
    for label in name.rstrip(".").split("."):
        out += bytes([len(label)]) + label.encode()
    return out + b"\x00"


def rr(name: bytes, rtype: int, ttl: int, rdata: bytes) -> bytes:
    return name + struct.pack("!HHIH", rtype, 1, ttl, len(rdata)) + rdata


def ptr(off: int) -> bytes:
    return struct.pack("!H", 0xC000 | off)


def response(qid: int, question: bytes, answers: list[bytes], flags=0x8180) -> bytes:
    return struct.pack("!HHHHHH", qid, flags, 1, len(answers), 0, 0) + question + b"".join(answers)


class FakeDns:
    """假的 DNS 服务器：校验收到的查询，然后调用 answer(qid, question) 得到要发回的若干个报文。"""

    def __init__(self, name: str, answer):
        self.expect_qname = wire(name)
        self.answer = answer
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.settimeout(0.1)
        self.port = self.sock.getsockname()[1]
        self.queries: list[bytes] = []
        self.errors: list[str] = []
        self._stop = threading.Event()
        self.t = threading.Thread(target=self._serve, daemon=True)
        self.t.start()

    def _check(self, q: bytes) -> list[str]:
        errs = []
        if len(q) < 12 + 1 + 4:
            return [f"查询报文太短（{len(q)} 字节）"]
        qid, flags, qd, an, ns, ar = struct.unpack("!HHHHHH", q[:12])
        if flags != 0x0100:
            errs.append(f"FLAGS 应为 0x0100（QR=0, OPCODE=0, RD=1），实际 0x{flags:04x}")
        if (qd, an, ns, ar) != (1, 0, 0, 0):
            errs.append(f"计数应为 QD=1 AN=0 NS=0 AR=0，实际 {qd} {an} {ns} {ar}")
        qn = q[12:12 + len(self.expect_qname)]
        if qn != self.expect_qname:
            errs.append(f"QNAME 编码错误：期望 {self.expect_qname!r}，实际 {q[12:-4]!r}")
        elif q[12 + len(qn):] != struct.pack("!HH", 1, 1):
            errs.append(f"QNAME 之后应恰好是 QTYPE=1 QCLASS=1（00 01 00 01），实际 {q[12 + len(qn):]!r}")
        return errs

    def _serve(self):
        while not self._stop.is_set():
            try:
                q, peer = self.sock.recvfrom(4096)
            except socket.timeout:
                continue
            except OSError:
                return
            self.queries.append(q)
            errs = self._check(q)
            qid = struct.unpack("!H", q[:2])[0] if len(q) >= 2 else 0
            if errs:
                self.errors += errs
                self.sock.sendto(struct.pack("!HHHHHH", qid, 0x8181, 0, 0, 0, 0), peer)  # FORMERR
                continue
            for pkt in self.answer(qid, q[12:]):
                self.sock.sendto(pkt, peer)

    def close(self):
        self._stop.set()
        self.t.join(timeout=5)
        self.sock.close()


def ask(exe, name: str, answer):
    srv = FakeDns(name, answer)
    try:
        r = run(exe, srv.port, name, timeout=10)
    finally:
        srv.close()
    if srv.errors:
        pytest.fail("假 DNS 服务器认为你的查询报文不对：\n  " + "\n  ".join(srv.errors), pytrace=False)
    return r, srv


def expect_output(r, want: str, what: str):
    if r.returncode != 0 or r.stdout != want:
        pytest.fail(f"{what}\n期望 stdout:\n{want}实际 exit {r.returncode}, stdout:\n{r.stdout}\n"
                    f"--- stderr ---\n{r.stderr}", pytrace=False)


def cname_then_two_a(qid, question):
    """CNAME www → edge.<qname>，然后两条 A 记录，owner 名字是指向 CNAME 目标的指针（指针套指针）。"""
    base = 12 + len(question)
    cname_rdata_off = base + 2 + 10  # CNAME 的 NAME(2 字节指针) + TYPE/CLASS/TTL/RDLENGTH(10)
    answers = [
        rr(ptr(12), 5, 300, b"\x04edge" + ptr(12)),
        rr(ptr(cname_rdata_off), 1, 60, socket.inet_aton("192.0.2.10")),
        rr(ptr(cname_rdata_off), 1, 3600, socket.inet_aton("198.51.100.7")),
    ]
    return [response(qid, question, answers)]


def test_cname_and_compressed_a_records(exe):
    r, srv = ask(exe, "www.example.test", cname_then_two_a)
    expect_output(r, "A 192.0.2.10 ttl=60\nA 198.51.100.7 ttl=3600\n",
                  "应跳过 CNAME 并打印两条 A 记录（名字都是压缩指针，指针指向的名字里还有指针）")


def test_trailing_dot_and_case(exe):
    def answer(qid, question):
        return [response(qid, question, [rr(ptr(12), 1, 86400, socket.inet_aton("10.1.2.3"))])]

    r, _ = ask(exe, "Api.Service.Internal.", answer)
    expect_output(r, "A 10.1.2.3 ttl=86400\n", "名字末尾的 '.' 不应编码成空 label；大小写原样保留")


def test_ignores_reply_with_wrong_id(exe):
    def answer(qid, question):
        forged = response(qid ^ 0x5A5A, question, [rr(ptr(12), 1, 1, socket.inet_aton("6.6.6.6"))])
        real = response(qid, question, [rr(ptr(12), 1, 120, socket.inet_aton("203.0.113.5"))])
        return [forged, real]

    r, _ = ask(exe, "bank.example.test", answer)
    expect_output(r, "A 203.0.113.5 ttl=120\n", "ID 不匹配的响应（伪造的）必须丢弃并继续等待真正的响应")


def test_ignores_out_of_bailiwick_records(exe):
    def answer(qid, question):
        return [response(qid, question, [
            rr(wire("evil.test"), 1, 999, socket.inet_aton("6.6.6.6")),
            rr(ptr(12), 1, 30, socket.inet_aton("192.0.2.99")),
        ])]

    r, _ = ask(exe, "shop.example.test", answer)
    expect_output(r, "A 192.0.2.99 ttl=30\n",
                  "owner 名字与查询名字（及其 CNAME 链）无关的 A 记录必须忽略（要真正解析出 owner 名字来比较）")


@pytest.mark.parametrize("kind", ["self_loop", "mutual_loop", "rdata_overflow", "truncated_rr"])
def test_malformed_reply_is_rejected(exe, kind):
    def answer(qid, question):
        base = 12 + len(question)
        if kind == "self_loop":
            answers = [rr(ptr(base), 1, 1, socket.inet_aton("1.1.1.1"))]
        elif kind == "mutual_loop":
            # 第一条记录的名字指向第二条记录的名字，第二条又指回第一条
            second = base + 2 + 10 + 4
            answers = [rr(ptr(second), 1, 1, socket.inet_aton("1.1.1.1")),
                       rr(ptr(base), 1, 1, socket.inet_aton("2.2.2.2"))]
        elif kind == "rdata_overflow":
            answers = [ptr(12) + struct.pack("!HHIH", 1, 1, 1, 4000) + b"\x01\x02\x03\x04"]
        else:
            answers = [ptr(12) + struct.pack("!HH", 1, 1)]
        return [response(qid, question, answers)]

    t0 = time.monotonic()
    r, _ = ask(exe, "loop.example.test", answer)
    elapsed = time.monotonic() - t0
    assert r.returncode == 1, (
        f"畸形响应（{kind}）应报错并 exit 1，实际 exit {r.returncode}"
        f"{'（ASan 报告了越界访问！）' if r.returncode == 23 else ''}\nstdout: {r.stdout}\nstderr: {r.stderr}")
    assert "1.1.1.1" not in r.stdout and elapsed < 8, "不应从畸形报文里打印出记录"


@pytest.mark.parametrize("bad", ["a" * 64 + ".example.test", "a..b.test", "x." * 130 + "test"])
def test_invalid_names_are_rejected_locally(exe, bad):
    srv = FakeDns("unused.test", lambda qid, q: [])
    try:
        r = run(exe, srv.port, bad, timeout=10)
        time.sleep(0.2)
    finally:
        srv.close()
    assert r.returncode == 1, f"非法名字 {bad[:30]!r}… 应 exit 1，实际 exit {r.returncode}\nstderr: {r.stderr}"
    assert not srv.queries, "非法名字（label > 63、空 label、总长 > 255）不应发出查询"
