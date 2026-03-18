// stream03_topk.rs
//
// Finding the Top-K most frequent elements in a stream is a classic problem
// in stream processing. Due to memory constraints, we can't store all elements,
// so we use probabilistic data structures like Count-Min Sketch combined with
// a min-heap to efficiently track top elements.
//
// How it works:
// - Count-Min Sketch: Probabilistic frequency counter with bounded error
// - Min-Heap: Keep exactly K elements, evicting the minimum when full
// - Hash functions: Multiple hashes for accuracy
//
// Your task: Implement a Top-K tracker for streaming data that can handle
// millions of unique elements with limited memory.
//
// Key concepts:
// - Space-efficient frequency estimation
// - Heap-based top-K maintenance
// - Hash collision handling
// - Trade-off between accuracy and memory

// I AM NOT DONE

use std::collections::{BinaryHeap, HashMap};
use std::cmp::Reverse;
use std::hash::{Hash, Hasher};
use std::collections::hash_map::DefaultHasher;

pub struct CountMinSketch {
    width: usize,   // Number of counters per row
    depth: usize,   // Number of hash functions (rows)
    table: Vec<Vec<u64>>,
}

impl CountMinSketch {
    pub fn new(width: usize, depth: usize) -> Self {
        // TODO: Initialize Count-Min Sketch
        // - Create depth rows of width counters each
        // - Initialize all counters to 0
        todo!()
    }

    pub fn increment(&mut self, item: &str) {
        // TODO: Increment counters for the item
        // - Hash the item with depth different hash functions
        // - Increment counter at each position
        // Hint: Use hash_with_seed() for different hash functions
        todo!()
    }

    pub fn estimate(&self, item: &str) -> u64 {
        // TODO: Estimate frequency of an item
        // - Hash with each hash function
        // - Return minimum value across all rows
        // This gives an upper bound on the true frequency
        todo!()
    }

    fn hash_with_seed(&self, item: &str, seed: usize) -> usize {
        // TODO: Hash function with seed for different hash functions
        // - Combine item hash with seed
        // - Return index in range [0, width)
        todo!()
    }
}

#[derive(Debug, Clone, Eq, PartialEq)]
struct HeapItem {
    item: String,
    count: u64,
}

impl Ord for HeapItem {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        // TODO: Implement ordering for min-heap
        // - Compare by count (reverse for min-heap)
        // - Use item as tiebreaker for stability
        todo!()
    }
}

impl PartialOrd for HeapItem {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

pub struct TopKTracker {
    k: usize,
    sketch: CountMinSketch,
    heap: BinaryHeap<Reverse<HeapItem>>,
    in_heap: HashMap<String, u64>, // Track items in heap
}

impl TopKTracker {
    pub fn new(k: usize, sketch_width: usize, sketch_depth: usize) -> Self {
        // TODO: Initialize Top-K tracker
        // - Create Count-Min Sketch
        // - Initialize empty min-heap
        // - Initialize tracking map
        todo!()
    }

    pub fn add(&mut self, item: String) {
        // TODO: Add an item to the stream
        // - Increment count in sketch
        // - Get estimated frequency
        // - Update heap if necessary:
        //   * If item already in heap, update its count
        //   * If heap not full, add item
        //   * If heap full and count > min, replace min
        todo!()
    }

    pub fn get_top_k(&self) -> Vec<(String, u64)> {
        // TODO: Return current top-K items sorted by frequency (descending)
        // - Extract items from heap
        // - Sort by count descending
        todo!()
    }

    pub fn get_frequency(&self, item: &str) -> u64 {
        // TODO: Get estimated frequency of any item
        todo!()
    }

    fn update_heap(&mut self, item: String, count: u64) {
        // TODO: Update the min-heap with new item/count
        // - Check if item already in heap
        // - If yes, update and rebuild heap
        // - If no, check if should be added
        todo!()
    }

    fn rebuild_heap(&mut self) {
        // TODO: Rebuild heap after updating counts
        // - Used when item count is updated
        todo!()
    }

    pub fn size(&self) -> usize {
        // TODO: Return current number of items in heap
        todo!()
    }

    pub fn get_min_frequency(&self) -> Option<u64> {
        // TODO: Return the minimum frequency in the heap
        // - Useful for knowing the threshold for top-K
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_count_min_sketch_basic() {
        let mut sketch = CountMinSketch::new(100, 5);

        sketch.increment("apple");
        sketch.increment("apple");
        sketch.increment("banana");

        assert_eq!(sketch.estimate("apple"), 2);
        assert_eq!(sketch.estimate("banana"), 1);
        assert_eq!(sketch.estimate("orange"), 0);
    }

    #[test]
    fn test_count_min_sketch_overestimation() {
        let mut sketch = CountMinSketch::new(10, 3); // Small width, more collisions

        for i in 0..100 {
            sketch.increment(&format!("item{}", i));
        }

        // Due to collisions, estimates should be >= 1
        let estimate = sketch.estimate("item0");
        assert!(estimate >= 1);
    }

    #[test]
    fn test_topk_basic() {
        let mut tracker = TopKTracker::new(3, 100, 5);

        tracker.add("apple".to_string());
        tracker.add("banana".to_string());
        tracker.add("apple".to_string());
        tracker.add("cherry".to_string());
        tracker.add("apple".to_string());

        let top_k = tracker.get_top_k();
        assert_eq!(top_k.len(), 3);
        assert_eq!(top_k[0].0, "apple"); // Most frequent
        assert_eq!(top_k[0].1, 3);
    }

    #[test]
    fn test_topk_eviction() {
        let mut tracker = TopKTracker::new(2, 100, 5);

        tracker.add("a".to_string());
        tracker.add("b".to_string());
        tracker.add("c".to_string());
        tracker.add("c".to_string());
        tracker.add("c".to_string());

        let top_k = tracker.get_top_k();
        assert_eq!(top_k.len(), 2);

        // "c" should definitely be in top 2 with count 3
        assert!(top_k.iter().any(|(item, count)| item == "c" && *count == 3));
    }

    #[test]
    fn test_topk_ordering() {
        let mut tracker = TopKTracker::new(3, 100, 5);

        for _ in 0..5 { tracker.add("first".to_string()); }
        for _ in 0..3 { tracker.add("second".to_string()); }
        for _ in 0..1 { tracker.add("third".to_string()); }

        let top_k = tracker.get_top_k();
        assert_eq!(top_k[0].0, "first");
        assert_eq!(top_k[1].0, "second");
        assert_eq!(top_k[2].0, "third");
    }

    #[test]
    fn test_get_frequency() {
        let mut tracker = TopKTracker::new(5, 100, 5);

        for _ in 0..10 { tracker.add("popular".to_string()); }
        tracker.add("rare".to_string());

        assert_eq!(tracker.get_frequency("popular"), 10);
        assert_eq!(tracker.get_frequency("rare"), 1);
        assert_eq!(tracker.get_frequency("nonexistent"), 0);
    }

    #[test]
    fn test_large_stream() {
        let mut tracker = TopKTracker::new(5, 1000, 5);

        // Add many items
        for i in 0..1000 {
            tracker.add(format!("item{}", i % 100));
        }

        let top_k = tracker.get_top_k();
        assert_eq!(top_k.len(), 5);

        // Each of top items should have count of 10 (1000 / 100)
        for (_, count) in top_k {
            assert_eq!(count, 10);
        }
    }

    #[test]
    fn test_min_frequency() {
        let mut tracker = TopKTracker::new(3, 100, 5);

        tracker.add("a".to_string());
        tracker.add("b".to_string());
        tracker.add("b".to_string());
        tracker.add("c".to_string());
        tracker.add("c".to_string());
        tracker.add("c".to_string());

        let min_freq = tracker.get_min_frequency();
        assert!(min_freq.is_some());
        assert_eq!(min_freq.unwrap(), 1);
    }

    #[test]
    fn test_empty_tracker() {
        let tracker = TopKTracker::new(5, 100, 5);

        assert_eq!(tracker.get_top_k().len(), 0);
        assert_eq!(tracker.get_frequency("anything"), 0);
        assert!(tracker.get_min_frequency().is_none());
    }

    #[test]
    fn test_k_equals_one() {
        let mut tracker = TopKTracker::new(1, 100, 5);

        tracker.add("first".to_string());
        tracker.add("second".to_string());
        tracker.add("second".to_string());
        tracker.add("third".to_string());

        let top_k = tracker.get_top_k();
        assert_eq!(top_k.len(), 1);
        assert_eq!(top_k[0].0, "second"); // Most frequent
    }

    #[test]
    fn test_duplicate_additions() {
        let mut tracker = TopKTracker::new(3, 100, 5);

        for _ in 0..10 {
            tracker.add("repeated".to_string());
        }

        assert_eq!(tracker.get_frequency("repeated"), 10);
        let top_k = tracker.get_top_k();
        assert_eq!(top_k.len(), 1);
    }

    #[test]
    fn test_sketch_accuracy() {
        let mut sketch = CountMinSketch::new(1000, 7);

        for i in 0..100 {
            for _ in 0..i {
                sketch.increment(&format!("item{}", i));
            }
        }

        // Check accuracy for various items
        for i in 90..100 {
            let estimate = sketch.estimate(&format!("item{}", i));
            // Estimate should be close to actual count
            assert!(estimate >= i as u64);
            // With good parameters, shouldn't overestimate too much
            assert!(estimate < (i as f64 * 1.5) as u64);
        }
    }
}
