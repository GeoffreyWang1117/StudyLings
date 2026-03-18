// rate03_sliding_window.rs
//
// Sliding Window Rate Limiter provides precise rate limiting by tracking
// requests in a rolling time window. More accurate than fixed windows.
//
// How it works:
// - Maintains timestamps of all requests in current window
// - Window slides with each new request
// - Removes requests older than window duration
// - Rejects requests if count exceeds limit
//
// Your task: Implement a sliding window rate limiter.
//
// Key concepts:
// - Rolling time window
// - Request timestamp tracking
// - Automatic cleanup of old requests
// - Precise rate limiting

// I AM NOT DONE

use std::collections::VecDeque;
use std::time::{Duration, Instant};

pub struct SlidingWindowRateLimiter {
    max_requests: usize,         // Maximum requests per window
    window_duration: Duration,   // Time window duration
    requests: VecDeque<Instant>, // Timestamps of requests in current window
}

impl SlidingWindowRateLimiter {
    pub fn new(max_requests: usize, window_duration: Duration) -> Self {
        // TODO: Initialize a new sliding window rate limiter
        // - Create empty request queue
        todo!()
    }

    fn cleanup_old_requests(&mut self, now: Instant) {
        // TODO: Remove requests outside the current window
        // - Calculate window start: now - window_duration
        // - Remove all requests from front of queue older than window start
        // - Use a loop with pop_front() while condition is true
        todo!()
    }

    pub fn try_acquire(&mut self) -> bool {
        // TODO: Try to acquire a slot for a new request
        // - Get current time
        // - Cleanup old requests
        // - Check if current count < max_requests
        // - If yes, add current time to queue and return true
        // - If no, return false
        todo!()
    }

    pub fn current_count(&mut self) -> usize {
        // TODO: Return current number of requests in window
        // - Cleanup old requests first
        // - Return queue length
        todo!()
    }

    pub fn remaining_capacity(&mut self) -> usize {
        // TODO: Return number of available request slots
        // - Return max_requests - current_count()
        todo!()
    }

    pub fn time_until_next_slot(&mut self) -> Option<Duration> {
        // TODO: Calculate time until a slot becomes available
        // - Cleanup old requests first
        // - If capacity available, return None
        // - Otherwise, calculate when oldest request will expire
        // - Return time until that expiration
        todo!()
    }

    pub fn reset(&mut self) {
        // TODO: Clear all requests from the window
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread::sleep;

    #[test]
    fn test_sliding_window_creation() {
        let mut limiter = SlidingWindowRateLimiter::new(10, Duration::from_secs(1));
        assert_eq!(limiter.current_count(), 0);
        assert_eq!(limiter.remaining_capacity(), 10);
    }

    #[test]
    fn test_acquire_requests() {
        let mut limiter = SlidingWindowRateLimiter::new(5, Duration::from_secs(1));

        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());

        assert_eq!(limiter.current_count(), 3);
        assert_eq!(limiter.remaining_capacity(), 2);
    }

    #[test]
    fn test_max_requests_limit() {
        let mut limiter = SlidingWindowRateLimiter::new(3, Duration::from_secs(1));

        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
        assert!(!limiter.try_acquire()); // Should be rejected

        assert_eq!(limiter.current_count(), 3);
        assert_eq!(limiter.remaining_capacity(), 0);
    }

    #[test]
    fn test_window_sliding() {
        let mut limiter = SlidingWindowRateLimiter::new(2, Duration::from_millis(500));

        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
        assert!(!limiter.try_acquire()); // Full

        sleep(Duration::from_millis(600)); // Wait for window to pass

        // Window has slid, old requests should be gone
        assert_eq!(limiter.current_count(), 0);
        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
    }

    #[test]
    fn test_partial_window_cleanup() {
        let mut limiter = SlidingWindowRateLimiter::new(5, Duration::from_secs(1));

        // Add 3 requests
        limiter.try_acquire();
        sleep(Duration::from_millis(100));
        limiter.try_acquire();
        sleep(Duration::from_millis(100));
        limiter.try_acquire();

        sleep(Duration::from_millis(900)); // First request should expire

        // Should have approximately 2 requests left
        let count = limiter.current_count();
        assert!(count >= 1 && count <= 2);
    }

    #[test]
    fn test_time_until_next_slot() {
        let mut limiter = SlidingWindowRateLimiter::new(2, Duration::from_millis(1000));

        limiter.try_acquire();
        sleep(Duration::from_millis(100));
        limiter.try_acquire();

        // Limiter is full
        let wait_time = limiter.time_until_next_slot();
        assert!(wait_time.is_some());

        // Should wait approximately 900ms (until first request expires)
        let duration = wait_time.unwrap();
        assert!(duration.as_millis() >= 800 && duration.as_millis() <= 1000);
    }

    #[test]
    fn test_time_until_next_slot_when_available() {
        let mut limiter = SlidingWindowRateLimiter::new(5, Duration::from_secs(1));

        limiter.try_acquire();
        limiter.try_acquire();

        let wait_time = limiter.time_until_next_slot();
        assert_eq!(wait_time, None); // Capacity still available
    }

    #[test]
    fn test_reset() {
        let mut limiter = SlidingWindowRateLimiter::new(3, Duration::from_secs(10));

        limiter.try_acquire();
        limiter.try_acquire();
        limiter.try_acquire();

        assert_eq!(limiter.current_count(), 3);

        limiter.reset();

        assert_eq!(limiter.current_count(), 0);
        assert!(limiter.try_acquire()); // Can acquire again
    }

    #[test]
    fn test_burst_handling() {
        let mut limiter = SlidingWindowRateLimiter::new(10, Duration::from_millis(500));

        // Try to acquire 15 requests rapidly
        let mut accepted = 0;
        let mut rejected = 0;

        for _ in 0..15 {
            if limiter.try_acquire() {
                accepted += 1;
            } else {
                rejected += 1;
            }
        }

        assert_eq!(accepted, 10);
        assert_eq!(rejected, 5);
    }

    #[test]
    fn test_sustained_rate() {
        let mut limiter = SlidingWindowRateLimiter::new(5, Duration::from_millis(500));

        // First batch
        for _ in 0..5 {
            limiter.try_acquire();
        }
        assert!(!limiter.try_acquire());

        sleep(Duration::from_millis(600));

        // Second batch after window slides
        for _ in 0..5 {
            assert!(limiter.try_acquire());
        }
        assert!(!limiter.try_acquire());
    }

    #[test]
    fn test_gradual_window_sliding() {
        let mut limiter = SlidingWindowRateLimiter::new(3, Duration::from_millis(300));

        limiter.try_acquire();
        sleep(Duration::from_millis(100));
        limiter.try_acquire();
        sleep(Duration::from_millis(100));
        limiter.try_acquire();

        assert!(!limiter.try_acquire()); // Full

        sleep(Duration::from_millis(120)); // First request should expire

        assert!(limiter.try_acquire()); // Should succeed now
    }

    #[test]
    fn test_empty_limiter() {
        let mut limiter = SlidingWindowRateLimiter::new(5, Duration::from_secs(1));

        assert_eq!(limiter.current_count(), 0);
        assert_eq!(limiter.remaining_capacity(), 5);
        assert_eq!(limiter.time_until_next_slot(), None);
    }

    #[test]
    fn test_precise_rate_limiting() {
        let mut limiter = SlidingWindowRateLimiter::new(10, Duration::from_secs(1));

        // Fill limiter
        for _ in 0..10 {
            assert!(limiter.try_acquire());
        }

        // Wait exactly half window
        sleep(Duration::from_millis(500));

        // Should still be full (all requests still in window)
        assert!(!limiter.try_acquire());

        // Wait for window to fully pass
        sleep(Duration::from_millis(600));

        // Now should be able to acquire
        assert!(limiter.try_acquire());
    }
}
