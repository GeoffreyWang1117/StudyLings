// stream10_backpressure.rs
//
// Backpressure is a mechanism to handle situations where data producers
// generate events faster than consumers can process them. Without proper
// backpressure, systems can experience:
// - Memory exhaustion (unbounded buffers)
// - Increased latency
// - System crashes
// - Data loss
//
// Backpressure strategies:
// 1. Blocking: Block producer until consumer catches up
// 2. Buffering: Use bounded buffer, apply policy when full
// 3. Dropping: Drop events when overwhelmed (with various policies)
// 4. Rate limiting: Limit producer rate
// 5. Dynamic: Adjust behavior based on system state
//
// Your task: Implement various backpressure mechanisms for stream processing
// pipelines to prevent overload and maintain system stability.
//
// Key concepts:
// - Bounded queues and overflow policies
// - Flow control signals
// - Reactive streams (request/acknowledgment)
// - Adaptive rate limiting

// I AM NOT DONE

use std::collections::VecDeque;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, PartialEq)]
pub enum OverflowPolicy {
    Block,           // Block producer
    DropOldest,      // Drop oldest items
    DropNewest,      // Drop newest items
    DropCurrent,     // Drop current item being added
}

#[derive(Debug, Clone)]
pub struct Event {
    pub id: u64,
    pub timestamp: u64,
    pub data: String,
}

pub struct BoundedBuffer {
    buffer: VecDeque<Event>,
    capacity: usize,
    overflow_policy: OverflowPolicy,
    dropped_count: u64,
}

impl BoundedBuffer {
    pub fn new(capacity: usize, overflow_policy: OverflowPolicy) -> Self {
        // TODO: Initialize bounded buffer
        // - Set capacity and overflow policy
        // - Create empty buffer
        // - Initialize dropped count to 0
        todo!()
    }

    pub fn try_push(&mut self, event: Event) -> Result<(), Event> {
        // TODO: Try to add event to buffer
        // - If buffer not full, add and return Ok
        // - If full, apply overflow policy:
        //   * Block: return Err(event) (caller should retry)
        //   * DropOldest: remove oldest, add new
        //   * DropNewest: drop new event
        //   * DropCurrent: same as DropNewest
        // - Increment dropped_count if dropping
        todo!()
    }

    pub fn pop(&mut self) -> Option<Event> {
        // TODO: Remove and return front event
        todo!()
    }

    pub fn len(&self) -> usize {
        // TODO: Return current buffer size
        todo!()
    }

    pub fn is_full(&self) -> bool {
        // TODO: Check if buffer is at capacity
        todo!()
    }

    pub fn dropped_count(&self) -> u64 {
        // TODO: Return number of dropped events
        todo!()
    }

    pub fn utilization(&self) -> f64 {
        // TODO: Return buffer utilization as percentage (0.0 to 1.0)
        todo!()
    }
}

pub struct ReactiveStream {
    buffer: VecDeque<Event>,
    capacity: usize,
    demand: i64,              // Outstanding demand from consumer
    produced_count: u64,
    consumed_count: u64,
}

impl ReactiveStream {
    pub fn new(capacity: usize) -> Self {
        // TODO: Initialize reactive stream
        // - Implements request/response backpressure model
        // - Consumer requests N items, producer can send up to N
        todo!()
    }

    pub fn request(&mut self, n: u64) {
        // TODO: Consumer requests n more items
        // - Add to demand counter
        // - This signals producer can send more
        todo!()
    }

    pub fn produce(&mut self, event: Event) -> Result<(), Event> {
        // TODO: Producer adds event if demand allows
        // - Check if demand > 0
        // - If yes, add to buffer and decrement demand
        // - If no, return error (backpressure)
        todo!()
    }

    pub fn consume(&mut self) -> Option<Event> {
        // TODO: Consumer takes an event
        // - Remove from buffer
        // - Increment consumed_count
        todo!()
    }

    pub fn available_demand(&self) -> i64 {
        // TODO: Return current demand
        todo!()
    }

    pub fn pending_events(&self) -> usize {
        // TODO: Return number of events in buffer
        todo!()
    }
}

pub struct AdaptiveRateLimiter {
    current_rate: f64,        // Events per second
    min_rate: f64,
    max_rate: f64,
    target_utilization: f64,  // Target buffer utilization (0.0-1.0)
    adjustment_factor: f64,   // How quickly to adjust rate
    last_adjustment: Instant,
}

impl AdaptiveRateLimiter {
    pub fn new(
        initial_rate: f64,
        min_rate: f64,
        max_rate: f64,
        target_utilization: f64,
    ) -> Self {
        // TODO: Initialize adaptive rate limiter
        // - Adjusts rate based on system feedback
        todo!()
    }

    pub fn adjust_rate(&mut self, current_utilization: f64) {
        // TODO: Adjust rate based on current buffer utilization
        // - If utilization > target, decrease rate
        // - If utilization < target, increase rate
        // - Respect min/max bounds
        // - Use exponential moving average for stability
        todo!()
    }

    pub fn get_current_rate(&self) -> f64 {
        // TODO: Return current rate limit
        todo!()
    }

    pub fn should_allow(&mut self, events_sent: u64, elapsed: Duration) -> bool {
        // TODO: Check if should allow more events
        // - Calculate current sending rate
        // - Compare with rate limit
        // - Return true if under limit
        todo!()
    }

    pub fn wait_time(&self, events_sent: u64, elapsed: Duration) -> Option<Duration> {
        // TODO: Calculate how long to wait before sending next event
        // - If under rate limit, return None
        // - Otherwise, return wait duration
        todo!()
    }
}

pub struct BackpressureMonitor {
    buffer_sizes: Vec<usize>,   // Historical buffer sizes
    sample_window: usize,
    total_events: u64,
    dropped_events: u64,
    blocked_events: u64,
}

impl BackpressureMonitor {
    pub fn new(sample_window: usize) -> Self {
        // TODO: Initialize backpressure monitor
        // - Tracks system health metrics
        todo!()
    }

    pub fn record_buffer_size(&mut self, size: usize) {
        // TODO: Record buffer size sample
        // - Add to buffer_sizes
        // - Keep only last sample_window entries
        todo!()
    }

    pub fn record_dropped(&mut self) {
        // TODO: Record dropped event
        todo!()
    }

    pub fn record_blocked(&mut self) {
        // TODO: Record blocked event
        todo!()
    }

    pub fn average_buffer_size(&self) -> f64 {
        // TODO: Calculate average buffer size over window
        todo!()
    }

    pub fn drop_rate(&self) -> f64 {
        // TODO: Calculate drop rate (dropped / total)
        todo!()
    }

    pub fn is_healthy(&self, max_drop_rate: f64, max_avg_buffer_ratio: f64, buffer_capacity: usize) -> bool {
        // TODO: Check if system is healthy
        // - Drop rate below threshold
        // - Average buffer size not too high
        todo!()
    }
}

pub struct PipelineStage {
    name: String,
    buffer: BoundedBuffer,
    processing_time: Duration,  // Simulated processing time
}

impl PipelineStage {
    pub fn new(name: String, capacity: usize, overflow_policy: OverflowPolicy, processing_time: Duration) -> Self {
        // TODO: Initialize pipeline stage
        todo!()
    }

    pub fn push(&mut self, event: Event) -> Result<(), Event> {
        // TODO: Push event to this stage
        todo!()
    }

    pub fn process_one(&mut self) -> Option<Event> {
        // TODO: Process one event from buffer
        // - Take event from buffer
        // - Simulate processing (in real system, do actual work)
        // - Return processed event
        todo!()
    }

    pub fn is_overloaded(&self) -> bool {
        // TODO: Check if stage is overloaded
        // - Buffer utilization > threshold (e.g., 0.8)
        todo!()
    }

    pub fn buffer_utilization(&self) -> f64 {
        // TODO: Return buffer utilization
        todo!()
    }
}

pub struct BackpressurePipeline {
    stages: Vec<PipelineStage>,
    monitor: BackpressureMonitor,
}

impl BackpressurePipeline {
    pub fn new(stages: Vec<PipelineStage>, monitor_window: usize) -> Self {
        // TODO: Initialize backpressure-aware pipeline
        todo!()
    }

    pub fn push(&mut self, event: Event) -> Result<(), String> {
        // TODO: Push event to first stage
        // - Check if first stage can accept
        // - Record metrics
        todo!()
    }

    pub fn process_all_stages(&mut self) {
        // TODO: Process events through all stages
        // - For each stage, process events and push to next stage
        // - Handle backpressure between stages
        todo!()
    }

    pub fn get_stage_status(&self) -> Vec<(String, f64)> {
        // TODO: Get status of all stages (name, utilization)
        todo!()
    }

    pub fn is_healthy(&self) -> bool {
        // TODO: Check if pipeline is healthy
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bounded_buffer_normal_operation() {
        let mut buffer = BoundedBuffer::new(5, OverflowPolicy::Block);

        for i in 0..3 {
            let event = Event { id: i, timestamp: i, data: format!("e{}", i) };
            assert!(buffer.try_push(event).is_ok());
        }

        assert_eq!(buffer.len(), 3);
        assert!(!buffer.is_full());
    }

    #[test]
    fn test_bounded_buffer_overflow_block() {
        let mut buffer = BoundedBuffer::new(2, OverflowPolicy::Block);

        buffer.try_push(Event { id: 1, timestamp: 1, data: "e1".to_string() }).unwrap();
        buffer.try_push(Event { id: 2, timestamp: 2, data: "e2".to_string() }).unwrap();

        let event3 = Event { id: 3, timestamp: 3, data: "e3".to_string() };
        let result = buffer.try_push(event3);

        assert!(result.is_err()); // Should return the event
        assert_eq!(buffer.len(), 2);
    }

    #[test]
    fn test_bounded_buffer_drop_oldest() {
        let mut buffer = BoundedBuffer::new(2, OverflowPolicy::DropOldest);

        buffer.try_push(Event { id: 1, timestamp: 1, data: "e1".to_string() }).unwrap();
        buffer.try_push(Event { id: 2, timestamp: 2, data: "e2".to_string() }).unwrap();
        buffer.try_push(Event { id: 3, timestamp: 3, data: "e3".to_string() }).unwrap();

        assert_eq!(buffer.len(), 2);
        assert_eq!(buffer.dropped_count(), 1);

        let first = buffer.pop().unwrap();
        assert_eq!(first.id, 2); // Event 1 was dropped
    }

    #[test]
    fn test_bounded_buffer_drop_newest() {
        let mut buffer = BoundedBuffer::new(2, OverflowPolicy::DropNewest);

        buffer.try_push(Event { id: 1, timestamp: 1, data: "e1".to_string() }).unwrap();
        buffer.try_push(Event { id: 2, timestamp: 2, data: "e2".to_string() }).unwrap();
        buffer.try_push(Event { id: 3, timestamp: 3, data: "e3".to_string() }).unwrap();

        assert_eq!(buffer.len(), 2);
        assert_eq!(buffer.dropped_count(), 1);

        let first = buffer.pop().unwrap();
        assert_eq!(first.id, 1); // Event 3 was dropped, 1 and 2 remain
    }

    #[test]
    fn test_buffer_utilization() {
        let mut buffer = BoundedBuffer::new(10, OverflowPolicy::Block);

        for i in 0..5 {
            buffer.try_push(Event { id: i, timestamp: i, data: format!("e{}", i) }).unwrap();
        }

        assert_eq!(buffer.utilization(), 0.5); // 5/10 = 0.5
    }

    #[test]
    fn test_reactive_stream_demand() {
        let mut stream = ReactiveStream::new(10);

        assert_eq!(stream.available_demand(), 0);

        stream.request(5);
        assert_eq!(stream.available_demand(), 5);

        let event = Event { id: 1, timestamp: 1, data: "e1".to_string() };
        stream.produce(event).unwrap();

        assert_eq!(stream.available_demand(), 4); // Demand decremented
    }

    #[test]
    fn test_reactive_stream_backpressure() {
        let mut stream = ReactiveStream::new(10);

        // No demand, should fail
        let event = Event { id: 1, timestamp: 1, data: "e1".to_string() };
        let result = stream.produce(event);
        assert!(result.is_err()); // Backpressure applied
    }

    #[test]
    fn test_reactive_stream_consume() {
        let mut stream = ReactiveStream::new(10);

        stream.request(2);
        stream.produce(Event { id: 1, timestamp: 1, data: "e1".to_string() }).unwrap();
        stream.produce(Event { id: 2, timestamp: 2, data: "e2".to_string() }).unwrap();

        let event = stream.consume();
        assert!(event.is_some());
        assert_eq!(event.unwrap().id, 1);
    }

    #[test]
    fn test_adaptive_rate_limiter_adjustment() {
        let mut limiter = AdaptiveRateLimiter::new(100.0, 10.0, 1000.0, 0.7);

        let initial_rate = limiter.get_current_rate();

        // High utilization should decrease rate
        limiter.adjust_rate(0.95);
        assert!(limiter.get_current_rate() < initial_rate);

        // Low utilization should increase rate
        limiter.adjust_rate(0.2);
        // Rate should increase (though may not exceed initial_rate immediately)
    }

    #[test]
    fn test_backpressure_monitor() {
        let mut monitor = BackpressureMonitor::new(10);

        monitor.record_buffer_size(5);
        monitor.record_buffer_size(7);
        monitor.record_buffer_size(6);

        let avg = monitor.average_buffer_size();
        assert!((avg - 6.0).abs() < 0.1);
    }

    #[test]
    fn test_pipeline_stage() {
        let mut stage = PipelineStage::new(
            "stage1".to_string(),
            5,
            OverflowPolicy::Block,
            Duration::from_millis(10),
        );

        let event = Event { id: 1, timestamp: 1, data: "e1".to_string() };
        assert!(stage.push(event).is_ok());

        assert_eq!(stage.buffer_utilization(), 0.2); // 1/5
    }

    #[test]
    fn test_pipeline_multiple_stages() {
        let stage1 = PipelineStage::new("s1".to_string(), 5, OverflowPolicy::Block, Duration::from_millis(1));
        let stage2 = PipelineStage::new("s2".to_string(), 5, OverflowPolicy::Block, Duration::from_millis(1));

        let mut pipeline = BackpressurePipeline::new(vec![stage1, stage2], 10);

        let event = Event { id: 1, timestamp: 1, data: "e1".to_string() };
        assert!(pipeline.push(event).is_ok());
    }

    #[test]
    fn test_monitor_health_check() {
        let mut monitor = BackpressureMonitor::new(10);

        monitor.total_events = 100;
        monitor.dropped_events = 5;

        assert_eq!(monitor.drop_rate(), 0.05);

        let healthy = monitor.is_healthy(0.1, 0.8, 10);
        assert!(healthy); // Drop rate below threshold
    }
}
