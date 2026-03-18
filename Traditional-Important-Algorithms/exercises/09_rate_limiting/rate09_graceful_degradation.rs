// rate09_graceful_degradation.rs
//
// Graceful Degradation is a fault tolerance pattern that maintains partial
// functionality when a system component fails, rather than complete failure.
//
// Strategies:
// - Fallback to cached/default values
// - Reduced functionality mode
// - Alternative service endpoints
// - Feature toggling based on system health
//
// Your task: Implement graceful degradation strategies.
//
// Key concepts:
// - Service health monitoring
// - Fallback mechanisms
// - Quality of service levels
// - Partial failure handling

// I AM NOT DONE

use std::collections::HashMap;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum ServiceHealth {
    Healthy,
    Degraded,
    Failing,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum QualityLevel {
    Full,       // All features enabled
    Reduced,    // Some features disabled
    Minimal,    // Only critical features
}

pub struct ServiceEndpoint<T> {
    primary: Box<dyn Fn() -> Result<T, String>>,
    fallback: Option<Box<dyn Fn() -> Result<T, String>>>,
    cache: Option<T>,
    health: ServiceHealth,
    last_success: Option<Instant>,
    failure_count: usize,
}

pub struct GracefulDegradation<T> {
    services: HashMap<String, ServiceEndpoint<T>>,
    health_check_interval: Duration,
    failure_threshold: usize,
}

impl<T: Clone> GracefulDegradation<T> {
    pub fn new(health_check_interval: Duration, failure_threshold: usize) -> Self {
        // TODO: Initialize graceful degradation system
        todo!()
    }

    pub fn register_service(
        &mut self,
        name: String,
        primary: Box<dyn Fn() -> Result<T, String>>,
        fallback: Option<Box<dyn Fn() -> Result<T, String>>>,
    ) {
        // TODO: Register a service with primary and optional fallback
        // - Create ServiceEndpoint with given functions
        // - Initialize health as Healthy
        // - Set failure_count to 0
        todo!()
    }

    pub fn call_service(&mut self, name: &str) -> Result<T, DegradationError> {
        // TODO: Call service with graceful degradation
        //
        // Strategy:
        // 1. Get service, return NotFound if doesn't exist
        // 2. Try primary service
        // 3. If success:
        //    - Update cache with result
        //    - Reset failure_count
        //    - Update health to Healthy
        //    - Update last_success
        //    - Return Ok(result)
        // 4. If failure:
        //    - Increment failure_count
        //    - Update health based on failure_count
        //    - Try fallback if available
        //    - If fallback succeeds, return Ok but keep degraded health
        //    - If no fallback or fallback fails, try cache
        //    - If cache exists, return cached value
        //    - Otherwise return Err(Unavailable)
        todo!()
    }

    pub fn get_health(&self, name: &str) -> Option<ServiceHealth> {
        // TODO: Return health status of service
        todo!()
    }

    pub fn get_quality_level(&self, name: &str) -> Option<QualityLevel> {
        // TODO: Determine quality level based on health
        // - Healthy -> Full
        // - Degraded -> Reduced
        // - Failing -> Minimal
        todo!()
    }

    pub fn update_cache(&mut self, name: &str, value: T) {
        // TODO: Manually update cache for a service
        todo!()
    }

    pub fn clear_cache(&mut self, name: &str) {
        // TODO: Clear cache for a service
        todo!()
    }

    pub fn reset_health(&mut self, name: &str) {
        // TODO: Reset service health to Healthy
        // - Set health to Healthy
        // - Reset failure_count to 0
        todo!()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum DegradationError {
    NotFound,
    Unavailable,
}

// Feature flag manager for graceful degradation
pub struct FeatureFlags {
    flags: HashMap<String, bool>,
    dependencies: HashMap<String, Vec<String>>, // Feature -> required services
}

impl FeatureFlags {
    pub fn new() -> Self {
        // TODO: Initialize feature flags
        todo!()
    }

    pub fn register_feature(&mut self, name: String, dependencies: Vec<String>) {
        // TODO: Register feature with service dependencies
        // - Add to flags as enabled by default
        // - Store dependencies
        todo!()
    }

    pub fn disable_feature(&mut self, name: &str) {
        // TODO: Disable a feature
        todo!()
    }

    pub fn enable_feature(&mut self, name: &str) {
        // TODO: Enable a feature
        todo!()
    }

    pub fn is_enabled(&self, name: &str) -> bool {
        // TODO: Check if feature is enabled
        // - Return false if not found
        todo!()
    }

    pub fn update_based_on_health(&mut self, service_health: &HashMap<String, ServiceHealth>) {
        // TODO: Update feature flags based on service health
        // - For each feature:
        //   - Check health of all dependency services
        //   - If any dependency is Failing, disable feature
        //   - If all dependencies are Healthy, enable feature
        todo!()
    }

    pub fn enabled_features(&self) -> Vec<String> {
        // TODO: Return list of enabled features
        todo!()
    }
}

impl Default for FeatureFlags {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_graceful_degradation_creation() {
        let degradation: GracefulDegradation<i32> = GracefulDegradation::new(
            Duration::from_secs(1),
            3,
        );
        assert_eq!(degradation.get_health("test"), None);
    }

    #[test]
    fn test_register_and_call_service() {
        let mut degradation = GracefulDegradation::new(Duration::from_secs(1), 3);

        degradation.register_service(
            "test".to_string(),
            Box::new(|| Ok(42)),
            None,
        );

        let result = degradation.call_service("test");
        assert_eq!(result, Ok(42));
        assert_eq!(degradation.get_health("test"), Some(ServiceHealth::Healthy));
    }

    #[test]
    fn test_fallback_on_primary_failure() {
        let mut degradation = GracefulDegradation::new(Duration::from_secs(1), 3);

        degradation.register_service(
            "test".to_string(),
            Box::new(|| Err("primary failed".to_string())),
            Some(Box::new(|| Ok(99))),
        );

        let result = degradation.call_service("test");
        assert_eq!(result, Ok(99)); // Fallback succeeded
    }

    #[test]
    fn test_cache_on_all_failures() {
        let mut degradation = GracefulDegradation::new(Duration::from_secs(1), 3);

        degradation.register_service(
            "test".to_string(),
            Box::new(|| Ok(42)),
            None,
        );

        // First call succeeds and caches
        degradation.call_service("test").ok();

        // Update service to fail
        degradation.register_service(
            "test".to_string(),
            Box::new(|| Err("failed".to_string())),
            None,
        );

        // Should return cached value
        let result = degradation.call_service("test");
        assert_eq!(result, Ok(42));
    }

    #[test]
    fn test_health_degradation() {
        let mut degradation = GracefulDegradation::new(Duration::from_secs(1), 2);

        degradation.register_service(
            "test".to_string(),
            Box::new(|| Err("fail".to_string())),
            None,
        );

        // First failure
        degradation.call_service("test").ok();
        assert_eq!(degradation.get_health("test"), Some(ServiceHealth::Degraded));

        // Second failure (reaches threshold)
        degradation.call_service("test").ok();
        assert_eq!(degradation.get_health("test"), Some(ServiceHealth::Failing));
    }

    #[test]
    fn test_quality_levels() {
        let mut degradation = GracefulDegradation::new(Duration::from_secs(1), 2);

        degradation.register_service(
            "test".to_string(),
            Box::new(|| Ok(42)),
            None,
        );

        // Initially healthy
        degradation.call_service("test").ok();
        assert_eq!(degradation.get_quality_level("test"), Some(QualityLevel::Full));

        // Cause degradation
        degradation.register_service(
            "test".to_string(),
            Box::new(|| Err("fail".to_string())),
            None,
        );
        degradation.call_service("test").ok();
        assert_eq!(degradation.get_quality_level("test"), Some(QualityLevel::Reduced));
    }

    #[test]
    fn test_service_not_found() {
        let mut degradation: GracefulDegradation<i32> = GracefulDegradation::new(
            Duration::from_secs(1),
            3,
        );

        let result = degradation.call_service("nonexistent");
        assert_eq!(result, Err(DegradationError::NotFound));
    }

    #[test]
    fn test_reset_health() {
        let mut degradation = GracefulDegradation::new(Duration::from_secs(1), 2);

        degradation.register_service(
            "test".to_string(),
            Box::new(|| Err("fail".to_string())),
            None,
        );

        // Cause failures
        degradation.call_service("test").ok();
        degradation.call_service("test").ok();
        assert_eq!(degradation.get_health("test"), Some(ServiceHealth::Failing));

        // Reset
        degradation.reset_health("test");
        assert_eq!(degradation.get_health("test"), Some(ServiceHealth::Healthy));
    }

    #[test]
    fn test_feature_flags() {
        let mut flags = FeatureFlags::new();

        flags.register_feature("search".to_string(), vec!["search-service".to_string()]);
        assert!(flags.is_enabled("search"));

        flags.disable_feature("search");
        assert!(!flags.is_enabled("search"));

        flags.enable_feature("search");
        assert!(flags.is_enabled("search"));
    }

    #[test]
    fn test_feature_flags_health_based() {
        let mut flags = FeatureFlags::new();

        flags.register_feature(
            "recommendations".to_string(),
            vec!["rec-service".to_string()],
        );

        let mut health = HashMap::new();
        health.insert("rec-service".to_string(), ServiceHealth::Failing);

        flags.update_based_on_health(&health);

        // Feature should be disabled due to failing dependency
        assert!(!flags.is_enabled("recommendations"));
    }

    #[test]
    fn test_enabled_features_list() {
        let mut flags = FeatureFlags::new();

        flags.register_feature("feature1".to_string(), vec![]);
        flags.register_feature("feature2".to_string(), vec![]);
        flags.register_feature("feature3".to_string(), vec![]);

        flags.disable_feature("feature2");

        let mut enabled = flags.enabled_features();
        enabled.sort();

        assert_eq!(enabled, vec!["feature1", "feature3"]);
    }

    #[test]
    fn test_manual_cache_update() {
        let mut degradation = GracefulDegradation::new(Duration::from_secs(1), 3);

        degradation.register_service(
            "test".to_string(),
            Box::new(|| Err("fail".to_string())),
            None,
        );

        degradation.update_cache("test", 123);

        let result = degradation.call_service("test");
        assert_eq!(result, Ok(123));
    }

    #[test]
    fn test_clear_cache() {
        let mut degradation = GracefulDegradation::new(Duration::from_secs(1), 3);

        degradation.register_service(
            "test".to_string(),
            Box::new(|| Ok(42)),
            None,
        );

        // Cache value
        degradation.call_service("test").ok();

        degradation.clear_cache("test");

        // Update to failing
        degradation.register_service(
            "test".to_string(),
            Box::new(|| Err("fail".to_string())),
            None,
        );

        // Should fail (no cache)
        let result = degradation.call_service("test");
        assert_eq!(result, Err(DegradationError::Unavailable));
    }
}
