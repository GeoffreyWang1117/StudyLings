// gc09_region_allocation.rs
//
// Region-based allocation (also called Arena allocation) allocates objects
// in regions/arenas. Entire regions are freed at once, making individual
// deallocations unnecessary.
//
// Your task: Implement a region-based memory allocator.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct RegionId(usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ObjectId(usize);

struct Region {
    id: RegionId,
    objects: Vec<ObjectId>,
    size: usize,
}

pub struct RegionAllocator {
    regions: HashMap<RegionId, Region>,
    objects: HashMap<ObjectId, Vec<u8>>,
    next_region_id: usize,
    next_object_id: usize,
    current_region: Option<RegionId>,
}

impl RegionAllocator {
    pub fn new() -> Self {
        Self {
            regions: HashMap::new(),
            objects: HashMap::new(),
            next_region_id: 0,
            next_object_id: 0,
            current_region: None,
        }
    }

    pub fn create_region(&mut self) -> RegionId {
        // TODO: Create a new region and make it current
        todo!()
    }

    pub fn allocate(&mut self, data: Vec<u8>) -> Result<ObjectId, &'static str> {
        // TODO: Allocate an object in the current region
        // Return error if no current region
        todo!()
    }

    pub fn free_region(&mut self, region_id: RegionId) {
        // TODO: Free all objects in the region and remove the region
        todo!()
    }

    pub fn switch_region(&mut self, region_id: RegionId) -> Result<(), &'static str> {
        // TODO: Switch to a different region
        // Return error if region doesn't exist
        todo!()
    }

    pub fn region_size(&self, region_id: RegionId) -> Option<usize> {
        // TODO: Return total size of objects in region
        self.regions.get(&region_id).map(|r| r.size)
    }

    pub fn region_object_count(&self, region_id: RegionId) -> Option<usize> {
        // TODO: Return number of objects in region
        self.regions.get(&region_id).map(|r| r.objects.len())
    }

    pub fn total_objects(&self) -> usize {
        self.objects.len()
    }

    pub fn total_regions(&self) -> usize {
        self.regions.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_region_creation() {
        let mut allocator = RegionAllocator::new();

        let region1 = allocator.create_region();
        let region2 = allocator.create_region();

        assert_eq!(allocator.total_regions(), 2);
        assert_ne!(region1, region2);
    }

    #[test]
    fn test_allocation_in_region() {
        let mut allocator = RegionAllocator::new();

        let region = allocator.create_region();

        let obj1 = allocator.allocate(vec![1, 2, 3]).unwrap();
        let obj2 = allocator.allocate(vec![4, 5, 6]).unwrap();

        assert_eq!(allocator.region_object_count(region), Some(2));
        assert_eq!(allocator.total_objects(), 2);
    }

    #[test]
    fn test_free_region() {
        let mut allocator = RegionAllocator::new();

        let region = allocator.create_region();

        allocator.allocate(vec![1, 2, 3]).unwrap();
        allocator.allocate(vec![4, 5, 6]).unwrap();

        assert_eq!(allocator.total_objects(), 2);

        allocator.free_region(region);

        assert_eq!(allocator.total_objects(), 0);
        assert_eq!(allocator.total_regions(), 0);
    }

    #[test]
    fn test_multiple_regions() {
        let mut allocator = RegionAllocator::new();

        let region1 = allocator.create_region();
        allocator.allocate(vec![1]).unwrap();

        let region2 = allocator.create_region();
        allocator.allocate(vec![2]).unwrap();
        allocator.allocate(vec![3]).unwrap();

        assert_eq!(allocator.region_object_count(region1), Some(1));
        assert_eq!(allocator.region_object_count(region2), Some(2));

        allocator.free_region(region1);

        assert_eq!(allocator.total_objects(), 2);
        assert_eq!(allocator.total_regions(), 1);
    }
}
