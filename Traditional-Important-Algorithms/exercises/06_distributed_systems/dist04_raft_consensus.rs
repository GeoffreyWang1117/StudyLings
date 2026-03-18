// dist04_raft_consensus.rs
//
// Raft is a consensus algorithm designed to be more understandable than Paxos
// while providing the same guarantees. It's used in distributed systems to ensure
// all nodes agree on a shared state.
//
// Key components:
// - Leader Election: One node is elected as leader to manage the log
// - Log Replication: Leader receives client requests and replicates to followers
// - Safety: Ensures committed entries are never lost
//
// Your task: Implement simplified Raft leader election and log replication.
//
// Key concepts:
// - Terms: Logical clock that increments with each election
// - States: Follower, Candidate, Leader
// - Election timeout: Random timeout that triggers new election
// - Heartbeat: Leader sends periodic heartbeats to maintain authority
// - Log entries: Commands with term number and index

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum NodeState {
    Follower,
    Candidate,
    Leader,
}

#[derive(Debug, Clone, PartialEq)]
pub struct LogEntry {
    pub term: u64,
    pub index: u64,
    pub command: String,
}

#[derive(Debug, Clone)]
pub struct RaftNode {
    pub id: usize,
    pub state: NodeState,
    pub current_term: u64,
    pub voted_for: Option<usize>,
    pub log: Vec<LogEntry>,
    pub commit_index: u64,
    pub last_applied: u64,

    // Leader-specific state
    pub next_index: HashMap<usize, u64>,   // For each server, index of next log entry to send
    pub match_index: HashMap<usize, u64>,  // For each server, index of highest log entry replicated

    // Election state
    pub votes_received: Vec<usize>,
    pub election_timeout: u64,
    pub time_since_heartbeat: u64,
}

impl RaftNode {
    pub fn new(id: usize, election_timeout: u64) -> Self {
        Self {
            id,
            state: NodeState::Follower,
            current_term: 0,
            voted_for: None,
            log: Vec::new(),
            commit_index: 0,
            last_applied: 0,
            next_index: HashMap::new(),
            match_index: HashMap::new(),
            votes_received: Vec::new(),
            election_timeout,
            time_since_heartbeat: 0,
        }
    }

    pub fn start_election(&mut self, cluster_size: usize) {
        // TODO: Start a new election
        // - Increment current_term
        // - Transition to Candidate state
        // - Vote for self
        // - Reset votes_received to just self
        // - Reset time_since_heartbeat
        todo!()
    }

    pub fn request_vote(&mut self, candidate_id: usize, candidate_term: u64,
                        last_log_index: u64, last_log_term: u64) -> (bool, u64) {
        // TODO: Handle RequestVote RPC
        // Grant vote if:
        // 1. candidate_term >= current_term
        // 2. Haven't voted for anyone else this term (or already voted for this candidate)
        // 3. Candidate's log is at least as up-to-date as receiver's log
        //    (compare last_log_term first, then last_log_index)
        //
        // If candidate_term > current_term:
        // - Update current_term
        // - Convert to Follower
        // - Reset voted_for
        //
        // Return (vote_granted, current_term)
        todo!()
    }

    pub fn receive_vote(&mut self, voter_id: usize, cluster_size: usize) -> bool {
        // TODO: Record a vote and check if won election
        // - Add voter_id to votes_received (if not already present)
        // - If received votes from majority of cluster, become Leader
        // - Initialize next_index and match_index for all nodes
        // - Return true if became leader
        todo!()
    }

    pub fn append_entries(&mut self, leader_term: u64) -> bool {
        // TODO: Handle heartbeat/AppendEntries RPC (simplified - just heartbeat)
        // - If leader_term < current_term, reject (return false)
        // - If leader_term >= current_term:
        //   - Update current_term if necessary
        //   - Convert to Follower if not already
        //   - Reset voted_for if term changed
        //   - Reset time_since_heartbeat
        //   - Return true
        todo!()
    }

    pub fn append_entry(&mut self, command: String) -> Option<u64> {
        // TODO: Leader appends a new entry to its log
        // - Only works if this node is Leader
        // - Create new LogEntry with current_term and next index
        // - Add to log
        // - Return the index of the new entry
        // - Return None if not leader
        todo!()
    }

    pub fn replicate_log_entry(&mut self, follower_id: usize, entry: &LogEntry) -> bool {
        // TODO: Simulate log replication to a follower
        // - Only works if this node is Leader
        // - Update next_index[follower_id] to entry.index + 1
        // - Update match_index[follower_id] to entry.index
        // - Return true if successful, false if not leader
        todo!()
    }

    pub fn try_commit(&mut self, cluster_size: usize) -> bool {
        // TODO: Try to commit entries based on replication
        // - Only works if this node is Leader
        // - Find highest index N where:
        //   1. N > commit_index
        //   2. Majority of match_index[i] >= N
        //   3. log[N].term == current_term
        // - Update commit_index to N if found
        // - Return true if commit_index was updated
        todo!()
    }

    pub fn tick(&mut self) {
        // TODO: Advance time by 1 unit
        // - Increment time_since_heartbeat
        // - If Follower or Candidate and time_since_heartbeat >= election_timeout,
        //   you would trigger an election (but we'll handle that externally)
        todo!()
    }

    pub fn get_last_log_index(&self) -> u64 {
        self.log.last().map(|e| e.index).unwrap_or(0)
    }

    pub fn get_last_log_term(&self) -> u64 {
        self.log.last().map(|e| e.term).unwrap_or(0)
    }

    pub fn is_election_timeout(&self) -> bool {
        self.time_since_heartbeat >= self.election_timeout
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_initial_state() {
        let node = RaftNode::new(1, 150);
        assert_eq!(node.state, NodeState::Follower);
        assert_eq!(node.current_term, 0);
        assert_eq!(node.voted_for, None);
    }

    #[test]
    fn test_start_election() {
        let mut node = RaftNode::new(1, 150);
        node.start_election(3);

        assert_eq!(node.state, NodeState::Candidate);
        assert_eq!(node.current_term, 1);
        assert_eq!(node.voted_for, Some(1));
        assert_eq!(node.votes_received, vec![1]);
    }

    #[test]
    fn test_request_vote_grant() {
        let mut node = RaftNode::new(1, 150);

        let (granted, term) = node.request_vote(2, 1, 0, 0);

        assert!(granted);
        assert_eq!(term, 1);
        assert_eq!(node.voted_for, Some(2));
        assert_eq!(node.current_term, 1);
    }

    #[test]
    fn test_request_vote_already_voted() {
        let mut node = RaftNode::new(1, 150);
        node.current_term = 1;
        node.voted_for = Some(2);

        // Different candidate, same term
        let (granted, _) = node.request_vote(3, 1, 0, 0);
        assert!(!granted);

        // Same candidate, same term
        let (granted, _) = node.request_vote(2, 1, 0, 0);
        assert!(granted);
    }

    #[test]
    fn test_request_vote_old_term() {
        let mut node = RaftNode::new(1, 150);
        node.current_term = 5;

        let (granted, term) = node.request_vote(2, 3, 0, 0);

        assert!(!granted);
        assert_eq!(term, 5);
    }

    #[test]
    fn test_win_election() {
        let mut node = RaftNode::new(1, 150);
        node.start_election(3);

        // Node 1 already voted for itself
        assert_eq!(node.state, NodeState::Candidate);

        // Receive vote from node 2 (now have 2/3 - majority)
        let won = node.receive_vote(2, 3);

        assert!(won);
        assert_eq!(node.state, NodeState::Leader);
    }

    #[test]
    fn test_election_needs_majority() {
        let mut node = RaftNode::new(1, 150);
        node.start_election(5);

        // Only 1/5 votes (self)
        assert_eq!(node.state, NodeState::Candidate);

        // 2/5 - not majority
        let won = node.receive_vote(2, 5);
        assert!(!won);
        assert_eq!(node.state, NodeState::Candidate);

        // 3/5 - majority!
        let won = node.receive_vote(3, 5);
        assert!(won);
        assert_eq!(node.state, NodeState::Leader);
    }

    #[test]
    fn test_heartbeat_updates_follower() {
        let mut node = RaftNode::new(1, 150);
        node.current_term = 1;
        node.time_since_heartbeat = 100;

        let accepted = node.append_entries(2);

        assert!(accepted);
        assert_eq!(node.current_term, 2);
        assert_eq!(node.state, NodeState::Follower);
        assert_eq!(node.time_since_heartbeat, 0);
    }

    #[test]
    fn test_heartbeat_rejects_old_term() {
        let mut node = RaftNode::new(1, 150);
        node.current_term = 5;

        let accepted = node.append_entries(3);

        assert!(!accepted);
        assert_eq!(node.current_term, 5); // Should not change
    }

    #[test]
    fn test_leader_append_entry() {
        let mut node = RaftNode::new(1, 150);
        node.state = NodeState::Leader;
        node.current_term = 1;

        let index = node.append_entry("SET x=1".to_string());

        assert_eq!(index, Some(1));
        assert_eq!(node.log.len(), 1);
        assert_eq!(node.log[0].term, 1);
        assert_eq!(node.log[0].index, 1);
        assert_eq!(node.log[0].command, "SET x=1");
    }

    #[test]
    fn test_follower_cannot_append_entry() {
        let mut node = RaftNode::new(1, 150);
        assert_eq!(node.state, NodeState::Follower);

        let index = node.append_entry("SET x=1".to_string());

        assert_eq!(index, None);
        assert_eq!(node.log.len(), 0);
    }

    #[test]
    fn test_log_replication() {
        let mut leader = RaftNode::new(1, 150);
        leader.state = NodeState::Leader;
        leader.current_term = 1;
        leader.next_index.insert(2, 1);
        leader.match_index.insert(2, 0);

        let index = leader.append_entry("SET x=1".to_string()).unwrap();
        let entry = leader.log[0].clone();

        let success = leader.replicate_log_entry(2, &entry);

        assert!(success);
        assert_eq!(leader.next_index[&2], 2);
        assert_eq!(leader.match_index[&2], 1);
    }

    #[test]
    fn test_commit_with_majority() {
        let mut leader = RaftNode::new(1, 150);
        leader.state = NodeState::Leader;
        leader.current_term = 1;

        // Leader has entry at index 1
        leader.append_entry("SET x=1".to_string());

        // Initialize for 3-node cluster
        leader.next_index.insert(2, 1);
        leader.next_index.insert(3, 1);
        leader.match_index.insert(1, 1); // Leader itself
        leader.match_index.insert(2, 0);
        leader.match_index.insert(3, 0);

        // Replicate to node 2
        leader.replicate_log_entry(2, &leader.log[0].clone());

        // Now 2/3 nodes have the entry (leader + node 2)
        let committed = leader.try_commit(3);

        assert!(committed);
        assert_eq!(leader.commit_index, 1);
    }

    #[test]
    fn test_election_timeout_tick() {
        let mut node = RaftNode::new(1, 150);

        for _ in 0..149 {
            node.tick();
            assert!(!node.is_election_timeout());
        }

        node.tick();
        assert!(node.is_election_timeout());
    }

    #[test]
    fn test_candidate_converts_to_follower_on_higher_term() {
        let mut node = RaftNode::new(1, 150);
        node.start_election(3);
        assert_eq!(node.state, NodeState::Candidate);
        assert_eq!(node.current_term, 1);

        // Receive heartbeat from leader with higher term
        node.append_entries(2);

        assert_eq!(node.state, NodeState::Follower);
        assert_eq!(node.current_term, 2);
    }
}
