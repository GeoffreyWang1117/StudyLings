// rate07_bulkhead.rs
//
// Bulkhead is a fault tolerance pattern that isolates resources into pools
// to prevent failure in one area from affecting others.
//
// Inspired by ship bulkheads that prevent entire ship from sinking if one
// compartment is breached.
//
// How it works:
// - Divide resources into isolated pools (e.g., thread pools per service)
// - Each pool has fixed capacity
// - Failure/exhaustion in one pool doesn't affect others
// - Limits blast radius of failures
//
// Your task: Implement a bulkhead isolation pattern.
//
// Key concepts:
// - Resource pool isolation
// - Capacity limits per bulkhead
// - Independent failure domains
// - Resource acquisition and release

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct BulkheadId(pub usize);

#[derive(Debug)]
struct BulkheadPool {
    name: String,
    capacity: usize,
    in_use: usize,
    total_accepted: usize,
    total_rejected: usize,
}

pub struct BulkheadIsolation {
    bulkheads: HashMap<BulkheadId, BulkheadPool>,
}

impl BulkheadIsolation {
    pub fn new() -> Self {
        // TODO: Initialize empty bulkhead isolation system
        todo!()
    }

    pub fn create_bulkhead(&mut self, id: BulkheadId, name: String, capacity: usize) {
        // TODO: Create a new bulkhead with given parameters
        // - Initialize BulkheadPool with capacity and name
        // - Set in_use, total_accepted, total_rejected to 0
        // - Insert into bulkheads map
        todo!()
    }

    pub fn try_acquire(&mut self, id: BulkheadId) -> Result<(), BulkheadError> {
        // TODO: Try to acquire a resource slot from bulkhead
        // - Check if bulkhead exists, return Err(BulkheadError::NotFound) if not
        // - Check if in_use < capacity
        // - If yes, increment in_use and total_accepted, return Ok(())
        // - If no, increment total_rejected, return Err(BulkheadError::Full)
        todo!()
    }

    pub fn release(&mut self, id: BulkheadId) -> Result<(), BulkheadError> {
        // TODO: Release a resource slot back to bulkhead
        // - Check if bulkhead exists
        // - Decrement in_use (but don't go below 0)
        // - Return Ok(()) or Err if not found
        todo!()
    }

    pub fn execute<F, T>(&mut self, id: BulkheadId, operation: F) -> Result<T, BulkheadError>
    where
        F: FnOnce() -> T,
    {
        // TODO: Execute operation with bulkhead protection
        // - Try to acquire slot
        // - If successful, execute operation
        // - Release slot (even if operation panics - use a guard or careful error handling)
        // - Return result wrapped in Ok, or propagate BulkheadError
        todo!()
    }

    pub fn get_stats(&self, id: BulkheadId) -> Option<BulkheadStats> {
        // TODO: Return statistics for given bulkhead
        // - Return None if not found
        // - Return Some(BulkheadStats) with current values
        todo!()
    }

    pub fn available_capacity(&self, id: BulkheadId) -> Option<usize> {
        // TODO: Return available capacity for bulkhead
        // - Return None if not found
        // - Return Some(capacity - in_use)
        todo!()
    }

    pub fn is_full(&self, id: BulkheadId) -> bool {
        // TODO: Check if bulkhead is at capacity
        // - Return true if in_use >= capacity
        // - Return false if not found or has capacity
        todo!()
    }

    pub fn reset(&mut self, id: BulkheadId) -> Result<(), BulkheadError> {
        // TODO: Reset bulkhead statistics (keep capacity)
        // - Reset in_use, total_accepted, total_rejected to 0
        todo!()
    }

    pub fn list_bulkheads(&self) -> Vec<BulkheadId> {
        // TODO: Return list of all bulkhead IDs
        todo!()
    }
}

impl Default for BulkheadIsolation {
    fn default() -> Self {
        Self::new()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum BulkheadError {
    NotFound,
    Full,
}

#[derive(Debug, Clone, PartialEq)]
pub struct BulkheadStats {
    pub name: String,
    pub capacity: usize,
    pub in_use: usize,
    pub available: usize,
    pub total_accepted: usize,
    pub total_rejected: usize,
    pub utilization: f64, // in_use / capacity
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_bulkhead() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "service-a".to_string(), 5);

        let stats = isolation.get_stats(BulkheadId(1)).unwrap();
        assert_eq!(stats.name, "service-a");
        assert_eq!(stats.capacity, 5);
        assert_eq!(stats.in_use, 0);
    }

    #[test]
    fn test_acquire_and_release() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "test".to_string(), 3);

        assert!(isolation.try_acquire(BulkheadId(1)).is_ok());
        assert_eq!(isolation.available_capacity(BulkheadId(1)), Some(2));

        assert!(isolation.release(BulkheadId(1)).is_ok());
        assert_eq!(isolation.available_capacity(BulkheadId(1)), Some(3));
    }

    #[test]
    fn test_capacity_limit() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "limited".to_string(), 2);

        assert!(isolation.try_acquire(BulkheadId(1)).is_ok());
        assert!(isolation.try_acquire(BulkheadId(1)).is_ok());
        assert_eq!(isolation.try_acquire(BulkheadId(1)), Err(BulkheadError::Full));

        assert!(isolation.is_full(BulkheadId(1)));
    }

    #[test]
    fn test_nonexistent_bulkhead() {
        let mut isolation = BulkheadIsolation::new();

        assert_eq!(isolation.try_acquire(BulkheadId(99)), Err(BulkheadError::NotFound));
        assert_eq!(isolation.get_stats(BulkheadId(99)), None);
    }

    #[test]
    fn test_execute_with_bulkhead() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "exec".to_string(), 3);

        let result = isolation.execute(BulkheadId(1), || 42);
        assert_eq!(result, Ok(42));

        // After execution, slot should be released
        assert_eq!(isolation.available_capacity(BulkheadId(1)), Some(3));
    }

    #[test]
    fn test_execute_when_full() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "full".to_string(), 1);

        isolation.try_acquire(BulkheadId(1)).ok();

        let result = isolation.execute(BulkheadId(1), || 42);
        assert_eq!(result, Err(BulkheadError::Full));
    }

    #[test]
    fn test_isolation_between_bulkheads() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "service-a".to_string(), 2);
        isolation.create_bulkhead(BulkheadId(2), "service-b".to_string(), 2);

        // Fill bulkhead 1
        isolation.try_acquire(BulkheadId(1)).ok();
        isolation.try_acquire(BulkheadId(1)).ok();

        // Bulkhead 1 full, but bulkhead 2 still available
        assert!(isolation.is_full(BulkheadId(1)));
        assert!(!isolation.is_full(BulkheadId(2)));
        assert!(isolation.try_acquire(BulkheadId(2)).is_ok());
    }

    #[test]
    fn test_statistics_tracking() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "stats".to_string(), 2);

        isolation.try_acquire(BulkheadId(1)).ok();
        isolation.try_acquire(BulkheadId(1)).ok();
        isolation.try_acquire(BulkheadId(1)).ok(); // Rejected

        let stats = isolation.get_stats(BulkheadId(1)).unwrap();
        assert_eq!(stats.total_accepted, 2);
        assert_eq!(stats.total_rejected, 1);
    }

    #[test]
    fn test_utilization_calculation() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "util".to_string(), 4);

        isolation.try_acquire(BulkheadId(1)).ok();
        isolation.try_acquire(BulkheadId(1)).ok();

        let stats = isolation.get_stats(BulkheadId(1)).unwrap();
        assert!((stats.utilization - 0.5).abs() < 0.01); // 2/4 = 50%
    }

    #[test]
    fn test_reset() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "reset".to_string(), 3);

        isolation.try_acquire(BulkheadId(1)).ok();
        isolation.try_acquire(BulkheadId(1)).ok();

        isolation.reset(BulkheadId(1)).ok();

        let stats = isolation.get_stats(BulkheadId(1)).unwrap();
        assert_eq!(stats.in_use, 0);
        assert_eq!(stats.total_accepted, 0);
        assert_eq!(stats.total_rejected, 0);
        assert_eq!(stats.capacity, 3); // Capacity unchanged
    }

    #[test]
    fn test_list_bulkheads() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "a".to_string(), 1);
        isolation.create_bulkhead(BulkheadId(2), "b".to_string(), 2);
        isolation.create_bulkhead(BulkheadId(3), "c".to_string(), 3);

        let mut ids = isolation.list_bulkheads();
        ids.sort_by_key(|id| id.0);

        assert_eq!(ids, vec![BulkheadId(1), BulkheadId(2), BulkheadId(3)]);
    }

    #[test]
    fn test_multiple_operations() {
        let mut isolation = BulkheadIsolation::new();
        isolation.create_bulkhead(BulkheadId(1), "multi".to_string(), 3);

        let r1 = isolation.execute(BulkheadId(1), || "first");
        let r2 = isolation.execute(BulkheadId(1), || "second");
        let r3 = isolation.execute(BulkheadId(1), || "third");

        assert_eq!(r1, Ok("first"));
        assert_eq!(r2, Ok("second"));
        assert_eq!(r3, Ok("third"));

        let stats = isolation.get_stats(BulkheadId(1)).unwrap();
        assert_eq!(stats.total_accepted, 3);
        assert_eq!(stats.in_use, 0); // All released
    }
}
