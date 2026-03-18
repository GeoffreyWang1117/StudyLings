// gc05_tricolor_marking.rs
//
// Tricolor marking is an algorithm for incremental/concurrent GC.
// Objects are classified into three colors:
// - White: Not yet visited (potentially garbage)
// - Gray: Visited but not scanned (work queue)
// - Black: Visited and scanned (definitely live)
//
// Your task: Implement tricolor marking for incremental collection.

// I AM NOT DONE

use std::collections::{HashMap, HashSet, VecDeque};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(usize);

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Color {
    White,
    Gray,
    Black,
}

#[derive(Debug)]
pub struct Object {
    id: ObjectId,
    color: Color,
    references: Vec<ObjectId>,
}

pub struct TricolorGC {
    objects: HashMap<ObjectId, Object>,
    next_id: usize,
    roots: HashSet<ObjectId>,
    gray_queue: VecDeque<ObjectId>,
}

impl TricolorGC {
    pub fn new() -> Self {
        Self {
            objects: HashMap::new(),
            next_id: 0,
            roots: HashSet::new(),
            gray_queue: VecDeque::new(),
        }
    }

    pub fn allocate(&mut self, references: Vec<ObjectId>) -> ObjectId {
        let id = ObjectId(self.next_id);
        self.next_id += 1;

        let obj = Object {
            id,
            color: Color::White,
            references,
        };

        self.objects.insert(id, obj);
        id
    }

    pub fn add_root(&mut self, id: ObjectId) {
        self.roots.insert(id);
    }

    pub fn init_collection(&mut self) {
        // TODO: Initialize a collection cycle
        // 1. Set all objects to white
        // 2. Clear gray queue
        // 3. Mark roots as gray and add to queue
        todo!()
    }

    pub fn mark_step(&mut self, steps: usize) -> bool {
        // TODO: Perform 'steps' marking steps
        // For each step:
        // 1. Pop an object from gray queue
        // 2. Mark it black
        // 3. Mark all its white references as gray and add to queue
        // Return true if marking is complete (gray queue empty)
        todo!()
    }

    pub fn sweep(&mut self) {
        // TODO: Remove all white objects
        todo!()
    }

    pub fn incremental_collect(&mut self, steps_per_round: usize) {
        // TODO: Run a complete incremental collection
        // 1. Initialize
        // 2. Keep calling mark_step until complete
        // 3. Sweep
        todo!()
    }

    pub fn object_count(&self) -> usize {
        self.objects.len()
    }

    pub fn get_color(&self, id: ObjectId) -> Option<Color> {
        self.objects.get(&id).map(|obj| obj.color)
    }

    pub fn white_count(&self) -> usize {
        self.objects
            .values()
            .filter(|obj| obj.color == Color::White)
            .count()
    }

    pub fn gray_count(&self) -> usize {
        self.objects
            .values()
            .filter(|obj| obj.color == Color::Gray)
            .count()
    }

    pub fn black_count(&self) -> usize {
        self.objects
            .values()
            .filter(|obj| obj.color == Color::Black)
            .count()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tricolor_marking() {
        let mut gc = TricolorGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![obj1]);
        let obj3 = gc.allocate(vec![]);

        gc.add_root(obj2);

        gc.init_collection();

        // Root should be gray
        assert_eq!(gc.get_color(obj2), Some(Color::Gray));

        // Mark all
        while !gc.mark_step(1) {}

        // obj1 and obj2 should be black, obj3 white
        assert_eq!(gc.get_color(obj1), Some(Color::Black));
        assert_eq!(gc.get_color(obj2), Some(Color::Black));
        assert_eq!(gc.get_color(obj3), Some(Color::White));

        gc.sweep();

        assert_eq!(gc.object_count(), 2);
    }

    #[test]
    fn test_incremental_steps() {
        let mut gc = TricolorGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![obj1]);

        gc.add_root(obj2);

        gc.init_collection();

        // First step: mark root
        assert_eq!(gc.mark_step(1), false);
        assert_eq!(gc.black_count(), 1);

        // Second step: mark referenced object
        assert_eq!(gc.mark_step(1), true);
        assert_eq!(gc.black_count(), 2);
    }
}
