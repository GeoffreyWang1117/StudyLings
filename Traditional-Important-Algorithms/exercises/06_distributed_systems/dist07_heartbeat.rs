// dist07_heartbeat.rs
//
// Heartbeat mechanisms are fundamental for failure detection in distributed systems.
// Nodes periodically send "I'm alive" messages to detect when peers have failed.
//
// Common approaches:
// - Fixed timeout: Declare node dead after missing N heartbeats
// - Adaptive timeout: Adjust based on network conditions
// - Phi Accrual Failure Detector: Continuous suspicion level instead of binary alive/dead
//
// Your task: Implement heartbeat-based failure detection with both fixed and
// adaptive strategies.
//
// Key concepts:
// - Heartbeat interval: How often to send heartbeats
// - Timeout threshold: When to suspect failure
// - False positives: Declaring healthy node as failed (due to slow network)
// - Detection time: How quickly failures are detected

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum NodeStatus {
    Alive,
    Suspected,
    Dead,
}

#[derive(Debug, Clone)]
pub struct HeartbeatRecord {
    pub node_id: usize,
    pub last_heartbeat: u64,
    pub heartbeat_count: usize,
    pub status: NodeStatus,
    pub missed_heartbeats: usize,
}

impl HeartbeatRecord {
    pub fn new(node_id: usize, current_time: u64) -> Self {
        Self {
            node_id,
            last_heartbeat: current_time,
            heartbeat_count: 0,
            status: NodeStatus::Alive,
            missed_heartbeats: 0,
        }
    }
}

pub struct FixedTimeoutDetector {
    nodes: HashMap<usize, HeartbeatRecord>,
    heartbeat_interval: u64,
    timeout_threshold: u64,
    current_time: u64,
}

impl FixedTimeoutDetector {
    pub fn new(heartbeat_interval: u64, timeout_threshold: u64) -> Self {
        Self {
            nodes: HashMap::new(),
            heartbeat_interval,
            timeout_threshold,
            current_time: 0,
        }
    }

    pub fn add_node(&mut self, node_id: usize) {
        self.nodes.insert(node_id, HeartbeatRecord::new(node_id, self.current_time));
    }

    pub fn receive_heartbeat(&mut self, node_id: usize) {
        // TODO: Process a heartbeat from a node
        // - Update last_heartbeat to current_time
        // - Increment heartbeat_count
        // - Reset missed_heartbeats to 0
        // - Set status to Alive
        // - If node doesn't exist, add it
        todo!()
    }

    pub fn check_timeouts(&mut self) {
        // TODO: Check all nodes for timeouts
        // - For each node, calculate time_since_heartbeat
        // - If time_since_heartbeat > timeout_threshold:
        //   - Set status to Dead
        //   - Increment missed_heartbeats
        // - Otherwise, ensure status is Alive
        todo!()
    }

    pub fn advance_time(&mut self, delta: u64) {
        self.current_time += delta;
        self.check_timeouts();
    }

    pub fn get_status(&self, node_id: usize) -> Option<NodeStatus> {
        self.nodes.get(&node_id).map(|record| record.status)
    }

    pub fn get_alive_nodes(&self) -> Vec<usize> {
        self.nodes
            .values()
            .filter(|record| record.status == NodeStatus::Alive)
            .map(|record| record.node_id)
            .collect()
    }

    pub fn get_dead_nodes(&self) -> Vec<usize> {
        self.nodes
            .values()
            .filter(|record| record.status == NodeStatus::Dead)
            .map(|record| record.node_id)
            .collect()
    }

    pub fn get_time(&self) -> u64 {
        self.current_time
    }
}

#[derive(Debug, Clone)]
pub struct AdaptiveHeartbeatRecord {
    pub node_id: usize,
    pub last_heartbeat: u64,
    pub heartbeat_count: usize,
    pub status: NodeStatus,
    pub heartbeat_history: Vec<u64>, // Intervals between heartbeats
    pub max_history: usize,
}

impl AdaptiveHeartbeatRecord {
    pub fn new(node_id: usize, current_time: u64, max_history: usize) -> Self {
        Self {
            node_id,
            last_heartbeat: current_time,
            heartbeat_count: 0,
            status: NodeStatus::Alive,
            heartbeat_history: Vec::new(),
            max_history,
        }
    }

    pub fn calculate_mean(&self) -> f64 {
        if self.heartbeat_history.is_empty() {
            return 0.0;
        }
        let sum: u64 = self.heartbeat_history.iter().sum();
        sum as f64 / self.heartbeat_history.len() as f64
    }

    pub fn calculate_std_dev(&self) -> f64 {
        if self.heartbeat_history.len() < 2 {
            return 0.0;
        }
        let mean = self.calculate_mean();
        let variance = self.heartbeat_history
            .iter()
            .map(|&x| {
                let diff = x as f64 - mean;
                diff * diff
            })
            .sum::<f64>() / self.heartbeat_history.len() as f64;
        variance.sqrt()
    }
}

pub struct AdaptiveTimeoutDetector {
    nodes: HashMap<usize, AdaptiveHeartbeatRecord>,
    max_history: usize,
    phi_threshold: f64,  // Suspicion level threshold
    current_time: u64,
}

impl AdaptiveTimeoutDetector {
    pub fn new(max_history: usize, phi_threshold: f64) -> Self {
        Self {
            nodes: HashMap::new(),
            max_history,
            phi_threshold,
            current_time: 0,
        }
    }

    pub fn add_node(&mut self, node_id: usize) {
        self.nodes.insert(
            node_id,
            AdaptiveHeartbeatRecord::new(node_id, self.current_time, self.max_history)
        );
    }

    pub fn receive_heartbeat(&mut self, node_id: usize) {
        // TODO: Process a heartbeat with adaptive tracking
        // - Calculate interval since last heartbeat
        // - Add interval to heartbeat_history
        // - Limit history size to max_history (remove oldest if needed)
        // - Update last_heartbeat to current_time
        // - Increment heartbeat_count
        // - Set status to Alive
        // - If node doesn't exist, add it
        todo!()
    }

    pub fn calculate_phi(&self, node_id: usize) -> f64 {
        // TODO: Calculate phi (suspicion level) for a node
        // Uses the Phi Accrual Failure Detector algorithm
        //
        // - Get time since last heartbeat
        // - Get mean and std_dev from heartbeat history
        // - If no history, return 0.0
        // - Calculate phi based on how many standard deviations away we are
        //
        // Simplified phi calculation:
        // phi = (time_since_last - mean) / (std_dev + 1.0)
        // (The +1.0 prevents division by zero)
        //
        // Return 0.0 if node doesn't exist
        todo!()
    }

    pub fn check_failures(&mut self) {
        // TODO: Check all nodes for failure based on phi threshold
        // - Calculate phi for each node
        // - If phi > phi_threshold, mark as Suspected
        // - If phi > phi_threshold * 2, mark as Dead
        // - Otherwise, mark as Alive
        todo!()
    }

    pub fn advance_time(&mut self, delta: u64) {
        self.current_time += delta;
        self.check_failures();
    }

    pub fn get_status(&self, node_id: usize) -> Option<NodeStatus> {
        self.nodes.get(&node_id).map(|record| record.status)
    }

    pub fn get_alive_nodes(&self) -> Vec<usize> {
        self.nodes
            .values()
            .filter(|record| record.status == NodeStatus::Alive)
            .map(|record| record.node_id)
            .collect()
    }

    pub fn get_suspected_nodes(&self) -> Vec<usize> {
        self.nodes
            .values()
            .filter(|record| record.status == NodeStatus::Suspected)
            .map(|record| record.node_id)
            .collect()
    }

    pub fn get_dead_nodes(&self) -> Vec<usize> {
        self.nodes
            .values()
            .filter(|record| record.status == NodeStatus::Dead)
            .map(|record| record.node_id)
            .collect()
    }

    pub fn get_time(&self) -> u64 {
        self.current_time
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fixed_timeout_initial_state() {
        let mut detector = FixedTimeoutDetector::new(10, 30);
        detector.add_node(1);

        assert_eq!(detector.get_status(1), Some(NodeStatus::Alive));
    }

    #[test]
    fn test_fixed_timeout_heartbeat() {
        let mut detector = FixedTimeoutDetector::new(10, 30);
        detector.add_node(1);

        detector.advance_time(10);
        detector.receive_heartbeat(1);

        assert_eq!(detector.get_status(1), Some(NodeStatus::Alive));
    }

    #[test]
    fn test_fixed_timeout_detection() {
        let mut detector = FixedTimeoutDetector::new(10, 30);
        detector.add_node(1);

        // No heartbeat for 31 time units
        detector.advance_time(31);

        assert_eq!(detector.get_status(1), Some(NodeStatus::Dead));
    }

    #[test]
    fn test_fixed_timeout_recovery() {
        let mut detector = FixedTimeoutDetector::new(10, 30);
        detector.add_node(1);

        // Node times out
        detector.advance_time(31);
        assert_eq!(detector.get_status(1), Some(NodeStatus::Dead));

        // Node sends heartbeat and recovers
        detector.receive_heartbeat(1);
        assert_eq!(detector.get_status(1), Some(NodeStatus::Alive));
    }

    #[test]
    fn test_multiple_nodes() {
        let mut detector = FixedTimeoutDetector::new(10, 30);
        detector.add_node(1);
        detector.add_node(2);
        detector.add_node(3);

        // Node 1 and 2 send heartbeats
        detector.receive_heartbeat(1);
        detector.receive_heartbeat(2);

        detector.advance_time(31);

        // Node 3 should be dead, 1 and 2 alive
        assert_eq!(detector.get_alive_nodes().len(), 2);
        assert_eq!(detector.get_dead_nodes(), vec![3]);
    }

    #[test]
    fn test_get_alive_and_dead_nodes() {
        let mut detector = FixedTimeoutDetector::new(10, 30);
        detector.add_node(1);
        detector.add_node(2);

        detector.receive_heartbeat(1);
        detector.advance_time(31);

        let alive = detector.get_alive_nodes();
        let dead = detector.get_dead_nodes();

        assert_eq!(alive, vec![1]);
        assert_eq!(dead, vec![2]);
    }

    #[test]
    fn test_adaptive_heartbeat_history() {
        let mut detector = AdaptiveTimeoutDetector::new(5, 3.0);
        detector.add_node(1);

        // Send heartbeats at regular intervals
        for _ in 0..10 {
            detector.advance_time(10);
            detector.receive_heartbeat(1);
        }

        let node = detector.nodes.get(&1).unwrap();
        assert!(node.heartbeat_history.len() <= 5); // Should be capped at max_history
    }

    #[test]
    fn test_adaptive_mean_calculation() {
        let mut detector = AdaptiveTimeoutDetector::new(10, 3.0);
        detector.add_node(1);

        // Send heartbeats at 10ms intervals
        for _ in 0..5 {
            detector.advance_time(10);
            detector.receive_heartbeat(1);
        }

        let node = detector.nodes.get(&1).unwrap();
        let mean = node.calculate_mean();
        assert!((mean - 10.0).abs() < 0.1);
    }

    #[test]
    fn test_adaptive_phi_calculation() {
        let mut detector = AdaptiveTimeoutDetector::new(10, 3.0);
        detector.add_node(1);

        // Establish pattern
        for _ in 0..5 {
            detector.advance_time(10);
            detector.receive_heartbeat(1);
        }

        // Small delay - phi should be low
        detector.advance_time(12);
        let phi = detector.calculate_phi(1);
        assert!(phi < 3.0);
    }

    #[test]
    fn test_adaptive_failure_detection() {
        let mut detector = AdaptiveTimeoutDetector::new(10, 2.0);
        detector.add_node(1);

        // Establish regular pattern (10ms intervals)
        for _ in 0..5 {
            detector.advance_time(10);
            detector.receive_heartbeat(1);
        }

        // Long delay should trigger suspicion
        detector.advance_time(50);

        let status = detector.get_status(1);
        // Should be suspected or dead due to high phi
        assert!(status == Some(NodeStatus::Suspected) || status == Some(NodeStatus::Dead));
    }

    #[test]
    fn test_adaptive_suspected_state() {
        let mut detector = AdaptiveTimeoutDetector::new(10, 3.0);
        detector.add_node(1);

        // Establish pattern
        for _ in 0..10 {
            detector.advance_time(10);
            detector.receive_heartbeat(1);
        }

        // Delay that causes high phi but not extreme
        detector.advance_time(35);

        let suspected = detector.get_suspected_nodes();
        // Node might be in suspected state
        assert!(suspected.is_empty() || suspected.contains(&1));
    }

    #[test]
    fn test_heartbeat_count() {
        let mut detector = FixedTimeoutDetector::new(10, 30);
        detector.add_node(1);

        for _ in 0..5 {
            detector.receive_heartbeat(1);
        }

        let node = detector.nodes.get(&1).unwrap();
        assert_eq!(node.heartbeat_count, 5);
    }

    #[test]
    fn test_auto_add_node_on_heartbeat() {
        let mut detector = FixedTimeoutDetector::new(10, 30);

        // Node doesn't exist yet
        assert_eq!(detector.get_status(1), None);

        // Receiving heartbeat should add it
        detector.receive_heartbeat(1);
        assert_eq!(detector.get_status(1), Some(NodeStatus::Alive));
    }

    #[test]
    fn test_missed_heartbeats_tracking() {
        let mut detector = FixedTimeoutDetector::new(10, 30);
        detector.add_node(1);

        detector.advance_time(31);
        detector.check_timeouts();

        let node = detector.nodes.get(&1).unwrap();
        assert!(node.missed_heartbeats > 0);
    }
}
