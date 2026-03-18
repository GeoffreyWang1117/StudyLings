// db05_mvcc.rs
//
// Multi-Version Concurrency Control (MVCC) is a technique that allows multiple
// transactions to access the same data concurrently without locking. Each transaction
// sees a consistent snapshot of the database as it existed at the start of the transaction.
//
// Key concepts:
// - Each write creates a new version of the data
// - Versions are tagged with transaction IDs and timestamps
// - Readers see the version visible at their snapshot timestamp
// - No read locks needed - readers don't block writers
//
// Benefits:
// - High concurrency (readers don't block writers)
// - Consistent reads (snapshot isolation)
// - No deadlocks from read locks
//
// Your task: Implement MVCC with versioned data and snapshot isolation.

// I AM NOT DONE

use std::collections::HashMap;

pub type TransactionId = u64;
pub type Timestamp = u64;

#[derive(Debug, Clone)]
pub struct Version<V: Clone> {
    value: V,
    created_by: TransactionId,
    created_at: Timestamp,
    deleted_at: Option<Timestamp>,
}

pub struct MVCCStore<K: Clone + Eq + std::hash::Hash, V: Clone> {
    versions: HashMap<K, Vec<Version<V>>>,
    next_tx_id: TransactionId,
    current_timestamp: Timestamp,
    active_snapshots: HashMap<TransactionId, Timestamp>,
}

impl<K: Clone + Eq + std::hash::Hash, V: Clone> MVCCStore<K, V> {
    pub fn new() -> Self {
        Self {
            versions: HashMap::new(),
            next_tx_id: 1,
            current_timestamp: 1,
            active_snapshots: HashMap::new(),
        }
    }

    pub fn begin_transaction(&mut self) -> TransactionId {
        // TODO: Start a new transaction
        // Assign a transaction ID and snapshot timestamp
        // Record the snapshot timestamp for this transaction
        todo!()
    }

    pub fn write(&mut self, tx_id: TransactionId, key: K, value: V) {
        // TODO: Write a new version of the data
        // Create a new version with the current transaction ID and timestamp
        // Add it to the version list for this key
        todo!()
    }

    pub fn read(&self, tx_id: TransactionId, key: &K) -> Option<V> {
        // TODO: Read the visible version for this transaction
        // Find the snapshot timestamp for this transaction
        // Return the latest version visible at that timestamp
        // A version is visible if:
        //   - It was created before or at the snapshot timestamp
        //   - It wasn't deleted before the snapshot timestamp
        todo!()
    }

    pub fn delete(&mut self, tx_id: TransactionId, key: K) {
        // TODO: Mark the current version as deleted
        // Find the latest version and set its deleted_at timestamp
        // This is a logical delete - old versions remain for other transactions
        todo!()
    }

    pub fn commit(&mut self, tx_id: TransactionId) {
        // TODO: Commit a transaction
        // Advance the timestamp
        // Remove the snapshot record
        todo!()
    }

    pub fn abort(&mut self, tx_id: TransactionId) {
        // TODO: Abort a transaction
        // Remove all versions created by this transaction
        // Remove the snapshot record
        todo!()
    }

    pub fn garbage_collect(&mut self) {
        // TODO: Remove old versions that are no longer visible to any transaction
        // Find the minimum active snapshot timestamp
        // Remove versions older than this that have been deleted
        todo!()
    }

    pub fn version_count(&self, key: &K) -> usize {
        self.versions.get(key).map_or(0, |v| v.len())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_mvcc_store() {
        let store: MVCCStore<String, i32> = MVCCStore::new();
        assert_eq!(store.version_count(&"key1".to_string()), 0);
    }

    #[test]
    fn test_simple_read_write() {
        let mut store = MVCCStore::new();
        let tx = store.begin_transaction();

        store.write(tx, "key1".to_string(), 100);
        assert_eq!(store.read(tx, &"key1".to_string()), Some(100));

        store.commit(tx);
    }

    #[test]
    fn test_snapshot_isolation() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);
        store.commit(tx1);

        // tx2 starts and reads the value
        let tx2 = store.begin_transaction();
        assert_eq!(store.read(tx2, &"key1".to_string()), Some(100));

        // tx3 updates the value
        let tx3 = store.begin_transaction();
        store.write(tx3, "key1".to_string(), 200);
        store.commit(tx3);

        // tx2 should still see the old value (snapshot isolation)
        assert_eq!(store.read(tx2, &"key1".to_string()), Some(100));

        store.commit(tx2);

        // New transaction should see the updated value
        let tx4 = store.begin_transaction();
        assert_eq!(store.read(tx4, &"key1".to_string()), Some(200));
        store.commit(tx4);
    }

    #[test]
    fn test_read_uncommitted_change() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);

        // tx2 should not see uncommitted changes from tx1
        let tx2 = store.begin_transaction();
        assert_eq!(store.read(tx2, &"key1".to_string()), None);

        store.commit(tx1);
        store.commit(tx2);
    }

    #[test]
    fn test_delete() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);
        store.commit(tx1);

        let tx2 = store.begin_transaction();
        store.delete(tx2, "key1".to_string());
        store.commit(tx2);

        let tx3 = store.begin_transaction();
        assert_eq!(store.read(tx3, &"key1".to_string()), None);
        store.commit(tx3);
    }

    #[test]
    fn test_abort_transaction() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);
        store.abort(tx1);

        let tx2 = store.begin_transaction();
        assert_eq!(store.read(tx2, &"key1".to_string()), None);
        store.commit(tx2);
    }

    #[test]
    fn test_multiple_versions() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);
        store.commit(tx1);

        let tx2 = store.begin_transaction();
        store.write(tx2, "key1".to_string(), 200);
        store.commit(tx2);

        // Should have multiple versions
        assert!(store.version_count(&"key1".to_string()) >= 2);
    }

    #[test]
    fn test_garbage_collection() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);
        store.commit(tx1);

        let tx2 = store.begin_transaction();
        store.write(tx2, "key1".to_string(), 200);
        store.commit(tx2);

        let tx3 = store.begin_transaction();
        store.write(tx3, "key1".to_string(), 300);
        store.commit(tx3);

        // Garbage collect old versions
        store.garbage_collect();

        // Should still be able to read the latest value
        let tx4 = store.begin_transaction();
        assert_eq!(store.read(tx4, &"key1".to_string()), Some(300));
        store.commit(tx4);
    }

    #[test]
    fn test_concurrent_updates() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);

        let tx2 = store.begin_transaction();
        store.write(tx2, "key1".to_string(), 200);

        store.commit(tx1);
        store.commit(tx2);

        let tx3 = store.begin_transaction();
        let value = store.read(tx3, &"key1".to_string());
        assert!(value == Some(100) || value == Some(200));
        store.commit(tx3);
    }

    #[test]
    fn test_read_after_delete_in_snapshot() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);
        store.commit(tx1);

        let tx2 = store.begin_transaction(); // Snapshot sees key1=100

        let tx3 = store.begin_transaction();
        store.delete(tx3, "key1".to_string());
        store.commit(tx3);

        // tx2 should still see the value (it was visible in its snapshot)
        assert_eq!(store.read(tx2, &"key1".to_string()), Some(100));
        store.commit(tx2);
    }

    #[test]
    fn test_multiple_keys() {
        let mut store = MVCCStore::new();

        let tx1 = store.begin_transaction();
        store.write(tx1, "key1".to_string(), 100);
        store.write(tx1, "key2".to_string(), 200);
        store.write(tx1, "key3".to_string(), 300);
        store.commit(tx1);

        let tx2 = store.begin_transaction();
        assert_eq!(store.read(tx2, &"key1".to_string()), Some(100));
        assert_eq!(store.read(tx2, &"key2".to_string()), Some(200));
        assert_eq!(store.read(tx2, &"key3".to_string()), Some(300));
        store.commit(tx2);
    }
}
