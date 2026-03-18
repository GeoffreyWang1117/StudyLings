package com.multiprocessor.spin_locks;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Exercise: Spin Locks
 *
 * CONCEPT: Different implementations of spin locks and their trade-offs
 *
 * Spin lock types:
 * - TAS (Test-and-Set): Simple but causes bus traffic
 * - TTAS (Test-and-Test-and-Set): Better - spins locally
 * - Backoff: TTAS with exponential backoff
 * - Array-based: Fair queuing using array
 * - MCS: Queue-based, truly scalable
 * - CLH: Queue-based, cache-friendly
 *
 * LEARNING OBJECTIVES:
 * - Implement various spin lock algorithms
 * - Understand cache coherence implications
 * - Compare performance characteristics
 */
public class Exercise01_SpinLocks {

    /**
     * TODO: Implement TAS Lock (Test-and-Set)
     *
     * Simple atomic test-and-set lock.
     * Problem: Causes cache coherence traffic on every spin
     */
    public static class TASLock {
        // TODO: Add AtomicBoolean state

        public TASLock() {
            // TODO: Initialize to false (unlocked)
        }

        /**
         * TODO: Implement lock using test-and-set
         *
         * Keep trying getAndSet(true) until it returns false
         */
        public void lock() {
            // TODO: Implement
            // HINT: while (state.getAndSet(true)) { }
        }

        /**
         * TODO: Implement unlock
         */
        public void unlock() {
            // TODO: Set state to false
        }
    }

    /**
     * TODO: Implement TTAS Lock (Test-and-Test-and-Set)
     *
     * Improvement over TAS: Test locally before test-and-set
     * Reduces bus traffic significantly
     */
    public static class TTASLock {
        // TODO: Add AtomicBoolean state

        public TTASLock() {
            // TODO: Initialize
        }

        /**
         * TODO: Implement TTAS lock
         *
         * while (true) {
         *   while (state.get()) { } // Spin locally (read-only)
         *   if (!state.getAndSet(true)) return; // Try to acquire
         * }
         */
        public void lock() {
            // TODO: Implement TTAS pattern
        }

        public void unlock() {
            // TODO: Implement
        }
    }

    /**
     * TODO: Implement Exponential Backoff Lock
     *
     * TTAS + exponential backoff on contention
     * Reduces contention by delaying retries
     */
    public static class BackoffLock {
        private AtomicBoolean state = new AtomicBoolean(false);
        private static final int MIN_DELAY = 1;
        private static final int MAX_DELAY = 1000;

        /**
         * TODO: Implement lock with exponential backoff
         */
        public void lock() {
            int delay = MIN_DELAY;
            while (true) {
                // TODO: Spin locally
                while (state.get()) {
                    // Optional: add small delay even while spinning
                }

                // TODO: Try to acquire
                if (!state.getAndSet(true)) {
                    return; // Success!
                }

                // TODO: Exponential backoff on failure
                // HINT: Thread.sleep(delay), then delay = min(delay * 2, MAX_DELAY)
                try {
                    Thread.sleep(delay);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                delay = Math.min(delay * 2, MAX_DELAY);
            }
        }

        public void unlock() {
            state.set(false);
        }
    }

    /**
     * TODO: Implement Anderson Array-Based Lock
     *
     * Uses array of flags for fairness
     * Each thread spins on its own flag (cache-friendly)
     */
    public static class AndersonLock {
        private final AtomicBoolean[] flags;
        private final AtomicInteger tail;
        private final ThreadLocal<Integer> mySlot;
        private final int numThreads;

        public AndersonLock(int numThreads) {
            this.numThreads = numThreads;
            this.flags = new AtomicBoolean[numThreads];
            // TODO: Initialize flags array
            // HINT: flags[0] = true, others = false
            for (int i = 0; i < numThreads; i++) {
                flags[i] = new AtomicBoolean(i == 0);
            }
            this.tail = new AtomicInteger(0);
            this.mySlot = ThreadLocal.withInitial(() -> 0);
        }

        /**
         * TODO: Implement lock
         *
         * 1. Get slot = getAndIncrement(tail) % numThreads
         * 2. Spin on flags[slot] until true
         * 3. Set flags[slot] = false
         */
        public void lock() {
            // TODO: Implement
            int slot = tail.getAndIncrement() % numThreads;
            mySlot.set(slot);
            // Spin until my flag is true
            while (!flags[slot].get()) {
                // Spin
            }
            flags[slot].set(false);
        }

        /**
         * TODO: Implement unlock
         *
         * Set flags[(mySlot + 1) % numThreads] = true
         */
        public void unlock() {
            // TODO: Implement
            int slot = mySlot.get();
            flags[(slot + 1) % numThreads].set(true);
        }
    }

    /**
     * TODO: Implement MCS Lock (Mellor-Crummey Scott)
     *
     * Queue-based lock with excellent scalability
     * Each thread spins on its own node (no cache coherence traffic)
     */
    public static class MCSLock {
        static class QNode {
            volatile boolean locked = false;
            volatile QNode next = null;
        }

        private final AtomicReference<QNode> tail;
        private final ThreadLocal<QNode> myNode;

        public MCSLock() {
            tail = new AtomicReference<>(null);
            myNode = ThreadLocal.withInitial(QNode::new);
        }

        /**
         * TODO: Implement MCS lock
         *
         * 1. Get my node, set locked = true
         * 2. CAS my node into tail
         * 3. If tail was not null:
         *    - Set pred.next = myNode
         *    - Spin on myNode.locked
         */
        public void lock() {
            // TODO: Implement MCS lock protocol
            QNode node = myNode.get();
            node.locked = true;
            QNode pred = tail.getAndSet(node);

            if (pred != null) {
                pred.next = node;
                // Spin on my own node
                while (node.locked) {
                    // Spin
                }
            }
        }

        /**
         * TODO: Implement MCS unlock
         *
         * If next == null:
         *   Try to CAS tail to null
         *   If fail, wait for next to be set
         * Set next.locked = false
         */
        public void unlock() {
            // TODO: Implement MCS unlock protocol
            QNode node = myNode.get();
            if (node.next == null) {
                if (tail.compareAndSet(node, null)) {
                    return;
                }
                // Wait for next to be set
                while (node.next == null) {
                    // Spin
                }
            }
            node.next.locked = false;
            node.next = null;
        }
    }

    /**
     * CLH Lock (Craig, Landin, and Hagersten)
     *
     * CRITICAL: Foundation of Java's AbstractQueuedSynchronizer (AQS)!
     *
     * Key differences from MCS:
     * - MCS: Explicit queue with successor pointers (spins on own node)
     * - CLH: Implicit queue with predecessor pointers (spins on predecessor's node)
     *
     * Benefits:
     * - Better cache behavior on cache-coherent systems
     * - Used in Java's ReentrantLock, Semaphore, CountDownLatch
     * - Simpler to implement than MCS
     *
     * How it works:
     * 1. Each thread has a QNode (initially locked=false)
     * 2. To acquire: swap my node into tail, spin on predecessor's locked field
     * 3. To release: set my node's locked=false
     * 4. Predecessor becomes garbage when next thread releases
     *
     * Real-world usage:
     * - Java j.u.c.locks.AbstractQueuedSynchronizer
     * - ReentrantLock, Semaphore, CountDownLatch all use AQS
     */
    public static class CLHLock {
        /**
         * Queue node for CLH lock
         * Each thread spins on its predecessor's locked field
         */
        static class QNode {
            volatile boolean locked = false;
        }

        private final AtomicReference<QNode> tail;
        private final ThreadLocal<QNode> myNode;
        private final ThreadLocal<QNode> myPred;

        public CLHLock() {
            tail = new AtomicReference<>(new QNode());
            myNode = ThreadLocal.withInitial(QNode::new);
            myPred = new ThreadLocal<>();
        }

        /**
         * CLH lock acquisition
         *
         * Algorithm:
         * 1. Get my node, set locked = true
         * 2. Swap my node into tail, get predecessor
         * 3. Spin on predecessor's locked field
         * 4. When pred.locked becomes false, I have the lock
         */
        public void lock() {
            QNode node = myNode.get();
            node.locked = true;  // Indicate I want the lock

            // Swap my node into tail, get predecessor
            QNode pred = tail.getAndSet(node);
            myPred.set(pred);  // Remember predecessor for unlock

            // Spin on predecessor's locked field
            // This is cache-friendly: each thread spins on different location
            while (pred.locked) {
                // Spin locally on predecessor's cached locked field
            }

            // When we exit the loop, we have acquired the lock
        }

        /**
         * CLH lock release
         *
         * Algorithm:
         * 1. Set my node's locked = false (releases successor)
         * 2. Reuse predecessor's node for next acquisition
         */
        public void unlock() {
            QNode node = myNode.get();
            node.locked = false;  // Release successor

            // Reuse predecessor's node (it's now garbage for the predecessor)
            // This is memory-efficient: nodes are recycled
            myNode.set(myPred.get());
        }

        /**
         * Compare with MCS Lock:
         *
         * MCS:
         * - Spins on own node (node.locked)
         * - Explicit queue with successor pointers
         * - Better for NUMA systems
         * - More complex unlock
         *
         * CLH:
         * - Spins on predecessor node (pred.locked)
         * - Implicit queue (only tail pointer)
         * - Better for cache-coherent systems
         * - Simpler implementation
         * - Used in Java AQS!
         *
         * Performance:
         * - Similar scalability
         * - CLH better on most modern systems (cache-coherent)
         * - MCS better on NUMA systems
         */
    }

    /**
     * Performance comparison framework
     */
    static class PerformanceTest {
        interface Lock {
            void lock();
            void unlock();
        }

        static long testLock(String name, Lock lock, int numThreads, int iterations)
                throws InterruptedException {
            Counter counter = new Counter();
            Thread[] threads = new Thread[numThreads];

            long startTime = System.nanoTime();

            for (int i = 0; i < numThreads; i++) {
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < iterations; j++) {
                        lock.lock();
                        try {
                            counter.increment();
                        } finally {
                            lock.unlock();
                        }
                    }
                });
                threads[i].start();
            }

            for (Thread t : threads) {
                t.join();
            }

            long endTime = System.nanoTime();
            long duration = (endTime - startTime) / 1_000_000; // ms

            System.out.printf("%20s: %6dms (count=%d)%n", name, duration, counter.get());
            return duration;
        }
    }

    static class Counter {
        private int count = 0;

        public void increment() {
            count++;
        }

        public int get() {
            return count;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Spin Locks Test ===\n");

        testCorrectness();
        System.out.println("\n=== Performance Comparison ===");
        comparePerformance();
    }

    private static void testCorrectness() throws InterruptedException {
        System.out.println("Testing correctness of locks:");

        int numThreads = 10;
        int incrementsPerThread = 1000;
        int expected = numThreads * incrementsPerThread;

        // Test each lock type
        testOneLock("TAS", new TASLock(), numThreads, incrementsPerThread, expected);
        testOneLock("TTAS", new TTASLock(), numThreads, incrementsPerThread, expected);
        testOneLock("Backoff", new BackoffLock(), numThreads, incrementsPerThread, expected);
        testOneLock("Anderson", new AndersonLock(numThreads), numThreads, incrementsPerThread, expected);
        testOneLock("MCS", new MCSLock(), numThreads, incrementsPerThread, expected);
        testOneLock("CLH", new CLHLock(), numThreads, incrementsPerThread, expected);
    }

    private static void testOneLock(String name, Object lockObj, int numThreads,
                                     int incrementsPerThread, int expected)
            throws InterruptedException {
        Counter counter = new Counter();
        Thread[] threads = new Thread[numThreads];

        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    if (lockObj instanceof TASLock) {
                        TASLock lock = (TASLock) lockObj;
                        lock.lock();
                        try { counter.increment(); } finally { lock.unlock(); }
                    } else if (lockObj instanceof TTASLock) {
                        TTASLock lock = (TTASLock) lockObj;
                        lock.lock();
                        try { counter.increment(); } finally { lock.unlock(); }
                    } else if (lockObj instanceof BackoffLock) {
                        BackoffLock lock = (BackoffLock) lockObj;
                        lock.lock();
                        try { counter.increment(); } finally { lock.unlock(); }
                    } else if (lockObj instanceof AndersonLock) {
                        AndersonLock lock = (AndersonLock) lockObj;
                        lock.lock();
                        try { counter.increment(); } finally { lock.unlock(); }
                    } else if (lockObj instanceof MCSLock) {
                        MCSLock lock = (MCSLock) lockObj;
                        lock.lock();
                        try { counter.increment(); } finally { lock.unlock(); }
                    } else if (lockObj instanceof CLHLock) {
                        CLHLock lock = (CLHLock) lockObj;
                        lock.lock();
                        try { counter.increment(); } finally { lock.unlock(); }
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        System.out.printf("%10s: Expected=%d, Actual=%d %s%n",
                         name, expected, counter.get(),
                         counter.get() == expected ? "✅" : "❌");
    }

    private static void comparePerformance() throws InterruptedException {
        int numThreads = 8;
        int iterations = 10000;

        System.out.println("Threads: " + numThreads + ", Iterations per thread: " + iterations);
        System.out.println();

        // Note: BackoffLock might be slower due to sleeps
        PerformanceTest.testLock("TAS Lock", new PerformanceTest.Lock() {
            TASLock lock = new TASLock();
            public void lock() { lock.lock(); }
            public void unlock() { lock.unlock(); }
        }, numThreads, iterations);

        PerformanceTest.testLock("TTAS Lock", new PerformanceTest.Lock() {
            TTASLock lock = new TTASLock();
            public void lock() { lock.lock(); }
            public void unlock() { lock.unlock(); }
        }, numThreads, iterations);

        PerformanceTest.testLock("MCS Lock", new PerformanceTest.Lock() {
            MCSLock lock = new MCSLock();
            public void lock() { lock.lock(); }
            public void unlock() { lock.unlock(); }
        }, numThreads, iterations);

        PerformanceTest.testLock("CLH Lock", new PerformanceTest.Lock() {
            CLHLock lock = new CLHLock();
            public void lock() { lock.lock(); }
            public void unlock() { lock.unlock(); }
        }, numThreads, iterations);

        System.out.println("\n💡 CLH and MCS locks both perform well under high contention");
        System.out.println("💡 CLH is the foundation of Java's AQS (AbstractQueuedSynchronizer)");
        System.out.println("💡 TTAS is simpler but causes more cache coherence traffic");
    }
}
