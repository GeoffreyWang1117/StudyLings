import errno
import os
import socket

import pytest

from studylings.probe import assert_ok, free_port, run, start


def _reserve_port() -> socket.socket:
    """在宿主机 netns 里占住 127.0.0.1 上的一个端口（只 bind 不 listen）。"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    return s


def test_private_netns_with_only_lo(exe):
    holder = _reserve_port()
    port = holder.getsockname()[1]
    try:
        with start(exe, port) as p:
            try:
                first = p.expect(r"^(userns unavailable|self-connect ok|ready)", timeout=10)
            except pytest.fail.Exception as e:
                hint = ""
                if "Address already in use" in p.stderr:
                    hint = ("\n提示：探针在宿主机上占住了这个端口，bind 却报 EADDRINUSE —— "
                            "说明程序还在宿主机的 network namespace 里（unshare 没做？）")
                elif "connect 127.0.0.1" in p.stderr:
                    hint = "\n提示：新 netns 里的 lo 默认是 DOWN 的，要先 SIOCSIFFLAGS 加上 IFF_UP"
                pytest.fail(f"{e}{hint}", pytrace=False)
            if first.group(1) == "userns unavailable":
                p.wait()
                pytest.skip("系统禁用了非特权 user namespace（unshare 返回 EPERM）。"
                            "在真实机器上：sysctl -w kernel.apparmor_restrict_unprivileged_userns=0 "
                            "或 kernel.unprivileged_userns_clone=1，或以 root 运行")
            p.expect(r"^ready$", timeout=10)

            ifaces = [ln.split()[1] for ln in p.out if ln.startswith("if ")]
            assert ifaces, f"程序应为每个接口打印一行 'if <名字>'\n{p.describe()}"
            assert set(ifaces) == {"lo"}, (
                f"新的 network namespace 里应该只有 lo，实际看到 {ifaces} —— "
                f"是不是没有 unshare(CLONE_NEWNET)，看到的还是宿主机的接口？")

            ours = os.readlink("/proc/self/ns/net")
            theirs = os.readlink(f"/proc/{p.pid}/ns/net")
            assert ours != theirs, (f"程序的 netns ({theirs}) 与探针相同 —— 没有进入新的 network namespace")

            # 宿主机的 127.0.0.1:PORT 只被 bind、没有 listen → 连接必须被拒绝。
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.settimeout(5)
            try:
                rc = c.connect_ex(("127.0.0.1", port))
            finally:
                c.close()
            assert rc == errno.ECONNREFUSED, (
                f"从宿主机连接 127.0.0.1:{port} 应被拒绝（程序的监听 socket 在另一个协议栈里），"
                f"实际 connect 结果 errno={rc} ({os.strerror(rc) if rc else '连接成功'})")

            p.close_stdin()
            rc = p.wait(timeout=10)
            assert rc == 0, f"stdin EOF 后应 exit 0，实际 {rc}\n{p.describe()}"
    finally:
        holder.close()


def test_really_rootless(nobody_exe):
    """降权成 nobody（无任何 capability）后仍然能建出自己的 netns 并把 lo 拉起来。"""
    prefix, path = nobody_exe
    port = free_port()
    r = run(prefix[0], *prefix[1:], path, port, input="", timeout=15)
    if "userns unavailable" in r.stdout:
        pytest.skip("系统禁用了非特权 user namespace；真实机器上可用 "
                    "sysctl -w kernel.apparmor_restrict_unprivileged_userns=0 打开")
    assert_ok(r, "self-connect ok", what="以 nobody 身份运行")
    assert "ready" in r.stdout
    ifaces = {ln.split()[1] for ln in r.stdout.splitlines() if ln.startswith("if ")}
    assert ifaces == {"lo"}, f"以 nobody 运行时也应只看到 lo，实际 {sorted(ifaces)}（没进入新的 netns？）"
