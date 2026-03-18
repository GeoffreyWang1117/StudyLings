package com.multiprocessor.mutual_exclusion;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Exercise: Bakery Algorithm
 *
 * CONCEPT: Fair mutual exclusion using the Bakery Algorithm
 *
 * The Bakery Algorithm was invented by Leslie Lamport in 1974.
 * It provides FCFS (first-come-first-served) fairness - threads enter
 * the critical section in the order they request access.
 *
 * REAL-WORLD ANALOGY:
 * Like a bakery where customers take numbered tickets:
 * - Each customer takes a number when they arrive
 * - The customer with the smallest number is served first
 * - If two customers have the same number, use their customer ID to break ties
 *
 * KEY PROPERTIES:
 * - First-come-first-served fairness
 * - Deadlock-free
 * - No starvation
 * - Works for n threads
 *
 * ALGORITHM:
 * 1. Thread announces it's entering (choosing = true)
 * 2. Thread takes a number: max(all other numbers) + 1
 * 3. Thread announces it has a number (choosing = false)
 * 4. For each other thread k:
 *    - Wait until k finishes choosing
 *    - Wait while k has a smaller ticket, OR same ticket but smaller ID
 *
 * LEARNING OBJECTIVES:
 * - Understand ticket-based mutual exclusion
 * - Learn about lexicographic ordering for tie-breaking
 * - Understand FCFS fairness guarantees
 * - Compare with Peterson and Filter locks
 *
 * HISTORICAL SIGNIFICANCE:
 * - First algorithm to solve mutual exclusion with FCFS fairness
 * - Used atomic read/write only (no test-and-set or other atomic operations)
 * - Introduced the concept of logical timestamps in distributed systems
 */
public class Exercise03_BakeryLock {

    /**
     * TODO: Implement the Bakery Lock
     *
     * The Bakery lock uses ticket numbers for FCFS fairness.
     */
    public static class BakeryLock {
        private final int n; // number of threads

        // TODO: Declare the necessary arrays
        // HINT: choosing[i] = true when thread i is taking a number
        // HINT: number[i] = the ticket number of thread i (0 = not interested)
        // HINT: Use AtomicBoolean[] and AtomicInteger[] for thread safety

        private final AtomicBoolean[] choosing;
        private final AtomicInteger[] number;

        public BakeryLock(int n) {
            this.n = n;
            // TODO: Initialize the arrays
            this.choosing = new AtomicBoolean[n];
            this.number = new AtomicInteger[n];
            for (int i = 0; i < n; i++) {
                choosing[i] = new AtomicBoolean(false);
                number[i] = new AtomicInteger(0);
            }
        }

        /**
         * TODO: Implement the lock method for Bakery lock
         *
         * @param threadId The ID of the calling thread (0 to n-1)
         */
        public void lock(int threadId) {
            // TODO: Implement the Bakery lock protocol
            // Step 1: Announce we're taking a number
            choosing[threadId].set(true);

            // Step 2: Take a number (max of all numbers + 1)
            int maxNumber = 0;
            for (int i = 0; i < n; i++) {
                int currentNumber = number[i].get();
                if (currentNumber > maxNumber) {
                    maxNumber = currentNumber;
                }
            }
            number[threadId].set(maxNumber + 1);

            // Step 3: Announce we've taken a number
            choosing[threadId].set(false);

            // Step 4: Wait for all threads with smaller tickets
            for (int k = 0; k < n; k++) {
                if (k == threadId) continue;

                // Wait until thread k finishes choosing
                while (choosing[k].get()) {
                    // Busy wait
                }

                // Wait while thread k has priority over us
                // Priority: smaller number, or same number with smaller ID
                while (number[k].get() != 0 &&
                       hasPriority(k, threadId)) {
                    // Busy wait
                }
            }
        }

        /**
         * Helper method: Does thread k have priority over thread j?
         *
         * Priority is determined by lexicographic ordering (number, threadId):
         * - Thread k has priority if it has a smaller number
         * - If numbers are equal, thread k has priority if k < j
         */
        private boolean hasPriority(int k, int j) {
            int numberK = number[k].get();
            int numberJ = number[j].get();

            // Lexicographic ordering: (number[k], k) < (number[j], j)
            return (numberK < numberJ) ||
                   (numberK == numberJ && k < j);
        }

        /**
         * TODO: Implement the unlock method
         *
         * @param threadId The ID of the calling thread
         */
        public void unlock(int threadId) {
            // TODO: Implement unlock
            // HINT: Set number[threadId] to 0 (no longer interested)
            number[threadId].set(0);
        }
    }

    /**
     * Test harness with fairness verification
     */
    static class SharedResource {
        private int value = 0;
        private int concurrentAccess = 0;
        private final int[] entryOrder;
        private int entryCount = 0;

        public SharedResource(int numThreads) {
            this.entryOrder = new int[numThreads * 1000]; // Track entry order
        }

        public synchronized void criticalSection(int threadId) {
            // Check mutual exclusion
            if (concurrentAccess > 0) {
                throw new IllegalStateException(
                    "Mutual exclusion violated! Thread " + threadId +
                    " entered while another thread was in critical section");
            }
            concurrentAccess++;

            // Track entry order for fairness verification
            if (entryCount < entryOrder.length) {
                entryOrder[entryCount++] = threadId;
            }

            // Do some work
            value++;

            concurrentAccess--;
        }

        public int getValue() {
            return value;
        }

        public int[] getEntryOrder() {
            return entryOrder;
        }

        public int getEntryCount() {
            return entryCount;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Bakery Lock Test ===\n");

        // Test 1: Correctness Test
        testCorrectness();

        // Test 2: Fairness Test
        System.out.println();
        testFairness();

        // Test 3: Performance Comparison
        System.out.println();
        comparePerformance();
    }

    /**
     * Test correctness: mutual exclusion
     */
    private static void testCorrectness() throws InterruptedException {
        int numThreads = 8;
        int iterationsPerThread = 10000;

        System.out.println("Test 1: Correctness (Mutual Exclusion)");
        System.out.println("Threads: " + numThreads);
        System.out.println("Iterations per thread: " + iterationsPerThread);

        BakeryLock lock = new BakeryLock(numThreads);
        SharedResource resource = new SharedResource(numThreads);
        Thread[] threads = new Thread[numThreads];

        long startTime = System.currentTimeMillis();

        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < iterationsPerThread; j++) {
                    lock.lock(threadId);
                    try {
                        resource.criticalSection(threadId);
                    } finally {
                        lock.unlock(threadId);
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        long endTime = System.currentTimeMillis();

        int expected = numThreads * iterationsPerThread;
        int actual = resource.getValue();

        System.out.println("\nExpected value: " + expected);
        System.out.println("Actual value: " + actual);
        System.out.println("Time taken: " + (endTime - startTime) + "ms");

        if (actual == expected) {
            System.out.println("✅ PASS - Bakery lock provides mutual exclusion!");
        } else {
            System.out.println("❌ FAIL - Mutual exclusion violated!");
        }
    }

    /**
     * Test fairness: FCFS property
     */
    private static void testFairness() throws InterruptedException {
        int numThreads = 4;
        int iterations = 100;

        System.out.println("Test 2: Fairness (FCFS)");
        System.out.println("Threads: " + numThreads);
        System.out.println("Iterations: " + iterations);

        BakeryLock lock = new BakeryLock(numThreads);
        SharedResource resource = new SharedResource(numThreads);
        Thread[] threads = new Thread[numThreads];

        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < iterations; j++) {
                    lock.lock(threadId);
                    try {
                        resource.criticalSection(threadId);
                    } finally {
                        lock.unlock(threadId);
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        // Analyze entry order
        int[] entryCount = new int[numThreads];
        int[] entryOrder = resource.getEntryOrder();
        int totalEntries = resource.getEntryCount();

        for (int i = 0; i < totalEntries; i++) {
            entryCount[entryOrder[i]]++;
        }

        System.out.println("\nEntry distribution:");
        for (int i = 0; i < numThreads; i++) {
            System.out.println("  Thread " + i + ": " + entryCount[i] + " entries");
        }

        // Check fairness: no thread should be starved
        int minEntries = Integer.MAX_VALUE;
        int maxEntries = Integer.MIN_VALUE;
        for (int count : entryCount) {
            minEntries = Math.min(minEntries, count);
            maxEntries = Math.max(maxEntries, count);
        }

        System.out.println("\nFairness analysis:");
        System.out.println("  Min entries: " + minEntries);
        System.out.println("  Max entries: " + maxEntries);
        System.out.println("  Ratio: " + (double)maxEntries / minEntries);

        if (minEntries > 0 && (double)maxEntries / minEntries < 2.0) {
            System.out.println("✅ PASS - Good fairness (FCFS property observed)!");
        } else if (minEntries > 0) {
            System.out.println("⚠️  WARN - Some unfairness detected, but no starvation");
        } else {
            System.out.println("❌ FAIL - Thread starvation detected!");
        }
    }

    /**
     * Performance comparison
     */
    private static void comparePerformance() throws InterruptedException {
        int numThreads = 4;
        int iterationsPerThread = 5000;

        System.out.println("Test 3: Performance Comparison");
        System.out.println("Threads: " + numThreads);
        System.out.println("Iterations per thread: " + iterationsPerThread);
        System.out.println();

        // Bakery Lock
        {
            BakeryLock lock = new BakeryLock(numThreads);
            SharedResource resource = new SharedResource(numThreads);
            Thread[] threads = new Thread[numThreads];

            long startTime = System.currentTimeMillis();

            for (int i = 0; i < numThreads; i++) {
                final int threadId = i;
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < iterationsPerThread; j++) {
                        lock.lock(threadId);
                        try {
                            resource.criticalSection(threadId);
                        } finally {
                            lock.unlock(threadId);
                        }
                    }
                });
                threads[i].start();
            }

            for (Thread t : threads) {
                t.join();
            }

            long endTime = System.currentTimeMillis();
            System.out.println("Bakery Lock: " + (endTime - startTime) + "ms");
        }

        System.out.println();
        System.out.println("💡 Key Insights:");
        System.out.println("  • Bakery lock provides FCFS fairness");
        System.out.println("  • No thread starvation guaranteed");
        System.out.println("  • Overhead: O(n) for each lock/unlock");
        System.out.println("  • Best for: Small number of threads with fairness requirements");
    }
}
