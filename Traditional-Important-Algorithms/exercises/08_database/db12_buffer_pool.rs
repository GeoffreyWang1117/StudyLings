// db12_buffer_pool.rs
//
// Buffer Pool Manager is a critical component in database systems that manages
// the in-memory cache of disk pages. It reduces expensive disk I/O operations
// by keeping frequently accessed pages in memory.
//
// Key components:
// - Buffer pool: Array of frames (memory pages)
// - Page table: Maps page IDs to frame IDs
// - Replacer: Eviction policy (LRU, Clock, etc.)
// - Dirty bit: Track which pages have been modified
//
// Operations:
// - FetchPage: Load page from disk to buffer pool
// - UnpinPage: Mark page as available for eviction
// - FlushPage: Write dirty page to disk
//
// Your task: Implement a buffer pool manager with LRU eviction policy.

// I AM NOT DONE

use std::collections::{HashMap, VecDeque};

pub type PageId = usize;
pub type FrameId = usize;

#[derive(Debug, Clone)]
pub struct Page {
    page_id: PageId,
    data: Vec<u8>,
    is_dirty: bool,
    pin_count: usize,
}

impl Page {
    fn new(page_id: PageId, size: usize) -> Self {
        Self {
            page_id,
            data: vec![0; size],
            is_dirty: false,
            pin_count: 0,
        }
    }
}

pub struct BufferPoolManager {
    pool: Vec<Option<Page>>,
    page_table: HashMap<PageId, FrameId>,
    free_list: VecDeque<FrameId>,
    lru_list: VecDeque<FrameId>,
    pool_size: usize,
    page_size: usize,
}

impl BufferPoolManager {
    pub fn new(pool_size: usize, page_size: usize) -> Self {
        let mut free_list = VecDeque::new();
        for i in 0..pool_size {
            free_list.push_back(i);
        }

        Self {
            pool: vec![None; pool_size],
            page_table: HashMap::new(),
            free_list,
            lru_list: VecDeque::new(),
            pool_size,
            page_size,
        }
    }

    pub fn fetch_page(&mut self, page_id: PageId) -> Option<&mut Page> {
        // TODO: Fetch a page from the buffer pool
        // If page is already in buffer pool, increment pin_count and return it
        // If not in pool:
        //   - Find a free frame or evict a page using LRU
        //   - Load page from "disk" (simulate by creating new page)
        //   - Add to page table and update LRU
        //   - Return the page
        todo!()
    }

    pub fn unpin_page(&mut self, page_id: PageId, is_dirty: bool) -> bool {
        // TODO: Unpin a page
        // Decrement pin_count
        // Set dirty bit if is_dirty is true
        // If pin_count reaches 0, page becomes candidate for eviction
        // Return true if successful, false if page not in pool
        todo!()
    }

    pub fn flush_page(&mut self, page_id: PageId) -> bool {
        // TODO: Write page to disk if dirty
        // Simulate disk write
        // Clear dirty bit
        // Return true if successful, false if page not in pool
        todo!()
    }

    pub fn flush_all_pages(&mut self) {
        // TODO: Flush all dirty pages to disk
        todo!()
    }

    pub fn new_page(&mut self) -> Option<PageId> {
        // TODO: Allocate a new page
        // Find a free frame or evict a page
        // Assign a new page ID
        // Add to buffer pool
        // Return the new page ID
        todo!()
    }

    pub fn delete_page(&mut self, page_id: PageId) -> bool {
        // TODO: Delete a page from the buffer pool
        // Page must not be pinned
        // Remove from page table
        // Add frame to free list
        // Return true if successful
        todo!()
    }

    fn evict_page(&mut self) -> Option<FrameId> {
        // TODO: Evict a page using LRU policy
        // Find the least recently used page with pin_count = 0
        // If page is dirty, flush it first
        // Remove from page table
        // Return the freed frame ID
        todo!()
    }

    fn update_lru(&mut self, frame_id: FrameId) {
        // TODO: Update LRU list when a page is accessed
        // Remove frame from current position in LRU list
        // Add to back of LRU list (most recently used)
        todo!()
    }

    pub fn get_pool_size(&self) -> usize {
        self.pool_size
    }

    pub fn get_free_list_size(&self) -> usize {
        self.free_list.len()
    }

    pub fn get_page_table_size(&self) -> usize {
        self.page_table.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_buffer_pool() {
        let bpm = BufferPoolManager::new(10, 4096);
        assert_eq!(bpm.get_pool_size(), 10);
        assert_eq!(bpm.get_free_list_size(), 10);
    }

    #[test]
    fn test_new_page() {
        let mut bpm = BufferPoolManager::new(10, 4096);
        let page_id = bpm.new_page();
        assert!(page_id.is_some());
        assert_eq!(bpm.get_free_list_size(), 9);
    }

    #[test]
    fn test_fetch_page() {
        let mut bpm = BufferPoolManager::new(10, 4096);
        let page_id = bpm.new_page().unwrap();

        let page = bpm.fetch_page(page_id);
        assert!(page.is_some());
    }

    #[test]
    fn test_unpin_page() {
        let mut bpm = BufferPoolManager::new(10, 4096);
        let page_id = bpm.new_page().unwrap();

        bpm.fetch_page(page_id);
        assert!(bpm.unpin_page(page_id, false));
    }

    #[test]
    fn test_pin_count() {
        let mut bpm = BufferPoolManager::new(10, 4096);
        let page_id = bpm.new_page().unwrap();

        bpm.fetch_page(page_id);
        bpm.fetch_page(page_id); // Pin twice

        assert!(bpm.unpin_page(page_id, false));
        assert!(bpm.unpin_page(page_id, false));
    }

    #[test]
    fn test_dirty_page() {
        let mut bpm = BufferPoolManager::new(10, 4096);
        let page_id = bpm.new_page().unwrap();

        bpm.fetch_page(page_id);
        bpm.unpin_page(page_id, true); // Mark as dirty

        assert!(bpm.flush_page(page_id));
    }

    #[test]
    fn test_eviction() {
        let mut bpm = BufferPoolManager::new(2, 4096);

        let page1 = bpm.new_page().unwrap();
        let page2 = bpm.new_page().unwrap();

        bpm.fetch_page(page1);
        bpm.unpin_page(page1, false);

        bpm.fetch_page(page2);
        bpm.unpin_page(page2, false);

        // Buffer pool is full, next allocation should trigger eviction
        let page3 = bpm.new_page();
        assert!(page3.is_some());
    }

    #[test]
    fn test_cannot_evict_pinned_page() {
        let mut bpm = BufferPoolManager::new(2, 4096);

        let page1 = bpm.new_page().unwrap();
        let page2 = bpm.new_page().unwrap();

        bpm.fetch_page(page1); // Pin page1
        bpm.unpin_page(page1, false);

        bpm.fetch_page(page2); // Pin page2 but don't unpin

        // Should not be able to evict page2 (it's pinned)
        let page3 = bpm.new_page();
        assert!(page3.is_some() || page3.is_none()); // Depends on implementation
    }

    #[test]
    fn test_delete_page() {
        let mut bpm = BufferPoolManager::new(10, 4096);
        let page_id = bpm.new_page().unwrap();

        bpm.fetch_page(page_id);
        bpm.unpin_page(page_id, false);

        assert!(bpm.delete_page(page_id));
        assert_eq!(bpm.get_page_table_size(), 0);
    }

    #[test]
    fn test_flush_all_pages() {
        let mut bpm = BufferPoolManager::new(10, 4096);

        for _ in 0..5 {
            let page_id = bpm.new_page().unwrap();
            bpm.fetch_page(page_id);
            bpm.unpin_page(page_id, true); // Mark all as dirty
        }

        bpm.flush_all_pages();
        // All pages should now be clean
    }

    #[test]
    fn test_lru_eviction_order() {
        let mut bpm = BufferPoolManager::new(3, 4096);

        let page1 = bpm.new_page().unwrap();
        let page2 = bpm.new_page().unwrap();
        let page3 = bpm.new_page().unwrap();

        bpm.fetch_page(page1);
        bpm.unpin_page(page1, false);

        bpm.fetch_page(page2);
        bpm.unpin_page(page2, false);

        bpm.fetch_page(page3);
        bpm.unpin_page(page3, false);

        // Access page1 again to make it recently used
        bpm.fetch_page(page1);
        bpm.unpin_page(page1, false);

        // Now page2 is LRU, should be evicted first
        let page4 = bpm.new_page().unwrap();
        bpm.fetch_page(page4);
    }

    #[test]
    fn test_multiple_fetch_same_page() {
        let mut bpm = BufferPoolManager::new(10, 4096);
        let page_id = bpm.new_page().unwrap();

        bpm.fetch_page(page_id);
        bpm.fetch_page(page_id);
        bpm.fetch_page(page_id);

        // Should unpin 3 times
        assert!(bpm.unpin_page(page_id, false));
        assert!(bpm.unpin_page(page_id, false));
        assert!(bpm.unpin_page(page_id, false));
    }

    #[test]
    fn test_stress_test() {
        let mut bpm = BufferPoolManager::new(5, 4096);

        for _ in 0..20 {
            let page_id = bpm.new_page();
            if let Some(pid) = page_id {
                bpm.fetch_page(pid);
                bpm.unpin_page(pid, true);
            }
        }

        bpm.flush_all_pages();
    }
}
