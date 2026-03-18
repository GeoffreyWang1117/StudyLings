// gc08_write_barrier.rs
//
// Write barriers intercept pointer writes to maintain GC invariants.
// They're essential for incremental and concurrent GC.
//
// Your task: Implement different write barrier strategies.

// I AM NOT DONE

use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(usize);

#[derive(Debug, Clone, Copy, PartialEq)]
enum Color {
    White,
    Gray,
    Black,
}

pub struct WriteBarrierGC {
    objects: HashMap<ObjectId, (Color, Vec<ObjectId>)>,
    next_id: usize,
    roots: HashSet<ObjectId>,
    remembered_set: HashSet<(ObjectId, ObjectId)>,
}

impl WriteBarrierGC {
    pub fn new() -> Self {
        Self {
            objects: HashMap::new(),
            next_id: 0,
            roots: HashSet::new(),
            remembered_set: HashSet::new(),
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

    fn get_color(&self, id: ObjectId) -> Option<Color> {
        self.objects.get(&id).map(|(color, _)| *color)
    }

    fn set_color(&mut self, id: ObjectId, color: Color) {
        if let Some((obj_color, _)) = self.objects.get_mut(&id) {
            *obj_color = color;
        }
    }

    pub fn dijkstra_write_barrier(&mut self, from: ObjectId, to: ObjectId) {
        // TODO: Implement Dijkstra write barrier
        // If a black object points to a white object, shade the white object gray
        // This maintains the tricolor invariant: no black object points to white
        todo!()
    }

    pub fn steele_write_barrier(&mut self, from: ObjectId, _to: ObjectId) {
        // TODO: Implement Steele write barrier
        // Shade the source object gray (more conservative than Dijkstra)
        todo!()
    }

    pub fn generational_write_barrier(&mut self, from: ObjectId, to: ObjectId) {
        // TODO: Implement generational write barrier
        // Record old-to-young pointers in remembered set
        // (Simplified: just record all cross-generation pointers)
        todo!()
    }

    pub fn write_reference(&mut self, from: ObjectId, new_ref: ObjectId, barrier_type: &str) {
        // TODO: Update reference with specified write barrier
        // 1. Apply write barrier
        // 2. Update the reference
        todo!()
    }

    pub fn object_count(&self) -> usize {
        self.objects.len()
    }

    pub fn remembered_set_size(&self) -> usize {
        self.remembered_set.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dijkstra_barrier() {
        let mut gc = WriteBarrierGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![]);

        gc.set_color(obj1, Color::Black);
        gc.set_color(obj2, Color::White);

        gc.dijkstra_write_barrier(obj1, obj2);

        // obj2 should now be gray
        assert_eq!(gc.get_color(obj2), Some(Color::Gray));
    }

    #[test]
    fn test_steele_barrier() {
        let mut gc = WriteBarrierGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![]);

        gc.set_color(obj1, Color::Black);

        gc.steele_write_barrier(obj1, obj2);

        // obj1 should now be gray
        assert_eq!(gc.get_color(obj1), Some(Color::Gray));
    }

    #[test]
    fn test_generational_barrier() {
        let mut gc = WriteBarrierGC::new();

        let old_obj = gc.allocate(vec![]);
        let young_obj = gc.allocate(vec![]);

        gc.generational_write_barrier(old_obj, young_obj);

        assert_eq!(gc.remembered_set_size(), 1);
    }

    #[test]
    fn test_write_with_barrier() {
        let mut gc = WriteBarrierGC::new();

        let obj1 = gc.allocate(vec![]);
        let obj2 = gc.allocate(vec![]);

        gc.set_color(obj1, Color::Black);
        gc.set_color(obj2, Color::White);

        gc.write_reference(obj1, obj2, "dijkstra");

        assert_eq!(gc.get_color(obj2), Some(Color::Gray));
    }
}
