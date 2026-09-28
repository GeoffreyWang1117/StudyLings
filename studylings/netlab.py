"""
Network namespace lab for Netlings probes (N09+): build small topologies out of netns + veth,
shape links with tc, and run the learner's binary inside a namespace.

    from studylings.netlab import netlab   # pytest fixture

    def test_x(exe, netlab):
        a, b = netlab.ns("client"), netlab.ns("server")
        netlab.link(a, b, "10.10.0.1/24", "10.10.0.2/24")
        netlab.qdisc(a, netlab.dev(a, b), "tbf rate 50mbit burst 32kbit latency 50ms")
        with netlab.start(b, exe, "server") as srv: ...

Needs root (or CAP_NET_ADMIN + CAP_SYS_ADMIN): uses `ip netns`, which bind-mounts under /run/netns.
Without it every test using the fixture is skipped with an explanation.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import uuid
from typing import Optional

import pytest

from .probe import Proc, sanitizer_env

__all__ = ["NetLab", "netlab", "has_qdisc"]


def _ip(*args, check=True) -> subprocess.CompletedProcess:
    r = subprocess.run(["ip", *map(str, args)], capture_output=True, text=True, timeout=20)
    if check and r.returncode != 0:
        pytest.fail(f"ip {' '.join(map(str, args))} 失败: {r.stderr.strip()}", pytrace=False)
    return r


class NetLab:
    def __init__(self):
        self.tag = uuid.uuid4().hex[:6]
        self.namespaces: list[str] = []
        self._links: dict[tuple[str, str], str] = {}
        self._n = 0

    # --- topology -------------------------------------------------------------------------
    def ns(self, role: str) -> str:
        name = f"sl{self.tag}{role}"[:15]
        _ip("netns", "add", name)
        self.namespaces.append(name)
        _ip("-n", name, "link", "set", "lo", "up")
        return name

    def link(self, a: str, b: str, addr_a: Optional[str] = None, addr_b: Optional[str] = None,
             mtu: Optional[int] = None) -> tuple[str, str]:
        """veth pair between namespaces a and b. Returns (dev in a, dev in b)."""
        self._n += 1
        dev_a, dev_b = f"v{self._n}a{self.tag}"[:15], f"v{self._n}b{self.tag}"[:15]
        _ip("link", "add", dev_a, "netns", a, "type", "veth", "peer", "name", dev_b, "netns", b)
        for ns, dev, addr in ((a, dev_a, addr_a), (b, dev_b, addr_b)):
            if addr:
                _ip("-n", ns, "addr", "add", addr, "dev", dev)
            if mtu:
                _ip("-n", ns, "link", "set", dev, "mtu", mtu)
            _ip("-n", ns, "link", "set", dev, "up")
        self._links[(a, b)] = dev_a
        self._links[(b, a)] = dev_b
        return dev_a, dev_b

    def dev(self, ns: str, peer: str) -> str:
        """Name of the device in `ns` that faces `peer`."""
        return self._links[(ns, peer)]

    def route(self, ns: str, dst: str, via: str):
        _ip("-n", ns, "route", "add", dst, "via", via)

    def forwarding(self, ns: str):
        self.run(ns, "sysctl", "-qw", "net.ipv4.ip_forward=1")

    def qdisc(self, ns: str, dev: str, spec: str):
        r = self.run(ns, "tc", "qdisc", "replace", "dev", dev, "root", *spec.split(), check=False)
        if r.returncode != 0:
            kind = spec.split()[0]
            pytest.skip(f"内核不支持 tc qdisc '{kind}'（{r.stderr.strip()}）；在真实机器上 modprobe sch_{kind}")

    # --- running things -------------------------------------------------------------------
    def run(self, ns: str, *argv, check: bool = True, timeout: float = 30, input=None,
            env: Optional[dict] = None) -> subprocess.CompletedProcess:
        text = not isinstance(input, bytes)
        r = subprocess.run(["ip", "netns", "exec", ns, *map(str, argv)], capture_output=True,
                           text=text, errors="replace" if text else None, timeout=timeout,
                           input=input, env=sanitizer_env(env))
        if check and r.returncode != 0:
            pytest.fail(f"[{ns}] {' '.join(map(str, argv))} 退出码 {r.returncode}\n"
                        f"stdout: {r.stdout}\nstderr: {r.stderr}", pytrace=False)
        return r

    def start(self, ns: str, exe, *args, env: Optional[dict] = None) -> Proc:
        return Proc("ip", "netns", "exec", ns, str(exe), *args, env=env)

    def close(self):
        for ns in reversed(self.namespaces):
            _ip("netns", "del", ns, check=False)


def _lab_available() -> Optional[str]:
    if shutil.which("ip") is None:
        return "需要 iproute2（apt install iproute2）"
    if os.geteuid() != 0:
        return "需要 root 才能创建 network namespace：sudo -E python -m netlings run <题目>"
    return None


_QDISC_MIN_ARGS = {"tbf": "rate 1mbit burst 32kbit latency 50ms", "htb": "default 1"}


def has_qdisc(kind: str) -> bool:
    """Whether the running kernel has a given qdisc (e.g. netem), tested in a throwaway netns."""
    if _lab_available():
        return False
    lab = NetLab()
    try:
        ns = lab.ns("q")
        r = lab.run(ns, "tc", "qdisc", "add", "dev", "lo", "root", kind,
                    *_QDISC_MIN_ARGS.get(kind, "").split(), check=False)
        return r.returncode == 0
    finally:
        lab.close()


@pytest.fixture
def netlab():
    why = _lab_available()
    if why:
        pytest.skip(why)
    lab = NetLab()
    try:
        yield lab
    finally:
        lab.close()
