"""
Project-specific configuration for Netlings (UNP modern edition → kernel-bypass networking).
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from studylings import ProjectConfig, ValidationMode

_project_root = Path(__file__).parent.parent

config = ProjectConfig(
    name="netlings",
    display_name="Netlings - UNP 现代版：socket → epoll → io_uring → eBPF → RDMA",
    version="0.1.0",
    validation_mode=ValidationMode.BUILD_AND_PROBE,
    exercises_dir="exercises",
    tests_dir="tests",
    solutions_dir="solutions",
    hints_dir="hints",
    project_root=_project_root,
    chapters={
        "01_tcp_sockets": "N01 TCP socket (UNP 4-7)",
        "02_udp": "N02 UDP (UNP 8, 11)",
        "03_select_poll": "N03 select / poll (UNP 6, 16)",
        "04_epoll": "N04 epoll 与事件循环",
        "05_unix_socket": "N05 Unix domain socket (UNP 15)",
        "06_mmap_shm": "N06 mmap 与共享内存",
        "07_pthread_sync": "N07 pthread 同步（服务器视角）",
        # Roadmap (see README): 08_io_uring, 09_netns_tc, 10_ebpf_xdp,
        # 11_connectx_25gbe, 12_rdma_roce
    },
    banner=r"""
    ███╗   ██╗███████╗████████╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗
    ████╗  ██║██╔════╝╚══██╔══╝██║     ██║████╗  ██║██╔════╝ ██╔════╝
    ██╔██╗ ██║█████╗     ██║   ██║     ██║██╔██╗ ██║██║  ███╗███████╗
    ██║╚██╗██║██╔══╝     ██║   ██║     ██║██║╚██╗██║██║   ██║╚════██║
    ██║ ╚████║███████╗   ██║   ███████╗██║██║ ╚████║╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

      socket → epoll → io_uring → netns/tc → eBPF/XDP → 25GbE → RDMA
    """,
    file_extension=".c",
    comment_prefix="//",
    todo_markers=["TODO:"],
    incomplete_markers=["I AM NOT DONE"],
    run_timeout=15,
)
