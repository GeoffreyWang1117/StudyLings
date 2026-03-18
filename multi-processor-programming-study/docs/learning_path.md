# Learning Path: Multi-Processor Programming

This document outlines the recommended learning path through the exercises, organized by chapters from "The Art of Multiprocessor Programming".

## How to Use This Guide

1. **Start with the Basics**: Even if you have some concurrent programming experience, start with Module 01
2. **Choose Your Language**: Pick Java or C++ (or do both!)
3. **Read Before Coding**: Understand the concepts before jumping into implementation
4. **Test Frequently**: Run tests after each exercise
5. **Experiment**: Try breaking things to understand why they work

## Detailed Learning Path

### 🌱 Module 01: Basics (Week 1)

**Goal**: Understand fundamental concurrent programming concepts

#### Exercise 01: Hello Threads
- **Concepts**: Thread creation, lifecycle, joining
- **Time**: 30 minutes
- **Prerequisites**: None
- **Key Takeaways**: How threads work at a basic level

#### Exercise 02: Race Condition
- **Concepts**: Shared memory, race conditions, non-determinism
- **Time**: 45 minutes
- **Prerequisites**: Exercise 01
- **Key Takeaways**: Why synchronization is necessary

#### Exercise 03: Synchronization
- **Concepts**: Mutual exclusion, synchronized/mutex, atomicity
- **Time**: 1 hour
- **Prerequisites**: Exercise 02
- **Key Takeaways**: Basic synchronization primitives

**Checkpoint**: Can you explain what a race condition is and how to prevent it?

---

### 🔒 Module 02: Mutual Exclusion (Week 2)

**Goal**: Master classical mutual exclusion algorithms

#### Exercise 01: Peterson Lock
- **Concepts**: Two-thread mutual exclusion, memory visibility
- **Time**: 2 hours
- **Prerequisites**: Module 01 complete
- **Key Takeaways**:
  - How mutual exclusion can be achieved without hardware support
  - Memory visibility issues
  - Safety vs liveness properties

#### Exercise 02: Filter Lock
- **Concepts**: n-thread mutual exclusion, levels of exclusion
- **Time**: 2 hours
- **Prerequisites**: Peterson Lock
- **Key Takeaways**:
  - Generalization of Peterson's algorithm
  - Trade-offs between correctness and performance

#### Exercise 03: Bakery Algorithm (Coming Soon)
- **Concepts**: FIFO fairness, lamport's bakery
- **Time**: 2 hours
- **Prerequisites**: Filter Lock

**Checkpoint**: Can you implement a correct mutual exclusion algorithm from scratch?

---

### 🎯 Module 03: Concurrent Objects (Week 3)

**Goal**: Understand correctness conditions for concurrent objects

#### Topics Covered:
- Quiescent consistency
- Sequential consistency
- Linearizability
- Progress conditions (wait-free, lock-free, obstruction-free)

**Status**: Coming soon

---

### 🏗️ Module 04: Foundations (Week 4)

**Goal**: Learn about atomic registers and snapshots

#### Topics Covered:
- Atomic register constructions
- MRSW to MRMW register
- Atomic snapshots
- Wait-free constructions

**Status**: Coming soon

---

### ⚙️ Module 05: Synchronization Primitives (Week 5)

**Goal**: Master hardware synchronization primitives

#### Topics Covered:
- Test-and-Set (TAS)
- Compare-and-Swap (CAS)
- Load-Linked/Store-Conditional (LL/SC)
- Fetch-and-Add (FAA)

**Status**: Coming soon

---

### 🤝 Module 06: Consensus (Week 6)

**Goal**: Understand consensus and its importance

#### Topics Covered:
- Consensus protocols
- Consensus hierarchy
- Universality of consensus
- Impossibility results

**Status**: Coming soon

---

### 🔄 Module 07: Spin Locks (Week 7)

**Goal**: Implement efficient spin locks

#### Topics Covered:
- TAS and TTAS locks
- Exponential backoff
- Array-based queue locks
- MCS and CLH locks

**Status**: Coming soon

---

### 🚦 Module 08: Monitors and Blocking (Week 8)

**Goal**: Learn blocking synchronization

#### Topics Covered:
- Condition variables
- Producer-consumer problem
- Readers-writers locks
- Semaphores

**Status**: Coming soon

---

### 🔗 Module 09: Linked Lists (Week 9)

**Goal**: Implement concurrent linked lists

#### Topics Covered:
- Coarse-grained synchronization
- Fine-grained synchronization
- Optimistic synchronization
- Lazy synchronization
- Lock-free lists

**Status**: Coming soon

---

### 📦 Module 10: Concurrent Queues (Week 10)

**Goal**: Build high-performance concurrent queues

#### Topics Covered:
- Bounded queues
- Unbounded queues
- ABA problem
- Lock-free queues (Michael-Scott)

**Status**: Coming soon

---

### 📚 Module 11: Concurrent Stacks (Week 11)

**Goal**: Implement concurrent stacks

#### Topics Covered:
- Lock-based stacks
- Lock-free stacks
- Elimination backoff stacks
- Performance comparison

**Status**: Coming soon

---

## Learning Tips

### 1. Understand Before Implementing
Read the concept explanation at the top of each exercise file before starting to code.

### 2. Start Simple
Don't try to optimize prematurely. Get correctness first, then worry about performance.

### 3. Use Tests
Tests are your friends. They tell you immediately if your implementation is correct.

### 4. Read Error Messages
Test failures often contain hints about what's wrong.

### 5. Compare Languages
If stuck in one language, try looking at the same exercise in the other language for inspiration.

### 6. Experiment
Try intentionally breaking things:
- Remove a synchronization primitive
- Change memory ordering
- Add extra threads

This helps you understand WHY the code works.

### 7. Time Yourself
These exercises include time estimates. If you're taking much longer, you might be overthinking it.

### 8. Ask Questions
If something doesn't make sense, it's probably an interesting edge case worth exploring.

## Common Pitfalls

### Java-specific:
1. **Forgetting `volatile`**: Non-volatile variables may not be visible across threads
2. **Using `synchronized` everywhere**: Sometimes `AtomicInteger` is better
3. **Catching `InterruptedException` incorrectly**: Always restore the interrupt status

### C++-specific:
1. **Wrong memory ordering**: Default to `seq_cst`, then optimize
2. **Forgetting to join threads**: Leads to crashes
3. **Data races on non-atomic variables**: Undefined behavior!

## Estimated Timeline

- **Complete Beginner**: 12-16 weeks (2-3 hours/week)
- **Some Experience**: 8-10 weeks (3-4 hours/week)
- **Advanced**: 6-8 weeks (4-5 hours/week)

## Next Steps After Completion

1. Read the full "The Art of Multiprocessor Programming" book
2. Implement your own concurrent data structures
3. Contribute to open-source concurrent libraries
4. Study advanced topics:
   - Lock-free data structures
   - Wait-free algorithms
   - Transactional memory
   - Memory models

## Resources

### Books:
- "The Art of Multiprocessor Programming" by Herlihy & Shavit (main reference)
- "Java Concurrency in Practice" by Goetz et al.
- "C++ Concurrency in Action" by Williams

### Online:
- [Preshing on Programming](https://preshing.com/) - Excellent articles on concurrency
- [Java Memory Model](https://docs.oracle.com/javase/specs/jls/se17/html/jls-17.html)
- [C++ Memory Model](https://en.cppreference.com/w/cpp/atomic/memory_order)

### Papers:
- Leslie Lamport's papers on mutual exclusion
- Maurice Herlihy's papers on wait-free synchronization

Good luck with your learning journey! 🚀
