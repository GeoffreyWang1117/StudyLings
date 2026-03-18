// con06_work_stealing.rs
//
// Work Stealing is a scheduling strategy where idle threads steal work from
// busy threads' queues. Each thread has its own deque (double-ended queue)
// where it pushes/pops tasks from one end, while other threads can steal
// from the other end.
//
// Your task: Implement a work-stealing scheduler with multiple worker threads.
//
// Key concepts:
// - Per-thread work queues (deques)
// - LIFO for local operations, FIFO for stealing
// - Load balancing through theft
// - Reduced contention compared to global queue

// I AM NOT DONE

use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
pub struct Task {
    pub id: usize,
    pub execution_time: u32,
}

impl Task {
    pub fn new(id: usize, execution_time: u32) -> Self {
        Self { id, execution_time }
    }
}

#[derive(Debug)]
pub struct WorkerQueue {
    pub worker_id: usize,
    deque: VecDeque<Task>,
    total_executed: u32,
    tasks_completed: usize,
    tasks_stolen: usize,
    tasks_stolen_from_me: usize,
}

impl WorkerQueue {
    pub fn new(worker_id: usize) -> Self {
        Self {
            worker_id,
            deque: VecDeque::new(),
            total_executed: 0,
            tasks_completed: 0,
            tasks_stolen: 0,
            tasks_stolen_from_me: 0,
        }
    }

    pub fn push(&mut self, task: Task) {
        // TODO: Push task to the back of the deque (LIFO for local operations)
        todo!()
    }

    pub fn pop(&mut self) -> Option<Task> {
        // TODO: Pop task from the back of the deque (LIFO for local operations)
        todo!()
    }

    pub fn steal(&mut self) -> Option<Task> {
        // TODO: Steal task from the front of the deque (FIFO for stealing)
        // Increment tasks_stolen_from_me counter
        todo!()
    }

    pub fn len(&self) -> usize {
        self.deque.len()
    }

    pub fn is_empty(&self) -> bool {
        self.deque.is_empty()
    }
}

pub struct WorkStealingScheduler {
    workers: Vec<WorkerQueue>,
    current_time: u32,
}

impl WorkStealingScheduler {
    pub fn new(num_workers: usize) -> Self {
        let mut workers = Vec::new();
        for i in 0..num_workers {
            workers.push(WorkerQueue::new(i));
        }

        Self {
            workers,
            current_time: 0,
        }
    }

    pub fn submit_task(&mut self, worker_id: usize, task: Task) {
        // TODO: Submit a task to a specific worker's queue
        todo!()
    }

    pub fn submit_tasks(&mut self, worker_id: usize, tasks: Vec<Task>) {
        for task in tasks {
            self.submit_task(worker_id, task);
        }
    }

    fn find_victim(&self, thief_id: usize) -> Option<usize> {
        // TODO: Find a worker to steal from
        // Strategy: Find the worker with the most tasks (excluding the thief)
        // Return None if no suitable victim is found
        todo!()
    }

    fn try_steal(&mut self, thief_id: usize) -> Option<Task> {
        // TODO: Try to steal a task for the given worker
        // 1. Find a victim using find_victim
        // 2. Steal from the victim's queue
        // 3. Update thief's stolen counter
        // 4. Return the stolen task
        todo!()
    }

    pub fn execute_step(&mut self, worker_id: usize) -> Option<usize> {
        // TODO: Execute one step for a worker
        // 1. Try to pop a task from worker's own queue
        // 2. If queue is empty, try to steal from another worker
        // 3. If got a task, "execute" it (update counters and time)
        // 4. Return the task ID that was executed (or None)
        todo!()
    }

    pub fn run_until_complete(&mut self) -> Vec<(usize, usize)> {
        // TODO: Run all workers until all tasks are complete
        // Use round-robin among workers
        // Return a vector of (worker_id, task_id) showing which worker executed which task
        todo!()
    }

    pub fn get_worker_stats(&self, worker_id: usize) -> WorkerStats {
        let worker = &self.workers[worker_id];
        WorkerStats {
            worker_id,
            tasks_completed: worker.tasks_completed,
            total_execution_time: worker.total_executed,
            tasks_stolen: worker.tasks_stolen,
            tasks_stolen_from_me: worker.tasks_stolen_from_me,
        }
    }

    pub fn is_complete(&self) -> bool {
        self.workers.iter().all(|w| w.is_empty())
    }

    pub fn current_time(&self) -> u32 {
        self.current_time
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct WorkerStats {
    pub worker_id: usize,
    pub tasks_completed: usize,
    pub total_execution_time: u32,
    pub tasks_stolen: usize,
    pub tasks_stolen_from_me: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_worker_single_task() {
        let mut scheduler = WorkStealingScheduler::new(1);
        scheduler.submit_task(0, Task::new(1, 10));

        let result = scheduler.execute_step(0);
        assert_eq!(result, Some(1));
        assert!(scheduler.is_complete());
    }

    #[test]
    fn test_lifo_local_execution() {
        let mut scheduler = WorkStealingScheduler::new(1);
        scheduler.submit_task(0, Task::new(1, 5));
        scheduler.submit_task(0, Task::new(2, 5));
        scheduler.submit_task(0, Task::new(3, 5));

        // Should execute in LIFO order (3, 2, 1)
        assert_eq!(scheduler.execute_step(0), Some(3));
        assert_eq!(scheduler.execute_step(0), Some(2));
        assert_eq!(scheduler.execute_step(0), Some(1));
    }

    #[test]
    fn test_work_stealing_basic() {
        let mut scheduler = WorkStealingScheduler::new(2);

        // Load all tasks on worker 0
        scheduler.submit_task(0, Task::new(1, 5));
        scheduler.submit_task(0, Task::new(2, 5));
        scheduler.submit_task(0, Task::new(3, 5));

        // Worker 1 should steal from worker 0
        let result = scheduler.execute_step(1);
        assert!(result.is_some());

        let stats = scheduler.get_worker_stats(1);
        assert_eq!(stats.tasks_stolen, 1);

        let stats = scheduler.get_worker_stats(0);
        assert_eq!(stats.tasks_stolen_from_me, 1);
    }

    #[test]
    fn test_fifo_stealing() {
        let mut scheduler = WorkStealingScheduler::new(2);

        // Add tasks to worker 0 in order: 1, 2, 3
        scheduler.submit_task(0, Task::new(1, 5));
        scheduler.submit_task(0, Task::new(2, 5));
        scheduler.submit_task(0, Task::new(3, 5));

        // Worker 1 steals - should get task 1 (FIFO)
        let stolen = scheduler.execute_step(1);
        assert_eq!(stolen, Some(1));

        // Worker 0 executes - should get task 3 (LIFO)
        let local = scheduler.execute_step(0);
        assert_eq!(local, Some(3));
    }

    #[test]
    fn test_load_balancing() {
        let mut scheduler = WorkStealingScheduler::new(3);

        // Give worker 0 many tasks
        for i in 0..10 {
            scheduler.submit_task(0, Task::new(i, 5));
        }

        scheduler.run_until_complete();

        // All workers should have done some work
        let stats0 = scheduler.get_worker_stats(0);
        let stats1 = scheduler.get_worker_stats(1);
        let stats2 = scheduler.get_worker_stats(2);

        assert!(stats0.tasks_completed > 0);
        assert!(stats1.tasks_completed > 0);
        assert!(stats2.tasks_completed > 0);

        // Total should be 10
        assert_eq!(stats0.tasks_completed + stats1.tasks_completed + stats2.tasks_completed, 10);
    }

    #[test]
    fn test_no_stealing_when_balanced() {
        let mut scheduler = WorkStealingScheduler::new(2);

        scheduler.submit_task(0, Task::new(1, 5));
        scheduler.submit_task(1, Task::new(2, 5));

        scheduler.run_until_complete();

        // No stealing should occur since work is balanced
        let stats0 = scheduler.get_worker_stats(0);
        let stats1 = scheduler.get_worker_stats(1);

        assert_eq!(stats0.tasks_stolen, 0);
        assert_eq!(stats1.tasks_stolen, 0);
    }

    #[test]
    fn test_steal_from_busiest() {
        let mut scheduler = WorkStealingScheduler::new(3);

        scheduler.submit_task(0, Task::new(1, 5));
        scheduler.submit_task(1, Task::new(2, 5));
        scheduler.submit_task(1, Task::new(3, 5));
        scheduler.submit_task(1, Task::new(4, 5));
        scheduler.submit_task(1, Task::new(5, 5));

        // Worker 2 should steal from worker 1 (busiest)
        scheduler.execute_step(2);

        let stats1 = scheduler.get_worker_stats(1);
        assert_eq!(stats1.tasks_stolen_from_me, 1);
    }

    #[test]
    fn test_execution_time_tracking() {
        let mut scheduler = WorkStealingScheduler::new(2);

        scheduler.submit_task(0, Task::new(1, 10));
        scheduler.submit_task(0, Task::new(2, 15));

        scheduler.run_until_complete();

        let total_time = scheduler.current_time();
        assert!(total_time >= 25); // At least the sum of execution times
    }
}
