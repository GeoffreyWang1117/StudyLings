// rate05_circuit_breaker.rs
//
// Circuit Breaker is a fault tolerance pattern that prevents cascading failures
// by stopping requests to a failing service and allowing it time to recover.
//
// States:
// - Closed: Normal operation, requests pass through
// - Open: Service failing, requests rejected immediately (fail fast)
// - Half-Open: Testing recovery, limited requests allowed
//
// Your task: Implement a circuit breaker with three states.
//
// Key concepts:
// - State transitions based on failure/success thresholds
// - Timeout for recovery attempts
// - Failure tracking in sliding window
// - Fail-fast behavior

// I AM NOT DONE

use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum CircuitState {
    Closed,    // Normal operation
    Open,      // Failing, rejecting requests
    HalfOpen,  // Testing recovery
}

#[derive(Debug, Clone, Copy)]
struct RequestResult {
    success: bool,
    timestamp: Instant,
}

pub struct CircuitBreaker {
    state: CircuitState,
    failure_threshold: usize,    // Failures needed to open circuit
    success_threshold: usize,    // Successes needed to close from half-open
    timeout: Duration,           // Time to wait before half-open
    window_size: usize,          // Number of recent requests to track

    recent_results: Vec<RequestResult>,
    opened_at: Option<Instant>,
    half_open_successes: usize,
}

impl CircuitBreaker {
    pub fn new(
        failure_threshold: usize,
        success_threshold: usize,
        timeout: Duration,
        window_size: usize,
    ) -> Self {
        // TODO: Initialize circuit breaker in Closed state
        todo!()
    }

    fn count_recent_failures(&self) -> usize {
        // TODO: Count failures in the recent window
        // - Iterate through recent_results
        // - Count how many have success = false
        // - Only consider up to window_size most recent results
        todo!()
    }

    fn should_transition_to_half_open(&self) -> bool {
        // TODO: Check if enough time has passed to try half-open
        // - Return true if state is Open and timeout has elapsed since opened_at
        // - Otherwise return false
        todo!()
    }

    fn update_state(&mut self) {
        // TODO: Update circuit state based on current conditions
        //
        // Logic:
        // 1. If state is Open and should_transition_to_half_open:
        //    - Set state to HalfOpen
        //    - Reset half_open_successes to 0
        //
        // 2. If state is Closed and count_recent_failures >= failure_threshold:
        //    - Set state to Open
        //    - Set opened_at to current time
        //
        // 3. If state is HalfOpen and half_open_successes >= success_threshold:
        //    - Set state to Closed
        //    - Clear recent_results
        todo!()
    }

    pub fn call<F, T, E>(&mut self, operation: F) -> Result<T, CircuitBreakerError<E>>
    where
        F: FnOnce() -> Result<T, E>,
    {
        // TODO: Execute operation with circuit breaker protection
        //
        // 1. Update state first
        // 2. If state is Open, return Err(CircuitBreakerError::Open)
        // 3. Execute operation
        // 4. Record result:
        //    - Add to recent_results (keep only last window_size entries)
        //    - If HalfOpen and success, increment half_open_successes
        //    - If HalfOpen and failure, set state to Open with new timeout
        // 5. Update state again
        // 6. Return result (wrapped in CircuitBreakerError::Inner if error)
        todo!()
    }

    pub fn state(&mut self) -> CircuitState {
        // TODO: Return current state (update state first)
        todo!()
    }

    pub fn failure_count(&self) -> usize {
        // TODO: Return count of recent failures
        todo!()
    }

    pub fn success_rate(&self) -> f64 {
        // TODO: Calculate success rate from recent results
        // - If no results, return 1.0 (100%)
        // - Otherwise: successes / total_results
        // - Only consider last window_size results
        todo!()
    }

    pub fn reset(&mut self) {
        // TODO: Reset circuit breaker to initial Closed state
        // - Clear recent_results
        // - Set state to Closed
        // - Reset counters
        todo!()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum CircuitBreakerError<E> {
    Open,       // Circuit is open, request rejected
    Inner(E),   // Underlying operation failed
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_circuit_breaker_creation() {
        let mut cb = CircuitBreaker::new(3, 2, Duration::from_secs(1), 10);
        assert_eq!(cb.state(), CircuitState::Closed);
    }

    #[test]
    fn test_successful_calls_stay_closed() {
        let mut cb = CircuitBreaker::new(3, 2, Duration::from_secs(1), 10);

        for _ in 0..10 {
            let result = cb.call(|| Ok::<_, ()>(42));
            assert_eq!(result, Ok(42));
        }

        assert_eq!(cb.state(), CircuitState::Closed);
    }

    #[test]
    fn test_failures_open_circuit() {
        let mut cb = CircuitBreaker::new(3, 2, Duration::from_millis(100), 10);

        // First 2 failures don't open circuit
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        assert_eq!(cb.state(), CircuitState::Closed);

        // Third failure opens circuit
        cb.call(|| Err::<(), _>("error")).ok();
        assert_eq!(cb.state(), CircuitState::Open);
    }

    #[test]
    fn test_open_circuit_rejects_requests() {
        let mut cb = CircuitBreaker::new(2, 2, Duration::from_secs(1), 10);

        // Open the circuit
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        assert_eq!(cb.state(), CircuitState::Open);

        // Next request should be rejected without calling operation
        let result = cb.call(|| Ok::<_, ()>(42));
        assert_eq!(result, Err(CircuitBreakerError::Open));
    }

    #[test]
    fn test_transition_to_half_open() {
        let mut cb = CircuitBreaker::new(2, 2, Duration::from_millis(100), 10);

        // Open circuit
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        assert_eq!(cb.state(), CircuitState::Open);

        // Wait for timeout
        std::thread::sleep(Duration::from_millis(150));

        // Should transition to half-open on next state check
        assert_eq!(cb.state(), CircuitState::HalfOpen);
    }

    #[test]
    fn test_half_open_success_closes_circuit() {
        let mut cb = CircuitBreaker::new(2, 2, Duration::from_millis(100), 10);

        // Open circuit
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Err::<(), _>("error")).ok();

        // Wait and transition to half-open
        std::thread::sleep(Duration::from_millis(150));
        cb.state();

        assert_eq!(cb.state(), CircuitState::HalfOpen);

        // Successful calls should close circuit
        cb.call(|| Ok::<_, ()>(1)).ok();
        cb.call(|| Ok::<_, ()>(2)).ok();

        assert_eq!(cb.state(), CircuitState::Closed);
    }

    #[test]
    fn test_half_open_failure_reopens_circuit() {
        let mut cb = CircuitBreaker::new(2, 2, Duration::from_millis(100), 10);

        // Open circuit
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Err::<(), _>("error")).ok();

        // Wait and transition to half-open
        std::thread::sleep(Duration::from_millis(150));
        cb.state();

        assert_eq!(cb.state(), CircuitState::HalfOpen);

        // Failure in half-open should reopen circuit
        cb.call(|| Err::<(), _>("error")).ok();

        assert_eq!(cb.state(), CircuitState::Open);
    }

    #[test]
    fn test_failure_count() {
        let mut cb = CircuitBreaker::new(5, 2, Duration::from_secs(1), 10);

        cb.call(|| Ok::<_, ()>(1)).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Ok::<_, ()>(2)).ok();

        assert_eq!(cb.failure_count(), 2);
    }

    #[test]
    fn test_success_rate() {
        let mut cb = CircuitBreaker::new(5, 2, Duration::from_secs(1), 10);

        cb.call(|| Ok::<_, ()>(1)).ok();
        cb.call(|| Ok::<_, ()>(2)).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Ok::<_, ()>(3)).ok();

        // 3 successes out of 4 = 75%
        assert!((cb.success_rate() - 0.75).abs() < 0.01);
    }

    #[test]
    fn test_window_size_limit() {
        let mut cb = CircuitBreaker::new(5, 2, Duration::from_secs(1), 3);

        // Add more results than window size
        for _ in 0..5 {
            cb.call(|| Ok::<_, ()>(1)).ok();
        }

        cb.call(|| Err::<(), _>("error")).ok();

        // Should only count failure in window of last 3 requests
        assert_eq!(cb.failure_count(), 1);
    }

    #[test]
    fn test_reset() {
        let mut cb = CircuitBreaker::new(2, 2, Duration::from_secs(1), 10);

        // Open circuit
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        assert_eq!(cb.state(), CircuitState::Open);

        // Reset
        cb.reset();

        assert_eq!(cb.state(), CircuitState::Closed);
        assert_eq!(cb.failure_count(), 0);
    }

    #[test]
    fn test_mixed_results() {
        let mut cb = CircuitBreaker::new(3, 2, Duration::from_secs(1), 10);

        cb.call(|| Ok::<_, ()>(1)).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Ok::<_, ()>(2)).ok();
        cb.call(|| Err::<(), _>("error")).ok();
        cb.call(|| Ok::<_, ()>(3)).ok();

        // Only 2 failures, should still be closed
        assert_eq!(cb.state(), CircuitState::Closed);
        assert_eq!(cb.failure_count(), 2);
    }

    #[test]
    fn test_error_propagation() {
        let mut cb = CircuitBreaker::new(5, 2, Duration::from_secs(1), 10);

        let result = cb.call(|| Err::<(), _>("custom error"));
        assert_eq!(result, Err(CircuitBreakerError::Inner("custom error")));
    }
}
