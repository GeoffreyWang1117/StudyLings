// crypto10_tls_handshake.rs
//
// TLS (Transport Layer Security) is the protocol that secures HTTPS, email, and
// most internet communications. The TLS handshake establishes a secure connection.
//
// TLS Handshake steps (simplified TLS 1.2):
// 1. ClientHello: Client sends supported cipher suites, random nonce
// 2. ServerHello: Server chooses cipher suite, sends certificate, random nonce
// 3. Key Exchange: Client and server use DH or RSA to establish shared secret
// 4. Finished: Both sides verify handshake with MAC
// 5. Application Data: Encrypted communication begins
//
// TLS 1.3 improvements:
// - Reduced handshake round trips (1-RTT or 0-RTT)
// - Removed insecure cipher suites
// - Forward secrecy mandatory
//
// Your task: Implement a simplified TLS handshake simulator.
//
// Security considerations:
// - Always verify server certificate chain
// - Check certificate hasn't expired
// - Verify certificate hostname matches server
// - Use strong cipher suites (AEAD like AES-GCM)
// - Implement certificate pinning for critical apps
// - Beware of downgrade attacks (use TLS 1.2+)
// - Implement proper certificate revocation checking (OCSP)
// - Use forward secrecy (ephemeral DH/ECDH)
// - Validate all handshake messages

// I AM NOT DONE

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum CipherSuite {
    TLS_DHE_RSA_WITH_AES_128_GCM,
    TLS_ECDHE_RSA_WITH_AES_256_GCM,
    TLS_RSA_WITH_AES_128_CBC,  // Weaker, no forward secrecy
}

#[derive(Debug, Clone, PartialEq)]
pub struct Certificate {
    pub subject: String,
    pub issuer: String,
    pub public_key: Vec<u8>,
    pub valid_from: u64,
    pub valid_until: u64,
    pub signature: Vec<u8>,
}

impl Certificate {
    pub fn is_valid(&self, current_time: u64) -> bool {
        // TODO: Check if certificate is currently valid
        // Verify current_time is between valid_from and valid_until
        todo!()
    }

    pub fn verify_signature(&self, ca_public_key: &[u8]) -> bool {
        // TODO: Verify certificate signature
        // In real implementation, verify signature using CA's public key
        // For this exercise, simplified check
        todo!()
    }
}

#[derive(Debug, Clone)]
pub struct ClientHello {
    pub client_random: [u8; 32],
    pub supported_ciphers: Vec<CipherSuite>,
    pub session_id: Option<Vec<u8>>,
}

#[derive(Debug, Clone)]
pub struct ServerHello {
    pub server_random: [u8; 32],
    pub chosen_cipher: CipherSuite,
    pub session_id: Vec<u8>,
    pub certificate: Certificate,
}

#[derive(Debug, Clone)]
pub struct KeyExchange {
    pub client_key_exchange: Vec<u8>,  // DH public key or encrypted premaster secret
}

#[derive(Debug, Clone)]
pub struct Finished {
    pub verify_data: Vec<u8>,  // MAC of all handshake messages
}

pub struct TlsHandshake {
    is_server: bool,
    state: HandshakeState,
    client_random: Option<[u8; 32]>,
    server_random: Option<[u8; 32]>,
    chosen_cipher: Option<CipherSuite>,
    premaster_secret: Option<Vec<u8>>,
    master_secret: Option<Vec<u8>>,
    handshake_messages: Vec<Vec<u8>>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum HandshakeState {
    Initial,
    ClientHelloSent,
    ServerHelloReceived,
    CertificateReceived,
    KeyExchangeComplete,
    Finished,
}

impl TlsHandshake {
    pub fn new_client() -> Self {
        Self {
            is_server: false,
            state: HandshakeState::Initial,
            client_random: None,
            server_random: None,
            chosen_cipher: None,
            premaster_secret: None,
            master_secret: None,
            handshake_messages: Vec::new(),
        }
    }

    pub fn new_server() -> Self {
        Self {
            is_server: true,
            state: HandshakeState::Initial,
            client_random: None,
            server_random: None,
            chosen_cipher: None,
            premaster_secret: None,
            master_secret: None,
            handshake_messages: Vec::new(),
        }
    }

    pub fn send_client_hello(&mut self, supported_ciphers: Vec<CipherSuite>) -> ClientHello {
        // TODO: Create and send ClientHello
        // 1. Generate random client_random (32 bytes)
        // 2. Store client_random
        // 3. Create ClientHello with supported ciphers
        // 4. Record message in handshake_messages
        // 5. Update state to ClientHelloSent
        // 6. Return ClientHello
        todo!()
    }

    pub fn receive_client_hello(&mut self, hello: ClientHello) -> Result<(), &'static str> {
        // TODO: Process ClientHello (server side)
        // 1. Verify we're in correct state
        // 2. Store client_random
        // 3. Record message
        // 4. Update state
        todo!()
    }

    pub fn send_server_hello(
        &mut self,
        certificate: Certificate,
        client_ciphers: &[CipherSuite],
    ) -> Result<ServerHello, &'static str> {
        // TODO: Create and send ServerHello
        // 1. Generate server_random
        // 2. Choose cipher suite from client's supported list
        // 3. Generate session_id
        // 4. Create ServerHello with certificate
        // 5. Record message
        // 6. Update state
        todo!()
    }

    pub fn receive_server_hello(&mut self, hello: ServerHello) -> Result<(), &'static str> {
        // TODO: Process ServerHello (client side)
        // 1. Verify certificate validity
        // 2. Verify certificate signature (simplified)
        // 3. Store server_random and chosen_cipher
        // 4. Record message
        // 5. Update state to ServerHelloReceived
        todo!()
    }

    pub fn send_key_exchange(&mut self) -> Result<KeyExchange, &'static str> {
        // TODO: Create and send KeyExchange
        // 1. Generate premaster secret (48 random bytes)
        // 2. In real TLS: encrypt with server's public key (RSA) or send DH public value
        // 3. For simplicity: just store premaster_secret
        // 4. Derive master_secret from premaster_secret, client_random, server_random
        // 5. Record message
        // 6. Return KeyExchange
        todo!()
    }

    pub fn receive_key_exchange(&mut self, key_exchange: KeyExchange) -> Result<(), &'static str> {
        // TODO: Process KeyExchange (server side)
        // 1. Extract premaster secret (decrypt if RSA, compute DH if DH)
        // 2. Derive master_secret
        // 3. Record message
        // 4. Update state
        todo!()
    }

    pub fn send_finished(&mut self) -> Result<Finished, &'static str> {
        // TODO: Create and send Finished message
        // 1. Compute verify_data: MAC of all handshake messages using master_secret
        // 2. Create Finished message
        // 3. Update state to Finished
        // 4. Return Finished
        todo!()
    }

    pub fn receive_finished(&mut self, finished: Finished) -> Result<(), &'static str> {
        // TODO: Verify Finished message
        // 1. Compute expected verify_data from handshake messages
        // 2. Compare with received verify_data (constant-time)
        // 3. If valid, update state to Finished
        // 4. Return Ok or error
        todo!()
    }

    pub fn is_handshake_complete(&self) -> bool {
        self.state == HandshakeState::Finished
    }

    pub fn get_master_secret(&self) -> Option<&Vec<u8>> {
        self.master_secret.as_ref()
    }

    pub fn derive_session_keys(&self) -> Result<SessionKeys, &'static str> {
        // TODO: Derive session keys from master secret
        // In real TLS, derive client_write_key, server_write_key, client_write_MAC, etc.
        // For this exercise, derive two keys: client_key and server_key
        todo!()
    }
}

#[derive(Debug, Clone)]
pub struct SessionKeys {
    pub client_write_key: Vec<u8>,
    pub server_write_key: Vec<u8>,
    pub client_mac_key: Vec<u8>,
    pub server_mac_key: Vec<u8>,
}

// PRF (Pseudo-Random Function) for deriving keys
fn prf(secret: &[u8], label: &[u8], seed: &[u8], output_len: usize) -> Vec<u8> {
    // TODO: TLS PRF function
    // Simplified version of TLS PRF
    // 1. Combine label and seed
    // 2. Use HMAC to expand secret into output_len bytes
    // 3. Return derived key material
    todo!()
}

// Derive master secret from premaster secret
fn derive_master_secret(
    premaster_secret: &[u8],
    client_random: &[u8; 32],
    server_random: &[u8; 32],
) -> Vec<u8> {
    // TODO: Derive 48-byte master secret
    // master_secret = PRF(premaster_secret, "master secret", client_random + server_random)[0..48]
    todo!()
}

fn generate_random_bytes(len: usize) -> Vec<u8> {
    // TODO: Generate random bytes (use simplified RNG)
    // In production, use CSPRNG
    todo!()
}

fn hmac(key: &[u8], data: &[u8]) -> Vec<u8> {
    // TODO: HMAC function (can reuse from previous exercises)
    todo!()
}

fn constant_time_compare(a: &[u8], b: &[u8]) -> bool {
    // TODO: Constant-time comparison
    todo!()
}

fn current_time() -> u64 {
    use std::time::{SystemTime, UNIX_EPOCH};
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_certificate_validity() {
        let now = current_time();

        let cert = Certificate {
            subject: "example.com".to_string(),
            issuer: "Root CA".to_string(),
            public_key: vec![1, 2, 3, 4],
            valid_from: now - 3600,
            valid_until: now + 3600,
            signature: vec![5, 6, 7, 8],
        };

        assert!(cert.is_valid(now));
        assert!(!cert.is_valid(now - 7200));  // Before valid_from
        assert!(!cert.is_valid(now + 7200));  // After valid_until
    }

    #[test]
    fn test_client_hello() {
        let mut client = TlsHandshake::new_client();

        let ciphers = vec![
            CipherSuite::TLS_ECDHE_RSA_WITH_AES_256_GCM,
            CipherSuite::TLS_DHE_RSA_WITH_AES_128_GCM,
        ];

        let hello = client.send_client_hello(ciphers);

        assert_eq!(hello.client_random.len(), 32);
        assert_eq!(hello.supported_ciphers.len(), 2);
    }

    #[test]
    fn test_server_hello() {
        let mut server = TlsHandshake::new_server();

        let client_hello = ClientHello {
            client_random: [1u8; 32],
            supported_ciphers: vec![CipherSuite::TLS_DHE_RSA_WITH_AES_128_GCM],
            session_id: None,
        };

        server.receive_client_hello(client_hello).unwrap();

        let now = current_time();
        let cert = Certificate {
            subject: "example.com".to_string(),
            issuer: "Root CA".to_string(),
            public_key: vec![1, 2, 3, 4],
            valid_from: now - 3600,
            valid_until: now + 86400,
            signature: vec![5, 6, 7, 8],
        };

        let server_hello = server
            .send_server_hello(cert.clone(), &[CipherSuite::TLS_DHE_RSA_WITH_AES_128_GCM])
            .unwrap();

        assert_eq!(server_hello.server_random.len(), 32);
        assert_eq!(server_hello.chosen_cipher, CipherSuite::TLS_DHE_RSA_WITH_AES_128_GCM);
    }

    #[test]
    fn test_full_handshake() {
        let mut client = TlsHandshake::new_client();
        let mut server = TlsHandshake::new_server();

        // 1. Client sends ClientHello
        let ciphers = vec![CipherSuite::TLS_DHE_RSA_WITH_AES_128_GCM];
        let client_hello = client.send_client_hello(ciphers.clone());

        // 2. Server receives ClientHello
        server.receive_client_hello(client_hello.clone()).unwrap();

        // 3. Server sends ServerHello
        let now = current_time();
        let cert = Certificate {
            subject: "example.com".to_string(),
            issuer: "Root CA".to_string(),
            public_key: vec![1, 2, 3, 4],
            valid_from: now - 3600,
            valid_until: now + 86400,
            signature: vec![5, 6, 7, 8],
        };

        let server_hello = server.send_server_hello(cert, &ciphers).unwrap();

        // 4. Client receives ServerHello
        client.receive_server_hello(server_hello).unwrap();

        // 5. Client sends KeyExchange
        let key_exchange = client.send_key_exchange().unwrap();

        // 6. Server receives KeyExchange
        server.receive_key_exchange(key_exchange).unwrap();

        // 7. Client sends Finished
        let client_finished = client.send_finished().unwrap();

        // 8. Server receives and verifies Finished
        server.receive_finished(client_finished).unwrap();

        // 9. Server sends Finished
        let server_finished = server.send_finished().unwrap();

        // 10. Client receives and verifies Finished
        client.receive_finished(server_finished).unwrap();

        // Both should be in Finished state
        assert!(client.is_handshake_complete());
        assert!(server.is_handshake_complete());

        // Both should have same master secret
        assert_eq!(client.get_master_secret(), server.get_master_secret());
    }

    #[test]
    fn test_cipher_suite_negotiation() {
        let mut server = TlsHandshake::new_server();

        let client_ciphers = vec![
            CipherSuite::TLS_RSA_WITH_AES_128_CBC,
            CipherSuite::TLS_DHE_RSA_WITH_AES_128_GCM,
        ];

        let client_hello = ClientHello {
            client_random: [1u8; 32],
            supported_ciphers: client_ciphers.clone(),
            session_id: None,
        };

        server.receive_client_hello(client_hello).unwrap();

        let now = current_time();
        let cert = Certificate {
            subject: "example.com".to_string(),
            issuer: "Root CA".to_string(),
            public_key: vec![1, 2, 3, 4],
            valid_from: now,
            valid_until: now + 86400,
            signature: vec![5, 6, 7, 8],
        };

        let server_hello = server.send_server_hello(cert, &client_ciphers).unwrap();

        // Server should choose a cipher from client's list
        assert!(client_ciphers.contains(&server_hello.chosen_cipher));
    }

    #[test]
    fn test_master_secret_derivation() {
        let premaster = vec![0x42; 48];
        let client_random = [0x01; 32];
        let server_random = [0x02; 32];

        let master = derive_master_secret(&premaster, &client_random, &server_random);

        assert_eq!(master.len(), 48);
    }

    #[test]
    fn test_session_keys_derivation() {
        let mut client = TlsHandshake::new_client();

        // Simulate completed handshake
        client.client_random = Some([0x01; 32]);
        client.server_random = Some([0x02; 32]);
        client.master_secret = Some(vec![0x42; 48]);
        client.state = HandshakeState::Finished;

        let keys = client.derive_session_keys().unwrap();

        assert!(keys.client_write_key.len() > 0);
        assert!(keys.server_write_key.len() > 0);
        assert_ne!(keys.client_write_key, keys.server_write_key);
    }

    #[test]
    fn test_expired_certificate() {
        let now = current_time();

        let cert = Certificate {
            subject: "example.com".to_string(),
            issuer: "Root CA".to_string(),
            public_key: vec![1, 2, 3, 4],
            valid_from: now - 7200,
            valid_until: now - 3600,  // Expired 1 hour ago
            signature: vec![5, 6, 7, 8],
        };

        assert!(!cert.is_valid(now));
    }

    #[test]
    fn test_not_yet_valid_certificate() {
        let now = current_time();

        let cert = Certificate {
            subject: "example.com".to_string(),
            issuer: "Root CA".to_string(),
            public_key: vec![1, 2, 3, 4],
            valid_from: now + 3600,  // Valid from 1 hour in future
            valid_until: now + 7200,
            signature: vec![5, 6, 7, 8],
        };

        assert!(!cert.is_valid(now));
    }

    #[test]
    fn test_handshake_state_progression() {
        let mut client = TlsHandshake::new_client();

        assert_eq!(client.state, HandshakeState::Initial);

        let ciphers = vec![CipherSuite::TLS_DHE_RSA_WITH_AES_128_GCM];
        client.send_client_hello(ciphers);

        assert_eq!(client.state, HandshakeState::ClientHelloSent);
    }

    #[test]
    fn test_prf_deterministic() {
        let secret = b"secret";
        let label = b"test label";
        let seed = b"seed data";

        let output1 = prf(secret, label, seed, 32);
        let output2 = prf(secret, label, seed, 32);

        assert_eq!(output1, output2);
    }

    #[test]
    fn test_different_randoms_different_master_secret() {
        let premaster = vec![0x42; 48];
        let client_random1 = [0x01; 32];
        let client_random2 = [0x02; 32];
        let server_random = [0x03; 32];

        let master1 = derive_master_secret(&premaster, &client_random1, &server_random);
        let master2 = derive_master_secret(&premaster, &client_random2, &server_random);

        assert_ne!(master1, master2);
    }
}
