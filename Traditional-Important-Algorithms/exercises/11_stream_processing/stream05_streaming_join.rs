// stream05_streaming_join.rs
//
// Stream joins are used to correlate events from multiple streams based on
// keys and time windows. There are two main types:
//
// 1. Stream-Stream Join:
//    - Join two streams of events
//    - Events joined within a time window
//    - Both sides are unbounded streams
//
// 2. Stream-Table Join:
//    - Join stream with a (slowly changing) table
//    - Table lookups for enrichment
//    - Useful for adding reference data to events
//
// Your task: Implement both types of joins with configurable time windows
// and join semantics (inner, left, right).
//
// Key concepts:
// - Join windows and buffering
// - Time-based event correlation
// - Memory management for buffered events
// - Late event handling

// I AM NOT DONE

use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone, PartialEq)]
pub struct StreamEvent {
    pub key: String,
    pub timestamp: u64,
    pub value: String,
}

#[derive(Debug, Clone, PartialEq)]
pub struct JoinedEvent {
    pub key: String,
    pub timestamp: u64,
    pub left_value: Option<String>,
    pub right_value: Option<String>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum JoinType {
    Inner,      // Only when both sides match
    LeftOuter,  // All left events, right may be None
    RightOuter, // All right events, left may be None
    FullOuter,  // All events from both sides
}

pub struct StreamStreamJoin {
    join_type: JoinType,
    window_size: u64,           // Time window for joining (ms)
    left_buffer: HashMap<String, VecDeque<StreamEvent>>,
    right_buffer: HashMap<String, VecDeque<StreamEvent>>,
    current_watermark: u64,
}

impl StreamStreamJoin {
    pub fn new(join_type: JoinType, window_size: u64) -> Self {
        // TODO: Initialize stream-stream join
        // - Set join type and window size
        // - Initialize empty buffers for both streams
        todo!()
    }

    pub fn add_left(&mut self, event: StreamEvent) -> Vec<JoinedEvent> {
        // TODO: Add event to left stream and produce join results
        // - Add event to left buffer
        // - Find matching events in right buffer within window
        // - Create joined events based on join type
        // - Return all matches
        todo!()
    }

    pub fn add_right(&mut self, event: StreamEvent) -> Vec<JoinedEvent> {
        // TODO: Add event to right stream and produce join results
        // - Add event to right buffer
        // - Find matching events in left buffer within window
        // - Create joined events based on join type
        todo!()
    }

    fn find_matches(&self, event: &StreamEvent, buffer: &HashMap<String, VecDeque<StreamEvent>>)
        -> Vec<StreamEvent> {
        // TODO: Find all events in buffer that match the key and are within window
        // - Look up events by key
        // - Filter by time window: |event.timestamp - other.timestamp| <= window_size
        todo!()
    }

    pub fn advance_watermark(&mut self, watermark: u64) -> Vec<JoinedEvent> {
        // TODO: Advance watermark and emit any pending outer join results
        // - Update current_watermark
        // - For outer joins, emit events that didn't find matches
        // - Clean up old events from buffers
        todo!()
    }

    fn evict_old_events(&mut self, watermark: u64) {
        // TODO: Remove events older than (watermark - window_size)
        // - They can't match with future events
        todo!()
    }

    pub fn get_buffer_size(&self) -> (usize, usize) {
        // TODO: Return (left_buffer_size, right_buffer_size) for monitoring
        todo!()
    }
}

pub struct StreamTableJoin<V: Clone> {
    table: HashMap<String, V>,
    join_type: JoinType,
}

impl<V: Clone> StreamTableJoin<V> {
    pub fn new(join_type: JoinType) -> Self {
        // TODO: Initialize stream-table join
        // - Initialize empty table
        todo!()
    }

    pub fn update_table(&mut self, key: String, value: V) {
        // TODO: Update or insert entry in the table
        todo!()
    }

    pub fn remove_from_table(&mut self, key: &str) {
        // TODO: Remove entry from table
        todo!()
    }

    pub fn join(&self, key: &str) -> Option<&V> {
        // TODO: Lookup key in table for enrichment
        // - Return value if found, None otherwise
        todo!()
    }

    pub fn join_event(&self, event: StreamEvent) -> Option<(StreamEvent, Option<V>)> {
        // TODO: Join stream event with table
        // - Lookup event.key in table
        // - Return based on join type:
        //   * Inner: only if key exists in table
        //   * Left: always return event, with optional table value
        todo!()
    }

    pub fn table_size(&self) -> usize {
        // TODO: Return number of entries in table
        todo!()
    }
}

pub struct TemporalJoin {
    // Table with versioned values (timestamp -> value)
    table: HashMap<String, VecDeque<(u64, String)>>,
    retention: u64, // How long to keep old versions
}

impl TemporalJoin {
    pub fn new(retention: u64) -> Self {
        // TODO: Initialize temporal join
        // - Keeps historical versions of table data
        todo!()
    }

    pub fn update_table(&mut self, key: String, timestamp: u64, value: String) {
        // TODO: Add a versioned entry to the table
        // - Store with timestamp
        // - Keep versions sorted by timestamp
        todo!()
    }

    pub fn join(&self, key: &str, event_timestamp: u64) -> Option<String> {
        // TODO: Join using the table version at event_timestamp
        // - Find the latest version with timestamp <= event_timestamp
        // - This ensures temporal consistency
        todo!()
    }

    pub fn evict_old_versions(&mut self, watermark: u64) {
        // TODO: Remove versions older than (watermark - retention)
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_inner_join_match() {
        let mut join = StreamStreamJoin::new(JoinType::Inner, 5000);

        let left = StreamEvent {
            key: "user1".to_string(),
            timestamp: 1000,
            value: "click".to_string(),
        };

        let right = StreamEvent {
            key: "user1".to_string(),
            timestamp: 2000,
            value: "purchase".to_string(),
        };

        join.add_left(left.clone());
        let results = join.add_right(right.clone());

        assert_eq!(results.len(), 1);
        assert_eq!(results[0].key, "user1");
        assert_eq!(results[0].left_value, Some("click".to_string()));
        assert_eq!(results[0].right_value, Some("purchase".to_string()));
    }

    #[test]
    fn test_inner_join_no_match_different_keys() {
        let mut join = StreamStreamJoin::new(JoinType::Inner, 5000);

        let left = StreamEvent {
            key: "user1".to_string(),
            timestamp: 1000,
            value: "click".to_string(),
        };

        let right = StreamEvent {
            key: "user2".to_string(),
            timestamp: 2000,
            value: "purchase".to_string(),
        };

        join.add_left(left);
        let results = join.add_right(right);

        assert_eq!(results.len(), 0); // Different keys, no match
    }

    #[test]
    fn test_inner_join_no_match_outside_window() {
        let mut join = StreamStreamJoin::new(JoinType::Inner, 1000);

        let left = StreamEvent {
            key: "user1".to_string(),
            timestamp: 1000,
            value: "click".to_string(),
        };

        let right = StreamEvent {
            key: "user1".to_string(),
            timestamp: 5000, // Outside 1-second window
            value: "purchase".to_string(),
        };

        join.add_left(left);
        let results = join.add_right(right);

        assert_eq!(results.len(), 0); // Outside window
    }

    #[test]
    fn test_left_outer_join() {
        let mut join = StreamStreamJoin::new(JoinType::LeftOuter, 5000);

        let left = StreamEvent {
            key: "user1".to_string(),
            timestamp: 1000,
            value: "click".to_string(),
        };

        let results = join.add_left(left.clone());

        // Left outer join may emit immediately or on watermark
        join.advance_watermark(10000);
        // Should have emitted left event even without right match
    }

    #[test]
    fn test_multiple_matches() {
        let mut join = StreamStreamJoin::new(JoinType::Inner, 10000);

        let left = StreamEvent {
            key: "user1".to_string(),
            timestamp: 1000,
            value: "click1".to_string(),
        };

        join.add_left(left);

        let right1 = StreamEvent {
            key: "user1".to_string(),
            timestamp: 2000,
            value: "purchase1".to_string(),
        };

        let right2 = StreamEvent {
            key: "user1".to_string(),
            timestamp: 3000,
            value: "purchase2".to_string(),
        };

        let results1 = join.add_right(right1);
        let results2 = join.add_right(right2);

        assert_eq!(results1.len(), 1);
        assert_eq!(results2.len(), 1);
    }

    #[test]
    fn test_stream_table_join_basic() {
        let mut join = StreamTableJoin::new(JoinType::Inner);

        join.update_table("user1".to_string(), "John Doe");
        join.update_table("user2".to_string(), "Jane Smith");

        assert_eq!(join.join("user1"), Some(&"John Doe"));
        assert_eq!(join.join("user3"), None);
    }

    #[test]
    fn test_stream_table_join_event() {
        let mut join = StreamTableJoin::new(JoinType::LeftOuter);

        join.update_table("user1".to_string(), "Premium");

        let event = StreamEvent {
            key: "user1".to_string(),
            timestamp: 1000,
            value: "purchase".to_string(),
        };

        let result = join.join_event(event);
        assert!(result.is_some());

        let (evt, table_val) = result.unwrap();
        assert_eq!(evt.key, "user1");
        assert_eq!(table_val, Some("Premium"));
    }

    #[test]
    fn test_stream_table_update() {
        let mut join = StreamTableJoin::new(JoinType::Inner);

        join.update_table("user1".to_string(), "Basic");
        assert_eq!(join.join("user1"), Some(&"Basic"));

        join.update_table("user1".to_string(), "Premium");
        assert_eq!(join.join("user1"), Some(&"Premium"));
    }

    #[test]
    fn test_stream_table_remove() {
        let mut join = StreamTableJoin::new(JoinType::Inner);

        join.update_table("user1".to_string(), "data");
        assert_eq!(join.table_size(), 1);

        join.remove_from_table("user1");
        assert_eq!(join.table_size(), 0);
        assert_eq!(join.join("user1"), None);
    }

    #[test]
    fn test_temporal_join_basic() {
        let mut join = TemporalJoin::new(10000);

        join.update_table("user1".to_string(), 1000, "version1".to_string());
        join.update_table("user1".to_string(), 3000, "version2".to_string());
        join.update_table("user1".to_string(), 5000, "version3".to_string());

        // Event at 2000 should get version1
        assert_eq!(join.join("user1", 2000), Some("version1".to_string()));

        // Event at 4000 should get version2
        assert_eq!(join.join("user1", 4000), Some("version2".to_string()));

        // Event at 6000 should get version3
        assert_eq!(join.join("user1", 6000), Some("version3".to_string()));
    }

    #[test]
    fn test_temporal_join_eviction() {
        let mut join = TemporalJoin::new(5000);

        join.update_table("user1".to_string(), 1000, "old".to_string());
        join.update_table("user1".to_string(), 8000, "new".to_string());

        join.evict_old_versions(10000);

        // Old version should be evicted (10000 - 5000 = 5000 > 1000)
        // But should still be able to join recent events
        assert_eq!(join.join("user1", 9000), Some("new".to_string()));
    }

    #[test]
    fn test_buffer_eviction() {
        let mut join = StreamStreamJoin::new(JoinType::Inner, 1000);

        for i in 0..10 {
            join.add_left(StreamEvent {
                key: format!("key{}", i),
                timestamp: i * 1000,
                value: format!("val{}", i),
            });
        }

        let (left_size, _) = join.get_buffer_size();
        assert_eq!(left_size, 10);

        join.advance_watermark(15000);

        let (left_size_after, _) = join.get_buffer_size();
        // Old events should be evicted
        assert!(left_size_after < left_size);
    }
}
