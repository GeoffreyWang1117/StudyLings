# I AM NOT DONE

"""
crypto04_digital_signature.py

Digital Signatures provide authentication, integrity, and non-repudiation.
They prove that a message was created by a specific sender and hasn't been modified.

How it works:
- Signing: Hash the message, then encrypt hash with private key
- Verification: Decrypt signature with public key, compare with message hash

Properties:
- Authentication: Proves who created the signature
- Integrity: Detects any tampering with the message
- Non-repudiation: Signer cannot deny signing the message

Common algorithms:
- RSA signatures (what we'll implement)
- DSA (Digital Signature Algorithm)
- ECDSA (Elliptic Curve DSA)
- EdDSA (Edwards-curve DSA)

Your task: Implement RSA-based digital signatures.

Security considerations:
- Always hash before signing (never sign raw data)
- Use PSS padding in production, not raw RSA
- Verify signatures before trusting any data
- Protect private signing keys more than encryption keys
- Use at least 2048-bit keys for RSA (4096 recommended)
- Consider post-quantum alternatives (e.g., SPHINCS+)
"""

import unittest
from typing import Optional, Tuple


class PublicKey:
    """RSA public key for signature verification."""

    def __init__(self, n: int, e: int):
        self.n = n
        self.e = e

    def __eq__(self, other):
        return isinstance(other, PublicKey) and self.n == other.n and self.e == other.e


class PrivateKey:
    """RSA private key for signing."""

    def __init__(self, n: int, d: int):
        self.n = n
        self.d = d


class DigitalSignature:
    """RSA-based digital signature implementation."""

    def __init__(self, p: int, q: int, e: int):
        """
        TODO: Generate key pair for signing.
        Same process as RSA encryption, but we'll use keys differently.
        1. Calculate n = p * q
        2. Calculate phi = (p-1) * (q-1)
        3. Calculate d = mod_inverse(e, phi)
        4. Create public and private keys
        """
        pass

    def sign(self, message: bytes) -> int:
        """
        TODO: Create digital signature.
        1. Hash the message using simple_hash
        2. Ensure hash < n
        3. Sign by computing: signature = hash^d mod n
        4. Return signature
        """
        pass

    def verify(self, message: bytes, signature: int) -> bool:
        """
        TODO: Verify digital signature.
        1. Hash the message
        2. Decrypt signature: recovered_hash = signature^e mod n
        3. Compare recovered_hash with computed hash
        4. Return True if they match
        """
        pass

    def get_public_key(self) -> PublicKey:
        """Return the public key."""
        return self.public_key

    @staticmethod
    def verify_with_public_key(public_key: PublicKey, message: bytes, signature: int) -> bool:
        """
        TODO: Verify signature using only public key.
        This allows anyone to verify signatures without access to private key.
        Same as verify() but uses provided public_key.
        """
        pass


def simple_hash(data: bytes) -> int:
    """
    TODO: Implement a simple hash function.
    1. Initialize hash = 5381 (prime number)
    2. For each byte: hash = hash * 33 + byte
    3. Return hash
    This is DJB2 hash - simple but not cryptographic.
    """
    pass


def modular_exponentiation(base: int, exp: int, modulus: int) -> int:
    """
    TODO: Same as RSA - implement efficient modular exponentiation.
    """
    pass


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    TODO: Extended Euclidean algorithm.
    """
    pass


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    TODO: Calculate modular multiplicative inverse.
    """
    pass


def gcd(a: int, b: int) -> int:
    """
    TODO: Calculate greatest common divisor.
    """
    pass


class TestDigitalSignature(unittest.TestCase):
    """Comprehensive test cases for digital signature implementation."""

    def test_signature_creation(self):
        """Test creating a signature."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b"Hello, World!"

        signature = signer.sign(message)

        # Signature should be a number
        self.assertGreater(signature, 0)
        self.assertLess(signature, p * q)

    def test_signature_verification(self):
        """Test verifying a valid signature."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b"Hello, World!"

        signature = signer.sign(message)
        valid = signer.verify(message, signature)

        self.assertTrue(valid)

    def test_tampered_message(self):
        """Test that tampering is detected."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b"Hello, World!"

        signature = signer.sign(message)

        # Try to verify with different message
        tampered = b"Hello, World?"
        valid = signer.verify(tampered, signature)

        self.assertFalse(valid)

    def test_different_messages_different_signatures(self):
        """Test that different messages produce different signatures."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)

        sig1 = signer.sign(b"Message 1")
        sig2 = signer.sign(b"Message 2")

        self.assertNotEqual(sig1, sig2)

    def test_verify_with_public_key_only(self):
        """Test verification with only public key."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b"Public message"

        signature = signer.sign(message)
        public_key = signer.get_public_key()

        # Verify using only public key (what recipients do)
        valid = DigitalSignature.verify_with_public_key(public_key, message, signature)

        self.assertTrue(valid)

    def test_invalid_signature(self):
        """Test that invalid signature is rejected."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b"Test message"

        signature = signer.sign(message)

        # Try with wrong signature
        valid = signer.verify(message, signature + 1)

        self.assertFalse(valid)

    def test_empty_message(self):
        """Test signing and verifying empty message."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b""

        signature = signer.sign(message)
        valid = signer.verify(message, signature)

        self.assertTrue(valid)

    def test_long_message(self):
        """Test signing and verifying long message."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b"This is a much longer message that will be hashed before signing. " \
                  b"The hash allows us to sign messages of any length."

        signature = signer.sign(message)
        valid = signer.verify(message, signature)

        self.assertTrue(valid)

    def test_deterministic_signatures(self):
        """Test that same message produces same signature."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b"Deterministic test"

        sig1 = signer.sign(message)
        sig2 = signer.sign(message)

        # Same message should produce same signature
        self.assertEqual(sig1, sig2)

    def test_simple_hash_function(self):
        """Test the simple hash function."""
        hash1 = simple_hash(b"test")
        hash2 = simple_hash(b"test")
        hash3 = simple_hash(b"Test")

        # Same input produces same hash
        self.assertEqual(hash1, hash2)

        # Different input produces different hash
        self.assertNotEqual(hash1, hash3)

    def test_multiple_signers(self):
        """Test multiple independent signers."""
        p1 = 61
        q1 = 53

        p2 = 67
        q2 = 71

        e = 17

        signer1 = DigitalSignature(p1, q1, e)
        signer2 = DigitalSignature(p2, q2, e)

        message = b"Test message"

        sig1 = signer1.sign(message)
        sig2 = signer2.sign(message)

        # Different signers produce different signatures
        self.assertNotEqual(sig1, sig2)

        # Each signer can verify their own signature
        self.assertTrue(signer1.verify(message, sig1))
        self.assertTrue(signer2.verify(message, sig2))

        # But not each other's
        self.assertFalse(signer1.verify(message, sig2))
        self.assertFalse(signer2.verify(message, sig1))

    def test_non_repudiation(self):
        """Test non-repudiation property."""
        p = 61
        q = 53
        e = 17

        signer = DigitalSignature(p, q, e)
        message = b"I agree to the terms"

        signature = signer.sign(message)

        # Anyone with public key can verify
        public_key = signer.get_public_key()
        verified = DigitalSignature.verify_with_public_key(public_key, message, signature)

        self.assertTrue(verified)
        # The signer cannot deny signing this message (non-repudiation)


if __name__ == '__main__':
    unittest.main()
