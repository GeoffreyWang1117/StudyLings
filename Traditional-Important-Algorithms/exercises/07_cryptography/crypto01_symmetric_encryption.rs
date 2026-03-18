// crypto01_symmetric_encryption.rs
//
// Symmetric Encryption uses the same key for both encryption and decryption.
// AES (Advanced Encryption Standard) is the most widely used symmetric cipher today.
//
// Key concepts:
// - Block cipher: Encrypts fixed-size blocks of data (e.g., 128 bits)
// - Substitution-Permutation Network: Core structure of AES
// - Modes of operation: ECB, CBC, CTR, GCM
// - Key sizes: 128, 192, or 256 bits
//
// Your task: Implement a simplified block cipher with basic operations.
//
// Security considerations:
// - NEVER use ECB mode in production (doesn't hide patterns)
// - Always use authenticated encryption (like AES-GCM)
// - Use proper key derivation functions, not raw passwords
// - Implement constant-time operations to prevent timing attacks

// I AM NOT DONE

const BLOCK_SIZE: usize = 16; // 128 bits
const SBOX: [u8; 256] = [
    // Simplified S-box for demonstration (not cryptographically secure)
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
];

pub struct BlockCipher {
    key: [u8; 16],
}

impl BlockCipher {
    pub fn new(key: [u8; 16]) -> Self {
        Self { key }
    }

    fn substitute_bytes(&self, block: &mut [u8; BLOCK_SIZE]) {
        // TODO: Apply S-box substitution to each byte in the block
        // Hint: Replace each byte with SBOX[byte]
        todo!()
    }

    fn shift_rows(&self, block: &mut [u8; BLOCK_SIZE]) {
        // TODO: Implement simplified row shifting
        // Treat block as 4x4 matrix and shift rows:
        // Row 0: no shift
        // Row 1: shift left by 1
        // Row 2: shift left by 2
        // Row 3: shift left by 3
        // Hint: Work with indices 0,1,2,3 | 4,5,6,7 | 8,9,10,11 | 12,13,14,15
        todo!()
    }

    fn add_round_key(&self, block: &mut [u8; BLOCK_SIZE], round: usize) {
        // TODO: XOR each byte of the block with the corresponding key byte
        // For simplicity, just XOR with key repeatedly
        // In real AES, this would use key schedule
        todo!()
    }

    pub fn encrypt_block(&self, plaintext: [u8; BLOCK_SIZE]) -> [u8; BLOCK_SIZE] {
        // TODO: Implement block encryption
        // 1. Copy plaintext to a mutable block
        // 2. Add round key (round 0)
        // 3. For rounds 1..4:
        //    a. Substitute bytes
        //    b. Shift rows
        //    c. Add round key
        // 4. Return encrypted block
        todo!()
    }

    pub fn decrypt_block(&self, ciphertext: [u8; BLOCK_SIZE]) -> [u8; BLOCK_SIZE] {
        // TODO: Implement block decryption
        // This is simplified - real AES decryption uses inverse operations
        // For this exercise, you can implement a simple reverse of encryption
        // or just use encryption again (making it symmetric like XOR)
        todo!()
    }

    pub fn encrypt(&self, data: &[u8]) -> Vec<u8> {
        // TODO: Encrypt arbitrary-length data
        // 1. Pad data to multiple of BLOCK_SIZE (use PKCS7 padding)
        // 2. Split into blocks
        // 3. Encrypt each block
        // 4. Return concatenated encrypted blocks
        todo!()
    }

    pub fn decrypt(&self, data: &[u8]) -> Result<Vec<u8>, &'static str> {
        // TODO: Decrypt arbitrary-length data
        // 1. Split into blocks
        // 2. Decrypt each block
        // 3. Remove padding
        // 4. Return plaintext
        // Return error if data length is not multiple of BLOCK_SIZE
        todo!()
    }
}

fn pkcs7_pad(data: &[u8], block_size: usize) -> Vec<u8> {
    // TODO: Implement PKCS7 padding
    // Add N bytes of value N where N = block_size - (data.len() % block_size)
    // If data is already aligned, add a full block of padding
    todo!()
}

fn pkcs7_unpad(data: &[u8]) -> Result<Vec<u8>, &'static str> {
    // TODO: Remove PKCS7 padding
    // 1. Get last byte value (this is padding length)
    // 2. Verify all padding bytes have same value
    // 3. Return data without padding
    // Return error if padding is invalid
    todo!()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_block_cipher_creation() {
        let key = [1u8; 16];
        let cipher = BlockCipher::new(key);
        assert_eq!(cipher.key, key);
    }

    #[test]
    fn test_substitute_bytes() {
        let key = [0u8; 16];
        let cipher = BlockCipher::new(key);
        let mut block = [0u8; 16];
        cipher.substitute_bytes(&mut block);

        // First byte should be SBOX[0] = 0x63
        assert_eq!(block[0], 0x63);
    }

    #[test]
    fn test_encrypt_decrypt_block() {
        let key = [42u8; 16];
        let cipher = BlockCipher::new(key);
        let plaintext = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];

        let ciphertext = cipher.encrypt_block(plaintext);
        assert_ne!(ciphertext, plaintext);

        let decrypted = cipher.decrypt_block(ciphertext);
        assert_eq!(decrypted, plaintext);
    }

    #[test]
    fn test_different_keys_different_outputs() {
        let plaintext = [1u8; 16];

        let cipher1 = BlockCipher::new([1u8; 16]);
        let cipher2 = BlockCipher::new([2u8; 16]);

        let ct1 = cipher1.encrypt_block(plaintext);
        let ct2 = cipher2.encrypt_block(plaintext);

        assert_ne!(ct1, ct2);
    }

    #[test]
    fn test_pkcs7_padding() {
        let data = vec![1, 2, 3, 4, 5];
        let padded = pkcs7_pad(&data, 16);

        // Should pad with 11 bytes of value 11
        assert_eq!(padded.len(), 16);
        assert_eq!(padded[15], 11);
        assert_eq!(padded[5], 11);
    }

    #[test]
    fn test_pkcs7_padding_full_block() {
        let data = vec![1u8; 16];
        let padded = pkcs7_pad(&data, 16);

        // Should add full block of padding (16 bytes of value 16)
        assert_eq!(padded.len(), 32);
        assert_eq!(padded[31], 16);
    }

    #[test]
    fn test_pkcs7_unpad() {
        let mut data = vec![1, 2, 3, 4, 5];
        data.extend(vec![11u8; 11]); // Add padding

        let unpadded = pkcs7_unpad(&data).unwrap();
        assert_eq!(unpadded, vec![1, 2, 3, 4, 5]);
    }

    #[test]
    fn test_encrypt_decrypt() {
        let key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
                   0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c];
        let cipher = BlockCipher::new(key);

        let plaintext = b"Hello, World!";
        let ciphertext = cipher.encrypt(plaintext);

        assert_ne!(ciphertext.as_slice(), plaintext);

        let decrypted = cipher.decrypt(&ciphertext).unwrap();
        assert_eq!(decrypted.as_slice(), plaintext);
    }

    #[test]
    fn test_encrypt_empty() {
        let key = [0u8; 16];
        let cipher = BlockCipher::new(key);

        let plaintext = b"";
        let ciphertext = cipher.encrypt(plaintext);

        // Should still have padding
        assert_eq!(ciphertext.len(), 16);
    }

    #[test]
    fn test_encrypt_exact_block() {
        let key = [0u8; 16];
        let cipher = BlockCipher::new(key);

        let plaintext = [1u8; 16];
        let ciphertext = cipher.encrypt(&plaintext);

        // Should add extra padding block
        assert_eq!(ciphertext.len(), 32);
    }

    #[test]
    fn test_decrypt_invalid_length() {
        let key = [0u8; 16];
        let cipher = BlockCipher::new(key);

        let invalid_data = vec![1, 2, 3, 4, 5]; // Not multiple of block size
        let result = cipher.decrypt(&invalid_data);

        assert!(result.is_err());
    }

    #[test]
    fn test_avalanche_effect() {
        let key = [0u8; 16];
        let cipher = BlockCipher::new(key);

        let plaintext1 = [1u8; 16];
        let mut plaintext2 = [1u8; 16];
        plaintext2[0] = 2; // Change one bit

        let ct1 = cipher.encrypt_block(plaintext1);
        let ct2 = cipher.encrypt_block(plaintext2);

        // Count differing bytes (should be significant)
        let diff_count = ct1.iter().zip(ct2.iter())
            .filter(|(a, b)| a != b)
            .count();

        // At least half the bytes should differ (avalanche effect)
        assert!(diff_count >= 8);
    }
}
