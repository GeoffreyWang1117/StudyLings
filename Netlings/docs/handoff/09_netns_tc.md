# 09_netns_tc — handoff for the real machine

Exercises: `ns1_unshare_net`, `ns2_rtnetlink_veth`, `ns3_tcp_info`, `ns4_congestion_control`, `ns5_router_pmtu`.

## What was validated on the build box (kernel 6.18, root, no netem/fq)

| Probe | Result here |
|---|---|
| ns1 `test_private_netns_with_only_lo`, `test_really_rootless` (setpriv → nobody) | PASS |
| ns2 `test_udp_over_self_made_veth`, `..._as_nobody` | PASS |
| ns3 `test_tcp_info_under_tbf_bottleneck` | PASS (goodput ~47.8 Mbit/s, delivery ~42–48) |
| ns3 `test_rtt_reflects_netem_delay`, `test_retrans_reflects_netem_loss` | **SKIP (no sch_netem)** |
| ns4 `test_per_socket_algorithm[bbr/cubic]`, `test_unknown_algorithm_reports_enoent`, `test_goodput_under_tbf[bbr/cubic]` | PASS |
| ns4 `test_bbr_beats_cubic_under_random_loss` | **SKIP (no sch_netem)** |
| ns5 `test_pmtu_discovery_through_router` | PASS (ICMP frag-needed reaches the client; route cache shows `mtu 1400`) |

The veth/tbf probes need root (`netlab` fixture). ns1/ns2 work without root, but they need unprivileged
user namespaces to be allowed.

## Checklist on the real machine

- [ ] Load netem: `sudo modprobe sch_netem`. If the module is missing: `sudo apt install linux-modules-extra-$(uname -r)`.
      Check: `sudo tc qdisc add dev lo root netem delay 1ms && sudo tc qdisc del dev lo root`.
- [ ] Make sure bbr is available: `sudo modprobe tcp_bbr`. Check with `cat /proc/sys/net/ipv4/tcp_available_congestion_control`.
- [ ] Run as root: `sudo -E python -m pytest -q tests/09_netns_tc` against solutions
      (`SL_BUILD_DIR=build/solutions` or `STUDYLINGS_PRESET=solutions`). Everything should PASS with **0 skips**.
- [ ] ns3 `test_rtt_reflects_netem_delay`: `netem delay 40ms rate 50mbit limit 10000` goes on the client egress.
      Pass = the median `rtt_us` of the second half of the samples is >= 40000.
      Risk: none expected, because the RTT is the one-way netem delay plus ~0.1 ms.
- [ ] ns3 `test_retrans_reflects_netem_loss`: `netem delay 5ms loss 1% rate 100mbit`, 3 s. Pass = `retrans > 0`.
- [ ] ns4 `test_bbr_beats_cubic_under_random_loss`: `netem delay 20ms loss 1% rate 100mbit`, 5 s for each algorithm.
      Pass = bbr goodput > 1.5 × cubic goodput. By the Mathis formula, CUBIC should get about 7–15 Mbit/s and
      BBR about 80–95 Mbit/s. **If this flakes**, first check that netem `rate` is honoured. Then consider
      raising SECONDS, or putting netem on the server side instead (ACK path). Keep the ratio assertion; do
      not replace it with absolute numbers.
- [ ] ns1/ns2 as a normal user (no sudo): `python -m pytest -q tests/09_netns_tc/test_ns1_unshare_net.py tests/09_netns_tc/test_ns2_rtnetlink_veth.py`.
      On Ubuntu 24.04+ AppArmor blocks unprivileged userns. The programs then print `userns unavailable`
      and the probe SKIPs. Enable it with `sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`.
- [ ] Non-root ns4: `cubic` is often not in `tcp_allowed_congestion_control`, so the probe SKIPs that case
      (EPERM is the correct kernel behaviour). As root it runs.
- [ ] Optional: repeat the ns5 PMTU probe once with a firewall rule that drops ICMP on the router
      (`ip netns exec <rtr> iptables -A OUTPUT -p icmp --icmp-type fragmentation-needed -j DROP`).
      The client must then give up after about 5 s with `gave up after 25 timeouts`. This is the classic
      PMTU black hole, and RFC 8899 DPLPMTUD is the fix.

## Assumptions / known risks in the code

- ns3/ns4 use `<linux/tcp.h>` `struct tcp_info` (tcpi_delivery_rate needs kernel ≥ 4.9 and tcpi_bytes_acked ≥ 4.1). On an older kernel those fields read 0.
- ns3/ns4 goodput uses `tcpi_bytes_acked / elapsed`, measured at the end of the send window.
  tbf is `rate 50mbit burst 32kbit latency 50ms`. With GSO on veth, tbf segments oversized skbs. On the
  box the goodput was ~47.8. The assertion window is 30–60.
- The ns4 `ss -tin` cross-check parses the first word of the info line (the algorithm name). If a newer
  iproute2 changes the layout, the helper returns None and the check is skipped silently, never failed.
- The ns5 client starts with the chunk size for MTU 1500, and the netlab veth default MTU is 1500. If the
  real machine's default veth MTU differs, the first datagram still gets EMSGSIZE/ICMP handling. The
  probe asserts that `path_mtu == 1400` and that the route cache shows `mtu 1400`.
- ns2 uses the fixed names sl0/sl1, the fixed subnet 10.99.0.0/24 and UDP port 7777. All of them live in
  private namespaces, so they cannot collide.

## Suggested extra experiments (not probed)

1. **RTO backoff**: during an ns3 transfer, run `tc qdisc replace dev <cli-dev> root netem loss 100%` for
   10 s, then remove it. Watch `rtt_us`, `cwnd` and `retrans` in the ns3 samples, together with
   `ss -tin` `rto:` and `backoff:`. The RTO should double (200 ms → 400 → 800 …, capped at
   `tcp_retries2`), and cwnd should collapse to 1 and slow-start afterwards (TCP/IP Illustrated §14.3–14.5).
2. **Reordering**: `netem delay 10ms reorder 25% 50%`. Compare `tcpi_reordering` and `tcpi_total_retrans`
   (spurious retransmits), with `net.ipv4.tcp_recovery` (RACK) set to 1 and to 0.
3. **BBR vs CUBIC plot**: `iperf3 -s` in the server ns, and
   `iperf3 -c 10.9.0.2 -t 30 -J -C bbr > bbr.json` (same for `-C cubic`) under
   `netem delay 30ms rate 200mbit limit 2000`. Plot `intervals[].streams[].bits_per_second` and `snd_cwnd`/`rtt`.
   Then add `loss 0.5%`, and try a shallow buffer (`limit 100`) against a deep one (`limit 10000`) to
   see bufferbloat: CUBIC fills the queue and RTT balloons, while BBR keeps the RTT near min_rtt.
4. **fq pacing**: on the real machine `modprobe sch_fq`, then `tc qdisc replace dev X root fq`, and compare
   BBR's `pacing_rate` and burstiness with and without fq (`tcpdump -ttt`).
5. **htb shaping + classes**: two flows in different htb classes (`htb rate 100mbit` with children of 70 and 30 mbit),
   and check that the per-flow goodput from ns3 follows the ratio. This is what Kubernetes bandwidth plugin / tc-based QoS does.
6. **ConnectX**: repeat ns4 across the 25GbE link (`NETLINGS_PEER_IP`) with an iperf3 server on the peer:
   BBR against CUBIC at line rate, and the impact of `tcp_wmem`/`tcp_rmem` limits on a high-BDP path
   (add `netem delay 20ms` on the NIC).
