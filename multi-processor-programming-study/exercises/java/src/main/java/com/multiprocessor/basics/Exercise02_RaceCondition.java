package com.multiprocessor.basics;

/**
 * Exercise 02: Race Condition
 *
 * CONCEPT: Understanding race conditions in concurrent programs
 *
 * A race condition occurs when multiple threads access shared data concurrently
 * and at least one thread modifies it, leading to unpredictable results.
 *
 * LEARNING OBJECTIVES:
 * - Observe a race condition in action
 * - Understand why unsynchronized access to shared data is dangerous
 * - Learn to identify potential race conditions
 *
 * TODO: Complete the implementation to demonstrate a race condition
 */
public class Exercise02_RaceCondition {

    /**
     * A simple counter that is NOT thread-safe
     */
    public static class UnsafeCounter {
        private int count = 0;

        /**
         * TODO: Implement increment method (without synchronization)
         * This should simply add 1 to count
         */
        public void increment() {
            // TODO: Implement this
            // HINT: Just read count, add 1, and write it back
            // This is intentionally unsafe to demonstrate the race condition
        }

        public int getCount() {
            return count;
        }
    }

    /**
     * TODO: Create threads that increment the counter concurrently
     *
     * @param counter The counter to increment
     * @param threadsCount Number of threads to create
     * @param incrementsPerThread Number of times each thread should increment
     * @return Array of threads
     */
    public static Thread[] createIncrementThreads(UnsafeCounter counter,
                                                   int threadsCount,
                                                   int incrementsPerThread) {
        // TODO: Implement this method
        // Create threads that each call counter.increment() incrementsPerThread times
        return null;
    }

    /**
     * Demonstration main method
     */
    public static void main(String[] args) throws InterruptedException {
        UnsafeCounter counter = new UnsafeCounter();
        int numThreads = 10;
        int incrementsPerThread = 1000;

        System.out.println("Starting race condition demonstration...");
        System.out.println("Expected final count: " + (numThreads * incrementsPerThread));

        Thread[] threads = createIncrementThreads(counter, numThreads, incrementsPerThread);

        // Start all threads
        for (Thread t : threads) {
            t.start();
        }

        // Wait for all threads
        for (Thread t : threads) {
            t.join();
        }

        System.out.println("Actual final count: " + counter.getCount());
        System.out.println("Difference: " + (numThreads * incrementsPerThread - counter.getCount()));

        if (counter.getCount() != numThreads * incrementsPerThread) {
            System.out.println("❌ Race condition detected! The count is incorrect.");
            System.out.println("💡 This happens because multiple threads read-modify-write without coordination.");
        } else {
            System.out.println("⚠️  No race condition observed this time (try running again)");
        }
    }
}
