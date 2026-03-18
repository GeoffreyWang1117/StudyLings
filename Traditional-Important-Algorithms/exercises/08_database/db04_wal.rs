// db04_wal.rs
//
// Write-Ahead Logging (WAL) is a technique used to ensure durability and atomicity
// in database systems. All modifications are first written to a log before being
// applied to the database. This allows for:
// - Recovery after crashes (replay the log)
// - Atomicity (all-or-nothing transactions)
// - Durability (changes persist even if the system crashes)
//
// WAL sequence:
// 1. Write operation to log
// 2. Flush log to disk
// 3. Apply operation to database
// 4. Checkpoint (periodically mark log entries as applied)
//
// Your task: Implement a Write-Ahead Log with recovery capabilities.

// I AM NOT DONE

use std::collections::HashMap;
use std::fmt::Debug;

#[derive(Debug, Clone, PartialEq)]
pub enum LogEntry<K: Clone + Debug, V: Clone + Debug> {
    Put { key: K, value: V },
    Delete { key: K },
    BeginTransaction { tx_id: u64 },
    Commit { tx_id: u64 },
    Abort { tx_id: u64 },
    Checkpoint { lsn: u64 }, // Log Sequence Number
}

pub struct WAL<K: Clone + Debug + Eq + std::hash::Hash, V: Clone + Debug> {
    log: Vec<LogEntry<K, V>>,
    data: HashMap<K, V>,
    next_lsn: u64,
    last_checkpoint: u64,
}

impl<K: Clone + Debug + Eq + std::hash::Hash, V: Clone + Debug> WAL<K, V> {
    pub fn new() -> Self {
        Self {
            log: Vec::new(),
            data: HashMap::new(),
            next_lsn: 0,
            last_checkpoint: 0,
        }
    }

    pub fn begin_transaction(&mut self, tx_id: u64) {
        // TODO: Write a BeginTransaction entry to the log
        todo!()
    }

    pub fn put(&mut self, key: K, value: V) {
        // TODO: Write the Put operation to the log first
        // Then apply it to the in-memory data structure
        todo!()
    }

    pub fn delete(&mut self, key: K) {
        // TODO: Write the Delete operation to the log first
        // Then apply it to the in-memory data structure
        todo!()
    }

    pub fn commit(&mut self, tx_id: u64) {
        // TODO: Write a Commit entry to the log
        // This marks the transaction as durable
        todo!()
    }

    pub fn abort(&mut self, tx_id: u64) {
        // TODO: Write an Abort entry to the log
        // Roll back any changes made by this transaction
        todo!()
    }

    pub fn get(&self, key: &K) -> Option<&V> {
        self.data.get(key)
    }

    pub fn checkpoint(&mut self) {
        // TODO: Create a checkpoint
        // Record the current LSN
        // In a real system, this would also flush all dirty pages to disk
        todo!()
    }

    pub fn recover(&mut self) {
        // TODO: Recover from the log
        // Replay all log entries from the last checkpoint
        // For each transaction:
        //   - If committed, apply all operations
        //   - If aborted or incomplete, ignore operations
        todo!()
    }

    pub fn log_size(&self) -> usize {
        self.log.len()
    }

    pub fn truncate_log(&mut self) {
        // TODO: Remove log entries before the last checkpoint
        // This is safe because those operations have been applied to the database
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_wal() {
        let wal: WAL<String, i32> = WAL::new();
        assert_eq!(wal.log_size(), 0);
    }

    #[test]
    fn test_simple_put_and_get() {
        let mut wal = WAL::new();
        wal.put("key1".to_string(), 100);
        assert_eq!(wal.get(&"key1".to_string()), Some(&100));
    }

    #[test]
    fn test_delete() {
        let mut wal = WAL::new();
        wal.put("key1".to_string(), 100);
        assert_eq!(wal.get(&"key1".to_string()), Some(&100));

        wal.delete("key1".to_string());
        assert_eq!(wal.get(&"key1".to_string()), None);
    }

    #[test]
    fn test_transaction_commit() {
        let mut wal = WAL::new();

        wal.begin_transaction(1);
        wal.put("key1".to_string(), 100);
        wal.put("key2".to_string(), 200);
        wal.commit(1);

        assert_eq!(wal.get(&"key1".to_string()), Some(&100));
        assert_eq!(wal.get(&"key2".to_string()), Some(&200));
    }

    #[test]
    fn test_transaction_abort() {
        let mut wal = WAL::new();

        wal.put("key1".to_string(), 100);

        wal.begin_transaction(1);
        wal.put("key1".to_string(), 200);
        wal.put("key2".to_string(), 300);
        wal.abort(1);

        // After abort, changes should be rolled back
        assert_eq!(wal.get(&"key1".to_string()), Some(&100));
        assert_eq!(wal.get(&"key2".to_string()), None);
    }

    #[test]
    fn test_checkpoint() {
        let mut wal = WAL::new();

        wal.put("key1".to_string(), 100);
        wal.put("key2".to_string(), 200);

        let size_before = wal.log_size();
        wal.checkpoint();

        assert!(wal.log_size() >= size_before);
    }

    #[test]
    fn test_recovery_after_checkpoint() {
        let mut wal = WAL::new();

        wal.put("key1".to_string(), 100);
        wal.checkpoint();
        wal.put("key2".to_string(), 200);

        // Simulate crash and recovery
        wal.data.clear();
        wal.recover();

        assert_eq!(wal.get(&"key1".to_string()), Some(&100));
        assert_eq!(wal.get(&"key2".to_string()), Some(&200));
    }

    #[test]
    fn test_recovery_uncommitted_transaction() {
        let mut wal = WAL::new();

        wal.put("key1".to_string(), 100);
        wal.begin_transaction(1);
        wal.put("key2".to_string(), 200);
        // Transaction 1 never commits

        // Simulate crash and recovery
        wal.data.clear();
        wal.recover();

        // key1 should be recovered, but key2 should not (uncommitted)
        assert_eq!(wal.get(&"key1".to_string()), Some(&100));
        assert_eq!(wal.get(&"key2".to_string()), None);
    }

    #[test]
    fn test_truncate_log() {
        let mut wal = WAL::new();

        wal.put("key1".to_string(), 100);
        wal.checkpoint();
        let checkpoint_size = wal.log_size();

        wal.put("key2".to_string(), 200);
        assert!(wal.log_size() > checkpoint_size);

        wal.truncate_log();
        // Log size should be reduced after truncation
        assert!(wal.log_size() <= checkpoint_size + 2);
    }

    #[test]
    fn test_multiple_transactions() {
        let mut wal = WAL::new();

        wal.begin_transaction(1);
        wal.put("key1".to_string(), 100);
        wal.commit(1);

        wal.begin_transaction(2);
        wal.put("key2".to_string(), 200);
        wal.commit(2);

        assert_eq!(wal.get(&"key1".to_string()), Some(&100));
        assert_eq!(wal.get(&"key2".to_string()), Some(&200));
    }

    #[test]
    fn test_interleaved_transactions() {
        let mut wal = WAL::new();

        wal.begin_transaction(1);
        wal.put("key1".to_string(), 100);

        wal.begin_transaction(2);
        wal.put("key2".to_string(), 200);

        wal.commit(1);
        wal.commit(2);

        assert_eq!(wal.get(&"key1".to_string()), Some(&100));
        assert_eq!(wal.get(&"key2".to_string()), Some(&200));
    }

    #[test]
    fn test_recovery_with_multiple_checkpoints() {
        let mut wal = WAL::new();

        wal.put("key1".to_string(), 100);
        wal.checkpoint();
        wal.put("key2".to_string(), 200);
        wal.checkpoint();
        wal.put("key3".to_string(), 300);

        wal.data.clear();
        wal.recover();

        assert_eq!(wal.get(&"key1".to_string()), Some(&100));
        assert_eq!(wal.get(&"key2".to_string()), Some(&200));
        assert_eq!(wal.get(&"key3".to_string()), Some(&300));
    }
}
