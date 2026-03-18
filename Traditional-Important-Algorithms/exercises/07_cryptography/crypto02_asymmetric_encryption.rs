// crypto02_asymmetric_encryption.rs
//
// Asymmetric Encryption (Public Key Cryptography) uses a pair of keys:
// - Public key: Can be shared freely, used for encryption
// - Private key: Must be kept secret, used for decryption
//
// RSA (Rivest-Shamir-Adleman) is the most widely used asymmetric algorithm.
//
// Key concepts:
// - Key generation: Choose two large primes p and q
// - Public key: (n, e) where n = p*q and e is public exponent
// - Private key: (n, d) where d is private exponent
// - Encryption: c = m^e mod n
// - Decryption: m = c^d mod n
//
// Your task: Implement simplified RSA with small numbers.
//
// Security considerations:
// - Real RSA uses 2048-4096 bit keys (we use small numbers for learning)
// - Never encrypt messages larger than key size without padding
// - Use OAEP padding in production, not raw RSA
// - Protect private keys with strong access controls
// - Use RSA for key exchange, not bulk encryption (too slow)

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub struct PublicKey {
    pub n: u64,  // modulus
    pub e: u64,  // public exponent
}

#[derive(Debug, Clone, PartialEq)]
pub struct PrivateKey {
    pub n: u64,  // modulus
    pub d: u64,  // private exponent
}

pub struct Rsa {
    public_key: PublicKey,
    private_key: PrivateKey,
}

impl Rsa {
    pub fn new(p: u64, q: u64, e: u64) -> Self {
        // TODO: Generate RSA key pair
        // 1. Calculate n = p * q
        // 2. Calculate phi = (p-1) * (q-1)
        // 3. Verify gcd(e, phi) = 1
        // 4. Calculate d = mod_inverse(e, phi)
        // 5. Create PublicKey and PrivateKey
        todo!()
    }

    pub fn encrypt(&self, message: u64) -> Result<u64, &'static str> {
        // TODO: Encrypt message with public key
        // 1. Verify message < n
        // 2. Calculate ciphertext = message^e mod n
        // Use modular_exponentiation helper function
        todo!()
    }

    pub fn decrypt(&self, ciphertext: u64) -> u64 {
        // TODO: Decrypt ciphertext with private key
        // Calculate message = ciphertext^d mod n
        // Use modular_exponentiation helper function
        todo!()
    }

    pub fn get_public_key(&self) -> &PublicKey {
        &self.public_key
    }

    pub fn get_private_key(&self) -> &PrivateKey {
        &self.private_key
    }

    pub fn encrypt_with_public_key(public_key: &PublicKey, message: u64) -> Result<u64, &'static str> {
        // TODO: Encrypt using only public key (for external users)
        // This allows encryption without access to private key
        todo!()
    }
}

// Helper function for modular exponentiation: (base^exp) mod m
fn modular_exponentiation(mut base: u64, mut exp: u64, modulus: u64) -> u64 {
    // TODO: Implement efficient modular exponentiation using binary method
    // 1. Initialize result = 1
    // 2. While exp > 0:
    //    - If exp is odd: result = (result * base) % modulus
    //    - base = (base * base) % modulus
    //    - exp = exp / 2
    // 3. Return result
    // This prevents overflow and is efficient for large exponents
    todo!()
}

// Extended Euclidean algorithm to find modular inverse
fn extended_gcd(a: i64, b: i64) -> (i64, i64, i64) {
    // TODO: Implement extended GCD
    // Returns (gcd, x, y) where gcd = a*x + b*y
    // Base case: if b == 0, return (a, 1, 0)
    // Recursive case: compute gcd(b, a % b)
    todo!()
}

fn mod_inverse(a: u64, m: u64) -> Option<u64> {
    // TODO: Calculate modular multiplicative inverse of a mod m
    // Use extended_gcd to find x such that a*x ≡ 1 (mod m)
    // Return None if inverse doesn't exist (when gcd(a,m) != 1)
    todo!()
}

fn gcd(mut a: u64, mut b: u64) -> u64 {
    // TODO: Implement Euclidean algorithm for GCD
    // While b != 0:
    //   temp = b
    //   b = a % b
    //   a = temp
    // Return a
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gcd() {
        assert_eq!(gcd(48, 18), 6);
        assert_eq!(gcd(17, 19), 1);
        assert_eq!(gcd(100, 50), 50);
    }

    #[test]
    fn test_modular_exponentiation() {
        assert_eq!(modular_exponentiation(2, 10, 1000), 24);
        assert_eq!(modular_exponentiation(3, 5, 7), 5);
        assert_eq!(modular_exponentiation(7, 3, 13), 5);
    }

    #[test]
    fn test_extended_gcd() {
        let (g, x, y) = extended_gcd(30, 20);
        assert_eq!(g, 10);
        assert_eq!(30 * x + 20 * y, g);
    }

    #[test]
    fn test_mod_inverse() {
        // 3 * 7 ≡ 1 (mod 10)
        assert_eq!(mod_inverse(3, 10), Some(7));

        // 17 * 233 ≡ 1 (mod 3120)
        let inv = mod_inverse(17, 3120).unwrap();
        assert_eq!((17 * inv) % 3120, 1);
    }

    #[test]
    fn test_mod_inverse_no_inverse() {
        // 2 and 4 are not coprime, no inverse exists
        assert_eq!(mod_inverse(2, 4), None);
    }

    #[test]
    fn test_rsa_key_generation() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let rsa = Rsa::new(p, q, e);

        assert_eq!(rsa.get_public_key().n, p * q);
        assert_eq!(rsa.get_public_key().e, e);
    }

    #[test]
    fn test_rsa_encrypt_decrypt() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let rsa = Rsa::new(p, q, e);

        let message = 42u64;
        let ciphertext = rsa.encrypt(message).unwrap();

        assert_ne!(ciphertext, message);

        let decrypted = rsa.decrypt(ciphertext);
        assert_eq!(decrypted, message);
    }

    #[test]
    fn test_rsa_different_messages() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let rsa = Rsa::new(p, q, e);

        let ct1 = rsa.encrypt(100).unwrap();
        let ct2 = rsa.encrypt(200).unwrap();

        assert_ne!(ct1, ct2);
    }

    #[test]
    fn test_rsa_message_too_large() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let rsa = Rsa::new(p, q, e);

        // Message larger than n should fail
        let result = rsa.encrypt(rsa.get_public_key().n + 1);
        assert!(result.is_err());
    }

    #[test]
    fn test_encrypt_with_public_key_only() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let rsa = Rsa::new(p, q, e);
        let public_key = rsa.get_public_key().clone();

        let message = 123u64;
        let ciphertext = Rsa::encrypt_with_public_key(&public_key, message).unwrap();

        let decrypted = rsa.decrypt(ciphertext);
        assert_eq!(decrypted, message);
    }

    #[test]
    fn test_rsa_zero_message() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let rsa = Rsa::new(p, q, e);

        let ciphertext = rsa.encrypt(0).unwrap();
        let decrypted = rsa.decrypt(ciphertext);

        assert_eq!(decrypted, 0);
    }

    #[test]
    fn test_rsa_deterministic() {
        let p = 61u64;
        let q = 53u64;
        let e = 17u64;

        let rsa = Rsa::new(p, q, e);

        let message = 42u64;
        let ct1 = rsa.encrypt(message).unwrap();
        let ct2 = rsa.encrypt(message).unwrap();

        // RSA without padding is deterministic
        assert_eq!(ct1, ct2);
    }
}
