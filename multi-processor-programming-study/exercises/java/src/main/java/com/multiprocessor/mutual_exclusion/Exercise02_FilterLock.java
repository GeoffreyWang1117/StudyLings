package com.multiprocessor.mutual_exclusion;

/**
 * Exercise: Filter Lock
 *
 * CONCEPT: n-thread mutual exclusion using the Filter lock
 *
 * The Filter lock is a generalization of Peterson's algorithm for n threads.
 * It creates n-1 "levels" of exclusion. At each level, at least one thread
 * trying to get in is blocked. This ensures that only one thread can reach
 * level n-1 (the critical section).
 *
 * KEY IDEA:
 * - n-1 levels (levels 0 through n-2)
 * - At most n-i threads at level i
 * - At level n-1, only 1 thread (mutual exclusion)
 *
 * ALGORITHM:
 * - Each thread announces its level
 * - Each thread becomes the victim for that level
 * - Each thread waits while there exists another thread at a higher or equal
 *   level AND it is the victim for that level
 *
 * LEARNING OBJECTIVES:
 * - Understand how Peterson's algorithm generalizes to n threads
 * - Learn about levels of exclusion
 * - Understand the relationship between levels and thread count
 */
public class Exercise02_FilterLock {

    /**
     * TODO: Implement the Filter Lock for n threads
     */
    public static class FilterLock {
        private final int n; // number of threads

        // TODO: Declare the necessary arrays
        // HINT: level[i] is the current level of thread i
        // HINT: victim[L] is the victim thread at level L
        // HINT: Both should be volatile arrays or use AtomicIntegerArray

        // private volatile int[] level;
        // private volatile int[] victim;

        public FilterLock(int n) {
            this.n = n;
            // TODO: Initialize the arrays
        }

        /**
         * TODO: Implement the lock method for Filter lock
         *
         * @param threadId The ID of the calling thread (0 to n-1)
         */
        public void lock(int threadId) {
            // TODO: Implement the Filter lock protocol
            // For each level from 0 to n-2:
            //   1. Set level[threadId] = L (announce your level)
            //   2. Set victim[L] = threadId (become the victim at this level)
            //   3. Wait while (exists k != threadId where level[k] >= L) AND victim[L] == threadId
        }

        /**
         * TODO: Implement the unlock method
         *
         * @param threadId The ID of the calling thread
         */
        public void unlock(int threadId) {
            // TODO: Implement unlock
            // HINT: Set level[threadId] to 0 (exit all levels)
        }
    }

    /**
     * Test harness
     */
    static class SharedResource {
        private int value = 0;
        private int concurrentAccess = 0;

        public void criticalSection(int threadId) {
            // Check mutual exclusion
            if (concurrentAccess > 0) {
                throw new IllegalStateException(
                    "Mutual exclusion violated! Thread " + threadId +
                    " entered while another thread was in critical section");
            }
            concurrentAccess++;

            // Do some work
            value++;

            concurrentAccess--;
        }

        public int getValue() {
            return value;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        int numThreads = 8;
        int iterationsPerThread = 10000;

        System.out.println("=== Filter Lock Test ===");
        System.out.println("Threads: " + numThreads);
        System.out.println("Iterations per thread: " + iterationsPerThread);

        FilterLock lock = new FilterLock(numThreads);
        SharedResource resource = new SharedResource();
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
            System.out.println("✅ PASS - Filter lock working correctly!");
        } else {
            System.out.println("❌ FAIL - Mutual exclusion violated!");
        }
    }
}
