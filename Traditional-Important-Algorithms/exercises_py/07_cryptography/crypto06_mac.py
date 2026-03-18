# I AM NOT DONE

"""
crypto06_mac.py

Message Authentication Code (MAC) provides authentication and integrity.
Unlike digital signatures, MACs use symmetric keys (shared secret).

HMAC (Hash-based Message Authentication Code) is the most common MAC:
- Combines a hash function with a secret key
- Provides authentication (proves sender knows the key)
- Provides integrity (detects tampering)
- Does NOT provide non-repudiation (both parties have same key)

HMAC construction:
HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
where:
- H is a hash function (e.g., SHA-256)
- K is the secret key
- m is the message
- opad = 0x5c repeated
- ipad = 0x36 repeated
- || is concatenation
- ⊕ is XOR

Your task: Implement HMAC with a simple hash function.

Security considerations:
- HMAC is more secure than simple Hash(key || message)
- Resistant to length extension attacks
- Use with SHA-256 or better (not MD5 or SHA-1)
- Key should be at least as long as hash output
- Always use constant-time comparison to prevent timing attacks
- MACs don't encrypt data, only authenticate it
"""

import unittest
from typing import Tuple


BLOCK_SIZE = 64
HASH_SIZE = 32


class HMAC:
    """HMAC implementation with simple hash function."""

    def __init__(self, key: bytes):
        """
        TODO: Create HMAC instance with key.
        1. If key is longer than BLOCK_SIZE, hash it first
        2. If key is shorter than BLOCK_SIZE, pad with zeros
        3. Store the processed key
        """
        pass

    def compute(self, message: bytes) -> bytes:
        """
        TODO: Compute HMAC.
        1. Create inner_key = key ⊕ ipad (0x36 repeated)
        2. Create outer_key = key ⊕ opad (0x5c repeated)
        3. Compute inner_hash = hash(inner_key || message)
        4. Compute hmac = hash(outer_key || inner_hash)
        5. Return hmac
        """
        pass

    def verify(self, message: bytes, mac: bytes) -> bool:
        """
        TODO: Verify HMAC in constant time.
        1. Compute expected MAC
        2. Use constant_time_compare to compare with provided MAC
        3. Return True if they match
        """
        pass

    @staticmethod
    def sign_and_encrypt(key: bytes, encryption_key: bytes, message: bytes) -> Tuple[bytes, bytes]:
        """
        TODO: Demonstrate encrypt-then-MAC (secure composition).
        1. Encrypt message using simple_encrypt with encryption_key
        2. Compute MAC of ciphertext using key
        3. Return (ciphertext, mac)
        Note: This is the SECURE way (MAC the ciphertext, not plaintext)
        """
        pass

    @staticmethod
    def verify_and_decrypt(key: bytes, encryption_key: bytes, ciphertext: bytes, mac: bytes) -> bytes:
        """
        TODO: Verify then decrypt.
        1. First verify MAC of ciphertext
        2. Only decrypt if MAC is valid
        3. Return decrypted message
        Raises ValueError if MAC is invalid.
        This prevents padding oracle attacks.
        """
        pass


def simple_hash(data: bytes) -> bytes:
    """
    TODO: Implement a simple hash.
    Use DJB2 algorithm extended to produce HASH_SIZE bytes.
    1. Initialize state with different seeds for each output byte
    2. Process all input data
    3. Return HASH_SIZE bytes
    """
    pass


def constant_time_compare(a: bytes, b: bytes) -> bool:
    """
    TODO: Compare two byte slices in constant time.
    1. If lengths differ, return False (but still check all bytes)
    2. XOR all corresponding bytes and OR results
    3. Return True only if result is 0
    IMPORTANT: Must take same time regardless of where difference occurs
    """
    pass


def simple_encrypt(key: bytes, plaintext: bytes) -> bytes:
    """
    TODO: XOR encryption.
    Repeat key to match plaintext length and XOR.
    """
    pass


def simple_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """XOR decryption (same as encryption for XOR)."""
    return simple_encrypt(key, ciphertext)


class TestHMAC(unittest.TestCase):
    """Comprehensive test cases for HMAC implementation."""

    def test_hmac_creation(self):
        """Test creating HMAC instance."""
        key = b"secret key"
        hmac = HMAC(key)
        self.assertEqual(len(hmac.key), BLOCK_SIZE)

    def test_hmac_compute(self):
        """Test computing HMAC."""
        key = b"secret key"
        hmac = HMAC(key)
        message = b"Hello, World!"
        mac = hmac.compute(message)
        self.assertEqual(len(mac), HASH_SIZE)

    def test_hmac_deterministic(self):
        """Test that HMAC is deterministic."""
        key = b"secret key"
        hmac = HMAC(key)
        message = b"Test message"
        mac1 = hmac.compute(message)
        mac2 = hmac.compute(message)
        self.assertEqual(mac1, mac2)

    def test_different_messages_different_macs(self):
        """Test different messages produce different MACs."""
        key = b"secret key"
        hmac = HMAC(key)
        mac1 = hmac.compute(b"Message 1")
        mac2 = hmac.compute(b"Message 2")
        self.assertNotEqual(mac1, mac2)

    def test_different_keys_different_macs(self):
        """Test different keys produce different MACs."""
        message = b"Same message"
        hmac1 = HMAC(b"key1")
        hmac2 = HMAC(b"key2")
        mac1 = hmac1.compute(message)
        mac2 = hmac2.compute(message)
        self.assertNotEqual(mac1, mac2)

    def test_hmac_verify_valid(self):
        """Test verifying valid HMAC."""
        key = b"secret key"
        hmac = HMAC(key)
        message = b"Authenticated message"
        mac = hmac.compute(message)
        self.assertTrue(hmac.verify(message, mac))

    def test_hmac_verify_invalid_mac(self):
        """Test verifying invalid MAC."""
        key = b"secret key"
        hmac = HMAC(key)
        message = b"Test message"
        mac = bytearray(hmac.compute(message))
        # Tamper with MAC
        mac[0] ^= 0x01
        self.assertFalse(hmac.verify(message, bytes(mac)))

    def test_hmac_verify_tampered_message(self):
        """Test detecting tampered message."""
        key = b"secret key"
        hmac = HMAC(key)
        message = b"Original message"
        mac = hmac.compute(message)
        tampered = b"Tampered message"
        self.assertFalse(hmac.verify(tampered, mac))

    def test_constant_time_compare(self):
        """Test constant-time comparison."""
        a = bytes([1, 2, 3, 4, 5])
        b = bytes([1, 2, 3, 4, 5])
        c = bytes([1, 2, 3, 4, 6])
        self.assertTrue(constant_time_compare(a, b))
        self.assertFalse(constant_time_compare(a, c))

    def test_encrypt_then_mac(self):
        """Test encrypt-then-MAC pattern."""
        mac_key = b"mac key"
        enc_key = b"encryption key"
        message = b"Secret message"
        ciphertext, mac = HMAC.sign_and_encrypt(mac_key, enc_key, message)
        # Ciphertext should be different from plaintext
        self.assertNotEqual(ciphertext, message)
        # MAC should be HASH_SIZE bytes
        self.assertEqual(len(mac), HASH_SIZE)

    def test_verify_and_decrypt_success(self):
        """Test successful verify and decrypt."""
        mac_key = b"mac key"
        enc_key = b"encryption key"
        message = b"Secret message"
        ciphertext, mac = HMAC.sign_and_encrypt(mac_key, enc_key, message)
        decrypted = HMAC.verify_and_decrypt(mac_key, enc_key, ciphertext, mac)
        self.assertEqual(decrypted, message)

    def test_verify_and_decrypt_invalid_mac(self):
        """Test that invalid MAC prevents decryption."""
        mac_key = b"mac key"
        enc_key = b"encryption key"
        message = b"Secret message"
        ciphertext, mac = HMAC.sign_and_encrypt(mac_key, enc_key, message)
        # Tamper with MAC
        mac = bytearray(mac)
        mac[0] ^= 0x01
        with self.assertRaises(ValueError):
            HMAC.verify_and_decrypt(mac_key, enc_key, ciphertext, bytes(mac))

    def test_long_key_handling(self):
        """Test handling of long keys."""
        long_key = bytes([0x42] * (BLOCK_SIZE + 10))
        hmac = HMAC(long_key)
        message = b"Test"
        mac = hmac.compute(message)
        self.assertEqual(len(mac), HASH_SIZE)

    def test_empty_message(self):
        """Test HMAC of empty message."""
        key = b"secret key"
        hmac = HMAC(key)
        mac = hmac.compute(b"")
        self.assertEqual(len(mac), HASH_SIZE)
        self.assertTrue(hmac.verify(b"", mac))


if __name__ == '__main__':
    unittest.main()
