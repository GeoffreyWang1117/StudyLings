// dist01_tcp_congestion_control.rs
//
// TCP Congestion Control is fundamental to Internet reliability. It prevents
// network congestion by adapting the transmission rate based on network conditions.
//
// Key algorithms:
// - Slow Start: Exponentially increase congestion window until threshold
// - Congestion Avoidance: Linearly increase window after threshold
// - AIMD (Additive Increase Multiplicative Decrease): Core fairness mechanism
// - Fast Recovery: Respond to packet loss without going back to slow start
//
// Your task: Implement a TCP congestion control simulator using AIMD strategy.
//
// Key concepts:
// - Congestion Window (cwnd): How many packets can be in flight
// - Slow Start Threshold (ssthresh): Switch point between slow start and congestion avoidance
// - RTT (Round Trip Time): Time for packet to reach destination and acknowledgment to return
// - Packet loss detection: Timeout or duplicate ACKs

// I AM NOT DONE

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum CongestionState {
    SlowStart,
    CongestionAvoidance,
    FastRecovery,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Event {
    AckReceived,      // Successful acknowledgment
    PacketLoss,       // Packet loss detected (timeout or 3 duplicate ACKs)
    Timeout,          // Timeout occurred
}

pub struct TcpCongestionControl {
    cwnd: f64,                           // Congestion window (in packets)
    ssthresh: f64,                       // Slow start threshold
    state: CongestionState,
    rtt: u32,                            // Round trip time in ms
    packets_sent: usize,
    packets_acked: usize,
    packets_lost: usize,
    duplicate_acks: usize,
}

impl TcpCongestionControl {
    pub fn new(initial_cwnd: f64, initial_ssthresh: f64, rtt: u32) -> Self {
        Self {
            cwnd: initial_cwnd,
            ssthresh: initial_ssthresh,
            state: CongestionState::SlowStart,
            rtt,
            packets_sent: 0,
            packets_acked: 0,
            packets_lost: 0,
            duplicate_acks: 0,
        }
    }

    pub fn handle_ack(&mut self) {
        // TODO: Handle ACK reception
        // - In SlowStart: Increase cwnd by 1 (exponential growth)
        // - In CongestionAvoidance: Increase cwnd by 1/cwnd (linear growth)
        // - In FastRecovery: Move to CongestionAvoidance and set cwnd to ssthresh
        // - Update packets_acked counter
        // - Check if we should transition from SlowStart to CongestionAvoidance
        todo!()
    }

    pub fn handle_packet_loss(&mut self) {
        // TODO: Handle packet loss (3 duplicate ACKs)
        // - Set ssthresh to max(cwnd / 2, 2)
        // - Set cwnd to ssthresh + 3 (for the 3 duplicate ACKs)
        // - Enter FastRecovery state
        // - Increment packets_lost counter
        todo!()
    }

    pub fn handle_timeout(&mut self) {
        // TODO: Handle timeout (more severe than packet loss)
        // - Set ssthresh to max(cwnd / 2, 2)
        // - Set cwnd back to initial value (usually 1)
        // - Enter SlowStart state
        // - Increment packets_lost counter
        todo!()
    }

    pub fn process_event(&mut self, event: Event) {
        match event {
            Event::AckReceived => self.handle_ack(),
            Event::PacketLoss => self.handle_packet_loss(),
            Event::Timeout => self.handle_timeout(),
        }
    }

    pub fn send_packets(&mut self) -> usize {
        // TODO: Return how many packets can be sent based on current cwnd
        // Update packets_sent counter
        // Return the number of packets that can be sent (floor of cwnd)
        todo!()
    }

    pub fn get_cwnd(&self) -> f64 {
        self.cwnd
    }

    pub fn get_ssthresh(&self) -> f64 {
        self.ssthresh
    }

    pub fn get_state(&self) -> CongestionState {
        self.state
    }

    pub fn get_stats(&self) -> CongestionStats {
        CongestionStats {
            packets_sent: self.packets_sent,
            packets_acked: self.packets_acked,
            packets_lost: self.packets_lost,
            current_cwnd: self.cwnd,
            current_ssthresh: self.ssthresh,
            state: self.state,
        }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct CongestionStats {
    pub packets_sent: usize,
    pub packets_acked: usize,
    pub packets_lost: usize,
    pub current_cwnd: f64,
    pub current_ssthresh: f64,
    pub state: CongestionState,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_initial_state() {
        let tcp = TcpCongestionControl::new(1.0, 16.0, 100);
        assert_eq!(tcp.get_cwnd(), 1.0);
        assert_eq!(tcp.get_ssthresh(), 16.0);
        assert_eq!(tcp.get_state(), CongestionState::SlowStart);
    }

    #[test]
    fn test_slow_start_exponential_growth() {
        let mut tcp = TcpCongestionControl::new(1.0, 16.0, 100);

        // In slow start, each ACK increases cwnd by 1
        tcp.handle_ack();
        assert_eq!(tcp.get_cwnd(), 2.0);

        tcp.handle_ack();
        assert_eq!(tcp.get_cwnd(), 3.0);

        tcp.handle_ack();
        assert_eq!(tcp.get_cwnd(), 4.0);
    }

    #[test]
    fn test_transition_to_congestion_avoidance() {
        let mut tcp = TcpCongestionControl::new(1.0, 4.0, 100);

        // Grow until we hit ssthresh
        for _ in 0..3 {
            tcp.handle_ack();
        }

        assert_eq!(tcp.get_cwnd(), 4.0);
        assert_eq!(tcp.get_state(), CongestionState::CongestionAvoidance);
    }

    #[test]
    fn test_congestion_avoidance_linear_growth() {
        let mut tcp = TcpCongestionControl::new(4.0, 4.0, 100);
        tcp.state = CongestionState::CongestionAvoidance;

        // In congestion avoidance, increase by 1/cwnd per ACK
        tcp.handle_ack();
        assert_eq!(tcp.get_cwnd(), 4.25); // 4 + 1/4

        tcp.handle_ack();
        assert!((tcp.get_cwnd() - 4.4705882).abs() < 0.001); // Approximately 4 + 1/4 + 1/4.25
    }

    #[test]
    fn test_packet_loss_response() {
        let mut tcp = TcpCongestionControl::new(16.0, 32.0, 100);
        tcp.state = CongestionState::CongestionAvoidance;

        tcp.handle_packet_loss();

        // ssthresh should be cwnd/2 = 8
        assert_eq!(tcp.get_ssthresh(), 8.0);
        // cwnd should be ssthresh + 3 = 11
        assert_eq!(tcp.get_cwnd(), 11.0);
        assert_eq!(tcp.get_state(), CongestionState::FastRecovery);
    }

    #[test]
    fn test_timeout_response() {
        let mut tcp = TcpCongestionControl::new(20.0, 32.0, 100);
        tcp.state = CongestionState::CongestionAvoidance;

        tcp.handle_timeout();

        // ssthresh should be cwnd/2 = 10
        assert_eq!(tcp.get_ssthresh(), 10.0);
        // cwnd should reset to 1
        assert_eq!(tcp.get_cwnd(), 1.0);
        assert_eq!(tcp.get_state(), CongestionState::SlowStart);
    }

    #[test]
    fn test_fast_recovery_to_congestion_avoidance() {
        let mut tcp = TcpCongestionControl::new(16.0, 32.0, 100);

        // Trigger fast recovery
        tcp.handle_packet_loss();
        assert_eq!(tcp.get_state(), CongestionState::FastRecovery);

        // ACK should move to congestion avoidance
        tcp.handle_ack();
        assert_eq!(tcp.get_state(), CongestionState::CongestionAvoidance);
        assert_eq!(tcp.get_cwnd(), tcp.get_ssthresh());
    }

    #[test]
    fn test_minimum_ssthresh() {
        let mut tcp = TcpCongestionControl::new(2.0, 16.0, 100);

        tcp.handle_timeout();

        // ssthresh should be max(cwnd/2, 2) = max(1, 2) = 2
        assert_eq!(tcp.get_ssthresh(), 2.0);
    }

    #[test]
    fn test_event_processing() {
        let mut tcp = TcpCongestionControl::new(1.0, 16.0, 100);

        tcp.process_event(Event::AckReceived);
        assert_eq!(tcp.get_cwnd(), 2.0);

        tcp.process_event(Event::Timeout);
        assert_eq!(tcp.get_cwnd(), 1.0);
    }

    #[test]
    fn test_statistics_tracking() {
        let mut tcp = TcpCongestionControl::new(1.0, 16.0, 100);

        tcp.handle_ack();
        tcp.handle_ack();
        tcp.handle_packet_loss();

        let stats = tcp.get_stats();
        assert_eq!(stats.packets_acked, 2);
        assert_eq!(stats.packets_lost, 1);
    }

    #[test]
    fn test_aimd_fairness() {
        let mut tcp = TcpCongestionControl::new(8.0, 16.0, 100);
        tcp.state = CongestionState::CongestionAvoidance;

        let initial_cwnd = tcp.get_cwnd();

        // Additive increase
        for _ in 0..10 {
            tcp.handle_ack();
        }
        let increased_cwnd = tcp.get_cwnd();
        assert!(increased_cwnd > initial_cwnd);

        // Multiplicative decrease
        tcp.handle_packet_loss();
        let decreased_cwnd = tcp.get_cwnd();
        assert!(decreased_cwnd < increased_cwnd / 2.0);
    }

    #[test]
    fn test_send_packets() {
        let mut tcp = TcpCongestionControl::new(5.7, 16.0, 100);

        let packets = tcp.send_packets();
        assert_eq!(packets, 5); // Floor of 5.7

        let stats = tcp.get_stats();
        assert_eq!(stats.packets_sent, 5);
    }
}
