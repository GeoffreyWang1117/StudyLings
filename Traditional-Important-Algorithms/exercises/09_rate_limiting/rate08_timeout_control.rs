// rate08_timeout_control.rs
//
// Timeout Control is a fault tolerance pattern that prevents operations from
// hanging indefinitely by enforcing time limits.
//
// How it works:
// - Set maximum duration for operation
// - Monitor execution time
// - Cancel/abort if timeout exceeded
// - Prevent resource exhaustion from slow operations
//
// Your task: Implement timeout control with cancellation.
//
// Key concepts:
// - Time-bounded execution
// - Graceful cancellation
// - Timeout detection
// - Resource cleanup

// I AM NOT DONE

use std::time::{Duration, Instant};
use std::thread;
use std::sync::{Arc, Mutex, mpsc};

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TimeoutResult<T> {
    Completed(T),
    TimedOut,
}

pub struct TimeoutController {
    default_timeout: Duration,
}

impl TimeoutController {
    pub fn new(default_timeout: Duration) -> Self {
        // TODO: Initialize timeout controller with default timeout
        todo!()
    }

    pub fn execute_with_timeout<F, T>(
        &self,
        timeout: Duration,
        operation: F,
    ) -> TimeoutResult<T>
    where
        F: FnOnce() -> T + Send + 'static,
        T: Send + 'static,
    {
        // TODO: Execute operation with timeout
        //
        // Strategy using channels:
        // 1. Create a channel for receiving result
        // 2. Spawn thread to execute operation and send result
        // 3. Use recv_timeout on channel with timeout duration
        // 4. If recv succeeds before timeout, return Completed(result)
        // 5. If recv times out, return TimedOut
        //
        // Note: This is a simplified implementation. In real systems,
        // you'd want cooperative cancellation or task-based approaches.
        todo!()
    }

    pub fn execute<F, T>(&self, operation: F) -> TimeoutResult<T>
    where
        F: FnOnce() -> T + Send + 'static,
        T: Send + 'static,
    {
        // TODO: Execute operation with default timeout
        // - Call execute_with_timeout with self.default_timeout
        todo!()
    }

    pub fn get_default_timeout(&self) -> Duration {
        // TODO: Return default timeout duration
        todo!()
    }
}

// Adaptive timeout that learns from execution history
pub struct AdaptiveTimeout {
    min_timeout: Duration,
    max_timeout: Duration,
    current_timeout: Duration,
    recent_durations: Vec<Duration>,
    window_size: usize,
}

impl AdaptiveTimeout {
    pub fn new(min_timeout: Duration, max_timeout: Duration, window_size: usize) -> Self {
        // TODO: Initialize adaptive timeout
        // - Set current_timeout to min_timeout
        // - Create empty recent_durations vector
        todo!()
    }

    pub fn record_duration(&mut self, duration: Duration) {
        // TODO: Record execution duration
        // - Add duration to recent_durations
        // - Keep only last window_size entries
        // - Update current_timeout based on statistics:
        //   - Calculate average or percentile (e.g., p95)
        //   - Add some buffer (e.g., 1.5x average)
        //   - Clamp between min_timeout and max_timeout
        todo!()
    }

    pub fn get_timeout(&self) -> Duration {
        // TODO: Return current timeout value
        todo!()
    }

    pub fn average_duration(&self) -> Option<Duration> {
        // TODO: Calculate average of recent durations
        // - Return None if no durations recorded
        // - Otherwise calculate and return average
        todo!()
    }

    pub fn reset(&mut self) {
        // TODO: Reset to initial state
        // - Clear recent_durations
        // - Reset current_timeout to min_timeout
        todo!()
    }
}

// Helper to measure execution time
pub fn measure_execution<F, T>(operation: F) -> (T, Duration)
where
    F: FnOnce() -> T,
{
    // TODO: Execute operation and measure duration
    // - Record start time
    // - Execute operation
    // - Calculate elapsed time
    // - Return (result, duration)
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_timeout_controller_creation() {
        let controller = TimeoutController::new(Duration::from_secs(1));
        assert_eq!(controller.get_default_timeout(), Duration::from_secs(1));
    }

    #[test]
    fn test_operation_completes_before_timeout() {
        let controller = TimeoutController::new(Duration::from_secs(1));

        let result = controller.execute_with_timeout(
            Duration::from_millis(500),
            || {
                thread::sleep(Duration::from_millis(100));
                42
            },
        );

        assert_eq!(result, TimeoutResult::Completed(42));
    }

    #[test]
    fn test_operation_times_out() {
        let controller = TimeoutController::new(Duration::from_secs(1));

        let result = controller.execute_with_timeout(
            Duration::from_millis(100),
            || {
                thread::sleep(Duration::from_millis(500));
                42
            },
        );

        assert_eq!(result, TimeoutResult::TimedOut);
    }

    #[test]
    fn test_execute_with_default_timeout() {
        let controller = TimeoutController::new(Duration::from_millis(200));

        let result = controller.execute(|| {
            thread::sleep(Duration::from_millis(50));
            "done"
        });

        assert_eq!(result, TimeoutResult::Completed("done"));
    }

    #[test]
    fn test_fast_operation() {
        let controller = TimeoutController::new(Duration::from_secs(1));

        let result = controller.execute_with_timeout(
            Duration::from_secs(1),
            || 123,
        );

        assert_eq!(result, TimeoutResult::Completed(123));
    }

    #[test]
    fn test_adaptive_timeout_creation() {
        let adaptive = AdaptiveTimeout::new(
            Duration::from_millis(100),
            Duration::from_secs(5),
            10,
        );

        assert_eq!(adaptive.get_timeout(), Duration::from_millis(100));
        assert_eq!(adaptive.average_duration(), None);
    }

    #[test]
    fn test_adaptive_timeout_learning() {
        let mut adaptive = AdaptiveTimeout::new(
            Duration::from_millis(100),
            Duration::from_secs(5),
            5,
        );

        // Record some durations
        adaptive.record_duration(Duration::from_millis(200));
        adaptive.record_duration(Duration::from_millis(250));
        adaptive.record_duration(Duration::from_millis(300));

        // Timeout should increase based on observed durations
        let timeout = adaptive.get_timeout();
        assert!(timeout > Duration::from_millis(100));
    }

    #[test]
    fn test_adaptive_timeout_bounds() {
        let mut adaptive = AdaptiveTimeout::new(
            Duration::from_millis(100),
            Duration::from_millis(500),
            5,
        );

        // Record very long durations
        for _ in 0..5 {
            adaptive.record_duration(Duration::from_secs(10));
        }

        // Should be capped at max_timeout
        assert_eq!(adaptive.get_timeout(), Duration::from_millis(500));
    }

    #[test]
    fn test_adaptive_timeout_window() {
        let mut adaptive = AdaptiveTimeout::new(
            Duration::from_millis(100),
            Duration::from_secs(10),
            3,
        );

        // Add more than window_size durations
        adaptive.record_duration(Duration::from_millis(100));
        adaptive.record_duration(Duration::from_millis(200));
        adaptive.record_duration(Duration::from_millis(300));
        adaptive.record_duration(Duration::from_millis(400));
        adaptive.record_duration(Duration::from_millis(500));

        let avg = adaptive.average_duration().unwrap();

        // Should only consider last 3 durations: 300, 400, 500
        // Average = 400ms
        assert!(avg >= Duration::from_millis(380) && avg <= Duration::from_millis(420));
    }

    #[test]
    fn test_adaptive_timeout_reset() {
        let mut adaptive = AdaptiveTimeout::new(
            Duration::from_millis(100),
            Duration::from_secs(5),
            5,
        );

        adaptive.record_duration(Duration::from_millis(500));
        adaptive.record_duration(Duration::from_millis(600));

        adaptive.reset();

        assert_eq!(adaptive.get_timeout(), Duration::from_millis(100));
        assert_eq!(adaptive.average_duration(), None);
    }

    #[test]
    fn test_measure_execution() {
        let (result, duration) = measure_execution(|| {
            thread::sleep(Duration::from_millis(100));
            42
        });

        assert_eq!(result, 42);
        assert!(duration >= Duration::from_millis(90));
        assert!(duration <= Duration::from_millis(200));
    }

    #[test]
    fn test_multiple_timeouts() {
        let controller = TimeoutController::new(Duration::from_secs(1));

        let r1 = controller.execute_with_timeout(
            Duration::from_millis(100),
            || {
                thread::sleep(Duration::from_millis(10));
                1
            },
        );

        let r2 = controller.execute_with_timeout(
            Duration::from_millis(100),
            || {
                thread::sleep(Duration::from_millis(10));
                2
            },
        );

        assert_eq!(r1, TimeoutResult::Completed(1));
        assert_eq!(r2, TimeoutResult::Completed(2));
    }

    #[test]
    fn test_zero_timeout() {
        let controller = TimeoutController::new(Duration::from_secs(1));

        let result = controller.execute_with_timeout(
            Duration::from_millis(0),
            || 42,
        );

        // Zero timeout should immediately timeout
        assert_eq!(result, TimeoutResult::TimedOut);
    }
}
