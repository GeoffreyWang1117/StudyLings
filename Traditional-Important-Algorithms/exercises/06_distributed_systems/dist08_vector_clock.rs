// dist08_vector_clock.rs
//
// Vector Clocks track causality in distributed systems without synchronized clocks.
// Each node maintains a vector of logical timestamps - one for each node in the system.
//
// Key properties:
// - Happens-before relationship: If event A → event B, then VC(A) < VC(B)
// - Concurrent events: Events are concurrent if neither VC(A) < VC(B) nor VC(B) < VC(A)
// - Causal ordering: Can determine if events are causally related or concurrent
//
// Your task: Implement vector clocks for tracking causality.
//
// Key concepts:
// - Local event: Increment own clock
// - Send event: Increment own clock, send vector with message
// - Receive event: Merge received vector (take max of each element), increment own clock
// - Comparison: Less than, greater than, concurrent, or equal

// I AM NOT DONE

use std::collections::HashMap;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq)]
pub struct VectorClock {
    clock: HashMap<usize, u64>, // node_id -> timestamp
    node_id: usize,
}

impl VectorClock {
    pub fn new(node_id: usize, num_nodes: usize) -> Self {
        let mut clock = HashMap::new();
        for i in 0..num_nodes {
            clock.insert(i, 0);
        }
        Self { clock, node_id }
    }

    pub fn increment(&mut self) {
        // TODO: Increment this node's timestamp
        // - Increment the counter for node_id
        todo!()
    }

    pub fn get(&self, node_id: usize) -> u64 {
        *self.clock.get(&node_id).unwrap_or(&0)
    }

    pub fn set(&mut self, node_id: usize, value: u64) {
        self.clock.insert(node_id, value);
    }

    pub fn merge(&mut self, other: &VectorClock) {
        // TODO: Merge another vector clock into this one
        // - For each node in other's clock, take the maximum of the two values
        // - Don't forget to increment own clock after merging!
        todo!()
    }

    pub fn compare(&self, other: &VectorClock) -> ClockOrdering {
        // TODO: Compare two vector clocks
        // - If all entries in self <= other and at least one is <, return HappensBefore
        // - If all entries in self >= other and at least one is >, return HappensAfter
        // - If all entries are equal, return Equal
        // - Otherwise, return Concurrent
        todo!()
    }

    pub fn happens_before(&self, other: &VectorClock) -> bool {
        self.compare(other) == ClockOrdering::HappensBefore
    }

    pub fn happens_after(&self, other: &VectorClock) -> bool {
        self.compare(other) == ClockOrdering::HappensAfter
    }

    pub fn is_concurrent(&self, other: &VectorClock) -> bool {
        self.compare(other) == ClockOrdering::Concurrent
    }

    pub fn clone_clock(&self) -> VectorClock {
        VectorClock {
            clock: self.clock.clone(),
            node_id: self.node_id,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ClockOrdering {
    HappensBefore,  // self < other
    HappensAfter,   // self > other
    Concurrent,     // self || other (concurrent)
    Equal,          // self == other
}

#[derive(Debug, Clone)]
pub struct Event {
    pub id: usize,
    pub node_id: usize,
    pub event_type: EventType,
    pub clock: VectorClock,
}

#[derive(Debug, Clone, PartialEq)]
pub enum EventType {
    Local(String),
    Send(String, usize),      // message, recipient
    Receive(String, usize),   // message, sender
}

pub struct DistributedSystem {
    nodes: HashMap<usize, VectorClock>,
    events: Vec<Event>,
    next_event_id: usize,
}

impl DistributedSystem {
    pub fn new(num_nodes: usize) -> Self {
        let mut nodes = HashMap::new();
        for i in 0..num_nodes {
            nodes.insert(i, VectorClock::new(i, num_nodes));
        }

        Self {
            nodes,
            events: Vec::new(),
            next_event_id: 0,
        }
    }

    pub fn local_event(&mut self, node_id: usize, description: String) -> usize {
        // TODO: Process a local event on a node
        // - Get the node's vector clock
        // - Increment it
        // - Create an Event with the current clock state
        // - Add event to events list
        // - Return event ID
        todo!()
    }

    pub fn send_message(&mut self, from: usize, to: usize, message: String) -> (usize, VectorClock) {
        // TODO: Process a send event
        // - Get sender's vector clock
        // - Increment it
        // - Create a Send event
        // - Return (event_id, copy of sender's clock to include with message)
        todo!()
    }

    pub fn receive_message(&mut self, node_id: usize, sender: usize, message: String,
                          sender_clock: VectorClock) -> usize {
        // TODO: Process a receive event
        // - Get receiver's vector clock
        // - Merge with sender's clock (this updates receiver's clock)
        // - Create a Receive event
        // - Return event ID
        todo!()
    }

    pub fn get_event(&self, event_id: usize) -> Option<&Event> {
        self.events.iter().find(|e| e.id == event_id)
    }

    pub fn get_node_clock(&self, node_id: usize) -> Option<&VectorClock> {
        self.nodes.get(&node_id)
    }

    pub fn compare_events(&self, event_id1: usize, event_id2: usize) -> Option<ClockOrdering> {
        let e1 = self.get_event(event_id1)?;
        let e2 = self.get_event(event_id2)?;
        Some(e1.clock.compare(&e2.clock))
    }

    pub fn get_concurrent_events(&self) -> Vec<(usize, usize)> {
        // TODO: Find all pairs of concurrent events
        // - Compare all pairs of events
        // - Return pairs where events are concurrent
        // - Only include each pair once (i.e., (a, b) not both (a, b) and (b, a))
        todo!()
    }

    pub fn get_causal_history(&self, event_id: usize) -> Vec<usize> {
        // TODO: Get all events that happened before this event
        // - Find all events e where e.clock < target_event.clock
        // - Return their event IDs
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vector_clock_creation() {
        let vc = VectorClock::new(0, 3);
        assert_eq!(vc.get(0), 0);
        assert_eq!(vc.get(1), 0);
        assert_eq!(vc.get(2), 0);
    }

    #[test]
    fn test_increment() {
        let mut vc = VectorClock::new(0, 3);
        vc.increment();
        assert_eq!(vc.get(0), 1);
        assert_eq!(vc.get(1), 0);

        vc.increment();
        assert_eq!(vc.get(0), 2);
    }

    #[test]
    fn test_merge() {
        let mut vc1 = VectorClock::new(0, 3);
        let mut vc2 = VectorClock::new(1, 3);

        vc1.set(0, 5);
        vc1.set(1, 2);
        vc1.set(2, 3);

        vc2.set(0, 3);
        vc2.set(1, 6);
        vc2.set(2, 4);

        vc1.merge(&vc2);

        // After merge, vc1 should have max of each + its own increment
        assert_eq!(vc1.get(0), 6); // max(5, 3) + 1
        assert_eq!(vc1.get(1), 6); // max(2, 6)
        assert_eq!(vc1.get(2), 4); // max(3, 4)
    }

    #[test]
    fn test_happens_before() {
        let mut vc1 = VectorClock::new(0, 2);
        let mut vc2 = VectorClock::new(0, 2);

        vc1.set(0, 1);
        vc1.set(1, 2);

        vc2.set(0, 2);
        vc2.set(1, 3);

        assert_eq!(vc1.compare(&vc2), ClockOrdering::HappensBefore);
        assert!(vc1.happens_before(&vc2));
    }

    #[test]
    fn test_happens_after() {
        let mut vc1 = VectorClock::new(0, 2);
        let mut vc2 = VectorClock::new(0, 2);

        vc1.set(0, 5);
        vc1.set(1, 4);

        vc2.set(0, 2);
        vc2.set(1, 3);

        assert_eq!(vc1.compare(&vc2), ClockOrdering::HappensAfter);
        assert!(vc1.happens_after(&vc2));
    }

    #[test]
    fn test_concurrent() {
        let mut vc1 = VectorClock::new(0, 2);
        let mut vc2 = VectorClock::new(1, 2);

        vc1.set(0, 3);
        vc1.set(1, 1);

        vc2.set(0, 1);
        vc2.set(1, 3);

        assert_eq!(vc1.compare(&vc2), ClockOrdering::Concurrent);
        assert!(vc1.is_concurrent(&vc2));
        assert!(vc2.is_concurrent(&vc1)); // Symmetry
    }

    #[test]
    fn test_equal() {
        let mut vc1 = VectorClock::new(0, 2);
        let mut vc2 = VectorClock::new(1, 2);

        vc1.set(0, 3);
        vc1.set(1, 2);

        vc2.set(0, 3);
        vc2.set(1, 2);

        assert_eq!(vc1.compare(&vc2), ClockOrdering::Equal);
    }

    #[test]
    fn test_local_event() {
        let mut system = DistributedSystem::new(3);

        let event_id = system.local_event(0, "process data".to_string());

        let clock = system.get_node_clock(0).unwrap();
        assert_eq!(clock.get(0), 1);

        let event = system.get_event(event_id).unwrap();
        assert_eq!(event.node_id, 0);
    }

    #[test]
    fn test_send_receive() {
        let mut system = DistributedSystem::new(2);

        let (_, sender_clock) = system.send_message(0, 1, "hello".to_string());
        system.receive_message(1, 0, "hello".to_string(), sender_clock);

        let clock0 = system.get_node_clock(0).unwrap();
        let clock1 = system.get_node_clock(1).unwrap();

        // Node 0 sent, so its clock[0] = 1
        assert_eq!(clock0.get(0), 1);

        // Node 1 received, so it merged and incremented
        assert!(clock1.get(0) >= 1);
        assert!(clock1.get(1) >= 1);
    }

    #[test]
    fn test_causal_ordering() {
        let mut system = DistributedSystem::new(2);

        let e1 = system.local_event(0, "event1".to_string());
        let (_, clock) = system.send_message(0, 1, "msg".to_string());
        let e3 = system.receive_message(1, 0, "msg".to_string(), clock);

        let ordering = system.compare_events(e1, e3);
        assert_eq!(ordering, Some(ClockOrdering::HappensBefore));
    }

    #[test]
    fn test_concurrent_events_detection() {
        let mut system = DistributedSystem::new(2);

        // Two independent events on different nodes
        let e1 = system.local_event(0, "event_a".to_string());
        let e2 = system.local_event(1, "event_b".to_string());

        let ordering = system.compare_events(e1, e2);
        assert_eq!(ordering, Some(ClockOrdering::Concurrent));
    }

    #[test]
    fn test_multiple_messages() {
        let mut system = DistributedSystem::new(3);

        // Node 0 sends to node 1
        let (_, clock1) = system.send_message(0, 1, "msg1".to_string());
        system.receive_message(1, 0, "msg1".to_string(), clock1);

        // Node 1 sends to node 2
        let (_, clock2) = system.send_message(1, 2, "msg2".to_string());
        system.receive_message(2, 1, "msg2".to_string(), clock2);

        // Node 2 should have causal information from node 0
        let clock2 = system.get_node_clock(2).unwrap();
        assert!(clock2.get(0) > 0); // Knows about node 0's event
    }

    #[test]
    fn test_causal_history() {
        let mut system = DistributedSystem::new(2);

        let e1 = system.local_event(0, "a".to_string());
        let e2 = system.local_event(0, "b".to_string());
        let (_, clock) = system.send_message(0, 1, "msg".to_string());
        let e4 = system.receive_message(1, 0, "msg".to_string(), clock);

        let history = system.get_causal_history(e4);

        // e4's causal history should include e1, e2, and the send event
        assert!(history.len() >= 2);
        assert!(history.contains(&e1));
        assert!(history.contains(&e2));
    }
}
