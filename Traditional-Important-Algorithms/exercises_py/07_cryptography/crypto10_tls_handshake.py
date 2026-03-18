# I AM NOT DONE

"""
crypto10_tls_handshake.py

TLS (Transport Layer Security) secures HTTPS, email, and most internet communications.
The TLS handshake establishes a secure connection.

TLS Handshake steps (simplified TLS 1.2):
1. ClientHello: Client sends supported cipher suites, random nonce
2. ServerHello: Server chooses cipher suite, sends certificate, random nonce
3. Key Exchange: Client and server use DH or RSA to establish shared secret
4. Finished: Both sides verify handshake with MAC
5. Application Data: Encrypted communication begins

Your task: Implement a simplified TLS handshake simulator.

Security considerations:
- Always verify server certificate chain
- Check certificate hasn't expired
- Verify certificate hostname matches server
- Use strong cipher suites (AEAD like AES-GCM)
- Implement forward secrecy (ephemeral DH/ECDH)
- Validate all handshake messages
"""

import unittest
import time
from enum import Enum
from typing import List, Optional, Tuple


class CipherSuite(Enum):
    """TLS cipher suites."""
    TLS_DHE_RSA_WITH_AES_128_GCM = "TLS_DHE_RSA_WITH_AES_128_GCM"
    TLS_ECDHE_RSA_WITH_AES_256_GCM = "TLS_ECDHE_RSA_WITH_AES_256_GCM"
    TLS_RSA_WITH_AES_128_CBC = "TLS_RSA_WITH_AES_128_CBC"  # Weaker


class Certificate:
    """TLS certificate."""
    
    def __init__(self, subject: str, issuer: str, public_key: bytes,
                 valid_from: int, valid_until: int, signature: bytes):
        self.subject = subject
        self.issuer = issuer
        self.public_key = public_key
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.signature = signature
    
    def is_valid(self, current_time: int) -> bool:
        """
        TODO: Check if certificate is currently valid.
        Verify current_time is between valid_from and valid_until.
        """
        pass
    
    def verify_signature(self, ca_public_key: bytes) -> bool:
        """
        TODO: Verify certificate signature.
        In real implementation, verify signature using CA's public key.
        For this exercise, simplified check.
        """
        pass


class ClientHello:
    """TLS ClientHello message."""
    
    def __init__(self, client_random: bytes, supported_ciphers: List[CipherSuite],
                 session_id: Optional[bytes] = None):
        self.client_random = client_random
        self.supported_ciphers = supported_ciphers
        self.session_id = session_id


class ServerHello:
    """TLS ServerHello message."""
    
    def __init__(self, server_random: bytes, chosen_cipher: CipherSuite,
                 session_id: bytes, certificate: Certificate):
        self.server_random = server_random
        self.chosen_cipher = chosen_cipher
        self.session_id = session_id
        self.certificate = certificate


class KeyExchange:
    """TLS KeyExchange message."""
    
    def __init__(self, client_key_exchange: bytes):
        self.client_key_exchange = client_key_exchange


class Finished:
    """TLS Finished message."""
    
    def __init__(self, verify_data: bytes):
        self.verify_data = verify_data


class HandshakeState(Enum):
    """TLS handshake states."""
    INITIAL = "INITIAL"
    CLIENT_HELLO_SENT = "CLIENT_HELLO_SENT"
    SERVER_HELLO_RECEIVED = "SERVER_HELLO_RECEIVED"
    CERTIFICATE_RECEIVED = "CERTIFICATE_RECEIVED"
    KEY_EXCHANGE_COMPLETE = "KEY_EXCHANGE_COMPLETE"
    FINISHED = "FINISHED"


class TLSHandshake:
    """TLS handshake state machine."""
    
    def __init__(self, is_server: bool):
        self.is_server = is_server
        self.state = HandshakeState.INITIAL
        self.client_random: Optional[bytes] = None
        self.server_random: Optional[bytes] = None
        self.chosen_cipher: Optional[CipherSuite] = None
        self.premaster_secret: Optional[bytes] = None
        self.master_secret: Optional[bytes] = None
        self.handshake_messages: List[bytes] = []
    
    @staticmethod
    def new_client() -> 'TLSHandshake':
        return TLSHandshake(is_server=False)
    
    @staticmethod
    def new_server() -> 'TLSHandshake':
        return TLSHandshake(is_server=True)
    
    def send_client_hello(self, supported_ciphers: List[CipherSuite]) -> ClientHello:
        """
        TODO: Create and send ClientHello.
        1. Generate random client_random (32 bytes)
        2. Store client_random
        3. Create ClientHello with supported ciphers
        4. Record message in handshake_messages
        5. Update state to CLIENT_HELLO_SENT
        6. Return ClientHello
        """
        pass
    
    def receive_client_hello(self, hello: ClientHello) -> None:
        """
        TODO: Process ClientHello (server side).
        1. Verify we're in correct state
        2. Store client_random
        3. Record message
        4. Update state
        """
        pass
    
    def send_server_hello(self, certificate: Certificate,
                         client_ciphers: List[CipherSuite]) -> ServerHello:
        """
        TODO: Create and send ServerHello.
        1. Generate server_random
        2. Choose cipher suite from client's supported list
        3. Generate session_id
        4. Create ServerHello with certificate
        5. Record message
        6. Update state
        """
        pass
    
    def receive_server_hello(self, hello: ServerHello) -> None:
        """
        TODO: Process ServerHello (client side).
        1. Verify certificate validity
        2. Verify certificate signature (simplified)
        3. Store server_random and chosen_cipher
        4. Record message
        5. Update state to SERVER_HELLO_RECEIVED
        """
        pass
    
    def send_key_exchange(self) -> KeyExchange:
        """
        TODO: Create and send KeyExchange.
        1. Generate premaster secret (48 random bytes)
        2. In real TLS: encrypt with server's public key (RSA) or send DH public value
        3. For simplicity: just store premaster_secret
        4. Derive master_secret from premaster_secret, client_random, server_random
        5. Record message
        6. Return KeyExchange
        """
        pass
    
    def receive_key_exchange(self, key_exchange: KeyExchange) -> None:
        """
        TODO: Process KeyExchange (server side).
        1. Extract premaster secret (decrypt if RSA, compute DH if DH)
        2. Derive master_secret
        3. Record message
        4. Update state
        """
        pass
    
    def send_finished(self) -> Finished:
        """
        TODO: Create and send Finished message.
        1. Compute verify_data: MAC of all handshake messages using master_secret
        2. Create Finished message
        3. Update state to FINISHED
        4. Return Finished
        """
        pass
    
    def receive_finished(self, finished: Finished) -> None:
        """
        TODO: Verify Finished message.
        1. Compute expected verify_data from handshake messages
        2. Compare with received verify_data (constant-time)
        3. If valid, update state to FINISHED
        4. Raise ValueError if invalid
        """
        pass
    
    def is_handshake_complete(self) -> bool:
        return self.state == HandshakeState.FINISHED
    
    def get_master_secret(self) -> Optional[bytes]:
        return self.master_secret
    
    def derive_session_keys(self) -> 'SessionKeys':
        """
        TODO: Derive session keys from master secret.
        In real TLS, derive client_write_key, server_write_key, client_write_MAC, etc.
        For this exercise, derive two keys: client_key and server_key.
        """
        pass


class SessionKeys:
    """TLS session keys."""
    
    def __init__(self, client_write_key: bytes, server_write_key: bytes,
                 client_mac_key: bytes, server_mac_key: bytes):
        self.client_write_key = client_write_key
        self.server_write_key = server_write_key
        self.client_mac_key = client_mac_key
        self.server_mac_key = server_mac_key


def prf(secret: bytes, label: bytes, seed: bytes, output_len: int) -> bytes:
    """
    TODO: TLS PRF function.
    Simplified version of TLS PRF.
    1. Combine label and seed
    2. Use HMAC to expand secret into output_len bytes
    3. Return derived key material
    """
    pass


def derive_master_secret(premaster_secret: bytes, client_random: bytes,
                         server_random: bytes) -> bytes:
    """
    TODO: Derive 48-byte master secret.
    master_secret = PRF(premaster_secret, "master secret", client_random + server_random)[0..48]
    """
    pass


def generate_random_bytes(length: int) -> bytes:
    """TODO: Generate random bytes (use secrets module)."""
    pass


def hmac(key: bytes, data: bytes) -> bytes:
    """TODO: HMAC function (can reuse from previous exercises)."""
    pass


def constant_time_compare(a: bytes, b: bytes) -> bool:
    """TODO: Constant-time comparison."""
    pass


def current_time() -> int:
    return int(time.time())


class TestTLSHandshake(unittest.TestCase):
    """Comprehensive test cases for TLS handshake."""
    
    def test_certificate_validity(self):
        """Test certificate validation."""
        now = current_time()
        cert = Certificate("example.com", "Root CA", b"\x01\x02\x03\x04",
                          now - 3600, now + 3600, b"\x05\x06\x07\x08")
        self.assertTrue(cert.is_valid(now))
        self.assertFalse(cert.is_valid(now - 7200))  # Before valid_from
        self.assertFalse(cert.is_valid(now + 7200))  # After valid_until
    
    def test_client_hello(self):
        """Test ClientHello creation."""
        client = TLSHandshake.new_client()
        ciphers = [CipherSuite.TLS_ECDHE_RSA_WITH_AES_256_GCM,
                   CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM]
        hello = client.send_client_hello(ciphers)
        self.assertEqual(len(hello.client_random), 32)
        self.assertEqual(len(hello.supported_ciphers), 2)
    
    def test_server_hello(self):
        """Test ServerHello creation."""
        server = TLSHandshake.new_server()
        client_hello = ClientHello(bytes([1] * 32),
                                   [CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM], None)
        server.receive_client_hello(client_hello)
        now = current_time()
        cert = Certificate("example.com", "Root CA", b"\x01\x02\x03\x04",
                          now - 3600, now + 86400, b"\x05\x06\x07\x08")
        server_hello = server.send_server_hello(cert, [CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM])
        self.assertEqual(len(server_hello.server_random), 32)
        self.assertEqual(server_hello.chosen_cipher, CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM)
    
    def test_full_handshake(self):
        """Test complete TLS handshake."""
        client = TLSHandshake.new_client()
        server = TLSHandshake.new_server()
        # 1. Client sends ClientHello
        ciphers = [CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM]
        client_hello = client.send_client_hello(ciphers)
        # 2. Server receives ClientHello
        server.receive_client_hello(client_hello)
        # 3. Server sends ServerHello
        now = current_time()
        cert = Certificate("example.com", "Root CA", b"\x01\x02\x03\x04",
                          now - 3600, now + 86400, b"\x05\x06\x07\x08")
        server_hello = server.send_server_hello(cert, ciphers)
        # 4. Client receives ServerHello
        client.receive_server_hello(server_hello)
        # 5. Client sends KeyExchange
        key_exchange = client.send_key_exchange()
        # 6. Server receives KeyExchange
        server.receive_key_exchange(key_exchange)
        # 7. Client sends Finished
        client_finished = client.send_finished()
        # 8. Server receives and verifies Finished
        server.receive_finished(client_finished)
        # 9. Server sends Finished
        server_finished = server.send_finished()
        # 10. Client receives and verifies Finished
        client.receive_finished(server_finished)
        # Both should be in Finished state
        self.assertTrue(client.is_handshake_complete())
        self.assertTrue(server.is_handshake_complete())
        # Both should have same master secret
        self.assertEqual(client.get_master_secret(), server.get_master_secret())
    
    def test_cipher_suite_negotiation(self):
        """Test cipher suite negotiation."""
        server = TLSHandshake.new_server()
        client_ciphers = [CipherSuite.TLS_RSA_WITH_AES_128_CBC,
                         CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM]
        client_hello = ClientHello(bytes([1] * 32), client_ciphers, None)
        server.receive_client_hello(client_hello)
        now = current_time()
        cert = Certificate("example.com", "Root CA", b"\x01\x02\x03\x04",
                          now, now + 86400, b"\x05\x06\x07\x08")
        server_hello = server.send_server_hello(cert, client_ciphers)
        # Server should choose a cipher from client's list
        self.assertIn(server_hello.chosen_cipher, client_ciphers)
    
    def test_master_secret_derivation(self):
        """Test master secret derivation."""
        premaster = bytes([0x42] * 48)
        client_random = bytes([0x01] * 32)
        server_random = bytes([0x02] * 32)
        master = derive_master_secret(premaster, client_random, server_random)
        self.assertEqual(len(master), 48)
    
    def test_session_keys_derivation(self):
        """Test session keys derivation."""
        client = TLSHandshake.new_client()
        # Simulate completed handshake
        client.client_random = bytes([0x01] * 32)
        client.server_random = bytes([0x02] * 32)
        client.master_secret = bytes([0x42] * 48)
        client.state = HandshakeState.FINISHED
        keys = client.derive_session_keys()
        self.assertGreater(len(keys.client_write_key), 0)
        self.assertGreater(len(keys.server_write_key), 0)
        self.assertNotEqual(keys.client_write_key, keys.server_write_key)
    
    def test_expired_certificate(self):
        """Test that expired certificates are rejected."""
        now = current_time()
        cert = Certificate("example.com", "Root CA", b"\x01\x02\x03\x04",
                          now - 7200, now - 3600, b"\x05\x06\x07\x08")  # Expired 1 hour ago
        self.assertFalse(cert.is_valid(now))
    
    def test_not_yet_valid_certificate(self):
        """Test that not-yet-valid certificates are rejected."""
        now = current_time()
        cert = Certificate("example.com", "Root CA", b"\x01\x02\x03\x04",
                          now + 3600, now + 7200, b"\x05\x06\x07\x08")  # Valid from 1 hour in future
        self.assertFalse(cert.is_valid(now))
    
    def test_handshake_state_progression(self):
        """Test that handshake state progresses correctly."""
        client = TLSHandshake.new_client()
        self.assertEqual(client.state, HandshakeState.INITIAL)
        ciphers = [CipherSuite.TLS_DHE_RSA_WITH_AES_128_GCM]
        client.send_client_hello(ciphers)
        self.assertEqual(client.state, HandshakeState.CLIENT_HELLO_SENT)
    
    def test_prf_deterministic(self):
        """Test that PRF is deterministic."""
        secret = b"secret"
        label = b"test label"
        seed = b"seed data"
        output1 = prf(secret, label, seed, 32)
        output2 = prf(secret, label, seed, 32)
        self.assertEqual(output1, output2)
    
    def test_different_randoms_different_master_secret(self):
        """Test that different randoms produce different master secrets."""
        premaster = bytes([0x42] * 48)
        client_random1 = bytes([0x01] * 32)
        client_random2 = bytes([0x02] * 32)
        server_random = bytes([0x03] * 32)
        master1 = derive_master_secret(premaster, client_random1, server_random)
        master2 = derive_master_secret(premaster, client_random2, server_random)
        self.assertNotEqual(master1, master2)


if __name__ == '__main__':
    unittest.main()
