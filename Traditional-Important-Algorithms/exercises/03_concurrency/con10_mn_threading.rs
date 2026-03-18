// con10_mn_threading.rs
//
// M:N Threading (also called hybrid threading) maps M user-level threads to
// N kernel threads. This combines the efficiency of user-level threads with
// the parallelism of kernel threads. The scheduler multiplexes many lightweight
// threads onto fewer OS threads.
//
// Your task: Implement an M:N thread scheduler.
//
// Key concepts:
// - User threads: Lightweight, managed by the runtime
// - Kernel threads (workers): Heavy, managed by the OS
// - Multiplexing: Many user threads share kernel threads
// - Work stealing: Balance load across kernel threads

// I AM NOT DONE

use std::collections::VecDeque;

pub type ThreadId = usize;
pub type WorkerId = usize;

#[derive(Debug, Clone, PartialEq)]
pub enum ThreadState {
    Ready,
    Running,
    Blocked,
    Completed,
}

#[derive(Debug, Clone)]
pub struct UserThread {
    pub id: ThreadId,
    pub state: ThreadState,
    pub remaining_work: u32,
    pub assigned_worker: Option<WorkerId>,
}

impl UserThread {
    pub fn new(id: ThreadId, work_amount: u32) -> Self {
        Self {
            id,
            state: ThreadState::Ready,
            remaining_work: work_amount,
            assigned_worker: None,
        }
    }

    pub fn is_complete(&self) -> bool {
        self.state == ThreadState::Completed
    }
}

#[derive(Debug)]
pub struct Worker {
    pub id: WorkerId,
    local_queue: VecDeque<ThreadId>,
    current_thread: Option<ThreadId>,
    total_execution_time: u32,
    threads_completed: usize,
}

impl Worker {
    pub fn new(id: WorkerId) -> Self {
        Self {
            id,
            local_queue: VecDeque::new(),
            current_thread: None,
            total_execution_time: 0,
            threads_completed: 0,
        }
    }

    pub fn enqueue(&mut self, thread_id: ThreadId) {
        // TODO: Add a thread to this worker's local queue
        todo!()
    }

    pub fn dequeue(&mut self) -> Option<ThreadId> {
        // TODO: Remove and return a thread from the local queue (LIFO)
        todo!()
    }

    pub fn steal(&mut self) -> Option<ThreadId> {
        // TODO: Steal a thread from the front of the queue (FIFO)
        todo!()
    }

    pub fn queue_len(&self) -> usize {
        self.local_queue.len()
    }

    pub fn is_idle(&self) -> bool {
        self.current_thread.is_none() && self.local_queue.is_empty()
    }
}

#[derive(Debug, Clone)]
pub struct SchedulerEvent {
    pub time: u32,
    pub event_type: EventType,
}

#[derive(Debug, Clone, PartialEq)]
pub enum EventType {
    ThreadStarted(ThreadId, WorkerId),
    ThreadCompleted(ThreadId, WorkerId),
    ThreadBlocked(ThreadId, WorkerId),
    ThreadResumed(ThreadId, WorkerId),
    ThreadStolen(ThreadId, WorkerId, WorkerId), // (thread, from_worker, to_worker)
}

pub struct MNScheduler {
    threads: Vec<UserThread>,
    workers: Vec<Worker>,
    global_queue: VecDeque<ThreadId>,
    quantum: u32,
    current_time: u32,
    events: Vec<SchedulerEvent>,
}

impl MNScheduler {
    pub fn new(num_workers: usize, quantum: u32) -> Self {
        let mut workers = Vec::new();
        for i in 0..num_workers {
            workers.push(Worker::new(i));
        }

        Self {
            threads: Vec::new(),
            workers,
            global_queue: VecDeque::new(),
            quantum,
            current_time: 0,
            events: Vec::new(),
        }
    }

    pub fn spawn_thread(&mut self, work_amount: u32) -> ThreadId {
        // TODO: Create a new user thread
        // 1. Create thread with unique ID
        // 2. Add to threads vector
        // 3. Add to global queue
        // 4. Return thread ID
        todo!()
    }

    fn log_event(&mut self, event_type: EventType) {
        self.events.push(SchedulerEvent {
            time: self.current_time,
            event_type,
        });
    }

    fn find_steal_victim(&self, thief_id: WorkerId) -> Option<WorkerId> {
        // TODO: Find the best worker to steal from
        // Choose the worker with the most queued threads (excluding thief)
        todo!()
    }

    fn try_steal(&mut self, thief_id: WorkerId) -> Option<ThreadId> {
        // TODO: Try to steal work for a worker
        // 1. Find a victim worker
        // 2. Steal a thread from the victim
        // 3. Log the theft event
        // 4. Return the stolen thread ID
        todo!()
    }

    fn assign_work(&mut self, worker_id: WorkerId) -> Option<ThreadId> {
        // TODO: Assign work to a worker
        // Try in order:
        // 1. Worker's local queue
        // 2. Global queue
        // 3. Steal from another worker
        todo!()
    }

    pub fn execute_step(&mut self, worker_id: WorkerId) -> bool {
        // TODO: Execute one step for a worker
        // 1. If worker has no current thread, assign work
        // 2. If still no thread, return false (idle)
        // 3. Execute current thread for min(quantum, remaining_work)
        // 4. Update thread state and time
        // 5. Log events
        // 6. If thread completes or blocks, clear current_thread
        // 7. Return true if work was done
        todo!()
    }

    pub fn run_all(&mut self) {
        // TODO: Run all workers until all threads complete
        // Use round-robin scheduling among workers
        loop {
            let mut any_work = false;
            for worker_id in 0..self.workers.len() {
                if self.execute_step(worker_id) {
                    any_work = true;
                }
            }
            if !any_work {
                break;
            }
        }
    }

    pub fn get_thread(&self, id: ThreadId) -> Option<&UserThread> {
        self.threads.iter().find(|t| t.id == id)
    }

    pub fn get_worker_stats(&self, worker_id: WorkerId) -> WorkerStats {
        let worker = &self.workers[worker_id];
        WorkerStats {
            worker_id,
            threads_completed: worker.threads_completed,
            total_execution_time: worker.total_execution_time,
            current_queue_length: worker.queue_len(),
        }
    }

    pub fn current_time(&self) -> u32 {
        self.current_time
    }

    pub fn get_events(&self) -> &[SchedulerEvent] {
        &self.events
    }

    pub fn all_complete(&self) -> bool {
        self.threads.iter().all(|t| t.is_complete())
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct WorkerStats {
    pub worker_id: WorkerId,
    pub threads_completed: usize,
    pub total_execution_time: u32,
    pub current_queue_length: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_worker_single_thread() {
        let mut scheduler = MNScheduler::new(1, 10);
        scheduler.spawn_thread(20);

        scheduler.run_all();

        assert!(scheduler.all_complete());
        let stats = scheduler.get_worker_stats(0);
        assert_eq!(stats.threads_completed, 1);
    }

    #[test]
    fn test_multiple_threads_single_worker() {
        let mut scheduler = MNScheduler::new(1, 5);
        scheduler.spawn_thread(10);
        scheduler.spawn_thread(10);
        scheduler.spawn_thread(10);

        scheduler.run_all();

        assert!(scheduler.all_complete());
        let stats = scheduler.get_worker_stats(0);
        assert_eq!(stats.threads_completed, 3);
    }

    #[test]
    fn test_multiple_workers_load_balancing() {
        let mut scheduler = MNScheduler::new(3, 10);

        // Spawn many threads
        for _ in 0..9 {
            scheduler.spawn_thread(10);
        }

        scheduler.run_all();

        assert!(scheduler.all_complete());

        // Work should be distributed across workers
        let stats0 = scheduler.get_worker_stats(0);
        let stats1 = scheduler.get_worker_stats(1);
        let stats2 = scheduler.get_worker_stats(2);

        assert!(stats0.threads_completed > 0);
        assert!(stats1.threads_completed > 0);
        assert!(stats2.threads_completed > 0);

        assert_eq!(
            stats0.threads_completed + stats1.threads_completed + stats2.threads_completed,
            9
        );
    }

    #[test]
    fn test_work_stealing() {
        let mut scheduler = MNScheduler::new(2, 5);

        // Add all work to worker 0's queue
        for i in 0..6 {
            let thread_id = scheduler.spawn_thread(10);
            // Manually assign to worker 0
            scheduler.workers[0].enqueue(thread_id);
        }
        scheduler.global_queue.clear(); // Clear global queue

        scheduler.run_all();

        // Worker 1 should have stolen work
        let events = scheduler.get_events();
        let steals: Vec<_> = events
            .iter()
            .filter(|e| matches!(e.event_type, EventType::ThreadStolen(_, _, _)))
            .collect();

        assert!(!steals.is_empty(), "Work stealing should have occurred");
    }

    #[test]
    fn test_quantum_enforcement() {
        let mut scheduler = MNScheduler::new(1, 5);
        scheduler.spawn_thread(20);

        // Execute one step
        scheduler.execute_step(0);

        let thread = scheduler.get_thread(0).unwrap();
        // Should have executed for quantum (5) time units
        assert_eq!(thread.remaining_work, 15);
    }

    #[test]
    fn test_thread_completion() {
        let mut scheduler = MNScheduler::new(1, 10);
        let thread_id = scheduler.spawn_thread(5);

        scheduler.run_all();

        let thread = scheduler.get_thread(thread_id).unwrap();
        assert_eq!(thread.state, ThreadState::Completed);
        assert_eq!(thread.remaining_work, 0);
    }

    #[test]
    fn test_event_logging() {
        let mut scheduler = MNScheduler::new(1, 10);
        scheduler.spawn_thread(5);

        scheduler.run_all();

        let events = scheduler.get_events();
        assert!(events
            .iter()
            .any(|e| matches!(e.event_type, EventType::ThreadStarted(_, _))));
        assert!(events
            .iter()
            .any(|e| matches!(e.event_type, EventType::ThreadCompleted(_, _))));
    }

    #[test]
    fn test_worker_utilization() {
        let mut scheduler = MNScheduler::new(2, 10);

        for _ in 0..4 {
            scheduler.spawn_thread(20);
        }

        scheduler.run_all();

        let stats0 = scheduler.get_worker_stats(0);
        let stats1 = scheduler.get_worker_stats(1);

        // Both workers should have done work
        assert!(stats0.total_execution_time > 0);
        assert!(stats1.total_execution_time > 0);
    }

    #[test]
    fn test_varying_work_amounts() {
        let mut scheduler = MNScheduler::new(2, 10);

        scheduler.spawn_thread(5);
        scheduler.spawn_thread(50);
        scheduler.spawn_thread(15);
        scheduler.spawn_thread(30);

        scheduler.run_all();

        assert!(scheduler.all_complete());

        let total_completed = scheduler
            .workers
            .iter()
            .map(|w| w.threads_completed)
            .sum::<usize>();

        assert_eq!(total_completed, 4);
    }

    #[test]
    fn test_empty_scheduler() {
        let mut scheduler = MNScheduler::new(2, 10);

        scheduler.run_all();

        assert!(scheduler.all_complete());
        assert_eq!(scheduler.current_time(), 0);
    }
}
