// gc03_copying_gc.rs
//
// Copying GC divides the heap into two semi-spaces: from-space and to-space.
// During collection:
// 1. Copy all live objects from from-space to to-space
// 2. Swap the spaces
// 3. All dead objects are implicitly freed
//
// Your task: Implement a simple copying garbage collector.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(usize);

#[derive(Debug, Clone)]
pub struct Object {
    data: Vec<u8>,
    references: Vec<ObjectId>,
}

pub struct CopyingGC {
    from_space: HashMap<ObjectId, Object>,
    to_space: HashMap<ObjectId, Object>,
    next_id: usize,
    roots: Vec<ObjectId>,
    // Forwarding table: maps old IDs to new IDs during collection
    forwarding: HashMap<ObjectId, ObjectId>,
}

impl CopyingGC {
    pub fn new() -> Self {
        Self {
            from_space: HashMap::new(),
            to_space: HashMap::new(),
            next_id: 0,
            roots: Vec::new(),
            forwarding: HashMap::new(),
        }
    }

    pub fn allocate(&mut self, data: Vec<u8>, references: Vec<ObjectId>) -> ObjectId {
        let id = ObjectId(self.next_id);
        self.next_id += 1;

        let obj = Object { data, references };
        self.from_space.insert(id, obj);
        id
    }

    pub fn add_root(&mut self, id: ObjectId) {
        self.roots.push(id);
    }

    fn copy_object(&mut self, old_id: ObjectId) -> ObjectId {
        // TODO: Copy an object from from-space to to-space
        // 1. Check if already copied (in forwarding table)
        // 2. If not, copy the object to to-space with a new ID
        // 3. Add to forwarding table
        // 4. Return the new ID
        todo!()
    }

    fn update_references(&mut self, obj_id: ObjectId) {
        // TODO: Update all references in the object to point to new IDs
        // Use the forwarding table to map old IDs to new IDs
        todo!()
    }

    pub fn collect(&mut self) {
        // TODO: Implement the copying collection algorithm
        // 1. Clear to_space and forwarding table
        // 2. Copy all root objects
        // 3. Update all references in copied objects
        // 4. Swap from_space and to_space
        // 5. Clear the old from_space
        todo!()
    }

    pub fn object_count(&self) -> usize {
        self.from_space.len()
    }

    pub fn get_object(&self, id: ObjectId) -> Option<&Object> {
        self.from_space.get(&id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_copy() {
        let mut gc = CopyingGC::new();

        let obj1 = gc.allocate(vec![1, 2, 3], vec![]);
        gc.add_root(obj1);

        let obj2 = gc.allocate(vec![4, 5, 6], vec![]);

        assert_eq!(gc.object_count(), 2);

        gc.collect();

        // Only obj1 should remain (it's a root)
        assert_eq!(gc.object_count(), 1);
    }

    #[test]
    fn test_reference_update() {
        let mut gc = CopyingGC::new();

        let obj1 = gc.allocate(vec![1], vec![]);
        let obj2 = gc.allocate(vec![2], vec![obj1]);

        gc.add_root(obj2);

        gc.collect();

        assert_eq!(gc.object_count(), 2);
    }

    #[test]
    fn test_multiple_collections() {
        let mut gc = CopyingGC::new();

        let obj1 = gc.allocate(vec![1], vec![]);
        gc.add_root(obj1);

        gc.collect();
        assert_eq!(gc.object_count(), 1);

        let obj2 = gc.allocate(vec![2], vec![]);
        gc.collect();

        // obj2 not rooted, should be collected
        assert_eq!(gc.object_count(), 1);
    }
}
