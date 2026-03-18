// dist10_two_phase_commit.rs
//
// Two-Phase Commit (2PC) is a distributed algorithm that ensures all participants
// in a distributed transaction either commit or abort together. It's crucial for
// maintaining ACID properties across distributed databases.
//
// Protocol phases:
// 1. Prepare Phase: Coordinator asks all participants to prepare (vote yes/no)
// 2. Commit Phase: If all vote yes, coordinator tells all to commit; otherwise abort
//
// Your task: Implement the Two-Phase Commit protocol with coordinator and participants.
//
// Key concepts:
// - Coordinator: Orchestrates the transaction
// - Participants: Nodes that execute parts of the transaction
// - Prepare: Participant locks resources and votes
// - Commit/Abort: Final decision applied atomically
// - Blocking: Protocol blocks if coordinator fails (limitation of 2PC)

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Vote {
    Yes,
    No,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ParticipantState {
    Idle,
    Prepared,
    Committed,
    Aborted,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum CoordinatorState {
    Idle,
    Preparing,
    Committing,
    Aborting,
    Committed,
    Aborted,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TransactionResult {
    Committed,
    Aborted,
    InProgress,
}

#[derive(Debug, Clone)]
pub struct Transaction {
    pub id: usize,
    pub operations: Vec<String>,
}

impl Transaction {
    pub fn new(id: usize, operations: Vec<String>) -> Self {
        Self { id, operations }
    }
}

pub struct Participant {
    pub id: usize,
    pub state: ParticipantState,
    pub prepared_transactions: HashMap<usize, Transaction>,
    pub committed_transactions: HashMap<usize, Transaction>,
    pub vote_to_abort: bool,  // Simulates failures
}

impl Participant {
    pub fn new(id: usize) -> Self {
        Self {
            id,
            state: ParticipantState::Idle,
            prepared_transactions: HashMap::new(),
            committed_transactions: HashMap::new(),
            vote_to_abort: false,
        }
    }

    pub fn prepare(&mut self, transaction: Transaction) -> Vote {
        // TODO: Handle prepare request
        // - If vote_to_abort is true, return Vote::No
        // - Otherwise, store transaction in prepared_transactions
        // - Change state to Prepared
        // - Return Vote::Yes
        todo!()
    }

    pub fn commit(&mut self, transaction_id: usize) -> bool {
        // TODO: Handle commit request
        // - Must be in Prepared state
        // - Move transaction from prepared_transactions to committed_transactions
        // - Change state to Committed
        // - Return true if successful, false otherwise
        todo!()
    }

    pub fn abort(&mut self, transaction_id: usize) -> bool {
        // TODO: Handle abort request
        // - Remove transaction from prepared_transactions
        // - Change state to Aborted
        // - Return true
        todo!()
    }

    pub fn set_vote_to_abort(&mut self, should_abort: bool) {
        self.vote_to_abort = should_abort;
    }

    pub fn is_transaction_committed(&self, transaction_id: usize) -> bool {
        self.committed_transactions.contains_key(&transaction_id)
    }

    pub fn reset(&mut self) {
        self.state = ParticipantState::Idle;
    }
}

pub struct Coordinator {
    pub state: CoordinatorState,
    pub transaction: Option<Transaction>,
    pub votes: HashMap<usize, Vote>,
    pub participants: Vec<usize>,
}

impl Coordinator {
    pub fn new() -> Self {
        Self {
            state: CoordinatorState::Idle,
            transaction: None,
            votes: HashMap::new(),
            participants: Vec::new(),
        }
    }

    pub fn add_participant(&mut self, participant_id: usize) {
        self.participants.push(participant_id);
    }

    pub fn start_transaction(&mut self, transaction: Transaction) {
        // TODO: Start a new transaction
        // - Store the transaction
        // - Clear votes
        // - Change state to Preparing
        todo!()
    }

    pub fn receive_vote(&mut self, participant_id: usize, vote: Vote) {
        // TODO: Record a vote from a participant
        // - Store the vote in votes HashMap
        todo!()
    }

    pub fn has_all_votes(&self) -> bool {
        // TODO: Check if all participants have voted
        // - Compare votes.len() with participants.len()
        todo!()
    }

    pub fn should_commit(&self) -> bool {
        // TODO: Determine if transaction should commit
        // - All votes must be Yes
        // - Return false if any vote is No or not all votes received
        todo!()
    }

    pub fn decide(&mut self) -> TransactionResult {
        // TODO: Make commit/abort decision
        // - Must have all votes
        // - If should_commit(), change state to Committing, return Committed
        // - Otherwise, change state to Aborting, return Aborted
        // - If not all votes, return InProgress
        todo!()
    }

    pub fn finalize_commit(&mut self) {
        self.state = CoordinatorState::Committed;
    }

    pub fn finalize_abort(&mut self) {
        self.state = CoordinatorState::Aborted;
    }

    pub fn reset(&mut self) {
        self.state = CoordinatorState::Idle;
        self.transaction = None;
        self.votes.clear();
    }
}

pub struct TwoPhaseCommitSystem {
    coordinator: Coordinator,
    participants: HashMap<usize, Participant>,
    transaction_counter: usize,
}

impl TwoPhaseCommitSystem {
    pub fn new() -> Self {
        Self {
            coordinator: Coordinator::new(),
            participants: HashMap::new(),
            transaction_counter: 0,
        }
    }

    pub fn add_participant(&mut self, participant_id: usize) {
        self.participants.insert(participant_id, Participant::new(participant_id));
        self.coordinator.add_participant(participant_id);
    }

    pub fn set_participant_vote(&mut self, participant_id: usize, vote_to_abort: bool) {
        if let Some(participant) = self.participants.get_mut(&participant_id) {
            participant.set_vote_to_abort(vote_to_abort);
        }
    }

    pub fn execute_transaction(&mut self, operations: Vec<String>) -> TransactionResult {
        // TODO: Execute a complete 2PC transaction
        //
        // Phase 1: Prepare
        // - Create transaction with next transaction_id
        // - Start transaction on coordinator
        // - Send prepare to all participants
        // - Collect votes and send to coordinator
        //
        // Phase 2: Commit or Abort
        // - Coordinator decides based on votes
        // - If Committed: send commit to all participants
        // - If Aborted: send abort to all participants
        // - Finalize coordinator state
        // - Return result
        todo!()
    }

    pub fn phase1_prepare(&mut self, transaction: Transaction) -> HashMap<usize, Vote> {
        // TODO: Execute Phase 1 (Prepare)
        // - For each participant, call prepare
        // - Collect and return all votes
        todo!()
    }

    pub fn phase2_commit(&mut self, transaction_id: usize) {
        // TODO: Execute Phase 2 Commit
        // - For each participant, call commit
        // - Finalize coordinator
        todo!()
    }

    pub fn phase2_abort(&mut self, transaction_id: usize) {
        // TODO: Execute Phase 2 Abort
        // - For each participant, call abort
        // - Finalize coordinator
        todo!()
    }

    pub fn get_coordinator_state(&self) -> CoordinatorState {
        self.coordinator.state
    }

    pub fn get_participant_state(&self, participant_id: usize) -> Option<ParticipantState> {
        self.participants.get(&participant_id).map(|p| p.state)
    }

    pub fn is_transaction_committed(&self, transaction_id: usize) -> bool {
        // Check if all participants have committed the transaction
        self.participants
            .values()
            .all(|p| p.is_transaction_committed(transaction_id))
    }

    pub fn reset_all(&mut self) {
        self.coordinator.reset();
        for participant in self.participants.values_mut() {
            participant.reset();
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_participant_prepare_yes() {
        let mut participant = Participant::new(1);
        let tx = Transaction::new(1, vec!["INSERT INTO table".to_string()]);

        let vote = participant.prepare(tx);

        assert_eq!(vote, Vote::Yes);
        assert_eq!(participant.state, ParticipantState::Prepared);
        assert!(participant.prepared_transactions.contains_key(&1));
    }

    #[test]
    fn test_participant_prepare_no() {
        let mut participant = Participant::new(1);
        participant.set_vote_to_abort(true);

        let tx = Transaction::new(1, vec!["INSERT INTO table".to_string()]);
        let vote = participant.prepare(tx);

        assert_eq!(vote, Vote::No);
    }

    #[test]
    fn test_participant_commit() {
        let mut participant = Participant::new(1);
        let tx = Transaction::new(1, vec!["INSERT INTO table".to_string()]);

        participant.prepare(tx);
        let success = participant.commit(1);

        assert!(success);
        assert_eq!(participant.state, ParticipantState::Committed);
        assert!(participant.is_transaction_committed(1));
        assert!(!participant.prepared_transactions.contains_key(&1));
    }

    #[test]
    fn test_participant_abort() {
        let mut participant = Participant::new(1);
        let tx = Transaction::new(1, vec!["INSERT INTO table".to_string()]);

        participant.prepare(tx);
        let success = participant.abort(1);

        assert!(success);
        assert_eq!(participant.state, ParticipantState::Aborted);
        assert!(!participant.prepared_transactions.contains_key(&1));
    }

    #[test]
    fn test_coordinator_all_yes_votes() {
        let mut coordinator = Coordinator::new();
        coordinator.add_participant(1);
        coordinator.add_participant(2);

        let tx = Transaction::new(1, vec!["UPDATE table".to_string()]);
        coordinator.start_transaction(tx);

        coordinator.receive_vote(1, Vote::Yes);
        coordinator.receive_vote(2, Vote::Yes);

        assert!(coordinator.has_all_votes());
        assert!(coordinator.should_commit());
    }

    #[test]
    fn test_coordinator_one_no_vote() {
        let mut coordinator = Coordinator::new();
        coordinator.add_participant(1);
        coordinator.add_participant(2);

        let tx = Transaction::new(1, vec!["UPDATE table".to_string()]);
        coordinator.start_transaction(tx);

        coordinator.receive_vote(1, Vote::Yes);
        coordinator.receive_vote(2, Vote::No);

        assert!(coordinator.has_all_votes());
        assert!(!coordinator.should_commit());
    }

    #[test]
    fn test_coordinator_decide_commit() {
        let mut coordinator = Coordinator::new();
        coordinator.add_participant(1);
        coordinator.add_participant(2);

        let tx = Transaction::new(1, vec!["UPDATE table".to_string()]);
        coordinator.start_transaction(tx);

        coordinator.receive_vote(1, Vote::Yes);
        coordinator.receive_vote(2, Vote::Yes);

        let result = coordinator.decide();
        assert_eq!(result, TransactionResult::Committed);
        assert_eq!(coordinator.state, CoordinatorState::Committing);
    }

    #[test]
    fn test_coordinator_decide_abort() {
        let mut coordinator = Coordinator::new();
        coordinator.add_participant(1);

        let tx = Transaction::new(1, vec!["UPDATE table".to_string()]);
        coordinator.start_transaction(tx);

        coordinator.receive_vote(1, Vote::No);

        let result = coordinator.decide();
        assert_eq!(result, TransactionResult::Aborted);
        assert_eq!(coordinator.state, CoordinatorState::Aborting);
    }

    #[test]
    fn test_full_commit_transaction() {
        let mut system = TwoPhaseCommitSystem::new();
        system.add_participant(1);
        system.add_participant(2);
        system.add_participant(3);

        let result = system.execute_transaction(vec![
            "INSERT INTO users VALUES (1, 'Alice')".to_string(),
            "INSERT INTO accounts VALUES (1, 100)".to_string(),
        ]);

        assert_eq!(result, TransactionResult::Committed);
        assert_eq!(system.get_coordinator_state(), CoordinatorState::Committed);

        // All participants should have committed
        for i in 1..=3 {
            assert_eq!(system.get_participant_state(i), Some(ParticipantState::Committed));
        }
    }

    #[test]
    fn test_abort_due_to_participant_failure() {
        let mut system = TwoPhaseCommitSystem::new();
        system.add_participant(1);
        system.add_participant(2);
        system.add_participant(3);

        // Participant 2 will vote to abort
        system.set_participant_vote(2, true);

        let result = system.execute_transaction(vec![
            "INSERT INTO users VALUES (1, 'Bob')".to_string(),
        ]);

        assert_eq!(result, TransactionResult::Aborted);
        assert_eq!(system.get_coordinator_state(), CoordinatorState::Aborted);

        // All participants should have aborted
        for i in 1..=3 {
            assert_eq!(system.get_participant_state(i), Some(ParticipantState::Aborted));
        }
    }

    #[test]
    fn test_phase1_prepare() {
        let mut system = TwoPhaseCommitSystem::new();
        system.add_participant(1);
        system.add_participant(2);

        let tx = Transaction::new(1, vec!["UPDATE table".to_string()]);
        let votes = system.phase1_prepare(tx);

        assert_eq!(votes.len(), 2);
        assert_eq!(votes.get(&1), Some(&Vote::Yes));
        assert_eq!(votes.get(&2), Some(&Vote::Yes));
    }

    #[test]
    fn test_atomicity_all_or_nothing() {
        let mut system = TwoPhaseCommitSystem::new();
        system.add_participant(1);
        system.add_participant(2);

        system.set_participant_vote(1, true); // Will abort

        system.execute_transaction(vec!["UPDATE table".to_string()]);

        // Neither participant should have committed
        assert!(!system.is_transaction_committed(1));
    }

    #[test]
    fn test_multiple_transactions() {
        let mut system = TwoPhaseCommitSystem::new();
        system.add_participant(1);
        system.add_participant(2);

        let result1 = system.execute_transaction(vec!["TX1".to_string()]);
        assert_eq!(result1, TransactionResult::Committed);

        system.reset_all();

        let result2 = system.execute_transaction(vec!["TX2".to_string()]);
        assert_eq!(result2, TransactionResult::Committed);
    }

    #[test]
    fn test_single_participant() {
        let mut system = TwoPhaseCommitSystem::new();
        system.add_participant(1);

        let result = system.execute_transaction(vec!["SINGLE OP".to_string()]);
        assert_eq!(result, TransactionResult::Committed);
    }

    #[test]
    fn test_all_participants_vote_no() {
        let mut system = TwoPhaseCommitSystem::new();
        system.add_participant(1);
        system.add_participant(2);

        system.set_participant_vote(1, true);
        system.set_participant_vote(2, true);

        let result = system.execute_transaction(vec!["UPDATE".to_string()]);
        assert_eq!(result, TransactionResult::Aborted);
    }
}
