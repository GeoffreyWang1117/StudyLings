// mm06_memory_pool.rs
//
// Memory pool pre-allocates fixed-size blocks and reuses them.
// Very efficient for allocating many objects of the same size.
//
// Your task: Implement a memory pool allocator.

// I AM NOT DONE

pub struct MemoryPool {
    block_size: usize,
    blocks: Vec<*mut u8>,
    free_list: Vec<*mut u8>,
    allocated_count: usize,
}

impl MemoryPool {
    pub fn new(block_size: usize, initial_blocks: usize) -> Self {
        // TODO: Create pool with initial blocks
        // All blocks start in free list
        todo!()
    }

    pub fn allocate(&mut self) -> Result<*mut u8, &'static str> {
        // TODO: Allocate a block
        // 1. Pop from free list if available
        // 2. Otherwise allocate new block
        // 3. Return pointer
        todo!()
    }

    pub fn deallocate(&mut self, ptr: *mut u8) -> Result<(), &'static str> {
        // TODO: Return block to free list
        // Verify ptr is valid (owned by this pool)
        todo!()
    }

    pub fn allocated_count(&self) -> usize {
        self.allocated_count
    }

    pub fn free_count(&self) -> usize {
        self.free_list.len()
    }

    pub fn total_blocks(&self) -> usize {
        self.blocks.len()
    }

    fn allocate_block(&mut self) -> *mut u8 {
        // TODO: Allocate a new block from system
        todo!()
    }

    fn is_owned(&self, ptr: *mut u8) -> bool {
        // TODO: Check if pointer belongs to this pool
        todo!()
    }
}

impl Drop for MemoryPool {
    fn drop(&mut self) {
        // TODO: Free all blocks
        todo!()
    }
}

// Type-safe wrapper around MemoryPool
pub struct TypedPool<T> {
    pool: MemoryPool,
    _phantom: std::marker::PhantomData<T>,
}

impl<T> TypedPool<T> {
    pub fn new(initial_capacity: usize) -> Self {
        // TODO: Create typed pool
        todo!()
    }

    pub fn allocate(&mut self, value: T) -> Result<*mut T, &'static str> {
        // TODO: Allocate and initialize with value
        todo!()
    }

    pub fn deallocate(&mut self, ptr: *mut T) -> Result<(), &'static str> {
        // TODO: Run destructor and return to pool
        todo!()
    }

    pub fn allocated_count(&self) -> usize {
        self.pool.allocated_count()
    }
}

impl<T> Drop for TypedPool<T> {
    fn drop(&mut self) {
        // Pool's drop will handle cleanup
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pool_allocation() {
        let mut pool = MemoryPool::new(64, 10);

        assert_eq!(pool.total_blocks(), 10);
        assert_eq!(pool.free_count(), 10);

        let ptr = pool.allocate().unwrap();
        assert_eq!(pool.free_count(), 9);
        assert_eq!(pool.allocated_count(), 1);

        pool.deallocate(ptr).unwrap();
        assert_eq!(pool.free_count(), 10);
        assert_eq!(pool.allocated_count(), 0);
    }

    #[test]
    fn test_pool_reuse() {
        let mut pool = MemoryPool::new(64, 5);

        let ptr1 = pool.allocate().unwrap();
        pool.deallocate(ptr1).unwrap();

        let ptr2 = pool.allocate().unwrap();

        // Should reuse the same block
        assert_eq!(ptr1, ptr2);
        assert_eq!(pool.total_blocks(), 5);
    }

    #[test]
    fn test_pool_expansion() {
        let mut pool = MemoryPool::new(64, 2);

        let _p1 = pool.allocate().unwrap();
        let _p2 = pool.allocate().unwrap();
        let _p3 = pool.allocate().unwrap();

        // Should have allocated more blocks
        assert_eq!(pool.total_blocks(), 3);
    }

    #[test]
    fn test_typed_pool() {
        let mut pool = TypedPool::<String>::new(10);

        let ptr = pool.allocate(String::from("hello")).unwrap();

        unsafe {
            assert_eq!(&*ptr, "hello");
        }

        pool.deallocate(ptr).unwrap();
        assert_eq!(pool.allocated_count(), 0);
    }

    #[test]
    fn test_invalid_dealloc() {
        let mut pool = MemoryPool::new(64, 10);
        let fake_ptr = 0x1234 as *mut u8;

        assert!(pool.deallocate(fake_ptr).is_err());
    }
}
