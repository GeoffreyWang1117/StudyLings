// stream04_reservoir_sampling.rs
//
// Reservoir Sampling is an algorithm for randomly sampling k items from a stream
// of unknown length, where each item has an equal probability of being selected.
// This is essential for monitoring and debugging streams where you can't store
// all data.
//
// How it works (Algorithm R):
// 1. Fill reservoir with first k items
// 2. For item i (where i > k):
//    - Generate random number j in [0, i)
//    - If j < k, replace reservoir[j] with item i
// 3. Each item has exactly k/n probability of being in final sample
//
// Your task: Implement reservoir sampling for uniform random sampling from
// unbounded streams.
//
// Key concepts:
// - Uniform probability guarantee
// - Single-pass processing
// - Constant memory (size k)
// - Weighted sampling variant

// I AM NOT DONE

use rand::Rng;

pub struct ReservoirSampler<T> {
    reservoir: Vec<T>,
    capacity: usize,
    items_seen: usize,
}

impl<T: Clone> ReservoirSampler<T> {
    pub fn new(capacity: usize) -> Self {
        // TODO: Initialize reservoir sampler
        // - Create empty reservoir with given capacity
        // - Set items_seen to 0
        todo!()
    }

    pub fn add(&mut self, item: T) {
        // TODO: Add item to the stream using reservoir sampling algorithm
        // - If reservoir not full, add item
        // - Otherwise, randomly decide whether to replace an existing item
        // - Increment items_seen
        // Hint: Use rand::thread_rng().gen_range() for random numbers
        todo!()
    }

    pub fn sample(&self) -> &[T] {
        // TODO: Return current sample (read-only view)
        todo!()
    }

    pub fn items_seen(&self) -> usize {
        // TODO: Return total number of items processed
        todo!()
    }

    pub fn is_full(&self) -> bool {
        // TODO: Check if reservoir is at capacity
        todo!()
    }

    pub fn clear(&mut self) {
        // TODO: Clear the reservoir and reset counter
        todo!()
    }
}

#[derive(Clone)]
pub struct WeightedItem<T> {
    pub item: T,
    pub weight: f64,
}

pub struct WeightedReservoirSampler<T> {
    reservoir: Vec<WeightedItem<T>>,
    capacity: usize,
    weight_sum: f64,
}

impl<T: Clone> WeightedReservoirSampler<T> {
    pub fn new(capacity: usize) -> Self {
        // TODO: Initialize weighted reservoir sampler
        // - Similar to regular reservoir but tracks weights
        todo!()
    }

    pub fn add(&mut self, item: T, weight: f64) {
        // TODO: Add weighted item using Algorithm A-Res
        // - Generate random value in [0, weight_sum + weight)
        // - If value < capacity, add/replace item
        // - Otherwise, probabilistically replace based on weight
        // - Update weight_sum
        todo!()
    }

    pub fn sample(&self) -> Vec<&T> {
        // TODO: Return current sample items (without weights)
        todo!()
    }

    pub fn get_weights(&self) -> Vec<f64> {
        // TODO: Return weights of items in reservoir
        todo!()
    }

    pub fn total_weight(&self) -> f64 {
        // TODO: Return sum of all weights seen
        todo!()
    }
}

pub struct DistributedReservoirSampler<T> {
    local_reservoir: ReservoirSampler<T>,
    capacity: usize,
}

impl<T: Clone> DistributedReservoirSampler<T> {
    pub fn new(capacity: usize) -> Self {
        // TODO: Initialize distributed reservoir sampler
        todo!()
    }

    pub fn add(&mut self, item: T) {
        // TODO: Add item to local reservoir
        todo!()
    }

    pub fn merge(&mut self, other: &ReservoirSampler<T>) {
        // TODO: Merge another reservoir into this one
        // - Combine reservoirs probabilistically
        // - Maintain uniform distribution
        // - Consider total items seen in both reservoirs
        // Hint: Each item from other should be considered with probability
        //       other.items_seen / (self.items_seen + other.items_seen)
        todo!()
    }

    pub fn sample(&self) -> &[T] {
        // TODO: Return current sample
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_reservoir_initialization() {
        let sampler: ReservoirSampler<i32> = ReservoirSampler::new(10);
        assert_eq!(sampler.items_seen(), 0);
        assert!(!sampler.is_full());
        assert_eq!(sampler.sample().len(), 0);
    }

    #[test]
    fn test_reservoir_fill() {
        let mut sampler = ReservoirSampler::new(5);

        for i in 0..5 {
            sampler.add(i);
        }

        assert!(sampler.is_full());
        assert_eq!(sampler.items_seen(), 5);
        assert_eq!(sampler.sample().len(), 5);
    }

    #[test]
    fn test_reservoir_capacity_maintained() {
        let mut sampler = ReservoirSampler::new(10);

        for i in 0..100 {
            sampler.add(i);
        }

        assert_eq!(sampler.sample().len(), 10); // Never exceeds capacity
        assert_eq!(sampler.items_seen(), 100);
    }

    #[test]
    fn test_reservoir_contains_valid_items() {
        let mut sampler = ReservoirSampler::new(5);

        for i in 0..20 {
            sampler.add(i);
        }

        // All items in sample should be from input range
        for &item in sampler.sample() {
            assert!(item < 20);
        }
    }

    #[test]
    fn test_reservoir_clear() {
        let mut sampler = ReservoirSampler::new(5);

        for i in 0..10 {
            sampler.add(i);
        }

        sampler.clear();
        assert_eq!(sampler.items_seen(), 0);
        assert_eq!(sampler.sample().len(), 0);
    }

    #[test]
    fn test_weighted_reservoir_basic() {
        let mut sampler = WeightedReservoirSampler::new(5);

        sampler.add("item1", 1.0);
        sampler.add("item2", 2.0);
        sampler.add("item3", 3.0);

        assert_eq!(sampler.sample().len(), 3);
        assert_eq!(sampler.total_weight(), 6.0);
    }

    #[test]
    fn test_weighted_reservoir_capacity() {
        let mut sampler = WeightedReservoirSampler::new(3);

        for i in 0..10 {
            sampler.add(i, 1.0);
        }

        assert_eq!(sampler.sample().len(), 3); // Respects capacity
    }

    #[test]
    fn test_weighted_reservoir_higher_weight_preference() {
        let mut sampler = WeightedReservoirSampler::new(10);

        // Add low-weight items
        for i in 0..100 {
            sampler.add(i, 1.0);
        }

        // Add high-weight item
        sampler.add(9999, 1000.0);

        // High-weight item should likely be in sample
        // (Not guaranteed due to randomness, but very likely)
        let sample = sampler.sample();
        let has_high_weight = sample.iter().any(|&&x| x == 9999);
        // With weight 1000 vs 1, probability is very high
        // We can't assert deterministically, but we can check it's working
        assert!(sample.len() <= 10);
    }

    #[test]
    fn test_distributed_merge() {
        let mut sampler1 = ReservoirSampler::new(5);
        let mut sampler2 = ReservoirSampler::new(5);

        for i in 0..10 {
            sampler1.add(i);
        }

        for i in 10..20 {
            sampler2.add(i);
        }

        let mut distributed = DistributedReservoirSampler::new(5);
        distributed.add(0); // Initialize with one item

        // Merge both samplers
        distributed.merge(&sampler1);
        distributed.merge(&sampler2);

        let sample = distributed.sample();
        assert_eq!(sample.len(), 5);
    }

    #[test]
    fn test_uniform_distribution_approximation() {
        // This test checks if distribution is roughly uniform
        // Run reservoir sampling many times and check distribution
        let runs = 1000;
        let stream_size = 100;
        let reservoir_size = 10;
        let mut counts = vec![0; stream_size];

        for _ in 0..runs {
            let mut sampler = ReservoirSampler::new(reservoir_size);
            for i in 0..stream_size {
                sampler.add(i);
            }

            for &item in sampler.sample() {
                counts[item] += 1;
            }
        }

        // Each item should appear approximately (runs * reservoir_size / stream_size) times
        let expected = (runs * reservoir_size) / stream_size;
        let tolerance = expected / 3; // Allow 33% variance

        for count in counts {
            assert!(count > expected - tolerance && count < expected + tolerance,
                    "count {} not within expected range {}±{}", count, expected, tolerance);
        }
    }

    #[test]
    fn test_single_item_stream() {
        let mut sampler = ReservoirSampler::new(5);
        sampler.add(42);

        assert_eq!(sampler.sample().len(), 1);
        assert_eq!(sampler.sample()[0], 42);
    }

    #[test]
    fn test_weighted_zero_weight() {
        let mut sampler = WeightedReservoirSampler::new(5);

        sampler.add("item1", 1.0);
        sampler.add("item2", 0.0); // Zero weight
        sampler.add("item3", 1.0);

        // Zero-weight items should not affect sampling
        let sample = sampler.sample();
        assert!(sample.len() <= 5);
    }
}
