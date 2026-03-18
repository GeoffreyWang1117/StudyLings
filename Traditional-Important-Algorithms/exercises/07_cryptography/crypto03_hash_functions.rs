// crypto03_hash_functions.rs
//
// Cryptographic Hash Functions are one-way functions that map arbitrary data
// to fixed-size outputs (digests). They are fundamental to digital signatures,
// password storage, and data integrity verification.
//
// Properties of cryptographic hash functions:
// - Deterministic: Same input always produces same output
// - Fast to compute
// - Avalanche effect: Small input change drastically changes output
// - Pre-image resistance: Hard to find input from output
// - Second pre-image resistance: Hard to find different input with same output
// - Collision resistance: Hard to find two inputs with same output
//
// Your task: Implement a simplified SHA-like hash function.
//
// Security considerations:
// - Never use MD5 or SHA-1 in production (both are broken)
// - Use SHA-256, SHA-3, or BLAKE2 for new applications
// - Hash functions alone are NOT suitable for password storage
// - Use for integrity checks, but add HMAC for authentication
// - Beware of length extension attacks (SHA-2 vulnerable, SHA-3 is not)

// I AM NOT DONE

const BLOCK_SIZE: usize = 64; // 512 bits
const HASH_SIZE: usize = 32;  // 256 bits

// Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
const INITIAL_HASH: [u32; 8] = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
];

// Round constants (first 32 bits of fractional parts of cube roots of first 64 primes)
const K: [u32; 64] = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
];

pub struct Sha256 {
    state: [u32; 8],
    buffer: Vec<u8>,
    total_len: u64,
}

impl Sha256 {
    pub fn new() -> Self {
        Self {
            state: INITIAL_HASH,
            buffer: Vec::new(),
            total_len: 0,
        }
    }

    pub fn update(&mut self, data: &[u8]) {
        // TODO: Update hash state with new data
        // 1. Append data to buffer
        // 2. Process complete blocks (64 bytes each)
        // 3. Keep remaining data in buffer
        // 4. Update total_len
        todo!()
    }

    pub fn finalize(&mut self) -> [u8; HASH_SIZE] {
        // TODO: Finalize hash and return digest
        // 1. Apply padding: append 0x80, then zeros, then 64-bit length
        // 2. Process remaining blocks
        // 3. Convert state to bytes (big-endian)
        // 4. Return 32-byte hash
        todo!()
    }

    fn process_block(&mut self, block: &[u8]) {
        // TODO: Process a single 512-bit block
        // 1. Create message schedule (W) array of 64 u32 values
        // 2. First 16 values come from block (big-endian)
        // 3. Remaining 48 values computed using SHA-256 formula
        // 4. Initialize working variables a-h from state
        // 5. Main loop: 64 rounds of compression function
        // 6. Add compressed values back to state
        todo!()
    }

    pub fn digest(data: &[u8]) -> [u8; HASH_SIZE] {
        // TODO: Convenience function to hash data in one call
        // 1. Create new Sha256
        // 2. Update with data
        // 3. Finalize and return
        todo!()
    }

    pub fn digest_hex(data: &[u8]) -> String {
        // TODO: Return hash as hex string
        let hash = Self::digest(data);
        hash.iter()
            .map(|b| format!("{:02x}", b))
            .collect()
    }
}

// SHA-256 helper functions
fn ch(x: u32, y: u32, z: u32) -> u32 {
    // TODO: Choice function: (x & y) ^ (!x & z)
    todo!()
}

fn maj(x: u32, y: u32, z: u32) -> u32 {
    // TODO: Majority function: (x & y) ^ (x & z) ^ (y & z)
    todo!()
}

fn sigma0(x: u32) -> u32 {
    // TODO: Σ0 function: ROTR(2) ^ ROTR(13) ^ ROTR(22)
    x.rotate_right(2) ^ x.rotate_right(13) ^ x.rotate_right(22)
}

fn sigma1(x: u32) -> u32 {
    // TODO: Σ1 function: ROTR(6) ^ ROTR(11) ^ ROTR(25)
    todo!()
}

fn gamma0(x: u32) -> u32 {
    // TODO: σ0 function: ROTR(7) ^ ROTR(18) ^ SHR(3)
    todo!()
}

fn gamma1(x: u32) -> u32 {
    // TODO: σ1 function: ROTR(17) ^ ROTR(19) ^ SHR(10)
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_string() {
        let hash = Sha256::digest(b"");
        let hex = Sha256::digest_hex(b"");

        assert_eq!(hash.len(), 32);
        // SHA-256 of empty string (verify against known value)
        assert_eq!(hex, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
    }

    #[test]
    fn test_simple_message() {
        let hash = Sha256::digest(b"abc");
        let hex = Sha256::digest_hex(b"abc");

        // SHA-256 of "abc"
        assert_eq!(hex, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
    }

    #[test]
    fn test_longer_message() {
        let message = b"The quick brown fox jumps over the lazy dog";
        let hex = Sha256::digest_hex(message);

        assert_eq!(hex, "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592");
    }

    #[test]
    fn test_deterministic() {
        let data = b"test message";

        let hash1 = Sha256::digest(data);
        let hash2 = Sha256::digest(data);

        assert_eq!(hash1, hash2);
    }

    #[test]
    fn test_avalanche_effect() {
        let hash1 = Sha256::digest(b"test");
        let hash2 = Sha256::digest(b"Test"); // One bit different

        // Count differing bits
        let diff_bits: u32 = hash1.iter()
            .zip(hash2.iter())
            .map(|(a, b)| (a ^ b).count_ones())
            .sum();

        // Should differ in approximately 50% of bits (128 out of 256)
        assert!(diff_bits > 100 && diff_bits < 156);
    }

    #[test]
    fn test_incremental_update() {
        let mut hasher = Sha256::new();
        hasher.update(b"Hello, ");
        hasher.update(b"World!");
        let hash1 = hasher.finalize();

        let hash2 = Sha256::digest(b"Hello, World!");

        assert_eq!(hash1, hash2);
    }

    #[test]
    fn test_long_message() {
        let message = vec![b'a'; 1000];
        let hash = Sha256::digest(&message);

        assert_eq!(hash.len(), 32);
    }

    #[test]
    fn test_boundary_block_size() {
        // Message exactly 64 bytes (one block)
        let message = vec![b'a'; 64];
        let hash = Sha256::digest(&message);

        assert_eq!(hash.len(), 32);
    }

    #[test]
    fn test_multiple_blocks() {
        // Message larger than one block
        let message = vec![b'b'; 200];
        let hash = Sha256::digest(&message);

        assert_eq!(hash.len(), 32);
    }

    #[test]
    fn test_binary_data() {
        let data: Vec<u8> = (0..=255).collect();
        let hash = Sha256::digest(&data);

        assert_eq!(hash.len(), 32);
    }

    #[test]
    fn test_helper_functions() {
        assert_eq!(ch(0xF0F0F0F0, 0xFF00FF00, 0x00FF00FF), 0x0FFF0FFF);
        assert_eq!(maj(0xF0F0F0F0, 0xFF00FF00, 0x00FF00FF), 0xF0FFF0F0);
    }

    #[test]
    fn test_collision_resistance() {
        // While we can't test true collision resistance,
        // we can verify different inputs give different outputs
        let hash1 = Sha256::digest(b"message1");
        let hash2 = Sha256::digest(b"message2");
        let hash3 = Sha256::digest(b"message3");

        assert_ne!(hash1, hash2);
        assert_ne!(hash2, hash3);
        assert_ne!(hash1, hash3);
    }
}
