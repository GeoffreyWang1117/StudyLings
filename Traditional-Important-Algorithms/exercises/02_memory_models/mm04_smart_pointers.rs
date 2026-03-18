// mm04_smart_pointers.rs
//
// Smart pointers provide automatic memory management through RAII.
// Common types: Box<T>, Rc<T>, Arc<T>, RefCell<T>
//
// Your task: Implement simplified versions of smart pointers.

// I AM NOT DONE

use std::ops::Deref;
use std::cell::Cell;

// Simple Box implementation
pub struct SimpleBox<T> {
    ptr: *mut T,
}

impl<T> SimpleBox<T> {
    pub fn new(value: T) -> Self {
        // TODO: Allocate value on heap and store raw pointer
        todo!()
    }
}

impl<T> Deref for SimpleBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        // TODO: Return reference to heap value
        todo!()
    }
}

impl<T> Drop for SimpleBox<T> {
    fn drop(&mut self) {
        // TODO: Deallocate heap memory
        todo!()
    }
}

// Simple Rc implementation (single-threaded reference counting)
pub struct SimpleRc<T> {
    ptr: *mut RcBox<T>,
}

struct RcBox<T> {
    value: T,
    ref_count: Cell<usize>,
}

impl<T> SimpleRc<T> {
    pub fn new(value: T) -> Self {
        // TODO: Create new Rc with ref_count = 1
        todo!()
    }

    pub fn clone(&self) -> Self {
        // TODO: Increment ref count and return new Rc
        todo!()
    }

    pub fn strong_count(&self) -> usize {
        // TODO: Return current reference count
        todo!()
    }
}

impl<T> Deref for SimpleRc<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        unsafe { &(*self.ptr).value }
    }
}

impl<T> Drop for SimpleRc<T> {
    fn drop(&mut self) {
        // TODO: Decrement ref count, deallocate if zero
        todo!()
    }
}

// Simple RefCell implementation (interior mutability)
use std::cell::UnsafeCell;

pub struct SimpleRefCell<T> {
    value: UnsafeCell<T>,
    borrow_state: Cell<isize>, // >0: immutable borrows, -1: mutable borrow, 0: no borrows
}

pub struct Ref<'a, T> {
    value: &'a T,
    borrow_state: &'a Cell<isize>,
}

pub struct RefMut<'a, T> {
    value: &'a mut T,
    borrow_state: &'a Cell<isize>,
}

impl<T> SimpleRefCell<T> {
    pub fn new(value: T) -> Self {
        Self {
            value: UnsafeCell::new(value),
            borrow_state: Cell::new(0),
        }
    }

    pub fn borrow(&self) -> Result<Ref<T>, &'static str> {
        // TODO: Create immutable borrow
        // Fail if mutably borrowed
        todo!()
    }

    pub fn borrow_mut(&self) -> Result<RefMut<T>, &'static str> {
        // TODO: Create mutable borrow
        // Fail if any borrows exist
        todo!()
    }
}

impl<'a, T> Drop for Ref<'a, T> {
    fn drop(&mut self) {
        // TODO: Decrement borrow count
        todo!()
    }
}

impl<'a, T> Drop for RefMut<'a, T> {
    fn drop(&mut self) {
        // TODO: Reset borrow state
        todo!()
    }
}

impl<'a, T> Deref for Ref<'a, T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        self.value
    }
}

impl<'a, T> Deref for RefMut<'a, T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        self.value
    }
}

impl<'a, T> std::ops::DerefMut for RefMut<'a, T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        self.value
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_box() {
        let b = SimpleBox::new(42);
        assert_eq!(*b, 42);
    }

    #[test]
    fn test_simple_rc() {
        let rc1 = SimpleRc::new(100);
        assert_eq!(rc1.strong_count(), 1);

        let rc2 = rc1.clone();
        assert_eq!(rc1.strong_count(), 2);
        assert_eq!(rc2.strong_count(), 2);

        drop(rc2);
        assert_eq!(rc1.strong_count(), 1);
    }

    #[test]
    fn test_refcell_immutable() {
        let cell = SimpleRefCell::new(42);

        let b1 = cell.borrow().unwrap();
        let b2 = cell.borrow().unwrap();

        assert_eq!(*b1, 42);
        assert_eq!(*b2, 42);
    }

    #[test]
    fn test_refcell_mutable() {
        let cell = SimpleRefCell::new(42);

        {
            let mut b = cell.borrow_mut().unwrap();
            *b = 100;
        }

        let b = cell.borrow().unwrap();
        assert_eq!(*b, 100);
    }

    #[test]
    fn test_refcell_borrow_rules() {
        let cell = SimpleRefCell::new(42);

        let _b1 = cell.borrow().unwrap();

        // Can't borrow mutably while immutably borrowed
        assert!(cell.borrow_mut().is_err());
    }

    #[test]
    fn test_refcell_mut_exclusive() {
        let cell = SimpleRefCell::new(42);

        let _b1 = cell.borrow_mut().unwrap();

        // Can't borrow while mutably borrowed
        assert!(cell.borrow().is_err());
        assert!(cell.borrow_mut().is_err());
    }
}
