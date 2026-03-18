# I AM NOT DONE

"""
crypto03_hash_functions.py

Cryptographic Hash Functions are one-way functions that map arbitrary data
to fixed-size outputs (digests). They are fundamental to digital signatures,
password storage, and data integrity verification.

Properties of cryptographic hash functions:
- Deterministic: Same input always produces same output
- Fast to compute
- Avalanche effect: Small input change drastically changes output
- Pre-image resistance: Hard to find input from output
- Second pre-image resistance: Hard to find different input with same output
- Collision resistance: Hard to find two inputs with same output

Your task: Implement a simplified SHA-like hash function.

Security considerations:
- Never use MD5 or SHA-1 in production (both are broken)
- Use SHA-256, SHA-3, or BLAKE2 for new applications
- Hash functions alone are NOT suitable for password storage
- Use for integrity checks, but add HMAC for authentication
- Beware of length extension attacks (SHA-2 vulnerable, SHA-3 is not)
"""

import unittest
from typing import List


BLOCK_SIZE = 64  # 512 bits
HASH_SIZE = 32   # 256 bits

# Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
INITIAL_HASH = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
]

# Round constants (first 32 bits of fractional parts of cube roots of first 64 primes)
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]


class SHA256:
    """Simplified SHA-256 hash function implementation."""

    def __init__(self):
        self.state = list(INITIAL_HASH)
        self.buffer = bytearray()
        self.total_len = 0

    def update(self, data: bytes) -> None:
        """
        TODO: Update hash state with new data.
        1. Append data to buffer
        2. Process complete blocks (64 bytes each)
        3. Keep remaining data in buffer
        4. Update total_len
        """
        pass

    def finalize(self) -> bytes:
        """
        TODO: Finalize hash and return digest.
        1. Apply padding: append 0x80, then zeros, then 64-bit length
        2. Process remaining blocks
        3. Convert state to bytes (big-endian)
        4. Return 32-byte hash
        """
        pass

    def process_block(self, block: bytes) -> None:
        """
        TODO: Process a single 512-bit block.
        1. Create message schedule (W) array of 64 u32 values
        2. First 16 values come from block (big-endian)
        3. Remaining 48 values computed using SHA-256 formula
        4. Initialize working variables a-h from state
        5. Main loop: 64 rounds of compression function
        6. Add compressed values back to state
        """
        pass

    @staticmethod
    def digest(data: bytes) -> bytes:
        """
        TODO: Convenience function to hash data in one call.
        1. Create new SHA256
        2. Update with data
        3. Finalize and return
        """
        pass

    @staticmethod
    def digest_hex(data: bytes) -> str:
        """Return hash as hex string."""
        hash_bytes = SHA256.digest(data)
        return ''.join(f'{b:02x}' for b in hash_bytes)


def ch(x: int, y: int, z: int) -> int:
    """
    TODO: Choice function: (x & y) ^ (~x & z)
    """
    pass


def maj(x: int, y: int, z: int) -> int:
    """
    TODO: Majority function: (x & y) ^ (x & z) ^ (y & z)
    """
    pass


def sigma0(x: int) -> int:
    """Σ0 function: ROTR(2) ^ ROTR(13) ^ ROTR(22)"""
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def sigma1(x: int) -> int:
    """
    TODO: Σ1 function: ROTR(6) ^ ROTR(11) ^ ROTR(25)
    """
    pass


def gamma0(x: int) -> int:
    """
    TODO: σ0 function: ROTR(7) ^ ROTR(18) ^ SHR(3)
    """
    pass


def gamma1(x: int) -> int:
    """
    TODO: σ1 function: ROTR(17) ^ ROTR(19) ^ SHR(10)
    """
    pass


def rotr(x: int, n: int) -> int:
    """Rotate right (circular right shift) for 32-bit values."""
    return ((x >> n) | (x << (32 - n))) & 0xffffffff


class TestSHA256(unittest.TestCase):
    """Comprehensive test cases for SHA-256 implementation."""

    def test_empty_string(self):
        """Test hashing empty string."""
        hash_bytes = SHA256.digest(b"")
        hex_hash = SHA256.digest_hex(b"")

        self.assertEqual(len(hash_bytes), 32)
        # SHA-256 of empty string
        self.assertEqual(hex_hash, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    def test_simple_message(self):
        """Test hashing 'abc'."""
        hex_hash = SHA256.digest_hex(b"abc")

        # SHA-256 of "abc"
        self.assertEqual(hex_hash, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_longer_message(self):
        """Test hashing longer message."""
        message = b"The quick brown fox jumps over the lazy dog"
        hex_hash = SHA256.digest_hex(message)

        self.assertEqual(hex_hash, "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592")

    def test_deterministic(self):
        """Test that same input produces same hash."""
        data = b"test message"

        hash1 = SHA256.digest(data)
        hash2 = SHA256.digest(data)

        self.assertEqual(hash1, hash2)

    def test_avalanche_effect(self):
        """Test that small changes produce large differences."""
        hash1 = SHA256.digest(b"test")
        hash2 = SHA256.digest(b"Test")  # One bit different

        # Count differing bits
        diff_bits = sum(bin(a ^ b).count('1') for a, b in zip(hash1, hash2))

        # Should differ in approximately 50% of bits (128 out of 256)
        self.assertGreater(diff_bits, 100)
        self.assertLess(diff_bits, 156)

    def test_incremental_update(self):
        """Test incremental hashing."""
        hasher = SHA256()
        hasher.update(b"Hello, ")
        hasher.update(b"World!")
        hash1 = hasher.finalize()

        hash2 = SHA256.digest(b"Hello, World!")

        self.assertEqual(hash1, hash2)

    def test_long_message(self):
        """Test hashing long message."""
        message = b'a' * 1000
        hash_bytes = SHA256.digest(message)

        self.assertEqual(len(hash_bytes), 32)

    def test_boundary_block_size(self):
        """Test message exactly 64 bytes."""
        message = b'a' * 64
        hash_bytes = SHA256.digest(message)

        self.assertEqual(len(hash_bytes), 32)

    def test_multiple_blocks(self):
        """Test message larger than one block."""
        message = b'b' * 200
        hash_bytes = SHA256.digest(message)

        self.assertEqual(len(hash_bytes), 32)

    def test_binary_data(self):
        """Test hashing binary data."""
        data = bytes(range(256))
        hash_bytes = SHA256.digest(data)

        self.assertEqual(len(hash_bytes), 32)

    def test_helper_functions(self):
        """Test SHA-256 helper functions."""
        self.assertEqual(ch(0xF0F0F0F0, 0xFF00FF00, 0x00FF00FF), 0x0FFF0FFF)
        self.assertEqual(maj(0xF0F0F0F0, 0xFF00FF00, 0x00FF00FF), 0xF0FFF0F0)

    def test_collision_resistance(self):
        """Test that different inputs produce different outputs."""
        hash1 = SHA256.digest(b"message1")
        hash2 = SHA256.digest(b"message2")
        hash3 = SHA256.digest(b"message3")

        self.assertNotEqual(hash1, hash2)
        self.assertNotEqual(hash2, hash3)
        self.assertNotEqual(hash1, hash3)


if __name__ == '__main__':
    unittest.main()
