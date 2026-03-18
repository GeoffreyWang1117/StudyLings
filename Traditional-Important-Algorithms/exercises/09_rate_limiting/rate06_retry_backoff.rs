// rate06_retry_backoff.rs
//
// Exponential Backoff is a retry strategy that progressively increases wait time
// between retries to avoid overwhelming a failing service.
//
// How it works:
// - First retry after short delay (e.g., 100ms)
// - Each subsequent retry doubles the delay (exponential growth)
// - Optional jitter adds randomness to prevent thundering herd
// - Maximum retry limit and maximum backoff cap
//
// Your task: Implement exponential backoff retry strategy.
//
// Key concepts:
// - Exponential delay growth
// - Jitter for distributed systems
// - Max retry attempts
// - Backoff ceiling

// I AM NOT DONE

use std::time::{Duration, Instant};
use std::thread::sleep;

#[derive(Debug, Clone)]
pub struct RetryConfig {
    pub max_attempts: usize,
    pub initial_delay: Duration,
    pub max_delay: Duration,
    pub multiplier: f64,
    pub use_jitter: bool,
}

impl Default for RetryConfig {
    fn default() -> Self {
        Self {
            max_attempts: 3,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(30),
            multiplier: 2.0,
            use_jitter: true,
        }
    }
}

pub struct RetryStrategy {
    config: RetryConfig,
    current_attempt: usize,
}

impl RetryStrategy {
    pub fn new(config: RetryConfig) -> Self {
        // TODO: Initialize retry strategy
        todo!()
    }

    pub fn with_defaults() -> Self {
        // TODO: Create with default configuration
        todo!()
    }

    fn calculate_delay(&self, attempt: usize) -> Duration {
        // TODO: Calculate delay for given attempt number (0-indexed)
        // - Base delay = initial_delay * (multiplier ^ attempt)
        // - Cap at max_delay
        // - If use_jitter, add random jitter (0% to 25% of delay)
        // - Return calculated duration
        //
        // Hint: Use rand or simple time-based randomness for jitter
        todo!()
    }

    pub fn next_delay(&self) -> Option<Duration> {
        // TODO: Get delay for next retry attempt
        // - If current_attempt >= max_attempts, return None
        // - Otherwise, calculate and return delay for current_attempt
        todo!()
    }

    pub fn execute<F, T, E>(&mut self, mut operation: F) -> Result<T, RetryError<E>>
    where
        F: FnMut() -> Result<T, E>,
    {
        // TODO: Execute operation with exponential backoff retry
        //
        // Logic:
        // 1. Loop through retry attempts (0 to max_attempts - 1)
        // 2. Execute operation
        // 3. If success, return Ok(result)
        // 4. If failure:
        //    - If more attempts available, sleep for calculated delay
        //    - Increment current_attempt
        //    - Continue loop
        // 5. If all attempts exhausted, return Err(RetryError::MaxAttemptsExceeded)
        todo!()
    }

    pub fn current_attempt(&self) -> usize {
        // TODO: Return current attempt number
        todo!()
    }

    pub fn reset(&mut self) {
        // TODO: Reset attempt counter
        todo!()
    }

    pub fn attempts_remaining(&self) -> usize {
        // TODO: Return number of attempts remaining
        todo!()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum RetryError<E> {
    MaxAttemptsExceeded { last_error: E, attempts: usize },
}

// Helper function to calculate total retry time
pub fn calculate_total_retry_time(config: &RetryConfig) -> Duration {
    // TODO: Calculate total time spent on retries (excluding first attempt)
    // - Sum delays for all retry attempts
    // - Don't include jitter in this calculation (use base delays)
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::{Arc, Mutex};

    #[test]
    fn test_retry_config_default() {
        let config = RetryConfig::default();
        assert_eq!(config.max_attempts, 3);
        assert_eq!(config.initial_delay, Duration::from_millis(100));
        assert_eq!(config.multiplier, 2.0);
    }

    #[test]
    fn test_successful_first_attempt() {
        let mut strategy = RetryStrategy::with_defaults();
        let result = strategy.execute(|| Ok::<_, ()>(42));
        assert_eq!(result, Ok(42));
        assert_eq!(strategy.current_attempt(), 0); // No retries needed
    }

    #[test]
    fn test_retry_after_failure() {
        let config = RetryConfig {
            max_attempts: 3,
            initial_delay: Duration::from_millis(10),
            max_delay: Duration::from_secs(1),
            multiplier: 2.0,
            use_jitter: false,
        };

        let mut strategy = RetryStrategy::new(config);
        let counter = Arc::new(Mutex::new(0));
        let counter_clone = counter.clone();

        let result = strategy.execute(|| {
            let mut count = counter_clone.lock().unwrap();
            *count += 1;
            if *count < 3 {
                Err("temporary failure")
            } else {
                Ok(42)
            }
        });

        assert_eq!(result, Ok(42));
        assert_eq!(*counter.lock().unwrap(), 3); // Two failures, one success
    }

    #[test]
    fn test_max_attempts_exceeded() {
        let config = RetryConfig {
            max_attempts: 3,
            initial_delay: Duration::from_millis(10),
            max_delay: Duration::from_secs(1),
            multiplier: 2.0,
            use_jitter: false,
        };

        let mut strategy = RetryStrategy::new(config);
        let counter = Arc::new(Mutex::new(0));
        let counter_clone = counter.clone();

        let result = strategy.execute(|| {
            let mut count = counter_clone.lock().unwrap();
            *count += 1;
            Err::<(), _>("persistent failure")
        });

        match result {
            Err(RetryError::MaxAttemptsExceeded { attempts, .. }) => {
                assert_eq!(attempts, 3);
            }
        }
        assert_eq!(*counter.lock().unwrap(), 3); // All attempts used
    }

    #[test]
    fn test_exponential_delay_growth() {
        let config = RetryConfig {
            max_attempts: 4,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(10),
            multiplier: 2.0,
            use_jitter: false,
        };

        let strategy = RetryStrategy::new(config);

        // Attempt 0: 100ms
        let delay0 = strategy.calculate_delay(0);
        assert_eq!(delay0.as_millis(), 100);

        // Attempt 1: 200ms
        let delay1 = strategy.calculate_delay(1);
        assert_eq!(delay1.as_millis(), 200);

        // Attempt 2: 400ms
        let delay2 = strategy.calculate_delay(2);
        assert_eq!(delay2.as_millis(), 400);

        // Attempt 3: 800ms
        let delay3 = strategy.calculate_delay(3);
        assert_eq!(delay3.as_millis(), 800);
    }

    #[test]
    fn test_max_delay_cap() {
        let config = RetryConfig {
            max_attempts: 10,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_millis(500),
            multiplier: 2.0,
            use_jitter: false,
        };

        let strategy = RetryStrategy::new(config);

        // Attempt 5 would be 3200ms, but should be capped at 500ms
        let delay5 = strategy.calculate_delay(5);
        assert_eq!(delay5.as_millis(), 500);
    }

    #[test]
    fn test_jitter_adds_randomness() {
        let config = RetryConfig {
            max_attempts: 3,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(10),
            multiplier: 2.0,
            use_jitter: true,
        };

        let strategy = RetryStrategy::new(config);

        // Calculate delay multiple times and check for variation
        let delay1 = strategy.calculate_delay(1);
        let delay2 = strategy.calculate_delay(1);

        // With jitter, delays might differ (though not guaranteed in tests)
        // At minimum, check they're in reasonable range (100-250ms for attempt 1)
        assert!(delay1.as_millis() >= 100 && delay1.as_millis() <= 300);
        assert!(delay2.as_millis() >= 100 && delay2.as_millis() <= 300);
    }

    #[test]
    fn test_reset() {
        let mut strategy = RetryStrategy::with_defaults();

        strategy.execute(|| Err::<(), _>("error")).ok();
        assert!(strategy.current_attempt() > 0);

        strategy.reset();
        assert_eq!(strategy.current_attempt(), 0);
    }

    #[test]
    fn test_attempts_remaining() {
        let config = RetryConfig {
            max_attempts: 5,
            initial_delay: Duration::from_millis(10),
            max_delay: Duration::from_secs(1),
            multiplier: 2.0,
            use_jitter: false,
        };

        let mut strategy = RetryStrategy::new(config);
        assert_eq!(strategy.attempts_remaining(), 5);

        strategy.execute(|| Err::<(), _>("error")).ok();
        assert_eq!(strategy.attempts_remaining(), 0); // All used
    }

    #[test]
    fn test_next_delay() {
        let config = RetryConfig {
            max_attempts: 3,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(10),
            multiplier: 2.0,
            use_jitter: false,
        };

        let mut strategy = RetryStrategy::new(config);

        assert!(strategy.next_delay().is_some());

        // Exhaust attempts
        strategy.execute(|| Err::<(), _>("error")).ok();

        assert_eq!(strategy.next_delay(), None);
    }

    #[test]
    fn test_calculate_total_retry_time() {
        let config = RetryConfig {
            max_attempts: 4,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(10),
            multiplier: 2.0,
            use_jitter: false,
        };

        // Total = 100 + 200 + 400 = 700ms (first attempt doesn't count)
        let total = calculate_total_retry_time(&config);
        assert_eq!(total.as_millis(), 700);
    }

    #[test]
    fn test_custom_multiplier() {
        let config = RetryConfig {
            max_attempts: 3,
            initial_delay: Duration::from_millis(100),
            max_delay: Duration::from_secs(10),
            multiplier: 3.0,
            use_jitter: false,
        };

        let strategy = RetryStrategy::new(config);

        let delay0 = strategy.calculate_delay(0);
        let delay1 = strategy.calculate_delay(1);
        let delay2 = strategy.calculate_delay(2);

        assert_eq!(delay0.as_millis(), 100);
        assert_eq!(delay1.as_millis(), 300); // 100 * 3
        assert_eq!(delay2.as_millis(), 900); // 100 * 3^2
    }

    #[test]
    fn test_eventual_success_timing() {
        let config = RetryConfig {
            max_attempts: 3,
            initial_delay: Duration::from_millis(50),
            max_delay: Duration::from_secs(10),
            multiplier: 2.0,
            use_jitter: false,
        };

        let mut strategy = RetryStrategy::new(config);
        let counter = Arc::new(Mutex::new(0));
        let counter_clone = counter.clone();

        let start = Instant::now();

        strategy.execute(|| {
            let mut count = counter_clone.lock().unwrap();
            *count += 1;
            if *count < 3 {
                Err("fail")
            } else {
                Ok(())
            }
        }).ok();

        let elapsed = start.elapsed();

        // Should take at least 50ms (first retry) + 100ms (second retry) = 150ms
        assert!(elapsed.as_millis() >= 140);
    }
}
