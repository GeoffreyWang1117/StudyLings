// crypto07_password_hashing.rs
//
// Password Hashing is critical for secure password storage. Never store passwords
// in plaintext or with simple hashes like SHA-256!
//
// Key concepts:
// - Salt: Random data added to password before hashing (prevents rainbow tables)
// - Iteration count (cost factor): Slow down brute force attacks
// - Memory-hard functions: Resist GPU/ASIC attacks (bcrypt, scrypt, Argon2)
// - Pepper: Optional secret added server-side (not stored with hash)
//
// Modern algorithms:
// - Argon2: Winner of Password Hashing Competition (recommended)
// - bcrypt: Widely used, good choice
// - scrypt: Memory-hard, good for preventing hardware attacks
// - PBKDF2: Older but still acceptable with high iteration count
//
// NEVER use: MD5, SHA-1, SHA-256 without iterations, or unsalted hashes
//
// Your task: Implement a password hashing system with salt and iterations.
//
// Security considerations:
// - Always use unique salt per password (never reuse)
// - Store salt alongside hash (it's not secret)
// - Use high iteration count (100,000+ for PBKDF2, tune for ~100ms)
// - Increase iterations over time as hardware improves
// - Use constant-time comparison when verifying passwords
// - Consider using a pepper (application-level secret)
// - For new systems, prefer Argon2id

// I AM NOT DONE

const SALT_SIZE: usize = 16;
const HASH_SIZE: usize = 32;
const DEFAULT_ITERATIONS: usize = 10000;

pub struct PasswordHash {
    pub hash: Vec<u8>,
    pub salt: Vec<u8>,
    pub iterations: usize,
}

impl PasswordHash {
    pub fn to_string(&self) -> String {
        // TODO: Serialize to string format (similar to bcrypt format)
        // Format: $iterations$salt$hash (all in hex)
        // Example: $10000$0123456789abcdef$fedcba9876543210...
        todo!()
    }

    pub fn from_string(s: &str) -> Result<Self, &'static str> {
        // TODO: Deserialize from string format
        // Parse the $iterations$salt$hash format
        // Return error if format is invalid
        todo!()
    }
}

pub struct PasswordHasher {
    iterations: usize,
    pepper: Option<Vec<u8>>,
}

impl PasswordHasher {
    pub fn new(iterations: usize) -> Self {
        Self {
            iterations,
            pepper: None,
        }
    }

    pub fn with_pepper(iterations: usize, pepper: Vec<u8>) -> Self {
        Self {
            iterations,
            pepper: Some(pepper),
        }
    }

    pub fn hash_password(&self, password: &str) -> PasswordHash {
        // TODO: Hash password with salt
        // 1. Generate random salt using generate_salt()
        // 2. Combine password with pepper if present
        // 3. Apply PBKDF2-like algorithm: hash repeatedly with salt
        // 4. Return PasswordHash with hash, salt, and iterations
        todo!()
    }

    pub fn verify_password(&self, password: &str, stored_hash: &PasswordHash) -> bool {
        // TODO: Verify password against stored hash
        // 1. Extract salt and iterations from stored_hash
        // 2. Hash the provided password with same salt and iterations
        // 3. Use constant_time_compare to compare hashes
        // 4. Return true if they match
        todo!()
    }

    pub fn needs_rehash(&self, stored_hash: &PasswordHash) -> bool {
        // TODO: Check if password needs rehashing (iterations too low)
        // Return true if stored_hash.iterations < self.iterations
        todo!()
    }
}

fn generate_salt() -> Vec<u8> {
    // TODO: Generate cryptographically secure random salt
    // Use simple pseudo-random for this exercise
    // In production, use a CSPRNG like rand::thread_rng()
    use std::collections::hash_map::RandomState;
    use std::hash::{BuildHasher, Hasher};

    let mut salt = Vec::with_capacity(SALT_SIZE);
    for i in 0..SALT_SIZE {
        let state = RandomState::new();
        let mut hasher = state.build_hasher();
        hasher.write_usize(i);
        hasher.write_u64(std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64);
        salt.push((hasher.finish() & 0xFF) as u8);
    }
    salt
}

fn pbkdf2(password: &[u8], salt: &[u8], iterations: usize) -> Vec<u8> {
    // TODO: Implement PBKDF2-like key derivation
    // 1. Combine password and salt
    // 2. Hash the combination
    // 3. For each iteration: hash = hash(previous_hash || password || salt)
    // 4. Return final hash
    todo!()
}

fn simple_hash(data: &[u8]) -> Vec<u8> {
    // TODO: Simple hash function (same as previous exercises)
    // Return HASH_SIZE bytes
    todo!()
}

fn constant_time_compare(a: &[u8], b: &[u8]) -> bool {
    // TODO: Constant-time comparison
    // Same implementation as in MAC exercise
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hash_password() {
        let hasher = PasswordHasher::new(1000);
        let password = "mySecurePassword123!";

        let hash = hasher.hash_password(password);

        assert_eq!(hash.salt.len(), SALT_SIZE);
        assert_eq!(hash.hash.len(), HASH_SIZE);
        assert_eq!(hash.iterations, 1000);
    }

    #[test]
    fn test_verify_correct_password() {
        let hasher = PasswordHasher::new(1000);
        let password = "correctPassword";

        let hash = hasher.hash_password(password);
        let is_valid = hasher.verify_password(password, &hash);

        assert!(is_valid);
    }

    #[test]
    fn test_verify_incorrect_password() {
        let hasher = PasswordHasher::new(1000);
        let password = "correctPassword";

        let hash = hasher.hash_password(password);
        let is_valid = hasher.verify_password("wrongPassword", &hash);

        assert!(!is_valid);
    }

    #[test]
    fn test_different_salts() {
        let hasher = PasswordHasher::new(1000);
        let password = "samePassword";

        let hash1 = hasher.hash_password(password);
        let hash2 = hasher.hash_password(password);

        // Same password should produce different hashes due to different salts
        assert_ne!(hash1.salt, hash2.salt);
        assert_ne!(hash1.hash, hash2.hash);
    }

    #[test]
    fn test_salt_uniqueness() {
        let salt1 = generate_salt();
        let salt2 = generate_salt();

        // Each salt should be unique
        assert_ne!(salt1, salt2);
    }

    #[test]
    fn test_password_hash_serialization() {
        let hasher = PasswordHasher::new(5000);
        let password = "testPassword";

        let hash = hasher.hash_password(password);
        let serialized = hash.to_string();

        // Should contain $ separators
        assert!(serialized.contains('$'));
    }

    #[test]
    fn test_password_hash_deserialization() {
        let hasher = PasswordHasher::new(5000);
        let password = "testPassword";

        let hash = hasher.hash_password(password);
        let serialized = hash.to_string();
        let deserialized = PasswordHash::from_string(&serialized).unwrap();

        assert_eq!(hash.iterations, deserialized.iterations);
        assert_eq!(hash.salt, deserialized.salt);
        assert_eq!(hash.hash, deserialized.hash);
    }

    #[test]
    fn test_needs_rehash() {
        let hasher_low = PasswordHasher::new(1000);
        let hasher_high = PasswordHasher::new(10000);

        let password = "testPassword";
        let hash = hasher_low.hash_password(password);

        // Higher iteration hasher should indicate rehash needed
        assert!(hasher_high.needs_rehash(&hash));

        // Same iteration hasher should not need rehash
        assert!(!hasher_low.needs_rehash(&hash));
    }

    #[test]
    fn test_with_pepper() {
        let pepper = b"application_secret_pepper".to_vec();
        let hasher = PasswordHasher::with_pepper(1000, pepper);

        let password = "testPassword";
        let hash = hasher.hash_password(password);

        // Should verify with same hasher (has pepper)
        assert!(hasher.verify_password(password, &hash));

        // Should NOT verify with hasher without pepper
        let hasher_no_pepper = PasswordHasher::new(1000);
        assert!(!hasher_no_pepper.verify_password(password, &hash));
    }

    #[test]
    fn test_iteration_count_matters() {
        let password = "test";
        let salt = vec![0x01; SALT_SIZE];

        let hash1 = pbkdf2(password.as_bytes(), &salt, 100);
        let hash2 = pbkdf2(password.as_bytes(), &salt, 1000);

        // Different iteration counts should produce different hashes
        assert_ne!(hash1, hash2);
    }

    #[test]
    fn test_empty_password() {
        let hasher = PasswordHasher::new(1000);
        let password = "";

        let hash = hasher.hash_password(password);
        assert!(hasher.verify_password(password, &hash));
    }

    #[test]
    fn test_long_password() {
        let hasher = PasswordHasher::new(1000);
        let password = "a".repeat(1000);

        let hash = hasher.hash_password(&password);
        assert!(hasher.verify_password(&password, &hash));
        assert!(!hasher.verify_password("wrong", &hash));
    }

    #[test]
    fn test_special_characters() {
        let hasher = PasswordHasher::new(1000);
        let password = "p@ssw0rd!#$%^&*()_+-=[]{}|;:,.<>?";

        let hash = hasher.hash_password(password);
        assert!(hasher.verify_password(password, &hash));
    }
}
