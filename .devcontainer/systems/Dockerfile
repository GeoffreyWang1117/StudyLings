# Toolchain for Unixlings / Netlings: modern C + Linux observability + networking lab.
# Ubuntu 26.04 LTS ships GCC 15 (C23 by default), LLVM 21, CMake 4.x.
FROM ubuntu:26.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc g++ clang clangd clang-format clang-tidy lld \
        cmake ninja-build pkg-config ccache mold \
        gdb lldb valgrind strace ltrace linux-tools-generic bpftrace bpfcc-tools \
        liburing-dev libbpf-dev bpftool libelf-dev libcap-dev \
        iproute2 iputils-ping iperf3 ethtool tcpdump tshark netcat-openbsd socat nftables \
        rdma-core ibverbs-utils libibverbs-dev librdmacm-dev perftest \
        python3 python3-pip python3-venv python3-pytest python3-click python3-rich python3-watchdog \
        python3-scapy hyperfine \
        git curl ca-certificates sudo less man-db manpages-dev manpages-posix-dev \
    && rm -rf /var/lib/apt/lists/*

# man 2/3 pages are the primary documentation for these projects
RUN yes | unminimize >/dev/null 2>&1 || true
