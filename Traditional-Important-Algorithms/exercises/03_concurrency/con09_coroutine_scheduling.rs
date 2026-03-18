// con09_coroutine_scheduling.rs
//
// Coroutines are functions that can suspend execution and resume later,
// allowing for cooperative multitasking. A coroutine scheduler manages
// multiple coroutines, switching between them when they yield.
//
// Your task: Implement a coroutine scheduler that can suspend and resume
// coroutine execution.
//
// Key concepts:
// - Yield points: Where coroutines can suspend
// - Resumption: Continuing from where a coroutine left off
// - Cooperative scheduling: Coroutines control when they yield
// - State preservation: Maintaining coroutine state across yields

// I AM NOT DONE

use std::collections::VecDeque;

pub type CoroutineId = usize;

#[derive(Debug, Clone, PartialEq)]
pub enum YieldType {
    Yield,          // Simple yield to scheduler
    YieldValue(i32), // Yield with a value
    Await(CoroutineId), // Wait for another coroutine to complete
}

#[derive(Debug, Clone, PartialEq)]
pub enum CoroutineState {
    Ready,
    Running,
    Suspended(YieldType),
    Completed(Option<i32>),
}

#[derive(Debug, Clone)]
pub struct Instruction {
    pub execute_for: u32,  // Time units to execute
    pub then: Action,       // What to do after execution
}

#[derive(Debug, Clone)]
pub enum Action {
    Yield(YieldType),
    Return(i32),
}

pub struct Coroutine {
    pub id: CoroutineId,
    pub state: CoroutineState,
    instructions: VecDeque<Instruction>,
    execution_time: u32,
}

impl Coroutine {
    pub fn new(id: CoroutineId, instructions: Vec<Instruction>) -> Self {
        Self {
            id,
            state: CoroutineState::Ready,
            instructions: instructions.into_iter().collect(),
            execution_time: 0,
        }
    }

    pub fn simple_yielding(id: CoroutineId, total_time: u32, yield_interval: u32) -> Self {
        // TODO: Create a coroutine that yields every yield_interval units
        // and completes after total_time units
        todo!()
    }

    pub fn is_complete(&self) -> bool {
        matches!(self.state, CoroutineState::Completed(_))
    }

    pub fn can_run(&self) -> bool {
        matches!(self.state, CoroutineState::Ready)
    }
}

#[derive(Debug, Clone)]
pub struct SchedulerEvent {
    pub time: u32,
    pub coroutine_id: CoroutineId,
    pub event: EventType,
}

#[derive(Debug, Clone, PartialEq)]
pub enum EventType {
    Started,
    Resumed,
    Yielded(YieldType),
    Completed(Option<i32>),
}

pub struct CoroutineScheduler {
    coroutines: Vec<Coroutine>,
    ready_queue: VecDeque<CoroutineId>,
    waiting: Vec<(CoroutineId, CoroutineId)>, // (waiting_id, waiting_for_id)
    current_time: u32,
    events: Vec<SchedulerEvent>,
}

impl CoroutineScheduler {
    pub fn new() -> Self {
        Self {
            coroutines: Vec::new(),
            ready_queue: VecDeque::new(),
            waiting: Vec::new(),
            current_time: 0,
            events: Vec::new(),
        }
    }

    pub fn spawn(&mut self, coroutine: Coroutine) -> CoroutineId {
        // TODO: Add a coroutine to the scheduler
        // 1. Add to coroutines vector
        // 2. Add to ready queue
        // 3. Return its ID
        todo!()
    }

    fn log_event(&mut self, coroutine_id: CoroutineId, event: EventType) {
        self.events.push(SchedulerEvent {
            time: self.current_time,
            coroutine_id,
            event,
        });
    }

    fn resume_waiting_coroutines(&mut self, completed_id: CoroutineId) {
        // TODO: Resume coroutines that were waiting for the completed coroutine
        // 1. Find all coroutines waiting for completed_id
        // 2. Move them back to ready queue
        // 3. Update their state to Ready
        // 4. Remove them from waiting list
        todo!()
    }

    pub fn run_next(&mut self) -> Option<CoroutineId> {
        // TODO: Run the next ready coroutine until it yields or completes
        // 1. Get next coroutine from ready queue
        // 2. Update its state to Running
        // 3. Execute its next instruction
        // 4. Handle the action (Yield or Return)
        // 5. Update current_time
        // 6. Log appropriate events
        // 7. Return the coroutine ID that ran
        todo!()
    }

    pub fn run_all(&mut self) {
        // TODO: Run all coroutines until completion
        while !self.ready_queue.is_empty() || !self.waiting.is_empty() {
            if self.ready_queue.is_empty() {
                // Deadlock detection: if waiting list is not empty but ready queue is,
                // we have a deadlock
                if !self.waiting.is_empty() {
                    break;
                }
            }
            self.run_next();
        }
    }

    pub fn get_coroutine(&self, id: CoroutineId) -> Option<&Coroutine> {
        self.coroutines.iter().find(|c| c.id == id)
    }

    pub fn current_time(&self) -> u32 {
        self.current_time
    }

    pub fn get_events(&self) -> &[SchedulerEvent] {
        &self.events
    }

    pub fn all_complete(&self) -> bool {
        self.coroutines.iter().all(|c| c.is_complete())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_coroutine_no_yield() {
        let mut scheduler = CoroutineScheduler::new();

        let coroutine = Coroutine::new(
            0,
            vec![Instruction {
                execute_for: 10,
                then: Action::Return(42),
            }],
        );

        scheduler.spawn(coroutine);
        scheduler.run_all();

        let coro = scheduler.get_coroutine(0).unwrap();
        assert_eq!(coro.state, CoroutineState::Completed(Some(42)));
        assert_eq!(scheduler.current_time(), 10);
    }

    #[test]
    fn test_coroutine_with_yields() {
        let mut scheduler = CoroutineScheduler::new();

        let coroutine = Coroutine::new(
            0,
            vec![
                Instruction {
                    execute_for: 5,
                    then: Action::Yield(YieldType::Yield),
                },
                Instruction {
                    execute_for: 5,
                    then: Action::Return(100),
                },
            ],
        );

        scheduler.spawn(coroutine);
        scheduler.run_all();

        let events = scheduler.get_events();
        assert!(events.iter().any(|e| e.event == EventType::Yielded(YieldType::Yield)));
        assert!(events.iter().any(|e| e.event == EventType::Completed(Some(100))));
    }

    #[test]
    fn test_multiple_coroutines() {
        let mut scheduler = CoroutineScheduler::new();

        scheduler.spawn(Coroutine::simple_yielding(0, 10, 5));
        scheduler.spawn(Coroutine::simple_yielding(1, 10, 5));

        scheduler.run_all();

        assert!(scheduler.all_complete());

        // Both should have run
        let events = scheduler.get_events();
        assert!(events.iter().any(|e| e.coroutine_id == 0));
        assert!(events.iter().any(|e| e.coroutine_id == 1));
    }

    #[test]
    fn test_round_robin_execution() {
        let mut scheduler = CoroutineScheduler::new();

        scheduler.spawn(Coroutine::simple_yielding(0, 15, 5));
        scheduler.spawn(Coroutine::simple_yielding(1, 15, 5));

        scheduler.run_all();

        let events = scheduler.get_events();

        // Events should alternate between coroutines
        let mut last_id = None;
        let mut switches = 0;

        for event in events {
            if matches!(event.event, EventType::Started | EventType::Resumed) {
                if let Some(last) = last_id {
                    if last != event.coroutine_id {
                        switches += 1;
                    }
                }
                last_id = Some(event.coroutine_id);
            }
        }

        assert!(switches > 0, "Coroutines should interleave execution");
    }

    #[test]
    fn test_yield_value() {
        let mut scheduler = CoroutineScheduler::new();

        let coroutine = Coroutine::new(
            0,
            vec![
                Instruction {
                    execute_for: 3,
                    then: Action::Yield(YieldType::YieldValue(42)),
                },
                Instruction {
                    execute_for: 3,
                    then: Action::Return(100),
                },
            ],
        );

        scheduler.spawn(coroutine);
        scheduler.run_all();

        let events = scheduler.get_events();
        assert!(events.iter().any(|e| e.event == EventType::Yielded(YieldType::YieldValue(42))));
    }

    #[test]
    fn test_await_coroutine() {
        let mut scheduler = CoroutineScheduler::new();

        let coroutine1 = Coroutine::new(
            0,
            vec![Instruction {
                execute_for: 10,
                then: Action::Return(42),
            }],
        );

        let coroutine2 = Coroutine::new(
            1,
            vec![
                Instruction {
                    execute_for: 5,
                    then: Action::Yield(YieldType::Await(0)),
                },
                Instruction {
                    execute_for: 5,
                    then: Action::Return(100),
                },
            ],
        );

        scheduler.spawn(coroutine1);
        scheduler.spawn(coroutine2);
        scheduler.run_all();

        // Both should complete
        assert!(scheduler.all_complete());

        let events = scheduler.get_events();
        // Coroutine 1 should complete before coroutine 2 resumes
        let coro1_complete_time = events
            .iter()
            .find(|e| e.coroutine_id == 0 && matches!(e.event, EventType::Completed(_)))
            .map(|e| e.time);

        let coro2_resume_time = events
            .iter()
            .filter(|e| e.coroutine_id == 1 && e.event == EventType::Resumed)
            .map(|e| e.time)
            .next();

        if let (Some(complete), Some(resume)) = (coro1_complete_time, coro2_resume_time) {
            assert!(complete <= resume, "Coroutine 2 should resume after coroutine 1 completes");
        }
    }

    #[test]
    fn test_immediate_completion() {
        let mut scheduler = CoroutineScheduler::new();

        let coroutine = Coroutine::new(
            0,
            vec![Instruction {
                execute_for: 0,
                then: Action::Return(1),
            }],
        );

        scheduler.spawn(coroutine);
        scheduler.run_all();

        assert!(scheduler.all_complete());
        assert_eq!(scheduler.current_time(), 0);
    }

    #[test]
    fn test_multiple_yields() {
        let mut scheduler = CoroutineScheduler::new();

        let coroutine = Coroutine::new(
            0,
            vec![
                Instruction {
                    execute_for: 1,
                    then: Action::Yield(YieldType::Yield),
                },
                Instruction {
                    execute_for: 1,
                    then: Action::Yield(YieldType::Yield),
                },
                Instruction {
                    execute_for: 1,
                    then: Action::Yield(YieldType::Yield),
                },
                Instruction {
                    execute_for: 1,
                    then: Action::Return(0),
                },
            ],
        );

        scheduler.spawn(coroutine);
        scheduler.run_all();

        let events = scheduler.get_events();
        let yield_count = events
            .iter()
            .filter(|e| matches!(e.event, EventType::Yielded(_)))
            .count();

        assert_eq!(yield_count, 3);
    }
}
