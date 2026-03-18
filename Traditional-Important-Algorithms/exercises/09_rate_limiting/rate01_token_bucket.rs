// rate01_token_bucket.rs
//
// Token Bucket is a rate limiting algorithm that allows bursts of traffic
// while maintaining an average rate limit over time.
//
// How it works:
// - Bucket holds tokens, each representing permission to perform one action
// - Tokens are added at a fixed rate (refill_rate)
// - Bucket has a maximum capacity
// - Request consumes tokens; if not enough tokens, request is denied
// - Allows bursts up to bucket capacity
//
// Your task: Implement a token bucket rate limiter.
//
// Key concepts:
// - Token refill based on time elapsed
// - Bucket capacity limiting
// - Thread-safe token consumption
// - Handling time-based refills

// I AM NOT DONE

use std::time::{Duration, Instant};

pub struct TokenBucket {
    capacity: f64,           // Maximum tokens in bucket
    tokens: f64,             // Current available tokens
    refill_rate: f64,        // Tokens added per second
    last_refill: Instant,    // Last time tokens were refilled
}

impl TokenBucket {
    pub fn new(capacity: f64, refill_rate: f64) -> Self {
        // TODO: Initialize a new token bucket
        // - Start with full capacity
        // - Set last_refill to current time
        todo!()
    }

    fn refill(&mut self) {
        // TODO: Refill tokens based on time elapsed since last refill
        // - Calculate elapsed time since last_refill
        // - Calculate new tokens: elapsed_seconds * refill_rate
        // - Add new tokens but don't exceed capacity
        // - Update last_refill to current time
        todo!()
    }

    pub fn try_consume(&mut self, tokens: f64) -> bool {
        // TODO: Try to consume the specified number of tokens
        // - First call refill() to update token count
        // - Check if enough tokens available
        // - If yes, subtract tokens and return true
        // - If no, return false (don't consume any tokens)
        todo!()
    }

    pub fn available_tokens(&mut self) -> f64 {
        // TODO: Return current number of available tokens
        // - Call refill() first to update count
        // - Return current tokens
        todo!()
    }

    pub fn wait_time_for(&mut self, tokens: f64) -> Option<Duration> {
        // TODO: Calculate how long to wait until requested tokens are available
        // - Call refill() first
        // - If tokens already available, return None
        // - Calculate tokens needed: tokens - self.tokens
        // - Calculate wait time: tokens_needed / refill_rate
        // - Return Some(duration)
        todo!()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread::sleep;

    #[test]
    fn test_token_bucket_creation() {
        let mut bucket = TokenBucket::new(10.0, 5.0);
        assert_eq!(bucket.available_tokens(), 10.0);
    }

    #[test]
    fn test_consume_tokens() {
        let mut bucket = TokenBucket::new(10.0, 5.0);
        assert!(bucket.try_consume(5.0));
        assert_eq!(bucket.available_tokens(), 5.0);
        assert!(bucket.try_consume(5.0));
        assert_eq!(bucket.available_tokens(), 0.0);
    }

    #[test]
    fn test_consume_too_many_tokens() {
        let mut bucket = TokenBucket::new(10.0, 5.0);
        assert!(!bucket.try_consume(15.0));
        assert_eq!(bucket.available_tokens(), 10.0); // No tokens consumed
    }

    #[test]
    fn test_insufficient_tokens() {
        let mut bucket = TokenBucket::new(10.0, 5.0);
        bucket.try_consume(8.0);
        assert!(!bucket.try_consume(5.0)); // Only 2 tokens left
    }

    #[test]
    fn test_token_refill() {
        let mut bucket = TokenBucket::new(10.0, 10.0); // 10 tokens per second
        bucket.try_consume(10.0);
        assert_eq!(bucket.available_tokens(), 0.0);

        sleep(Duration::from_millis(500)); // Wait 0.5 seconds

        // Should have approximately 5 tokens (10 tokens/sec * 0.5 sec)
        let available = bucket.available_tokens();
        assert!(available >= 4.5 && available <= 5.5);
    }

    #[test]
    fn test_refill_does_not_exceed_capacity() {
        let mut bucket = TokenBucket::new(10.0, 10.0);
        bucket.try_consume(5.0);

        sleep(Duration::from_secs(2)); // Wait 2 seconds

        // Should refill to capacity (10), not beyond
        let available = bucket.available_tokens();
        assert_eq!(available, 10.0);
    }

    #[test]
    fn test_burst_traffic() {
        let mut bucket = TokenBucket::new(10.0, 2.0); // Low refill rate

        // Can handle burst up to capacity
        assert!(bucket.try_consume(3.0));
        assert!(bucket.try_consume(3.0));
        assert!(bucket.try_consume(3.0));
        assert_eq!(bucket.available_tokens(), 1.0);
    }

    #[test]
    fn test_wait_time_calculation() {
        let mut bucket = TokenBucket::new(10.0, 5.0); // 5 tokens per second
        bucket.try_consume(10.0);

        let wait_time = bucket.wait_time_for(5.0);
        assert!(wait_time.is_some());

        // Should wait approximately 1 second (5 tokens / 5 tokens per second)
        let duration = wait_time.unwrap();
        assert!(duration.as_secs_f64() >= 0.9 && duration.as_secs_f64() <= 1.1);
    }

    #[test]
    fn test_wait_time_when_tokens_available() {
        let mut bucket = TokenBucket::new(10.0, 5.0);

        let wait_time = bucket.wait_time_for(5.0);
        assert_eq!(wait_time, None); // Tokens already available
    }

    #[test]
    fn test_partial_refill() {
        let mut bucket = TokenBucket::new(10.0, 20.0); // 20 tokens per second
        bucket.try_consume(10.0);

        sleep(Duration::from_millis(250)); // 0.25 seconds

        // Should have approximately 5 tokens (20 tokens/sec * 0.25 sec)
        let available = bucket.available_tokens();
        assert!(available >= 4.5 && available <= 5.5);
    }

    #[test]
    fn test_zero_consumption() {
        let mut bucket = TokenBucket::new(10.0, 5.0);
        assert!(bucket.try_consume(0.0));
        assert_eq!(bucket.available_tokens(), 10.0);
    }

    #[test]
    fn test_fractional_tokens() {
        let mut bucket = TokenBucket::new(10.0, 5.0);
        assert!(bucket.try_consume(2.5));
        assert_eq!(bucket.available_tokens(), 7.5);
        assert!(bucket.try_consume(1.25));
        assert_eq!(bucket.available_tokens(), 6.25);
    }
}
