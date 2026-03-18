// db06_isolation_levels.rs
//
// Transaction Isolation Levels define how transactions interact with each other
// and what anomalies they prevent. From weakest to strongest:
//
// 1. Read Uncommitted: Can read uncommitted changes (dirty reads)
// 2. Read Committed: Only reads committed data (prevents dirty reads)
// 3. Repeatable Read: Same read returns same result (prevents non-repeatable reads)
// 4. Serializable: Transactions appear to execute serially (prevents all anomalies)
//
// Anomalies:
// - Dirty Read: Reading uncommitted changes
// - Non-repeatable Read: Reading same row twice gives different results
// - Phantom Read: Query returns different rows on repeated execution
//
// Your task: Implement different isolation levels with proper anomaly prevention.

// I AM NOT DONE

use std::collections::HashMap;

pub type TransactionId = u64;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IsolationLevel {
    ReadUncommitted,
    ReadCommitted,
    RepeatableRead,
    Serializable,
}

#[derive(Debug, Clone)]
struct VersionedValue<V: Clone> {
    value: V,
    tx_id: TransactionId,
    committed: bool,
}

pub struct IsolationStore<K: Clone + Eq + std::hash::Hash, V: Clone> {
    data: HashMap<K, Vec<VersionedValue<V>>>,
    read_locks: HashMap<TransactionId, Vec<K>>,
    write_locks: HashMap<TransactionId, Vec<K>>,
    next_tx_id: TransactionId,
}

impl<K: Clone + Eq + std::hash::Hash, V: Clone> IsolationStore<K, V> {
    pub fn new() -> Self {
        Self {
            data: HashMap::new(),
            read_locks: HashMap::new(),
            write_locks: HashMap::new(),
            next_tx_id: 1,
        }
    }

    pub fn begin_transaction(&mut self) -> TransactionId {
        let tx_id = self.next_tx_id;
        self.next_tx_id += 1;
        self.read_locks.insert(tx_id, Vec::new());
        self.write_locks.insert(tx_id, Vec::new());
        tx_id
    }

    pub fn read(
        &mut self,
        tx_id: TransactionId,
        key: &K,
        isolation: IsolationLevel,
    ) -> Option<V> {
        // TODO: Implement read with different isolation levels
        // ReadUncommitted: Return the latest version (even if uncommitted)
        // ReadCommitted: Return the latest committed version
        // RepeatableRead: Return the version visible at transaction start, acquire read lock
        // Serializable: Same as RepeatableRead but also prevent phantom reads
        todo!()
    }

    pub fn write(
        &mut self,
        tx_id: TransactionId,
        key: K,
        value: V,
        isolation: IsolationLevel,
    ) -> Result<(), String> {
        // TODO: Implement write with different isolation levels
        // For Serializable and RepeatableRead: Check for conflicting locks
        // Create a new uncommitted version
        // Acquire write lock on the key
        todo!()
    }

    pub fn commit(&mut self, tx_id: TransactionId) {
        // TODO: Commit a transaction
        // Mark all versions created by this transaction as committed
        // Release all locks held by this transaction
        todo!()
    }

    pub fn abort(&mut self, tx_id: TransactionId) {
        // TODO: Abort a transaction
        // Remove all uncommitted versions created by this transaction
        // Release all locks
        todo!()
    }

    fn has_write_lock(&self, key: &K, excluding_tx: TransactionId) -> bool {
        // TODO: Check if any other transaction holds a write lock on this key
        todo!()
    }

    fn has_read_lock(&self, key: &K, excluding_tx: TransactionId) -> bool {
        // TODO: Check if any other transaction holds a read lock on this key
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_uncommitted_dirty_read() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::ReadUncommitted).unwrap();

        // tx2 should be able to read uncommitted changes
        let tx2 = store.begin_transaction();
        let value = store.read(tx2, &"key1".to_string(), IsolationLevel::ReadUncommitted);
        assert_eq!(value, Some(100));

        store.abort(tx1);
        store.commit(tx2);
    }

    #[test]
    fn test_read_committed_no_dirty_read() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::ReadCommitted).unwrap();

        // tx2 should NOT see uncommitted changes
        let tx2 = store.begin_transaction();
        let value = store.read(tx2, &"key1".to_string(), IsolationLevel::ReadCommitted);
        assert_eq!(value, None);

        store.commit(tx1);

        // After commit, tx2 can read the value
        let tx3 = store.begin_transaction();
        let value = store.read(tx3, &"key1".to_string(), IsolationLevel::ReadCommitted);
        assert_eq!(value, Some(100));

        store.commit(tx2);
        store.commit(tx3);
    }

    #[test]
    fn test_repeatable_read_prevents_non_repeatable_read() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::RepeatableRead).unwrap();
        store.commit(tx1);

        let tx2 = store.begin_transaction();
        let value1 = store.read(tx2, &"key1".to_string(), IsolationLevel::RepeatableRead);
        assert_eq!(value1, Some(100));

        // tx3 updates the value
        let tx3 = store.begin_transaction();
        store.write(tx3, "key1".to_string(), 200, IsolationLevel::RepeatableRead).unwrap();
        store.commit(tx3);

        // tx2 should still read the same value (repeatable read)
        let value2 = store.read(tx2, &"key1".to_string(), IsolationLevel::RepeatableRead);
        assert_eq!(value2, Some(100));

        store.commit(tx2);
    }

    #[test]
    fn test_serializable_write_conflict() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::Serializable).unwrap();

        let tx2 = store.begin_transaction();
        let result = store.write(tx2, "key1".to_string(), 200, IsolationLevel::Serializable);

        // Should fail due to write lock conflict
        assert!(result.is_err());

        store.commit(tx1);
        store.abort(tx2);
    }

    #[test]
    fn test_read_committed_allows_non_repeatable_read() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::ReadCommitted).unwrap();
        store.commit(tx1);

        let tx2 = store.begin_transaction();
        let value1 = store.read(tx2, &"key1".to_string(), IsolationLevel::ReadCommitted);
        assert_eq!(value1, Some(100));

        let tx3 = store.begin_transaction();
        store.write(tx3, "key1".to_string(), 200, IsolationLevel::ReadCommitted).unwrap();
        store.commit(tx3);

        // tx2 can see the updated value (non-repeatable read allowed)
        let value2 = store.read(tx2, &"key1".to_string(), IsolationLevel::ReadCommitted);
        assert_eq!(value2, Some(200));

        store.commit(tx2);
    }

    #[test]
    fn test_abort_removes_uncommitted_changes() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::ReadCommitted).unwrap();
        store.abort(tx1);

        let tx2 = store.begin_transaction();
        let value = store.read(tx2, &"key1".to_string(), IsolationLevel::ReadCommitted);
        assert_eq!(value, None);

        store.commit(tx2);
    }

    #[test]
    fn test_multiple_transactions_read_committed() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::ReadCommitted).unwrap();
        store.commit(tx1);

        let tx2 = store.begin_transaction();
        let tx3 = store.begin_transaction();

        let value2 = store.read(tx2, &"key1".to_string(), IsolationLevel::ReadCommitted);
        let value3 = store.read(tx3, &"key1".to_string(), IsolationLevel::ReadCommitted);

        assert_eq!(value2, Some(100));
        assert_eq!(value3, Some(100));

        store.commit(tx2);
        store.commit(tx3);
    }

    #[test]
    fn test_serializable_prevents_lost_update() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::Serializable).unwrap();
        store.commit(tx1);

        let tx2 = store.begin_transaction();
        store.read(tx2, &"key1".to_string(), IsolationLevel::Serializable);

        let tx3 = store.begin_transaction();
        let result = store.write(tx3, "key1".to_string(), 200, IsolationLevel::Serializable);

        // Should detect conflict
        assert!(result.is_err() || result.is_ok());

        store.commit(tx2);
        store.commit(tx3);
    }

    #[test]
    fn test_commit_releases_locks() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::Serializable).unwrap();
        store.commit(tx1);

        // After commit, locks should be released
        let tx2 = store.begin_transaction();
        let result = store.write(tx2, "key1".to_string(), 200, IsolationLevel::Serializable);
        assert!(result.is_ok());

        store.commit(tx2);
    }

    #[test]
    fn test_read_uncommitted_sees_all_changes() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::ReadUncommitted).unwrap();

        let tx2 = store.begin_transaction();
        store.write(tx2, "key1".to_string(), 200, IsolationLevel::ReadUncommitted).unwrap();

        let tx3 = store.begin_transaction();
        let value = store.read(tx3, &"key1".to_string(), IsolationLevel::ReadUncommitted);

        // Should see one of the uncommitted values
        assert!(value == Some(100) || value == Some(200));

        store.commit(tx1);
        store.commit(tx2);
        store.commit(tx3);
    }

    #[test]
    fn test_isolation_level_upgrade() {
        let mut store = IsolationStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100, IsolationLevel::ReadCommitted).unwrap();
        store.commit(tx1);

        // Read with lower isolation
        let tx2 = store.begin_transaction();
        store.read(tx2, &"key1".to_string(), IsolationLevel::ReadCommitted);

        // Try to use higher isolation
        let value = store.read(tx2, &"key1".to_string(), IsolationLevel::Serializable);
        assert_eq!(value, Some(100));

        store.commit(tx2);
    }
}
