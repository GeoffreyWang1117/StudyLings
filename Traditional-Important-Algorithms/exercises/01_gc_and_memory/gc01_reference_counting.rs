// gc01_reference_counting.rs
//
// Reference Counting is a simple garbage collection technique where each object
// keeps track of how many references point to it. When the count reaches zero,
// the object can be safely deallocated.
//
// Your task: Implement a simple reference-counted smart pointer.
//
// Note: This implementation won't handle cycles - that's a known limitation!

// I AM NOT DONE

use std::ops::Deref;
use std::cell::Cell;

struct RcBox<T> {
    value: T,
    ref_count: Cell<usize>,
}

pub struct Rc<T> {
    ptr: *mut RcBox<T>,
}

impl<T> Rc<T> {
    pub fn new(value: T) -> Self {
        // TODO: Allocate a new RcBox on the heap with ref_count = 1
        // Hint: Use Box::into_raw to convert Box to raw pointer
        todo!()
    }

    pub fn clone(&self) -> Self {
        // TODO: Increment the reference count and return a new Rc pointing to the same data
        todo!()
    }

    pub fn strong_count(&self) -> usize {
        // TODO: Return the current reference count
        todo!()
    }
}

impl<T> Deref for Rc<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        // TODO: Return a reference to the inner value
        unsafe { &(*self.ptr).value }
    }
}

impl<T> Drop for Rc<T> {
    fn drop(&mut self) {
        // TODO: Decrement ref count. If it reaches 0, deallocate the RcBox
        // Hint: Use Box::from_raw to convert raw pointer back to Box for cleanup
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_reference_counting() {
        let rc1 = Rc::new(42);
        assert_eq!(rc1.strong_count(), 1);

        let rc2 = rc1.clone();
        assert_eq!(rc1.strong_count(), 2);
        assert_eq!(rc2.strong_count(), 2);

        drop(rc2);
        assert_eq!(rc1.strong_count(), 1);
    }

    #[test]
    fn test_deref() {
        let rc = Rc::new(String::from("hello"));
        assert_eq!(rc.len(), 5);
    }

    #[test]
    fn test_multiple_clones() {
        let rc1 = Rc::new(100);
        let rc2 = rc1.clone();
        let rc3 = rc1.clone();
        let rc4 = rc2.clone();

        assert_eq!(rc1.strong_count(), 4);
        assert_eq!(*rc4, 100);
    }
}
