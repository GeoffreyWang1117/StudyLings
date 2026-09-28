"""本章（eBPF / XDP）共享的 fixture。

- `netlab`：studylings.netlab 的 netns + veth 实验台（需要 root，否则整个测试 skip）。
- `bpf_root`：不用 netlab 的测试（如 tracepoint）用它检查 root。
加载 BPF 程序需要 CAP_BPF + CAP_NET_ADMIN / CAP_PERFMON，本章统一要求 root：
    sudo -E python -m netlings run <题目>
"""
import os

import pytest

from studylings.netlab import netlab  # noqa: F401  (re-export fixture)


@pytest.fixture
def bpf_root():
    if os.geteuid() != 0:
        pytest.skip("加载 BPF 程序需要 root（CAP_BPF/CAP_PERFMON）：sudo -E python -m netlings run <题目>")
