#!/usr/bin/env bash
# Netlings environment report — run on the target machine (ideally as root) and paste the output
# into the Claude Code session. Read-only: it changes nothing.
#
#   sudo -E Netlings/tools/hwcheck.sh            # NETLINGS_IFACE / NETLINGS_RDMA_DEV honoured if set

set -u
ok()   { printf '  [ok]   %s\n' "$*"; }
warn() { printf '  [--]   %s\n' "$*"; }
hdr()  { printf '\n== %s ==\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

hdr "System"
echo "  kernel: $(uname -r)   arch: $(uname -m)   euid: $(id -u)"
[ -r /etc/os-release ] && echo "  os: $(. /etc/os-release; echo "$PRETTY_NAME")"
echo "  cpus: $(nproc)   numa nodes: $(ls -d /sys/devices/system/node/node* 2>/dev/null | wc -l)"

hdr "Toolchain"
for t in gcc clang cmake ninja python3 pytest strace bpftool bpftrace ethtool ip tc iperf3 ib_write_bw rdma ibv_devinfo; do
  case $t in ip|tc) vf=-V ;; ibv_devinfo) vf=-l ;; *) vf=--version ;; esac
  if have "$t"; then ok "$t: $("$t" $vf 2>&1 | head -1)"; else warn "$t missing"; fi
done
for h in liburing.h bpf/libbpf.h infiniband/verbs.h rdma/rdma_cma.h; do
  [ -e "/usr/include/$h" ] && ok "header $h" || warn "header $h missing"
done
have pkg-config && for p in liburing libbpf libibverbs librdmacm; do
  v=$(pkg-config --modversion "$p" 2>/dev/null) && ok "$p $v" || warn "pkg-config $p missing"
done

hdr "Kernel features"
cfg() { { zcat /proc/config.gz 2>/dev/null || cat "/boot/config-$(uname -r)" 2>/dev/null; } | grep -E "^$1=" | head -1; }
for c in CONFIG_IO_URING CONFIG_BPF_SYSCALL CONFIG_BPF_JIT CONFIG_DEBUG_INFO_BTF CONFIG_XDP_SOCKETS \
         CONFIG_NET_SCH_NETEM CONFIG_NET_SCH_FQ CONFIG_NET_SCH_TBF CONFIG_NET_CLS_BPF CONFIG_TCP_CONG_BBR \
         CONFIG_MLX5_CORE CONFIG_MLX5_CORE_EN CONFIG_MLX5_INFINIBAND CONFIG_RDMA_RXE CONFIG_INFINIBAND_USER_ACCESS; do
  v=$(cfg "$c"); [ -n "$v" ] && ok "$v" || warn "$c not found (not set, or config unavailable)"
done
[ -r /proc/sys/kernel/io_uring_disabled ] && echo "  kernel.io_uring_disabled = $(cat /proc/sys/kernel/io_uring_disabled) (0 = enabled)"
echo "  tcp congestion available: $(cat /proc/sys/net/ipv4/tcp_available_congestion_control)"
echo "  unprivileged userns: $(cat /proc/sys/kernel/unprivileged_userns_clone 2>/dev/null || echo n/a)" \
     " apparmor_restrict_unprivileged_userns: $(cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns 2>/dev/null || echo n/a)"
[ -d /sys/kernel/tracing/events ] && ok "tracefs mounted" || warn "tracefs not mounted (mount -t tracefs tracefs /sys/kernel/tracing)"
[ -r /sys/kernel/btf/vmlinux ] && ok "BTF /sys/kernel/btf/vmlinux" || warn "no kernel BTF"
if [ "$(id -u)" = 0 ] && have ip && have tc; then
  ns=slhw$$; ip netns add $ns 2>/dev/null
  for q in netem fq tbf htb fq_codel; do
    extra=""; [ $q = tbf ] && extra="rate 1mbit burst 32kbit latency 50ms"; [ $q = htb ] && extra="default 1"
    if ip netns exec $ns tc qdisc add dev lo root $q $extra 2>/dev/null; then ok "qdisc $q"; ip netns exec $ns tc qdisc del dev lo root 2>/dev/null
    else warn "qdisc $q unavailable (modprobe sch_$q)"; fi
  done
  ip netns del $ns 2>/dev/null
else
  warn "not root: skipped netns/qdisc checks"
fi

hdr "Network interfaces"
for d in /sys/class/net/*; do
  n=$(basename "$d"); [ "$n" = lo ] && continue
  drv=$(basename "$(readlink -f "$d/device/driver" 2>/dev/null)" 2>/dev/null)
  printf '  %-18s driver=%-12s mtu=%-5s state=%-5s speed=%s numa=%s\n' "$n" "${drv:-virtual}" \
    "$(cat "$d/mtu")" "$(cat "$d/operstate")" "$(cat "$d/speed" 2>/dev/null || echo ?)" \
    "$(cat "$d/device/numa_node" 2>/dev/null || echo -)"
done
IFACE=${NETLINGS_IFACE:-$(for d in /sys/class/net/*; do [ "$(basename "$(readlink -f "$d/device/driver" 2>/dev/null)")" = mlx5_core ] && basename "$d" && break; done)}
if [ -n "${IFACE:-}" ] && [ -e "/sys/class/net/$IFACE" ]; then
  hdr "ConnectX / $IFACE"
  have ethtool && { ethtool -i "$IFACE" | sed 's/^/  /'; ethtool "$IFACE" 2>/dev/null | grep -E "Speed|Duplex|Link detected" | sed 's/^/  /';
                    ethtool -l "$IFACE" 2>/dev/null | sed 's/^/  /'; ethtool -g "$IFACE" 2>/dev/null | sed 's/^/  /';
                    ethtool -k "$IFACE" 2>/dev/null | grep -E "^(tcp-segmentation-offload|generic-receive-offload|large-receive-offload|rx-gro-hw|rx-checksumming|tx-checksumming):" | sed 's/^/  /'; }
  echo "  local_cpulist: $(cat /sys/class/net/$IFACE/device/local_cpulist 2>/dev/null)"
  echo "  IRQs: $(grep -c -E "mlx5_comp|$IFACE" /proc/interrupts) lines in /proc/interrupts"
  have mlnx_qos && mlnx_qos -i "$IFACE" 2>/dev/null | head -20 | sed 's/^/  /'
  echo "  export NETLINGS_IFACE=$IFACE"
else
  warn "no mlx5_core netdev found (set NETLINGS_IFACE)"
fi

hdr "RDMA"
if have rdma; then rdma link show 2>&1 | sed 's/^/  /'; fi
if have ibv_devinfo; then ibv_devinfo -l 2>&1 | sed 's/^/  /'; fi
for dev in /sys/class/infiniband/*; do
  [ -e "$dev" ] || { warn "no RDMA devices (modprobe rdma_rxe; rdma link add rxe0 type rxe netdev <iface>)"; break; }
  dn=$(basename "$dev")
  for p in "$dev"/ports/*; do
    echo "  $dn port $(basename "$p"): state=$(cat "$p/state") link_layer=$(cat "$p/link_layer" 2>/dev/null)"
    for t in "$p"/gid_attrs/types/*; do
      ty=$(cat "$t" 2>/dev/null) || continue; i=$(basename "$t"); gid=$(cat "$p/gids/$i")
      [ "$gid" = "0000:0000:0000:0000:0000:0000:0000:0000" ] && continue
      echo "    gid[$i] $gid  $ty"
    done
  done
  echo "  export NETLINGS_RDMA_DEV=$dn"
done
echo
echo "Env: NETLINGS_IFACE=${NETLINGS_IFACE:-} NETLINGS_PEER_IP=${NETLINGS_PEER_IP:-} NETLINGS_RDMA_DEV=${NETLINGS_RDMA_DEV:-} NETLINGS_RDMA_GID_INDEX=${NETLINGS_RDMA_GID_INDEX:-}"
