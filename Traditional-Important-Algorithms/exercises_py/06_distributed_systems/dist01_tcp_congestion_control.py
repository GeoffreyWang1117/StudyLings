# I AM NOT DONE

"""
dist01_tcp_congestion_control.py

TCP Congestion Control is fundamental to Internet reliability. It prevents
network congestion by adapting the transmission rate based on network conditions.

Key algorithms:
- Slow Start: Exponentially increase congestion window until threshold
- Congestion Avoidance: Linearly increase window after threshold
- AIMD (Additive Increase Multiplicative Decrease): Core fairness mechanism
- Fast Recovery: Respond to packet loss without going back to slow start

Your task: Implement a TCP congestion control simulator using AIMD strategy.

Key concepts:
- Congestion Window (cwnd): How many packets can be in flight
- Slow Start Threshold (ssthresh): Switch point between slow start and congestion avoidance
- RTT (Round Trip Time): Time for packet to reach destination and acknowledgment to return
- Packet loss detection: Timeout or duplicate ACKs
"""

from enum import Enum, auto
from dataclasses import dataclass
import unittest


class CongestionState(Enum):
    """TCP congestion control states."""
    SLOW_START = auto()
    CONGESTION_AVOIDANCE = auto()
    FAST_RECOVERY = auto()


class Event(Enum):
    """Events that can occur during TCP transmission."""
    ACK_RECEIVED = auto()   # Successful acknowledgment
    PACKET_LOSS = auto()    # Packet loss detected (3 duplicate ACKs)
    TIMEOUT = auto()        # Timeout occurred


@dataclass
class CongestionStats:
    """Statistics for TCP congestion control."""
    packets_sent: int
    packets_acked: int
    packets_lost: int
    current_cwnd: float
    current_ssthresh: float
    state: CongestionState


class TcpCongestionControl:
    """TCP congestion control using AIMD."""

    def __init__(self, initial_cwnd: float, initial_ssthresh: float, rtt: int):
        """Initialize TCP congestion control."""
        self.cwnd = initial_cwnd
        self.ssthresh = initial_ssthresh
        self.state = CongestionState.SLOW_START
        self.rtt = rtt
        self.packets_sent = 0
        self.packets_acked = 0
        self.packets_lost = 0
        self.duplicate_acks = 0

    def handle_ack(self):
        """
        TODO: Handle ACK reception.

        - In SLOW_START: Increase cwnd by 1 (exponential growth)
        - In CONGESTION_AVOIDANCE: Increase cwnd by 1/cwnd (linear growth)
        - In FAST_RECOVERY: Move to CONGESTION_AVOIDANCE and set cwnd to ssthresh
        - Update packets_acked counter
        - Check if we should transition from SLOW_START to CONGESTION_AVOIDANCE
        """
        pass  # TODO: Implement this

    def handle_packet_loss(self):
        """
        TODO: Handle packet loss (3 duplicate ACKs).

        - Set ssthresh to max(cwnd / 2, 2)
        - Set cwnd to ssthresh + 3 (for the 3 duplicate ACKs)
        - Enter FAST_RECOVERY state
        - Increment packets_lost counter
        """
        pass  # TODO: Implement this

    def handle_timeout(self):
        """
        TODO: Handle timeout (more severe than packet loss).

        - Set ssthresh to max(cwnd / 2, 2)
        - Set cwnd back to initial value (usually 1)
        - Enter SLOW_START state
        - Increment packets_lost counter
        """
        pass  # TODO: Implement this

    def process_event(self, event: Event):
        """Process an event."""
        if event == Event.ACK_RECEIVED:
            self.handle_ack()
        elif event == Event.PACKET_LOSS:
            self.handle_packet_loss()
        elif event == Event.TIMEOUT:
            self.handle_timeout()

    def send_packets(self) -> int:
        """
        TODO: Return how many packets can be sent based on current cwnd.

        Update packets_sent counter.
        Return the number of packets that can be sent (floor of cwnd).
        """
        pass  # TODO: Implement this

    def get_cwnd(self) -> float:
        """Get current congestion window."""
        return self.cwnd

    def get_ssthresh(self) -> float:
        """Get current slow start threshold."""
        return self.ssthresh

    def get_state(self) -> CongestionState:
        """Get current state."""
        return self.state

    def get_stats(self) -> CongestionStats:
        """Get current statistics."""
        return CongestionStats(
            packets_sent=self.packets_sent,
            packets_acked=self.packets_acked,
            packets_lost=self.packets_lost,
            current_cwnd=self.cwnd,
            current_ssthresh=self.ssthresh,
            state=self.state
        )


# Unit Tests
class TestTcpCongestionControl(unittest.TestCase):

    def test_initial_state(self):
        tcp = TcpCongestionControl(1.0, 16.0, 100)
        self.assertEqual(tcp.get_cwnd(), 1.0)
        self.assertEqual(tcp.get_ssthresh(), 16.0)
        self.assertEqual(tcp.get_state(), CongestionState.SLOW_START)

    def test_slow_start_exponential_growth(self):
        tcp = TcpCongestionControl(1.0, 16.0, 100)

        # In slow start, each ACK increases cwnd by 1
        tcp.handle_ack()
        self.assertEqual(tcp.get_cwnd(), 2.0)

        tcp.handle_ack()
        self.assertEqual(tcp.get_cwnd(), 3.0)

        tcp.handle_ack()
        self.assertEqual(tcp.get_cwnd(), 4.0)

    def test_transition_to_congestion_avoidance(self):
        tcp = TcpCongestionControl(1.0, 4.0, 100)

        # Grow until we hit ssthresh
        for _ in range(3):
            tcp.handle_ack()

        self.assertEqual(tcp.get_cwnd(), 4.0)
        self.assertEqual(tcp.get_state(), CongestionState.CONGESTION_AVOIDANCE)

    def test_congestion_avoidance_linear_growth(self):
        tcp = TcpCongestionControl(4.0, 4.0, 100)
        tcp.state = CongestionState.CONGESTION_AVOIDANCE

        # In congestion avoidance, increase by 1/cwnd per ACK
        tcp.handle_ack()
        self.assertEqual(tcp.get_cwnd(), 4.25)  # 4 + 1/4

        tcp.handle_ack()
        self.assertAlmostEqual(tcp.get_cwnd(), 4.4705882, places=5)

    def test_packet_loss_response(self):
        tcp = TcpCongestionControl(16.0, 32.0, 100)
        tcp.state = CongestionState.CONGESTION_AVOIDANCE

        tcp.handle_packet_loss()

        # ssthresh should be cwnd/2 = 8
        self.assertEqual(tcp.get_ssthresh(), 8.0)
        # cwnd should be ssthresh + 3 = 11
        self.assertEqual(tcp.get_cwnd(), 11.0)
        self.assertEqual(tcp.get_state(), CongestionState.FAST_RECOVERY)

    def test_timeout_response(self):
        tcp = TcpCongestionControl(20.0, 32.0, 100)
        tcp.state = CongestionState.CONGESTION_AVOIDANCE

        tcp.handle_timeout()

        # ssthresh should be cwnd/2 = 10
        self.assertEqual(tcp.get_ssthresh(), 10.0)
        # cwnd should reset to 1
        self.assertEqual(tcp.get_cwnd(), 1.0)
        self.assertEqual(tcp.get_state(), CongestionState.SLOW_START)

    def test_fast_recovery_to_congestion_avoidance(self):
        tcp = TcpCongestionControl(16.0, 32.0, 100)

        # Trigger fast recovery
        tcp.handle_packet_loss()
        self.assertEqual(tcp.get_state(), CongestionState.FAST_RECOVERY)

        # ACK should move to congestion avoidance
        tcp.handle_ack()
        self.assertEqual(tcp.get_state(), CongestionState.CONGESTION_AVOIDANCE)
        self.assertEqual(tcp.get_cwnd(), tcp.get_ssthresh())

    def test_minimum_ssthresh(self):
        tcp = TcpCongestionControl(2.0, 16.0, 100)

        tcp.handle_timeout()

        # ssthresh should be max(cwnd/2, 2) = max(1, 2) = 2
        self.assertEqual(tcp.get_ssthresh(), 2.0)

    def test_event_processing(self):
        tcp = TcpCongestionControl(1.0, 16.0, 100)

        tcp.process_event(Event.ACK_RECEIVED)
        self.assertEqual(tcp.get_cwnd(), 2.0)

        tcp.process_event(Event.TIMEOUT)
        self.assertEqual(tcp.get_cwnd(), 1.0)

    def test_statistics_tracking(self):
        tcp = TcpCongestionControl(1.0, 16.0, 100)

        tcp.handle_ack()
        tcp.handle_ack()
        tcp.handle_packet_loss()

        stats = tcp.get_stats()
        self.assertEqual(stats.packets_acked, 2)
        self.assertEqual(stats.packets_lost, 1)

    def test_send_packets(self):
        tcp = TcpCongestionControl(5.7, 16.0, 100)

        packets = tcp.send_packets()
        self.assertEqual(packets, 5)  # Floor of 5.7

        stats = tcp.get_stats()
        self.assertEqual(stats.packets_sent, 5)


if __name__ == '__main__':
    unittest.main()
