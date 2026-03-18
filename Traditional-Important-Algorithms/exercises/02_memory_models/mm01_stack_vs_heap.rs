// mm01_stack_vs_heap.rs
//
// Understanding the difference between stack and heap allocation is fundamental.
// Stack: LIFO, fast, automatic cleanup, fixed size, local scope
// Heap: flexible size, manual management, slower, can outlive scope
//
// Your task: Implement a simple memory allocator that simulates stack and heap.

// I AM NOT DONE

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum AllocLocation {
    Stack,
    Heap,
}

pub struct MemorySimulator {
    stack: Vec<u8>,
    stack_pointer: usize,
    heap: Vec<Option<Vec<u8>>>,
    stack_capacity: usize,
}

impl MemorySimulator {
    pub fn new(stack_capacity: usize) -> Self {
        Self {
            stack: vec![0; stack_capacity],
            stack_pointer: 0,
            heap: Vec::new(),
            stack_capacity,
        }
    }

    pub fn stack_alloc(&mut self, size: usize) -> Result<usize, &'static str> {
        // TODO: Allocate on stack
        // Return the address (stack_pointer) if successful
        // Return error if not enough space
        todo!()
    }

    pub fn stack_free(&mut self, size: usize) -> Result<(), &'static str> {
        // TODO: Free from stack (just move stack pointer)
        // Stack frees in LIFO order
        todo!()
    }

    pub fn heap_alloc(&mut self, data: Vec<u8>) -> usize {
        // TODO: Allocate on heap
        // Find a free slot or add new one
        // Return the index as "address"
        todo!()
    }

    pub fn heap_free(&mut self, addr: usize) -> Result<(), &'static str> {
        // TODO: Free heap allocation
        // Mark slot as free (None)
        todo!()
    }

    pub fn stack_usage(&self) -> usize {
        self.stack_pointer
    }

    pub fn heap_usage(&self) -> usize {
        self.heap.iter().filter(|slot| slot.is_some()).count()
    }

    pub fn can_stack_alloc(&self, size: usize) -> bool {
        // TODO: Check if stack has enough space
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stack_allocation() {
        let mut sim = MemorySimulator::new(1024);

        let addr1 = sim.stack_alloc(100).unwrap();
        assert_eq!(addr1, 0);
        assert_eq!(sim.stack_usage(), 100);

        let addr2 = sim.stack_alloc(50).unwrap();
        assert_eq!(addr2, 100);
        assert_eq!(sim.stack_usage(), 150);
    }

    #[test]
    fn test_stack_free_lifo() {
        let mut sim = MemorySimulator::new(1024);

        sim.stack_alloc(100).unwrap();
        sim.stack_alloc(50).unwrap();

        sim.stack_free(50).unwrap();
        assert_eq!(sim.stack_usage(), 100);

        sim.stack_free(100).unwrap();
        assert_eq!(sim.stack_usage(), 0);
    }

    #[test]
    fn test_stack_overflow() {
        let mut sim = MemorySimulator::new(100);

        assert!(sim.stack_alloc(150).is_err());
    }

    #[test]
    fn test_heap_allocation() {
        let mut sim = MemorySimulator::new(1024);

        let addr1 = sim.heap_alloc(vec![1, 2, 3]);
        let addr2 = sim.heap_alloc(vec![4, 5, 6]);

        assert_eq!(sim.heap_usage(), 2);
        assert_ne!(addr1, addr2);
    }

    #[test]
    fn test_heap_free_and_reuse() {
        let mut sim = MemorySimulator::new(1024);

        let addr1 = sim.heap_alloc(vec![1, 2, 3]);
        sim.heap_free(addr1).unwrap();

        assert_eq!(sim.heap_usage(), 0);

        let addr2 = sim.heap_alloc(vec![4, 5, 6]);
        // Should reuse the freed slot
        assert_eq!(addr1, addr2);
    }
}
