// os04_fifo_replacement.rs
//
// FIFO (First-In-First-Out) is the simplest page replacement algorithm. When a page
// needs to be replaced, the oldest page (the one that has been in memory the longest)
// is chosen for replacement.
//
// Your task: Implement a FIFO page replacement algorithm to simulate page faults.

// I AM NOT DONE

use std::collections::{HashMap, VecDeque};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct PageId(usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct FrameId(usize);

pub struct FIFOPageReplacement {
    frames: HashMap<FrameId, PageId>,
    page_to_frame: HashMap<PageId, FrameId>,
    fifo_queue: VecDeque<FrameId>,
    num_frames: usize,
    page_faults: usize,
    page_hits: usize,
}

impl FIFOPageReplacement {
    pub fn new(num_frames: usize) -> Self {
        // TODO: Initialize the FIFO page replacement system
        // Create the specified number of frames
        todo!()
    }

    pub fn access_page(&mut self, page: PageId) -> bool {
        // TODO: Access a page, returns true if page fault occurred
        // 1. Check if page is already in memory (page hit)
        // 2. If not, a page fault occurs:
        //    a. If there are free frames, use one
        //    b. Otherwise, evict the oldest page (front of FIFO queue)
        // 3. Update statistics
        todo!()
    }

    fn find_free_frame(&self) -> Option<FrameId> {
        // TODO: Find a free frame (one that doesn't contain a page)
        todo!()
    }

    fn evict_page(&mut self) -> Option<PageId> {
        // TODO: Evict the oldest page using FIFO policy
        // 1. Remove the front frame from the FIFO queue
        // 2. Get the page in that frame
        // 3. Remove the page-to-frame mapping
        // 4. Return the evicted page
        todo!()
    }

    pub fn page_faults(&self) -> usize {
        self.page_faults
    }

    pub fn page_hits(&self) -> usize {
        self.page_hits
    }

    pub fn hit_rate(&self) -> f64 {
        let total = self.page_faults + self.page_hits;
        if total == 0 {
            0.0
        } else {
            self.page_hits as f64 / total as f64
        }
    }

    pub fn is_page_in_memory(&self, page: PageId) -> bool {
        self.page_to_frame.contains_key(&page)
    }

    pub fn reset_stats(&mut self) {
        self.page_faults = 0;
        self.page_hits = 0;
    }
}

pub fn simulate_page_references(
    num_frames: usize,
    references: &[usize],
) -> (usize, usize, f64) {
    // TODO: Simulate a sequence of page references
    // Return (page_faults, page_hits, hit_rate)
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_page_faults() {
        let mut fifo = FIFOPageReplacement::new(3);

        // All unique pages, all should be page faults
        assert!(fifo.access_page(PageId(1)));
        assert!(fifo.access_page(PageId(2)));
        assert!(fifo.access_page(PageId(3)));

        assert_eq!(fifo.page_faults(), 3);
        assert_eq!(fifo.page_hits(), 0);
    }

    #[test]
    fn test_page_hits() {
        let mut fifo = FIFOPageReplacement::new(3);

        fifo.access_page(PageId(1));
        fifo.access_page(PageId(2));
        fifo.access_page(PageId(3));

        // Access existing pages - should be hits
        assert!(!fifo.access_page(PageId(1)));
        assert!(!fifo.access_page(PageId(2)));

        assert_eq!(fifo.page_faults(), 3);
        assert_eq!(fifo.page_hits(), 2);
    }

    #[test]
    fn test_fifo_replacement() {
        let mut fifo = FIFOPageReplacement::new(3);

        fifo.access_page(PageId(1));
        fifo.access_page(PageId(2));
        fifo.access_page(PageId(3));

        // This should evict page 1 (oldest)
        fifo.access_page(PageId(4));

        assert!(!fifo.is_page_in_memory(PageId(1)));
        assert!(fifo.is_page_in_memory(PageId(2)));
        assert!(fifo.is_page_in_memory(PageId(3)));
        assert!(fifo.is_page_in_memory(PageId(4)));
    }

    #[test]
    fn test_belady_anomaly() {
        // With 3 frames
        let (faults_3, _, _) = simulate_page_references(3, &[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]);

        // With 4 frames
        let (faults_4, _, _) = simulate_page_references(4, &[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]);

        // FIFO can exhibit Belady's anomaly (more frames -> more faults)
        // This test just ensures both complete successfully
        assert!(faults_3 > 0);
        assert!(faults_4 > 0);
    }

    #[test]
    fn test_sequential_pattern() {
        let mut fifo = FIFOPageReplacement::new(3);

        // Sequential access pattern
        for i in 0..10 {
            fifo.access_page(PageId(i));
        }

        // Should have many page faults due to sequential access
        assert!(fifo.page_faults() > 7);
    }

    #[test]
    fn test_cyclic_pattern() {
        let mut fifo = FIFOPageReplacement::new(3);

        // Cyclic pattern that fits in frames
        for _ in 0..10 {
            fifo.access_page(PageId(1));
            fifo.access_page(PageId(2));
            fifo.access_page(PageId(3));
        }

        // After first 3 accesses, all should be hits
        assert_eq!(fifo.page_faults(), 3);
        assert_eq!(fifo.page_hits(), 27); // 3 * 10 - 3
    }

    #[test]
    fn test_worst_case_pattern() {
        let mut fifo = FIFOPageReplacement::new(3);

        // Worst case: cyclic pattern with 4 pages (frames + 1)
        for _ in 0..5 {
            fifo.access_page(PageId(1));
            fifo.access_page(PageId(2));
            fifo.access_page(PageId(3));
            fifo.access_page(PageId(4));
        }

        // Every 4th access causes a page fault
        assert_eq!(fifo.page_faults(), 20); // All accesses are faults
    }

    #[test]
    fn test_hit_rate_calculation() {
        let mut fifo = FIFOPageReplacement::new(2);

        fifo.access_page(PageId(1)); // Fault
        fifo.access_page(PageId(2)); // Fault
        fifo.access_page(PageId(1)); // Hit
        fifo.access_page(PageId(2)); // Hit

        assert_eq!(fifo.hit_rate(), 0.5);
    }

    #[test]
    fn test_reset_stats() {
        let mut fifo = FIFOPageReplacement::new(3);

        fifo.access_page(PageId(1));
        fifo.access_page(PageId(2));

        assert_eq!(fifo.page_faults(), 2);

        fifo.reset_stats();

        assert_eq!(fifo.page_faults(), 0);
        assert_eq!(fifo.page_hits(), 0);
    }

    #[test]
    fn test_single_frame() {
        let mut fifo = FIFOPageReplacement::new(1);

        fifo.access_page(PageId(1));
        fifo.access_page(PageId(2));
        fifo.access_page(PageId(3));

        // With only 1 frame, every new page is a fault
        assert_eq!(fifo.page_faults(), 3);
        assert!(fifo.is_page_in_memory(PageId(3)));
        assert!(!fifo.is_page_in_memory(PageId(1)));
        assert!(!fifo.is_page_in_memory(PageId(2)));
    }
}
