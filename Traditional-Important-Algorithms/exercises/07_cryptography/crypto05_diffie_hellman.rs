// crypto05_diffie_hellman.rs
//
// Diffie-Hellman Key Exchange allows two parties to establish a shared secret
// over an insecure channel without prior communication. This shared secret can
// then be used for symmetric encryption.
//
// How it works:
// 1. Alice and Bob agree on public parameters: prime p and generator g
// 2. Alice generates private key a, computes A = g^a mod p, sends A to Bob
// 3. Bob generates private key b, computes B = g^b mod p, sends B to Alice
// 4. Alice computes shared secret: s = B^a mod p
// 5. Bob computes shared secret: s = A^b mod p
// 6. Both arrive at the same secret: s = g^(ab) mod p
//
// Security basis:
// - Discrete logarithm problem: Given g, p, and g^x mod p, hard to find x
// - Forward secrecy: If long-term keys compromised, past sessions still secure
//
// Your task: Implement Diffie-Hellman key exchange.
//
// Security considerations:
// - Use at least 2048-bit primes in production
// - Vulnerable to man-in-the-middle attacks (needs authentication)
// - Use ephemeral DH (DHE) for forward secrecy
// - Consider Elliptic Curve DH (ECDH) for better performance
// - Validate received public keys to prevent small subgroup attacks
// - Post-quantum: DH is vulnerable to quantum computers

// I AM NOT DONE

pub struct DiffieHellman {
    p: u64,              // Large prime modulus
    g: u64,              // Generator
    private_key: u64,    // Secret key (a or b)
    public_key: u64,     // Public key (g^private mod p)
}

impl DiffieHellman {
    pub fn new(p: u64, g: u64, private_key: u64) -> Self {
        // TODO: Create new DH instance
        // 1. Store p, g, and private_key
        // 2. Calculate public_key = g^private_key mod p
        // 3. Return DiffieHellman struct
        todo!()
    }

    pub fn get_public_key(&self) -> u64 {
        self.public_key
    }

    pub fn compute_shared_secret(&self, other_public_key: u64) -> u64 {
        // TODO: Compute shared secret
        // Calculate: shared_secret = other_public_key^private_key mod p
        // Use modular_exponentiation
        todo!()
    }

    pub fn get_parameters(&self) -> (u64, u64) {
        (self.p, self.g)
    }
}

fn modular_exponentiation(mut base: u64, mut exp: u64, modulus: u64) -> u64 {
    // TODO: Implement efficient modular exponentiation
    // Same algorithm as in previous exercises
    todo!()
}

// Helper to check if a number is prime (simple trial division)
pub fn is_prime(n: u64) -> bool {
    // TODO: Implement primality test
    // 1. If n < 2, return false
    // 2. If n == 2, return true
    // 3. If n is even, return false
    // 4. Check divisibility by odd numbers up to sqrt(n)
    // 5. Return true if no divisors found
    todo!()
}

// Check if g is a valid generator for prime p
pub fn is_generator(g: u64, p: u64) -> bool {
    // TODO: Simplified generator check
    // For a safe prime p = 2q + 1, check that:
    // 1. g > 1 and g < p
    // 2. g^2 mod p != 1
    // 3. g^q mod p != 1 (where q = (p-1)/2)
    // This is simplified; real checks are more comprehensive
    todo!()
}

// Generate a safe prime (p where p = 2q + 1 and q is also prime)
// Note: This is very slow for large numbers; here for educational purposes
pub fn generate_safe_prime(start: u64, limit: u64) -> Option<u64> {
    // TODO: Find a safe prime in range [start, limit]
    // 1. For each candidate p in range
    // 2. Check if p is prime
    // 3. Check if (p-1)/2 is also prime
    // 4. Return first safe prime found
    // Return None if no safe prime found
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_key_exchange() {
        let p = 23u64;  // Prime
        let g = 5u64;   // Generator

        // Alice's side
        let alice = DiffieHellman::new(p, g, 6);  // Private key: 6
        let alice_public = alice.get_public_key();

        // Bob's side
        let bob = DiffieHellman::new(p, g, 15);   // Private key: 15
        let bob_public = bob.get_public_key();

        // Compute shared secrets
        let alice_secret = alice.compute_shared_secret(bob_public);
        let bob_secret = bob.compute_shared_secret(alice_public);

        // Both should arrive at same secret
        assert_eq!(alice_secret, bob_secret);
    }

    #[test]
    fn test_different_private_keys() {
        let p = 23u64;
        let g = 5u64;

        let dh1 = DiffieHellman::new(p, g, 6);
        let dh2 = DiffieHellman::new(p, g, 15);

        // Different private keys should produce different public keys
        assert_ne!(dh1.get_public_key(), dh2.get_public_key());
    }

    #[test]
    fn test_larger_prime() {
        let p = 2003u64;  // Larger prime
        let g = 2u64;

        let alice = DiffieHellman::new(p, g, 123);
        let bob = DiffieHellman::new(p, g, 456);

        let alice_secret = alice.compute_shared_secret(bob.get_public_key());
        let bob_secret = bob.compute_shared_secret(alice.get_public_key());

        assert_eq!(alice_secret, bob_secret);
    }

    #[test]
    fn test_public_keys_are_public() {
        let p = 23u64;
        let g = 5u64;

        let alice = DiffieHellman::new(p, g, 6);
        let bob = DiffieHellman::new(p, g, 15);

        // Public keys can be shared openly
        let alice_public = alice.get_public_key();
        let bob_public = bob.get_public_key();

        assert!(alice_public < p);
        assert!(bob_public < p);
    }

    #[test]
    fn test_modular_exponentiation() {
        assert_eq!(modular_exponentiation(5, 6, 23), 8);
        assert_eq!(modular_exponentiation(5, 15, 23), 19);
        assert_eq!(modular_exponentiation(2, 10, 1000), 24);
    }

    #[test]
    fn test_is_prime() {
        assert!(is_prime(2));
        assert!(is_prime(3));
        assert!(is_prime(23));
        assert!(is_prime(2003));

        assert!(!is_prime(1));
        assert!(!is_prime(4));
        assert!(!is_prime(100));
    }

    #[test]
    fn test_same_private_key() {
        let p = 23u64;
        let g = 5u64;

        let alice = DiffieHellman::new(p, g, 10);
        let bob = DiffieHellman::new(p, g, 10);

        // Same private keys produce same public keys
        assert_eq!(alice.get_public_key(), bob.get_public_key());
    }

    #[test]
    fn test_three_party_exchange() {
        let p = 23u64;
        let g = 5u64;

        let alice = DiffieHellman::new(p, g, 6);
        let bob = DiffieHellman::new(p, g, 15);
        let carol = DiffieHellman::new(p, g, 12);

        // Alice-Bob share secret
        let alice_bob_secret1 = alice.compute_shared_secret(bob.get_public_key());
        let alice_bob_secret2 = bob.compute_shared_secret(alice.get_public_key());
        assert_eq!(alice_bob_secret1, alice_bob_secret2);

        // Alice-Carol share different secret
        let alice_carol_secret1 = alice.compute_shared_secret(carol.get_public_key());
        let alice_carol_secret2 = carol.compute_shared_secret(alice.get_public_key());
        assert_eq!(alice_carol_secret1, alice_carol_secret2);

        // Different pairs should have different secrets
        assert_ne!(alice_bob_secret1, alice_carol_secret1);
    }

    #[test]
    fn test_parameters() {
        let p = 23u64;
        let g = 5u64;

        let dh = DiffieHellman::new(p, g, 6);
        let (p_out, g_out) = dh.get_parameters();

        assert_eq!(p_out, p);
        assert_eq!(g_out, g);
    }

    #[test]
    fn test_is_generator() {
        // For prime 23, generator 5 is valid
        assert!(is_generator(5, 23));

        // 1 is never a generator
        assert!(!is_generator(1, 23));

        // p is never a generator
        assert!(!is_generator(23, 23));
    }

    #[test]
    fn test_generate_safe_prime() {
        // Look for small safe primes
        let safe_prime = generate_safe_prime(5, 50);

        assert!(safe_prime.is_some());
        let p = safe_prime.unwrap();

        // Verify it's prime
        assert!(is_prime(p));

        // Verify (p-1)/2 is also prime
        assert!(is_prime((p - 1) / 2));
    }

    #[test]
    fn test_secret_remains_secret() {
        let p = 2003u64;
        let g = 2u64;

        let alice = DiffieHellman::new(p, g, 123);
        let bob = DiffieHellman::new(p, g, 456);

        let alice_public = alice.get_public_key();
        let bob_public = bob.get_public_key();

        // Eve intercepts public keys but cannot compute shared secret
        // without knowing private keys
        let shared_secret = alice.compute_shared_secret(bob_public);

        // There's no way to compute shared_secret from just p, g,
        // alice_public, and bob_public (discrete log problem)
        assert!(shared_secret < p);
    }
}
