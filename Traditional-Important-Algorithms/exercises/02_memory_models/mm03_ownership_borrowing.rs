// mm03_ownership_borrowing.rs
//
// Rust's ownership system ensures memory safety without garbage collection.
// Rules:
// 1. Each value has one owner
// 2. When owner goes out of scope, value is dropped
// 3. Can have many immutable borrows OR one mutable borrow
//
// Your task: Implement a simplified ownership system.

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ValueId(usize);

#[derive(Debug, Clone)]
pub struct Value {
    data: String,
}

pub struct OwnershipSystem {
    values: HashMap<ValueId, Value>,
    owners: HashMap<ValueId, String>,
    immutable_borrows: HashMap<ValueId, Vec<String>>,
    mutable_borrow: HashMap<ValueId, Option<String>>,
    next_id: usize,
}

impl OwnershipSystem {
    pub fn new() -> Self {
        Self {
            values: HashMap::new(),
            owners: HashMap::new(),
            immutable_borrows: HashMap::new(),
            mutable_borrow: HashMap::new(),
            next_id: 0,
        }
    }

    pub fn create_value(&mut self, owner: &str, data: String) -> ValueId {
        // TODO: Create a new value with owner
        todo!()
    }

    pub fn transfer_ownership(&mut self, value_id: ValueId, new_owner: &str) -> Result<(), &'static str> {
        // TODO: Transfer ownership from current owner to new owner
        // Clear all borrows when ownership transfers
        todo!()
    }

    pub fn borrow_immutable(&mut self, value_id: ValueId, borrower: &str) -> Result<(), &'static str> {
        // TODO: Create immutable borrow
        // Fail if there's a mutable borrow
        todo!()
    }

    pub fn borrow_mutable(&mut self, value_id: ValueId, borrower: &str) -> Result<(), &'static str> {
        // TODO: Create mutable borrow
        // Fail if there are any other borrows (mutable or immutable)
        todo!()
    }

    pub fn release_immutable_borrow(&mut self, value_id: ValueId, borrower: &str) -> Result<(), &'static str> {
        // TODO: Release an immutable borrow
        todo!()
    }

    pub fn release_mutable_borrow(&mut self, value_id: ValueId) -> Result<(), &'static str> {
        // TODO: Release the mutable borrow
        todo!()
    }

    pub fn drop_value(&mut self, value_id: ValueId) -> Result<(), &'static str> {
        // TODO: Drop value (owner must exist, no borrows can be active)
        todo!()
    }

    pub fn get_owner(&self, value_id: ValueId) -> Option<&String> {
        self.owners.get(&value_id)
    }

    pub fn has_mutable_borrow(&self, value_id: ValueId) -> bool {
        self.mutable_borrow.get(&value_id)
            .and_then(|b| b.as_ref())
            .is_some()
    }

    pub fn immutable_borrow_count(&self, value_id: ValueId) -> usize {
        self.immutable_borrows.get(&value_id)
            .map(|v| v.len())
            .unwrap_or(0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ownership_transfer() {
        let mut sys = OwnershipSystem::new();

        let val = sys.create_value("owner1", "data".to_string());
        assert_eq!(sys.get_owner(val), Some(&"owner1".to_string()));

        sys.transfer_ownership(val, "owner2").unwrap();
        assert_eq!(sys.get_owner(val), Some(&"owner2".to_string()));
    }

    #[test]
    fn test_immutable_borrows() {
        let mut sys = OwnershipSystem::new();

        let val = sys.create_value("owner", "data".to_string());

        sys.borrow_immutable(val, "borrower1").unwrap();
        sys.borrow_immutable(val, "borrower2").unwrap();

        assert_eq!(sys.immutable_borrow_count(val), 2);
    }

    #[test]
    fn test_mutable_borrow_exclusive() {
        let mut sys = OwnershipSystem::new();

        let val = sys.create_value("owner", "data".to_string());

        sys.borrow_mutable(val, "borrower1").unwrap();

        // Can't borrow immutably while mutably borrowed
        assert!(sys.borrow_immutable(val, "borrower2").is_err());

        // Can't borrow mutably while already mutably borrowed
        assert!(sys.borrow_mutable(val, "borrower3").is_err());
    }

    #[test]
    fn test_no_mutable_with_immutable() {
        let mut sys = OwnershipSystem::new();

        let val = sys.create_value("owner", "data".to_string());

        sys.borrow_immutable(val, "borrower1").unwrap();

        // Can't borrow mutably while immutably borrowed
        assert!(sys.borrow_mutable(val, "borrower2").is_err());
    }

    #[test]
    fn test_borrow_release() {
        let mut sys = OwnershipSystem::new();

        let val = sys.create_value("owner", "data".to_string());

        sys.borrow_mutable(val, "borrower").unwrap();
        sys.release_mutable_borrow(val).unwrap();

        // Can borrow again after release
        sys.borrow_immutable(val, "borrower2").unwrap();
    }

    #[test]
    fn test_drop_with_borrows() {
        let mut sys = OwnershipSystem::new();

        let val = sys.create_value("owner", "data".to_string());

        sys.borrow_immutable(val, "borrower").unwrap();

        // Can't drop while borrowed
        assert!(sys.drop_value(val).is_err());

        sys.release_immutable_borrow(val, "borrower").unwrap();

        // Can drop after releasing borrows
        assert!(sys.drop_value(val).is_ok());
    }
}
