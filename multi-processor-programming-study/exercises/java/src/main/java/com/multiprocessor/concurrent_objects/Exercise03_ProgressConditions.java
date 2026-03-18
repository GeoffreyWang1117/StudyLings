package com.multiprocessor.concurrent_objects;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Exercise: Progress Conditions
 *
 * CONCEPT: Different guarantees about thread progress
 *
 * Progress conditions specify what happens when threads compete:
 *
 * WAIT-FREE: Every thread completes in finite steps (strongest)
 * LOCK-FREE: Some thread always makes progress (system-wide)
 * OBSTRUCTION-FREE: Thread makes progress when run alone
 * BLOCKING: Threads may wait for locks (weakest)
 *
 * LEARNING OBJECTIVES:
 * - Understand different progress conditions
 * - Implement wait-free, lock-free, and blocking algorithms
 * - Compare their properties
 */
public class Exercise03_ProgressConditions {

    /**
     * TODO: Implement a WAIT-FREE counter
     *
     * Every thread completes increment in finite steps, regardless of other threads.
     * Uses atomic operations that complete in bounded time.
     */
    public static class WaitFreeCounter {
        // TODO: Add necessary fields
        // HINT: Use AtomicInteger

        public WaitFreeCounter(int initialValue) {
            // TODO: Initialize
        }

        /**
         * TODO: Implement wait-free increment
         *
         * WAIT-FREE property: This operation completes in O(1) steps
         * regardless of contention.
         *
         * @return value AFTER increment
         */
        public int incrementAndGet() {
            // TODO: Implement using getAndIncrement + 1
            // HINT: AtomicInteger.incrementAndGet() is wait-free
            return 0;
        }

        public int get() {
            // TODO: Implement
            return 0;
        }
    }

    /**
     * TODO: Implement a LOCK-FREE stack
     *
     * At least one thread makes progress, even under contention.
     * Uses CAS loops - some threads may retry, but some will succeed.
     */
    public static class LockFreeStack<T> {
        private static class Node<T> {
            final T value;
            Node<T> next;

            Node(T value) {
                this.value = value;
            }
        }

        // TODO: Add necessary fields
        // HINT: AtomicReference<Node<T>> for top

        public LockFreeStack() {
            // TODO: Initialize
        }

        /**
         * TODO: Implement lock-free push
         *
         * LOCK-FREE property: Even if some threads are delayed, at least
         * one thread makes progress in finite steps.
         *
         * @param value value to push
         */
        public void push(T value) {
            // TODO: Implement using CAS loop
            // Create node
            // Loop:
            //   Read current top
            //   Set node.next = top
            //   Try CAS(top, oldTop, node)
            //   If successful, return
            //   Else retry
        }

        /**
         * TODO: Implement lock-free pop
         *
         * @return popped value, or null if empty
         */
        public T pop() {
            // TODO: Implement using CAS loop
            return null;
        }
    }

    /**
     * TODO: Implement a BLOCKING counter using locks
     *
     * Threads may block waiting for locks.
     * Simpler to implement but may have worse progress guarantees.
     */
    public static class BlockingCounter {
        private int count;
        // TODO: Add lock
        // HINT: Use Object for synchronized, or explicit Lock

        public BlockingCounter(int initialValue) {
            this.count = initialValue;
        }

        /**
         * TODO: Implement blocking increment
         *
         * BLOCKING property: Thread may wait indefinitely for lock
         * (but with fair scheduling, will eventually proceed)
         *
         * @return value AFTER increment
         */
        public synchronized int incrementAndGet() {
            // TODO: Implement with synchronization
            return 0;
        }

        public synchronized int get() {
            return count;
        }
    }

    /**
     * TODO: Implement an OBSTRUCTION-FREE counter
     *
     * A thread makes progress if it runs alone (no contention).
     * Simpler than lock-free, but weaker guarantee.
     */
    public static class ObstructionFreeCounter {
        // TODO: Add necessary fields

        public ObstructionFreeCounter(int initialValue) {
            // TODO: Initialize
        }

        /**
         * TODO: Implement obstruction-free increment
         *
         * OBSTRUCTION-FREE property: If this thread runs alone,
         * it completes in finite steps.
         *
         * Note: In practice, this is similar to lock-free CAS loop,
         * but we don't guarantee system-wide progress under contention.
         *
         * @return value AFTER increment
         */
        public int incrementAndGet() {
            // TODO: Implement using CAS
            // Single CAS attempt (or limited retries)
            return 0;
        }

        public int get() {
            // TODO: Implement
            return 0;
        }
    }

    /**
     * Performance comparison test
     */
    static class PerformanceTest {
        static long testCounter(String name, Runnable incrementOp, int numThreads, int opsPerThread)
                throws InterruptedException {
            Thread[] threads = new Thread[numThreads];

            long startTime = System.nanoTime();

            for (int i = 0; i < numThreads; i++) {
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < opsPerThread; j++) {
                        incrementOp.run();
                    }
                });
                threads[i].start();
            }

            for (Thread t : threads) {
                t.join();
            }

            long endTime = System.nanoTime();
            long duration = (endTime - startTime) / 1_000_000; // ms

            System.out.println(name + ": " + duration + "ms");
            return duration;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Progress Conditions Test ===\n");

        testCorrectness();
        System.out.println("\n=== Performance Comparison ===");
        comparePerformance();
    }

    private static void testCorrectness() throws InterruptedException {
        int numThreads = 10;
        int opsPerThread = 1000;
        int expected = numThreads * opsPerThread;

        // Test Wait-Free
        System.out.println("Testing Wait-Free Counter:");
        WaitFreeCounter wfCounter = new WaitFreeCounter(0);
        Thread[] wfThreads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            wfThreads[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    wfCounter.incrementAndGet();
                }
            });
            wfThreads[i].start();
        }
        for (Thread t : wfThreads) t.join();
        System.out.println("Expected: " + expected + ", Actual: " + wfCounter.get());
        System.out.println(wfCounter.get() == expected ? "✅ PASS" : "❌ FAIL");

        // Test Lock-Free
        System.out.println("\nTesting Lock-Free Stack:");
        LockFreeStack<Integer> lfStack = new LockFreeStack<>();
        Thread[] lfPushers = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            lfPushers[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    lfStack.push(id * opsPerThread + j);
                }
            });
            lfPushers[i].start();
        }
        for (Thread t : lfPushers) t.join();

        int popCount = 0;
        while (lfStack.pop() != null) popCount++;
        System.out.println("Expected: " + expected + ", Actual: " + popCount);
        System.out.println(popCount == expected ? "✅ PASS" : "❌ FAIL");

        // Test Blocking
        System.out.println("\nTesting Blocking Counter:");
        BlockingCounter bCounter = new BlockingCounter(0);
        Thread[] bThreads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            bThreads[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    bCounter.incrementAndGet();
                }
            });
            bThreads[i].start();
        }
        for (Thread t : bThreads) t.join();
        System.out.println("Expected: " + expected + ", Actual: " + bCounter.get());
        System.out.println(bCounter.get() == expected ? "✅ PASS" : "❌ FAIL");
    }

    private static void comparePerformance() throws InterruptedException {
        int numThreads = 8;
        int opsPerThread = 100000;

        WaitFreeCounter wfCounter = new WaitFreeCounter(0);
        BlockingCounter bCounter = new BlockingCounter(0);

        PerformanceTest.testCounter("Wait-Free", wfCounter::incrementAndGet, numThreads, opsPerThread);
        PerformanceTest.testCounter("Blocking ", bCounter::incrementAndGet, numThreads, opsPerThread);

        System.out.println("\n💡 Note: Results depend on contention level and hardware.");
        System.out.println("   Wait-free is typically faster under high contention.");
    }
}
