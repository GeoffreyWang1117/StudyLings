// gc07_concurrent_gc.rs
//
// Concurrent GC runs the collector concurrently with the mutator (application).
// This requires synchronization and write barriers to maintain correctness.
//
// Your task: Implement a simplified concurrent GC with basic write barrier.

// I AM NOT DONE

use std::collections::{HashMap, HashSet};
use std::sync::{Arc, Mutex};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(usize);

#[derive(Debug, Clone)]
struct Object {
    references: Vec<ObjectId>,
    marked: bool,
}

#[derive(Clone)]
pub struct ConcurrentGC {
    objects: Arc<Mutex<HashMap<ObjectId, Object>>>,
    next_id: Arc<Mutex<usize>>,
    roots: Arc<Mutex<HashSet<ObjectId>>>,
    write_barrier_log: Arc<Mutex<Vec<(ObjectId, ObjectId)>>>,
}

impl ConcurrentGC {
    pub fn new() -> Self {
        Self {
            objects: Arc::new(Mutex::new(HashMap::new())),
            next_id: Arc::new(Mutex::new(0)),
            roots: Arc::new(Mutex::new(HashSet::new())),
            write_barrier_log: Arc::new(Mutex::new(Vec::new())),
        }
    }

    pub fn allocate(&self, references: Vec<ObjectId>) -> ObjectId {
        let mut next_id = self.next_id.lock().unwrap();
        let id = ObjectId(*next_id);
        *next_id += 1;

        let obj = Object {
            references,
            marked: false,
        };

        let mut objects = self.objects.lock().unwrap();
        objects.insert(id, obj);
        id
    }

    pub fn add_root(&self, id: ObjectId) {
        let mut roots = self.roots.lock().unwrap();
        roots.insert(id);
    }

    pub fn write_barrier(&self, from: ObjectId, to: ObjectId) {
        // TODO: Implement write barrier
        // Log pointer writes during concurrent marking
        // This ensures we don't miss references created during GC
        todo!()
    }

    pub fn update_reference(&self, from: ObjectId, index: usize, to: ObjectId) {
        // TODO: Update a reference with write barrier
        // 1. Call write barrier
        // 2. Update the actual reference
        todo!()
    }

    fn mark(&self, id: ObjectId, marked: &mut HashSet<ObjectId>) {
        if marked.contains(&id) {
            return;
        }
        marked.insert(id);

        let objects = self.objects.lock().unwrap();
        if let Some(obj) = objects.get(&id) {
            let refs = obj.references.clone();
            drop(objects);

            for &ref_id in &refs {
                self.mark(ref_id, marked);
            }
        }
    }

    pub fn concurrent_collect(&self) {
        // TODO: Implement concurrent collection
        // 1. Mark from roots
        // 2. Process write barrier log
        // 3. Sweep unmarked objects
        todo!()
    }

    pub fn object_count(&self) -> usize {
        let objects = self.objects.lock().unwrap();
        objects.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;

    #[test]
    fn test_concurrent_allocation() {
        let gc = ConcurrentGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![obj1]);

        gc.add_root(obj2);

        gc.concurrent_collect();

        assert_eq!(gc.object_count(), 2);
    }

    #[test]
    fn test_write_barrier() {
        let gc = ConcurrentGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![]);

        gc.add_root(obj1);

        gc.update_reference(obj1, 0, obj2);

        gc.concurrent_collect();

        assert_eq!(gc.object_count(), 2);
    }

    #[test]
    fn test_concurrent_threads() {
        let gc = ConcurrentGC::new();

        let obj1 = gc.allocate(vec![]);
        gc.add_root(obj1);

        let gc_clone = gc.clone();
        let handle = thread::spawn(move || {
            gc_clone.concurrent_collect();
        });

        // Allocate while GC runs
        let _obj2 = gc.allocate(vec![]);

        handle.join().unwrap();

        assert!(gc.object_count() >= 1);
    }
}
