// crypto06_mac.rs
//
// Message Authentication Code (MAC) provides authentication and integrity.
// Unlike digital signatures, MACs use symmetric keys (shared secret).
//
// HMAC (Hash-based Message Authentication Code) is the most common MAC:
// - Combines a hash function with a secret key
// - Provides authentication (proves sender knows the key)
// - Provides integrity (detects tampering)
// - Does NOT provide non-repudiation (both parties have same key)
//
// HMAC construction:
// HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
// where:
// - H is a hash function (e.g., SHA-256)
// - K is the secret key
// - m is the message
// - opad = 0x5c repeated
// - ipad = 0x36 repeated
// - || is concatenation
// - ⊕ is XOR
//
// Your task: Implement HMAC with a simple hash function.
//
// Security considerations:
// - HMAC is more secure than simple Hash(key || message)
// - Resistant to length extension attacks
// - Use with SHA-256 or better (not MD5 or SHA-1)
// - Key should be at least as long as hash output
// - Always use constant-time comparison to prevent timing attacks
// - MACs don't encrypt data, only authenticate it

// I AM NOT DONE

const BLOCK_SIZE: usize = 64;
const HASH_SIZE: usize = 32;

pub struct Hmac {
    key: Vec<u8>,
}

impl Hmac {
    pub fn new(key: &[u8]) -> Self {
        // TODO: Create HMAC instance with key
        // 1. If key is longer than BLOCK_SIZE, hash it first
        // 2. If key is shorter than BLOCK_SIZE, pad with zeros
        // 3. Store the processed key
        todo!()
    }

    pub fn compute(&self, message: &[u8]) -> Vec<u8> {
        // TODO: Compute HMAC
        // 1. Create inner_key = key ⊕ ipad (0x36 repeated)
        // 2. Create outer_key = key ⊕ opad (0x5c repeated)
        // 3. Compute inner_hash = hash(inner_key || message)
        // 4. Compute hmac = hash(outer_key || inner_hash)
        // 5. Return hmac
        todo!()
    }

    pub fn verify(&self, message: &[u8], mac: &[u8]) -> bool {
        // TODO: Verify HMAC in constant time
        // 1. Compute expected MAC
        // 2. Use constant_time_compare to compare with provided MAC
        // 3. Return true if they match
        todo!()
    }

    pub fn sign_and_encrypt(key: &[u8], encryption_key: &[u8], message: &[u8]) -> (Vec<u8>, Vec<u8>) {
        // TODO: Demonstrate encrypt-then-MAC (secure composition)
        // 1. Encrypt message using simple_encrypt with encryption_key
        // 2. Compute MAC of ciphertext using key
        // 3. Return (ciphertext, mac)
        // Note: This is the SECURE way (MAC the ciphertext, not plaintext)
        todo!()
    }

    pub fn verify_and_decrypt(
        key: &[u8],
        encryption_key: &[u8],
        ciphertext: &[u8],
        mac: &[u8],
    ) -> Result<Vec<u8>, &'static str> {
        // TODO: Verify then decrypt
        // 1. First verify MAC of ciphertext
        // 2. Only decrypt if MAC is valid
        // 3. Return decrypted message or error
        // This prevents padding oracle attacks
        todo!()
    }
}

// Simple hash function (NOT cryptographically secure - for demonstration only)
fn simple_hash(data: &[u8]) -> Vec<u8> {
    // TODO: Implement a simple hash
    // Use DJB2 algorithm extended to produce HASH_SIZE bytes
    // 1. Initialize state with different seeds for each output byte
    // 2. Process all input data
    // 3. Return HASH_SIZE bytes
    todo!()
}

// Constant-time comparison to prevent timing attacks
fn constant_time_compare(a: &[u8], b: &[u8]) -> bool {
    // TODO: Compare two byte slices in constant time
    // 1. If lengths differ, return false (but still check all bytes)
    // 2. XOR all corresponding bytes and OR results
    // 3. Return true only if result is 0
    // IMPORTANT: Must take same time regardless of where difference occurs
    todo!()
}

// Simple XOR-based encryption (NOT secure - for demonstration only)
fn simple_encrypt(key: &[u8], plaintext: &[u8]) -> Vec<u8> {
    // TODO: XOR encryption
    // Repeat key to match plaintext length and XOR
    todo!()
}

fn simple_decrypt(key: &[u8], ciphertext: &[u8]) -> Vec<u8> {
    // TODO: XOR decryption (same as encryption for XOR)
    simple_encrypt(key, ciphertext)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hmac_creation() {
        let key = b"secret key";
        let hmac = Hmac::new(key);

        // Should create successfully
        assert!(hmac.key.len() == BLOCK_SIZE);
    }

    #[test]
    fn test_hmac_compute() {
        let key = b"secret key";
        let hmac = Hmac::new(key);

        let message = b"Hello, World!";
        let mac = hmac.compute(message);

        assert_eq!(mac.len(), HASH_SIZE);
    }

    #[test]
    fn test_hmac_deterministic() {
        let key = b"secret key";
        let hmac = Hmac::new(key);

        let message = b"Test message";
        let mac1 = hmac.compute(message);
        let mac2 = hmac.compute(message);

        assert_eq!(mac1, mac2);
    }

    #[test]
    fn test_different_messages_different_macs() {
        let key = b"secret key";
        let hmac = Hmac::new(key);

        let mac1 = hmac.compute(b"Message 1");
        let mac2 = hmac.compute(b"Message 2");

        assert_ne!(mac1, mac2);
    }

    #[test]
    fn test_different_keys_different_macs() {
        let message = b"Same message";

        let hmac1 = Hmac::new(b"key1");
        let hmac2 = Hmac::new(b"key2");

        let mac1 = hmac1.compute(message);
        let mac2 = hmac2.compute(message);

        assert_ne!(mac1, mac2);
    }

    #[test]
    fn test_hmac_verify_valid() {
        let key = b"secret key";
        let hmac = Hmac::new(key);

        let message = b"Authenticated message";
        let mac = hmac.compute(message);

        assert!(hmac.verify(message, &mac));
    }

    #[test]
    fn test_hmac_verify_invalid_mac() {
        let key = b"secret key";
        let hmac = Hmac::new(key);

        let message = b"Test message";
        let mut mac = hmac.compute(message);

        // Tamper with MAC
        mac[0] ^= 0x01;

        assert!(!hmac.verify(message, &mac));
    }

    #[test]
    fn test_hmac_verify_tampered_message() {
        let key = b"secret key";
        let hmac = Hmac::new(key);

        let message = b"Original message";
        let mac = hmac.compute(message);

        let tampered = b"Tampered message";

        assert!(!hmac.verify(tampered, &mac));
    }

    #[test]
    fn test_constant_time_compare() {
        let a = vec![1, 2, 3, 4, 5];
        let b = vec![1, 2, 3, 4, 5];
        let c = vec![1, 2, 3, 4, 6];

        assert!(constant_time_compare(&a, &b));
        assert!(!constant_time_compare(&a, &c));
    }

    #[test]
    fn test_encrypt_then_mac() {
        let mac_key = b"mac key";
        let enc_key = b"encryption key";
        let message = b"Secret message";

        let (ciphertext, mac) = Hmac::sign_and_encrypt(mac_key, enc_key, message);

        // Ciphertext should be different from plaintext
        assert_ne!(ciphertext.as_slice(), message);

        // MAC should be HASH_SIZE bytes
        assert_eq!(mac.len(), HASH_SIZE);
    }

    #[test]
    fn test_verify_and_decrypt_success() {
        let mac_key = b"mac key";
        let enc_key = b"encryption key";
        let message = b"Secret message";

        let (ciphertext, mac) = Hmac::sign_and_encrypt(mac_key, enc_key, message);

        let decrypted = Hmac::verify_and_decrypt(mac_key, enc_key, &ciphertext, &mac).unwrap();

        assert_eq!(decrypted.as_slice(), message);
    }

    #[test]
    fn test_verify_and_decrypt_invalid_mac() {
        let mac_key = b"mac key";
        let enc_key = b"encryption key";
        let message = b"Secret message";

        let (ciphertext, mut mac) = Hmac::sign_and_encrypt(mac_key, enc_key, message);

        // Tamper with MAC
        mac[0] ^= 0x01;

        let result = Hmac::verify_and_decrypt(mac_key, enc_key, &ciphertext, &mac);

        assert!(result.is_err());
    }

    #[test]
    fn test_long_key_handling() {
        // Key longer than BLOCK_SIZE should be hashed
        let long_key = vec![0x42; BLOCK_SIZE + 10];
        let hmac = Hmac::new(&long_key);

        let message = b"Test";
        let mac = hmac.compute(message);

        assert_eq!(mac.len(), HASH_SIZE);
    }

    #[test]
    fn test_empty_message() {
        let key = b"secret key";
        let hmac = Hmac::new(key);

        let mac = hmac.compute(b"");

        assert_eq!(mac.len(), HASH_SIZE);
        assert!(hmac.verify(b"", &mac));
    }
}
