// gc02_mark_sweep.rs
//
// Mark-Sweep is a classic garbage collection algorithm with two phases:
// 1. Mark: Starting from root objects, traverse and mark all reachable objects
// 2. Sweep: Free all unmarked objects
//
// Your task: Implement a simple mark-sweep garbage collector.

// I AM NOT DONE

use std::collections::{HashSet, HashMap};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(usize);

#[derive(Debug)]
pub struct Object {
    id: ObjectId,
    marked: bool,
    // References to other objects
    references: Vec<ObjectId>,
}

pub struct MarkSweepGC {
    objects: HashMap<ObjectId, Object>,
    next_id: usize,
    roots: HashSet<ObjectId>,
}

impl MarkSweepGC {
    pub fn new() -> Self {
        Self {
            objects: HashMap::new(),
            next_id: 0,
            roots: HashSet::new(),
        }
    }

    pub fn allocate(&mut self, references: Vec<ObjectId>) -> ObjectId {
        let id = ObjectId(self.next_id);
        self.next_id += 1;

        let obj = Object {
            id,
            marked: false,
            references,
        };

        self.objects.insert(id, obj);
        id
    }

    pub fn add_root(&mut self, id: ObjectId) {
        self.roots.insert(id);
    }

    pub fn remove_root(&mut self, id: ObjectId) {
        self.roots.remove(&id);
    }

    fn mark(&mut self, id: ObjectId) {
        // TODO: Implement the mark phase
        // 1. If object is already marked, return
        // 2. Mark this object
        // 3. Recursively mark all objects this one references
        todo!()
    }

    fn mark_all_roots(&mut self) {
        // TODO: Mark all objects reachable from roots
        // Hint: Clone the roots set first to avoid borrow checker issues
        todo!()
    }

    fn sweep(&mut self) {
        // TODO: Implement the sweep phase
        // Remove all unmarked objects from the objects HashMap
        // Reset the marked flag on remaining objects
        todo!()
    }

    pub fn collect(&mut self) {
        // TODO: Run a full mark-sweep collection cycle
        // 1. Mark all reachable objects
        // 2. Sweep unmarked objects
        todo!()
    }

    pub fn object_count(&self) -> usize {
        self.objects.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_collection() {
        let mut gc = MarkSweepGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![]);

        gc.add_root(obj1);

        assert_eq!(gc.object_count(), 2);

        gc.collect();

        // obj2 should be collected, obj1 should remain
        assert_eq!(gc.object_count(), 1);
    }

    #[test]
    fn test_transitive_reachability() {
        let mut gc = MarkSweepGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![obj1]);
        let obj3 = gc.allocate(vec![obj2]);
        let obj4 = gc.allocate(vec![]);

        gc.add_root(obj3);

        assert_eq!(gc.object_count(), 4);

        gc.collect();

        // obj1, obj2, obj3 are reachable; obj4 is not
        assert_eq!(gc.object_count(), 3);
    }

    #[test]
    fn test_no_roots() {
        let mut gc = MarkSweepGC::new();

        gc.allocate(vec![]);
        gc.allocate(vec![]);
        gc.allocate(vec![]);

        assert_eq!(gc.object_count(), 3);

        gc.collect();

        // All should be collected
        assert_eq!(gc.object_count(), 0);
    }
}
