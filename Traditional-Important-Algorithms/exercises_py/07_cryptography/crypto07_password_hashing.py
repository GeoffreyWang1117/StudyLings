# I AM NOT DONE

"""
crypto07_password_hashing.py

Password Hashing is critical for secure password storage. Never store passwords
in plaintext or with simple hashes like SHA-256!

Key concepts:
- Salt: Random data added to password before hashing (prevents rainbow tables)
- Iteration count (cost factor): Slow down brute force attacks
- Memory-hard functions: Resist GPU/ASIC attacks (bcrypt, scrypt, Argon2)
- Pepper: Optional secret added server-side (not stored with hash)

Modern algorithms:
- Argon2: Winner of Password Hashing Competition (recommended)
- bcrypt: Widely used, good choice
- scrypt: Memory-hard, good for preventing hardware attacks
- PBKDF2: Older but still acceptable with high iteration count

NEVER use: MD5, SHA-1, SHA-256 without iterations, or unsalted hashes

Your task: Implement a password hashing system with salt and iterations.

Security considerations:
- Always use unique salt per password (never reuse)
- Store salt alongside hash (it's not secret)
- Use high iteration count (100,000+ for PBKDF2, tune for ~100ms)
- Increase iterations over time as hardware improves
- Use constant-time comparison when verifying passwords
- Consider using a pepper (application-level secret)
- For new systems, prefer Argon2id
"""

import unittest
import secrets
import time


SALT_SIZE = 16
HASH_SIZE = 32
DEFAULT_ITERATIONS = 10000


class PasswordHash:
    """Represents a password hash with metadata."""

    def __init__(self, hash_bytes: bytes, salt: bytes, iterations: int):
        self.hash_bytes = hash_bytes
        self.salt = salt
        self.iterations = iterations

    def to_string(self) -> str:
        """
        TODO: Serialize to string format (similar to bcrypt format).
        Format: $iterations$salt$hash (all in hex)
        Example: $10000$0123456789abcdef$fedcba9876543210...
        """
        pass

    @staticmethod
    def from_string(s: str) -> 'PasswordHash':
        """
        TODO: Deserialize from string format.
        Parse the $iterations$salt$hash format.
        Raises ValueError if format is invalid.
        """
        pass


class PasswordHasher:
    """Password hasher with configurable iterations and optional pepper."""

    def __init__(self, iterations: int = DEFAULT_ITERATIONS, pepper: bytes = None):
        self.iterations = iterations
        self.pepper = pepper

    def hash_password(self, password: str) -> PasswordHash:
        """
        TODO: Hash password with salt.
        1. Generate random salt using generate_salt()
        2. Combine password with pepper if present
        3. Apply PBKDF2-like algorithm: hash repeatedly with salt
        4. Return PasswordHash with hash, salt, and iterations
        """
        pass

    def verify_password(self, password: str, stored_hash: PasswordHash) -> bool:
        """
        TODO: Verify password against stored hash.
        1. Extract salt and iterations from stored_hash
        2. Hash the provided password with same salt and iterations
        3. Use constant_time_compare to compare hashes
        4. Return True if they match
        """
        pass

    def needs_rehash(self, stored_hash: PasswordHash) -> bool:
        """
        TODO: Check if password needs rehashing (iterations too low).
        Return True if stored_hash.iterations < self.iterations
        """
        pass


def generate_salt() -> bytes:
    """
    TODO: Generate cryptographically secure random salt.
    Use secrets.token_bytes() or similar.
    """
    pass


def pbkdf2(password: bytes, salt: bytes, iterations: int) -> bytes:
    """
    TODO: Implement PBKDF2-like key derivation.
    1. Combine password and salt
    2. Hash the combination
    3. For each iteration: hash = hash(previous_hash || password || salt)
    4. Return final hash
    """
    pass


def simple_hash(data: bytes) -> bytes:
    """
    TODO: Simple hash function (same as previous exercises).
    Return HASH_SIZE bytes.
    """
    pass


def constant_time_compare(a: bytes, b: bytes) -> bool:
    """
    TODO: Constant-time comparison.
    Same implementation as in MAC exercise.
    """
    pass


class TestPasswordHashing(unittest.TestCase):
    """Comprehensive test cases for password hashing."""

    def test_hash_password(self):
        """Test hashing a password."""
        hasher = PasswordHasher(1000)
        password = "mySecurePassword123!"
        hash_obj = hasher.hash_password(password)
        self.assertEqual(len(hash_obj.salt), SALT_SIZE)
        self.assertEqual(len(hash_obj.hash_bytes), HASH_SIZE)
        self.assertEqual(hash_obj.iterations, 1000)

    def test_verify_correct_password(self):
        """Test verifying correct password."""
        hasher = PasswordHasher(1000)
        password = "correctPassword"
        hash_obj = hasher.hash_password(password)
        is_valid = hasher.verify_password(password, hash_obj)
        self.assertTrue(is_valid)

    def test_verify_incorrect_password(self):
        """Test verifying incorrect password."""
        hasher = PasswordHasher(1000)
        password = "correctPassword"
        hash_obj = hasher.hash_password(password)
        is_valid = hasher.verify_password("wrongPassword", hash_obj)
        self.assertFalse(is_valid)

    def test_different_salts(self):
        """Test that same password produces different hashes with different salts."""
        hasher = PasswordHasher(1000)
        password = "samePassword"
        hash1 = hasher.hash_password(password)
        hash2 = hasher.hash_password(password)
        # Same password should produce different hashes due to different salts
        self.assertNotEqual(hash1.salt, hash2.salt)
        self.assertNotEqual(hash1.hash_bytes, hash2.hash_bytes)

    def test_salt_uniqueness(self):
        """Test that salts are unique."""
        salt1 = generate_salt()
        salt2 = generate_salt()
        self.assertNotEqual(salt1, salt2)

    def test_password_hash_serialization(self):
        """Test serializing password hash."""
        hasher = PasswordHasher(5000)
        password = "testPassword"
        hash_obj = hasher.hash_password(password)
        serialized = hash_obj.to_string()
        # Should contain $ separators
        self.assertIn('$', serialized)

    def test_password_hash_deserialization(self):
        """Test deserializing password hash."""
        hasher = PasswordHasher(5000)
        password = "testPassword"
        hash_obj = hasher.hash_password(password)
        serialized = hash_obj.to_string()
        deserialized = PasswordHash.from_string(serialized)
        self.assertEqual(hash_obj.iterations, deserialized.iterations)
        self.assertEqual(hash_obj.salt, deserialized.salt)
        self.assertEqual(hash_obj.hash_bytes, deserialized.hash_bytes)

    def test_needs_rehash(self):
        """Test detecting when rehashing is needed."""
        hasher_low = PasswordHasher(1000)
        hasher_high = PasswordHasher(10000)
        password = "testPassword"
        hash_obj = hasher_low.hash_password(password)
        # Higher iteration hasher should indicate rehash needed
        self.assertTrue(hasher_high.needs_rehash(hash_obj))
        # Same iteration hasher should not need rehash
        self.assertFalse(hasher_low.needs_rehash(hash_obj))

    def test_with_pepper(self):
        """Test password hashing with pepper."""
        pepper = b"application_secret_pepper"
        hasher = PasswordHasher(1000, pepper)
        password = "testPassword"
        hash_obj = hasher.hash_password(password)
        # Should verify with same hasher (has pepper)
        self.assertTrue(hasher.verify_password(password, hash_obj))
        # Should NOT verify with hasher without pepper
        hasher_no_pepper = PasswordHasher(1000)
        self.assertFalse(hasher_no_pepper.verify_password(password, hash_obj))

    def test_iteration_count_matters(self):
        """Test that iteration count affects hash."""
        password = b"test"
        salt = bytes([0x01] * SALT_SIZE)
        hash1 = pbkdf2(password, salt, 100)
        hash2 = pbkdf2(password, salt, 1000)
        # Different iteration counts should produce different hashes
        self.assertNotEqual(hash1, hash2)

    def test_empty_password(self):
        """Test hashing empty password."""
        hasher = PasswordHasher(1000)
        password = ""
        hash_obj = hasher.hash_password(password)
        self.assertTrue(hasher.verify_password(password, hash_obj))

    def test_long_password(self):
        """Test hashing long password."""
        hasher = PasswordHasher(1000)
        password = "a" * 1000
        hash_obj = hasher.hash_password(password)
        self.assertTrue(hasher.verify_password(password, hash_obj))
        self.assertFalse(hasher.verify_password("wrong", hash_obj))

    def test_special_characters(self):
        """Test password with special characters."""
        hasher = PasswordHasher(1000)
        password = "p@ssw0rd!#$%^&*()_+-=[]{}|;:,.<>?"
        hash_obj = hasher.hash_password(password)
        self.assertTrue(hasher.verify_password(password, hash_obj))


if __name__ == '__main__':
    unittest.main()
