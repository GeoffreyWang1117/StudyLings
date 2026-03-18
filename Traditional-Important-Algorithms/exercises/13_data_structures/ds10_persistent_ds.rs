// ds10_persistent_ds.rs
//
// Persistent Data Structures preserve all previous versions when modified, allowing
// access to any historical state. Unlike ephemeral data structures that destroy old
// versions on updates, persistent structures maintain a full version history.
//
// Types of Persistence:
// - Partially Persistent: Can query all versions, but only modify the latest
// - Fully Persistent: Can query and modify all versions (creates version tree)
// - Confluently Persistent: Can also merge versions
//
// Implementation Techniques:
// - Fat Nodes: Store all versions in each node (space inefficient)
// - Path Copying: Copy nodes along path to root when modifying (most common)
// - Node Copying: Only copy changed nodes, share unchanged subtrees
//
// Applications:
// - Functional programming languages
// - Version control systems
// - Undo/redo functionality
// - Concurrent data structures
// - Time-travel debugging
//
// Time Complexity (Path Copying):
// - Query: O(log n) same as regular structure
// - Update: O(log n) with additional copying overhead
// - Space: O(1) per update (only modified path is copied)
// - Version space: O(n + m*log n) for n elements and m updates
//
// Your task: Implement persistent binary search tree and persistent array using path copying.

// I AM NOT DONE

use std::fmt::Debug;
use std::rc::Rc;

// Persistent Binary Search Tree using path copying
#[derive(Debug, Clone)]
pub struct PersistentBST<T: Ord + Clone + Debug> {
    root: Option<Rc<Node<T>>>,
    size: usize,
}

#[derive(Debug, Clone)]
struct Node<T: Ord + Clone + Debug> {
    value: T,
    left: Option<Rc<Node<T>>>,
    right: Option<Rc<Node<T>>>,
}

impl<T: Ord + Clone + Debug> Node<T> {
    fn new(value: T) -> Self {
        Self {
            value,
            left: None,
            right: None,
        }
    }
}

impl<T: Ord + Clone + Debug> PersistentBST<T> {
    pub fn new() -> Self {
        Self {
            root: None,
            size: 0,
        }
    }

    pub fn insert(&self, value: T) -> PersistentBST<T> {
        // TODO: Return a new version with value inserted
        // Uses path copying: only copies nodes on path from root to insertion point
        // Unchanged subtrees are shared via Rc
        todo!()
    }

    fn insert_recursive(&self, node: Option<Rc<Node<T>>>, value: T) -> Option<Rc<Node<T>>> {
        // TODO: Recursive helper for insert with path copying
        // 1. If node is None, create new node wrapped in Rc
        // 2. If value < node.value:
        //    - Recursively insert into left subtree
        //    - Create NEW node with updated left child, keep right child (share via Rc)
        // 3. Similar for right subtree
        // 4. If value == node.value, can replace or ignore
        todo!()
    }

    pub fn delete(&self, value: &T) -> PersistentBST<T> {
        // TODO: Return a new version with value deleted
        // Uses path copying: only copies nodes on path from root to deleted node
        todo!()
    }

    fn delete_recursive(&self, node: Option<Rc<Node<T>>>, value: &T) -> Option<Rc<Node<T>>> {
        // TODO: Recursive helper for delete with path copying
        todo!()
    }

    pub fn search(&self, value: &T) -> bool {
        // TODO: Search for value (read-only, no copying needed)
        todo!()
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn inorder(&self) -> Vec<T> {
        // TODO: Return values in sorted order
        todo!()
    }

    fn inorder_helper(node: &Option<Rc<Node<T>>>, result: &mut Vec<T>) {
        // TODO: Recursive inorder traversal
        todo!()
    }
}

// Persistent Array using path copying (binary tree representation)
#[derive(Debug, Clone)]
pub struct PersistentArray<T: Clone + Debug> {
    root: Option<Rc<ArrayNode<T>>>,
    size: usize,
}

#[derive(Debug, Clone)]
struct ArrayNode<T: Clone + Debug> {
    value: T,
    left: Option<Rc<ArrayNode<T>>>,
    right: Option<Rc<ArrayNode<T>>>,
}

impl<T: Clone + Debug> PersistentArray<T> {
    pub fn new(data: Vec<T>) -> Self {
        // TODO: Build persistent array from vector
        // Use a complete binary tree representation
        // Array indices map to tree positions
        todo!()
    }

    fn build(data: &[T], start: usize, end: usize) -> Option<Rc<ArrayNode<T>>> {
        // TODO: Build tree from array range [start, end)
        todo!()
    }

    pub fn get(&self, index: usize) -> Option<T> {
        // TODO: Get value at index (read-only, no copying)
        todo!()
    }

    fn get_recursive(node: &Option<Rc<ArrayNode<T>>>, index: usize, start: usize, end: usize)
        -> Option<T> {
        // TODO: Recursive helper for get
        todo!()
    }

    pub fn set(&self, index: usize, value: T) -> PersistentArray<T> {
        // TODO: Return new version with value at index updated
        // Uses path copying
        todo!()
    }

    fn set_recursive(node: &Option<Rc<ArrayNode<T>>>, index: usize, value: T,
                      start: usize, end: usize) -> Option<Rc<ArrayNode<T>>> {
        // TODO: Recursive helper for set with path copying
        // Only copy nodes on path to updated index
        todo!()
    }

    pub fn len(&self) -> usize {
        self.size
    }
}

// Version manager for tracking multiple versions
#[derive(Debug, Clone)]
pub struct VersionManager<T: Ord + Clone + Debug> {
    versions: Vec<PersistentBST<T>>,
}

impl<T: Ord + Clone + Debug> VersionManager<T> {
    pub fn new() -> Self {
        Self {
            versions: vec![PersistentBST::new()],
        }
    }

    pub fn insert(&mut self, value: T) {
        // TODO: Insert into latest version and save new version
        todo!()
    }

    pub fn delete(&mut self, value: &T) {
        // TODO: Delete from latest version and save new version
        todo!()
    }

    pub fn get_version(&self, version: usize) -> Option<&PersistentBST<T>> {
        // TODO: Return reference to specific version
        todo!()
    }

    pub fn current_version(&self) -> usize {
        self.versions.len() - 1
    }

    pub fn num_versions(&self) -> usize {
        self.versions.len()
    }

    pub fn rollback(&mut self, version: usize) {
        // TODO: Rollback to a specific version
        // Create new version based on old version
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_persistent_bst_create() {
        let bst: PersistentBST<i32> = PersistentBST::new();
        assert_eq!(bst.size(), 0);
    }

    #[test]
    fn test_persistent_bst_insert() {
        let v0 = PersistentBST::new();
        let v1 = v0.insert(10);
        let v2 = v1.insert(5);
        let v3 = v2.insert(15);

        // All versions should be accessible
        assert_eq!(v0.size(), 0);
        assert_eq!(v1.size(), 1);
        assert_eq!(v2.size(), 2);
        assert_eq!(v3.size(), 3);

        assert!(!v0.search(&10));
        assert!(v1.search(&10));
        assert!(v2.search(&5));
        assert!(v3.search(&15));
    }

    #[test]
    fn test_persistent_bst_versions_independent() {
        let v0 = PersistentBST::new();
        let v1 = v0.insert(10);
        let v2 = v1.insert(20);
        let v3 = v1.insert(5); // Branch from v1, not v2

        // v2 and v3 should be independent
        assert!(v2.search(&20));
        assert!(!v2.search(&5));
        assert!(v3.search(&5));
        assert!(!v3.search(&20));
    }

    #[test]
    fn test_persistent_bst_delete() {
        let v0 = PersistentBST::new();
        let v1 = v0.insert(10).insert(5).insert(15);
        let v2 = v1.delete(&5);

        assert!(v1.search(&5));
        assert!(!v2.search(&5));
        assert_eq!(v1.size(), 3);
        assert_eq!(v2.size(), 2);
    }

    #[test]
    fn test_persistent_bst_inorder() {
        let bst = PersistentBST::new()
            .insert(50)
            .insert(30)
            .insert(70)
            .insert(20)
            .insert(40);

        let result = bst.inorder();
        assert_eq!(result, vec![20, 30, 40, 50, 70]);
    }

    #[test]
    fn test_persistent_array_create() {
        let arr = PersistentArray::new(vec![1, 2, 3, 4, 5]);
        assert_eq!(arr.len(), 5);
    }

    #[test]
    fn test_persistent_array_get() {
        let arr = PersistentArray::new(vec![10, 20, 30, 40, 50]);
        assert_eq!(arr.get(0), Some(10));
        assert_eq!(arr.get(2), Some(30));
        assert_eq!(arr.get(4), Some(50));
        assert_eq!(arr.get(5), None);
    }

    #[test]
    fn test_persistent_array_set() {
        let v0 = PersistentArray::new(vec![1, 2, 3, 4, 5]);
        let v1 = v0.set(2, 100);

        assert_eq!(v0.get(2), Some(3));   // Original unchanged
        assert_eq!(v1.get(2), Some(100)); // New version updated
    }

    #[test]
    fn test_persistent_array_multiple_versions() {
        let v0 = PersistentArray::new(vec![1, 2, 3]);
        let v1 = v0.set(0, 10);
        let v2 = v1.set(1, 20);
        let v3 = v0.set(2, 30); // Branch from v0

        assert_eq!(v0.get(0), Some(1));
        assert_eq!(v1.get(0), Some(10));
        assert_eq!(v2.get(1), Some(20));
        assert_eq!(v3.get(2), Some(30));
        assert_eq!(v3.get(0), Some(1)); // v3 branched from v0, not v1
    }

    #[test]
    fn test_version_manager() {
        let mut vm = VersionManager::new();

        vm.insert(10);
        vm.insert(20);
        vm.insert(30);

        assert_eq!(vm.num_versions(), 4); // Initial empty + 3 inserts

        let v2 = vm.get_version(2).unwrap();
        assert!(v2.search(&10));
        assert!(v2.search(&20));
        assert!(!v2.search(&30)); // Not yet in version 2
    }

    #[test]
    fn test_version_manager_rollback() {
        let mut vm = VersionManager::new();

        vm.insert(10);
        vm.insert(20);
        vm.insert(30);

        let before_rollback = vm.current_version();
        vm.rollback(1); // Rollback to version 1 (only has 10)

        let current = vm.get_version(vm.current_version()).unwrap();
        assert!(current.search(&10));
        assert!(!current.search(&20));
        assert!(!current.search(&30));
    }

    #[test]
    fn test_version_manager_delete() {
        let mut vm = VersionManager::new();

        vm.insert(10);
        vm.insert(20);
        vm.delete(&10);

        let current = vm.get_version(vm.current_version()).unwrap();
        assert!(!current.search(&10));
        assert!(current.search(&20));

        // Old version still has 10
        let v1 = vm.get_version(1).unwrap();
        assert!(v1.search(&10));
    }
}
