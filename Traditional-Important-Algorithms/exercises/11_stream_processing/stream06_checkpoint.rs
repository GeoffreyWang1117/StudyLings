// stream06_checkpoint.rs
//
// Checkpointing is a fault tolerance mechanism in stream processing that
// periodically saves the state of the computation. If a failure occurs,
// the system can restore from the last checkpoint and replay events.
//
// Key concepts:
// - Consistent snapshots across distributed operators
// - Checkpoint barriers (Chandy-Lamport algorithm)
// - State serialization and recovery
// - Trade-off between checkpoint frequency and overhead
//
// Your task: Implement a checkpoint coordinator that manages state snapshots
// and recovery for stream processing operators.
//
// Key features:
// - Barrier-based checkpointing
// - State save and restore
// - Checkpoint alignment
// - Incremental checkpoints

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub struct CheckpointBarrier {
    pub checkpoint_id: u64,
    pub timestamp: u64,
}

#[derive(Debug, Clone)]
pub struct OperatorState {
    pub operator_id: String,
    pub checkpoint_id: u64,
    pub state_data: HashMap<String, Vec<u8>>, // Key-value state
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum CheckpointStatus {
    InProgress,
    Completed,
    Failed,
}

pub struct Checkpoint {
    pub id: u64,
    pub timestamp: u64,
    pub status: CheckpointStatus,
    pub operator_states: HashMap<String, OperatorState>,
}

pub struct CheckpointCoordinator {
    next_checkpoint_id: u64,
    active_checkpoints: HashMap<u64, Checkpoint>,
    completed_checkpoints: Vec<Checkpoint>,
    checkpoint_interval: u64, // milliseconds
    last_checkpoint_time: u64,
    max_retained_checkpoints: usize,
}

impl CheckpointCoordinator {
    pub fn new(checkpoint_interval: u64, max_retained: usize) -> Self {
        // TODO: Initialize checkpoint coordinator
        // - Set checkpoint interval and retention policy
        // - Initialize empty checkpoint tracking structures
        todo!()
    }

    pub fn should_trigger_checkpoint(&self, current_time: u64) -> bool {
        // TODO: Determine if it's time to trigger a new checkpoint
        // - Check if enough time has passed since last checkpoint
        todo!()
    }

    pub fn trigger_checkpoint(&mut self, timestamp: u64) -> CheckpointBarrier {
        // TODO: Trigger a new checkpoint
        // - Generate new checkpoint ID
        // - Create checkpoint barrier
        // - Initialize checkpoint in active_checkpoints
        // - Update last_checkpoint_time
        // - Return barrier to be sent to operators
        todo!()
    }

    pub fn acknowledge_checkpoint(&mut self, checkpoint_id: u64, operator_state: OperatorState) {
        // TODO: Record operator's checkpoint acknowledgment
        // - Add operator state to the checkpoint
        // - Check if all operators have acknowledged (for simplicity, assume single operator)
        // - If complete, finalize checkpoint
        todo!()
    }

    fn finalize_checkpoint(&mut self, checkpoint_id: u64) {
        // TODO: Mark checkpoint as completed
        // - Update status to Completed
        // - Move to completed_checkpoints
        // - Remove from active_checkpoints
        // - Trim old checkpoints based on retention policy
        todo!()
    }

    pub fn get_latest_checkpoint(&self) -> Option<&Checkpoint> {
        // TODO: Return the most recent completed checkpoint
        todo!()
    }

    pub fn restore_from_checkpoint(&self, checkpoint_id: u64) -> Option<&Checkpoint> {
        // TODO: Get checkpoint for restoration
        // - Find checkpoint by ID in completed checkpoints
        todo!()
    }

    pub fn fail_checkpoint(&mut self, checkpoint_id: u64) {
        // TODO: Mark checkpoint as failed
        // - Update status to Failed
        // - Clean up from active_checkpoints
        todo!()
    }

    pub fn get_checkpoint_statistics(&self) -> CheckpointStats {
        // TODO: Return statistics about checkpointing
        todo!()
    }

    fn trim_old_checkpoints(&mut self) {
        // TODO: Keep only the most recent N checkpoints
        // - Remove oldest checkpoints beyond retention limit
        todo!()
    }
}

#[derive(Debug)]
pub struct CheckpointStats {
    pub total_completed: usize,
    pub total_failed: usize,
    pub active_count: usize,
    pub latest_checkpoint_id: Option<u64>,
}

pub struct StatefulOperator {
    operator_id: String,
    state: HashMap<String, Vec<u8>>,
    pending_barrier: Option<CheckpointBarrier>,
}

impl StatefulOperator {
    pub fn new(operator_id: String) -> Self {
        // TODO: Initialize stateful operator
        todo!()
    }

    pub fn update_state(&mut self, key: String, value: Vec<u8>) {
        // TODO: Update operator state
        todo!()
    }

    pub fn get_state(&self, key: &str) -> Option<&Vec<u8>> {
        // TODO: Get state value by key
        todo!()
    }

    pub fn receive_barrier(&mut self, barrier: CheckpointBarrier) -> OperatorState {
        // TODO: Handle checkpoint barrier
        // - Save current barrier
        // - Create snapshot of current state
        // - Return OperatorState for this checkpoint
        todo!()
    }

    pub fn restore_state(&mut self, operator_state: &OperatorState) {
        // TODO: Restore state from checkpoint
        // - Replace current state with checkpoint state
        // - Clear pending barrier
        todo!()
    }

    pub fn state_size(&self) -> usize {
        // TODO: Return number of state entries
        todo!()
    }
}

pub struct IncrementalCheckpoint {
    base_checkpoint_id: u64,
    incremental_states: Vec<(u64, HashMap<String, Vec<u8>>)>, // (checkpoint_id, changed_keys)
}

impl IncrementalCheckpoint {
    pub fn new(base_checkpoint_id: u64) -> Self {
        // TODO: Initialize incremental checkpoint
        // - Store base checkpoint ID
        // - Initialize empty incremental states
        todo!()
    }

    pub fn add_incremental(&mut self, checkpoint_id: u64, changed_state: HashMap<String, Vec<u8>>) {
        // TODO: Add incremental state change
        // - Only store keys that changed since base
        todo!()
    }

    pub fn reconstruct_full_state(&self, base_state: &HashMap<String, Vec<u8>>) -> HashMap<String, Vec<u8>> {
        // TODO: Reconstruct full state from base + incrementals
        // - Start with base state
        // - Apply incremental changes in order
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_checkpoint_coordinator_creation() {
        let coordinator = CheckpointCoordinator::new(5000, 3);
        assert_eq!(coordinator.checkpoint_interval, 5000);
        assert_eq!(coordinator.max_retained_checkpoints, 3);
    }

    #[test]
    fn test_trigger_checkpoint() {
        let mut coordinator = CheckpointCoordinator::new(5000, 3);

        let barrier = coordinator.trigger_checkpoint(1000);
        assert_eq!(barrier.checkpoint_id, 1);
        assert_eq!(barrier.timestamp, 1000);
    }

    #[test]
    fn test_checkpoint_timing() {
        let mut coordinator = CheckpointCoordinator::new(5000, 3);

        assert!(coordinator.should_trigger_checkpoint(0));

        coordinator.trigger_checkpoint(0);

        assert!(!coordinator.should_trigger_checkpoint(3000));
        assert!(coordinator.should_trigger_checkpoint(6000));
    }

    #[test]
    fn test_acknowledge_checkpoint() {
        let mut coordinator = CheckpointCoordinator::new(5000, 3);

        let barrier = coordinator.trigger_checkpoint(1000);

        let mut state_data = HashMap::new();
        state_data.insert("key1".to_string(), vec![1, 2, 3]);

        let operator_state = OperatorState {
            operator_id: "op1".to_string(),
            checkpoint_id: barrier.checkpoint_id,
            state_data,
        };

        coordinator.acknowledge_checkpoint(barrier.checkpoint_id, operator_state);

        let latest = coordinator.get_latest_checkpoint();
        assert!(latest.is_some());
        assert_eq!(latest.unwrap().id, 1);
    }

    #[test]
    fn test_checkpoint_retention() {
        let mut coordinator = CheckpointCoordinator::new(5000, 2);

        // Create 3 checkpoints
        for i in 0..3 {
            let barrier = coordinator.trigger_checkpoint(i * 5000);
            let operator_state = OperatorState {
                operator_id: "op1".to_string(),
                checkpoint_id: barrier.checkpoint_id,
                state_data: HashMap::new(),
            };
            coordinator.acknowledge_checkpoint(barrier.checkpoint_id, operator_state);
        }

        // Should only retain 2 most recent
        let stats = coordinator.get_checkpoint_statistics();
        assert!(stats.total_completed <= 2);
    }

    #[test]
    fn test_checkpoint_failure() {
        let mut coordinator = CheckpointCoordinator::new(5000, 3);

        let barrier = coordinator.trigger_checkpoint(1000);
        coordinator.fail_checkpoint(barrier.checkpoint_id);

        let latest = coordinator.get_latest_checkpoint();
        assert!(latest.is_none()); // No completed checkpoints
    }

    #[test]
    fn test_stateful_operator() {
        let mut operator = StatefulOperator::new("op1".to_string());

        operator.update_state("counter".to_string(), vec![0, 0, 0, 5]);
        assert_eq!(operator.state_size(), 1);

        let value = operator.get_state("counter");
        assert_eq!(value, Some(&vec![0, 0, 0, 5]));
    }

    #[test]
    fn test_operator_checkpoint() {
        let mut operator = StatefulOperator::new("op1".to_string());

        operator.update_state("key1".to_string(), vec![1, 2, 3]);
        operator.update_state("key2".to_string(), vec![4, 5, 6]);

        let barrier = CheckpointBarrier {
            checkpoint_id: 1,
            timestamp: 1000,
        };

        let state = operator.receive_barrier(barrier);

        assert_eq!(state.checkpoint_id, 1);
        assert_eq!(state.operator_id, "op1");
        assert_eq!(state.state_data.len(), 2);
    }

    #[test]
    fn test_operator_restore() {
        let mut operator = StatefulOperator::new("op1".to_string());

        operator.update_state("key1".to_string(), vec![1, 2, 3]);

        let mut checkpoint_state = HashMap::new();
        checkpoint_state.insert("key2".to_string(), vec![4, 5, 6]);
        checkpoint_state.insert("key3".to_string(), vec![7, 8, 9]);

        let operator_state = OperatorState {
            operator_id: "op1".to_string(),
            checkpoint_id: 1,
            state_data: checkpoint_state,
        };

        operator.restore_state(&operator_state);

        assert_eq!(operator.state_size(), 2);
        assert!(operator.get_state("key1").is_none()); // Old state replaced
        assert!(operator.get_state("key2").is_some());
        assert!(operator.get_state("key3").is_some());
    }

    #[test]
    fn test_restore_from_checkpoint() {
        let mut coordinator = CheckpointCoordinator::new(5000, 3);

        let barrier = coordinator.trigger_checkpoint(1000);

        let mut state_data = HashMap::new();
        state_data.insert("counter".to_string(), vec![0, 0, 0, 42]);

        let operator_state = OperatorState {
            operator_id: "op1".to_string(),
            checkpoint_id: barrier.checkpoint_id,
            state_data,
        };

        coordinator.acknowledge_checkpoint(barrier.checkpoint_id, operator_state);

        let restored = coordinator.restore_from_checkpoint(1);
        assert!(restored.is_some());
        assert_eq!(restored.unwrap().id, 1);
    }

    #[test]
    fn test_incremental_checkpoint() {
        let mut incremental = IncrementalCheckpoint::new(1);

        let mut changes1 = HashMap::new();
        changes1.insert("key1".to_string(), vec![1, 2, 3]);
        incremental.add_incremental(2, changes1);

        let mut changes2 = HashMap::new();
        changes2.insert("key2".to_string(), vec![4, 5, 6]);
        incremental.add_incremental(3, changes2);

        let mut base = HashMap::new();
        base.insert("key0".to_string(), vec![0]);

        let full_state = incremental.reconstruct_full_state(&base);
        assert_eq!(full_state.len(), 3);
        assert!(full_state.contains_key("key0"));
        assert!(full_state.contains_key("key1"));
        assert!(full_state.contains_key("key2"));
    }

    #[test]
    fn test_checkpoint_statistics() {
        let mut coordinator = CheckpointCoordinator::new(5000, 3);

        coordinator.trigger_checkpoint(1000);
        coordinator.trigger_checkpoint(6000);

        let stats = coordinator.get_checkpoint_statistics();
        assert_eq!(stats.active_count, 2);
    }
}
