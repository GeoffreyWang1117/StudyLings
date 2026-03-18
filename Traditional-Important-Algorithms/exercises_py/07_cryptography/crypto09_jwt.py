# I AM NOT DONE

"""
crypto09_jwt.py

JSON Web Tokens (JWT) are a compact, URL-safe means of representing claims
to be transferred between two parties. Used widely for authentication.

JWT structure: header.payload.signature
- Header: Algorithm and token type (base64url encoded)
- Payload: Claims/data (base64url encoded)
- Signature: HMAC or RSA signature of header.payload

Common claims:
- iss (issuer), sub (subject), aud (audience)
- exp (expiration), nbf (not before), iat (issued at), jti (JWT ID)

Your task: Implement JWT creation and verification with HMAC.

Security considerations:
- Always verify signature before trusting claims
- Check expiration time (exp claim)
- Validate issuer and audience
- Never put sensitive data in payload (only encoded, not encrypted)
- Use HTTPS, short expiration times, refresh tokens
- Beware of algorithm confusion attacks
"""

import unittest
import base64
import json
import time
from typing import Dict, Optional


class JWTPayload:
    """JWT payload with claims."""
    
    def __init__(self):
        self.claims: Dict[str, str] = {}
    
    def set_claim(self, key: str, value: str) -> None:
        self.claims[key] = value
    
    def get_claim(self, key: str) -> Optional[str]:
        return self.claims.get(key)
    
    def set_expiration(self, exp: int) -> None:
        self.claims['exp'] = str(exp)
    
    def set_issued_at(self, iat: int) -> None:
        self.claims['iat'] = str(iat)
    
    def set_subject(self, sub: str) -> None:
        self.claims['sub'] = sub
    
    def set_issuer(self, iss: str) -> None:
        self.claims['iss'] = iss
    
    def to_json(self) -> str:
        """TODO: Convert payload to JSON string."""
        pass
    
    @staticmethod
    def from_json(json_str: str) -> 'JWTPayload':
        """TODO: Parse JSON string to JWTPayload."""
        pass


class JWT:
    """JWT implementation with HMAC signing."""
    
    def __init__(self, secret: bytes):
        self.secret = secret
    
    def create_token(self, payload: JWTPayload) -> str:
        """
        TODO: Create JWT token.
        1. Create header with alg="HS256", typ="JWT"
        2. Serialize header to JSON and base64url encode
        3. Serialize payload to JSON and base64url encode
        4. Create signing input: base64url(header).base64url(payload)
        5. Sign with HMAC-SHA256
        6. base64url encode signature
        7. Return header.payload.signature
        """
        pass
    
    def verify_token(self, token: str) -> JWTPayload:
        """
        TODO: Verify and decode JWT token.
        1. Split token into header, payload, signature parts
        2. Verify signature
        3. Decode and verify header (check algorithm)
        4. Decode payload
        5. Check expiration if present
        6. Return payload
        Raises ValueError if invalid.
        """
        pass
    
    def decode_without_verify(self, token: str) -> JWTPayload:
        """
        TODO: Decode token without verification (for debugging only!).
        WARNING: Never use this for authentication in production.
        """
        pass


def base64url_encode(data: bytes) -> str:
    """
    TODO: Implement base64url encoding.
    Like base64 but: use '-' instead of '+', '_' instead of '/', no padding '='
    """
    pass


def base64url_decode(s: str) -> bytes:
    """
    TODO: Implement base64url decoding.
    """
    pass


def hmac_sha256(key: bytes, data: bytes) -> bytes:
    """
    TODO: Implement HMAC-SHA256.
    Can reuse implementation from MAC exercise.
    """
    pass


def constant_time_compare(a: bytes, b: bytes) -> bool:
    """TODO: Constant-time comparison."""
    pass


def current_timestamp() -> int:
    """Return current Unix timestamp."""
    return int(time.time())


class TestJWT(unittest.TestCase):
    """Comprehensive test cases for JWT implementation."""
    
    def test_jwt_creation(self):
        """Test creating a JWT."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        payload = JWTPayload()
        payload.set_subject("user123")
        payload.set_issuer("myapp")
        token = jwt.create_token(payload)
        # Token should have 3 parts separated by dots
        self.assertEqual(token.count('.'), 2)
    
    def test_jwt_verification(self):
        """Test verifying a valid JWT."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        payload = JWTPayload()
        payload.set_subject("user123")
        token = jwt.create_token(payload)
        verified_payload = jwt.verify_token(token)
        self.assertEqual(verified_payload.get_claim("sub"), "user123")
    
    def test_jwt_tampered_payload(self):
        """Test that tampered tokens are rejected."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        payload = JWTPayload()
        payload.set_subject("user123")
        token = jwt.create_token(payload)
        # Tamper with token
        parts = token.split('.')
        if len(parts) == 3:
            tampered = parts[0] + '.tampered.' + parts[2]
            with self.assertRaises(ValueError):
                jwt.verify_token(tampered)
    
    def test_jwt_wrong_secret(self):
        """Test that wrong secret fails verification."""
        jwt1 = JWT(b"secret1")
        jwt2 = JWT(b"secret2")
        payload = JWTPayload()
        payload.set_subject("user123")
        token = jwt1.create_token(payload)
        with self.assertRaises(ValueError):
            jwt2.verify_token(token)
    
    def test_jwt_expiration(self):
        """Test that expired tokens are rejected."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        payload = JWTPayload()
        payload.set_subject("user123")
        payload.set_expiration(current_timestamp() - 3600)  # Expired 1 hour ago
        token = jwt.create_token(payload)
        with self.assertRaises(ValueError):
            jwt.verify_token(token)
    
    def test_jwt_valid_expiration(self):
        """Test that non-expired tokens pass."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        payload = JWTPayload()
        payload.set_subject("user123")
        payload.set_expiration(current_timestamp() + 3600)  # Expires in 1 hour
        token = jwt.create_token(payload)
        result = jwt.verify_token(token)
        self.assertIsNotNone(result)
    
    def test_multiple_claims(self):
        """Test JWT with multiple claims."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        payload = JWTPayload()
        payload.set_subject("user123")
        payload.set_issuer("myapp")
        payload.set_claim("role", "admin")
        payload.set_claim("email", "user@example.com")
        token = jwt.create_token(payload)
        verified = jwt.verify_token(token)
        self.assertEqual(verified.get_claim("sub"), "user123")
        self.assertEqual(verified.get_claim("iss"), "myapp")
        self.assertEqual(verified.get_claim("role"), "admin")
        self.assertEqual(verified.get_claim("email"), "user@example.com")
    
    def test_base64url_encoding(self):
        """Test base64url encoding."""
        data = b"Hello, World!"
        encoded = base64url_encode(data)
        # Should not contain '+', '/', or '='
        self.assertNotIn('+', encoded)
        self.assertNotIn('/', encoded)
        self.assertNotIn('=', encoded)
        decoded = base64url_decode(encoded)
        self.assertEqual(decoded, data)
    
    def test_decode_without_verify(self):
        """Test decoding without verification."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        payload = JWTPayload()
        payload.set_subject("user123")
        token = jwt.create_token(payload)
        decoded = jwt.decode_without_verify(token)
        self.assertEqual(decoded.get_claim("sub"), "user123")
    
    def test_empty_payload(self):
        """Test JWT with empty payload."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        payload = JWTPayload()
        token = jwt.create_token(payload)
        verified = jwt.verify_token(token)
        self.assertEqual(len(verified.claims), 0)
    
    def test_issued_at_claim(self):
        """Test issued_at claim."""
        secret = b"my-secret-key"
        jwt = JWT(secret)
        now = current_timestamp()
        payload = JWTPayload()
        payload.set_issued_at(now)
        token = jwt.create_token(payload)
        verified = jwt.verify_token(token)
        self.assertEqual(verified.get_claim("iat"), str(now))
    
    def test_payload_json_serialization(self):
        """Test payload JSON serialization."""
        payload = JWTPayload()
        payload.set_claim("key1", "value1")
        payload.set_claim("key2", "value2")
        json_str = payload.to_json()
        parsed = JWTPayload.from_json(json_str)
        self.assertEqual(parsed.get_claim("key1"), "value1")
        self.assertEqual(parsed.get_claim("key2"), "value2")


if __name__ == '__main__':
    unittest.main()
