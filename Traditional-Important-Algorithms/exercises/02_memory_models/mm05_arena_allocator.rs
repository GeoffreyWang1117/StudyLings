// mm05_arena_allocator.rs
//
// Arena allocator (bump allocator) allocates from a large buffer.
// Extremely fast allocation (just increment pointer), but can only
// free all allocations at once.
//
// Your task: Implement an arena allocator.

// I AM NOT DONE

pub struct Arena {
    buffer: Vec<u8>,
    offset: usize,
}

impl Arena {
    pub fn new(capacity: usize) -> Self {
        // TODO: Create new arena with given capacity
        todo!()
    }

    pub fn allocate(&mut self, size: usize, align: usize) -> Result<usize, &'static str> {
        // TODO: Allocate 'size' bytes with alignment
        // 1. Align current offset
        // 2. Check if enough space
        // 3. Return offset and increment
        todo!()
    }

    pub fn allocate_slice<T: Copy>(&mut self, values: &[T]) -> Result<usize, &'static str> {
        // TODO: Allocate space for slice
        // Calculate size and alignment for T
        todo!()
    }

    pub fn reset(&mut self) {
        // TODO: Reset arena (free all allocations)
        todo!()
    }

    pub fn used(&self) -> usize {
        self.offset
    }

    pub fn capacity(&self) -> usize {
        self.buffer.len()
    }

    pub fn available(&self) -> usize {
        self.capacity() - self.used()
    }

    // Helper to align offset
    fn align_offset(offset: usize, align: usize) -> usize {
        (offset + align - 1) & !(align - 1)
    }
}

// Arena-allocated string
pub struct ArenaString<'a> {
    arena: &'a mut Arena,
    offset: usize,
    len: usize,
}

impl<'a> ArenaString<'a> {
    pub fn new(arena: &'a mut Arena, s: &str) -> Result<Self, &'static str> {
        // TODO: Allocate string in arena
        // Store bytes and return ArenaString
        todo!()
    }

    pub fn as_str(&self) -> &str {
        // TODO: Return string slice from arena
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_allocation() {
        let mut arena = Arena::new(1024);

        let addr1 = arena.allocate(100, 1).unwrap();
        assert_eq!(addr1, 0);
        assert_eq!(arena.used(), 100);

        let addr2 = arena.allocate(50, 1).unwrap();
        assert_eq!(addr2, 100);
        assert_eq!(arena.used(), 150);
    }

    #[test]
    fn test_alignment() {
        let mut arena = Arena::new(1024);

        arena.allocate(1, 1).unwrap();
        let addr = arena.allocate(8, 8).unwrap();

        // Should be aligned to 8 bytes
        assert_eq!(addr % 8, 0);
    }

    #[test]
    fn test_out_of_memory() {
        let mut arena = Arena::new(100);

        assert!(arena.allocate(150, 1).is_err());
    }

    #[test]
    fn test_reset() {
        let mut arena = Arena::new(1024);

        arena.allocate(100, 1).unwrap();
        arena.allocate(200, 1).unwrap();

        assert_eq!(arena.used(), 300);

        arena.reset();

        assert_eq!(arena.used(), 0);
        assert_eq!(arena.available(), 1024);
    }

    #[test]
    fn test_allocate_slice() {
        let mut arena = Arena::new(1024);

        let values = [1u32, 2, 3, 4, 5];
        let addr = arena.allocate_slice(&values).unwrap();

        // Should be aligned for u32
        assert_eq!(addr % std::mem::align_of::<u32>(), 0);
    }

    #[test]
    fn test_arena_string() {
        let mut arena = Arena::new(1024);

        let s = ArenaString::new(&mut arena, "hello world").unwrap();
        assert_eq!(s.as_str(), "hello world");
    }

    #[test]
    fn test_many_allocations() {
        let mut arena = Arena::new(1024);

        for i in 0..100 {
            let _ = arena.allocate(8, 1).unwrap();
        }

        assert!(arena.used() <= arena.capacity());
    }
}
