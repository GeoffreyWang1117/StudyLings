// stream02_watermark.rs
//
// Watermarks are a core concept in stream processing for handling out-of-order
// events. A watermark is a timestamp that indicates that no events with a
// timestamp earlier than the watermark will arrive.
//
// How watermarks work:
// - Watermark(t) means "all events with timestamp < t have been seen"
// - Used to determine when to close windows and emit results
// - Handle late-arriving data (events that arrive after watermark)
// - Balance latency vs completeness trade-off
//
// Your task: Implement a watermark-based event processor that handles
// out-of-order events and triggers computations when watermarks advance.
//
// Key concepts:
// - Watermark generation and propagation
// - Event time vs processing time
// - Late event handling (drop, side-output, or update)
// - Allowed lateness configuration

// I AM NOT DONE

use std::collections::{BTreeMap, VecDeque};

#[derive(Debug, Clone)]
pub struct Event {
    pub timestamp: u64,  // Event time in milliseconds
    pub data: String,
}

#[derive(Debug, Clone)]
pub struct WindowResult {
    pub window_end: u64,
    pub events: Vec<Event>,
    pub count: usize,
}

pub enum LateEventStrategy {
    Drop,                           // Discard late events
    SideOutput,                     // Keep late events separately
    UpdateWindow,                   // Allow window updates
}

pub struct WatermarkProcessor {
    current_watermark: u64,
    allowed_lateness: u64,          // How late can events arrive
    late_strategy: LateEventStrategy,
    pending_events: BTreeMap<u64, Vec<Event>>, // Buffered events
    completed_windows: BTreeMap<u64, WindowResult>,
    late_events: Vec<Event>,        // For SideOutput strategy
    window_size: u64,
}

impl WatermarkProcessor {
    pub fn new(window_size: u64, allowed_lateness: u64, late_strategy: LateEventStrategy) -> Self {
        // TODO: Initialize the watermark processor
        // - Set current_watermark to 0
        // - Initialize empty collections
        todo!()
    }

    pub fn add_event(&mut self, event: Event) {
        // TODO: Add an event to the processor
        // - Check if event is late (timestamp < current_watermark - allowed_lateness)
        // - Handle based on late_strategy
        // - If not late, add to pending_events
        // Hint: Group events by window
        todo!()
    }

    pub fn advance_watermark(&mut self, new_watermark: u64) -> Vec<WindowResult> {
        // TODO: Advance the watermark and trigger window computations
        // - Ensure new_watermark >= current_watermark (monotonic)
        // - Close all windows where window_end <= new_watermark
        // - Move completed windows to completed_windows
        // - Return newly completed windows
        // - Evict very old completed windows (outside allowed_lateness)
        todo!()
    }

    fn close_window(&mut self, window_end: u64) -> Option<WindowResult> {
        // TODO: Close a window and compute its result
        // - Collect all events in the window
        // - Create WindowResult with count and events
        // - Remove events from pending_events
        todo!()
    }

    fn is_late_event(&self, event_time: u64) -> bool {
        // TODO: Check if an event is too late
        // - Compare event_time with (current_watermark - allowed_lateness)
        todo!()
    }

    fn get_window_end(&self, event_time: u64) -> u64 {
        // TODO: Calculate which window this event belongs to
        // - Align to window boundaries based on window_size
        // - Return the window end timestamp
        todo!()
    }

    pub fn get_current_watermark(&self) -> u64 {
        // TODO: Return the current watermark value
        todo!()
    }

    pub fn get_late_events(&self) -> &[Event] {
        // TODO: Return late events (for SideOutput strategy)
        todo!()
    }

    pub fn get_pending_event_count(&self) -> usize {
        // TODO: Return total number of pending events
        todo!()
    }

    pub fn get_completed_window(&self, window_end: u64) -> Option<&WindowResult> {
        // TODO: Get a completed window by its end time
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_watermark_advancement() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::Drop,
        );

        assert_eq!(processor.get_current_watermark(), 0);

        processor.advance_watermark(5000);
        assert_eq!(processor.get_current_watermark(), 5000);

        processor.advance_watermark(10000);
        assert_eq!(processor.get_current_watermark(), 10000);
    }

    #[test]
    fn test_in_order_events() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::Drop,
        );

        processor.add_event(Event {
            timestamp: 1000,
            data: "event1".to_string(),
        });
        processor.add_event(Event {
            timestamp: 2000,
            data: "event2".to_string(),
        });

        let results = processor.advance_watermark(6000);
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].window_end, 5000);
        assert_eq!(results[0].count, 2);
    }

    #[test]
    fn test_out_of_order_events() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::Drop,
        );

        processor.add_event(Event {
            timestamp: 3000,
            data: "event1".to_string(),
        });
        processor.add_event(Event {
            timestamp: 1000,
            data: "event2".to_string(),
        });
        processor.add_event(Event {
            timestamp: 2000,
            data: "event3".to_string(),
        });

        let results = processor.advance_watermark(6000);
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].count, 3); // All events in same window
    }

    #[test]
    fn test_late_event_drop_strategy() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::Drop,
        );

        processor.add_event(Event {
            timestamp: 2000,
            data: "event1".to_string(),
        });

        processor.advance_watermark(6000);

        // This event is late (outside allowed_lateness)
        processor.add_event(Event {
            timestamp: 1000,
            data: "late_event".to_string(),
        });

        assert_eq!(processor.get_pending_event_count(), 0);
    }

    #[test]
    fn test_late_event_side_output_strategy() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::SideOutput,
        );

        processor.advance_watermark(6000);

        processor.add_event(Event {
            timestamp: 1000,
            data: "late_event".to_string(),
        });

        let late_events = processor.get_late_events();
        assert_eq!(late_events.len(), 1);
        assert_eq!(late_events[0].data, "late_event");
    }

    #[test]
    fn test_allowed_lateness() {
        let mut processor = WatermarkProcessor::new(
            5000,
            2000, // Allow 2 seconds lateness
            LateEventStrategy::Drop,
        );

        processor.advance_watermark(6000);

        // Event at 4500 is within allowed lateness (6000 - 2000 = 4000)
        processor.add_event(Event {
            timestamp: 4500,
            data: "late_but_ok".to_string(),
        });

        assert!(processor.get_pending_event_count() > 0);

        // Event at 3000 is too late (< 4000)
        processor.add_event(Event {
            timestamp: 3000,
            data: "too_late".to_string(),
        });

        // Should not increase pending count
    }

    #[test]
    fn test_multiple_windows() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::Drop,
        );

        processor.add_event(Event { timestamp: 1000, data: "w1".to_string() });
        processor.add_event(Event { timestamp: 6000, data: "w2".to_string() });
        processor.add_event(Event { timestamp: 11000, data: "w3".to_string() });

        let results = processor.advance_watermark(16000);
        assert_eq!(results.len(), 3);
        assert_eq!(results[0].window_end, 5000);
        assert_eq!(results[1].window_end, 10000);
        assert_eq!(results[2].window_end, 15000);
    }

    #[test]
    fn test_watermark_monotonicity() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::Drop,
        );

        processor.advance_watermark(10000);
        processor.advance_watermark(8000); // Should not decrease

        assert_eq!(processor.get_current_watermark(), 10000);
    }

    #[test]
    fn test_get_completed_window() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::Drop,
        );

        processor.add_event(Event {
            timestamp: 2000,
            data: "event".to_string(),
        });

        processor.advance_watermark(6000);

        let window = processor.get_completed_window(5000);
        assert!(window.is_some());
        assert_eq!(window.unwrap().count, 1);
    }

    #[test]
    fn test_window_alignment() {
        let mut processor = WatermarkProcessor::new(
            10000, // 10 second windows
            1000,
            LateEventStrategy::Drop,
        );

        processor.add_event(Event { timestamp: 0, data: "e1".to_string() });
        processor.add_event(Event { timestamp: 9999, data: "e2".to_string() });
        processor.add_event(Event { timestamp: 10000, data: "e3".to_string() });

        let results = processor.advance_watermark(20000);
        assert_eq!(results.len(), 2);
        assert_eq!(results[0].count, 2); // e1 and e2 in [0-10000)
        assert_eq!(results[1].count, 1); // e3 in [10000-20000)
    }

    #[test]
    fn test_empty_windows() {
        let mut processor = WatermarkProcessor::new(
            5000,
            1000,
            LateEventStrategy::Drop,
        );

        // Advance watermark without adding events
        let results = processor.advance_watermark(10000);
        // Should not create empty windows
        assert_eq!(results.len(), 0);
    }
}
