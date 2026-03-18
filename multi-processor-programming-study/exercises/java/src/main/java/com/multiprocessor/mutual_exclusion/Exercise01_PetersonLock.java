package com.multiprocessor.mutual_exclusion;

/**
 * Exercise: Peterson's Algorithm
 *
 * CONCEPT: Two-thread mutual exclusion using Peterson's algorithm
 *
 * Peterson's algorithm is a classic solution to the mutual exclusion problem
 * for two threads. It uses two flags and a victim variable to ensure that
 * only one thread can enter the critical section at a time.
 *
 * KEY PROPERTIES:
 * 1. Mutual Exclusion: At most one thread in critical section
 * 2. Deadlock-free: Some thread eventually enters critical section
 * 3. Starvation-free: Every thread eventually enters critical section
 *
 * ALGORITHM:
 * - Each thread sets its flag to indicate interest
 * - Each thread sets itself as the victim
 * - Each thread waits while the other is interested AND it is the victim
 *
 * LEARNING OBJECTIVES:
 * - Understand classical mutual exclusion algorithms
 * - Learn about memory visibility and ordering
 * - Understand the difference between safety and liveness properties
 *
 * NOTE: In Java, you need to use 'volatile' for correctness due to memory model
 */
public class Exercise01_PetersonLock {

    /**
     * TODO: Implement Peterson's Lock for two threads
     */
    public static class PetersonLock {
        // TODO: Declare the necessary instance variables
        // HINT: You need two flags (one per thread) and a victim variable
        // HINT: These should be volatile to ensure proper memory visibility

        // private volatile boolean[] flag = new boolean[2];
        // private volatile int victim;

        /**
         * TODO: Implement the lock method for Peterson's algorithm
         *
         * @param threadId The ID of the calling thread (0 or 1)
         */
        public void lock(int threadId) {
            // TODO: Implement Peterson's lock protocol
            // Step 1: Set your flag to true (indicate interest)
            // Step 2: Set yourself as the victim
            // Step 3: Wait while the other thread is interested AND you are the victim
        }

        /**
         * TODO: Implement the unlock method
         *
         * @param threadId The ID of the calling thread (0 or 1)
         */
        public void unlock(int threadId) {
            // TODO: Implement unlock
            // HINT: Just set your flag to false
        }
    }

    /**
     * Test harness to verify mutual exclusion
     */
    static class Counter {
        private int count = 0;

        public void increment() {
            count++;
        }

        public int getCount() {
            return count;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Peterson Lock Test ===");

        PetersonLock lock = new PetersonLock();
        Counter counter = new Counter();
        int incrementsPerThread = 100000;

        Thread thread0 = new Thread(() -> {
            for (int i = 0; i < incrementsPerThread; i++) {
                lock.lock(0);
                try {
                    counter.increment();
                } finally {
                    lock.unlock(0);
                }
            }
        });

        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < incrementsPerThread; i++) {
                lock.lock(1);
                try {
                    counter.increment();
                } finally {
                    lock.unlock(1);
                }
            }
        });

        long startTime = System.currentTimeMillis();
        thread0.start();
        thread1.start();

        thread0.join();
        thread1.join();
        long endTime = System.currentTimeMillis();

        int expected = incrementsPerThread * 2;
        int actual = counter.getCount();

        System.out.println("Expected count: " + expected);
        System.out.println("Actual count: " + actual);
        System.out.println("Time taken: " + (endTime - startTime) + "ms");

        if (actual == expected) {
            System.out.println("✅ PASS - Mutual exclusion preserved!");
        } else {
            System.out.println("❌ FAIL - Race condition detected!");
            System.out.println("Difference: " + (expected - actual));
        }
    }
}
