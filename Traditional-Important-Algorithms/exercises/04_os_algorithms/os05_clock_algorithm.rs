// os05_clock_algorithm.rs
//
// The Clock algorithm (also known as Second-Chance algorithm) is an approximation of LRU
// that uses a circular list and a reference bit. When a page needs to be replaced, the
// algorithm scans through pages giving them a "second chance" if their reference bit is set.
//
// Your task: Implement the Clock page replacement algorithm.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct PageId(usize);

#[derive(Debug, Clone)]
struct ClockFrame {
    page: Option<PageId>,
    reference_bit: bool,
}

pub struct ClockAlgorithm {
    frames: Vec<ClockFrame>,
    page_to_frame: HashMap<PageId, usize>,
    clock_hand: usize,
    page_faults: usize,
    page_hits: usize,
}

impl ClockAlgorithm {
    pub fn new(num_frames: usize) -> Self {
        // TODO: Initialize the Clock algorithm
        // Create frames with no pages and reference_bit = false
        todo!()
    }

    pub fn access_page(&mut self, page: PageId) -> bool {
        // TODO: Access a page, returns true if page fault occurred
        // 1. Check if page is in memory
        //    a. If yes (page hit): set reference bit to true, return false
        //    b. If no (page fault): find victim and replace, return true
        todo!()
    }

    fn find_victim(&mut self) -> usize {
        // TODO: Find a victim frame using the clock algorithm
        // 1. Start at clock_hand position
        // 2. Loop through frames:
        //    a. If reference_bit is false, return this frame
        //    b. If reference_bit is true, set it to false and advance clock_hand
        // 3. Update clock_hand position
        todo!()
    }

    fn replace_page(&mut self, frame_idx: usize, new_page: PageId) {
        // TODO: Replace the page in the given frame
        // 1. If frame contains a page, remove it from page_to_frame map
        // 2. Insert new page into the frame
        // 3. Set reference_bit to true (just accessed)
        // 4. Update page_to_frame map
        todo!()
    }

    pub fn set_reference_bit(&mut self, page: PageId, value: bool) {
        // TODO: Set the reference bit for a page
        // This simulates hardware setting/clearing the bit
        todo!()
    }

    pub fn get_reference_bit(&self, page: PageId) -> Option<bool> {
        // TODO: Get the reference bit for a page
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

    pub fn clock_position(&self) -> usize {
        self.clock_hand
    }

    pub fn reset_stats(&mut self) {
        self.page_faults = 0;
        self.page_hits = 0;
    }
}

pub fn simulate_with_clock(num_frames: usize, references: &[usize]) -> (usize, usize, f64) {
    // TODO: Simulate page references using Clock algorithm
    // Return (page_faults, page_hits, hit_rate)
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_initial_page_faults() {
        let mut clock = ClockAlgorithm::new(3);

        assert!(clock.access_page(PageId(1)));
        assert!(clock.access_page(PageId(2)));
        assert!(clock.access_page(PageId(3)));

        assert_eq!(clock.page_faults(), 3);
        assert_eq!(clock.page_hits(), 0);
    }

    #[test]
    fn test_page_hits() {
        let mut clock = ClockAlgorithm::new(3);

        clock.access_page(PageId(1));
        clock.access_page(PageId(2));
        clock.access_page(PageId(3));

        // Access existing pages
        assert!(!clock.access_page(PageId(1)));
        assert!(!clock.access_page(PageId(2)));

        assert_eq!(clock.page_faults(), 3);
        assert_eq!(clock.page_hits(), 2);
    }

    #[test]
    fn test_second_chance() {
        let mut clock = ClockAlgorithm::new(3);

        // Fill all frames
        clock.access_page(PageId(1));
        clock.access_page(PageId(2));
        clock.access_page(PageId(3));

        // Access page 1, setting its reference bit
        clock.access_page(PageId(1));

        // Access new page - should skip page 1 due to reference bit
        clock.access_page(PageId(4));

        // Page 1 should still be in memory (got second chance)
        assert!(clock.is_page_in_memory(PageId(1)));
    }

    #[test]
    fn test_reference_bits() {
        let mut clock = ClockAlgorithm::new(3);

        clock.access_page(PageId(1));
        clock.access_page(PageId(2));

        // Both should have reference bit set (just accessed)
        assert_eq!(clock.get_reference_bit(PageId(1)), Some(true));
        assert_eq!(clock.get_reference_bit(PageId(2)), Some(true));

        // Clear reference bit
        clock.set_reference_bit(PageId(1), false);
        assert_eq!(clock.get_reference_bit(PageId(1)), Some(false));
    }

    #[test]
    fn test_clock_hand_movement() {
        let mut clock = ClockAlgorithm::new(3);

        let initial_pos = clock.clock_position();

        clock.access_page(PageId(1));
        clock.access_page(PageId(2));
        clock.access_page(PageId(3));

        // Fill frames - clock hand should be at start
        assert_eq!(clock.clock_position(), initial_pos);

        // Trigger replacement - clock hand should advance
        clock.access_page(PageId(4));

        // Clock hand should have moved
        assert!(clock.clock_position() != initial_pos || clock.clock_position() == 0);
    }

    #[test]
    fn test_cyclic_pattern() {
        let mut clock = ClockAlgorithm::new(3);

        // Pattern that fits in frames
        for _ in 0..10 {
            clock.access_page(PageId(1));
            clock.access_page(PageId(2));
            clock.access_page(PageId(3));
        }

        // After first 3, all should be hits
        assert_eq!(clock.page_faults(), 3);
        assert_eq!(clock.page_hits(), 27);
    }

    #[test]
    fn test_better_than_fifo() {
        // Clock should perform better than FIFO on certain patterns
        // due to the second-chance mechanism
        let references = vec![1, 2, 3, 1, 4, 1, 5, 1, 6];
        let (faults, _, _) = simulate_with_clock(3, &references);

        // With repeated access to page 1, Clock should give it second chances
        assert!(faults < references.len());
    }

    #[test]
    fn test_all_reference_bits_set() {
        let mut clock = ClockAlgorithm::new(3);

        clock.access_page(PageId(1));
        clock.access_page(PageId(2));
        clock.access_page(PageId(3));

        // All have reference bits set
        // Access all to keep reference bits set
        clock.access_page(PageId(1));
        clock.access_page(PageId(2));
        clock.access_page(PageId(3));

        // Now add a new page - should clear all reference bits
        // and replace the first one encountered
        clock.access_page(PageId(4));

        assert_eq!(clock.page_faults(), 4);
    }

    #[test]
    fn test_single_frame() {
        let mut clock = ClockAlgorithm::new(1);

        clock.access_page(PageId(1));
        clock.access_page(PageId(2));
        clock.access_page(PageId(3));

        // With 1 frame, every new page causes replacement
        assert_eq!(clock.page_faults(), 3);
        assert!(clock.is_page_in_memory(PageId(3)));
    }

    #[test]
    fn test_sequential_vs_random() {
        // Sequential pattern
        let sequential: Vec<usize> = (0..20).collect();
        let (seq_faults, _, _) = simulate_with_clock(4, &sequential);

        // Random pattern with locality
        let random = vec![1, 2, 3, 1, 2, 4, 1, 2, 3, 5, 1, 2, 6];
        let (rand_faults, _, _) = simulate_with_clock(4, &random);

        // Both should complete successfully
        assert!(seq_faults > 0);
        assert!(rand_faults > 0);
    }

    #[test]
    fn test_hit_rate() {
        let mut clock = ClockAlgorithm::new(3);

        clock.access_page(PageId(1));
        clock.access_page(PageId(2));
        clock.access_page(PageId(1)); // Hit
        clock.access_page(PageId(2)); // Hit

        let hit_rate = clock.hit_rate();
        assert!((hit_rate - 0.5).abs() < 0.01); // Should be 50%
    }
}
