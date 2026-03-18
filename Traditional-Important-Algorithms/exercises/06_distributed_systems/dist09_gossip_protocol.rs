// dist09_gossip_protocol.rs
//
// Gossip Protocol (also called epidemic protocol) spreads information through
// a distributed system similar to how gossip or diseases spread in a population.
// Nodes periodically exchange information with random peers.
//
// Key properties:
// - Eventual consistency: All nodes eventually receive all updates
// - Fault tolerance: Works even if some nodes fail or messages are lost
// - Scalability: Communication overhead grows logarithmically with cluster size
// - No central coordination required
//
// Your task: Implement a gossip protocol for information dissemination.
//
// Key concepts:
// - Push gossip: Sender pushes updates to random nodes
// - Pull gossip: Receiver pulls updates from random nodes
// - Push-Pull: Combination of both (most efficient)
// - Fanout: Number of nodes to gossip with per round
// - Round: One iteration of gossip exchange

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, PartialEq)]
pub struct GossipMessage {
    pub key: String,
    pub value: String,
    pub version: u64,
    pub timestamp: u64,
}

impl GossipMessage {
    pub fn new(key: String, value: String, version: u64, timestamp: u64) -> Self {
        Self { key, value, version, timestamp }
    }
}

#[derive(Debug, Clone)]
pub struct GossipNode {
    pub id: usize,
    pub data: HashMap<String, GossipMessage>,
    pub peers: HashSet<usize>,
    pub rounds_participated: usize,
    pub messages_sent: usize,
    pub messages_received: usize,
}

impl GossipNode {
    pub fn new(id: usize) -> Self {
        Self {
            id,
            data: HashMap::new(),
            peers: HashSet::new(),
            rounds_participated: 0,
            messages_sent: 0,
            messages_received: 0,
        }
    }

    pub fn add_peer(&mut self, peer_id: usize) {
        if peer_id != self.id {
            self.peers.insert(peer_id);
        }
    }

    pub fn update(&mut self, key: String, value: String, version: u64, timestamp: u64) {
        // TODO: Update local data
        // - Only update if version is newer than current version
        // - If key doesn't exist, add it
        // - Return true if updated, false if ignored (older version)
        todo!()
    }

    pub fn get(&self, key: &str) -> Option<&GossipMessage> {
        self.data.get(key)
    }

    pub fn get_all_data(&self) -> Vec<GossipMessage> {
        self.data.values().cloned().collect()
    }
}

pub struct GossipCluster {
    nodes: HashMap<usize, GossipNode>,
    current_time: u64,
    fanout: usize,  // How many random nodes to gossip with
    rng_seed: u64,  // For deterministic randomness in tests
}

impl GossipCluster {
    pub fn new(fanout: usize) -> Self {
        Self {
            nodes: HashMap::new(),
            current_time: 0,
            fanout,
            rng_seed: 12345,
        }
    }

    pub fn add_node(&mut self, node_id: usize) {
        self.nodes.insert(node_id, GossipNode::new(node_id));
    }

    pub fn connect_all(&mut self) {
        // TODO: Create a fully connected network
        // - Each node should have all other nodes as peers
        todo!()
    }

    pub fn update_node_data(&mut self, node_id: usize, key: String, value: String, version: u64) {
        // TODO: Update data on a specific node
        // - Use current_time as timestamp
        // - Update the node's local data
        todo!()
    }

    fn select_random_peers(&self, node_id: usize, count: usize) -> Vec<usize> {
        // TODO: Select random peers for gossip
        // - Get the node's peer list
        // - Return up to 'count' random peers
        // - Use simple deterministic selection for testing:
        //   Take first 'count' peers when sorted by ID
        // - In real implementation, this would be truly random
        todo!()
    }

    pub fn gossip_round_push(&mut self, node_id: usize) {
        // TODO: Perform one round of push-based gossip
        // - Select fanout random peers
        // - For each peer, send all of this node's data
        // - Peer updates its data based on versions
        // - Update statistics (messages_sent, messages_received, rounds_participated)
        todo!()
    }

    pub fn gossip_round_pull(&mut self, node_id: usize) {
        // TODO: Perform one round of pull-based gossip
        // - Select fanout random peers
        // - For each peer, request all their data
        // - Update this node's data based on versions
        // - Update statistics
        todo!()
    }

    pub fn gossip_round_push_pull(&mut self, node_id: usize) {
        // TODO: Perform one round of push-pull gossip (most efficient)
        // - Select fanout random peers
        // - For each peer:
        //   1. Send all this node's data (push)
        //   2. Receive all peer's data (pull)
        //   3. Both nodes update their data
        // - Update statistics
        todo!()
    }

    pub fn run_gossip_round_all(&mut self) {
        // TODO: Run one gossip round for all nodes
        // - Each node performs push-pull gossip
        // - Process nodes in sorted order for deterministic testing
        todo!()
    }

    pub fn run_until_convergence(&mut self, max_rounds: usize) -> usize {
        // TODO: Run gossip until all nodes have the same data
        // - Run rounds until convergence or max_rounds reached
        // - Return number of rounds needed
        // - Convergence: all nodes have same data (same keys with same versions)
        todo!()
    }

    pub fn is_converged(&self) -> bool {
        // TODO: Check if all nodes have converged
        // - All nodes should have the same set of keys
        // - For each key, all nodes should have the same version
        todo!()
    }

    pub fn get_node(&self, node_id: usize) -> Option<&GossipNode> {
        self.nodes.get(&node_id)
    }

    pub fn get_convergence_percentage(&self) -> f64 {
        // TODO: Calculate what percentage of data has converged
        // - Find all unique keys across all nodes
        // - For each key, find the highest version number
        // - Count how many nodes have that version
        // - Return average percentage across all keys
        todo!()
    }

    pub fn advance_time(&mut self, delta: u64) {
        self.current_time += delta;
    }

    pub fn get_time(&self) -> u64 {
        self.current_time
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_node() {
        let node = GossipNode::new(1);
        assert_eq!(node.id, 1);
        assert_eq!(node.data.len(), 0);
    }

    #[test]
    fn test_update_local_data() {
        let mut node = GossipNode::new(1);

        node.update("key1".to_string(), "value1".to_string(), 1, 100);

        let msg = node.get("key1").unwrap();
        assert_eq!(msg.value, "value1");
        assert_eq!(msg.version, 1);
    }

    #[test]
    fn test_update_with_newer_version() {
        let mut node = GossipNode::new(1);

        node.update("key1".to_string(), "value1".to_string(), 1, 100);
        node.update("key1".to_string(), "value2".to_string(), 2, 200);

        let msg = node.get("key1").unwrap();
        assert_eq!(msg.value, "value2");
        assert_eq!(msg.version, 2);
    }

    #[test]
    fn test_ignore_older_version() {
        let mut node = GossipNode::new(1);

        node.update("key1".to_string(), "value2".to_string(), 2, 200);
        node.update("key1".to_string(), "value1".to_string(), 1, 100);

        let msg = node.get("key1").unwrap();
        assert_eq!(msg.value, "value2"); // Should keep newer version
        assert_eq!(msg.version, 2);
    }

    #[test]
    fn test_connect_all() {
        let mut cluster = GossipCluster::new(2);
        cluster.add_node(0);
        cluster.add_node(1);
        cluster.add_node(2);

        cluster.connect_all();

        let node0 = cluster.get_node(0).unwrap();
        assert_eq!(node0.peers.len(), 2); // Connected to nodes 1 and 2
    }

    #[test]
    fn test_gossip_push() {
        let mut cluster = GossipCluster::new(1);
        cluster.add_node(0);
        cluster.add_node(1);
        cluster.connect_all();

        cluster.update_node_data(0, "key1".to_string(), "value1".to_string(), 1);

        cluster.gossip_round_push(0);

        // Node 1 should have received the data
        let node1 = cluster.get_node(1).unwrap();
        assert!(node1.get("key1").is_some());
    }

    #[test]
    fn test_gossip_pull() {
        let mut cluster = GossipCluster::new(1);
        cluster.add_node(0);
        cluster.add_node(1);
        cluster.connect_all();

        cluster.update_node_data(1, "key1".to_string(), "value1".to_string(), 1);

        cluster.gossip_round_pull(0);

        // Node 0 should have pulled the data
        let node0 = cluster.get_node(0).unwrap();
        assert!(node0.get("key1").is_some());
    }

    #[test]
    fn test_push_pull_bidirectional() {
        let mut cluster = GossipCluster::new(1);
        cluster.add_node(0);
        cluster.add_node(1);
        cluster.connect_all();

        cluster.update_node_data(0, "key1".to_string(), "value1".to_string(), 1);
        cluster.update_node_data(1, "key2".to_string(), "value2".to_string(), 1);

        cluster.gossip_round_push_pull(0);

        // Both nodes should have both keys
        let node0 = cluster.get_node(0).unwrap();
        let node1 = cluster.get_node(1).unwrap();

        assert!(node0.get("key1").is_some());
        assert!(node0.get("key2").is_some());
        assert!(node1.get("key1").is_some());
        assert!(node1.get("key2").is_some());
    }

    #[test]
    fn test_convergence() {
        let mut cluster = GossipCluster::new(2);

        for i in 0..5 {
            cluster.add_node(i);
        }
        cluster.connect_all();

        // Add different data to different nodes
        cluster.update_node_data(0, "key1".to_string(), "value1".to_string(), 1);
        cluster.update_node_data(1, "key2".to_string(), "value2".to_string(), 1);
        cluster.update_node_data(2, "key3".to_string(), "value3".to_string(), 1);

        let rounds = cluster.run_until_convergence(20);

        assert!(rounds > 0);
        assert!(cluster.is_converged());

        // All nodes should have all keys
        for i in 0..5 {
            let node = cluster.get_node(i).unwrap();
            assert!(node.get("key1").is_some());
            assert!(node.get("key2").is_some());
            assert!(node.get("key3").is_some());
        }
    }

    #[test]
    fn test_version_conflict_resolution() {
        let mut cluster = GossipCluster::new(2);
        cluster.add_node(0);
        cluster.add_node(1);
        cluster.connect_all();

        // Node 0 has older version
        cluster.update_node_data(0, "key1".to_string(), "old".to_string(), 1);

        // Node 1 has newer version
        cluster.update_node_data(1, "key1".to_string(), "new".to_string(), 2);

        cluster.run_until_convergence(10);

        // Both should have the newer version
        let node0 = cluster.get_node(0).unwrap();
        let node1 = cluster.get_node(1).unwrap();

        assert_eq!(node0.get("key1").unwrap().value, "new");
        assert_eq!(node1.get("key1").unwrap().value, "new");
        assert_eq!(node0.get("key1").unwrap().version, 2);
        assert_eq!(node1.get("key1").unwrap().version, 2);
    }

    #[test]
    fn test_fanout_limits_connections() {
        let mut cluster = GossipCluster::new(2);

        for i in 0..10 {
            cluster.add_node(i);
        }
        cluster.connect_all();

        cluster.update_node_data(0, "key1".to_string(), "value1".to_string(), 1);

        let node0 = cluster.get_node(0).unwrap();
        let initial_sent = node0.messages_sent;

        cluster.gossip_round_push(0);

        let node0 = cluster.get_node(0).unwrap();
        // Should have gossiped to fanout (2) nodes, not all 9 peers
        assert!(node0.messages_sent - initial_sent <= 2 * 10); // 2 peers * some messages
    }

    #[test]
    fn test_statistics_tracking() {
        let mut cluster = GossipCluster::new(1);
        cluster.add_node(0);
        cluster.add_node(1);
        cluster.connect_all();

        cluster.update_node_data(0, "key1".to_string(), "value1".to_string(), 1);

        cluster.gossip_round_push_pull(0);

        let node0 = cluster.get_node(0).unwrap();
        assert!(node0.rounds_participated > 0);
        assert!(node0.messages_sent > 0 || node0.messages_received > 0);
    }

    #[test]
    fn test_large_cluster_convergence() {
        let mut cluster = GossipCluster::new(3);

        for i in 0..20 {
            cluster.add_node(i);
        }
        cluster.connect_all();

        // Each node starts with unique data
        for i in 0..20 {
            cluster.update_node_data(i, format!("key{}", i), format!("value{}", i), 1);
        }

        let rounds = cluster.run_until_convergence(50);

        // Should converge in logarithmic rounds
        assert!(rounds < 20); // Should be much less than 50
        assert!(cluster.is_converged());
    }
}
