// os02_segmentation.rs
//
// Segmentation is a memory management scheme that supports the user's view of memory.
// A program is a collection of segments such as main program, procedures, functions,
// stack, symbol table, arrays, etc. Each segment has a name and a length.
//
// Your task: Implement a segmentation system with a segment table for address translation.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct SegmentId(usize);

#[derive(Debug, Clone, Copy)]
pub struct SegmentTableEntry {
    base: usize,    // Base address in physical memory
    limit: usize,   // Length of the segment
    valid: bool,
    readable: bool,
    writable: bool,
    executable: bool,
}

pub struct SegmentTable {
    entries: HashMap<SegmentId, SegmentTableEntry>,
}

impl SegmentTable {
    pub fn new() -> Self {
        Self {
            entries: HashMap::new(),
        }
    }

    pub fn add_segment(
        &mut self,
        id: SegmentId,
        base: usize,
        limit: usize,
        readable: bool,
        writable: bool,
        executable: bool,
    ) {
        // TODO: Add a new segment to the segment table
        todo!()
    }

    pub fn remove_segment(&mut self, id: SegmentId) {
        // TODO: Remove a segment from the segment table
        todo!()
    }

    pub fn translate(
        &self,
        segment: SegmentId,
        offset: usize,
    ) -> Result<usize, &'static str> {
        // TODO: Translate a logical address (segment, offset) to a physical address
        // 1. Check if segment is valid
        // 2. Check if offset is within the segment limit
        // 3. Return base + offset
        todo!()
    }

    pub fn check_permission(
        &self,
        segment: SegmentId,
        read: bool,
        write: bool,
        execute: bool,
    ) -> bool {
        // TODO: Check if the requested operations are allowed on the segment
        todo!()
    }

    pub fn get_segment_size(&self, segment: SegmentId) -> Option<usize> {
        // TODO: Return the size (limit) of the segment
        todo!()
    }
}

pub struct SegmentationSystem {
    segment_table: SegmentTable,
    next_base: usize,
    memory_size: usize,
}

impl SegmentationSystem {
    pub fn new(memory_size: usize) -> Self {
        Self {
            segment_table: SegmentTable::new(),
            next_base: 0,
            memory_size,
        }
    }

    pub fn allocate_segment(
        &mut self,
        id: SegmentId,
        size: usize,
        readable: bool,
        writable: bool,
        executable: bool,
    ) -> Result<(), &'static str> {
        // TODO: Allocate a new segment
        // 1. Check if there's enough free space
        // 2. Add segment to the table with the current next_base
        // 3. Update next_base
        todo!()
    }

    pub fn free_segment(&mut self, id: SegmentId) -> Result<(), &'static str> {
        // TODO: Free a segment
        // Note: This simple implementation doesn't compact memory,
        // so it won't reduce next_base
        todo!()
    }

    pub fn translate_address(
        &self,
        segment: SegmentId,
        offset: usize,
    ) -> Result<usize, &'static str> {
        self.segment_table.translate(segment, offset)
    }

    pub fn check_access(
        &self,
        segment: SegmentId,
        offset: usize,
        read: bool,
        write: bool,
        execute: bool,
    ) -> Result<usize, &'static str> {
        // TODO: Check permissions and translate address
        // 1. Check if the operation is permitted on the segment
        // 2. Translate the address
        // Return the physical address if everything is valid
        todo!()
    }

    pub fn free_space(&self) -> usize {
        // TODO: Calculate remaining free space
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_segment_table() {
        let mut st = SegmentTable::new();

        st.add_segment(SegmentId(0), 1000, 500, true, true, false);
        st.add_segment(SegmentId(1), 2000, 1000, true, false, true);

        assert_eq!(st.translate(SegmentId(0), 100), Ok(1100));
        assert_eq!(st.translate(SegmentId(1), 500), Ok(2500));
    }

    #[test]
    fn test_segment_limit_violation() {
        let mut st = SegmentTable::new();

        st.add_segment(SegmentId(0), 1000, 500, true, true, false);

        // Offset exceeds segment limit
        assert!(st.translate(SegmentId(0), 600).is_err());
    }

    #[test]
    fn test_invalid_segment() {
        let st = SegmentTable::new();

        // Segment doesn't exist
        assert!(st.translate(SegmentId(0), 100).is_err());
    }

    #[test]
    fn test_permissions() {
        let mut st = SegmentTable::new();

        st.add_segment(SegmentId(0), 1000, 500, true, false, false); // Read-only

        assert!(st.check_permission(SegmentId(0), true, false, false));
        assert!(!st.check_permission(SegmentId(0), false, true, false));
    }

    #[test]
    fn test_allocate_segments() {
        let mut system = SegmentationSystem::new(10000);

        assert_eq!(system.free_space(), 10000);

        system
            .allocate_segment(SegmentId(0), 1000, true, true, false)
            .unwrap();
        assert_eq!(system.free_space(), 9000);

        system
            .allocate_segment(SegmentId(1), 2000, true, false, true)
            .unwrap();
        assert_eq!(system.free_space(), 7000);
    }

    #[test]
    fn test_out_of_memory() {
        let mut system = SegmentationSystem::new(1000);

        system
            .allocate_segment(SegmentId(0), 800, true, true, false)
            .unwrap();

        let result = system.allocate_segment(SegmentId(1), 300, true, true, false);
        assert!(result.is_err());
    }

    #[test]
    fn test_free_segment() {
        let mut system = SegmentationSystem::new(10000);

        system
            .allocate_segment(SegmentId(0), 1000, true, true, false)
            .unwrap();
        system
            .allocate_segment(SegmentId(1), 2000, true, true, false)
            .unwrap();

        system.free_segment(SegmentId(0)).unwrap();

        // Segment should not be accessible after freeing
        assert!(system.translate_address(SegmentId(0), 100).is_err());
    }

    #[test]
    fn test_access_control() {
        let mut system = SegmentationSystem::new(10000);

        system
            .allocate_segment(SegmentId(0), 1000, true, false, false)
            .unwrap();

        // Read should succeed
        assert!(system.check_access(SegmentId(0), 100, true, false, false).is_ok());

        // Write should fail
        assert!(system.check_access(SegmentId(0), 100, false, true, false).is_err());
    }

    #[test]
    fn test_multiple_segments() {
        let mut system = SegmentationSystem::new(10000);

        // Code segment
        system
            .allocate_segment(SegmentId(0), 2000, true, false, true)
            .unwrap();

        // Data segment
        system
            .allocate_segment(SegmentId(1), 3000, true, true, false)
            .unwrap();

        // Stack segment
        system
            .allocate_segment(SegmentId(2), 1000, true, true, false)
            .unwrap();

        let code_addr = system.translate_address(SegmentId(0), 500).unwrap();
        let data_addr = system.translate_address(SegmentId(1), 1000).unwrap();
        let stack_addr = system.translate_address(SegmentId(2), 100).unwrap();

        // All segments should have different base addresses
        assert!(code_addr < data_addr);
        assert!(data_addr < stack_addr);
    }
}
