// os01_paging.rs
//
// Paging is a memory management scheme that eliminates the need for contiguous
// allocation of physical memory. The physical address space is divided into fixed-size
// blocks called frames, and the logical address space is divided into blocks of the
// same size called pages.
//
// Your task: Implement a simple paging system with a page table for address translation.

// I AM NOT DONE

use std::collections::HashMap;

const PAGE_SIZE: usize = 4096; // 4KB pages

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct PageNumber(usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct FrameNumber(usize);

#[derive(Debug, Clone, Copy)]
pub struct PageTableEntry {
    frame: FrameNumber,
    valid: bool,
    dirty: bool,
    referenced: bool,
}

pub struct PageTable {
    entries: HashMap<PageNumber, PageTableEntry>,
}

impl PageTable {
    pub fn new() -> Self {
        Self {
            entries: HashMap::new(),
        }
    }

    pub fn map_page(&mut self, page: PageNumber, frame: FrameNumber) {
        // TODO: Create a new page table entry mapping the page to the frame
        // Set valid=true, dirty=false, referenced=false
        todo!()
    }

    pub fn unmap_page(&mut self, page: PageNumber) {
        // TODO: Remove the page table entry for the given page
        todo!()
    }

    pub fn translate(&self, page: PageNumber) -> Option<FrameNumber> {
        // TODO: Translate a page number to a frame number
        // Return None if the page is not mapped or not valid
        todo!()
    }

    pub fn set_dirty(&mut self, page: PageNumber) {
        // TODO: Mark a page as dirty (modified)
        todo!()
    }

    pub fn set_referenced(&mut self, page: PageNumber) {
        // TODO: Mark a page as referenced (accessed)
        todo!()
    }

    pub fn is_dirty(&self, page: PageNumber) -> bool {
        // TODO: Check if a page is dirty
        todo!()
    }

    pub fn is_referenced(&self, page: PageNumber) -> bool {
        // TODO: Check if a page is referenced
        todo!()
    }
}

pub struct PagingSystem {
    page_table: PageTable,
    free_frames: Vec<FrameNumber>,
    next_frame: usize,
}

impl PagingSystem {
    pub fn new(total_frames: usize) -> Self {
        // TODO: Initialize the paging system with the given number of frames
        // All frames should initially be free
        todo!()
    }

    pub fn allocate_page(&mut self, page: PageNumber) -> Result<FrameNumber, &'static str> {
        // TODO: Allocate a free frame for the given page
        // Return an error if no free frames are available
        // Update the page table to map the page to the allocated frame
        todo!()
    }

    pub fn free_page(&mut self, page: PageNumber) -> Result<(), &'static str> {
        // TODO: Free the frame associated with the given page
        // Add the frame back to the free list
        // Unmap the page from the page table
        todo!()
    }

    pub fn translate_address(&self, virtual_addr: usize) -> Option<usize> {
        // TODO: Translate a virtual address to a physical address
        // Virtual address = page_number * PAGE_SIZE + offset
        // Physical address = frame_number * PAGE_SIZE + offset
        todo!()
    }

    pub fn free_frames_count(&self) -> usize {
        self.free_frames.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_page_table_mapping() {
        let mut pt = PageTable::new();

        pt.map_page(PageNumber(0), FrameNumber(5));
        pt.map_page(PageNumber(1), FrameNumber(10));

        assert_eq!(pt.translate(PageNumber(0)), Some(FrameNumber(5)));
        assert_eq!(pt.translate(PageNumber(1)), Some(FrameNumber(10)));
        assert_eq!(pt.translate(PageNumber(2)), None);
    }

    #[test]
    fn test_page_table_unmap() {
        let mut pt = PageTable::new();

        pt.map_page(PageNumber(0), FrameNumber(5));
        assert_eq!(pt.translate(PageNumber(0)), Some(FrameNumber(5)));

        pt.unmap_page(PageNumber(0));
        assert_eq!(pt.translate(PageNumber(0)), None);
    }

    #[test]
    fn test_dirty_and_referenced_bits() {
        let mut pt = PageTable::new();

        pt.map_page(PageNumber(0), FrameNumber(5));
        assert!(!pt.is_dirty(PageNumber(0)));
        assert!(!pt.is_referenced(PageNumber(0)));

        pt.set_dirty(PageNumber(0));
        assert!(pt.is_dirty(PageNumber(0)));

        pt.set_referenced(PageNumber(0));
        assert!(pt.is_referenced(PageNumber(0)));
    }

    #[test]
    fn test_allocate_and_free_pages() {
        let mut system = PagingSystem::new(10);

        assert_eq!(system.free_frames_count(), 10);

        let frame1 = system.allocate_page(PageNumber(0)).unwrap();
        assert_eq!(system.free_frames_count(), 9);

        let frame2 = system.allocate_page(PageNumber(1)).unwrap();
        assert_eq!(system.free_frames_count(), 8);

        system.free_page(PageNumber(0)).unwrap();
        assert_eq!(system.free_frames_count(), 9);
    }

    #[test]
    fn test_address_translation() {
        let mut system = PagingSystem::new(10);

        system.allocate_page(PageNumber(0)).unwrap();
        system.allocate_page(PageNumber(1)).unwrap();

        // Test address translation
        let virtual_addr = PAGE_SIZE + 100; // Page 1, offset 100
        let physical_addr = system.translate_address(virtual_addr);

        assert!(physical_addr.is_some());
        let physical = physical_addr.unwrap();
        assert_eq!(physical % PAGE_SIZE, 100); // Offset should be preserved
    }

    #[test]
    fn test_out_of_frames() {
        let mut system = PagingSystem::new(2);

        system.allocate_page(PageNumber(0)).unwrap();
        system.allocate_page(PageNumber(1)).unwrap();

        let result = system.allocate_page(PageNumber(2));
        assert!(result.is_err());
    }

    #[test]
    fn test_multiple_allocations() {
        let mut system = PagingSystem::new(5);

        for i in 0..5 {
            let result = system.allocate_page(PageNumber(i));
            assert!(result.is_ok());
        }

        assert_eq!(system.free_frames_count(), 0);

        system.free_page(PageNumber(2)).unwrap();
        assert_eq!(system.free_frames_count(), 1);

        let result = system.allocate_page(PageNumber(10));
        assert!(result.is_ok());
        assert_eq!(system.free_frames_count(), 0);
    }
}
