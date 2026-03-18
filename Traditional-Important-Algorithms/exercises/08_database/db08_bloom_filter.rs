// db08_bloom_filter.rs
//
// Bloom Filter is a space-efficient probabilistic data structure used to test
// whether an element is a member of a set. It can have false positives but
// never false negatives.
//
// Key properties:
// - Space efficient: Uses bit array + hash functions
// - Fast: O(k) for insert and query (k = number of hash functions)
// - Probabilistic: May return false positives, never false negatives
// - Immutable size: Bit array size fixed at creation
//
// Used in databases to:
// - Avoid expensive disk lookups for non-existent keys
// - Cache invalidation
// - Reduce unnecessary network requests
//
// Your task: Implement a Bloom filter with configurable size and hash functions.

// I AM NOT DONE

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

pub struct BloomFilter {
    bit_array: Vec<bool>,
    num_hash_functions: usize,
    size: usize,
}

impl BloomFilter {
    pub fn new(size: usize, num_hash_functions: usize) -> Self {
        // TODO: Create a new Bloom filter
        // Initialize bit array with all false values
        // Store the number of hash functions
        todo!()
    }

    pub fn insert<T: Hash>(&mut self, item: &T) {
        // TODO: Insert an item into the Bloom filter
        // Calculate k hash values for the item
        // Set the corresponding bits in the bit array
        todo!()
    }

    pub fn contains<T: Hash>(&self, item: &T) -> bool {
        // TODO: Check if an item might be in the set
        // Calculate k hash values for the item
        // Check if all corresponding bits are set
        // Return true if all bits are set, false otherwise
        todo!()
    }

    fn hash<T: Hash>(&self, item: &T, seed: usize) -> usize {
        // TODO: Generate a hash value for the item with a seed
        // Use the seed to generate different hash values
        // Return hash % size to get bit index
        todo!()
    }

    pub fn estimated_false_positive_rate(&self) -> f64 {
        // TODO: Calculate the estimated false positive rate
        // Formula: (1 - e^(-k*n/m))^k
        // where k = num hash functions, n = items inserted, m = bit array size
        // For now, count the number of set bits
        let set_bits = self.bit_array.iter().filter(|&&b| b).count();
        (set_bits as f64) / (self.size as f64)
    }

    pub fn clear(&mut self) {
        // TODO: Clear the Bloom filter
        // Reset all bits to false
        todo!()
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn num_bits_set(&self) -> usize {
        self.bit_array.iter().filter(|&&b| b).count()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_bloom_filter() {
        let bf = BloomFilter::new(1000, 3);
        assert_eq!(bf.size(), 1000);
        assert_eq!(bf.num_bits_set(), 0);
    }

    #[test]
    fn test_insert_and_contains() {
        let mut bf = BloomFilter::new(1000, 3);
        bf.insert(&"hello");
        bf.insert(&"world");

        assert!(bf.contains(&"hello"));
        assert!(bf.contains(&"world"));
    }

    #[test]
    fn test_no_false_negatives() {
        let mut bf = BloomFilter::new(1000, 3);
        let items = vec!["apple", "banana", "cherry", "date", "elderberry"];

        for item in &items {
            bf.insert(item);
        }

        for item in &items {
            assert!(bf.contains(item), "False negative for {}", item);
        }
    }

    #[test]
    fn test_probable_absence() {
        let mut bf = BloomFilter::new(1000, 3);
        bf.insert(&"hello");

        // These items were never inserted, so contains should return false
        // (with high probability for a well-sized filter)
        assert!(!bf.contains(&"goodbye") || true); // May have false positive
    }

    #[test]
    fn test_clear() {
        let mut bf = BloomFilter::new(1000, 3);
        bf.insert(&"hello");
        bf.insert(&"world");

        assert!(bf.num_bits_set() > 0);

        bf.clear();
        assert_eq!(bf.num_bits_set(), 0);
        assert!(!bf.contains(&"hello"));
    }

    #[test]
    fn test_different_types() {
        let mut bf = BloomFilter::new(1000, 3);

        bf.insert(&42);
        bf.insert(&"string");
        bf.insert(&vec![1, 2, 3]);

        assert!(bf.contains(&42));
        assert!(bf.contains(&"string"));
        assert!(bf.contains(&vec![1, 2, 3]));
    }

    #[test]
    fn test_bits_set_increases_with_inserts() {
        let mut bf = BloomFilter::new(1000, 3);

        let initial_bits = bf.num_bits_set();
        bf.insert(&"item1");
        let after_one = bf.num_bits_set();
        bf.insert(&"item2");
        let after_two = bf.num_bits_set();

        assert!(after_one >= initial_bits);
        assert!(after_two >= after_one);
    }

    #[test]
    fn test_false_positive_rate_increases_with_items() {
        let mut bf = BloomFilter::new(100, 3);

        let rate_empty = bf.estimated_false_positive_rate();

        for i in 0..50 {
            bf.insert(&i);
        }

        let rate_half_full = bf.estimated_false_positive_rate();

        assert!(rate_half_full > rate_empty);
    }

    #[test]
    fn test_multiple_hash_functions() {
        let mut bf1 = BloomFilter::new(1000, 1);
        let mut bf2 = BloomFilter::new(1000, 5);

        bf1.insert(&"test");
        bf2.insert(&"test");

        // More hash functions means more bits set
        assert!(bf2.num_bits_set() >= bf1.num_bits_set());
    }

    #[test]
    fn test_large_dataset() {
        let mut bf = BloomFilter::new(10000, 4);

        for i in 0..1000 {
            bf.insert(&i);
        }

        // All inserted items should be found
        for i in 0..1000 {
            assert!(bf.contains(&i));
        }
    }

    #[test]
    fn test_string_elements() {
        let mut bf = BloomFilter::new(1000, 3);
        let words = vec!["apple", "banana", "cherry", "date"];

        for word in &words {
            bf.insert(word);
        }

        for word in &words {
            assert!(bf.contains(word));
        }

        assert!(!bf.contains(&"zebra") || true); // May have false positive
    }

    #[test]
    fn test_optimal_size() {
        // Test that filter works with different sizes
        let sizes = vec![100, 1000, 10000];

        for size in sizes {
            let mut bf = BloomFilter::new(size, 3);
            bf.insert(&"test");
            assert!(bf.contains(&"test"));
        }
    }
}
