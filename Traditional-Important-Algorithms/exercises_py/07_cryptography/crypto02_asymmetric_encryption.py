# I AM NOT DONE

"""
crypto02_asymmetric_encryption.py

Asymmetric Encryption (Public Key Cryptography) uses a pair of keys:
- Public key: Can be shared freely, used for encryption
- Private key: Must be kept secret, used for decryption

RSA (Rivest-Shamir-Adleman) is the most widely used asymmetric algorithm.

Key concepts:
- Key generation: Choose two large primes p and q
- Public key: (n, e) where n = p*q and e is public exponent
- Private key: (n, d) where d is private exponent
- Encryption: c = m^e mod n
- Decryption: m = c^d mod n

Your task: Implement simplified RSA with small numbers.

Security considerations:
- Real RSA uses 2048-4096 bit keys (we use small numbers for learning)
- Never encrypt messages larger than key size without padding
- Use OAEP padding in production, not raw RSA
- Protect private keys with strong access controls
- Use RSA for key exchange, not bulk encryption (too slow)
"""

import unittest
from typing import Optional, Tuple


class PublicKey:
    """RSA public key."""

    def __init__(self, n: int, e: int):
        self.n = n  # modulus
        self.e = e  # public exponent

    def __eq__(self, other):
        return isinstance(other, PublicKey) and self.n == other.n and self.e == other.e


class PrivateKey:
    """RSA private key."""

    def __init__(self, n: int, d: int):
        self.n = n  # modulus
        self.d = d  # private exponent

    def __eq__(self, other):
        return isinstance(other, PrivateKey) and self.n == other.n and self.d == other.d


class RSA:
    """Simplified RSA encryption implementation."""

    def __init__(self, p: int, q: int, e: int):
        """
        TODO: Generate RSA key pair.
        1. Calculate n = p * q
        2. Calculate phi = (p-1) * (q-1)
        3. Verify gcd(e, phi) = 1
        4. Calculate d = mod_inverse(e, phi)
        5. Create PublicKey and PrivateKey
        """
        pass

    def encrypt(self, message: int) -> int:
        """
        TODO: Encrypt message with public key.
        1. Verify message < n
        2. Calculate ciphertext = message^e mod n
        Use modular_exponentiation helper function
        Raises ValueError if message >= n
        """
        pass

    def decrypt(self, ciphertext: int) -> int:
        """
        TODO: Decrypt ciphertext with private key.
        Calculate message = ciphertext^d mod n
        Use modular_exponentiation helper function
        """
        pass

    def get_public_key(self) -> PublicKey:
        """Return the public key."""
        return self.public_key

    def get_private_key(self) -> PrivateKey:
        """Return the private key."""
        return self.private_key

    @staticmethod
    def encrypt_with_public_key(public_key: PublicKey, message: int) -> int:
        """
        TODO: Encrypt using only public key (for external users).
        This allows encryption without access to private key.
        Raises ValueError if message >= n
        """
        pass


def modular_exponentiation(base: int, exp: int, modulus: int) -> int:
    """
    TODO: Implement efficient modular exponentiation using binary method.
    1. Initialize result = 1
    2. While exp > 0:
       - If exp is odd: result = (result * base) % modulus
       - base = (base * base) % modulus
       - exp = exp // 2
    3. Return result
    This prevents overflow and is efficient for large exponents.
    """
    pass


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    TODO: Implement extended GCD.
    Returns (gcd, x, y) where gcd = a*x + b*y
    Base case: if b == 0, return (a, 1, 0)
    Recursive case: compute gcd(b, a % b)
    """
    pass


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    TODO: Calculate modular multiplicative inverse of a mod m.
    Use extended_gcd to find x such that a*x ≡ 1 (mod m)
    Return None if inverse doesn't exist (when gcd(a,m) != 1)
    """
    pass


def gcd(a: int, b: int) -> int:
    """
    TODO: Implement Euclidean algorithm for GCD.
    While b != 0:
      temp = b
      b = a % b
      a = temp
    Return a
    """
    pass


class TestRSA(unittest.TestCase):
    """Comprehensive test cases for RSA implementation."""

    def test_gcd(self):
        """Test GCD calculation."""
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(17, 19), 1)
        self.assertEqual(gcd(100, 50), 50)

    def test_modular_exponentiation(self):
        """Test modular exponentiation."""
        self.assertEqual(modular_exponentiation(2, 10, 1000), 24)
        self.assertEqual(modular_exponentiation(3, 5, 7), 5)
        self.assertEqual(modular_exponentiation(7, 3, 13), 5)

    def test_extended_gcd(self):
        """Test extended GCD."""
        g, x, y = extended_gcd(30, 20)
        self.assertEqual(g, 10)
        self.assertEqual(30 * x + 20 * y, g)

    def test_mod_inverse(self):
        """Test modular multiplicative inverse."""
        # 3 * 7 ≡ 1 (mod 10)
        self.assertEqual(mod_inverse(3, 10), 7)

        # 17 * 233 ≡ 1 (mod 3120)
        inv = mod_inverse(17, 3120)
        self.assertIsNotNone(inv)
        self.assertEqual((17 * inv) % 3120, 1)

    def test_mod_inverse_no_inverse(self):
        """Test that mod_inverse returns None when no inverse exists."""
        # 2 and 4 are not coprime, no inverse exists
        self.assertIsNone(mod_inverse(2, 4))

    def test_rsa_key_generation(self):
        """Test RSA key generation."""
        p = 61
        q = 53
        e = 17

        rsa = RSA(p, q, e)

        self.assertEqual(rsa.get_public_key().n, p * q)
        self.assertEqual(rsa.get_public_key().e, e)

    def test_rsa_encrypt_decrypt(self):
        """Test RSA encryption and decryption."""
        p = 61
        q = 53
        e = 17

        rsa = RSA(p, q, e)

        message = 42
        ciphertext = rsa.encrypt(message)

        self.assertNotEqual(ciphertext, message)

        decrypted = rsa.decrypt(ciphertext)
        self.assertEqual(decrypted, message)

    def test_rsa_different_messages(self):
        """Test that different messages produce different ciphertexts."""
        p = 61
        q = 53
        e = 17

        rsa = RSA(p, q, e)

        ct1 = rsa.encrypt(100)
        ct2 = rsa.encrypt(200)

        self.assertNotEqual(ct1, ct2)

    def test_rsa_message_too_large(self):
        """Test that encrypting a message larger than n fails."""
        p = 61
        q = 53
        e = 17

        rsa = RSA(p, q, e)

        # Message larger than n should fail
        with self.assertRaises(ValueError):
            rsa.encrypt(rsa.get_public_key().n + 1)

    def test_encrypt_with_public_key_only(self):
        """Test encryption using only the public key."""
        p = 61
        q = 53
        e = 17

        rsa = RSA(p, q, e)
        public_key = rsa.get_public_key()

        message = 123
        ciphertext = RSA.encrypt_with_public_key(public_key, message)

        decrypted = rsa.decrypt(ciphertext)
        self.assertEqual(decrypted, message)

    def test_rsa_zero_message(self):
        """Test RSA with zero message."""
        p = 61
        q = 53
        e = 17

        rsa = RSA(p, q, e)

        ciphertext = rsa.encrypt(0)
        decrypted = rsa.decrypt(ciphertext)

        self.assertEqual(decrypted, 0)

    def test_rsa_deterministic(self):
        """Test that RSA without padding is deterministic."""
        p = 61
        q = 53
        e = 17

        rsa = RSA(p, q, e)

        message = 42
        ct1 = rsa.encrypt(message)
        ct2 = rsa.encrypt(message)

        # RSA without padding is deterministic
        self.assertEqual(ct1, ct2)


if __name__ == '__main__':
    unittest.main()
