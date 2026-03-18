// stream01_sliding_window.rs
//
// Sliding windows are fundamental building blocks in stream processing for
// grouping events into finite sets for aggregation. There are three main types:
//
// 1. Tumbling Windows: Fixed-size, non-overlapping windows
//    Example: [0-5s], [5-10s], [10-15s]
//
// 2. Hopping Windows: Fixed-size, overlapping windows with a hop interval
//    Example: [0-5s], [2-7s], [4-9s] (window=5s, hop=2s)
//
// 3. Session Windows: Variable-size windows based on gaps in activity
//    Example: Events grouped if gap < timeout
//
// Your task: Implement a sliding window aggregator that supports all three
// window types for real-time stream aggregation.
//
// Key concepts:
// - Window lifecycle (creation, updating, expiration)
// - Event time vs processing time
// - Window boundaries and alignment
// - Efficient storage of window state

// I AM NOT DONE

use std::collections::{BTreeMap, HashMap};
use std::time::Duration;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WindowType {
    Tumbling { size: Duration },
    Hopping { size: Duration, hop: Duration },
    Session { gap: Duration },
}

#[derive(Debug, Clone)]
pub struct Event {
    pub timestamp: u64,  // milliseconds
    pub value: i64,
}

#[derive(Debug, Clone)]
pub struct Window {
    pub start: u64,
    pub end: u64,
    pub count: usize,
    pub sum: i64,
    pub min: i64,
    pub max: i64,
}

pub struct SlidingWindowAggregator {
    window_type: WindowType,
    windows: BTreeMap<u64, Window>, // key: window start time
    session_windows: HashMap<u64, Window>, // for session windows
}

impl SlidingWindowAggregator {
    pub fn new(window_type: WindowType) -> Self {
        // TODO: Initialize the aggregator with the specified window type
        todo!()
    }

    pub fn add_event(&mut self, event: Event) {
        // TODO: Add an event to the appropriate window(s)
        // - For tumbling windows: assign to exactly one window
        // - For hopping windows: may belong to multiple overlapping windows
        // - For session windows: merge with existing session or create new one
        // Hint: Use get_window_key() to determine which window(s) the event belongs to
        todo!()
    }

    fn get_window_key(&self, timestamp: u64) -> u64 {
        // TODO: Calculate the window start time for the given timestamp
        // - For tumbling: align to window boundaries
        // - For hopping: may need to return multiple keys
        // - For session: use timestamp as key initially
        todo!()
    }

    fn merge_sessions(&mut self, event: &Event) {
        // TODO: For session windows, check if event should merge existing sessions
        // - Find sessions within gap distance
        // - Merge overlapping/adjacent sessions
        // - Update window boundaries
        todo!()
    }

    fn update_window(&mut self, key: u64, event: &Event) {
        // TODO: Update window statistics with new event
        // - Increment count
        // - Add to sum
        // - Update min/max
        todo!()
    }

    pub fn get_windows(&self) -> Vec<Window> {
        // TODO: Return all current windows
        // - For session windows, use session_windows
        // - For tumbling/hopping, use windows
        todo!()
    }

    pub fn evict_old_windows(&mut self, watermark: u64) {
        // TODO: Remove windows that have ended before the watermark
        // - Only keep windows that might still receive events
        // - For session windows, consider gap timeout
        todo!()
    }

    pub fn get_window_at(&self, timestamp: u64) -> Option<&Window> {
        // TODO: Get the window containing the given timestamp
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tumbling_window_basic() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Tumbling {
            size: Duration::from_secs(5),
        });

        agg.add_event(Event { timestamp: 1000, value: 10 });
        agg.add_event(Event { timestamp: 2000, value: 20 });
        agg.add_event(Event { timestamp: 6000, value: 30 });

        let windows = agg.get_windows();
        assert_eq!(windows.len(), 2);

        // First window [0-5000]
        let w1 = &windows[0];
        assert_eq!(w1.count, 2);
        assert_eq!(w1.sum, 30);

        // Second window [5000-10000]
        let w2 = &windows[1];
        assert_eq!(w2.count, 1);
        assert_eq!(w2.sum, 30);
    }

    #[test]
    fn test_tumbling_window_alignment() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Tumbling {
            size: Duration::from_secs(10),
        });

        agg.add_event(Event { timestamp: 0, value: 1 });
        agg.add_event(Event { timestamp: 9999, value: 2 });
        agg.add_event(Event { timestamp: 10000, value: 3 });

        let windows = agg.get_windows();
        assert_eq!(windows.len(), 2);
        assert_eq!(windows[0].count, 2);
        assert_eq!(windows[1].count, 1);
    }

    #[test]
    fn test_hopping_window_overlap() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Hopping {
            size: Duration::from_secs(10),
            hop: Duration::from_secs(5),
        });

        agg.add_event(Event { timestamp: 3000, value: 100 });

        let windows = agg.get_windows();
        // Event at 3000 should appear in windows [0-10000]
        // In a full implementation, could also be in [-5000-5000] if we allow negative
        assert!(windows.len() >= 1);
        assert!(windows.iter().any(|w| w.sum == 100));
    }

    #[test]
    fn test_hopping_window_multiple_events() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Hopping {
            size: Duration::from_secs(10),
            hop: Duration::from_secs(5),
        });

        agg.add_event(Event { timestamp: 2000, value: 10 });
        agg.add_event(Event { timestamp: 7000, value: 20 });
        agg.add_event(Event { timestamp: 12000, value: 30 });

        let windows = agg.get_windows();
        // Windows: [0-10000], [5000-15000], [10000-20000]
        assert!(windows.len() >= 2);
    }

    #[test]
    fn test_session_window_single_session() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Session {
            gap: Duration::from_secs(5),
        });

        agg.add_event(Event { timestamp: 1000, value: 10 });
        agg.add_event(Event { timestamp: 3000, value: 20 });
        agg.add_event(Event { timestamp: 5000, value: 30 });

        let windows = agg.get_windows();
        assert_eq!(windows.len(), 1);
        assert_eq!(windows[0].count, 3);
        assert_eq!(windows[0].sum, 60);
    }

    #[test]
    fn test_session_window_multiple_sessions() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Session {
            gap: Duration::from_secs(5),
        });

        agg.add_event(Event { timestamp: 1000, value: 10 });
        agg.add_event(Event { timestamp: 2000, value: 20 });
        agg.add_event(Event { timestamp: 10000, value: 30 }); // Gap > 5s
        agg.add_event(Event { timestamp: 11000, value: 40 });

        let windows = agg.get_windows();
        assert_eq!(windows.len(), 2);
    }

    #[test]
    fn test_window_aggregates() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Tumbling {
            size: Duration::from_secs(5),
        });

        agg.add_event(Event { timestamp: 1000, value: 5 });
        agg.add_event(Event { timestamp: 2000, value: 15 });
        agg.add_event(Event { timestamp: 3000, value: 10 });

        let windows = agg.get_windows();
        assert_eq!(windows.len(), 1);

        let w = &windows[0];
        assert_eq!(w.count, 3);
        assert_eq!(w.sum, 30);
        assert_eq!(w.min, 5);
        assert_eq!(w.max, 15);
    }

    #[test]
    fn test_evict_old_windows() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Tumbling {
            size: Duration::from_secs(5),
        });

        agg.add_event(Event { timestamp: 1000, value: 10 });
        agg.add_event(Event { timestamp: 6000, value: 20 });
        agg.add_event(Event { timestamp: 11000, value: 30 });

        assert_eq!(agg.get_windows().len(), 3);

        agg.evict_old_windows(10000);
        let windows = agg.get_windows();
        assert!(windows.len() <= 2); // Should evict windows ending before 10000
    }

    #[test]
    fn test_get_window_at_timestamp() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Tumbling {
            size: Duration::from_secs(10),
        });

        agg.add_event(Event { timestamp: 5000, value: 100 });

        let window = agg.get_window_at(5000);
        assert!(window.is_some());
        assert_eq!(window.unwrap().sum, 100);

        let no_window = agg.get_window_at(15000);
        assert!(no_window.is_none());
    }

    #[test]
    fn test_session_window_merging() {
        let mut agg = SlidingWindowAggregator::new(WindowType::Session {
            gap: Duration::from_secs(3),
        });

        agg.add_event(Event { timestamp: 1000, value: 10 });
        agg.add_event(Event { timestamp: 10000, value: 20 });
        assert_eq!(agg.get_windows().len(), 2);

        // This event bridges the gap
        agg.add_event(Event { timestamp: 5000, value: 15 });
        let windows = agg.get_windows();
        assert_eq!(windows.len(), 1); // Should merge into one session
        assert_eq!(windows[0].sum, 45);
    }

    #[test]
    fn test_empty_windows() {
        let agg = SlidingWindowAggregator::new(WindowType::Tumbling {
            size: Duration::from_secs(5),
        });

        assert_eq!(agg.get_windows().len(), 0);
    }
}
