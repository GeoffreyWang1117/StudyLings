# Key Concepts in Multi-Processor Programming

This document provides detailed explanations of core concepts from "The Art of Multiprocessor Programming".

## Table of Contents

1. [Mutual Exclusion](#mutual-exclusion)
2. [Race Conditions](#race-conditions)
3. [Memory Models](#memory-models)
4. [Linearizability](#linearizability)
5. [Progress Conditions](#progress-conditions)
6. [Consensus](#consensus)

---

## Mutual Exclusion

**Definition**: At most one thread can be in the critical section at any time.

### Why It Matters
Without mutual exclusion, concurrent access to shared data can lead to:
- Lost updates
- Inconsistent state
- Corrupted data structures

### Classical Algorithms

#### Peterson's Algorithm (2 threads)
```
lock(i):
    flag[i] = true
    victim = i
    while flag[j] && victim == i:
        wait
```

**Key Insight**: Each thread politely defers to the other by being the "victim".

#### Filter Lock (n threads)
Generalizes Peterson's to n threads using n-1 levels of exclusion.

**Key Insight**: At each level, at least one thread is blocked, ensuring only one reaches the critical section.

### Properties

1. **Mutual Exclusion** (Safety): Critical section has at most one thread
2. **Deadlock-Freedom** (Liveness): If threads want in, someone gets in
3. **Starvation-Freedom** (Fairness): Every thread eventually gets in

---

## Race Conditions

**Definition**: When program behavior depends on the relative timing of thread execution.

### Example
```java
// Thread 1           // Thread 2
count++;              count++;

// Expected: count increases by 2
// Actual: might increase by 1 (lost update)
```

### Why They Occur
`count++` is really three operations:
1. READ: load count
2. MODIFY: add 1
3. WRITE: store result

Threads can interleave these operations.

### How to Prevent
- Use mutual exclusion (locks)
- Use atomic operations
- Eliminate shared mutable state

---

## Memory Models

**Definition**: Rules about how memory operations from different threads are ordered.

### Sequential Consistency
"Execution appears as if all operations executed in some sequential order, and operations of each thread appear in this sequence in program order."

**Intuition**: All threads see memory operations in the same order.

### Java Memory Model
- Uses **happens-before** relationship
- **volatile** ensures visibility and ordering
- **synchronized** provides mutual exclusion + memory visibility

### C++ Memory Model
More fine-grained control with memory orderings:
- `memory_order_seq_cst`: Sequential consistency (default, safest)
- `memory_order_acquire`: Synchronizes with release
- `memory_order_release`: Synchronizes with acquire
- `memory_order_relaxed`: No synchronization, just atomicity

---

## Linearizability

**Definition**: Each operation appears to take effect instantaneously at some point between its invocation and response.

### Why It Matters
Linearizability is the gold standard for concurrent objects. It means:
- Operations have a total order
- Order respects real-time
- Each operation is atomic

### Example
```
Thread A: enqueue(x) -------|
Thread B:           |-------- dequeue() -> x
```
The dequeue can return x if there's a linearization point where enqueue(x) completed before dequeue() started.

---

## Progress Conditions

Different guarantees about threads making progress:

### Wait-Free
**Every** thread completes its operation in a finite number of steps.
- Strongest guarantee
- Hard to achieve
- Example: Atomic register operations

### Lock-Free
**Some** thread makes progress in a finite number of steps.
- Weaker than wait-free
- System-wide progress guaranteed
- Example: Lock-free queue

### Obstruction-Free
A thread makes progress if it runs **in isolation** (no contention).
- Weakest non-blocking guarantee
- Progress only guaranteed without interference

### Blocking
Threads can wait indefinitely (but with scheduling guarantees, will eventually proceed).
- Uses locks
- Deadlock possible (must be prevented)
- Example: Java synchronized

---

## Consensus

**Definition**: Agreement protocol where threads propose values and must agree on one.

### The Consensus Problem
- Each thread proposes a value
- All threads must decide on the same value
- The decided value must be one of the proposed values

### Consensus Number
The maximum number of threads for which a primitive can solve consensus.

**Hierarchy:**
- Atomic registers: 1 (can't solve consensus for 2 threads)
- Test-and-Set, Swap: 2
- Compare-and-Swap, Load-Linked/Store-Conditional: ∞

### Universality
Any object with consensus number n can implement any object for n threads in a wait-free manner.

---

## Atomic Operations

### Compare-and-Swap (CAS)
```java
boolean compareAndSwap(int expected, int new) {
    if (value == expected) {
        value = new;
        return true;
    }
    return false;
}
```

**Use Case**: Lock-free algorithms

### Test-and-Set (TAS)
```java
boolean testAndSet() {
    boolean old = value;
    value = true;
    return old;
}
```

**Use Case**: Simple spin locks

### Fetch-and-Add (FAA)
```java
int fetchAndAdd(int delta) {
    int old = value;
    value += delta;
    return old;
}
```

**Use Case**: Counters, sequence numbers

---

## Performance Considerations

### Contention
When multiple threads try to access the same resource.

**Effects:**
- Increased latency
- Reduced throughput
- Cache coherence traffic

**Solutions:**
- Reduce critical section size
- Use backoff strategies
- Eliminate hot spots
- Use lock-free data structures

### False Sharing
When different threads access different variables that share a cache line.

**Solution:** Padding to separate cache lines

### Amdahl's Law
Maximum speedup limited by sequential portion:
```
Speedup = 1 / (S + (1-S)/N)
```
where S = sequential fraction, N = number of processors

---

## Best Practices

1. **Minimize Shared Mutable State**: Less sharing = fewer problems
2. **Use Higher-Level Abstractions**: Prefer concurrent collections over raw locks
3. **Keep Critical Sections Small**: Less time in lock = better performance
4. **Avoid Nested Locks**: Can cause deadlock
5. **Document Synchronization Strategy**: Make threading assumptions explicit
6. **Test with ThreadSanitizer/Helgrind**: Catch races early
7. **Prefer Immutability**: Immutable objects are automatically thread-safe

---

## Common Patterns

### Producer-Consumer
```java
BlockingQueue<T> queue = new LinkedBlockingQueue<>();

// Producer
queue.put(item);

// Consumer
T item = queue.take();
```

### Reader-Writer Lock
Multiple readers OR single writer.

### Double-Checked Locking
```java
if (instance == null) {  // Check 1 (no lock)
    synchronized(this) {
        if (instance == null) {  // Check 2 (with lock)
            instance = new Object();
        }
    }
}
```
**Warning:** Requires volatile in Java!

---

## Further Reading

- **Book**: "The Art of Multiprocessor Programming" (Herlihy & Shavit)
- **Book**: "Java Concurrency in Practice" (Goetz et al.)
- **Paper**: "Linearizability: A Correctness Condition for Concurrent Objects" (Herlihy & Wing)
- **Online**: [Preshing on Programming](https://preshing.com/)
- **Online**: [The JSR-133 Cookbook](http://gee.cs.oswego.edu/dl/jmm/cookbook.html)

---

Remember: Concurrent programming is hard. Start simple, ensure correctness, then optimize. Happy learning! 🚀
