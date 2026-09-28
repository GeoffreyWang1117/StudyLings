import pytest

from studylings.probe import assert_ok, run

SKIP_USERNS = ("系统禁用了非特权 user namespace（unshare 返回 EPERM）。在真实机器上："
               "sysctl -w kernel.apparmor_restrict_unprivileged_userns=0，或以 root 运行")


def _check(r):
    if "userns unavailable" in r.stdout:
        pytest.skip(SKIP_USERNS)
    if "Function not implemented" in r.stderr:
        pytest.fail("nl_create_veth / nl_add_ipv4 / nl_link_up 还是占位实现（ENOSYS）。\n"
                    f"--- stderr ---\n{r.stderr}", pytrace=False)
    if "RTM_NEWLINK veth" in r.stderr:
        pytest.fail("内核拒绝了创建 veth 的 RTM_NEWLINK 请求 —— 检查嵌套属性的结构和长度"
                    "（VETH_INFO_PEER 的负载要先放一个 struct ifinfomsg；每个 nest 都要 nla_nest_end）。\n"
                    f"--- stderr ---\n{r.stderr}", pytrace=False)
    assert_ok(r, "udp over veth ok", what="veth 两端的 UDP 往返")


def test_udp_over_self_made_veth(exe):
    _check(run(exe, timeout=30))


def test_udp_over_self_made_veth_as_nobody(nobody_exe):
    """降权成 nobody 也能完成：CAP_NET_ADMIN 只在自己的 user namespace 里有效。"""
    prefix, path = nobody_exe
    _check(run(prefix[0], *prefix[1:], path, timeout=30))
