// dist06_lease_mechanism.rs
//
// Leases are time-based locks used in distributed systems to grant exclusive
// access to a resource for a limited time. They're essential for coordination
// without requiring continuous communication.
//
// Key properties:
// - Time-bounded: Automatically expire after a duration
// - No revocation needed: Holder knows when lease expires
// - Fault-tolerant: System recovers when lease expires
// - Used for: Leader election, distributed locks, cache consistency
//
// Your task: Implement a lease-based distributed lock system.
//
// Key concepts:
// - Lease grant: Server grants lease to a client for specific duration
// - Lease renewal: Client can renew before expiration
// - Lease expiration: Automatic release when time runs out
// - Clock skew: Handle minor time differences between nodes

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub struct Lease {
    pub resource: String,
    pub holder: String,
    pub granted_at: u64,
    pub expires_at: u64,
    pub version: u64,
}

impl Lease {
    pub fn new(resource: String, holder: String, granted_at: u64, duration: u64, version: u64) -> Self {
        Self {
            resource,
            holder,
            granted_at,
            expires_at: granted_at + duration,
            version,
        }
    }

    pub fn is_expired(&self, current_time: u64) -> bool {
        current_time >= self.expires_at
    }

    pub fn remaining_time(&self, current_time: u64) -> u64 {
        if self.is_expired(current_time) {
            0
        } else {
            self.expires_at - current_time
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum LeaseError {
    AlreadyLeased,
    NotHolder,
    Expired,
    ResourceNotFound,
}

pub struct LeaseManager {
    leases: HashMap<String, Lease>,
    current_time: u64,
    default_duration: u64,
    max_duration: u64,
    version_counter: u64,
}

impl LeaseManager {
    pub fn new(default_duration: u64, max_duration: u64) -> Self {
        Self {
            leases: HashMap::new(),
            current_time: 0,
            default_duration,
            max_duration,
            version_counter: 0,
        }
    }

    pub fn acquire_lease(&mut self, resource: String, holder: String, duration: Option<u64>)
        -> Result<Lease, LeaseError> {
        // TODO: Acquire a new lease
        // - Check if resource already has a valid (non-expired) lease
        // - If expired or no lease, grant new lease
        // - Use provided duration or default_duration (capped at max_duration)
        // - Increment version_counter for new lease
        // - Return the lease or appropriate error
        todo!()
    }

    pub fn renew_lease(&mut self, resource: &str, holder: &str, duration: Option<u64>)
        -> Result<Lease, LeaseError> {
        // TODO: Renew an existing lease
        // - Check if lease exists
        // - Verify caller is the holder
        // - Check if lease has expired (if so, return Expired error)
        // - Extend expires_at by duration (capped at max_duration from current_time)
        // - Increment version
        // - Return updated lease or error
        todo!()
    }

    pub fn release_lease(&mut self, resource: &str, holder: &str) -> Result<(), LeaseError> {
        // TODO: Release a lease early
        // - Check if lease exists
        // - Verify caller is the holder
        // - Remove the lease
        // - Return Ok(()) or appropriate error
        todo!()
    }

    pub fn check_lease(&self, resource: &str) -> Option<&Lease> {
        // TODO: Check current lease status
        // - Return the lease if it exists and is not expired
        // - Return None if no lease or expired
        todo!()
    }

    pub fn advance_time(&mut self, delta: u64) {
        // TODO: Advance current time and clean up expired leases
        // - Increment current_time by delta
        // - Remove all expired leases from the HashMap
        todo!()
    }

    pub fn set_time(&mut self, time: u64) {
        self.current_time = time;
        // Clean up expired leases
        self.leases.retain(|_, lease| !lease.is_expired(self.current_time));
    }

    pub fn get_time(&self) -> u64 {
        self.current_time
    }

    pub fn get_active_leases(&self) -> Vec<Lease> {
        self.leases
            .values()
            .filter(|lease| !lease.is_expired(self.current_time))
            .cloned()
            .collect()
    }

    pub fn get_lease_info(&self, resource: &str) -> Option<LeaseInfo> {
        self.leases.get(resource).map(|lease| {
            LeaseInfo {
                resource: lease.resource.clone(),
                holder: lease.holder.clone(),
                is_expired: lease.is_expired(self.current_time),
                remaining_time: lease.remaining_time(self.current_time),
                version: lease.version,
            }
        })
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct LeaseInfo {
    pub resource: String,
    pub holder: String,
    pub is_expired: bool,
    pub remaining_time: u64,
    pub version: u64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_acquire_lease() {
        let mut manager = LeaseManager::new(100, 500);

        let lease = manager.acquire_lease("resource1".to_string(), "client1".to_string(), None);
        assert!(lease.is_ok());

        let lease = lease.unwrap();
        assert_eq!(lease.resource, "resource1");
        assert_eq!(lease.holder, "client1");
        assert_eq!(lease.expires_at, 100);
    }

    #[test]
    fn test_cannot_acquire_leased_resource() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();

        let result = manager.acquire_lease("resource1".to_string(), "client2".to_string(), None);
        assert_eq!(result, Err(LeaseError::AlreadyLeased));
    }

    #[test]
    fn test_lease_expiration() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();

        // Before expiration
        assert!(manager.check_lease("resource1").is_some());

        // Advance time past expiration
        manager.advance_time(101);

        // After expiration
        assert!(manager.check_lease("resource1").is_none());
    }

    #[test]
    fn test_acquire_after_expiration() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();
        manager.advance_time(101);

        // Different client can now acquire
        let lease = manager.acquire_lease("resource1".to_string(), "client2".to_string(), None);
        assert!(lease.is_ok());
        assert_eq!(lease.unwrap().holder, "client2");
    }

    #[test]
    fn test_renew_lease() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();
        manager.advance_time(50);

        let lease = manager.renew_lease("resource1", "client1", Some(100));
        assert!(lease.is_ok());

        let lease = lease.unwrap();
        assert_eq!(lease.expires_at, 150); // 50 + 100
    }

    #[test]
    fn test_cannot_renew_others_lease() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();

        let result = manager.renew_lease("resource1", "client2", Some(100));
        assert_eq!(result, Err(LeaseError::NotHolder));
    }

    #[test]
    fn test_cannot_renew_expired_lease() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();
        manager.advance_time(101);

        let result = manager.renew_lease("resource1", "client1", Some(100));
        assert_eq!(result, Err(LeaseError::Expired));
    }

    #[test]
    fn test_release_lease() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();

        let result = manager.release_lease("resource1", "client1");
        assert!(result.is_ok());

        // Resource should now be available
        assert!(manager.check_lease("resource1").is_none());
    }

    #[test]
    fn test_cannot_release_others_lease() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();

        let result = manager.release_lease("resource1", "client2");
        assert_eq!(result, Err(LeaseError::NotHolder));
    }

    #[test]
    fn test_max_duration_cap() {
        let mut manager = LeaseManager::new(100, 200);

        let lease = manager.acquire_lease("resource1".to_string(), "client1".to_string(), Some(500));
        assert!(lease.is_ok());

        let lease = lease.unwrap();
        // Should be capped at max_duration (200), not requested 500
        assert_eq!(lease.expires_at, 200);
    }

    #[test]
    fn test_lease_versions() {
        let mut manager = LeaseManager::new(100, 500);

        let lease1 = manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();
        assert_eq!(lease1.version, 1);

        manager.advance_time(50);
        let lease2 = manager.renew_lease("resource1", "client1", None).unwrap();
        assert_eq!(lease2.version, 2);
    }

    #[test]
    fn test_multiple_resources() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();
        manager.acquire_lease("resource2".to_string(), "client2".to_string(), None).unwrap();
        manager.acquire_lease("resource3".to_string(), "client1".to_string(), None).unwrap();

        let active = manager.get_active_leases();
        assert_eq!(active.len(), 3);
    }

    #[test]
    fn test_lease_info() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();
        manager.advance_time(30);

        let info = manager.get_lease_info("resource1").unwrap();
        assert_eq!(info.holder, "client1");
        assert_eq!(info.is_expired, false);
        assert_eq!(info.remaining_time, 70);
    }

    #[test]
    fn test_cleanup_expired_leases() {
        let mut manager = LeaseManager::new(100, 500);

        manager.acquire_lease("resource1".to_string(), "client1".to_string(), None).unwrap();
        manager.acquire_lease("resource2".to_string(), "client2".to_string(), None).unwrap();

        manager.advance_time(101);

        let active = manager.get_active_leases();
        assert_eq!(active.len(), 0);
    }
}
