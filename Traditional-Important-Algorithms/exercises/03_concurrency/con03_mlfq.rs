// con03_mlfq.rs
//
// Multi-Level Feedback Queue (MLFQ) is an advanced scheduling algorithm that
// uses multiple priority queues. Tasks start at the highest priority and move
// to lower priorities if they use their full quantum. This favors I/O-bound
// and interactive tasks while still completing CPU-bound tasks.
//
// Your task: Implement a multi-level feedback queue scheduler.
//
// Key concepts:
// - Multiple queues with different priorities
// - Dynamic priority adjustment based on behavior
// - Quantum increases at lower priority levels

// I AM NOT DONE

use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
pub struct Task {
    pub id: usize,
    pub remaining_time: u32,
    pub priority_level: usize,
}

impl Task {
    pub fn new(id: usize, execution_time: u32) -> Self {
        Self {
            id,
            remaining_time: execution_time,
            priority_level: 0, // Start at highest priority
        }
    }

    pub fn is_complete(&self) -> bool {
        self.remaining_time == 0
    }
}

pub struct MLFQ {
    queues: Vec<VecDeque<Task>>,
    quantums: Vec<u32>,
    current_time: u32,
    boost_interval: u32,
    time_since_boost: u32,
}

impl MLFQ {
    pub fn new(num_levels: usize, base_quantum: u32, boost_interval: u32) -> Self {
        // Create queues and quantum sizes
        let mut queues = Vec::new();
        let mut quantums = Vec::new();

        for i in 0..num_levels {
            queues.push(VecDeque::new());
            // Quantum doubles at each lower level
            quantums.push(base_quantum * 2_u32.pow(i as u32));
        }

        Self {
            queues,
            quantums,
            current_time: 0,
            boost_interval,
            time_since_boost: 0,
        }
    }

    pub fn add_task(&mut self, task: Task) {
        // TODO: Add a task to the appropriate queue based on its priority level
        todo!()
    }

    fn boost_all_tasks(&mut self) {
        // TODO: Move all tasks to the highest priority queue
        // This prevents starvation of long-running tasks
        todo!()
    }

    fn find_next_task(&mut self) -> Option<Task> {
        // TODO: Find the next task to run from the highest non-empty queue
        todo!()
    }

    pub fn run_next(&mut self) -> Option<(usize, usize, u32)> {
        // TODO: Run the next task
        // 1. Check if it's time for a priority boost
        // 2. Find the next task from the highest priority queue
        // 3. Get the quantum for that priority level
        // 4. Execute for min(quantum, remaining_time)
        // 5. If the task used its full quantum AND isn't complete, demote it
        // 6. If the task didn't use full quantum, keep it at same priority
        // 7. Update current_time and time_since_boost
        // 8. Return (task_id, priority_level, time_executed)
        todo!()
    }

    pub fn run_all(&mut self) -> Vec<(usize, usize, u32)> {
        // TODO: Run all tasks until completion
        // Return a vector of (task_id, priority_level, time_slice) for each execution
        todo!()
    }

    pub fn is_empty(&self) -> bool {
        self.queues.iter().all(|q| q.is_empty())
    }

    pub fn current_time(&self) -> u32 {
        self.current_time
    }

    pub fn queue_lengths(&self) -> Vec<usize> {
        self.queues.iter().map(|q| q.len()).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_task() {
        let mut mlfq = MLFQ::new(3, 4, 100);
        mlfq.add_task(Task::new(1, 10));

        let result = mlfq.run_next();
        assert_eq!(result, Some((1, 0, 4))); // Run for quantum at level 0

        let result = mlfq.run_next();
        assert_eq!(result, Some((1, 1, 6))); // Demoted to level 1, runs for remaining time
    }

    #[test]
    fn test_task_demotion() {
        let mut mlfq = MLFQ::new(3, 2, 100);
        mlfq.add_task(Task::new(1, 20));

        // Task should be demoted after using full quantum
        mlfq.run_next(); // Level 0, quantum 2
        assert_eq!(mlfq.queue_lengths(), vec![0, 1, 0]);

        mlfq.run_next(); // Level 1, quantum 4
        assert_eq!(mlfq.queue_lengths(), vec![0, 0, 1]);

        mlfq.run_next(); // Level 2, quantum 8
        assert_eq!(mlfq.queue_lengths(), vec![0, 0, 1]); // Stays at lowest level
    }

    #[test]
    fn test_io_bound_task() {
        let mut mlfq = MLFQ::new(3, 10, 100);

        // Simulate I/O-bound task (short CPU bursts)
        mlfq.add_task(Task::new(1, 3));

        let result = mlfq.run_next();
        // Should complete in first quantum without demotion
        assert_eq!(result, Some((1, 0, 3)));
        assert!(mlfq.is_empty());
    }

    #[test]
    fn test_mixed_tasks() {
        let mut mlfq = MLFQ::new(3, 4, 100);

        mlfq.add_task(Task::new(1, 20)); // CPU-bound
        mlfq.add_task(Task::new(2, 3));  // I/O-bound

        // I/O-bound task should stay at high priority
        let mut executions = vec![];
        while !mlfq.is_empty() {
            if let Some((id, level, _)) = mlfq.run_next() {
                executions.push((id, level));
            }
        }

        // Task 2 should appear at high priority levels
        assert!(executions.iter().any(|&(id, level)| id == 2 && level == 0));
    }

    #[test]
    fn test_priority_boost() {
        let mut mlfq = MLFQ::new(3, 5, 20);

        mlfq.add_task(Task::new(1, 50));

        // Run for a while, task will be demoted
        for _ in 0..3 {
            mlfq.run_next();
        }

        // Should be at low priority now
        assert!(mlfq.queue_lengths()[2] > 0 || mlfq.is_empty());

        // Add a new task and continue running until boost
        if !mlfq.is_empty() {
            let initial_time = mlfq.current_time();
            while mlfq.current_time() - initial_time < 20 && !mlfq.is_empty() {
                mlfq.run_next();
            }

            // After boost, tasks should be at high priority
            if !mlfq.is_empty() {
                assert!(mlfq.queue_lengths()[0] > 0);
            }
        }
    }

    #[test]
    fn test_round_robin_within_level() {
        let mut mlfq = MLFQ::new(2, 3, 100);

        mlfq.add_task(Task::new(1, 3));
        mlfq.add_task(Task::new(2, 3));
        mlfq.add_task(Task::new(3, 3));

        let executions = mlfq.run_all();

        // All tasks should complete at level 0 (I/O-bound behavior)
        assert_eq!(executions.len(), 3);
        assert!(executions.iter().all(|&(_, level, _)| level == 0));
    }

    #[test]
    fn test_quantum_doubling() {
        let mlfq = MLFQ::new(4, 2, 100);

        assert_eq!(mlfq.quantums, vec![2, 4, 8, 16]);
    }
}
