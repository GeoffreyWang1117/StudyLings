// os06_buddy_system.rs
//
// The Buddy System is a memory allocation algorithm that divides memory into partitions
// to try to satisfy memory requests as efficiently as possible. When a request is made,
// it rounds up to the next power of 2 and allocates a block of that size by splitting
// larger blocks if necessary.
//
// Your task: Implement a buddy system memory allocator.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct BlockId(usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Block {
    start: usize,
    size: usize,
    allocated: bool,
}

pub struct BuddySystem {
    min_block_size: usize,
    max_block_size: usize,
    // Free lists for each power-of-2 size
    free_lists: HashMap<usize, Vec<Block>>,
    // Track allocated blocks
    allocated_blocks: HashMap<BlockId, Block>,
    next_id: usize,
}

impl BuddySystem {
    pub fn new(total_size: usize, min_block_size: usize) -> Self {
        // TODO: Initialize the buddy system
        // 1. Ensure total_size is a power of 2
        // 2. Create free lists for each power of 2 from min_block_size to total_size
        // 3. Add one large block to the largest free list
        todo!()
    }

    fn get_buddy_address(&self, addr: usize, size: usize) -> usize {
        // TODO: Calculate the address of the buddy block
        // The buddy of a block at address addr with size is at addr XOR size
        todo!()
    }

    fn next_power_of_2(&self, size: usize) -> usize {
        // TODO: Round up to the next power of 2
        // Hint: Use size.next_power_of_two() or implement manually
        todo!()
    }

    pub fn allocate(&mut self, size: usize) -> Result<BlockId, &'static str> {
        // TODO: Allocate a block of at least 'size' bytes
        // 1. Round size up to next power of 2, but at least min_block_size
        // 2. Find a free block of appropriate size (may need to split larger blocks)
        // 3. Mark as allocated and return BlockId
        todo!()
    }

    fn find_and_remove_free_block(&mut self, size: usize) -> Option<Block> {
        // TODO: Find and remove a free block of the given size
        // If not available, try to split a larger block recursively
        todo!()
    }

    fn split_block(&mut self, block: Block) -> (Block, Block) {
        // TODO: Split a block into two buddy blocks of half the size
        // The two blocks should be adjacent and of equal size
        todo!()
    }

    pub fn free(&mut self, id: BlockId) -> Result<(), &'static str> {
        // TODO: Free a block and merge with buddy if possible
        // 1. Remove from allocated_blocks
        // 2. Try to merge with buddy recursively
        // 3. Add to appropriate free list
        todo!()
    }

    fn try_merge(&mut self, block: Block) -> Block {
        // TODO: Try to merge block with its buddy
        // 1. Calculate buddy address
        // 2. Check if buddy is free and same size
        // 3. If yes, merge and try to merge the larger block recursively
        // 4. If no, return the block as-is
        todo!()
    }

    fn remove_from_free_list(&mut self, block: Block) -> bool {
        // TODO: Remove a specific block from its free list
        // Return true if found and removed, false otherwise
        todo!()
    }

    fn add_to_free_list(&mut self, block: Block) {
        // TODO: Add a block to the appropriate free list based on its size
        todo!()
    }

    pub fn get_block_info(&self, id: BlockId) -> Option<Block> {
        self.allocated_blocks.get(&id).copied()
    }

    pub fn total_free_memory(&self) -> usize {
        // TODO: Calculate total free memory across all free lists
        todo!()
    }

    pub fn free_blocks_of_size(&self, size: usize) -> usize {
        // TODO: Count number of free blocks of a specific size
        todo!()
    }

    pub fn fragmentation_ratio(&self) -> f64 {
        // TODO: Calculate fragmentation as ratio of largest free block to total free memory
        // Lower fragmentation means memory is less fragmented
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_allocation() {
        let mut buddy = BuddySystem::new(1024, 64);

        let block1 = buddy.allocate(64).unwrap();
        let block2 = buddy.allocate(128).unwrap();

        assert!(buddy.get_block_info(block1).is_some());
        assert!(buddy.get_block_info(block2).is_some());
    }

    #[test]
    fn test_allocation_and_free() {
        let mut buddy = BuddySystem::new(1024, 64);

        let block = buddy.allocate(128).unwrap();
        let info = buddy.get_block_info(block).unwrap();

        assert_eq!(info.size, 128);

        buddy.free(block).unwrap();

        // After freeing, should be able to allocate again
        let block2 = buddy.allocate(128).unwrap();
        assert!(buddy.get_block_info(block2).is_some());
    }

    #[test]
    fn test_buddy_merging() {
        let mut buddy = BuddySystem::new(1024, 64);

        // Allocate two buddy blocks
        let block1 = buddy.allocate(256).unwrap();
        let block2 = buddy.allocate(256).unwrap();

        buddy.free(block1).unwrap();
        buddy.free(block2).unwrap();

        // After freeing both buddies, they should merge
        // We should be able to allocate a 512-byte block
        let large_block = buddy.allocate(512).unwrap();
        assert!(buddy.get_block_info(large_block).is_some());
    }

    #[test]
    fn test_splitting() {
        let mut buddy = BuddySystem::new(1024, 64);

        // Request small block, should split larger ones
        let block = buddy.allocate(64).unwrap();
        let info = buddy.get_block_info(block).unwrap();

        assert_eq!(info.size, 64);
    }

    #[test]
    fn test_out_of_memory() {
        let mut buddy = BuddySystem::new(256, 64);

        buddy.allocate(128).unwrap();
        buddy.allocate(64).unwrap();
        buddy.allocate(64).unwrap();

        // Should be out of memory now
        let result = buddy.allocate(64);
        assert!(result.is_err());
    }

    #[test]
    fn test_power_of_two_rounding() {
        let mut buddy = BuddySystem::new(1024, 64);

        // Request 100 bytes, should allocate 128 (next power of 2)
        let block = buddy.allocate(100).unwrap();
        let info = buddy.get_block_info(block).unwrap();

        assert_eq!(info.size, 128);
    }

    #[test]
    fn test_minimum_block_size() {
        let mut buddy = BuddySystem::new(1024, 64);

        // Request less than minimum, should allocate minimum
        let block = buddy.allocate(32).unwrap();
        let info = buddy.get_block_info(block).unwrap();

        assert_eq!(info.size, 64);
    }

    #[test]
    fn test_multiple_allocations() {
        let mut buddy = BuddySystem::new(1024, 64);

        let mut blocks = Vec::new();
        for _ in 0..5 {
            let block = buddy.allocate(64).unwrap();
            blocks.push(block);
        }

        // All blocks should be valid
        for block in &blocks {
            assert!(buddy.get_block_info(*block).is_some());
        }

        // Free all blocks
        for block in blocks {
            buddy.free(block).unwrap();
        }
    }

    #[test]
    fn test_fragmentation() {
        let mut buddy = BuddySystem::new(1024, 64);

        let b1 = buddy.allocate(64).unwrap();
        let _b2 = buddy.allocate(64).unwrap();
        let b3 = buddy.allocate(64).unwrap();

        // Free alternating blocks to create fragmentation
        buddy.free(b1).unwrap();
        buddy.free(b3).unwrap();

        let frag = buddy.fragmentation_ratio();
        assert!(frag >= 0.0 && frag <= 1.0);
    }

    #[test]
    fn test_total_free_memory() {
        let mut buddy = BuddySystem::new(1024, 64);

        let initial_free = buddy.total_free_memory();
        assert_eq!(initial_free, 1024);

        let block = buddy.allocate(256).unwrap();

        let after_alloc = buddy.total_free_memory();
        assert_eq!(after_alloc, 1024 - 256);

        buddy.free(block).unwrap();

        let after_free = buddy.total_free_memory();
        assert_eq!(after_free, 1024);
    }

    #[test]
    fn test_complex_merging() {
        let mut buddy = BuddySystem::new(1024, 64);

        // Allocate several blocks
        let b1 = buddy.allocate(128).unwrap();
        let b2 = buddy.allocate(128).unwrap();
        let b3 = buddy.allocate(128).unwrap();
        let b4 = buddy.allocate(128).unwrap();

        // Free in specific order to test merging
        buddy.free(b2).unwrap();
        buddy.free(b1).unwrap();
        buddy.free(b4).unwrap();
        buddy.free(b3).unwrap();

        // All blocks should be merged back
        assert_eq!(buddy.total_free_memory(), 1024);
    }

    #[test]
    fn test_free_blocks_count() {
        let mut buddy = BuddySystem::new(1024, 64);

        // Initially should have 1 block of size 1024
        assert_eq!(buddy.free_blocks_of_size(1024), 1);

        // Allocate a 256-byte block
        buddy.allocate(256).unwrap();

        // Should have split: 1 block of 512, 1 of 256, smaller ones
        assert!(buddy.free_blocks_of_size(512) >= 1);
    }
}
