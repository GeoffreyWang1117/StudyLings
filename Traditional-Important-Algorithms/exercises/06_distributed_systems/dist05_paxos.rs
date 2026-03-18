// dist05_paxos.rs
//
// Paxos is a family of protocols for solving consensus in a network of unreliable
// processors. It's fundamental to distributed systems but known for being difficult
// to understand and implement.
//
// Basic Paxos has two phases:
// - Phase 1 (Prepare): Proposer asks acceptors to promise not to accept older proposals
// - Phase 2 (Accept): If majority promises, proposer asks acceptors to accept value
//
// Your task: Implement Basic Paxos (single-decree).
//
// Key concepts:
// - Proposal numbers: Unique, totally-ordered identifiers
// - Quorum: Majority of acceptors must agree
// - Promise: Acceptor's commitment to ignore older proposals
// - Chosen value: Value accepted by majority of acceptors
// - Safety: Only one value can be chosen

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub struct Proposal {
    pub number: u64,           // Unique proposal number (higher = newer)
    pub value: String,
}

impl Proposal {
    pub fn new(number: u64, value: String) -> Self {
        Self { number, value }
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Promise {
    pub proposal_number: u64,
    pub accepted_proposal: Option<Proposal>, // Previously accepted proposal, if any
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Phase {
    Idle,
    Prepare,
    Accept,
    Decided,
}

pub struct Proposer {
    pub id: usize,
    pub proposal_number: u64,
    pub proposed_value: Option<String>,
    pub promises_received: HashMap<usize, Promise>,
    pub accepts_received: Vec<usize>,
    pub phase: Phase,
    pub decided_value: Option<String>,
}

impl Proposer {
    pub fn new(id: usize) -> Self {
        Self {
            id,
            proposal_number: id as u64, // Start with ID to ensure uniqueness
            proposed_value: None,
            promises_received: HashMap::new(),
            accepts_received: Vec::new(),
            phase: Phase::Idle,
            decided_value: None,
        }
    }

    pub fn prepare(&mut self, value: String, cluster_size: usize) -> u64 {
        // TODO: Start Phase 1 (Prepare)
        // - Generate new proposal number (increment by cluster_size to maintain uniqueness)
        // - Store the value we want to propose
        // - Clear promises_received and accepts_received
        // - Set phase to Prepare
        // - Return the proposal number
        todo!()
    }

    pub fn receive_promise(&mut self, acceptor_id: usize, promise: Promise, cluster_size: usize) -> bool {
        // TODO: Handle a Promise response from an acceptor
        // - Store the promise
        // - If received promises from majority:
        //   - Check if any promise includes a previously accepted value
        //   - If so, must propose the value from the highest-numbered accepted proposal
        //   - Set phase to Accept
        //   - Return true (ready for Phase 2)
        // - Otherwise return false (need more promises)
        todo!()
    }

    pub fn receive_accept(&mut self, acceptor_id: usize, cluster_size: usize) -> bool {
        // TODO: Handle an Accept response from an acceptor
        // - Record the acceptance
        // - If received accepts from majority:
        //   - Set decided_value to the proposed value
        //   - Set phase to Decided
        //   - Return true (consensus reached!)
        // - Otherwise return false (need more accepts)
        todo!()
    }

    pub fn get_value_to_propose(&self) -> Option<String> {
        self.proposed_value.clone()
    }

    pub fn is_decided(&self) -> bool {
        self.phase == Phase::Decided
    }
}

pub struct Acceptor {
    pub id: usize,
    pub promised_number: Option<u64>,      // Highest proposal number promised
    pub accepted_proposal: Option<Proposal>, // Highest-numbered proposal accepted
}

impl Acceptor {
    pub fn new(id: usize) -> Self {
        Self {
            id,
            promised_number: None,
            accepted_proposal: None,
        }
    }

    pub fn receive_prepare(&mut self, proposal_number: u64) -> Option<Promise> {
        // TODO: Handle a Prepare request
        // - If proposal_number > promised_number (or no promise yet):
        //   - Update promised_number to proposal_number
        //   - Return Promise with proposal_number and accepted_proposal (if any)
        // - Otherwise, reject (return None)
        todo!()
    }

    pub fn receive_accept_request(&mut self, proposal: Proposal) -> bool {
        // TODO: Handle an Accept request
        // - If no promise yet, or proposal.number >= promised_number:
        //   - Update promised_number to proposal.number
        //   - Update accepted_proposal to this proposal
        //   - Return true (accepted)
        // - Otherwise, reject (return false)
        todo!()
    }

    pub fn get_accepted_value(&self) -> Option<String> {
        self.accepted_proposal.as_ref().map(|p| p.value.clone())
    }
}

pub struct PaxosCluster {
    proposers: HashMap<usize, Proposer>,
    acceptors: HashMap<usize, Acceptor>,
}

impl PaxosCluster {
    pub fn new(num_acceptors: usize) -> Self {
        let mut acceptors = HashMap::new();
        for i in 0..num_acceptors {
            acceptors.insert(i, Acceptor::new(i));
        }

        Self {
            proposers: HashMap::new(),
            acceptors,
        }
    }

    pub fn add_proposer(&mut self, id: usize) -> &mut Proposer {
        self.proposers.insert(id, Proposer::new(id));
        self.proposers.get_mut(&id).unwrap()
    }

    pub fn get_proposer(&self, id: usize) -> Option<&Proposer> {
        self.proposers.get(&id)
    }

    pub fn get_proposer_mut(&mut self, id: usize) -> Option<&mut Proposer> {
        self.proposers.get_mut(&id)
    }

    pub fn get_acceptor(&self, id: usize) -> Option<&Acceptor> {
        self.acceptors.get(&id)
    }

    pub fn cluster_size(&self) -> usize {
        self.acceptors.len()
    }

    pub fn phase1_prepare(&mut self, proposer_id: usize, value: String) -> Vec<(usize, Option<Promise>)> {
        // TODO: Execute Phase 1 for a proposer
        // - Call prepare on proposer
        // - Send prepare to all acceptors
        // - Collect promises
        // - Return vector of (acceptor_id, promise)
        todo!()
    }

    pub fn phase2_accept(&mut self, proposer_id: usize) -> Vec<(usize, bool)> {
        // TODO: Execute Phase 2 for a proposer
        // - Get the value to propose from proposer
        // - Create proposal with proposer's proposal_number
        // - Send accept request to all acceptors
        // - Return vector of (acceptor_id, accepted)
        todo!()
    }

    pub fn run_paxos(&mut self, proposer_id: usize, value: String) -> Option<String> {
        // TODO: Run full Paxos protocol for a proposer
        // - Execute Phase 1
        // - Process promises
        // - If got majority, execute Phase 2
        // - Process accepts
        // - Return decided value if consensus reached
        todo!()
    }

    pub fn get_consensus_value(&self) -> Option<String> {
        // Check if any proposer has reached consensus
        self.proposers.values()
            .find(|p| p.is_decided())
            .and_then(|p| p.decided_value.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_acceptor_promise() {
        let mut acceptor = Acceptor::new(0);

        let promise = acceptor.receive_prepare(10);
        assert!(promise.is_some());
        assert_eq!(promise.unwrap().proposal_number, 10);
        assert_eq!(acceptor.promised_number, Some(10));
    }

    #[test]
    fn test_acceptor_rejects_old_prepare() {
        let mut acceptor = Acceptor::new(0);
        acceptor.receive_prepare(10);

        let promise = acceptor.receive_prepare(5);
        assert!(promise.is_none());
        assert_eq!(acceptor.promised_number, Some(10)); // Should not change
    }

    #[test]
    fn test_acceptor_accept() {
        let mut acceptor = Acceptor::new(0);
        acceptor.receive_prepare(10);

        let proposal = Proposal::new(10, "value1".to_string());
        let accepted = acceptor.receive_accept_request(proposal.clone());

        assert!(accepted);
        assert_eq!(acceptor.accepted_proposal, Some(proposal));
    }

    #[test]
    fn test_acceptor_rejects_old_accept() {
        let mut acceptor = Acceptor::new(0);
        acceptor.receive_prepare(10);

        let proposal = Proposal::new(5, "value1".to_string());
        let accepted = acceptor.receive_accept_request(proposal);

        assert!(!accepted);
        assert!(acceptor.accepted_proposal.is_none());
    }

    #[test]
    fn test_proposer_prepare_phase() {
        let mut proposer = Proposer::new(0);
        let proposal_num = proposer.prepare("value1".to_string(), 5);

        assert_eq!(proposal_num, 5); // 0 + 5
        assert_eq!(proposer.phase, Phase::Prepare);
        assert_eq!(proposer.get_value_to_propose(), Some("value1".to_string()));
    }

    #[test]
    fn test_proposer_receives_majority_promises() {
        let mut proposer = Proposer::new(0);
        proposer.prepare("value1".to_string(), 5);

        // Receive promises from 3 out of 5 acceptors
        let ready = proposer.receive_promise(0, Promise { proposal_number: 5, accepted_proposal: None }, 5);
        assert!(!ready);

        let ready = proposer.receive_promise(1, Promise { proposal_number: 5, accepted_proposal: None }, 5);
        assert!(!ready);

        let ready = proposer.receive_promise(2, Promise { proposal_number: 5, accepted_proposal: None }, 5);
        assert!(ready); // Now have majority (3/5)
        assert_eq!(proposer.phase, Phase::Accept);
    }

    #[test]
    fn test_proposer_must_use_accepted_value() {
        let mut proposer = Proposer::new(0);
        proposer.prepare("value1".to_string(), 5);

        // Acceptor 0 has previously accepted a different value
        let old_proposal = Proposal::new(3, "old_value".to_string());
        proposer.receive_promise(0, Promise {
            proposal_number: 5,
            accepted_proposal: Some(old_proposal),
        }, 3);

        // Acceptor 1 has no previous acceptance
        proposer.receive_promise(1, Promise {
            proposal_number: 5,
            accepted_proposal: None,
        }, 3);

        // Should now use "old_value" instead of "value1"
        assert_eq!(proposer.get_value_to_propose(), Some("old_value".to_string()));
    }

    #[test]
    fn test_proposer_uses_highest_accepted_value() {
        let mut proposer = Proposer::new(0);
        proposer.prepare("value1".to_string(), 5);

        // Two acceptors with different accepted values
        proposer.receive_promise(0, Promise {
            proposal_number: 5,
            accepted_proposal: Some(Proposal::new(2, "value_a".to_string())),
        }, 3);

        proposer.receive_promise(1, Promise {
            proposal_number: 5,
            accepted_proposal: Some(Proposal::new(4, "value_b".to_string())),
        }, 3);

        // Should use value from highest-numbered proposal (4 > 2)
        assert_eq!(proposer.get_value_to_propose(), Some("value_b".to_string()));
    }

    #[test]
    fn test_full_paxos_single_proposer() {
        let mut cluster = PaxosCluster::new(3);
        cluster.add_proposer(0);

        let result = cluster.run_paxos(0, "my_value".to_string());

        assert_eq!(result, Some("my_value".to_string()));
        assert!(cluster.get_proposer(0).unwrap().is_decided());
    }

    #[test]
    fn test_acceptor_updates_promise() {
        let mut acceptor = Acceptor::new(0);

        acceptor.receive_prepare(10);
        assert_eq!(acceptor.promised_number, Some(10));

        acceptor.receive_prepare(20);
        assert_eq!(acceptor.promised_number, Some(20));
    }

    #[test]
    fn test_promise_includes_accepted_proposal() {
        let mut acceptor = Acceptor::new(0);

        acceptor.receive_prepare(10);
        acceptor.receive_accept_request(Proposal::new(10, "value1".to_string()));

        let promise = acceptor.receive_prepare(20).unwrap();
        assert_eq!(promise.proposal_number, 20);
        assert_eq!(promise.accepted_proposal, Some(Proposal::new(10, "value1".to_string())));
    }

    #[test]
    fn test_consensus_reached() {
        let mut cluster = PaxosCluster::new(5);
        cluster.add_proposer(0);

        cluster.run_paxos(0, "consensus_value".to_string());

        // Check that majority of acceptors accepted the value
        let mut count = 0;
        for i in 0..5 {
            if let Some(acceptor) = cluster.get_acceptor(i) {
                if acceptor.get_accepted_value() == Some("consensus_value".to_string()) {
                    count += 1;
                }
            }
        }

        assert!(count >= 3); // Majority of 5
    }

    #[test]
    fn test_proposal_number_uniqueness() {
        let proposer1 = Proposer::new(0);
        let proposer2 = Proposer::new(1);
        let proposer3 = Proposer::new(2);

        // With cluster_size 3, proposals will be 0+3=3, 1+3=4, 2+3=5
        assert_eq!(proposer1.proposal_number, 0);
        assert_eq!(proposer2.proposal_number, 1);
        assert_eq!(proposer3.proposal_number, 2);
    }
}
