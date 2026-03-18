# CPU and Hardware Requirements Analysis

This document analyzes the hardware requirements for each exercise in the multiprocessor programming learning platform.

## Overview

Different exercises have varying requirements for:
- **Number of CPU cores/threads**: Some exercises require more cores to observe contention and scalability
- **Cache hierarchy**: Cache-line padding and false sharing exercises need L1/L2/L3 cache
- **Memory ordering visibility**: Exercises testing memory models benefit from weaker memory ordering architectures
- **NUMA awareness**: Large-scale exercises may benefit from NUMA systems

## Hardware Requirement Categories

### Minimal Requirements (2-4 cores)
Suitable for basic learning, correctness testing, and understanding fundamental concepts.

### Standard Requirements (4-8 cores)
Optimal for most exercises, allows observation of contention and basic scalability.

### High Requirements (8-16 cores)
Needed to observe significant performance differences and scalability issues.

### Very High Requirements (16+ cores)
Required for advanced scalability testing and observing contention effects at scale.

---

## Detailed Exercise Analysis

### Chapter 1: Basics

#### Exercise 01: Hello Threads
- **Minimum cores**: 1 (single core with time-slicing)
- **Recommended cores**: 2-4
- **Key observations**:
  - With 1-2 cores: Thread scheduling overhead visible
  - With 4+ cores: True parallelism
- **Special requirements**: None
- **Learning impact**: Understanding thread lifecycle works on any hardware

#### Exercise 02: Race Condition
- **Minimum cores**: 2
- **Recommended cores**: 4-8
- **Key observations**:
  - With 2 cores: Race conditions may be intermittent
  - With 4+ cores: Higher probability of observing races
  - With 8+ cores: Races become very frequent
- **Special requirements**: None
- **Learning impact**: More cores = more visible race conditions

#### Exercise 03: Synchronization
- **Minimum cores**: 2
- **Recommended cores**: 4-8
- **Key observations**:
  - With 2-4 cores: Basic synchronization overhead visible
  - With 8+ cores: Lock contention becomes significant
- **Special requirements**: None
- **Learning impact**: Contention effects more visible with more cores

---

### Chapter 2: Mutual Exclusion

#### Exercise 01: Peterson Lock
- **Minimum cores**: 2 (exactly 2, algorithm is two-thread only)
- **Recommended cores**: 2
- **Key observations**:
  - Requires exactly 2 threads for correctness
  - Memory ordering effects visible on weak memory models (ARM, PowerPC)
  - x86 strong ordering may hide issues
- **Special requirements**:
  - **Weak memory ordering CPU** (ARM, RISC-V) recommended for full learning
  - x86/x64 less instructive due to strong memory model
- **Learning impact**: ARM/RISC-V shows memory ordering importance

#### Exercise 02: Filter Lock
- **Minimum cores**: 2
- **Recommended cores**: 4-8
- **Optimal cores**: 8-16
- **Key observations**:
  - With 2-4 cores: Basic algorithm understanding
  - With 8+ cores: Contention "hot spots" at higher levels
  - With 16+ cores: Severe contention, poor scalability visible
- **Special requirements**: None
- **Learning impact**: More cores = clearer demonstration of poor scalability

#### Exercise 03: Bakery Lock (if added)
- **Minimum cores**: 2
- **Recommended cores**: 8-16
- **Key observations**:
  - Requires many cores to show O(n²) space complexity impact
  - Cache pollution effects visible with 8+ cores
- **Special requirements**: Large L1/L2 cache helpful
- **Learning impact**: High core count essential for observing scalability issues

---

### Chapter 3: Concurrent Objects

#### Exercise 01: Sequential Consistency
- **Minimum cores**: 2
- **Recommended cores**: 4
- **Key observations**:
  - Conceptual exercise, works on any hardware
  - Memory ordering effects visible on weak memory models
- **Special requirements**: None
- **Learning impact**: Understanding works on minimal hardware

#### Exercise 02: Linearizability
- **Minimum cores**: 2
- **Recommended cores**: 4-8
- **Key observations**:
  - With 2-4 cores: Basic linearization points visible
  - With 8+ cores: Concurrent operation interleaving increases
- **Special requirements**: None
- **Learning impact**: More cores = more complex interleavings to reason about

#### Exercise 03: Progress Conditions
- **Minimum cores**: 4
- **Recommended cores**: 8-16
- **Optimal cores**: 16+
- **Key observations**:
  - With 4 cores: Basic differences between wait-free, lock-free, blocking
  - With 8-16 cores: Lock-free vs blocking performance gap widens
  - With 16+ cores: Dramatic scalability differences
- **Special requirements**: None
- **Learning impact**: **HIGH CORE COUNT CRITICAL** for observing scalability

---

### Chapter 4: Foundations

#### Exercise 01: Atomic Registers
- **Minimum cores**: 2
- **Recommended cores**: 4-8
- **Key observations**:
  - Multi-reader/multi-writer benefits from 4+ threads
  - Timestamp contention visible with 8+ cores
- **Special requirements**:
  - **Weak memory ordering CPU** helpful for understanding atomicity
- **Learning impact**: More readers/writers = more interesting scenarios

---

### Chapter 5: Synchronization Primitives

#### Exercise 01: Compare-and-Swap
- **Minimum cores**: 2
- **Recommended cores**: 4-8
- **Optimal cores**: 8-16
- **Key observations**:
  - With 2-4 cores: CAS retry loops occasional
  - With 8+ cores: CAS contention becomes significant
  - With 16+ cores: Exponential backoff effectiveness visible
- **Special requirements**:
  - CPU with efficient CAS instruction (all modern CPUs)
- **Learning impact**: High contention scenarios need 8+ cores

---

### Chapter 6: Consensus

#### Exercise 01: Consensus Hierarchy
- **Minimum cores**: 2
- **Recommended cores**: 4-8
- **Key observations**:
  - Conceptual exercise demonstrating consensus numbers
  - Universal construction benefits from 4+ threads for testing
- **Special requirements**: None
- **Learning impact**: Works well on standard hardware

---

### Chapter 7: Spin Locks

#### Exercise 01: Spin Locks (TAS, TTAS, Backoff, Anderson, MCS)
- **Minimum cores**: 2
- **Recommended cores**: 8-16
- **Optimal cores**: 16-32+
- **Key observations**:
  - With 2-4 cores: All locks perform similarly
  - With 8 cores: TAS/TTAS start showing contention
  - With 16 cores: MCS/Anderson dramatically outperform TAS/TTAS
  - With 32+ cores: **Critical for observing scalability differences**
- **Special requirements**:
  - **Large L3 cache** (8MB+) for cache pollution effects
  - **High cache coherence traffic** visible on many cores
  - **NUMA systems** (2+ sockets) show Anderson lock benefits
- **Learning impact**: **MOST CORE-SENSITIVE EXERCISE**
  - 2-4 cores: Educational value LOW
  - 8-16 cores: Educational value MEDIUM
  - 16-32+ cores: Educational value HIGH

---

### Chapter 8: Monitors

#### Exercise 01: Monitors (Bounded Buffer, Readers-Writers, etc.)
- **Minimum cores**: 2
- **Recommended cores**: 4-8
- **Key observations**:
  - Bounded buffer: 4+ cores for producer/consumer parallelism
  - Readers-writers: 8+ cores to show reader scalability
  - Dining philosophers: 5 cores minimum (5 philosophers)
- **Special requirements**: None
- **Learning impact**: Standard hardware sufficient

---

### Chapter 9: Linked Lists

#### Exercise 01: Concurrent Lists (Coarse, Fine, Optimistic, Lazy)
- **Minimum cores**: 2
- **Recommended cores**: 8-16
- **Optimal cores**: 16+
- **Key observations**:
  - With 2-4 cores: Minimal difference between strategies
  - With 8 cores: Fine-grained locking shows benefits
  - With 16+ cores: Lazy synchronization significantly outperforms coarse
- **Special requirements**: None
- **Learning impact**: Need 8+ cores for meaningful performance comparison

---

### Chapter 10: Concurrent Queues

#### Exercise 01: Concurrent Queues (Bounded, Unbounded, Lock-Free)
- **Minimum cores**: 2
- **Recommended cores**: 8-16
- **Optimal cores**: 16+
- **Key observations**:
  - With 2-4 cores: Lock-free shows minimal advantage
  - With 8 cores: Lock-free begins to outperform locked
  - With 16+ cores: Lock-free scalability advantage dramatic
- **Special requirements**:
  - **Memory ordering visibility** on weak memory architectures
- **Learning impact**: 8+ cores needed to justify lock-free complexity

---

### Chapter 11: Concurrent Stacks

#### Exercise 01: Concurrent Stacks (Lock-Based, Lock-Free, Elimination)
- **Minimum cores**: 4
- **Recommended cores**: 8-16
- **Optimal cores**: 16-32+
- **Key observations**:
  - With 4 cores: Basic Treiber stack works well
  - With 8-16 cores: Top-of-stack contention becomes bottleneck
  - With 16+ cores: **Elimination backoff shows dramatic benefits**
  - With 32+ cores: Elimination array size tuning becomes critical
- **Special requirements**:
  - **High cache coherence bandwidth** for elimination to show benefits
  - **Many cores essential** for elimination effectiveness
- **Learning impact**: **HIGH CORE COUNT HIGHLY RECOMMENDED**
  - Without 16+ cores, elimination seems unnecessarily complex

---

### Chapter 12: Parallel Counting (Part 2)

#### Exercise 01: Parallel Counting (Combining, Padded, Striped)
- **Minimum cores**: 4
- **Recommended cores**: 8-16
- **Optimal cores**: 16-32+
- **Key observations**:
  - With 4 cores: Some contention visible
  - With 8 cores: Cache-line padding effects visible
  - With 16+ cores: **Striping and combining show major benefits**
  - With 32+ cores: False sharing effects dramatic without padding
- **Special requirements**:
  - **64-byte cache line** (standard on x86, ARM)
  - **Cache coherence protocol** that exhibits false sharing
  - **Large L3 cache** helps observe cache pollution
- **Learning impact**: **VERY CORE-SENSITIVE**
  - 4-8 cores: Can observe basic effects
  - 16+ cores: Full educational value, dramatic performance differences

---

### Chapter 13: Concurrent Hashing (Part 2)

#### Exercise 01: Concurrent Hash Maps (Striped, Lock-Free, Cuckoo)
- **Minimum cores**: 4
- **Recommended cores**: 8-16
- **Optimal cores**: 16+
- **Key observations**:
  - With 4 cores: Lock striping shows some benefit
  - With 8-16 cores: Stripe count tuning becomes important
  - With 16+ cores: Dynamic resizing contention visible
- **Special requirements**: None
- **Learning impact**: 8+ cores recommended for performance comparisons

---

### Chapter 14: Skip Lists (Part 2)

#### Exercise 01: Lock-Free Skip List
- **Minimum cores**: 2
- **Recommended cores**: 8-16
- **Key observations**:
  - With 2-4 cores: Algorithm complexity seems unjustified
  - With 8+ cores: Lock-free benefits become apparent
  - With 16+ cores: Scalability advantages clear
- **Special requirements**: None
- **Learning impact**: 8+ cores needed to justify lock-free complexity

---

### Chapter 18: Transactional Memory (Part 2)

#### Exercise 01: Software Transactional Memory (STM)
- **Minimum cores**: 4
- **Recommended cores**: 8-16
- **Optimal cores**: 16+
- **Key observations**:
  - With 4 cores: Retry overhead visible but manageable
  - With 8-16 cores: Contention causes transaction retries
  - With 16+ cores: Optimistic concurrency vs locking trade-offs clear
- **Special requirements**:
  - **Hardware Transactional Memory** (Intel TSX, ARM TME) if comparing to HTM
- **Learning impact**: 8+ cores recommended for observing contention

---

## Special Hardware Considerations

### Cache Line Size
**Critical for**: Chapter 12 (Parallel Counting), Chapter 7 (Spin Locks)
- Standard: 64 bytes (x86, ARM)
- Some ARM: 128 bytes
- Padding exercises assume 64-byte cache lines

### Memory Ordering Architecture
**Critical for**: Chapter 2 (Mutual Exclusion), Chapter 4 (Atomic Registers)
- **Strong ordering (x86/x64)**: Hides many memory ordering bugs
- **Weak ordering (ARM, RISC-V, PowerPC)**: Exposes memory ordering issues
- **Recommendation**: Test on ARM or use ThreadSanitizer on x86

### NUMA Systems
**Beneficial for**: Chapter 7 (Spin Locks), Chapter 12 (Counting)
- Systems with 2+ CPU sockets
- Non-uniform memory access latencies
- Shows importance of locality-aware algorithms

### Hardware Transactional Memory (HTM)
**Relevant for**: Chapter 18 (Transactional Memory)
- Intel TSX (Transactional Synchronization Extensions)
- IBM POWER8+ TM
- ARM TME (Transactional Memory Extension)
- Not required but enables HTM vs STM comparison

---

## Recommended Hardware Configurations

### Minimum Learning Configuration
- **CPU**: 4 cores / 8 threads
- **Architecture**: Any modern x86-64 or ARM64
- **RAM**: 8 GB
- **Learning coverage**: ~60% of concepts observable

### Standard Learning Configuration
- **CPU**: 8 cores / 16 threads
- **Architecture**: x86-64 or ARM64
- **RAM**: 16 GB
- **Learning coverage**: ~85% of concepts observable

### Optimal Learning Configuration
- **CPU**: 16+ cores / 32+ threads
- **Architecture**: ARM64 (for weak memory ordering) or x86-64
- **RAM**: 32 GB
- **Special**: NUMA system (2+ sockets) if possible
- **Learning coverage**: ~95% of concepts fully observable

### Professional/Research Configuration
- **CPU**: 32+ cores / 64+ threads
- **Architecture**: Multi-socket NUMA system
- **RAM**: 64+ GB
- **Special**: HTM support (Intel TSX or ARM TME)
- **Learning coverage**: 100% including advanced scalability studies

---

## Core Count Impact Summary

| Core Count | Exercises with Full Educational Value | Limitations |
|------------|--------------------------------------|-------------|
| 2 cores | Chapters 1-3, Peterson Lock | Cannot observe scalability, contention minimal |
| 4 cores | Chapters 1-6, basic data structures | Spin lock differences unclear, elimination ineffective |
| 8 cores | Chapters 1-11 (partial value) | Scalability differences visible but not dramatic |
| 16 cores | All chapters (good value) | Most scalability effects clearly visible |
| 32+ cores | All chapters (optimal value) | Full scalability spectrum, dramatic performance differences |

---

## Exercise Priority by Core Count

### If you have 4 cores or fewer:
**Focus on**: Chapters 1-6, 8
- Correctness and fundamental concepts
- Basic synchronization patterns
- Skip performance comparisons

### If you have 8 cores:
**Focus on**: All chapters, but performance comparisons have limited value
- Can observe basic contention
- Lock-free advantages subtle
- Elimination backoff seems over-engineered

### If you have 16+ cores:
**All chapters have full educational value**
- Performance differences are dramatic
- Scalability issues clearly visible
- Justifies complexity of advanced algorithms

---

## Testing Recommendations

### For Contention-Sensitive Exercises:
1. **Vary thread count**: Test with threads = cores, threads = 2×cores
2. **Measure cache misses**: Use `perf` on Linux to count cache misses
3. **Monitor contention**: Use profiling tools to identify hot locks
4. **Thread affinity**: Pin threads to cores for consistent results

### For Memory Ordering Exercises:
1. **Use thread sanitizers**: ThreadSanitizer (TSan) on any architecture
2. **Test on ARM**: If possible, run on ARM64 to see memory ordering effects
3. **Stress testing**: Run millions of iterations to catch rare race conditions

### For Performance Comparison:
1. **Warm-up runs**: Discard first few runs for JIT compilation
2. **Multiple runs**: Average 5-10 runs for statistical significance
3. **Isolate cores**: Use `taskset` on Linux to isolate CPU cores
4. **Disable frequency scaling**: Lock CPU frequency for consistent timing

---

## Cloud Testing Options

For students without access to high-core-count systems:

### AWS EC2 Instances:
- **c6i.8xlarge**: 32 vCPUs (16 cores), good for most exercises
- **c6i.16xlarge**: 64 vCPUs (32 cores), excellent for all exercises
- **Graviton (ARM)**: c7g instances for weak memory ordering tests

### Azure:
- **F32s_v2**: 32 vCPUs, high compute performance
- **Ampere (ARM)**: Dpds_v5 series for ARM testing

### Google Cloud:
- **c2-standard-30**: 30 vCPUs
- **Tau T2A (ARM)**: ARM-based VMs for memory ordering tests

### Budget Option:
- **GitHub Actions**: Free CI/CD with 2-core runners (sufficient for basic testing)
- **GitLab CI**: Free tier with 2-core runners

---

## Conclusion

The multiprocessor programming exercises have varying hardware requirements:

- **Correctness understanding**: 2-4 cores sufficient
- **Basic performance understanding**: 8 cores recommended
- **Full educational value**: 16+ cores optimal
- **Research and advanced study**: 32+ cores ideal

The most hardware-sensitive exercises are:
1. **Chapter 7**: Spin Locks (16+ cores essential)
2. **Chapter 11**: Elimination Backoff (16+ cores highly recommended)
3. **Chapter 12**: Parallel Counting (16+ cores highly recommended)
4. **Chapter 3**: Progress Conditions (8+ cores recommended)

Students with limited hardware should focus on correctness and fundamental concepts rather than performance comparisons. Cloud instances can be used sparingly for high-core-count experiments.
