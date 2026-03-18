// con01_round_robin.rs
//
// Round Robin Scheduling is a preemptive scheduling algorithm where each task
// gets a fixed time slice (quantum) to execute. When a task's quantum expires,
// it moves to the back of the queue, and the next task gets to run.
//
// Your task: Implement a round robin scheduler that manages task execution.
//
// Key concepts:
// - Time quantum: Fixed time slice for each task
// - Queue-based: Tasks wait in a FIFO queue
// - Fair: Each task gets equal CPU time

// I AM NOT DONE

use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
pub struct Task {
    pub id: usize,
    pub remaining_time: u32,
}

impl Task {
    pub fn new(id: usize, execution_time: u32) -> Self {
        Self {
            id,
            remaining_time: execution_time,
        }
    }

    pub fn is_complete(&self) -> bool {
        self.remaining_time == 0
    }
}

pub struct RoundRobinScheduler {
    queue: VecDeque<Task>,
    quantum: u32,
    current_time: u32,
}

impl RoundRobinScheduler {
    pub fn new(quantum: u32) -> Self {
        Self {
            queue: VecDeque::new(),
            quantum,
            current_time: 0,
        }
    }

    pub fn add_task(&mut self, task: Task) {
        // TODO: Add a task to the ready queue
        todo!()
    }

    pub fn run_next(&mut self) -> Option<usize> {
        // TODO: Run the next task for one quantum (or until completion)
        // 1. Remove the task from the front of the queue
        // 2. Execute it for min(quantum, remaining_time)
        // 3. Update current_time
        // 4. If the task isn't complete, add it back to the queue
        // 5. Return the ID of the task that just ran (or None if queue is empty)
        todo!()
    }

    pub fn run_all(&mut self) -> Vec<(usize, u32, u32)> {
        // TODO: Run all tasks until completion
        // Return a vector of (task_id, start_time, end_time) for each execution slice
        todo!()
    }

    pub fn is_empty(&self) -> bool {
        self.queue.is_empty()
    }

    pub fn current_time(&self) -> u32 {
        self.current_time
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_task() {
        let mut scheduler = RoundRobinScheduler::new(10);
        scheduler.add_task(Task::new(1, 5));

        let task_id = scheduler.run_next();
        assert_eq!(task_id, Some(1));
        assert_eq!(scheduler.current_time(), 5);
        assert!(scheduler.is_empty());
    }

    #[test]
    fn test_multiple_tasks_within_quantum() {
        let mut scheduler = RoundRobinScheduler::new(10);
        scheduler.add_task(Task::new(1, 5));
        scheduler.add_task(Task::new(2, 8));
        scheduler.add_task(Task::new(3, 3));

        scheduler.run_next(); // Task 1: 0-5
        scheduler.run_next(); // Task 2: 5-13
        scheduler.run_next(); // Task 3: 13-16

        assert_eq!(scheduler.current_time(), 16);
        assert!(scheduler.is_empty());
    }

    #[test]
    fn test_task_exceeds_quantum() {
        let mut scheduler = RoundRobinScheduler::new(5);
        scheduler.add_task(Task::new(1, 12));

        scheduler.run_next(); // 0-5, task goes back to queue
        assert!(!scheduler.is_empty());
        assert_eq!(scheduler.current_time(), 5);

        scheduler.run_next(); // 5-10, task goes back to queue
        assert!(!scheduler.is_empty());
        assert_eq!(scheduler.current_time(), 10);

        scheduler.run_next(); // 10-12, task completes
        assert!(scheduler.is_empty());
        assert_eq!(scheduler.current_time(), 12);
    }

    #[test]
    fn test_interleaved_execution() {
        let mut scheduler = RoundRobinScheduler::new(4);
        scheduler.add_task(Task::new(1, 10));
        scheduler.add_task(Task::new(2, 10));

        let execution_log = scheduler.run_all();

        // Should alternate between tasks
        assert_eq!(execution_log.len(), 6); // 3 slices per task
        assert_eq!(execution_log[0].0, 1); // Task 1: 0-4
        assert_eq!(execution_log[1].0, 2); // Task 2: 4-8
        assert_eq!(execution_log[2].0, 1); // Task 1: 8-12
        assert_eq!(execution_log[3].0, 2); // Task 2: 12-16
        assert_eq!(execution_log[4].0, 1); // Task 1: 16-18
        assert_eq!(execution_log[5].0, 2); // Task 2: 18-20
    }

    #[test]
    fn test_varying_arrival_times() {
        let mut scheduler = RoundRobinScheduler::new(3);
        scheduler.add_task(Task::new(1, 7));

        scheduler.run_next(); // Task 1: 0-3

        scheduler.add_task(Task::new(2, 5));
        scheduler.run_next(); // Task 2: 3-6
        scheduler.run_next(); // Task 1: 6-9
        scheduler.run_next(); // Task 2: 9-11
        scheduler.run_next(); // Task 1: 11-12

        assert!(scheduler.is_empty());
        assert_eq!(scheduler.current_time(), 12);
    }
}
