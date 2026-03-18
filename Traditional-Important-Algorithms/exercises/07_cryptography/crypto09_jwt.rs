// crypto09_jwt.rs
//
// JSON Web Tokens (JWT) are a compact, URL-safe means of representing claims
// to be transferred between two parties. They're widely used for authentication
// and information exchange.
//
// JWT structure: header.payload.signature
// - Header: Algorithm and token type (base64url encoded)
// - Payload: Claims/data (base64url encoded)
// - Signature: HMAC or RSA signature of header.payload
//
// Common claims:
// - iss (issuer): Who created the token
// - sub (subject): Who the token is about
// - aud (audience): Who should accept the token
// - exp (expiration): When token expires (Unix timestamp)
// - nbf (not before): Token not valid before this time
// - iat (issued at): When token was created
// - jti (JWT ID): Unique identifier
//
// Your task: Implement JWT creation and verification with HMAC.
//
// Security considerations:
// - Always verify signature before trusting claims
// - Check expiration time (exp claim)
// - Validate issuer and audience
// - Never put sensitive data in payload (it's only encoded, not encrypted)
// - Use HTTPS when transmitting JWTs
// - Store tokens securely (not in localStorage for sensitive apps)
// - Use short expiration times
// - Consider using refresh tokens for long-lived sessions
// - Beware of algorithm confusion attacks (verify "alg" header)

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub struct JwtHeader {
    pub alg: String,  // Algorithm (e.g., "HS256")
    pub typ: String,  // Type (usually "JWT")
}

#[derive(Debug, Clone, PartialEq)]
pub struct JwtPayload {
    claims: HashMap<String, String>,
}

impl JwtPayload {
    pub fn new() -> Self {
        Self {
            claims: HashMap::new(),
        }
    }

    pub fn set_claim(&mut self, key: &str, value: &str) {
        self.claims.insert(key.to_string(), value.to_string());
    }

    pub fn get_claim(&self, key: &str) -> Option<&String> {
        self.claims.get(key)
    }

    pub fn set_expiration(&mut self, exp: u64) {
        self.claims.insert("exp".to_string(), exp.to_string());
    }

    pub fn set_issued_at(&mut self, iat: u64) {
        self.claims.insert("iat".to_string(), iat.to_string());
    }

    pub fn set_subject(&mut self, sub: &str) {
        self.claims.insert("sub".to_string(), sub.to_string());
    }

    pub fn set_issuer(&mut self, iss: &str) {
        self.claims.insert("iss".to_string(), iss.to_string());
    }

    fn to_json(&self) -> String {
        // TODO: Convert payload to JSON string
        // Simple JSON serialization (claims as key-value pairs)
        // Format: {"key1":"value1","key2":"value2"}
        todo!()
    }

    fn from_json(json: &str) -> Result<Self, &'static str> {
        // TODO: Parse JSON string to JwtPayload
        // Simple JSON parsing (extract key-value pairs)
        todo!()
    }
}

pub struct Jwt {
    secret: Vec<u8>,
}

impl Jwt {
    pub fn new(secret: &[u8]) -> Self {
        Self {
            secret: secret.to_vec(),
        }
    }

    pub fn create_token(&self, payload: &JwtPayload) -> String {
        // TODO: Create JWT token
        // 1. Create header with alg="HS256", typ="JWT"
        // 2. Serialize header to JSON and base64url encode
        // 3. Serialize payload to JSON and base64url encode
        // 4. Create signing input: base64url(header).base64url(payload)
        // 5. Sign with HMAC-SHA256
        // 6. base64url encode signature
        // 7. Return header.payload.signature
        todo!()
    }

    pub fn verify_token(&self, token: &str) -> Result<JwtPayload, &'static str> {
        // TODO: Verify and decode JWT token
        // 1. Split token into header, payload, signature parts
        // 2. Verify signature:
        //    a. Recreate signing input from header and payload
        //    b. Compute expected signature
        //    c. Compare with provided signature (constant-time)
        // 3. Decode and verify header (check algorithm)
        // 4. Decode payload
        // 5. Check expiration if present
        // 6. Return payload
        todo!()
    }

    pub fn decode_without_verify(&self, token: &str) -> Result<JwtPayload, &'static str> {
        // TODO: Decode token without verification (for debugging only!)
        // WARNING: Never use this for authentication in production
        // 1. Split token
        // 2. Decode payload
        // 3. Return payload
        todo!()
    }
}

// Base64 URL encoding (RFC 4648)
fn base64url_encode(data: &[u8]) -> String {
    // TODO: Implement base64url encoding
    // Like base64 but:
    // - Use '-' instead of '+'
    // - Use '_' instead of '/'
    // - No padding ('=')
    todo!()
}

fn base64url_decode(s: &str) -> Result<Vec<u8>, &'static str> {
    // TODO: Implement base64url decoding
    // Reverse of base64url_encode
    todo!()
}

// HMAC-SHA256 for signing (simplified)
fn hmac_sha256(key: &[u8], data: &[u8]) -> Vec<u8> {
    // TODO: Implement HMAC-SHA256
    // Can reuse implementation from MAC exercise
    // Or use simplified version for this exercise
    todo!()
}

fn constant_time_compare(a: &[u8], b: &[u8]) -> bool {
    // TODO: Constant-time comparison (same as MAC exercise)
    todo!()
}

fn current_timestamp() -> u64 {
    // TODO: Get current Unix timestamp
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
    fn test_jwt_creation() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let mut payload = JwtPayload::new();
        payload.set_subject("user123");
        payload.set_issuer("myapp");

        let token = jwt.create_token(&payload);

        // Token should have 3 parts separated by dots
        assert_eq!(token.matches('.').count(), 2);
    }

    #[test]
    fn test_jwt_verification() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let mut payload = JwtPayload::new();
        payload.set_subject("user123");

        let token = jwt.create_token(&payload);
        let verified_payload = jwt.verify_token(&token).unwrap();

        assert_eq!(verified_payload.get_claim("sub"), Some(&"user123".to_string()));
    }

    #[test]
    fn test_jwt_tampered_payload() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let mut payload = JwtPayload::new();
        payload.set_subject("user123");

        let token = jwt.create_token(&payload);

        // Tamper with token (change a character in payload)
        let mut tampered = token.clone();
        let bytes = unsafe { tampered.as_bytes_mut() };
        if bytes.len() > 50 {
            bytes[50] ^= 1;
        }

        let result = jwt.verify_token(&tampered);
        assert!(result.is_err());
    }

    #[test]
    fn test_jwt_wrong_secret() {
        let jwt1 = Jwt::new(b"secret1");
        let jwt2 = Jwt::new(b"secret2");

        let mut payload = JwtPayload::new();
        payload.set_subject("user123");

        let token = jwt1.create_token(&payload);

        // Verification with wrong secret should fail
        let result = jwt2.verify_token(&token);
        assert!(result.is_err());
    }

    #[test]
    fn test_jwt_expiration() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let mut payload = JwtPayload::new();
        payload.set_subject("user123");
        payload.set_expiration(current_timestamp() - 3600); // Expired 1 hour ago

        let token = jwt.create_token(&payload);
        let result = jwt.verify_token(&token);

        // Should fail due to expiration
        assert!(result.is_err());
    }

    #[test]
    fn test_jwt_valid_expiration() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let mut payload = JwtPayload::new();
        payload.set_subject("user123");
        payload.set_expiration(current_timestamp() + 3600); // Expires in 1 hour

        let token = jwt.create_token(&payload);
        let result = jwt.verify_token(&token);

        assert!(result.is_ok());
    }

    #[test]
    fn test_multiple_claims() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let mut payload = JwtPayload::new();
        payload.set_subject("user123");
        payload.set_issuer("myapp");
        payload.set_claim("role", "admin");
        payload.set_claim("email", "user@example.com");

        let token = jwt.create_token(&payload);
        let verified = jwt.verify_token(&token).unwrap();

        assert_eq!(verified.get_claim("sub"), Some(&"user123".to_string()));
        assert_eq!(verified.get_claim("iss"), Some(&"myapp".to_string()));
        assert_eq!(verified.get_claim("role"), Some(&"admin".to_string()));
        assert_eq!(verified.get_claim("email"), Some(&"user@example.com".to_string()));
    }

    #[test]
    fn test_base64url_encoding() {
        let data = b"Hello, World!";
        let encoded = base64url_encode(data);

        // Should not contain '+', '/', or '='
        assert!(!encoded.contains('+'));
        assert!(!encoded.contains('/'));
        assert!(!encoded.contains('='));

        let decoded = base64url_decode(&encoded).unwrap();
        assert_eq!(decoded, data);
    }

    #[test]
    fn test_decode_without_verify() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let mut payload = JwtPayload::new();
        payload.set_subject("user123");

        let token = jwt.create_token(&payload);
        let decoded = jwt.decode_without_verify(&token).unwrap();

        assert_eq!(decoded.get_claim("sub"), Some(&"user123".to_string()));
    }

    #[test]
    fn test_empty_payload() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let payload = JwtPayload::new();
        let token = jwt.create_token(&payload);
        let verified = jwt.verify_token(&token).unwrap();

        assert_eq!(verified.claims.len(), 0);
    }

    #[test]
    fn test_issued_at_claim() {
        let secret = b"my-secret-key";
        let jwt = Jwt::new(secret);

        let now = current_timestamp();
        let mut payload = JwtPayload::new();
        payload.set_issued_at(now);

        let token = jwt.create_token(&payload);
        let verified = jwt.verify_token(&token).unwrap();

        assert_eq!(verified.get_claim("iat"), Some(&now.to_string()));
    }

    #[test]
    fn test_payload_json_serialization() {
        let mut payload = JwtPayload::new();
        payload.set_claim("key1", "value1");
        payload.set_claim("key2", "value2");

        let json = payload.to_json();
        let parsed = JwtPayload::from_json(&json).unwrap();

        assert_eq!(parsed.get_claim("key1"), Some(&"value1".to_string()));
        assert_eq!(parsed.get_claim("key2"), Some(&"value2".to_string()));
    }
}
