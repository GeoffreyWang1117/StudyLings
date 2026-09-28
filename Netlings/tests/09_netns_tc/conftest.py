"""09_netns_tc 共享工具。

- `netlab` / `has_qdisc`：见 studylings/netlab.py（需要 root；否则自动 skip）。
- `nobody_exe`：以 root 运行探针时，把被测程序复制到一个所有人可读的临时目录，返回
  (argv 前缀, 程序路径)，用 `setpriv` 降权成 nobody 来证明它真的是 rootless 的。
"""
import os
import shutil
import tempfile

import pytest

from studylings.netlab import has_qdisc, netlab  # noqa: F401  (re-export fixture)


@pytest.fixture
def nobody_exe(exe):
    if os.geteuid() != 0:
        pytest.skip("本用例需要 root 才能降权成 nobody 来验证 rootless（普通用户运行时上面的用例已经是 rootless）")
    if shutil.which("setpriv") is None:
        pytest.skip("需要 setpriv（util-linux）")
    d = tempfile.mkdtemp(prefix="sl-nobody-")
    try:
        os.chmod(d, 0o755)
        dst = os.path.join(d, exe.name)
        shutil.copy2(exe, dst)
        os.chmod(dst, 0o755)
        yield ["setpriv", "--reuid=65534", "--regid=65534", "--clear-groups"], dst
    finally:
        shutil.rmtree(d, ignore_errors=True)


CLI_IP, SRV_IP = "10.9.0.1", "10.9.0.2"


@pytest.fixture
def pair(netlab):
    """两个 netns（cli、srv）之间一条 veth：cli 10.9.0.1/24 —— srv 10.9.0.2/24。
    返回 (netlab, cli, srv, cli 端网卡名)。服务器地址是 10.9.0.2。"""
    cli, srv = netlab.ns("cli"), netlab.ns("srv")
    netlab.link(cli, srv, f"{CLI_IP}/24", f"{SRV_IP}/24")
    return netlab, cli, srv, netlab.dev(cli, srv)


@pytest.fixture
def need_netem():
    if not has_qdisc("netem"):
        pytest.skip("内核没有 sch_netem（这台验证机就没有）。在真实机器上：sudo modprobe sch_netem "
                    "（Ubuntu 可能需要 apt install linux-modules-extra-$(uname -r)）后重跑")
