// stream09_event_time.rs
//
// Event time vs processing time is a fundamental concept in stream processing.
//
// - Event Time: When the event actually occurred (in the data)
// - Processing Time: When the system processes the event
// - Ingestion Time: When the event entered the system
//
// Challenges:
// - Network delays cause events to arrive out-of-order
// - Event time provides correct results even with delays
// - Processing time provides lower latency but incorrect results
//
// Your task: Implement event-time processing with out-of-order handling,
// late event management, and comparison with processing-time semantics.
//
// Key concepts:
// - Watermarks for event-time progress
// - Allowed lateness windows
// - Trigger policies (time-based, count-based, custom)
// - State retention and cleanup

// I AM NOT DONE

use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq)]
pub struct Event {
    pub event_time: u64,      // When event occurred
    pub processing_time: u64,  // When we received it
    pub data: String,
}

#[derive(Debug, Clone)]
pub struct WindowState {
    pub window_start: u64,
    pub window_end: u64,
    pub event_count: usize,
    pub events: Vec<Event>,
    pub is_finalized: bool,
}

pub enum TimeCharacteristic {
    EventTime,
    ProcessingTime,
    IngestionTime,
}

pub struct EventTimeProcessor {
    time_characteristic: TimeCharacteristic,
    window_size: u64,
    allowed_lateness: u64,
    current_watermark: u64,
    windows: BTreeMap<u64, WindowState>, // Key: window_end
}

impl EventTimeProcessor {
    pub fn new(
        time_characteristic: TimeCharacteristic,
        window_size: u64,
        allowed_lateness: u64,
    ) -> Self {
        // TODO: Initialize event-time processor
        // - Set time characteristic and window configuration
        // - Initialize empty windows map
        // - Set watermark to 0
        todo!()
    }

    pub fn process_event(&mut self, event: Event) -> ProcessingResult {
        // TODO: Process event based on time characteristic
        // - For EventTime: use event.event_time
        // - For ProcessingTime: use event.processing_time
        // - Determine which window the event belongs to
        // - Check if event is late (based on watermark and allowed_lateness)
        // - Add to appropriate window
        // - Return result indicating if added or dropped
        todo!()
    }

    fn get_effective_time(&self, event: &Event) -> u64 {
        // TODO: Get the effective timestamp based on time characteristic
        // - Return event_time or processing_time based on setting
        todo!()
    }

    fn get_window_for_time(&self, timestamp: u64) -> u64 {
        // TODO: Calculate window end time for given timestamp
        // - Align to window boundaries
        // - Return window_end
        todo!()
    }

    fn is_late(&self, event_time: u64) -> bool {
        // TODO: Check if event is too late to process
        // - Compare with (current_watermark - allowed_lateness)
        todo!()
    }

    pub fn advance_watermark(&mut self, new_watermark: u64) -> Vec<WindowState> {
        // TODO: Advance watermark and finalize windows
        // - Update current_watermark (ensure monotonic)
        // - Find all windows that should close (window_end <= watermark)
        // - Mark windows as finalized
        // - Return finalized windows
        todo!()
    }

    pub fn get_active_windows(&self) -> Vec<&WindowState> {
        // TODO: Return all non-finalized windows
        todo!()
    }

    pub fn get_watermark(&self) -> u64 {
        // TODO: Return current watermark
        todo!()
    }

    fn cleanup_old_windows(&mut self) {
        // TODO: Remove windows outside allowed lateness
        // - Remove finalized windows where window_end < watermark - allowed_lateness
        todo!()
    }
}

#[derive(Debug)]
pub struct ProcessingResult {
    pub added: bool,
    pub was_late: bool,
    pub window_end: u64,
}

pub struct WatermarkGenerator {
    max_event_time: u64,
    max_out_of_orderness: u64,
}

impl WatermarkGenerator {
    pub fn new(max_out_of_orderness: u64) -> Self {
        // TODO: Initialize watermark generator
        // - Set max allowed out-of-orderness
        // - Initialize max_event_time to 0
        todo!()
    }

    pub fn observe_event(&mut self, event_time: u64) {
        // TODO: Update watermark based on observed event
        // - Track maximum event time seen
        todo!()
    }

    pub fn current_watermark(&self) -> u64 {
        // TODO: Calculate current watermark
        // - Watermark = max_event_time - max_out_of_orderness
        // - Ensures events within max_out_of_orderness are still accepted
        todo!()
    }
}

pub struct PeriodicWatermarkGenerator {
    last_watermark: u64,
    period: u64,
    last_emission: u64,
}

impl PeriodicWatermarkGenerator {
    pub fn new(period: u64) -> Self {
        // TODO: Initialize periodic watermark generator
        // - Emits watermarks at fixed intervals
        todo!()
    }

    pub fn should_emit(&self, current_time: u64) -> bool {
        // TODO: Check if enough time has passed to emit watermark
        todo!()
    }

    pub fn emit_watermark(&mut self, current_time: u64, event_time: u64) -> Option<u64> {
        // TODO: Emit watermark if period has elapsed
        // - Check if should emit
        // - Update last_emission
        // - Return new watermark (or None if not time yet)
        todo!()
    }
}

pub struct Trigger {
    count_threshold: Option<usize>,
    time_threshold: Option<u64>,
    last_trigger_time: u64,
}

impl Trigger {
    pub fn count_trigger(count: usize) -> Self {
        // TODO: Create trigger that fires after N events
        todo!()
    }

    pub fn time_trigger(duration: u64) -> Self {
        // TODO: Create trigger that fires after duration
        todo!()
    }

    pub fn count_or_time_trigger(count: usize, duration: u64) -> Self {
        // TODO: Create trigger that fires on count OR time
        todo!()
    }

    pub fn should_fire(&mut self, event_count: usize, current_time: u64) -> bool {
        // TODO: Check if trigger condition is met
        // - Check count threshold
        // - Check time threshold
        // - Return true if any condition is met
        todo!()
    }

    pub fn reset(&mut self, current_time: u64) {
        // TODO: Reset trigger state after firing
        todo!()
    }
}

pub struct LateDataHandler {
    late_events: Vec<Event>,
    max_late_events: usize,
}

impl LateDataHandler {
    pub fn new(max_late_events: usize) -> Self {
        // TODO: Initialize late data handler
        todo!()
    }

    pub fn handle_late_event(&mut self, event: Event) {
        // TODO: Store late event for side output
        // - Add to late_events
        // - If exceeds max, remove oldest
        todo!()
    }

    pub fn get_late_events(&self) -> &[Event] {
        // TODO: Return late events
        todo!()
    }

    pub fn clear(&mut self) {
        // TODO: Clear late events
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_event_time_in_order() {
        let mut processor = EventTimeProcessor::new(
            TimeCharacteristic::EventTime,
            5000,
            1000,
        );

        let event1 = Event {
            event_time: 1000,
            processing_time: 1000,
            data: "e1".to_string(),
        };

        let result = processor.process_event(event1);
        assert!(result.added);
        assert!(!result.was_late);
    }

    #[test]
    fn test_event_time_out_of_order() {
        let mut processor = EventTimeProcessor::new(
            TimeCharacteristic::EventTime,
            5000,
            2000,
        );

        let event1 = Event {
            event_time: 3000,
            processing_time: 3000,
            data: "e1".to_string(),
        };

        let event2 = Event {
            event_time: 1000, // Earlier event arrives later
            processing_time: 4000,
            data: "e2".to_string(),
        };

        processor.process_event(event1);
        processor.process_event(event2);

        // Both should be in same window [0-5000)
        let windows = processor.get_active_windows();
        assert_eq!(windows.len(), 1);
        assert_eq!(windows[0].event_count, 2);
    }

    #[test]
    fn test_late_event_within_allowed_lateness() {
        let mut processor = EventTimeProcessor::new(
            TimeCharacteristic::EventTime,
            5000,
            2000, // Allow 2 seconds lateness
        );

        processor.advance_watermark(6000);

        let late_event = Event {
            event_time: 4500, // Before watermark but within allowed lateness
            processing_time: 7000,
            data: "late".to_string(),
        };

        let result = processor.process_event(late_event);
        assert!(result.added); // Should be accepted
    }

    #[test]
    fn test_late_event_outside_allowed_lateness() {
        let mut processor = EventTimeProcessor::new(
            TimeCharacteristic::EventTime,
            5000,
            1000,
        );

        processor.advance_watermark(8000);

        let very_late_event = Event {
            event_time: 2000, // Way before (watermark - allowed_lateness)
            processing_time: 9000,
            data: "very_late".to_string(),
        };

        let result = processor.process_event(very_late_event);
        assert!(!result.added); // Should be dropped
        assert!(result.was_late);
    }

    #[test]
    fn test_watermark_closes_windows() {
        let mut processor = EventTimeProcessor::new(
            TimeCharacteristic::EventTime,
            5000,
            1000,
        );

        processor.process_event(Event {
            event_time: 2000,
            processing_time: 2000,
            data: "e1".to_string(),
        });

        processor.process_event(Event {
            event_time: 7000,
            processing_time: 7000,
            data: "e2".to_string(),
        });

        let finalized = processor.advance_watermark(6000);
        assert_eq!(finalized.len(), 1); // First window [0-5000) should close
        assert!(finalized[0].is_finalized);
    }

    #[test]
    fn test_processing_time_semantics() {
        let mut processor = EventTimeProcessor::new(
            TimeCharacteristic::ProcessingTime,
            5000,
            0, // No lateness for processing time
        );

        let event = Event {
            event_time: 1000,
            processing_time: 6000, // Different from event time
            data: "e1".to_string(),
        };

        let result = processor.process_event(event);
        // Should use processing_time (6000) for window assignment
        assert_eq!(result.window_end, 10000); // [5000-10000)
    }

    #[test]
    fn test_watermark_generator() {
        let mut gen = WatermarkGenerator::new(1000);

        gen.observe_event(5000);
        assert_eq!(gen.current_watermark(), 4000); // 5000 - 1000

        gen.observe_event(3000); // Out of order, shouldn't affect watermark
        assert_eq!(gen.current_watermark(), 4000); // Still 4000

        gen.observe_event(8000);
        assert_eq!(gen.current_watermark(), 7000); // 8000 - 1000
    }

    #[test]
    fn test_periodic_watermark() {
        let mut gen = PeriodicWatermarkGenerator::new(1000);

        assert!(gen.should_emit(0));

        let wm = gen.emit_watermark(0, 5000);
        assert!(wm.is_some());

        assert!(!gen.should_emit(500)); // Too soon
        assert!(gen.should_emit(1500)); // After period
    }

    #[test]
    fn test_count_trigger() {
        let mut trigger = Trigger::count_trigger(3);

        assert!(!trigger.should_fire(1, 1000));
        assert!(!trigger.should_fire(2, 1000));
        assert!(trigger.should_fire(3, 1000));

        trigger.reset(1000);
        assert!(!trigger.should_fire(1, 2000));
    }

    #[test]
    fn test_time_trigger() {
        let mut trigger = Trigger::time_trigger(5000);

        assert!(trigger.should_fire(0, 0));
        trigger.reset(0);

        assert!(!trigger.should_fire(0, 3000));
        assert!(trigger.should_fire(0, 6000));
    }

    #[test]
    fn test_late_data_handler() {
        let mut handler = LateDataHandler::new(10);

        handler.handle_late_event(Event {
            event_time: 1000,
            processing_time: 5000,
            data: "late1".to_string(),
        });

        assert_eq!(handler.get_late_events().len(), 1);

        handler.clear();
        assert_eq!(handler.get_late_events().len(), 0);
    }

    #[test]
    fn test_multiple_windows() {
        let mut processor = EventTimeProcessor::new(
            TimeCharacteristic::EventTime,
            1000,
            500,
        );

        processor.process_event(Event { event_time: 500, processing_time: 500, data: "e1".to_string() });
        processor.process_event(Event { event_time: 1500, processing_time: 1500, data: "e2".to_string() });
        processor.process_event(Event { event_time: 2500, processing_time: 2500, data: "e3".to_string() });

        assert_eq!(processor.get_active_windows().len(), 3);
    }
}
