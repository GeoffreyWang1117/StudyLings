// gc06_incremental_gc.rs
//
// Incremental GC breaks up collection work into small increments
// to avoid long pause times. Based on tricolor marking.
//
// Your task: Implement an incremental garbage collector with configurable work units.

// I AM NOT DONE

use std::collections::{HashMap, HashSet, VecDeque};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(usize);

#[derive(Debug, Clone, Copy, PartialEq)]
enum Color {
    White,
    Gray,
    Black,
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum GCPhase {
    Idle,
    Marking,
    Sweeping,
}

pub struct IncrementalGC {
    objects: HashMap<ObjectId, (Color, Vec<ObjectId>)>,
    next_id: usize,
    roots: HashSet<ObjectId>,
    gray_queue: VecDeque<ObjectId>,
    phase: GCPhase,
    sweep_iterator: Vec<ObjectId>,
    sweep_index: usize,
}

impl IncrementalGC {
    pub fn new() -> Self {
        Self {
            objects: HashMap::new(),
            next_id: 0,
            roots: HashSet::new(),
            gray_queue: VecDeque::new(),
            phase: GCPhase::Idle,
            sweep_iterator: Vec::new(),
            sweep_index: 0,
        }
    }

    pub fn allocate(&mut self, references: Vec<ObjectId>) -> ObjectId {
        let id = ObjectId(self.next_id);
        self.next_id += 1;
        self.objects.insert(id, (Color::White, references));
        id
    }

    pub fn add_root(&mut self, id: ObjectId) {
        self.roots.insert(id);
    }

    pub fn start_collection(&mut self) {
        // TODO: Start a new collection cycle
        // Initialize tricolor marking
        todo!()
    }

    pub fn incremental_step(&mut self, work_units: usize) {
        // TODO: Perform one incremental step based on current phase
        // In Marking phase: mark 'work_units' objects
        // In Sweeping phase: sweep 'work_units' objects
        // Transition between phases as needed
        todo!()
    }

    fn mark_work(&mut self, units: usize) -> bool {
        // TODO: Do 'units' amount of marking work
        // Return true if marking phase complete
        todo!()
    }

    fn sweep_work(&mut self, units: usize) -> bool {
        // TODO: Do 'units' amount of sweeping work
        // Return true if sweeping phase complete
        todo!()
    }

    pub fn get_phase(&self) -> &str {
        match self.phase {
            GCPhase::Idle => "Idle",
            GCPhase::Marking => "Marking",
            GCPhase::Sweeping => "Sweeping",
        }
    }

    pub fn object_count(&self) -> usize {
        self.objects.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_incremental_collection() {
        let mut gc = IncrementalGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![]);

        gc.add_root(obj1);

        gc.start_collection();
        assert_eq!(gc.get_phase(), "Marking");

        // Run incremental steps
        for _ in 0..10 {
            gc.incremental_step(1);
        }

        assert_eq!(gc.get_phase(), "Idle");
        assert_eq!(gc.object_count(), 1);
    }

    #[test]
    fn test_multiple_incremental_cycles() {
        let mut gc = IncrementalGC::new();

        let obj1 = gc.allocate(vec![]);
        gc.add_root(obj1);

        gc.start_collection();
        while gc.get_phase() != "Idle" {
            gc.incremental_step(1);
        }

        assert_eq!(gc.object_count(), 1);

        let _obj2 = gc.allocate(vec![]);

        gc.start_collection();
        while gc.get_phase() != "Idle" {
            gc.incremental_step(1);
        }

        assert_eq!(gc.object_count(), 1);
    }
}
