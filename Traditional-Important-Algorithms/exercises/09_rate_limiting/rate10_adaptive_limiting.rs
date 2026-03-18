// rate10_adaptive_limiting.rs
//
// Adaptive Rate Limiting dynamically adjusts rate limits based on system load,
// performance metrics, and historical patterns.
//
// How it works:
// - Monitor system metrics (CPU, memory, latency, error rate)
// - Adjust rate limits based on current capacity
// - Increase limits when system is healthy
// - Decrease limits when system is under stress
// - Use feedback loops for continuous optimization
//
// Your task: Implement an adaptive rate limiter that adjusts to system load.
//
// Key concepts:
// - System health monitoring
// - Dynamic threshold adjustment
// - Feedback control loops
// - Load-based rate limiting

// I AM NOT DONE

use std::collections::VecDeque;
use std::time::{Duration, Instant};

#[derive(Debug, Clone)]
pub struct SystemMetrics {
    pub cpu_usage: f64,        // 0.0 to 1.0
    pub memory_usage: f64,     // 0.0 to 1.0
    pub error_rate: f64,       // 0.0 to 1.0
    pub avg_latency_ms: f64,
    pub timestamp: Instant,
}

#[derive(Debug, Clone)]
pub struct AdaptiveConfig {
    pub min_rate: usize,           // Minimum requests per second
    pub max_rate: usize,           // Maximum requests per second
    pub cpu_threshold: f64,        // Start reducing rate above this
    pub memory_threshold: f64,     // Start reducing rate above this
    pub error_threshold: f64,      // Start reducing rate above this
    pub latency_threshold_ms: f64, // Start reducing rate above this
    pub increase_factor: f64,      // Rate increase multiplier
    pub decrease_factor: f64,      // Rate decrease multiplier
}

impl Default for AdaptiveConfig {
    fn default() -> Self {
        Self {
            min_rate: 10,
            max_rate: 1000,
            cpu_threshold: 0.7,
            memory_threshold: 0.8,
            error_threshold: 0.05,
            latency_threshold_ms: 1000.0,
            increase_factor: 1.1,
            decrease_factor: 0.8,
        }
    }
}

pub struct AdaptiveRateLimiter {
    config: AdaptiveConfig,
    current_rate: usize,           // Current requests per second
    request_history: VecDeque<Instant>,
    metrics_history: VecDeque<SystemMetrics>,
    last_adjustment: Instant,
    adjustment_interval: Duration,
}

impl AdaptiveRateLimiter {
    pub fn new(config: AdaptiveConfig, adjustment_interval: Duration) -> Self {
        // TODO: Initialize adaptive rate limiter
        // - Set current_rate to max_rate (start optimistic)
        // - Create empty histories
        // - Set last_adjustment to now
        todo!()
    }

    pub fn with_defaults() -> Self {
        // TODO: Create with default config and 1-second adjustment interval
        todo!()
    }

    fn cleanup_old_requests(&mut self, window: Duration) {
        // TODO: Remove requests older than window from history
        // - Calculate cutoff time
        // - Remove old requests from front of queue
        todo!()
    }

    fn should_adjust(&self) -> bool {
        // TODO: Check if enough time has passed to adjust rate
        // - Return true if time since last_adjustment >= adjustment_interval
        todo!()
    }

    fn calculate_new_rate(&self, metrics: &SystemMetrics) -> usize {
        // TODO: Calculate new rate based on system metrics
        //
        // Logic:
        // 1. Start with current_rate
        // 2. Check each threshold:
        //    - If CPU > threshold, multiply by decrease_factor
        //    - If memory > threshold, multiply by decrease_factor
        //    - If error_rate > threshold, multiply by decrease_factor
        //    - If latency > threshold, multiply by decrease_factor
        // 3. If all metrics healthy, multiply by increase_factor
        // 4. Clamp result between min_rate and max_rate
        // 5. Return new rate as usize
        todo!()
    }

    pub fn update_metrics(&mut self, metrics: SystemMetrics) {
        // TODO: Update system metrics and adjust rate if needed
        // - Add metrics to metrics_history
        // - Keep only recent metrics (e.g., last 100)
        // - If should_adjust():
        //   - Calculate new rate
        //   - Update current_rate
        //   - Update last_adjustment
        todo!()
    }

    pub fn try_acquire(&mut self) -> bool {
        // TODO: Try to acquire request slot
        // - Cleanup old requests (1 second window)
        // - Count requests in last second
        // - If count < current_rate:
        //   - Add current time to request_history
        //   - Return true
        // - Otherwise return false
        todo!()
    }

    pub fn current_rate(&self) -> usize {
        // TODO: Return current rate limit
        todo!()
    }

    pub fn request_count_last_second(&mut self) -> usize {
        // TODO: Return number of requests in last second
        // - Cleanup old requests first
        // - Return request_history length
        todo!()
    }

    pub fn average_cpu_usage(&self) -> Option<f64> {
        // TODO: Calculate average CPU usage from recent metrics
        // - Return None if no metrics
        // - Otherwise average the cpu_usage values
        todo!()
    }

    pub fn average_latency(&self) -> Option<f64> {
        // TODO: Calculate average latency from recent metrics
        // - Return None if no metrics
        // - Otherwise average the avg_latency_ms values
        todo!()
    }

    pub fn is_system_healthy(&self) -> bool {
        // TODO: Check if system is healthy based on recent metrics
        // - Get most recent metrics, return true if none
        // - Check all thresholds
        // - Return true only if all metrics below thresholds
        todo!()
    }

    pub fn reset(&mut self) {
        // TODO: Reset to initial state
        // - Clear histories
        // - Reset current_rate to max_rate
        // - Update last_adjustment
        todo!()
    }
}

// AIMD (Additive Increase Multiplicative Decrease) strategy
pub struct AIMDRateLimiter {
    current_rate: f64,
    min_rate: f64,
    max_rate: f64,
    increase_amount: f64,
    decrease_factor: f64,
    last_success: bool,
}

impl AIMDRateLimiter {
    pub fn new(
        initial_rate: f64,
        min_rate: f64,
        max_rate: f64,
        increase_amount: f64,
        decrease_factor: f64,
    ) -> Self {
        // TODO: Initialize AIMD rate limiter
        todo!()
    }

    pub fn on_success(&mut self) {
        // TODO: Handle successful request
        // - Additively increase rate
        // - current_rate += increase_amount
        // - Clamp to max_rate
        // - Set last_success to true
        todo!()
    }

    pub fn on_failure(&mut self) {
        // TODO: Handle failed request
        // - Multiplicatively decrease rate
        // - current_rate *= decrease_factor
        // - Clamp to min_rate
        // - Set last_success to false
        todo!()
    }

    pub fn get_rate(&self) -> f64 {
        // TODO: Return current rate
        todo!()
    }

    pub fn reset(&mut self, rate: f64) {
        // TODO: Reset to specific rate
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_adaptive_limiter_creation() {
        let limiter = AdaptiveRateLimiter::with_defaults();
        assert_eq!(limiter.current_rate(), 1000); // Starts at max
    }

    #[test]
    fn test_acquire_under_limit() {
        let mut limiter = AdaptiveRateLimiter::with_defaults();

        // Should be able to acquire up to current rate
        for _ in 0..10 {
            assert!(limiter.try_acquire());
        }
    }

    #[test]
    fn test_rate_limiting() {
        let config = AdaptiveConfig {
            min_rate: 5,
            max_rate: 10,
            ..Default::default()
        };

        let mut limiter = AdaptiveRateLimiter::new(config, Duration::from_secs(1));

        // Fill up to limit
        for _ in 0..10 {
            limiter.try_acquire();
        }

        // Next should be rejected
        assert!(!limiter.try_acquire());
    }

    #[test]
    fn test_rate_decrease_on_high_cpu() {
        let config = AdaptiveConfig {
            cpu_threshold: 0.5,
            decrease_factor: 0.5,
            ..Default::default()
        };

        let mut limiter = AdaptiveRateLimiter::new(config, Duration::from_millis(10));
        let initial_rate = limiter.current_rate();

        std::thread::sleep(Duration::from_millis(15));

        // High CPU usage
        let metrics = SystemMetrics {
            cpu_usage: 0.9,
            memory_usage: 0.3,
            error_rate: 0.0,
            avg_latency_ms: 100.0,
            timestamp: Instant::now(),
        };

        limiter.update_metrics(metrics);

        // Rate should decrease
        assert!(limiter.current_rate() < initial_rate);
    }

    #[test]
    fn test_rate_increase_when_healthy() {
        let config = AdaptiveConfig {
            increase_factor: 1.5,
            max_rate: 1000,
            ..Default::default()
        };

        let mut limiter = AdaptiveRateLimiter::new(config, Duration::from_millis(10));

        // Start at lower rate
        limiter.update_metrics(SystemMetrics {
            cpu_usage: 0.9,
            memory_usage: 0.9,
            error_rate: 0.0,
            avg_latency_ms: 100.0,
            timestamp: Instant::now(),
        });

        std::thread::sleep(Duration::from_millis(15));

        let rate_before = limiter.current_rate();

        // Healthy metrics
        let metrics = SystemMetrics {
            cpu_usage: 0.3,
            memory_usage: 0.3,
            error_rate: 0.0,
            avg_latency_ms: 100.0,
            timestamp: Instant::now(),
        };

        limiter.update_metrics(metrics);

        // Rate should increase
        assert!(limiter.current_rate() > rate_before);
    }

    #[test]
    fn test_rate_bounds() {
        let config = AdaptiveConfig {
            min_rate: 10,
            max_rate: 100,
            decrease_factor: 0.1,
            increase_factor: 10.0,
            ..Default::default()
        };

        let mut limiter = AdaptiveRateLimiter::new(config, Duration::from_millis(10));

        // Try to decrease below min
        std::thread::sleep(Duration::from_millis(15));
        for _ in 0..10 {
            limiter.update_metrics(SystemMetrics {
                cpu_usage: 1.0,
                memory_usage: 1.0,
                error_rate: 1.0,
                avg_latency_ms: 10000.0,
                timestamp: Instant::now(),
            });
            std::thread::sleep(Duration::from_millis(15));
        }

        assert_eq!(limiter.current_rate(), 10); // Clamped to min

        // Try to increase above max
        for _ in 0..10 {
            limiter.update_metrics(SystemMetrics {
                cpu_usage: 0.0,
                memory_usage: 0.0,
                error_rate: 0.0,
                avg_latency_ms: 1.0,
                timestamp: Instant::now(),
            });
            std::thread::sleep(Duration::from_millis(15));
        }

        assert_eq!(limiter.current_rate(), 100); // Clamped to max
    }

    #[test]
    fn test_request_count() {
        let mut limiter = AdaptiveRateLimiter::with_defaults();

        limiter.try_acquire();
        limiter.try_acquire();
        limiter.try_acquire();

        assert_eq!(limiter.request_count_last_second(), 3);
    }

    #[test]
    fn test_average_metrics() {
        let mut limiter = AdaptiveRateLimiter::with_defaults();

        limiter.update_metrics(SystemMetrics {
            cpu_usage: 0.5,
            memory_usage: 0.5,
            error_rate: 0.0,
            avg_latency_ms: 200.0,
            timestamp: Instant::now(),
        });

        limiter.update_metrics(SystemMetrics {
            cpu_usage: 0.7,
            memory_usage: 0.6,
            error_rate: 0.0,
            avg_latency_ms: 300.0,
            timestamp: Instant::now(),
        });

        let avg_cpu = limiter.average_cpu_usage().unwrap();
        let avg_latency = limiter.average_latency().unwrap();

        assert!((avg_cpu - 0.6).abs() < 0.01);
        assert!((avg_latency - 250.0).abs() < 1.0);
    }

    #[test]
    fn test_system_health_check() {
        let mut limiter = AdaptiveRateLimiter::with_defaults();

        // Healthy metrics
        limiter.update_metrics(SystemMetrics {
            cpu_usage: 0.3,
            memory_usage: 0.4,
            error_rate: 0.01,
            avg_latency_ms: 100.0,
            timestamp: Instant::now(),
        });

        assert!(limiter.is_system_healthy());

        // Unhealthy metrics
        limiter.update_metrics(SystemMetrics {
            cpu_usage: 0.9,
            memory_usage: 0.9,
            error_rate: 0.1,
            avg_latency_ms: 5000.0,
            timestamp: Instant::now(),
        });

        assert!(!limiter.is_system_healthy());
    }

    #[test]
    fn test_aimd_creation() {
        let aimd = AIMDRateLimiter::new(100.0, 10.0, 1000.0, 5.0, 0.8);
        assert_eq!(aimd.get_rate(), 100.0);
    }

    #[test]
    fn test_aimd_additive_increase() {
        let mut aimd = AIMDRateLimiter::new(100.0, 10.0, 1000.0, 10.0, 0.8);

        aimd.on_success();
        assert_eq!(aimd.get_rate(), 110.0);

        aimd.on_success();
        assert_eq!(aimd.get_rate(), 120.0);
    }

    #[test]
    fn test_aimd_multiplicative_decrease() {
        let mut aimd = AIMDRateLimiter::new(100.0, 10.0, 1000.0, 5.0, 0.5);

        aimd.on_failure();
        assert_eq!(aimd.get_rate(), 50.0);

        aimd.on_failure();
        assert_eq!(aimd.get_rate(), 25.0);
    }

    #[test]
    fn test_aimd_bounds() {
        let mut aimd = AIMDRateLimiter::new(50.0, 10.0, 100.0, 20.0, 0.5);

        // Try to increase above max
        for _ in 0..10 {
            aimd.on_success();
        }
        assert_eq!(aimd.get_rate(), 100.0);

        // Try to decrease below min
        for _ in 0..10 {
            aimd.on_failure();
        }
        assert_eq!(aimd.get_rate(), 10.0);
    }

    #[test]
    fn test_aimd_reset() {
        let mut aimd = AIMDRateLimiter::new(100.0, 10.0, 1000.0, 5.0, 0.8);

        aimd.on_success();
        aimd.on_success();

        aimd.reset(200.0);
        assert_eq!(aimd.get_rate(), 200.0);
    }

    #[test]
    fn test_adaptive_reset() {
        let mut limiter = AdaptiveRateLimiter::with_defaults();

        limiter.try_acquire();
        limiter.try_acquire();

        limiter.reset();

        assert_eq!(limiter.request_count_last_second(), 0);
        assert_eq!(limiter.current_rate(), 1000);
    }
}
