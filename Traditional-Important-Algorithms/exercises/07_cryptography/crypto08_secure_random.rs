// crypto08_secure_random.rs
//
// Cryptographically Secure Random Number Generation (CSPRNG) is essential
// for generating keys, salts, nonces, and other security-critical values.
//
// Key properties of CSPRNG:
// - Unpredictable: Cannot predict future outputs from past outputs
// - Non-reproducible: Each run produces different values
// - Uniform distribution: All values equally likely
// - Sufficient entropy: Seeded with high-quality randomness
//
// Common CSPRNGs:
// - ChaCha20: Modern, fast, secure stream cipher
// - AES-CTR: AES in counter mode
// - /dev/urandom (Unix): OS-provided CSPRNG
// - CryptGenRandom (Windows): Windows CSPRNG
//
// NEVER use for crypto:
// - rand() from C standard library
// - Math.random() in JavaScript
// - Linear congruential generators
// - Mersenne Twister (good for simulation, not crypto)
//
// Your task: Implement a simple CSPRNG based on a stream cipher.
//
// Security considerations:
// - Always use OS-provided CSPRNGs in production (e.g., getrandom())
// - Seed with high-entropy source (hardware RNG, OS entropy pool)
// - Never reuse nonces in stream ciphers
// - Reseed periodically to maintain forward secrecy
// - Be careful with fork(): child processes inherit RNG state
// - Some PRNGs vulnerable to state compromise extension

// I AM NOT DONE

const STATE_SIZE: usize = 32;
const RESEED_INTERVAL: usize = 1000000; // Reseed after this many bytes

pub struct SecureRandom {
    state: [u8; STATE_SIZE],
    counter: u64,
    bytes_generated: usize,
}

impl SecureRandom {
    pub fn new() -> Self {
        // TODO: Create new CSPRNG with random seed
        // 1. Get seed from entropy source (use system_entropy())
        // 2. Initialize state with seed
        // 3. Set counter to 0
        // 4. Return SecureRandom
        todo!()
    }

    pub fn from_seed(seed: [u8; STATE_SIZE]) -> Self {
        // TODO: Create CSPRNG from explicit seed (for testing)
        // Initialize state, counter, and bytes_generated
        todo!()
    }

    pub fn next_bytes(&mut self, output: &mut [u8]) {
        // TODO: Generate random bytes
        // 1. Check if reseed is needed
        // 2. For each output byte:
        //    a. Generate byte using stream_cipher
        //    b. Increment counter
        //    c. Update bytes_generated
        // 3. If bytes_generated > RESEED_INTERVAL, reseed
        todo!()
    }

    pub fn next_u32(&mut self) -> u32 {
        // TODO: Generate random u32
        // Use next_bytes to fill 4-byte buffer
        // Convert to u32 (little-endian)
        todo!()
    }

    pub fn next_u64(&mut self) -> u64 {
        // TODO: Generate random u64
        // Use next_bytes to fill 8-byte buffer
        todo!()
    }

    pub fn next_range(&mut self, min: u64, max: u64) -> u64 {
        // TODO: Generate random number in range [min, max)
        // IMPORTANT: Avoid modulo bias
        // 1. Calculate range = max - min
        // 2. Calculate limit = u64::MAX - (u64::MAX % range)
        // 3. Generate random u64, reject if >= limit (retry)
        // 4. Return (random % range) + min
        todo!()
    }

    pub fn shuffle<T>(&mut self, slice: &mut [T]) {
        // TODO: Shuffle slice using Fisher-Yates algorithm
        // For i from n-1 down to 1:
        //   j = random integer in range [0, i]
        //   swap slice[i] and slice[j]
        todo!()
    }

    fn reseed(&mut self) {
        // TODO: Reseed the RNG for forward secrecy
        // 1. Get new entropy from system_entropy()
        // 2. Mix with current state using XOR
        // 3. Hash the result to get new state
        // 4. Reset bytes_generated counter
        todo!()
    }
}

// Simple stream cipher for generating random bytes
fn stream_cipher(state: &[u8; STATE_SIZE], counter: u64) -> u8 {
    // TODO: Generate one pseudo-random byte
    // This is a simplified stream cipher (not production-quality)
    // 1. Combine state and counter
    // 2. Apply mixing function (XOR with rotations)
    // 3. Return one byte of output
    // Real implementation would use ChaCha20 or similar
    todo!()
}

// Get entropy from system (simplified version)
fn system_entropy() -> [u8; STATE_SIZE] {
    // TODO: Get entropy from system
    // In real implementation, use getrandom() syscall or /dev/urandom
    // For this exercise, use timestamp + process info as seed
    // NOTE: This is NOT secure for production!
    use std::time::{SystemTime, UNIX_EPOCH};

    let mut entropy = [0u8; STATE_SIZE];
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos();

    // Fill entropy with timestamp-based values (simplified)
    for i in 0..STATE_SIZE {
        entropy[i] = ((now >> (i * 8)) & 0xFF) as u8;
    }

    // Mix with process-specific info
    let pid = std::process::id();
    for i in 0..4 {
        entropy[i] ^= ((pid >> (i * 8)) & 0xFF) as u8;
    }

    entropy
}

// Simple hash function for mixing
fn mix_hash(data: &[u8]) -> [u8; STATE_SIZE] {
    // TODO: Hash function to mix entropy
    // Use simple mixing (not cryptographically secure)
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_random_creation() {
        let rng = SecureRandom::new();

        // Should initialize successfully
        assert_eq!(rng.counter, 0);
    }

    #[test]
    fn test_next_bytes() {
        let mut rng = SecureRandom::new();
        let mut buf1 = [0u8; 32];
        let mut buf2 = [0u8; 32];

        rng.next_bytes(&mut buf1);
        rng.next_bytes(&mut buf2);

        // Should produce different outputs
        assert_ne!(buf1, buf2);
    }

    #[test]
    fn test_deterministic_with_seed() {
        let seed = [42u8; STATE_SIZE];

        let mut rng1 = SecureRandom::from_seed(seed);
        let mut rng2 = SecureRandom::from_seed(seed);

        let mut buf1 = [0u8; 16];
        let mut buf2 = [0u8; 16];

        rng1.next_bytes(&mut buf1);
        rng2.next_bytes(&mut buf2);

        // Same seed should produce same output
        assert_eq!(buf1, buf2);
    }

    #[test]
    fn test_next_u32() {
        let mut rng = SecureRandom::new();

        let n1 = rng.next_u32();
        let n2 = rng.next_u32();

        // Should produce different values (with very high probability)
        assert_ne!(n1, n2);
    }

    #[test]
    fn test_next_u64() {
        let mut rng = SecureRandom::new();

        let n1 = rng.next_u64();
        let n2 = rng.next_u64();

        assert_ne!(n1, n2);
    }

    #[test]
    fn test_next_range() {
        let mut rng = SecureRandom::new();

        for _ in 0..100 {
            let n = rng.next_range(10, 20);
            assert!(n >= 10 && n < 20);
        }
    }

    #[test]
    fn test_next_range_single_value() {
        let mut rng = SecureRandom::new();

        let n = rng.next_range(5, 6);
        assert_eq!(n, 5);
    }

    #[test]
    fn test_shuffle() {
        let mut rng = SecureRandom::from_seed([42u8; STATE_SIZE]);
        let mut data = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let original = data.clone();

        rng.shuffle(&mut data);

        // Should be different order (with very high probability)
        assert_ne!(data, original);

        // Should contain same elements
        let mut sorted = data.clone();
        sorted.sort();
        assert_eq!(sorted, original);
    }

    #[test]
    fn test_uniform_distribution() {
        let mut rng = SecureRandom::new();
        let mut buckets = [0usize; 10];

        // Generate many samples
        for _ in 0..10000 {
            let n = rng.next_range(0, 10);
            buckets[n as usize] += 1;
        }

        // Each bucket should have roughly 1000 samples (±30%)
        for count in buckets.iter() {
            assert!(*count > 700 && *count < 1300);
        }
    }

    #[test]
    fn test_no_obvious_patterns() {
        let mut rng = SecureRandom::new();
        let mut bytes = [0u8; 256];

        rng.next_bytes(&mut bytes);

        // Count zero bits and one bits
        let mut zero_bits = 0;
        let mut one_bits = 0;

        for byte in bytes.iter() {
            zero_bits += byte.count_zeros();
            one_bits += byte.count_ones();
        }

        // Should be roughly 50/50 (±10%)
        let total_bits = (zero_bits + one_bits) as f64;
        let one_ratio = one_bits as f64 / total_bits;

        assert!(one_ratio > 0.4 && one_ratio < 0.6);
    }

    #[test]
    fn test_different_seeds_different_output() {
        let seed1 = [1u8; STATE_SIZE];
        let seed2 = [2u8; STATE_SIZE];

        let mut rng1 = SecureRandom::from_seed(seed1);
        let mut rng2 = SecureRandom::from_seed(seed2);

        let n1 = rng1.next_u64();
        let n2 = rng2.next_u64();

        assert_ne!(n1, n2);
    }

    #[test]
    fn test_system_entropy_varies() {
        let entropy1 = system_entropy();

        // Small delay to ensure different timestamp
        std::thread::sleep(std::time::Duration::from_nanos(100));

        let entropy2 = system_entropy();

        // Should produce different entropy each time
        assert_ne!(entropy1, entropy2);
    }

    #[test]
    fn test_large_range() {
        let mut rng = SecureRandom::new();

        let n = rng.next_range(0, u64::MAX / 2);

        assert!(n < u64::MAX / 2);
    }

    #[test]
    fn test_sequential_calls() {
        let mut rng = SecureRandom::new();
        let mut values = Vec::new();

        for _ in 0..100 {
            values.push(rng.next_u32());
        }

        // No two values should be the same (with very high probability)
        for i in 0..values.len() {
            for j in i + 1..values.len() {
                if values[i] == values[j] {
                    panic!("Found duplicate values at {} and {}", i, j);
                }
            }
        }
    }
}
