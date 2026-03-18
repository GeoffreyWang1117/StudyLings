// rate04_fixed_window.rs
//
// Fixed Window Counter is a simple rate limiting algorithm that divides time
// into fixed windows and counts requests per window.
//
// How it works:
// - Time is divided into fixed-size windows (e.g., every minute starts at :00)
// - Each window has a counter starting at 0
// - When request arrives, check if in current window and increment counter
// - If counter exceeds limit, reject request
// - Counter resets at window boundary
//
// Your task: Implement a fixed window counter rate limiter.
//
// Key concepts:
// - Window boundary calculation
// - Counter reset on window change
// - Simple but allows burst at window edges
// - Trade-off: simplicity vs accuracy

// I AM NOT DONE

use std::time::{Duration, Instant};

pub struct FixedWindowCounter {
    max_requests: usize,      // Maximum requests per window
    window_duration: Duration, // Duration of each window
    current_count: usize,     // Requests in current window
    window_start: Instant,    // Start time of current window
}

impl FixedWindowCounter {
    pub fn new(max_requests: usize, window_duration: Duration) -> Self {
        // TODO: Initialize a new fixed window counter
        // - Set window_start to current time
        // - Set current_count to 0
        todo!()
    }

    fn check_and_reset_window(&mut self, now: Instant) {
        // TODO: Check if we've moved to a new window and reset if needed
        // - Calculate time elapsed since window_start
        // - If elapsed >= window_duration:
        //   - Calculate how many complete windows have passed
        //   - Update window_start to start of current window
        //   - Reset current_count to 0
        todo!()
    }

    pub fn try_acquire(&mut self) -> bool {
        // TODO: Try to acquire a request slot
        // - Get current time
        // - Check and reset window if needed
        // - If current_count < max_requests:
        //   - Increment current_count
        //   - Return true
        // - Otherwise return false
        todo!()
    }

    pub fn current_count(&mut self) -> usize {
        // TODO: Return current request count in window
        // - Check and reset window first
        // - Return current_count
        todo!()
    }

    pub fn remaining_capacity(&mut self) -> usize {
        // TODO: Return remaining request slots in current window
        // - Return max_requests - current_count()
        todo!()
    }

    pub fn time_until_reset(&mut self) -> Duration {
        // TODO: Return time until current window resets
        // - Get current time
        // - Calculate window_end = window_start + window_duration
        // - Return window_end - now
        // - If result is negative or zero, return Duration::ZERO
        todo!()
    }

    pub fn reset(&mut self) {
        // TODO: Manually reset the counter to start a new window
        // - Set window_start to current time
        // - Set current_count to 0
        todo!()
    }

    pub fn window_start_time(&self) -> Instant {
        // TODO: Return the start time of current window
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread::sleep;

    #[test]
    fn test_fixed_window_creation() {
        let mut limiter = FixedWindowCounter::new(10, Duration::from_secs(1));
        assert_eq!(limiter.current_count(), 0);
        assert_eq!(limiter.remaining_capacity(), 10);
    }

    #[test]
    fn test_acquire_requests() {
        let mut limiter = FixedWindowCounter::new(5, Duration::from_secs(1));

        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());

        assert_eq!(limiter.current_count(), 3);
        assert_eq!(limiter.remaining_capacity(), 2);
    }

    #[test]
    fn test_max_requests_limit() {
        let mut limiter = FixedWindowCounter::new(3, Duration::from_secs(1));

        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
        assert!(!limiter.try_acquire()); // Should be rejected

        assert_eq!(limiter.current_count(), 3);
        assert_eq!(limiter.remaining_capacity(), 0);
    }

    #[test]
    fn test_window_reset() {
        let mut limiter = FixedWindowCounter::new(2, Duration::from_millis(500));

        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
        assert!(!limiter.try_acquire()); // Full

        sleep(Duration::from_millis(600)); // Wait for window to reset

        // New window, should be able to acquire again
        assert_eq!(limiter.current_count(), 0);
        assert!(limiter.try_acquire());
        assert!(limiter.try_acquire());
    }

    #[test]
    fn test_time_until_reset() {
        let limiter = FixedWindowCounter::new(5, Duration::from_secs(1));

        let time_until = limiter.time_until_reset();

        // Should be approximately 1 second (just created)
        assert!(time_until.as_millis() >= 900 && time_until.as_millis() <= 1100);
    }

    #[test]
    fn test_time_until_reset_decreases() {
        let mut limiter = FixedWindowCounter::new(5, Duration::from_millis(1000));

        sleep(Duration::from_millis(300));

        let time_until = limiter.time_until_reset();

        // Should be approximately 700ms remaining
        assert!(time_until.as_millis() >= 600 && time_until.as_millis() <= 800);
    }

    #[test]
    fn test_manual_reset() {
        let mut limiter = FixedWindowCounter::new(3, Duration::from_secs(10));

        limiter.try_acquire();
        limiter.try_acquire();
        limiter.try_acquire();

        assert_eq!(limiter.current_count(), 3);

        limiter.reset();

        assert_eq!(limiter.current_count(), 0);
        assert!(limiter.try_acquire()); // Can acquire again
    }

    #[test]
    fn test_burst_at_window_edge() {
        let mut limiter = FixedWindowCounter::new(5, Duration::from_millis(200));

        // Fill current window
        for _ in 0..5 {
            assert!(limiter.try_acquire());
        }

        sleep(Duration::from_millis(250)); // New window

        // Can burst again
        for _ in 0..5 {
            assert!(limiter.try_acquire());
        }

        assert_eq!(limiter.current_count(), 5);
    }

    #[test]
    fn test_multiple_window_transitions() {
        let mut limiter = FixedWindowCounter::new(2, Duration::from_millis(300));

        // Window 1
        limiter.try_acquire();
        limiter.try_acquire();

        sleep(Duration::from_millis(350)); // Window 2

        assert_eq!(limiter.current_count(), 0);
        limiter.try_acquire();

        sleep(Duration::from_millis(350)); // Window 3

        assert_eq!(limiter.current_count(), 0);
        limiter.try_acquire();
        limiter.try_acquire();
    }

    #[test]
    fn test_partial_window_usage() {
        let mut limiter = FixedWindowCounter::new(10, Duration::from_secs(1));

        limiter.try_acquire();
        limiter.try_acquire();
        limiter.try_acquire();

        sleep(Duration::from_millis(500)); // Still in same window

        assert_eq!(limiter.current_count(), 3); // Count preserved
        assert!(limiter.try_acquire());
    }

    #[test]
    fn test_rapid_requests_in_window() {
        let mut limiter = FixedWindowCounter::new(100, Duration::from_secs(1));

        let mut accepted = 0;
        for _ in 0..150 {
            if limiter.try_acquire() {
                accepted += 1;
            }
        }

        assert_eq!(accepted, 100);
        assert_eq!(limiter.current_count(), 100);
    }

    #[test]
    fn test_window_start_time() {
        let limiter = FixedWindowCounter::new(5, Duration::from_secs(1));
        let start = limiter.window_start_time();
        let now = Instant::now();

        // Window start should be very close to now
        let diff = now.duration_since(start);
        assert!(diff.as_millis() < 10);
    }

    #[test]
    fn test_zero_count_after_reset() {
        let mut limiter = FixedWindowCounter::new(3, Duration::from_millis(100));

        limiter.try_acquire();
        sleep(Duration::from_millis(150));

        // After window reset, checking count should show 0
        assert_eq!(limiter.current_count(), 0);
    }
}
