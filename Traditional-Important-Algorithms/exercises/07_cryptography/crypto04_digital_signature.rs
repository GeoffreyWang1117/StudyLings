// crypto04_digital_signature.rs
//
// Digital Signatures provide authentication, integrity, and non-repudiation.
// They prove that a message was created by a specific sender and hasn't been modified.
//
// How it works:
// - Signing: Hash the message, then encrypt hash with private key
// - Verification: Decrypt signature with public key, compare with message hash
//
// Properties:
// - Authentication: Proves who created the signature
// - Integrity: Detects any tampering with the message
// - Non-repudiation: Signer cannot deny signing the message
//
// Common algorithms:
// - RSA signatures (what we'll implement)
// - DSA (Digital Signature Algorithm)
// - ECDSA (Elliptic Curve DSA)
// - EdDSA (Edwards-curve DSA)
//
// Your task: Implement RSA-based digital signatures.
//
// Security considerations:
// - Always hash before signing (never sign raw data)
// - Use PSS padding in production, not raw RSA
// - Verify signatures before trusting any data
// - Protect private signing keys more than encryption keys
// - Use at least 2048-bit keys for RSA (4096 recommended)
// - Consider post-quantum alternatives (e.g., SPHINCS+)

// I AM NOT DONE

#[derive(Debug, Clone, PartialEq)]
pub struct PublicKey {
    pub n: u64,
    pub e: u64,
}

#[derive(Debug, Clone, PartialEq)]
pub struct PrivateKey {
    pub n: u64,
    pub d: u64,
}

pub struct DigitalSignature {
    private_key: PrivateKey,
    public_key: PublicKey,
}

impl DigitalSignature {
    pub fn new(p: u64, q: u64, e: u64) -> Self {
        // TODO: Generate key pair for signing
        // Same process as RSA encryption, but we'll use keys differently
        // 1. Calculate n = p * q
        // 2. Calculate phi = (p-1) * (q-1)
        // 3. Calculate d = mod_inverse(e, phi)
        // 4. Create public and private keys
        todo!()
    }

    pub fn sign(&self, message: &[u8]) -> u64 {
        // TODO: Create digital signature
        // 1. Hash the message using simple_hash
        // 2. Ensure hash < n
        // 3. Sign by computing: signature = hash^d mod n
        // 4. Return signature
        todo!()
    }

    pub fn verify(&self, message: &[u8], signature: u64) -> bool {
        // TODO: Verify digital signature
        // 1. Hash the message
        // 2. Decrypt signature: recovered_hash = signature^e mod n
        // 3. Compare recovered_hash with computed hash
        // 4. Return true if they match
        todo!()
    }

    pub fn get_public_key(&self) -> &PublicKey {
        &self.public_key
    }

    pub fn verify_with_public_key(public_key: &PublicKey, message: &[u8], signature: u64) -> bool {
        // TODO: Verify signature using only public key
        // This allows anyone to verify signatures without access to private key
        // Same as verify() but uses provided public_key
        todo!()
    }
}

// Simple hash function for demonstration (NOT cryptographically secure)
// In production, use SHA-256 or better
fn simple_hash(data: &[u8]) -> u64 {
    // TODO: Implement a simple hash function
    // 1. Initialize hash = 5381 (prime number)
    // 2. For each byte: hash = hash * 33 + byte
    // 3. Return hash
    // This is DJB2 hash - simple but not cryptographic
    todo!()
}

fn modular_exponentiation(mut base: u64, mut exp: u64, modulus: u64) -> u64 {
    // TODO: Same as RSA - implement efficient modular exponentiation
    todo!()
}

fn extended_gcd(a: i64, b: i64) -> (i64, i64, i64) {
    // TODO: Extended Euclidean algorithm
    todo!()
}

fn mod_inverse(a: u64, m: u64) -> Option<u64> {
    // TODO: Calculate modular multiplicative inverse
    todo!()
}

fn gcd(mut a: u64, mut b: u64) -> u64 {
    // TODO: Calculate greatest common divisor
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_signature_creation() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"Hello, World!";

        let signature = signer.sign(message);

        // Signature should be a number
        assert!(signature > 0);
        assert!(signature < p * q);
    }

    #[test]
    fn test_signature_verification() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"Hello, World!";

        let signature = signer.sign(message);
        let valid = signer.verify(message, signature);

        assert!(valid);
    }

    #[test]
    fn test_tampered_message() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"Hello, World!";

        let signature = signer.sign(message);

        // Try to verify with different message
        let tampered = b"Hello, World?";
        let valid = signer.verify(tampered, signature);

        assert!(!valid);
    }

    #[test]
    fn test_different_messages_different_signatures() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);

        let sig1 = signer.sign(b"Message 1");
        let sig2 = signer.sign(b"Message 2");

        assert_ne!(sig1, sig2);
    }

    #[test]
    fn test_verify_with_public_key_only() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"Public message";

        let signature = signer.sign(message);
        let public_key = signer.get_public_key().clone();

        // Verify using only public key (what recipients do)
        let valid = DigitalSignature::verify_with_public_key(&public_key, message, signature);

        assert!(valid);
    }

    #[test]
    fn test_invalid_signature() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"Test message";

        let signature = signer.sign(message);

        // Try with wrong signature
        let valid = signer.verify(message, signature + 1);

        assert!(!valid);
    }

    #[test]
    fn test_empty_message() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"";

        let signature = signer.sign(message);
        let valid = signer.verify(message, signature);

        assert!(valid);
    }

    #[test]
    fn test_long_message() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"This is a much longer message that will be hashed before signing. \
                        The hash allows us to sign messages of any length.";

        let signature = signer.sign(message);
        let valid = signer.verify(message, signature);

        assert!(valid);
    }

    #[test]
    fn test_deterministic_signatures() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"Deterministic test";

        let sig1 = signer.sign(message);
        let sig2 = signer.sign(message);

        // Same message should produce same signature
        assert_eq!(sig1, sig2);
    }

    #[test]
    fn test_simple_hash_function() {
        let hash1 = simple_hash(b"test");
        let hash2 = simple_hash(b"test");
        let hash3 = simple_hash(b"Test");

        // Same input produces same hash
        assert_eq!(hash1, hash2);

        // Different input produces different hash
        assert_ne!(hash1, hash3);
    }

    #[test]
    fn test_multiple_signers() {
        let p1 = 61u64;
        let q1 = 53u64;

        let p2 = 67u64;
        let q2 = 71u64;

        let e = 17u64;

        let signer1 = DigitalSignature::new(p1, q1, e);
        let signer2 = DigitalSignature::new(p2, q2, e);

        let message = b"Test message";

        let sig1 = signer1.sign(message);
        let sig2 = signer2.sign(message);

        // Different signers produce different signatures
        assert_ne!(sig1, sig2);

        // Each signer can verify their own signature
        assert!(signer1.verify(message, sig1));
        assert!(signer2.verify(message, sig2));

        // But not each other's
        assert!(!signer1.verify(message, sig2));
        assert!(!signer2.verify(message, sig1));
    }

    #[test]
    fn test_non_repudiation() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let signer = DigitalSignature::new(p, q, e);
        let message = b"I agree to the terms";

        let signature = signer.sign(message);

        // Anyone with public key can verify
        let public_key = signer.get_public_key().clone();
        let verified = DigitalSignature::verify_with_public_key(&public_key, message, signature);

        assert!(verified);
        // The signer cannot deny signing this message (non-repudiation)
    }
}
