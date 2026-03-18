// comp07_inline_caching.rs
//
// Inline caching is an optimization technique for dynamic dispatch used in
// dynamic languages. It caches the result of method lookups at call sites
// to avoid repeated lookups.
//
// Your task: Implement inline caching for virtual method calls.
//
// Types of inline caches:
// - Monomorphic: One cached type (fastest)
// - Polymorphic: Few cached types (still fast)
// - Megamorphic: Many types seen (fall back to lookup)

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct TypeId(pub usize);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct MethodId(pub usize);

#[derive(Debug, Clone)]
pub struct VTable {
    pub type_id: TypeId,
    // Maps method names to actual function addresses (simulated as MethodId)
    pub methods: HashMap<String, MethodId>,
}

impl VTable {
    pub fn new(type_id: TypeId) -> Self {
        Self {
            type_id,
            methods: HashMap::new(),
        }
    }

    pub fn add_method(&mut self, name: String, method: MethodId) {
        self.methods.insert(name, method);
    }

    pub fn lookup(&self, method: &str) -> Option<MethodId> {
        self.methods.get(method).copied()
    }
}

#[derive(Debug, Clone)]
pub struct CacheEntry {
    pub type_id: TypeId,
    pub method_id: MethodId,
    pub hit_count: usize,
}

#[derive(Debug, Clone, PartialEq)]
pub enum CacheState {
    Uninitialized,      // No calls yet
    Monomorphic,        // One type seen
    Polymorphic,        // 2-4 types seen
    Megamorphic,        // 5+ types seen (too many to cache efficiently)
}

pub struct InlineCache {
    method_name: String,
    entries: Vec<CacheEntry>,
    miss_count: usize,
    max_polymorphic_size: usize,
}

impl InlineCache {
    pub fn new(method_name: String) -> Self {
        Self {
            method_name,
            entries: Vec::new(),
            miss_count: 0,
            max_polymorphic_size: 4,
        }
    }

    pub fn lookup(&mut self, vtable: &VTable) -> Option<MethodId> {
        // TODO: Lookup method in the cache
        // 1. Check if we have a cached entry for this type
        // 2. If yes, increment hit count and return method
        // 3. If no, record a cache miss and perform vtable lookup
        // 4. Add to cache if not megamorphic
        todo!()
    }

    fn find_cached_entry(&mut self, type_id: TypeId) -> Option<MethodId> {
        // TODO: Search cache entries for matching type
        // If found, increment hit_count and return method
        todo!()
    }

    fn add_to_cache(&mut self, type_id: TypeId, method_id: MethodId) {
        // TODO: Add a new entry to the cache
        // Don't add if already megamorphic
        // Update state after adding
        todo!()
    }

    pub fn state(&self) -> CacheState {
        // TODO: Determine current cache state based on number of entries
        // Uninitialized: 0 entries
        // Monomorphic: 1 entry
        // Polymorphic: 2-4 entries
        // Megamorphic: 5+ entries
        todo!()
    }

    pub fn total_hits(&self) -> usize {
        // TODO: Return total number of cache hits
        todo!()
    }

    pub fn total_misses(&self) -> usize {
        self.miss_count
    }

    pub fn hit_rate(&self) -> f64 {
        // TODO: Calculate hit rate (hits / (hits + misses))
        // Return 0.0 if no calls yet
        todo!()
    }

    pub fn cached_types(&self) -> Vec<TypeId> {
        // TODO: Return all type IDs currently in cache
        todo!()
    }

    pub fn clear(&mut self) {
        // TODO: Clear all cache entries and reset counters
        todo!()
    }
}

pub struct CallSite {
    name: String,
    cache: InlineCache,
    vtable_registry: HashMap<TypeId, VTable>,
}

impl CallSite {
    pub fn new(method_name: String) -> Self {
        Self {
            name: method_name.clone(),
            cache: InlineCache::new(method_name),
            vtable_registry: HashMap::new(),
        }
    }

    pub fn register_vtable(&mut self, vtable: VTable) {
        self.vtable_registry.insert(vtable.type_id, vtable);
    }

    pub fn call(&mut self, receiver_type: TypeId) -> Option<MethodId> {
        // TODO: Perform method call with inline caching
        // 1. Get vtable for receiver type
        // 2. Use cache to lookup method
        // 3. Return method ID if found
        todo!()
    }

    pub fn cache_state(&self) -> CacheState {
        self.cache.state()
    }

    pub fn statistics(&self) -> CacheStats {
        CacheStats {
            hits: self.cache.total_hits(),
            misses: self.cache.total_misses(),
            hit_rate: self.cache.hit_rate(),
            state: self.cache.state(),
            cached_types: self.cache.cached_types().len(),
        }
    }
}

#[derive(Debug, Clone)]
pub struct CacheStats {
    pub hits: usize,
    pub misses: usize,
    pub hit_rate: f64,
    pub state: CacheState,
    pub cached_types: usize,
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_vtable(type_id: usize, method_name: &str, method_id: usize) -> VTable {
        let mut vtable = VTable::new(TypeId(type_id));
        vtable.add_method(method_name.to_string(), MethodId(method_id));
        vtable
    }

    #[test]
    fn test_uninitialized_cache() {
        let cache = InlineCache::new("toString".to_string());
        assert_eq!(cache.state(), CacheState::Uninitialized);
        assert_eq!(cache.total_hits(), 0);
        assert_eq!(cache.total_misses(), 0);
    }

    #[test]
    fn test_monomorphic_cache() {
        let mut call_site = CallSite::new("toString".to_string());

        let vtable = create_vtable(1, "toString", 100);
        call_site.register_vtable(vtable);

        // First call - cache miss
        let result = call_site.call(TypeId(1));
        assert_eq!(result, Some(MethodId(100)));
        assert_eq!(call_site.cache_state(), CacheState::Monomorphic);

        // Second call - cache hit
        let result = call_site.call(TypeId(1));
        assert_eq!(result, Some(MethodId(100)));

        let stats = call_site.statistics();
        assert_eq!(stats.hits, 1);
        assert_eq!(stats.misses, 1);
        assert_eq!(stats.cached_types, 1);
    }

    #[test]
    fn test_polymorphic_cache() {
        let mut call_site = CallSite::new("compute".to_string());

        // Register three different types
        for i in 1..=3 {
            let vtable = create_vtable(i, "compute", 100 + i);
            call_site.register_vtable(vtable);
        }

        // Call with each type
        for i in 1..=3 {
            call_site.call(TypeId(i));
        }

        assert_eq!(call_site.cache_state(), CacheState::Polymorphic);
        assert_eq!(call_site.statistics().cached_types, 3);
    }

    #[test]
    fn test_megamorphic_cache() {
        let mut call_site = CallSite::new("process".to_string());

        // Register many different types
        for i in 1..=6 {
            let vtable = create_vtable(i, "process", 200 + i);
            call_site.register_vtable(vtable);
        }

        // Call with each type
        for i in 1..=6 {
            call_site.call(TypeId(i));
        }

        assert_eq!(call_site.cache_state(), CacheState::Megamorphic);
    }

    #[test]
    fn test_cache_hits() {
        let mut call_site = CallSite::new("method".to_string());

        let vtable = create_vtable(1, "method", 42);
        call_site.register_vtable(vtable);

        // Call multiple times with same type
        for _ in 0..10 {
            let result = call_site.call(TypeId(1));
            assert_eq!(result, Some(MethodId(42)));
        }

        let stats = call_site.statistics();
        assert_eq!(stats.hits, 9);  // First is miss, rest are hits
        assert_eq!(stats.misses, 1);
        assert!(stats.hit_rate > 0.8);
    }

    #[test]
    fn test_polymorphic_hits() {
        let mut call_site = CallSite::new("execute".to_string());

        // Register two types
        for i in 1..=2 {
            let vtable = create_vtable(i, "execute", 300 + i);
            call_site.register_vtable(vtable);
        }

        // Alternate between types
        for _ in 0..5 {
            call_site.call(TypeId(1));
            call_site.call(TypeId(2));
        }

        let stats = call_site.statistics();
        assert_eq!(stats.state, CacheState::Polymorphic);
        assert_eq!(stats.misses, 2);  // One miss per type initially
        assert_eq!(stats.hits, 8);    // Rest are hits
    }

    #[test]
    fn test_cache_clear() {
        let mut call_site = CallSite::new("clear_test".to_string());

        let vtable = create_vtable(1, "clear_test", 999);
        call_site.register_vtable(vtable);

        call_site.call(TypeId(1));
        assert_eq!(call_site.cache_state(), CacheState::Monomorphic);

        call_site.cache.clear();
        assert_eq!(call_site.cache_state(), CacheState::Uninitialized);
        assert_eq!(call_site.cache.total_hits(), 0);
        assert_eq!(call_site.cache.total_misses(), 0);
    }

    #[test]
    fn test_different_methods_same_type() {
        let mut call_site1 = CallSite::new("method1".to_string());
        let mut call_site2 = CallSite::new("method2".to_string());

        let mut vtable = VTable::new(TypeId(1));
        vtable.add_method("method1".to_string(), MethodId(10));
        vtable.add_method("method2".to_string(), MethodId(20));

        call_site1.register_vtable(vtable.clone());
        call_site2.register_vtable(vtable);

        let result1 = call_site1.call(TypeId(1));
        let result2 = call_site2.call(TypeId(1));

        assert_eq!(result1, Some(MethodId(10)));
        assert_eq!(result2, Some(MethodId(20)));
    }

    #[test]
    fn test_missing_method() {
        let mut call_site = CallSite::new("nonexistent".to_string());

        let vtable = create_vtable(1, "other_method", 42);
        call_site.register_vtable(vtable);

        let result = call_site.call(TypeId(1));
        assert_eq!(result, None);
    }

    #[test]
    fn test_hit_rate_calculation() {
        let mut call_site = CallSite::new("test".to_string());

        let vtable = create_vtable(1, "test", 1);
        call_site.register_vtable(vtable);

        // 1 miss + 9 hits = 90% hit rate
        for _ in 0..10 {
            call_site.call(TypeId(1));
        }

        let stats = call_site.statistics();
        assert_eq!(stats.hits, 9);
        assert_eq!(stats.misses, 1);
        assert!((stats.hit_rate - 0.9).abs() < 0.01);
    }
}
