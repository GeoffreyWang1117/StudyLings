// con05_cooperative_scheduling.rs
//
// Cooperative Scheduling (also called non-preemptive scheduling) relies on
// tasks voluntarily yielding control back to the scheduler. Tasks run until
// they explicitly yield or complete. This is simpler than preemptive scheduling
// but can lead to starvation if a task doesn't yield.
//
// Your task: Implement a cooperative scheduler where tasks must yield control.
//
// Key concepts:
// - Voluntary yielding: Tasks control when they give up CPU
// - No forced preemption: Scheduler cannot interrupt tasks
// - Simpler context switching: Only happens at yield points

// I AM NOT DONE

use std::collections::VecDeque;

#[derive(Debug, Clone, PartialEq)]
pub enum YieldReason {
    Voluntary,    // Task chose to yield
    IoWait,       // Task is waiting for I/O
    Completed,    // Task finished execution
}

#[derive(Debug, Clone)]
pub struct TaskAction {
    pub run_for: u32,      // Time units to run before action
    pub action: Action,     // What to do after running
}

#[derive(Debug, Clone, PartialEq)]
pub enum Action {
    Yield(YieldReason),
    Continue(u32),  // Continue for more time units
}

#[derive(Debug, Clone)]
pub struct Task {
    pub id: usize,
    pub actions: VecDeque<TaskAction>,
    pub total_execution_time: u32,
}

impl Task {
    pub fn new(id: usize, actions: Vec<TaskAction>) -> Self {
        let total_execution_time = actions.iter().map(|a| a.run_for).sum();
        Self {
            id,
            actions: actions.into_iter().collect(),
            total_execution_time,
        }
    }

    pub fn simple(id: usize, execution_time: u32, yield_interval: u32) -> Self {
        // TODO: Create a task that yields every yield_interval units
        // Hint: Calculate how many yields are needed and create TaskActions
        todo!()
    }

    pub fn is_complete(&self) -> bool {
        self.actions.is_empty()
    }

    pub fn next_action(&mut self) -> Option<TaskAction> {
        self.actions.pop_front()
    }
}

#[derive(Debug, Clone)]
pub struct SchedulerEvent {
    pub time: u32,
    pub task_id: usize,
    pub event: EventType,
}

#[derive(Debug, Clone, PartialEq)]
pub enum EventType {
    Started,
    Yielded(YieldReason),
    Resumed,
}

pub struct CooperativeScheduler {
    ready_queue: VecDeque<Task>,
    waiting_queue: VecDeque<(Task, u32)>, // (task, time_to_wait)
    current_time: u32,
    events: Vec<SchedulerEvent>,
}

impl CooperativeScheduler {
    pub fn new() -> Self {
        Self {
            ready_queue: VecDeque::new(),
            waiting_queue: VecDeque::new(),
            current_time: 0,
            events: Vec::new(),
        }
    }

    fn log_event(&mut self, task_id: usize, event: EventType) {
        self.events.push(SchedulerEvent {
            time: self.current_time,
            task_id,
            event,
        });
    }

    pub fn add_task(&mut self, task: Task) {
        // TODO: Add a task to the ready queue
        todo!()
    }

    fn update_waiting_tasks(&mut self) {
        // TODO: Check waiting tasks and move ready ones back to ready queue
        // Decrement wait time for all waiting tasks
        // Move tasks with wait_time == 0 back to ready queue
        todo!()
    }

    pub fn run_next(&mut self) -> Option<usize> {
        // TODO: Run the next task until it yields or completes
        // 1. Update waiting tasks
        // 2. Get next task from ready queue
        // 3. Log Started event
        // 4. Execute task actions until it yields or completes
        // 5. Handle the yield reason appropriately
        // 6. Return the task ID that ran (or None if no tasks)
        todo!()
    }

    pub fn run_all(&mut self) {
        // TODO: Run all tasks until completion
        while !self.is_idle() {
            self.run_next();
        }
    }

    pub fn is_idle(&self) -> bool {
        self.ready_queue.is_empty() && self.waiting_queue.is_empty()
    }

    pub fn current_time(&self) -> u32 {
        self.current_time
    }

    pub fn get_events(&self) -> &[SchedulerEvent] {
        &self.events
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_task_no_yield() {
        let mut scheduler = CooperativeScheduler::new();

        let task = Task::new(1, vec![
            TaskAction { run_for: 10, action: Action::Yield(YieldReason::Completed) },
        ]);

        scheduler.add_task(task);
        scheduler.run_all();

        assert_eq!(scheduler.current_time(), 10);
        assert!(scheduler.is_idle());
    }

    #[test]
    fn test_task_with_voluntary_yields() {
        let mut scheduler = CooperativeScheduler::new();

        let task = Task::new(1, vec![
            TaskAction { run_for: 3, action: Action::Yield(YieldReason::Voluntary) },
            TaskAction { run_for: 3, action: Action::Yield(YieldReason::Voluntary) },
            TaskAction { run_for: 4, action: Action::Yield(YieldReason::Completed) },
        ]);

        scheduler.add_task(task);
        scheduler.run_all();

        let events = scheduler.get_events();
        assert_eq!(events.iter().filter(|e| e.event == EventType::Yielded(YieldReason::Voluntary)).count(), 2);
        assert_eq!(scheduler.current_time(), 10);
    }

    #[test]
    fn test_multiple_tasks_round_robin() {
        let mut scheduler = CooperativeScheduler::new();

        scheduler.add_task(Task::simple(1, 10, 5));
        scheduler.add_task(Task::simple(2, 10, 5));

        scheduler.run_all();

        let events = scheduler.get_events();

        // Tasks should interleave
        let task1_events: Vec<_> = events.iter().filter(|e| e.task_id == 1).collect();
        let task2_events: Vec<_> = events.iter().filter(|e| e.task_id == 2).collect();

        assert!(task1_events.len() > 1);
        assert!(task2_events.len() > 1);
    }

    #[test]
    fn test_io_wait() {
        let mut scheduler = CooperativeScheduler::new();

        let task = Task::new(1, vec![
            TaskAction { run_for: 5, action: Action::Yield(YieldReason::IoWait) },
            TaskAction { run_for: 5, action: Action::Yield(YieldReason::Completed) },
        ]);

        scheduler.add_task(task);

        // Add another task to run while first is waiting
        scheduler.add_task(Task::simple(2, 8, 8));

        scheduler.run_all();

        let events = scheduler.get_events();
        assert!(events.iter().any(|e| e.task_id == 1 && e.event == EventType::Yielded(YieldReason::IoWait)));
        assert!(events.iter().any(|e| e.task_id == 2));
    }

    #[test]
    fn test_task_hogging_cpu() {
        let mut scheduler = CooperativeScheduler::new();

        // Task that never yields
        let selfish_task = Task::new(1, vec![
            TaskAction { run_for: 100, action: Action::Yield(YieldReason::Completed) },
        ]);

        scheduler.add_task(selfish_task);
        scheduler.add_task(Task::simple(2, 10, 5));

        // Run just the first task
        scheduler.run_next();

        // Task 2 should not have run yet (starvation)
        let events = scheduler.get_events();
        assert!(events.iter().all(|e| e.task_id == 1));
        assert_eq!(scheduler.current_time(), 100);
    }

    #[test]
    fn test_fair_yielding() {
        let mut scheduler = CooperativeScheduler::new();

        // Both tasks yield fairly
        scheduler.add_task(Task::simple(1, 20, 4));
        scheduler.add_task(Task::simple(2, 20, 4));

        scheduler.run_all();

        // Both should complete in reasonable time
        assert_eq!(scheduler.current_time(), 40);

        let events = scheduler.get_events();
        let task1_time: u32 = events.iter()
            .filter(|e| e.task_id == 1 && e.event == EventType::Started)
            .count() as u32;
        let task2_time: u32 = events.iter()
            .filter(|e| e.task_id == 2 && e.event == EventType::Started)
            .count() as u32;

        // Should get roughly equal scheduling opportunities
        assert!(task1_time > 0 && task2_time > 0);
    }

    #[test]
    fn test_complex_yield_pattern() {
        let mut scheduler = CooperativeScheduler::new();

        let task = Task::new(1, vec![
            TaskAction { run_for: 2, action: Action::Yield(YieldReason::Voluntary) },
            TaskAction { run_for: 3, action: Action::Yield(YieldReason::IoWait) },
            TaskAction { run_for: 1, action: Action::Yield(YieldReason::Voluntary) },
            TaskAction { run_for: 4, action: Action::Yield(YieldReason::Completed) },
        ]);

        scheduler.add_task(task);
        scheduler.run_all();

        let events = scheduler.get_events();
        assert_eq!(events.iter().filter(|e| matches!(e.event, EventType::Yielded(_))).count(), 4);
        assert_eq!(scheduler.current_time(), 10);
    }
}
