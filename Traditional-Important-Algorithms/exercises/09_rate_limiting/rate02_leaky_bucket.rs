// rate02_leaky_bucket.rs
//
// Leaky Bucket is a rate limiting algorithm that enforces a constant output rate
// regardless of input bursts. It's similar to token bucket but processes requests
// at a fixed rate.
//
// How it works:
// - Requests enter a queue (bucket)
// - Requests are processed at a constant rate (leak rate)
// - If bucket is full, new requests are rejected
// - Smooths out bursts to maintain steady flow
//
// Your task: Implement a leaky bucket rate limiter.
//
// Key concepts:
// - Queue-based request handling
// - Fixed processing rate
// - Bucket overflow protection
// - Time-based request processing

// I AM NOT DONE

use std::collections::VecDeque;
use std::time::{Duration, Instant};

#[derive(Debug, Clone)]
pub struct Request {
    pub id: usize,
    pub timestamp: Instant,
}

pub struct LeakyBucket {
    capacity: usize,              // Maximum requests in bucket
    leak_rate: f64,               // Requests processed per second
    queue: VecDeque<Request>,     // Queued requests
    last_leak: Instant,           // Last time bucket leaked
}

impl LeakyBucket {
    pub fn new(capacity: usize, leak_rate: f64) -> Self {
        // TODO: Initialize a new leaky bucket
        // - Create empty queue
        // - Set last_leak to current time
        todo!()
    }

    fn leak(&mut self) {
        // TODO: Process (remove) requests based on time elapsed
        // - Calculate elapsed time since last_leak
        // - Calculate requests to process: elapsed_seconds * leak_rate
        // - Remove that many requests from front of queue
        // - Update last_leak to current time
        // - Don't remove more requests than available
        todo!()
    }

    pub fn try_add(&mut self, request: Request) -> bool {
        // TODO: Try to add a request to the bucket
        // - First call leak() to process pending requests
        // - Check if queue is at capacity
        // - If yes, return false (bucket full)
        // - If no, add request to back of queue and return true
        todo!()
    }

    pub fn current_size(&mut self) -> usize {
        // TODO: Return current number of requests in bucket
        // - Call leak() first to update queue
        // - Return queue length
        todo!()
    }

    pub fn is_full(&mut self) -> bool {
        // TODO: Check if bucket is at capacity
        // - Call leak() first to update queue
        // - Return true if queue length >= capacity
        todo!()
    }

    pub fn pending_requests(&mut self) -> Vec<Request> {
        // TODO: Return a copy of all pending requests
        // - Call leak() first
        // - Return cloned requests from queue
        todo!()
    }

    pub fn time_until_space(&mut self) -> Option<Duration> {
        // TODO: Calculate time until there's space for a new request
        // - Call leak() first
        // - If not full, return None
        // - Calculate time to leak one request: 1.0 / leak_rate seconds
        // - Return Some(duration)
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread::sleep;

    #[test]
    fn test_leaky_bucket_creation() {
        let mut bucket = LeakyBucket::new(10, 5.0);
        assert_eq!(bucket.current_size(), 0);
        assert!(!bucket.is_full());
    }

    #[test]
    fn test_add_requests() {
        let mut bucket = LeakyBucket::new(5, 2.0);
        let req1 = Request { id: 1, timestamp: Instant::now() };
        let req2 = Request { id: 2, timestamp: Instant::now() };

        assert!(bucket.try_add(req1));
        assert!(bucket.try_add(req2));
        assert_eq!(bucket.current_size(), 2);
    }

    #[test]
    fn test_bucket_full() {
        let mut bucket = LeakyBucket::new(3, 1.0);

        for i in 0..3 {
            let req = Request { id: i, timestamp: Instant::now() };
            assert!(bucket.try_add(req));
        }

        assert!(bucket.is_full());

        let req = Request { id: 99, timestamp: Instant::now() };
        assert!(!bucket.try_add(req)); // Should be rejected
    }

    #[test]
    fn test_leak_over_time() {
        let mut bucket = LeakyBucket::new(10, 10.0); // 10 requests per second

        // Add 10 requests
        for i in 0..10 {
            let req = Request { id: i, timestamp: Instant::now() };
            bucket.try_add(req);
        }

        assert_eq!(bucket.current_size(), 10);

        sleep(Duration::from_millis(500)); // Wait 0.5 seconds

        // Should have leaked approximately 5 requests (10/sec * 0.5 sec)
        let size = bucket.current_size();
        assert!(size >= 4 && size <= 6);
    }

    #[test]
    fn test_leak_all_requests() {
        let mut bucket = LeakyBucket::new(5, 5.0); // 5 requests per second

        for i in 0..5 {
            let req = Request { id: i, timestamp: Instant::now() };
            bucket.try_add(req);
        }

        sleep(Duration::from_secs(2)); // Wait 2 seconds (more than needed)

        assert_eq!(bucket.current_size(), 0); // All leaked
    }

    #[test]
    fn test_add_after_leak() {
        let mut bucket = LeakyBucket::new(3, 10.0);

        // Fill bucket
        for i in 0..3 {
            let req = Request { id: i, timestamp: Instant::now() };
            bucket.try_add(req);
        }

        assert!(bucket.is_full());

        sleep(Duration::from_millis(200)); // Leak approximately 2 requests

        // Should have space now
        let req = Request { id: 99, timestamp: Instant::now() };
        assert!(bucket.try_add(req));
    }

    #[test]
    fn test_pending_requests() {
        let mut bucket = LeakyBucket::new(5, 1.0);

        for i in 0..3 {
            let req = Request { id: i, timestamp: Instant::now() };
            bucket.try_add(req);
        }

        let pending = bucket.pending_requests();
        assert_eq!(pending.len(), 3);
        assert_eq!(pending[0].id, 0);
        assert_eq!(pending[1].id, 1);
        assert_eq!(pending[2].id, 2);
    }

    #[test]
    fn test_time_until_space() {
        let mut bucket = LeakyBucket::new(2, 5.0); // 5 requests per second

        // Fill bucket
        for i in 0..2 {
            let req = Request { id: i, timestamp: Instant::now() };
            bucket.try_add(req);
        }

        let wait_time = bucket.time_until_space();
        assert!(wait_time.is_some());

        // Should wait approximately 0.2 seconds (1 / 5 requests per second)
        let duration = wait_time.unwrap();
        assert!(duration.as_secs_f64() >= 0.15 && duration.as_secs_f64() <= 0.25);
    }

    #[test]
    fn test_time_until_space_when_not_full() {
        let mut bucket = LeakyBucket::new(5, 2.0);

        let req = Request { id: 1, timestamp: Instant::now() };
        bucket.try_add(req);

        let wait_time = bucket.time_until_space();
        assert_eq!(wait_time, None); // Not full, no wait needed
    }

    #[test]
    fn test_constant_leak_rate() {
        let mut bucket = LeakyBucket::new(20, 4.0); // 4 requests per second

        // Fill bucket
        for i in 0..20 {
            let req = Request { id: i, timestamp: Instant::now() };
            bucket.try_add(req);
        }

        sleep(Duration::from_millis(500)); // 0.5 seconds

        let size1 = bucket.current_size();
        // Should have leaked ~2 requests

        sleep(Duration::from_millis(500)); // Another 0.5 seconds

        let size2 = bucket.current_size();
        // Should have leaked ~2 more requests

        let leaked1 = 20 - size1;
        let leaked2 = size1 - size2;

        // Both should be approximately 2 (allowing for timing variance)
        assert!(leaked1 >= 1 && leaked1 <= 3);
        assert!(leaked2 >= 1 && leaked2 <= 3);
    }

    #[test]
    fn test_rapid_add_attempts() {
        let mut bucket = LeakyBucket::new(3, 1.0);

        let mut accepted = 0;
        let mut rejected = 0;

        for i in 0..10 {
            let req = Request { id: i, timestamp: Instant::now() };
            if bucket.try_add(req) {
                accepted += 1;
            } else {
                rejected += 1;
            }
        }

        assert_eq!(accepted, 3); // Only capacity worth accepted
        assert_eq!(rejected, 7); // Rest rejected
    }

    #[test]
    fn test_empty_bucket_operations() {
        let mut bucket = LeakyBucket::new(5, 2.0);

        assert_eq!(bucket.current_size(), 0);
        assert!(!bucket.is_full());
        assert_eq!(bucket.pending_requests().len(), 0);
        assert_eq!(bucket.time_until_space(), None);
    }
}
