// con08_event_loop.rs
//
// An Event Loop is a programming construct that waits for and dispatches events
// or messages in a program. It's the foundation of asynchronous I/O frameworks
// and is used in Node.js, browser JavaScript, and async Rust runtimes.
//
// Your task: Implement a simple event loop with timers and I/O events.
//
// Key concepts:
// - Event queue: Stores pending events
// - Event handlers: Functions that process events
// - Timers: Delayed execution
// - Non-blocking I/O: Process events without waiting

// I AM NOT DONE

use std::collections::{BinaryHeap, VecDeque};
use std::cmp::{Ordering, Reverse};

pub type EventId = usize;
pub type TimerId = usize;
pub type HandlerId = usize;

#[derive(Debug, Clone, PartialEq)]
pub enum Event {
    Timer(TimerId),
    IO(String),
    Custom(String),
}

#[derive(Debug, Clone)]
pub struct ScheduledEvent {
    pub id: EventId,
    pub event: Event,
    pub scheduled_time: u64,
}

impl PartialEq for ScheduledEvent {
    fn eq(&self, other: &Self) -> bool {
        self.scheduled_time == other.scheduled_time && self.id == other.id
    }
}

impl Eq for ScheduledEvent {}

impl PartialOrd for ScheduledEvent {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for ScheduledEvent {
    fn cmp(&self, other: &Self) -> Ordering {
        // Reverse ordering so earlier times have higher priority
        other.scheduled_time.cmp(&self.scheduled_time)
            .then_with(|| other.id.cmp(&self.id))
    }
}

pub type EventHandler = Box<dyn FnMut(&Event, &mut EventLoop)>;

pub struct EventLoop {
    current_time: u64,
    next_event_id: EventId,
    next_timer_id: TimerId,
    immediate_queue: VecDeque<ScheduledEvent>,
    timer_queue: BinaryHeap<ScheduledEvent>,
    handlers: Vec<EventHandler>,
    event_log: Vec<(u64, Event)>,
}

impl EventLoop {
    pub fn new() -> Self {
        Self {
            current_time: 0,
            next_event_id: 0,
            next_timer_id: 0,
            immediate_queue: VecDeque::new(),
            timer_queue: BinaryHeap::new(),
            handlers: Vec::new(),
            event_log: Vec::new(),
        }
    }

    pub fn schedule_immediate(&mut self, event: Event) -> EventId {
        // TODO: Schedule an event to run immediately (in the next tick)
        // Add to immediate_queue with current_time as scheduled_time
        todo!()
    }

    pub fn schedule_timer(&mut self, event: Event, delay: u64) -> EventId {
        // TODO: Schedule an event to run after a delay
        // Add to timer_queue with current_time + delay as scheduled_time
        todo!()
    }

    pub fn set_timeout(&mut self, delay: u64) -> TimerId {
        // TODO: Create a timer that fires after delay
        // Similar to JavaScript's setTimeout
        // Returns the timer ID
        todo!()
    }

    pub fn add_handler<F>(&mut self, handler: F) -> HandlerId
    where
        F: FnMut(&Event, &mut EventLoop) + 'static,
    {
        // TODO: Add an event handler
        // Return the handler ID (its index in the handlers vector)
        todo!()
    }

    fn process_event(&mut self, event: Event) {
        // TODO: Process an event by calling all handlers
        // 1. Log the event
        // 2. Call each handler with the event
        // Note: We need to be careful with borrowing - collect handler indices first
        todo!()
    }

    pub fn tick(&mut self) -> bool {
        // TODO: Process one iteration of the event loop
        // 1. Process all immediate events (in order)
        // 2. Check timer queue for events ready to fire
        // 3. Process the next ready timer event
        // 4. Increment current_time
        // 5. Return true if any event was processed
        todo!()
    }

    pub fn run(&mut self) {
        // TODO: Run the event loop until no more events
        while self.tick() {
            // Keep running
        }
    }

    pub fn run_for(&mut self, duration: u64) {
        // TODO: Run the event loop for a specific duration
        let end_time = self.current_time + duration;
        while self.current_time < end_time && self.tick() {
            // Keep running
        }
    }

    pub fn current_time(&self) -> u64 {
        self.current_time
    }

    pub fn has_pending_events(&self) -> bool {
        !self.immediate_queue.is_empty() || !self.timer_queue.is_empty()
    }

    pub fn get_event_log(&self) -> &[(u64, Event)] {
        &self.event_log
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_immediate_event() {
        let mut event_loop = EventLoop::new();
        event_loop.schedule_immediate(Event::Custom("test".to_string()));

        assert!(event_loop.has_pending_events());
        let processed = event_loop.tick();
        assert!(processed);
        assert!(!event_loop.has_pending_events());
    }

    #[test]
    fn test_timer_event() {
        let mut event_loop = EventLoop::new();
        event_loop.schedule_timer(Event::Custom("delayed".to_string()), 10);

        // Event should not fire immediately
        for _ in 0..9 {
            event_loop.tick();
        }

        let log = event_loop.get_event_log();
        assert!(log.is_empty());

        // Should fire on or after the 10th tick
        event_loop.tick();
        let log = event_loop.get_event_log();
        assert_eq!(log.len(), 1);
    }

    #[test]
    fn test_event_ordering() {
        let mut event_loop = EventLoop::new();

        event_loop.schedule_immediate(Event::Custom("first".to_string()));
        event_loop.schedule_immediate(Event::Custom("second".to_string()));
        event_loop.schedule_immediate(Event::Custom("third".to_string()));

        event_loop.run();

        let log = event_loop.get_event_log();
        assert_eq!(log.len(), 3);

        if let Event::Custom(ref s) = log[0].1 {
            assert_eq!(s, "first");
        }
        if let Event::Custom(ref s) = log[1].1 {
            assert_eq!(s, "second");
        }
    }

    #[test]
    fn test_timer_ordering() {
        let mut event_loop = EventLoop::new();

        event_loop.schedule_timer(Event::Custom("long".to_string()), 20);
        event_loop.schedule_timer(Event::Custom("short".to_string()), 5);
        event_loop.schedule_timer(Event::Custom("medium".to_string()), 10);

        event_loop.run();

        let log = event_loop.get_event_log();
        assert_eq!(log.len(), 3);

        // Should fire in order: short, medium, long
        if let Event::Custom(ref s) = log[0].1 {
            assert_eq!(s, "short");
        }
        if let Event::Custom(ref s) = log[1].1 {
            assert_eq!(s, "medium");
        }
        if let Event::Custom(ref s) = log[2].1 {
            assert_eq!(s, "long");
        }
    }

    #[test]
    fn test_mixed_events() {
        let mut event_loop = EventLoop::new();

        event_loop.schedule_timer(Event::Custom("timer".to_string()), 5);
        event_loop.schedule_immediate(Event::Custom("immediate".to_string()));

        event_loop.tick(); // Process immediate

        let log = event_loop.get_event_log();
        assert_eq!(log.len(), 1);
        if let Event::Custom(ref s) = log[0].1 {
            assert_eq!(s, "immediate");
        }

        event_loop.run(); // Process timer

        let log = event_loop.get_event_log();
        assert_eq!(log.len(), 2);
    }

    #[test]
    fn test_event_handler() {
        let mut event_loop = EventLoop::new();
        let mut count = 0;

        let handler = move |event: &Event, _: &mut EventLoop| {
            if matches!(event, Event::Custom(_)) {
                count += 1;
            }
        };

        event_loop.add_handler(handler);
        event_loop.schedule_immediate(Event::Custom("test1".to_string()));
        event_loop.schedule_immediate(Event::Custom("test2".to_string()));

        event_loop.run();

        // Handler should have been called twice (but we can't easily verify count here)
        assert_eq!(event_loop.get_event_log().len(), 2);
    }

    #[test]
    fn test_recursive_scheduling() {
        let mut event_loop = EventLoop::new();

        // Handler that schedules another event
        event_loop.add_handler(|event: &Event, ev_loop: &mut EventLoop| {
            if let Event::Custom(s) = event {
                if s == "spawn" {
                    ev_loop.schedule_immediate(Event::Custom("spawned".to_string()));
                }
            }
        });

        event_loop.schedule_immediate(Event::Custom("spawn".to_string()));
        event_loop.run();

        let log = event_loop.get_event_log();
        assert!(log.len() >= 2); // Original event + spawned event
    }

    #[test]
    fn test_run_for_duration() {
        let mut event_loop = EventLoop::new();

        event_loop.schedule_timer(Event::Custom("t1".to_string()), 5);
        event_loop.schedule_timer(Event::Custom("t2".to_string()), 15);
        event_loop.schedule_timer(Event::Custom("t3".to_string()), 25);

        event_loop.run_for(20);

        let log = event_loop.get_event_log();
        // Should have processed t1 and t2, but not t3
        assert_eq!(log.len(), 2);
        assert!(event_loop.has_pending_events()); // t3 still pending
    }

    #[test]
    fn test_set_timeout() {
        let mut event_loop = EventLoop::new();

        let timer1 = event_loop.set_timeout(10);
        let timer2 = event_loop.set_timeout(5);

        assert_ne!(timer1, timer2);

        event_loop.run();

        let log = event_loop.get_event_log();
        assert_eq!(log.len(), 2);
    }
}
