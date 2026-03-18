# Exercises Overview

Complete list of all exercises in the Multi-Processor Programming Study project.

## Chapter 1: Basics (基础知识)

**Status**: ✅ Complete (Java & C++)

### Exercise 01: Hello Threads
- **Concept**: Thread creation and lifecycle
- **Skills**: Creating threads, joining, basic thread management
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/basics/Exercise01_HelloThreads.java`
  - C++: `exercises/cpp/01_basics/exercise01_hello_threads.cpp`

### Exercise 02: Race Condition
- **Concept**: Understanding race conditions
- **Skills**: Observing data races, understanding shared memory issues
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/basics/Exercise02_RaceCondition.java`
  - C++: `exercises/cpp/01_basics/exercise02_race_condition.cpp`

### Exercise 03: Synchronization
- **Concept**: Basic mutual exclusion
- **Skills**: Using synchronized/mutex, thread-safe counter, bank account example
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/basics/Exercise03_Synchronization.java`
  - C++: `exercises/cpp/01_basics/exercise03_synchronization.cpp`

---

## Chapter 2: Mutual Exclusion (互斥算法)

**Status**: ✅ Complete (Java & C++)

### Exercise 01: Peterson Lock
- **Concept**: Two-thread mutual exclusion algorithm
- **Skills**: Classical mutual exclusion, volatile/atomic variables, memory visibility
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/mutual_exclusion/Exercise01_PetersonLock.java`
  - C++: `exercises/cpp/02_mutual_exclusion/exercise01_peterson_lock.cpp`

### Exercise 02: Filter Lock
- **Concept**: n-thread mutual exclusion
- **Skills**: Generalization of Peterson's algorithm, levels of exclusion
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/mutual_exclusion/Exercise02_FilterLock.java`
  - C++: `exercises/cpp/02_mutual_exclusion/exercise02_filter_lock.cpp`

### Exercise 03: Bakery Lock ⭐ NEW (Phase 8)
- **Concept**: Fair mutual exclusion with FCFS (first-come-first-served)
- **Skills**: Ticket-based mutual exclusion, lexicographic ordering, fairness guarantees
- **Historical**: Leslie Lamport's classic algorithm (1974), introduced logical timestamps
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/mutual_exclusion/Exercise03_BakeryLock.java`
  - C++: `exercises/cpp/02_mutual_exclusion/exercise04_bakery_lock.cpp`

**Key Algorithms Implemented**:
1. **Peterson Lock**: 2-thread mutual exclusion
2. **Filter Lock**: n-thread mutual exclusion (no fairness)
3. **Bakery Lock**: n-thread with FCFS fairness

---

## Chapter 3: Concurrent Objects (并发对象)

**Status**: ✅ Complete (Java), 🔄 Partial (C++)

### Exercise 01: Sequential Consistency
- **Concept**: Sequential consistency model
- **Skills**: Implementing sequentially consistent counter and register
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/concurrent_objects/Exercise01_SequentialConsistency.java`
  - C++: `exercises/cpp/03_concurrent_objects/exercise01_sequential_consistency.cpp`

### Exercise 02: Linearizability
- **Concept**: Linearizability - the gold standard
- **Skills**: Lock-free stack, linearization points, atomic operations
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/concurrent_objects/Exercise02_Linearizability.java`

### Exercise 03: Progress Conditions
- **Concept**: Wait-free, lock-free, obstruction-free, blocking
- **Skills**: Understanding different progress guarantees, performance comparison
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/concurrent_objects/Exercise03_ProgressConditions.java`

---

## Chapter 4: Foundations (共享内存基础)

**Status**: ✅ Complete (Java)

### Exercise 01: Atomic Registers
- **Concept**: SRSW, MRSW, MRMW registers
- **Skills**: Building complex registers from simple ones, timestamps
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/foundations/Exercise01_AtomicRegisters.java`

---

## Chapter 5: Synchronization Primitives (同步原语)

**Status**: ✅ Complete (Java)

### Exercise 01: Compare-and-Swap (CAS)
- **Concept**: CAS operation and its applications
- **Skills**: Lock-free counter, stack, queue, ABA problem
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/synchronization/Exercise01_CompareAndSwap.java`

---

## Chapter 6: Consensus (共识)

**Status**: 📋 Planned

Topics to cover:
- Consensus problem
- Consensus hierarchy
- Universality of consensus

---

## Chapter 7: Spin Locks (自旋锁)

**Status**: ✅ Complete (Java & C++)

### Exercise 01: Spin Lock Implementations
- **Concept**: Different spin lock algorithms
- **Skills**: TAS, TTAS, Backoff, Anderson, MCS, CLH locks
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/spin_locks/Exercise01_SpinLocks.java`
  - C++: `exercises/cpp/07_spin_locks/exercise01_spin_locks.cpp`

**Key Algorithms Implemented**:
1. **TAS Lock**: Simple test-and-set
2. **TTAS Lock**: Test-and-test-and-set (better cache behavior)
3. **Backoff Lock**: Exponential backoff to reduce contention
4. **Anderson Lock**: Array-based queue lock (Java only)
5. **MCS Lock**: Scalable queue-based lock with explicit queue
6. **CLH Lock** ⭐ NEW (Phase 8): Implicit queue, foundation of Java's AQS!

**🔥 Special Note on CLH Lock**:
- **Critical for Java developers**: CLH is the foundation of `AbstractQueuedSynchronizer` (AQS)
- **Used in**: `ReentrantLock`, `Semaphore`, `CountDownLatch`, `ReadWriteLock`
- **Comparison**:
  - **MCS**: Spins on own node, explicit queue, better for NUMA
  - **CLH**: Spins on predecessor's node, implicit queue, better for cache-coherent systems

---

## Chapter 8: Monitors and Blocking (监视器和阻塞同步)

**Status**: 📋 Planned

Topics to cover:
- Condition variables
- Producer-consumer problem
- Readers-writers locks
- Semaphores

---

## Chapter 9: Linked Lists (并发链表)

**Status**: ✅ Complete (Java)

### Exercise 01: Concurrent Linked Lists
- **Concept**: Different synchronization strategies for lists
- **Skills**: Coarse-grained, fine-grained, optimistic, lazy synchronization
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/linked_lists/Exercise01_ConcurrentLists.java`

**Implementations**:
1. **Coarse-Grained**: Single lock for entire list
2. **Fine-Grained**: Hand-over-hand locking
3. **Optimistic**: Lock-free traversal with validation
4. **Lazy**: Logical deletion before physical removal

---

## Chapter 10: Queues (并发队列)

**Status**: ✅ Complete (Java)

### Exercise 01: Concurrent Queues
- **Concept**: Producer-consumer queues
- **Skills**: Bounded/unbounded queues, Michael-Scott algorithm, ABA problem
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/queues/Exercise01_ConcurrentQueues.java`

**Implementations**:
1. **Bounded Blocking Queue**: Fixed capacity with blocking
2. **Unbounded Queue**: Dynamic with separate locks
3. **Michael-Scott Lock-Free Queue**: CAS-based queue

---

## Chapter 11: Stacks (并发栈)

**Status**: ✅ Complete (Java)

### Exercise 01: Concurrent Stacks
- **Concept**: Lock-free and elimination-based stacks
- **Skills**: Treiber stack, elimination backoff
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/stacks/Exercise01_ConcurrentStacks.java`

**Implementations**:
1. **Lock-Based Stack**: Simple with global lock
2. **Lock-Free Stack**: Treiber stack using CAS
3. **Elimination Stack**: Optimization for high contention

---

## Exercise Statistics ⭐ Updated for Phase 8

### Java Exercises
- **Chapter 1**: 3 exercises ✅
- **Chapter 2**: 3 exercises ✅ (+Bakery Lock 🆕)
- **Chapter 3**: 3 exercises ✅
- **Chapter 4**: 1 exercise ✅
- **Chapter 5**: 1 exercise ✅
- **Chapter 6**: 0 exercises (planned)
- **Chapter 7**: 1 exercise (6 algorithms: TAS, TTAS, Backoff, Anderson, MCS, CLH 🆕) ✅
- **Chapter 8**: 0 exercises (planned)
- **Chapter 9**: 1 exercise (4 implementations) ✅
- **Chapter 10**: 1 exercise (3 implementations) ✅
- **Chapter 11**: 1 exercise (3 implementations) ✅
- **Part 2 - Memory Reclamation**: 2 exercises ✅ (Hazard Pointers, EBR 🆕)
- **Part 2 - Thread Pool**: 1 exercise ✅ (🔥 Most Practical Pattern 🆕)
- **Part 2 - Other**: Work Stealing, Priority Queues, RCU, Parallel Algorithms ✅

**Total**: 26 exercise files, covering 100+ algorithms and patterns

### C++ Exercises
- **Chapter 1**: 3 exercises ✅
- **Chapter 2**: 3 exercises ✅ (Peterson, Filter, Bakery 🆕)
- **Chapter 3**: 3 exercises ✅ (Sequential Consistency, Linearizability, Progress Conditions)
- **Chapter 7**: 1 exercise (6 algorithms: TAS, TTAS, Backoff, MCS, CLH 🆕) ✅
- **Chapter 10**: 1 exercise (2 implementations) ✅ (Bounded Queue, Lock-Free Queue)
- **Chapter 11**: 1 exercise (2 implementations) ✅ (Lock-Based Stack, Lock-Free Stack)
- **Part 2 - Memory Reclamation**: 2 exercises ✅ (Hazard Pointers, EBR 🆕)
- **Part 2 - Thread Pool**: 1 exercise ✅ (🔥 Most Practical Pattern 🆕)
- **Part 2 - Other**: Work Stealing, Priority Queues, RCU, Parallel Algorithms ✅

**Total**: 21 exercise files, covering 45+ algorithms

---

### Phase 8 Summary (NEW! 🎉)

**What Was Added**:
1. ✅ **Bakery Lock** (Chapter 2) - FCFS fairness algorithm by Leslie Lamport
2. ✅ **CLH Lock** (Chapter 7) - Foundation of Java's AbstractQueuedSynchronizer!
3. ✅ **Epoch-Based Reclamation** (Part 2) - Alternative to Hazard Pointers
4. ✅ **Thread Pool Patterns** (Part 2) - THE most practical concurrency pattern

**Impact**:
- 🔥 **Thread Pool**: Most widely used pattern in production systems
- 🎓 **CLH Lock**: Understanding Java's lock infrastructure (AQS)
- 🚀 **EBR**: Modern memory reclamation used in Rust's Crossbeam
- 📚 **Bakery**: Classic algorithm introducing logical timestamps

**Exercise Count**:
- Java: 26 exercises (was 22) - **+4 exercises**
- C++: 21 exercises (was 17) - **+4 exercises**
- **Total algorithms**: 100+ (was 93+) - **+7+ algorithms**

---

## Learning Path Recommendation

### Beginner Path (4-6 weeks)
1. Chapter 1: Basics (all exercises)
2. Chapter 2: Mutual Exclusion (Peterson Lock)
3. Chapter 3: Concurrent Objects (Sequential Consistency)
4. Chapter 7: Spin Locks (TAS, TTAS)
5. Chapter 11: Stacks (Lock-free stack)

### Intermediate Path (6-8 weeks)
Follow the chapter order, completing:
- Chapters 1-5 (all exercises)
- Chapter 7 (all spin locks)
- Chapter 9 (Coarse, Fine, Lazy lists)
- Chapter 10 (Bounded queue, Lock-free queue)

### Advanced Path (8-12 weeks)
Complete all exercises, focusing on:
- Performance optimization
- Understanding cache coherence effects
- Implementing variants of algorithms
- Creating your own concurrent data structures

---

## Key Concepts Covered

### Correctness Conditions
- ✅ Sequential Consistency
- ✅ Linearizability
- ✅ Progress Conditions (wait-free, lock-free, obstruction-free)

### Synchronization Techniques
- ✅ Locks (synchronized, mutex)
- ✅ Atomic operations (CAS, TAS)
- ✅ Memory models (volatile, atomic)

### Classical Algorithms
- ✅ Peterson's Lock
- ✅ Filter Lock
- ✅ Bakery Algorithm (planned)

### Modern Algorithms
- ✅ Treiber Stack
- ✅ Michael-Scott Queue
- ✅ MCS Lock
- ✅ Elimination Backoff

### Data Structures
- ✅ Counters (various implementations)
- ✅ Stacks (lock-based, lock-free, elimination)
- ✅ Queues (bounded, unbounded, lock-free)
- ✅ Linked Lists (4 synchronization strategies)

---

## Testing

All exercises include:
- Main methods for direct execution
- Unit tests (JUnit 5 for Java, Google Test for C++)
- Performance comparison frameworks
- Correctness verification

Run tests:
```bash
# Java
cd exercises/java
mvn test

# C++
cd exercises/cpp/build
ctest
```

---

## Solutions

Reference solutions provided in `solutions/` directory:

**Java Solutions:**
- Exercise 01: Hello Threads
- Exercise 02: Race Condition
- Exercise 01: Peterson Lock

**C++ Solutions:**
- Exercise 01: Hello Threads (C++)
- Exercise 01: Peterson Lock (C++)
- Lock-Free Stack (Treiber Stack complete implementation)

More solutions can be found by examining the fully implemented exercises with filled-in TODOs.

---

## Contributing

Want to add more exercises? Consider:
- Bakery Algorithm
- Readers-Writers locks
- Lock-free skip list
- Transactional memory examples
- Parallel algorithms (reduce, scan, etc.)

---

## Next Steps

After completing these exercises, consider:
1. Reading "The Art of Multiprocessor Programming" (full book)
2. Implementing your own concurrent data structure
3. Contributing to open-source concurrent libraries
4. Exploring advanced topics:
   - Software transactional memory
   - RDMA and distributed shared memory
   - GPU concurrency
   - Formal verification of concurrent algorithms

Happy learning! 🚀

---

## ✨ PART 2: Practice (实践篇)

### Chapter 6: Consensus (共识)

**Status**: ✅ Complete (Java)

- **Exercise 01: Consensus and Universality**
  - Two-thread consensus using atomic swap
  - Universal consensus using CAS
  - Universal construction
  - Consensus hierarchy demonstration
  - File: `exercises/java/src/main/java/com/multiprocessor/consensus/Exercise01_Consensus.java`

**Key Concepts**:
- Consensus number hierarchy
- Universality theorem
- Wait-free universal construction

---

### Chapter 8: Monitors and Blocking (监视器)

**Status**: ✅ Complete (Java)

- **Exercise 01: Monitors and Blocking Synchronization**
  - Bounded buffer (producer-consumer)
  - Readers-writers lock
  - Dining philosophers (deadlock avoidance)
  - Barrier synchronization
  - File: `exercises/java/src/main/java/com/multiprocessor/monitors/Exercise01_Monitors.java`

**Key Concepts**:
- Condition variables
- Lock and Condition API
- Classic synchronization problems
- Deadlock avoidance strategies

---

### Chapter 12: Counting, Sorting, and Coordination (计数与排序)

**Status**: ✅ Complete (Java & C++)

- **Exercise 01: Parallel Counting** (Java)
  - Combining counter
  - Cache-line padded counter
  - Striped counter
  - Parallel array sum (Fork/Join)
  - File: `exercises/java/src/main/java/com/multiprocessor/part2/counting/Exercise01_ParallelCounting.java`

- **Exercise 01: Parallel Counting** (C++)
  - Cache-line padded counter (alignas)
  - Striped counter
  - Thread-local combining
  - File: `exercises/cpp/part2/counting/exercise01_parallel_counting.cpp`

**Key Concepts**:
- False sharing prevention
- Cache-line alignment
- Combining techniques
- Dynamic striping (LongAdder pattern)

---

### Chapter 13: Concurrent Hashing (并发哈希表)

**Status**: ✅ Complete (Java)

- **Exercise 01: Concurrent Hash Maps**
  - Striped hash map (lock striping)
  - Lock-free hash map (CAS-based)
  - Cuckoo hash map (two tables)
  - Performance comparison
  - File: `exercises/java/src/main/java/com/multiprocessor/part2/hashing/Exercise01_ConcurrentHashMap.java`

**Key Concepts**:
- Lock striping for fine-grained concurrency
- Open vs closed addressing
- Cuckoo hashing with displacement
- Resize challenges

---

### Chapter 14: Skip Lists and Balanced Search (跳表)

**Status**: ✅ Complete (Java)

- **Exercise 01: Concurrent Skip List**
  - Lock-free skip list implementation
  - Lazy deletion with marking
  - Probabilistic level generation
  - Concurrent add/remove/contains
  - File: `exercises/java/src/main/java/com/multiprocessor/part2/skiplists/Exercise01_ConcurrentSkipList.java`

**Key Concepts**:
- Probabilistic data structures
- Lock-free search structures
- Lazy deletion pattern
- O(log n) expected time complexity

---

### Chapter 18: Transactional Memory (事务内存)

**Status**: ✅ Complete (Java)

- **Exercise 01: Software Transactional Memory**
  - TVar (transactional variables)
  - Transaction with read/write sets
  - Optimistic concurrency control
  - Automatic retry on conflicts
  - Bank transfer example
  - File: `exercises/java/src/main/java/com/multiprocessor/part2/transactional_memory/Exercise01_STM.java`

**Key Concepts**:
- ACID properties (Atomicity, Consistency, Isolation)
- Version-based concurrency control
- Read/write set tracking
- Transaction composition

---

## Part 2: Chapter 19+ Memory Reclamation (内存回收)

**Status**: ✅ Complete (Java & C++) ⭐⭐

### Exercise 01: Hazard Pointers
- **Concept**: Fine-grained memory reclamation for lock-free structures
- **Approach**: Per-pointer protection
- **Skills**: Hazard pointer protocol, protected dereferencing, deferred deletion
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/part2/memory_reclamation/Exercise01_HazardPointers.java`
  - C++: `exercises/cpp/part2/memory_reclamation/exercise01_hazard_pointers.cpp`

### Exercise 02: Epoch-Based Reclamation (EBR) ⭐ NEW (Phase 8)
- **Concept**: Coarse-grained memory reclamation using global epochs
- **Approach**: Epoch-based protection (simpler than hazard pointers)
- **Skills**: Global epoch tracking, per-thread epochs, batch reclamation
- **Real-World**: Used in userspace RCU, Crossbeam (Rust)
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/part2/memory_reclamation/Exercise02_EpochBasedReclamation.java`
  - C++: `exercises/cpp/part2/memory_reclamation/exercise02_epoch_based_reclamation.cpp`

**Key Concepts**:
- The memory reclamation problem (use-after-free)
- **Hazard Pointers**: Fine-grained, per-pointer protection
- **EBR**: Coarse-grained, epoch-based protection, simpler implementation

**Comparison**:
| Feature | Hazard Pointers | Epoch-Based Reclamation |
|---------|----------------|------------------------|
| Granularity | Fine (per-pointer) | Coarse (per-epoch) |
| Complexity | More complex | Simpler |
| Overhead | Higher per-operation | Lower per-operation |
| Memory bound | Bounded | May be unbounded if threads stall |
| Best for | Low-medium contention | High-throughput scenarios |

**Importance**:
- 🔥 **CRITICAL for C++**: Lock-free structures unsafe without memory reclamation
- 📚 **Educational for Java**: Understanding what GC does for you
- 🌉 **Cross-language**: Essential for C++/Java interoperability understanding
- 🚀 **Production**: EBR widely used in high-performance systems

**CPU Requirements**:
- Minimum: 4 cores
- Recommended: 8+ cores (higher contention shows importance)
- Observation: Reclamation overhead visible with 8+ threads

---

## Part 2: Work Stealing and Task Parallelism (工作窃取)

**Status**: ✅ New (Java & C++) ⭐⭐

- **Exercise 01: Work-Stealing Deque (Chase-Lev)**
  - Lock-free work-stealing deque algorithm
  - Owner operations (push/pop from bottom) - LIFO
  - Thief operations (steal from top) - FIFO
  - Dynamic array resizing
  - Asymmetric access pattern optimization
  - Task parallelism foundations
  - Files:
    - Java: `exercises/java/src/main/java/com/multiprocessor/part2/work_stealing/Exercise01_WorkStealingDeque.java`
    - C++: `exercises/cpp/part2/work_stealing/exercise01_work_stealing_deque.cpp`
  - Solutions:
    - Java: `solutions/java/WorkStealingDeque_Solution.java`
    - C++: `solutions/cpp/work_stealing_deque_solution.cpp`

**Key Concepts**:
- Asymmetric deque (owner vs thieves)
- LIFO for owner (cache locality)
- FIFO for thieves (load balancing)
- Lock-free with minimal CAS
- Circular array with power-of-2 sizing

**Applications**:
- ✅ Java ForkJoinPool (uses similar algorithm)
- ✅ .NET Task Parallel Library
- ✅ Intel TBB (Threading Building Blocks)
- ✅ Rust Rayon parallel framework

**Importance**:
- 🔥 **Foundation of modern task parallelism**: Fork/Join, parallel-for
- 🎯 **Automatic load balancing**: Idle workers steal from busy ones
- ⚡ **High performance**: Owner operations are wait-free
- 📚 **Real-world usage**: Production parallel frameworks

**CPU Requirements**:
- Minimum: 4 cores (to show work stealing benefits)
- Recommended: 8-16 cores (uneven workload distribution)
- Optimal: 16+ cores (dramatic load balancing benefits)
- Observation: Load balancing effectiveness increases with core count

---

## Part 2: Thread Pool Patterns ⭐ NEW (Phase 8) (线程池)

**Status**: ✅ New (Java & C++) 🔥🔥🔥

### Exercise 01: Thread Pool Implementation
- **Concept**: Production-grade thread pool patterns
- **Most Practical Pattern**: Thread pools are THE most widely used concurrency pattern
- **Skills**: Worker threads, task queues, graceful shutdown, work stealing
- **Files**:
  - Java: `exercises/java/src/main/java/com/multiprocessor/part2/thread_pool/Exercise01_ThreadPool.java`
  - C++: `exercises/cpp/part2/thread_pool/exercise01_thread_pool.cpp`

**Implementations**:
1. **Fixed Thread Pool**
   - Fixed number of worker threads
   - Shared task queue (BlockingQueue in Java)
   - Worker threads compete for tasks
   - Graceful shutdown protocol

2. **Work-Stealing Thread Pool**
   - Per-worker task deques
   - LIFO for owners (cache locality)
   - FIFO stealing for load balancing
   - Better performance under uneven load

**Key Concepts**:
- Worker thread lifecycle
- Task submission and execution
- Graceful shutdown (finish pending tasks)
- Exception handling in tasks
- Work stealing for load balancing

**Real-World Usage**:
- ✅ **Java**: `ExecutorService`, `ThreadPoolExecutor`, `ForkJoinPool`
- ✅ **C++**: `std::async`, Thread pools in Boost.Asio
- ✅ **Web Servers**: Request handling pools
- ✅ **Databases**: Query execution pools
- ✅ **Background Processing**: Task queues in production systems

**Importance**:
- 🔥🔥🔥 **MOST PRACTICAL PATTERN**: Used in virtually ALL production systems
- 🎯 **Essential Skill**: Every developer should understand thread pools
- 💼 **Interview Favorite**: Commonly asked in technical interviews
- 🏭 **Production Ready**: Direct application to real-world systems

**Best Practices**:
- Pool size = `CPU cores` for CPU-bound tasks
- Pool size > `CPU cores` for I/O-bound tasks
- Always shutdown gracefully
- Handle exceptions in tasks
- Monitor queue size to prevent overflow

**CPU Requirements**:
- Minimum: 4 cores (to see parallel execution)
- Recommended: 8+ cores (to observe work stealing benefits)
- Optimal: 16+ cores (dramatic throughput improvements)

---

## Part 2: Priority Queues (优先队列)

**Status**: ✅ New (Java & C++) ⭐

- **Exercise 01: Concurrent Priority Queues**
  - Lock-based heap priority queue
  - Skiplist-based priority queue (better concurrency)
  - Relaxed priority queue (bounded error, high scalability)
  - Files:
    - Java: `exercises/java/src/main/java/com/multiprocessor/part2/priority_queues/Exercise01_ConcurrentPriorityQueue.java`
    - C++: `exercises/cpp/part2/priority_queues/exercise01_concurrent_priority_queue.cpp`

**Key Concepts**:
- Root contention in heap-based queues
- Lock-based vs. lock-free approaches
- Hand-over-hand locking in skiplists
- Relaxed data structures (bounded error tolerance)
- Segment-based distribution
- Trade-offs: strict ordering vs. scalability

**Implementations**:
1. **Lock-Based Heap**:
   - ✅ Simple single-lock protection
   - ✅ Strict priority ordering
   - ❌ Root is bottleneck
   - Use case: Low contention scenarios

2. **Skiplist-Based**:
   - ✅ Better concurrency (no single hotspot)
   - ✅ Logarithmic operations
   - ⚠️  Some head contention remains
   - Use case: Moderate contention, strict ordering needed

3. **Relaxed Priority Queue**:
   - ✅ Excellent scalability
   - ✅ Distributed contention across segments
   - ✅ Bounded error (one segment width)
   - ⚠️  Approximate ordering only
   - Use case: High contention, approximate ordering acceptable

**Applications**:
- Task schedulers (CPU scheduling)
- Event-driven systems
- Graph algorithms (Dijkstra, A*)
- Real-time systems (deadline scheduling)
- Discrete event simulation

**Importance**:
- 🎯 **Fundamental data structure**: Critical for many algorithms
- ⚖️ **Design trade-offs**: Strict vs. relaxed semantics
- 📈 **Scalability challenges**: Root contention problem
- 🔧 **Practical solutions**: Various strategies for different scenarios

**CPU Requirements**:
- Minimum: 4 cores
- Recommended: 8+ cores (root contention observable)
- Optimal: 16+ cores (scalability differences dramatic)
- Observation: Relaxed queue scales much better with core count

---

## Part 2: Read-Copy-Update (RCU) (读-复制-更新)

**Status**: ✅ New (Java & C++) Phase 6 ⭐

- **Exercise 01: RCU**
  - Simple RCU mechanism implementation
  - RCU-protected linked list
  - Grace period concept
  - Comparison with lock-based approach
  - Files:
    - Java: `exercises/java/src/main/java/com/multiprocessor/part2/rcu/Exercise01_RCU.java`
    - C++: `exercises/cpp/part2/rcu/exercise01_rcu.cpp`

**Key Concepts**:
- Read-side: ZERO overhead (no locks, no atomic ops)
- Write-side: Copy-update-wait pattern
- Grace period: Wait for all readers to finish
- Publish-subscribe model
- Multiple version coexistence

**RCU Principles**:
1. **Readers have no overhead**: Completely wait-free
2. **Writers use copy-update**: Allocate new, update, publish
3. **Grace period ensures safety**: Wait before reclaiming memory
4. **Read-heavy optimization**: 90%+ reads optimal

**Applications**:
- Linux kernel (extensive usage in networking, VFS, scheduler)
- High-performance databases
- Network routing tables
- Configuration management systems

**Importance**:
- 🚀 **Read performance**: Zero overhead for readers
- 🔧 **Linux kernel**: Millions of lines use RCU
- 📊 **Read-heavy workloads**: Optimal for 90%+ reads
- 🌉 **Cross-language**: Understanding systems programming

**CPU Requirements**:
- Minimum: 4 cores
- Recommended: 8+ cores (many readers)
- Optimal: 16+ cores (dramatic read scalability)
- Observation: Read throughput scales linearly

---

## Enhanced Memory Model Exercises (内存模型)

**Status**: ✅ New (C++) Phase 6 ⭐

- **Exercise 03: C++ Memory Ordering** (in 02_mutual_exclusion)
  - Relaxed ordering for counters
  - Acquire-release for message passing
  - Dekker's algorithm with explicit memory_order
  - Sequential consistency vs relaxed comparison
  - File: `exercises/cpp/02_mutual_exclusion/exercise03_memory_ordering.cpp`

**Key Concepts**:
- C++ memory_order levels (relaxed, acquire, release, acq_rel, seq_cst)
- Acquire-release synchronization
- Relaxed atomics (no ordering guarantees)
- Sequential consistency (total global order)
- Platform differences (x86 vs ARM)

**Memory Order Levels**:
1. **relaxed**: No ordering, just atomicity
2. **acquire**: Synchronize with release stores
3. **release**: Synchronize with acquire loads
4. **acq_rel**: Both acquire and release
5. **seq_cst**: Total global order (default, strongest)

**When to Use**:
- Relaxed: Simple counters, no dependencies
- Acquire/Release: Producer-consumer, flags
- Seq_cst: When unsure, or need global order

**Performance Impact**:
- Relaxed: Cheapest (no barriers)
- Acquire/Release: Moderate (partial barriers)
- Seq_cst: Most expensive (full barriers)

**Importance**:
- ⚡ **Performance optimization**: Choose right memory order
- 🔍 **Understanding C++ model**: Fine-grained control
- 🏗️ **Platform awareness**: x86 vs ARM differences
- 🛡️ **Correctness**: Use ThreadSanitizer to catch bugs

**CPU Requirements**:
- Minimum: 2 cores
- Recommended: 4+ cores
- Optimal: ARM/RISC-V (weak memory architecture exposes issues)
- Note: x86 strong memory model hides many bugs

---

## Part 2: Parallel Algorithms (并行算法)

**Status**: ✅ New (Java & C++) Phase 7 ⭐

- **Exercise 01: Parallel Sorting**
  - Parallel Merge Sort using ForkJoinPool (Java) / std::async (C++)
  - Parallel Quick Sort with concurrent partitioning
  - Sequential cutoff optimization (10,000 elements)
  - Comparison with built-in parallel sorts
  - Performance benchmarks with large arrays
  - Files:
    - Java: `exercises/java/src/main/java/com/multiprocessor/part2/parallel_algorithms/Exercise01_ParallelSorting.java`
    - C++: `exercises/cpp/part2/parallel_algorithms/exercise01_parallel_sorting.cpp`

**Key Concepts**:
- Divide-and-conquer parallelism
- Sequential cutoff thresholds
- Work-stealing schedulers (ForkJoinPool)
- Cache locality vs parallelism trade-offs
- Task granularity tuning

**Implementations**:
1. **Parallel Merge Sort**:
   - ✅ Stable sort (preserves order of equal elements)
   - ✅ Predictable divide (always split at midpoint)
   - ⚠️ Extra memory needed (temp array)
   - Use case: When stability is required

2. **Parallel Quick Sort**:
   - ✅ In-place sorting (no extra memory)
   - ✅ Good cache locality
   - ⚠️ Pivot selection affects balance
   - Use case: When memory is constrained

**Applications**:
- Large dataset processing
- Database query optimization
- MapReduce-style computations
- Scientific computing

**Importance**:
- 🎯 **Fundamental parallel pattern**: Divide-and-conquer
- ⚡ **Performance gains**: Near-linear speedup possible
- 🔧 **Production-ready**: Built into Java and C++ standard libraries
- 📚 **Educational**: Understanding task parallelism

**CPU Requirements**:
- Minimum: 4 cores (basic speedup observable)
- Recommended: 8+ cores (significant speedup)
- Optimal: 16+ cores (dramatic performance gains)
- Array size: 10M+ elements for best demonstration

**Built-in Alternatives**:
- **Java**: `Arrays.parallelSort()` (uses similar algorithm)
- **C++**: `std::execution::par` policies (C++17)

---

## 📊 Updated Statistics

### Part 1: Foundations (Chapters 1-11)

**Java**: 13 exercises covering 30+ algorithms
**C++**: 12 exercises covering 23+ algorithms (added memory ordering)

### Part 2: Practice (Chapters 12-19+) ✨ PHASE 5, 6 & 7 COMPLETE

**Java**: 11 exercises covering advanced topics:
- Parallel counting and reduction
- Concurrent hash maps (3 implementations)
- Lock-free skip lists
- Software transactional memory
- Memory reclamation (Hazard Pointers) 🆕 Phase 5
- Work-stealing deque (Chase-Lev) 🆕 Phase 5
- Priority queues (3 implementations) 🆕 Phase 6
- RCU (Read-Copy-Update) 🆕 Phase 6
- Parallel sorting (merge sort, quick sort) 🆕 Phase 7

**C++**: 7 exercises:
- Parallel counting with cache optimization
- Memory reclamation (Hazard Pointers) 🆕 Phase 5
- Work-stealing deque (Chase-Lev) 🆕 Phase 5
- Priority queues (3 implementations) 🆕 Phase 6
- RCU (Read-Copy-Update) 🆕 Phase 6
- Memory ordering (relaxed, acquire/release, seq_cst) 🆕 Phase 6
- Parallel sorting (merge sort, quick sort) 🆕 Phase 7

### Grand Total

- **Java**: 24 exercise files, 55+ algorithms ✨✨
- **C++**: 19 exercise files, 38+ algorithms ✨✨
- **Combined**: 43 exercise files, 93+ algorithms ✨✨

### Solution Files 🆕

- **Java Solutions**: 6 complete reference implementations
  - Hello Threads, Race Condition, Peterson Lock
  - Hazard Pointers, Work-Stealing Deque
  - (Additional solutions in exercise files with filled TODOs)

- **C++ Solutions**: 6 complete reference implementations
  - Hello Threads, Peterson Lock, Lock-Free Stack
  - Hazard Pointers, Work-Stealing Deque
  - (Additional solutions in exercise files with filled TODOs)

---

## 🎯 Part 2 Learning Path

### Advanced Track (After completing Part 1)

1. **Week 12**: Chapter 6 (Consensus)
   - Understand consensus hierarchy
   - Universal constructions

2. **Week 13**: Chapter 8 (Monitors)
   - Condition variables
   - Classic synchronization problems

3. **Week 14**: Chapter 12 (Counting)
   - Scalable counters
   - False sharing prevention

4. **Week 15**: Chapter 13 (Hashing)
   - Concurrent hash map strategies
   - Cuckoo hashing

5. **Week 16**: Chapter 14 (Skip Lists)
   - Probabilistic structures
   - Lock-free implementation

6. **Week 17**: Chapter 18 (STM)
   - Transactional memory concepts
   - Compare with traditional locking

7. **Week 18**: Memory Reclamation & Work Stealing
   - Hazard pointers for safe reclamation
   - Chase-Lev work-stealing deque

8. **Week 19**: Priority Queues & RCU
   - Concurrent priority queue strategies
   - Read-Copy-Update pattern

9. **Week 20**: Parallel Algorithms
   - Parallel merge sort and quick sort
   - Task parallelism patterns

---

## 🌟 New Algorithms in Part 2

### Counting & Reduction
- ✅ Combining Counter (thread-local aggregation)
- ✅ Striped Counter (load distribution)
- ✅ Cache-line Padded Counter (false sharing prevention)
- ✅ Parallel Array Sum (Fork/Join pattern)

### Concurrent Data Structures
- ✅ Striped Hash Map (lock per bucket group)
- ✅ Lock-Free Hash Map (CAS-based operations)
- ✅ Cuckoo Hash Map (two-table displacement)
- ✅ Lock-Free Skip List (probabilistic search)

### Synchronization Patterns
- ✅ Universal Consensus (wait-free construction)
- ✅ Bounded Buffer (producer-consumer)
- ✅ Readers-Writers Lock (multiple readers OR single writer)
- ✅ Dining Philosophers (deadlock avoidance)
- ✅ Barrier (all threads synchronization point)

### Advanced Techniques
- ✅ Software Transactional Memory (optimistic concurrency)
- ✅ Version-based Concurrency Control
- ✅ Lazy Deletion with Marking
- ✅ Hazard Pointers (safe memory reclamation) 🆕
- ✅ Work-Stealing Deque (Chase-Lev algorithm) 🆕

### Task Parallelism
- ✅ Work-Stealing Deque (owner LIFO, thief FIFO) 🆕
- ✅ Dynamic Load Balancing
- ✅ Fork/Join pattern foundations

### Parallel Algorithms
- ✅ Parallel Merge Sort (divide-and-conquer) 🆕 Phase 7
- ✅ Parallel Quick Sort (concurrent partitioning) 🆕 Phase 7
- ✅ Sequential cutoff optimization
- ✅ Work-stealing task scheduler integration

---

## 💡 Key Learnings from Part 2

### Performance Optimization
1. **Cache-Line Awareness**
   - Use `alignas(64)` in C++ for padding
   - Prevent false sharing between threads
   - Demonstrated in counting exercises

2. **Contention Reduction**
   - Striping: Distribute load across multiple locations
   - Combining: Batch updates to reduce synchronization
   - Lock-free: Eliminate lock contention entirely

3. **Scalability Patterns**
   - Dynamic striping (like Java's LongAdder)
   - Probabilistic algorithms (skip lists)
   - Optimistic concurrency (STM)

### Advanced Concurrency
1. **Consensus and Universality**
   - Understanding primitive power (consensus numbers)
   - Building wait-free objects from consensus
   - CAS is universal (consensus number ∞)

2. **Transactional Memory**
   - Composable atomic operations
   - Automatic conflict detection and retry
   - Cleaner code than explicit locking

3. **Lock-Free Data Structures**
   - Skip lists with lazy deletion
   - Hash maps with CAS
   - Marking nodes for logical deletion

---

## 🚀 What's Next?

### Completed Topics ✅

- ✅ **Phase 5**: Memory Reclamation, Work-Stealing Deques
- ✅ **Phase 6**: Priority Queues, RCU, Enhanced Memory Model
- ✅ **Phase 7**: Parallel Algorithms (sorting)

### Remaining Topics from the Book

1. **Chapter 16**: Futures and Work Distribution (planned)
2. **Chapter 17**: Barriers (partial - basic barrier implemented)
3. **Chapters 19-20**: Additional advanced topics

### Suggested Extensions

1. **More C++ Part 2 Exercises**
   - STM in C++
   - Skip lists in C++
   - Concurrent hash maps in C++

2. **Additional Topics**
   - Epoch-based reclamation (alternative to hazard pointers)
   - Flat combining
   - Hardware Transactional Memory (HTM)
   - Additional parallel algorithms

3. **Real-World Applications**
   - Thread pool implementations
   - Concurrent memory allocators
   - Lock-free data structure library

---

## 📚 Updated Solutions

**Java Solutions** (3):
- Exercise 01: Hello Threads
- Exercise 02: Race Condition
- Exercise 01: Peterson Lock

**C++ Solutions** (3):
- Exercise 01: Hello Threads
- Exercise 01: Peterson Lock
- Lock-Free Stack (Treiber)

**Part 2**: Most exercises include complete implementations with TODOs marked for learning.

---

## 📖 New Documentation Resources 🆕

To help you better understand hardware requirements and second edition topics:

### CPU Requirements Analysis
**File**: `docs/CPU_REQUIREMENTS.md`

Comprehensive analysis of hardware requirements for each exercise:
- Minimum, recommended, and optimal core counts
- Hardware-sensitive exercises identification
- Special requirements (cache size, memory ordering, NUMA)
- Cloud testing options (AWS, Azure, GCP)
- Performance testing recommendations

**Most Hardware-Sensitive Exercises**:
1. Chapter 7: Spin Locks (16+ cores essential)
2. Chapter 11: Elimination Backoff (16+ cores highly recommended)
3. Chapter 12: Parallel Counting (16+ cores for dramatic effects)

**Key Insight**:
- 2-4 cores: ~60% educational value (correctness focus)
- 8 cores: ~85% educational value (basic scalability)
- 16+ cores: ~95% educational value (full scalability spectrum)

### Second Edition Topics Analysis
**File**: `docs/SECOND_EDITION_TOPICS.md`

Analysis of what's new in the second edition and implementation priorities:

**Phase 5: High Priority** ✅ COMPLETED:
- ✅ **Memory Reclamation** (Hazard Pointers) - IMPLEMENTED with solutions!
- ✅ **Work Stealing Deques** (Chase-Lev) - IMPLEMENTED with solutions!

**Phase 6: Medium Priority** ✅ COMPLETED:
- ✅ **Priority Queues** - IMPLEMENTED! (3 implementations: lock-based, skiplist, relaxed)
- ✅ **Read-Copy-Update (RCU)** - IMPLEMENTED! (Java & C++)
- ✅ **Enhanced Memory Model Exercises** - IMPLEMENTED! (C++ memory_order)

**Lower Priority (Phase 7)**:
- ⏳ Hardware Transactional Memory (hardware-dependent)
- ⏳ Parallel Sorting

**Topics Already Covered**: ✅
- STM, Concurrent Data Structures, Spin Locks, Consensus, Monitors

### Additional Documentation
- **Learning Path**: `docs/learning_path.md` - 17-week structured progression
- **Concepts Guide**: `docs/concepts.md` - Deep dive into core concepts
- **Getting Started**: `docs/getting_started.md` - Installation and setup

---

## 🎯 Recommended Study Approach

### Based on Your Hardware

**If you have 4 cores or fewer:**
- Focus on Chapters 1-6, 8 (correctness and fundamentals)
- Skip performance comparison sections
- Use cloud instances for high-core experiments

**If you have 8 cores:**
- All chapters have value, but performance differences subtle
- Can observe basic contention and scalability
- Good for most learning objectives

**If you have 16+ cores:**
- ALL exercises reach full educational value
- Performance differences are dramatic
- Justifies complexity of advanced algorithms
- Highly recommended for serious study

### Based on Your Language

**Java Developers:**
- All 20 Java exercises
- Appreciate what garbage collection does for you
- Focus on algorithm understanding over manual memory management

**C++ Developers:**
- All 13 C++ exercises
- Memory reclamation exercises are CRITICAL
- Focus on safe production-ready lock-free code

**Both Languages:**
- Best learning experience
- Understand memory model differences
- Cross-language concurrent programming skills

---

Happy learning! You now have access to comprehensive exercises covering both foundational and advanced multiprocessor programming topics, with detailed hardware requirements and second edition coverage! 🎉

