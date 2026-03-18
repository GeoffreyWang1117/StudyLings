// gc04_generational_gc.rs
//
// Generational GC is based on the observation that most objects die young.
// Objects are separated into generations (young, old) and young generation
// is collected more frequently.
//
// Your task: Implement a simple two-generation garbage collector.

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(usize);

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Generation {
    Young,
    Old,
}

#[derive(Debug)]
pub struct Object {
    id: ObjectId,
    generation: Generation,
    age: usize,
    references: Vec<ObjectId>,
}

pub struct GenerationalGC {
    objects: HashMap<ObjectId, Object>,
    next_id: usize,
    roots: HashSet<ObjectId>,
    promotion_threshold: usize,
}

impl GenerationalGC {
    pub fn new(promotion_threshold: usize) -> Self {
        Self {
            objects: HashMap::new(),
            next_id: 0,
            roots: HashSet::new(),
            promotion_threshold,
        }
    }

    pub fn allocate(&mut self, references: Vec<ObjectId>) -> ObjectId {
        // New objects always start in young generation
        let id = ObjectId(self.next_id);
        self.next_id += 1;

        let obj = Object {
            id,
            generation: Generation::Young,
            age: 0,
            references,
        };

        self.objects.insert(id, obj);
        id
    }

    pub fn add_root(&mut self, id: ObjectId) {
        self.roots.insert(id);
    }

    fn mark_from(&self, id: ObjectId, marked: &mut HashSet<ObjectId>) {
        if marked.contains(&id) {
            return;
        }
        marked.insert(id);

        if let Some(obj) = self.objects.get(&id) {
            for &ref_id in &obj.references {
                self.mark_from(ref_id, marked);
            }
        }
    }

    pub fn minor_collection(&mut self) {
        // TODO: Implement minor collection (young generation only)
        // 1. Mark all reachable objects from roots
        // 2. Remove unmarked young objects
        // 3. Age surviving young objects
        // 4. Promote old enough objects to old generation
        todo!()
    }

    pub fn major_collection(&mut self) {
        // TODO: Implement major collection (all generations)
        // 1. Mark all reachable objects from roots
        // 2. Remove all unmarked objects (young and old)
        // 3. Age surviving objects
        // 4. Promote objects that reach threshold
        todo!()
    }

    pub fn object_count(&self) -> usize {
        self.objects.len()
    }

    pub fn young_count(&self) -> usize {
        self.objects
            .values()
            .filter(|obj| obj.generation == Generation::Young)
            .count()
    }

    pub fn old_count(&self) -> usize {
        self.objects
            .values()
            .filter(|obj| obj.generation == Generation::Old)
            .count()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_minor_collection() {
        let mut gc = GenerationalGC::new(2);

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![]);

        gc.add_root(obj1);

        assert_eq!(gc.young_count(), 2);

        gc.minor_collection();

        // obj2 should be collected
        assert_eq!(gc.young_count(), 1);
    }

    #[test]
    fn test_promotion() {
        let mut gc = GenerationalGC::new(2);

        let obj1 = gc.allocate(vec![]);
        gc.add_root(obj1);

        assert_eq!(gc.young_count(), 1);
        assert_eq!(gc.old_count(), 0);

        gc.minor_collection();
        gc.minor_collection();

        // After 2 collections, should be promoted
        assert_eq!(gc.young_count(), 0);
        assert_eq!(gc.old_count(), 1);
    }

    #[test]
    fn test_major_collection() {
        let mut gc = GenerationalGC::new(1);

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![]);

        gc.add_root(obj1);

        gc.minor_collection(); // obj1 promoted, obj2 collected

        let obj3 = gc.allocate(vec![]);

        gc.major_collection();

        // Only obj1 should remain
        assert_eq!(gc.object_count(), 1);
    }
}
