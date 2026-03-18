// con04_preemptive_scheduling.rs
//
// Preemptive Scheduling allows the scheduler to interrupt a running task and
// switch to another task. This is crucial for responsive systems where high-
// priority tasks need to run immediately.
//
// Your task: Implement a preemptive scheduler with priority and time slicing.
//
// Key concepts:
// - Context switching: Saving and restoring task state
// - Preemption points: When scheduler can interrupt tasks
// - Time slicing: Tasks are interrupted after their quantum expires

// I AM NOT DONE

use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
pub enum TaskState {
    Ready,
    Running,
    Waiting,
}

#[derive(Debug, Clone)]
pub struct Task {
    pub id: usize,
    pub priority: u32,
    pub remaining_time: u32,
    pub state: TaskState,
    pub time_slice_used: u32,
}

impl Task {
    pub fn new(id: usize, priority: u32, execution_time: u32) -> Self {
        Self {
            id,
            priority,
            remaining_time: execution_time,
            state: TaskState::Ready,
            time_slice_used: 0,
        }
    }

    pub fn is_complete(&self) -> bool {
        self.remaining_time == 0
    }
}

#[derive(Debug, Clone)]
pub struct SchedulerEvent {
    pub time: u32,
    pub event_type: EventType,
    pub task_id: usize,
}

#[derive(Debug, Clone, PartialEq)]
pub enum EventType {
    TaskStarted,
    TaskPreempted,
    TaskCompleted,
    ContextSwitch,
}

pub struct PreemptiveScheduler {
    ready_queue: VecDeque<Task>,
    running_task: Option<Task>,
    quantum: u32,
    current_time: u32,
    context_switch_cost: u32,
    events: Vec<SchedulerEvent>,
}

impl PreemptiveScheduler {
    pub fn new(quantum: u32, context_switch_cost: u32) -> Self {
        Self {
            ready_queue: VecDeque::new(),
            running_task: None,
            quantum,
            current_time: 0,
            context_switch_cost,
            events: Vec::new(),
        }
    }

    fn log_event(&mut self, event_type: EventType, task_id: usize) {
        self.events.push(SchedulerEvent {
            time: self.current_time,
            event_type,
            task_id,
        });
    }

    fn context_switch(&mut self) {
        // TODO: Simulate context switch overhead
        // Increment current_time by context_switch_cost
        todo!()
    }

    fn should_preempt(&self, new_task: &Task) -> bool {
        // TODO: Determine if the running task should be preempted
        // Preempt if:
        // 1. No task is running, OR
        // 2. New task has higher priority, OR
        // 3. Running task has used up its quantum
        todo!()
    }

    pub fn add_task(&mut self, task: Task) {
        // TODO: Add a task and potentially preempt the running task
        // 1. Check if the new task should preempt the current one
        // 2. If yes, move running task back to ready queue and context switch
        // 3. Add the new task appropriately
        todo!()
    }

    pub fn tick(&mut self) -> Option<usize> {
        // TODO: Execute one time unit
        // 1. If no task is running, schedule the next one from ready queue
        // 2. Execute the running task for 1 time unit
        // 3. Check if quantum expired or task completed
        // 4. Handle preemption if needed
        // 5. Return the ID of the task that executed (or None)
        todo!()
    }

    pub fn run_until_idle(&mut self) {
        // TODO: Run until all tasks are complete
        while self.running_task.is_some() || !self.ready_queue.is_empty() {
            self.tick();
        }
    }

    pub fn get_events(&self) -> &[SchedulerEvent] {
        &self.events
    }

    pub fn current_time(&self) -> u32 {
        self.current_time
    }

    pub fn is_idle(&self) -> bool {
        self.running_task.is_none() && self.ready_queue.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_task_no_preemption() {
        let mut scheduler = PreemptiveScheduler::new(10, 1);
        scheduler.add_task(Task::new(1, 5, 8));

        scheduler.run_until_idle();

        let events = scheduler.get_events();
        assert!(events.iter().any(|e| e.event_type == EventType::TaskStarted));
        assert!(events.iter().any(|e| e.event_type == EventType::TaskCompleted));
        assert_eq!(events.iter().filter(|e| e.event_type == EventType::TaskPreempted).count(), 0);
    }

    #[test]
    fn test_quantum_expiration() {
        let mut scheduler = PreemptiveScheduler::new(5, 1);
        scheduler.add_task(Task::new(1, 5, 12));

        for _ in 0..5 {
            scheduler.tick();
        }

        // Task should be preempted after quantum expires
        let events = scheduler.get_events();
        assert!(events.iter().any(|e| e.event_type == EventType::TaskPreempted));
    }

    #[test]
    fn test_priority_preemption() {
        let mut scheduler = PreemptiveScheduler::new(10, 1);
        scheduler.add_task(Task::new(1, 5, 20));

        // Let task 1 run for a bit
        for _ in 0..3 {
            scheduler.tick();
        }

        // Add higher priority task
        scheduler.add_task(Task::new(2, 10, 5));

        // Task 1 should be preempted
        let events = scheduler.get_events();
        assert!(events.iter().any(|e| e.event_type == EventType::TaskPreempted && e.task_id == 1));
        assert!(events.iter().any(|e| e.event_type == EventType::ContextSwitch));
    }

    #[test]
    fn test_context_switch_overhead() {
        let mut scheduler = PreemptiveScheduler::new(5, 2);
        scheduler.add_task(Task::new(1, 5, 10));
        scheduler.add_task(Task::new(2, 10, 5)); // Higher priority

        scheduler.run_until_idle();

        // Total time should include context switch overhead
        // Task 2: 5 units + switch (2) + Task 1: 10 units
        assert!(scheduler.current_time() >= 15);
    }

    #[test]
    fn test_round_robin_with_preemption() {
        let mut scheduler = PreemptiveScheduler::new(4, 0);
        scheduler.add_task(Task::new(1, 5, 10));
        scheduler.add_task(Task::new(2, 5, 10));

        scheduler.run_until_idle();

        let events = scheduler.get_events();

        // Both tasks should be preempted and resumed multiple times
        let task1_starts = events.iter().filter(|e| e.task_id == 1 && e.event_type == EventType::TaskStarted).count();
        let task2_starts = events.iter().filter(|e| e.task_id == 2 && e.event_type == EventType::TaskStarted).count();

        assert!(task1_starts > 1);
        assert!(task2_starts > 1);
    }

    #[test]
    fn test_no_preemption_on_lower_priority() {
        let mut scheduler = PreemptiveScheduler::new(10, 1);
        scheduler.add_task(Task::new(1, 10, 15));

        for _ in 0..5 {
            scheduler.tick();
        }

        // Add lower priority task
        let events_before = scheduler.get_events().len();
        scheduler.add_task(Task::new(2, 5, 5));

        // Should not cause preemption
        let events = scheduler.get_events();
        assert_eq!(events.len(), events_before); // No new events
    }

    #[test]
    fn test_task_completion_during_quantum() {
        let mut scheduler = PreemptiveScheduler::new(10, 0);
        scheduler.add_task(Task::new(1, 5, 3));

        scheduler.run_until_idle();

        let events = scheduler.get_events();
        assert!(events.iter().any(|e| e.event_type == EventType::TaskCompleted));
        assert_eq!(events.iter().filter(|e| e.event_type == EventType::TaskPreempted).count(), 0);
        assert_eq!(scheduler.current_time(), 3);
    }
}
