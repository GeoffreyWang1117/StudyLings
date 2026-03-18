// db03_lsm_tree.rs
//
// Log-Structured Merge (LSM) Tree is a data structure optimized for write-heavy workloads.
// It's used in many modern databases like LevelDB, RocksDB, Cassandra, and HBase.
//
// Key components:
// - MemTable: In-memory sorted structure for recent writes
// - SSTables (Sorted String Tables): Immutable on-disk sorted files
// - Compaction: Background process to merge and remove obsolete data
//
// Write path: Write → MemTable → (when full) → Flush to SSTable
// Read path: Check MemTable → Check SSTables (newest to oldest)
//
// Your task: Implement a simplified LSM Tree with memtable, SSTables, and basic compaction.

// I AM NOT DONE

use std::collections::BTreeMap;
use std::fmt::Debug;

const MEMTABLE_SIZE_LIMIT: usize = 100;

#[derive(Debug, Clone)]
pub struct SSTable<K: Ord + Clone + Debug, V: Clone + Debug> {
    data: BTreeMap<K, Option<V>>, // None represents a tombstone (deletion)
    id: usize,
}

impl<K: Ord + Clone + Debug, V: Clone + Debug> SSTable<K, V> {
    fn new(id: usize, data: BTreeMap<K, Option<V>>) -> Self {
        Self { data, id }
    }

    fn get(&self, key: &K) -> Option<&Option<V>> {
        self.data.get(key)
    }
}

pub struct LSMTree<K: Ord + Clone + Debug, V: Clone + Debug> {
    memtable: BTreeMap<K, Option<V>>,
    sstables: Vec<SSTable<K, V>>,
    next_sstable_id: usize,
}

impl<K: Ord + Clone + Debug, V: Clone + Debug> LSMTree<K, V> {
    pub fn new() -> Self {
        Self {
            memtable: BTreeMap::new(),
            sstables: Vec::new(),
            next_sstable_id: 0,
        }
    }

    pub fn put(&mut self, key: K, value: V) {
        // TODO: Insert key-value pair into memtable
        // If memtable exceeds size limit, flush to SSTable
        todo!()
    }

    pub fn get(&self, key: &K) -> Option<V> {
        // TODO: Search for key in LSM tree
        // First check memtable
        // Then check SSTables from newest to oldest
        // Return None if key not found or if tombstone is found
        todo!()
    }

    pub fn delete(&mut self, key: K) {
        // TODO: Delete a key by inserting a tombstone
        // This is a logical delete - actual removal happens during compaction
        todo!()
    }

    fn flush_memtable(&mut self) {
        // TODO: Flush the current memtable to a new SSTable
        // Create a new SSTable with the memtable data
        // Clear the memtable
        // Add SSTable to the list
        todo!()
    }

    pub fn compact(&mut self) {
        // TODO: Merge all SSTables into one
        // Combine all SSTables, keeping only the latest version of each key
        // Remove tombstones for keys that don't exist in earlier levels
        // Replace multiple SSTables with a single compacted one
        todo!()
    }

    pub fn num_sstables(&self) -> usize {
        self.sstables.len()
    }

    pub fn memtable_size(&self) -> usize {
        self.memtable.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_empty_lsm_tree() {
        let tree: LSMTree<i32, String> = LSMTree::new();
        assert_eq!(tree.memtable_size(), 0);
        assert_eq!(tree.num_sstables(), 0);
    }

    #[test]
    fn test_put_and_get() {
        let mut tree = LSMTree::new();
        tree.put(1, "one".to_string());
        tree.put(2, "two".to_string());

        assert_eq!(tree.get(&1), Some("one".to_string()));
        assert_eq!(tree.get(&2), Some("two".to_string()));
        assert_eq!(tree.get(&3), None);
    }

    #[test]
    fn test_memtable_flush() {
        let mut tree = LSMTree::new();
        // Insert enough data to trigger flush
        for i in 0..MEMTABLE_SIZE_LIMIT + 10 {
            tree.put(i, format!("value_{}", i));
        }

        assert!(tree.num_sstables() > 0);
    }

    #[test]
    fn test_get_from_sstable() {
        let mut tree = LSMTree::new();
        // Force flush by filling memtable
        for i in 0..MEMTABLE_SIZE_LIMIT + 1 {
            tree.put(i, format!("value_{}", i));
        }

        // Should be able to read from SSTable
        assert_eq!(tree.get(&0), Some("value_0".to_string()));
    }

    #[test]
    fn test_update_value() {
        let mut tree = LSMTree::new();
        tree.put(1, "first".to_string());
        tree.put(1, "second".to_string());

        assert_eq!(tree.get(&1), Some("second".to_string()));
    }

    #[test]
    fn test_delete() {
        let mut tree = LSMTree::new();
        tree.put(1, "value".to_string());
        assert_eq!(tree.get(&1), Some("value".to_string()));

        tree.delete(1);
        assert_eq!(tree.get(&1), None);
    }

    #[test]
    fn test_delete_after_flush() {
        let mut tree = LSMTree::new();
        tree.put(1, "value".to_string());
        tree.flush_memtable();

        tree.delete(1);
        assert_eq!(tree.get(&1), None);
    }

    #[test]
    fn test_compaction_reduces_sstables() {
        let mut tree = LSMTree::new();

        // Create multiple SSTables
        for batch in 0..3 {
            for i in 0..MEMTABLE_SIZE_LIMIT {
                tree.put(batch * 1000 + i, format!("value_{}_{}", batch, i));
            }
            tree.flush_memtable();
        }

        let sstable_count_before = tree.num_sstables();
        tree.compact();
        let sstable_count_after = tree.num_sstables();

        assert!(sstable_count_after <= sstable_count_before);
    }

    #[test]
    fn test_compaction_keeps_latest_value() {
        let mut tree = LSMTree::new();

        tree.put(1, "first".to_string());
        tree.flush_memtable();

        tree.put(1, "second".to_string());
        tree.flush_memtable();

        tree.compact();
        assert_eq!(tree.get(&1), Some("second".to_string()));
    }

    #[test]
    fn test_range_of_operations() {
        let mut tree = LSMTree::new();

        // Insert
        for i in 0..50 {
            tree.put(i, i * 2);
        }

        // Update some
        for i in 0..10 {
            tree.put(i, i * 3);
        }

        // Delete some
        for i in 40..50 {
            tree.delete(i);
        }

        // Verify
        for i in 0..10 {
            assert_eq!(tree.get(&i), Some(i * 3));
        }
        for i in 10..40 {
            assert_eq!(tree.get(&i), Some(i * 2));
        }
        for i in 40..50 {
            assert_eq!(tree.get(&i), None);
        }
    }

    #[test]
    fn test_compaction_removes_tombstones() {
        let mut tree = LSMTree::new();

        for i in 0..20 {
            tree.put(i, i);
        }
        tree.flush_memtable();

        for i in 0..10 {
            tree.delete(i);
        }
        tree.flush_memtable();

        tree.compact();

        // Deleted keys should still be gone
        for i in 0..10 {
            assert_eq!(tree.get(&i), None);
        }
        // Non-deleted keys should remain
        for i in 10..20 {
            assert_eq!(tree.get(&i), Some(i));
        }
    }
}
