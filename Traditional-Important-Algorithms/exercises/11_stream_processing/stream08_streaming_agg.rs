// stream08_streaming_agg.rs
//
// Streaming aggregation computes aggregate functions (sum, count, avg, min, max)
// incrementally as events arrive, without storing all historical data.
// This is essential for real-time analytics and monitoring.
//
// Key techniques:
// - Incremental computation (avoid recomputing from scratch)
// - Algebraic aggregates (can be combined: sum, count, min, max)
// - Holistic aggregates (need more state: median, percentiles)
// - Windowed aggregation (tumbling, sliding, session)
//
// Your task: Implement various streaming aggregation functions with
// efficient incremental updates and memory-bounded computation.
//
// Key concepts:
// - Combine functions for distributed aggregation
// - Retraction (handling updates/deletes in streams)
// - Approximate aggregates for large state (HyperLogLog, T-Digest)

// I AM NOT DONE

use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone)]
pub struct AggregateState {
    pub count: u64,
    pub sum: f64,
    pub min: f64,
    pub max: f64,
}

impl AggregateState {
    pub fn new() -> Self {
        // TODO: Initialize empty aggregate state
        // - Set count to 0
        // - Use f64::INFINITY and f64::NEG_INFINITY for min/max
        todo!()
    }

    pub fn add(&mut self, value: f64) {
        // TODO: Incrementally update aggregates with new value
        // - Increment count
        // - Add to sum
        // - Update min/max
        todo!()
    }

    pub fn remove(&mut self, value: f64) {
        // TODO: Remove a value from aggregates (for sliding windows)
        // - Decrement count
        // - Subtract from sum
        // - Note: Can't easily update min/max without full scan
        todo!()
    }

    pub fn avg(&self) -> Option<f64> {
        // TODO: Calculate average
        // - Return None if count is 0
        // - Otherwise return sum / count
        todo!()
    }

    pub fn combine(&mut self, other: &AggregateState) {
        // TODO: Combine two aggregate states (for distributed aggregation)
        // - Add counts and sums
        // - Take min of mins, max of maxes
        todo!()
    }
}

pub struct StreamingAggregator {
    state: AggregateState,
}

impl StreamingAggregator {
    pub fn new() -> Self {
        // TODO: Initialize streaming aggregator
        todo!()
    }

    pub fn add(&mut self, value: f64) {
        // TODO: Add value to aggregation
        todo!()
    }

    pub fn get_state(&self) -> &AggregateState {
        // TODO: Get current aggregate state
        todo!()
    }

    pub fn reset(&mut self) {
        // TODO: Reset aggregator
        todo!()
    }
}

pub struct SlidingWindowAggregator {
    window_size: usize,
    buffer: VecDeque<f64>,
    state: AggregateState,
}

impl SlidingWindowAggregator {
    pub fn new(window_size: usize) -> Self {
        // TODO: Initialize sliding window aggregator
        // - Set window size
        // - Create empty buffer and state
        todo!()
    }

    pub fn add(&mut self, value: f64) {
        // TODO: Add value with sliding window semantics
        // - Add to buffer
        // - Add to state
        // - If buffer exceeds window_size, remove oldest
        // - Update state by removing oldest value
        todo!()
    }

    pub fn get_state(&self) -> &AggregateState {
        // TODO: Get current windowed aggregate state
        todo!()
    }
}

pub struct GroupedAggregator {
    groups: HashMap<String, AggregateState>,
}

impl GroupedAggregator {
    pub fn new() -> Self {
        // TODO: Initialize grouped aggregator
        todo!()
    }

    pub fn add(&mut self, key: String, value: f64) {
        // TODO: Add value to specific group
        // - Get or create state for key
        // - Add value to group's state
        todo!()
    }

    pub fn get_state(&self, key: &str) -> Option<&AggregateState> {
        // TODO: Get aggregate state for a group
        todo!()
    }

    pub fn get_all_groups(&self) -> Vec<(String, AggregateState)> {
        // TODO: Get all groups and their states
        todo!()
    }

    pub fn group_count(&self) -> usize {
        // TODO: Return number of groups
        todo!()
    }
}

// HyperLogLog for approximate distinct count
pub struct HyperLogLog {
    registers: Vec<u8>,
    num_registers: usize,
}

impl HyperLogLog {
    pub fn new(precision: u8) -> Self {
        // TODO: Initialize HyperLogLog
        // - num_registers = 2^precision
        // - Create vector of registers initialized to 0
        todo!()
    }

    pub fn add(&mut self, item: &str) {
        // TODO: Add item to HyperLogLog
        // - Hash the item
        // - Extract register index from first 'precision' bits
        // - Count leading zeros in remaining bits
        // - Update register with max of current and new value
        todo!()
    }

    pub fn count(&self) -> u64 {
        // TODO: Estimate cardinality using HyperLogLog formula
        // - Calculate harmonic mean of register values
        // - Apply correction factor
        // - Return estimated distinct count
        todo!()
    }

    fn hash(&self, item: &str) -> u64 {
        // TODO: Hash function for HyperLogLog
        // - Simple hash implementation
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        let mut hasher = DefaultHasher::new();
        item.hash(&mut hasher);
        hasher.finish()
    }

    fn leading_zeros(&self, value: u64, skip_bits: u8) -> u8 {
        // TODO: Count leading zeros after skipping first 'skip_bits' bits
        todo!()
    }

    pub fn merge(&mut self, other: &HyperLogLog) {
        // TODO: Merge another HyperLogLog into this one
        // - Take maximum value for each register
        todo!()
    }
}

pub struct PercentileAggregator {
    values: Vec<f64>, // Simplified: store all values (real impl would use T-Digest)
    max_size: usize,
}

impl PercentileAggregator {
    pub fn new(max_size: usize) -> Self {
        // TODO: Initialize percentile aggregator
        // - In production, would use T-Digest or similar
        // - For this exercise, bound the number of stored values
        todo!()
    }

    pub fn add(&mut self, value: f64) {
        // TODO: Add value for percentile calculation
        // - Add to values vector
        // - If exceeds max_size, sample/evict oldest
        todo!()
    }

    pub fn percentile(&mut self, p: f64) -> Option<f64> {
        // TODO: Calculate percentile (0.0 to 1.0)
        // - Sort values
        // - Find element at position p * len
        // - Linear interpolation if needed
        todo!()
    }

    pub fn median(&mut self) -> Option<f64> {
        // TODO: Calculate median (50th percentile)
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_aggregation() {
        let mut agg = StreamingAggregator::new();

        agg.add(10.0);
        agg.add(20.0);
        agg.add(30.0);

        let state = agg.get_state();
        assert_eq!(state.count, 3);
        assert_eq!(state.sum, 60.0);
        assert_eq!(state.min, 10.0);
        assert_eq!(state.max, 30.0);
        assert_eq!(state.avg(), Some(20.0));
    }

    #[test]
    fn test_aggregate_combine() {
        let mut state1 = AggregateState::new();
        state1.add(10.0);
        state1.add(20.0);

        let mut state2 = AggregateState::new();
        state2.add(30.0);
        state2.add(40.0);

        state1.combine(&state2);

        assert_eq!(state1.count, 4);
        assert_eq!(state1.sum, 100.0);
        assert_eq!(state1.min, 10.0);
        assert_eq!(state1.max, 40.0);
    }

    #[test]
    fn test_sliding_window() {
        let mut agg = SlidingWindowAggregator::new(3);

        agg.add(10.0);
        agg.add(20.0);
        agg.add(30.0);

        let state = agg.get_state();
        assert_eq!(state.count, 3);
        assert_eq!(state.sum, 60.0);

        agg.add(40.0); // Should evict 10.0

        let state = agg.get_state();
        assert_eq!(state.count, 3);
        assert_eq!(state.sum, 90.0); // 20 + 30 + 40
    }

    #[test]
    fn test_grouped_aggregation() {
        let mut agg = GroupedAggregator::new();

        agg.add("user1".to_string(), 10.0);
        agg.add("user1".to_string(), 20.0);
        agg.add("user2".to_string(), 30.0);

        assert_eq!(agg.group_count(), 2);

        let user1_state = agg.get_state("user1");
        assert!(user1_state.is_some());
        assert_eq!(user1_state.unwrap().count, 2);
        assert_eq!(user1_state.unwrap().sum, 30.0);

        let user2_state = agg.get_state("user2");
        assert_eq!(user2_state.unwrap().count, 1);
    }

    #[test]
    fn test_grouped_all_groups() {
        let mut agg = GroupedAggregator::new();

        agg.add("a".to_string(), 1.0);
        agg.add("b".to_string(), 2.0);
        agg.add("c".to_string(), 3.0);

        let all = agg.get_all_groups();
        assert_eq!(all.len(), 3);
    }

    #[test]
    fn test_hyperloglog_basic() {
        let mut hll = HyperLogLog::new(10);

        for i in 0..100 {
            hll.add(&format!("item{}", i));
        }

        let count = hll.count();
        // Should be approximately 100 (allow 20% error)
        assert!(count >= 80 && count <= 120,
                "HyperLogLog count {} not within expected range", count);
    }

    #[test]
    fn test_hyperloglog_duplicates() {
        let mut hll = HyperLogLog::new(10);

        // Add same items multiple times
        for _ in 0..10 {
            for i in 0..50 {
                hll.add(&format!("item{}", i));
            }
        }

        let count = hll.count();
        // Should estimate ~50 distinct items
        assert!(count >= 40 && count <= 60,
                "HyperLogLog count {} not within expected range", count);
    }

    #[test]
    fn test_hyperloglog_merge() {
        let mut hll1 = HyperLogLog::new(10);
        let mut hll2 = HyperLogLog::new(10);

        for i in 0..50 {
            hll1.add(&format!("item{}", i));
        }

        for i in 25..75 {
            hll2.add(&format!("item{}", i));
        }

        hll1.merge(&hll2);

        let count = hll1.count();
        // Should estimate ~75 distinct items (0..75)
        assert!(count >= 60 && count <= 90);
    }

    #[test]
    fn test_percentile_basic() {
        let mut perc = PercentileAggregator::new(1000);

        for i in 1..=100 {
            perc.add(i as f64);
        }

        let p50 = perc.percentile(0.5);
        assert!(p50.is_some());
        let median = p50.unwrap();
        assert!(median >= 48.0 && median <= 52.0);

        let p90 = perc.percentile(0.9);
        assert!(p90.is_some());
        let p90_val = p90.unwrap();
        assert!(p90_val >= 88.0 && p90_val <= 92.0);
    }

    #[test]
    fn test_median() {
        let mut perc = PercentileAggregator::new(1000);

        perc.add(1.0);
        perc.add(2.0);
        perc.add(3.0);
        perc.add(4.0);
        perc.add(5.0);

        let median = perc.median();
        assert_eq!(median, Some(3.0));
    }

    #[test]
    fn test_empty_aggregates() {
        let state = AggregateState::new();
        assert_eq!(state.count, 0);
        assert_eq!(state.avg(), None);

        let agg = StreamingAggregator::new();
        assert_eq!(agg.get_state().count, 0);
    }

    #[test]
    fn test_single_value_aggregates() {
        let mut agg = StreamingAggregator::new();
        agg.add(42.0);

        let state = agg.get_state();
        assert_eq!(state.count, 1);
        assert_eq!(state.sum, 42.0);
        assert_eq!(state.min, 42.0);
        assert_eq!(state.max, 42.0);
        assert_eq!(state.avg(), Some(42.0));
    }

    #[test]
    fn test_reset_aggregator() {
        let mut agg = StreamingAggregator::new();

        agg.add(10.0);
        agg.add(20.0);

        agg.reset();

        assert_eq!(agg.get_state().count, 0);
        assert_eq!(agg.get_state().sum, 0.0);
    }
}
