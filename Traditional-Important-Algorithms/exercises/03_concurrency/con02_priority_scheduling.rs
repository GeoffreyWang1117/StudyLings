// con02_priority_scheduling.rs
//
// Priority Scheduling assigns a priority to each task and always executes
// the highest-priority task that's ready. This can be preemptive (where a
// higher-priority task can interrupt a lower-priority one) or non-preemptive.
//
// Your task: Implement a priority-based scheduler.
//
// Key concepts:
// - Priority levels: Higher number = higher priority
// - Starvation: Low-priority tasks may never execute
// - Aging: Can be used to prevent starvation

// I AM NOT DONE

use std::collections::BinaryHeap;
use std::cmp::Ordering;

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct Task {
    pub id: usize,
    pub priority: u32,
    pub remaining_time: u32,
    pub age: u32, // For aging mechanism
}

impl Task {
    pub fn new(id: usize, priority: u32, execution_time: u32) -> Self {
        Self {
            id,
            priority,
            remaining_time: execution_time,
            age: 0,
        }
    }

    pub fn is_complete(&self) -> bool {
        self.remaining_time == 0
    }

    pub fn effective_priority(&self) -> u32 {
        // TODO: Calculate effective priority with aging
        // Hint: Add age to base priority to prevent starvation
        todo!()
    }
}

impl Ord for Task {
    fn cmp(&self, other: &Self) -> Ordering {
        // TODO: Compare tasks by effective priority (higher priority comes first)
        // Break ties by task ID (lower ID first)
        todo!()
    }
}

impl PartialOrd for Task {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct PriorityScheduler {
    ready_queue: BinaryHeap<Task>,
    current_time: u32,
    enable_aging: bool,
}

impl PriorityScheduler {
    pub fn new(enable_aging: bool) -> Self {
        Self {
            ready_queue: BinaryHeap::new(),
            current_time: 0,
            enable_aging,
        }
    }

    pub fn add_task(&mut self, task: Task) {
        // TODO: Add a task to the ready queue
        todo!()
    }

    fn age_tasks(&mut self) {
        // TODO: Increment age for all waiting tasks (if aging is enabled)
        // Hint: Drain the heap, age all tasks, and rebuild it
        todo!()
    }

    pub fn run_next(&mut self, quantum: u32) -> Option<usize> {
        // TODO: Run the highest priority task for the given quantum
        // 1. Age all waiting tasks if aging is enabled
        // 2. Pop the highest priority task
        // 3. Execute it for min(quantum, remaining_time)
        // 4. Update current_time
        // 5. If not complete, reset age to 0 and add back to queue
        // 6. Return the task ID (or None if no tasks)
        todo!()
    }

    pub fn run_to_completion(&mut self) -> Vec<(usize, u32)> {
        // TODO: Run all tasks to completion (non-preemptive)
        // Return a vector of (task_id, execution_time) pairs
        todo!()
    }

    pub fn is_empty(&self) -> bool {
        self.ready_queue.is_empty()
    }

    pub fn current_time(&self) -> u32 {
        self.current_time
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_priority_order() {
        let mut scheduler = PriorityScheduler::new(false);
        scheduler.add_task(Task::new(1, 1, 5));
        scheduler.add_task(Task::new(2, 3, 5));
        scheduler.add_task(Task::new(3, 2, 5));

        // Should run in order: 2 (priority 3), 3 (priority 2), 1 (priority 1)
        assert_eq!(scheduler.run_next(10), Some(2));
        assert_eq!(scheduler.run_next(10), Some(3));
        assert_eq!(scheduler.run_next(10), Some(1));
    }

    #[test]
    fn test_equal_priority() {
        let mut scheduler = PriorityScheduler::new(false);
        scheduler.add_task(Task::new(1, 5, 5));
        scheduler.add_task(Task::new(2, 5, 5));
        scheduler.add_task(Task::new(3, 5, 5));

        // Should break ties by task ID
        assert_eq!(scheduler.run_next(10), Some(1));
        assert_eq!(scheduler.run_next(10), Some(2));
        assert_eq!(scheduler.run_next(10), Some(3));
    }

    #[test]
    fn test_preemptive_scheduling() {
        let mut scheduler = PriorityScheduler::new(false);
        scheduler.add_task(Task::new(1, 1, 10));

        scheduler.run_next(3); // Run task 1 for 3 units

        scheduler.add_task(Task::new(2, 5, 5)); // Higher priority arrives

        // Task 2 should run next (preemption)
        assert_eq!(scheduler.run_next(10), Some(2));
        assert_eq!(scheduler.run_next(10), Some(1));
    }

    #[test]
    fn test_aging_prevents_starvation() {
        let mut scheduler = PriorityScheduler::new(true);
        scheduler.add_task(Task::new(1, 1, 5));
        scheduler.add_task(Task::new(2, 10, 5));

        // Without aging, task 1 would never run
        // With aging, task 1's priority increases each quantum
        scheduler.run_next(1); // Task 2 runs (age 1 -> priority 11)
        scheduler.run_next(1); // Task 2 runs (age 2 -> priority 12)
        // Eventually task 1's aged priority should allow it to run

        let mut task1_ran = false;
        for _ in 0..20 {
            if let Some(id) = scheduler.run_next(1) {
                if id == 1 {
                    task1_ran = true;
                }
            }
        }
        assert!(task1_ran, "Task 1 should eventually run with aging");
    }

    #[test]
    fn test_run_to_completion() {
        let mut scheduler = PriorityScheduler::new(false);
        scheduler.add_task(Task::new(1, 2, 5));
        scheduler.add_task(Task::new(2, 3, 8));
        scheduler.add_task(Task::new(3, 1, 3));

        let execution_log = scheduler.run_to_completion();

        assert_eq!(execution_log.len(), 3);
        assert_eq!(execution_log[0].0, 2); // Highest priority
        assert_eq!(execution_log[1].0, 1); // Medium priority
        assert_eq!(execution_log[2].0, 3); // Lowest priority
    }

    #[test]
    fn test_mixed_execution_times() {
        let mut scheduler = PriorityScheduler::new(false);
        scheduler.add_task(Task::new(1, 10, 1));
        scheduler.add_task(Task::new(2, 5, 10));
        scheduler.add_task(Task::new(3, 8, 3));

        assert_eq!(scheduler.run_next(5), Some(1)); // Priority 10
        assert_eq!(scheduler.run_next(5), Some(3)); // Priority 8
        assert_eq!(scheduler.run_next(5), Some(2)); // Priority 5 (partial)
        assert_eq!(scheduler.run_next(5), Some(2)); // Priority 5 (complete)
    }
}
