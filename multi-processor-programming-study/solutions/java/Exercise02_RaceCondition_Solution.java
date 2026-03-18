package com.multiprocessor.basics;

/**
 * SOLUTION for Exercise 02: Race Condition
 *
 * This demonstrates a race condition by implementing an unsafe counter.
 * The race condition is INTENTIONAL to show the problem.
 */
public class Exercise02_RaceCondition_Solution {

    public static class UnsafeCounter {
        private int count = 0;

        /**
         * SOLUTION: Intentionally unsafe increment
         * This causes a race condition when multiple threads call it
         */
        public void increment() {
            // This is a read-modify-write operation that is NOT atomic
            // Multiple threads can read the same value, increment it,
            // and write back, causing lost updates
            count = count + 1;

            // Equivalent to:
            // int temp = count;    // READ
            // temp = temp + 1;     // MODIFY
            // count = temp;        // WRITE
        }

        public int getCount() {
            return count;
        }
    }

    /**
     * SOLUTION: Create threads that increment the counter
     */
    public static Thread[] createIncrementThreads(UnsafeCounter counter,
                                                   int threadsCount,
                                                   int incrementsPerThread) {
        Thread[] threads = new Thread[threadsCount];

        for (int i = 0; i < threadsCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment();
                }
            });
        }

        return threads;
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
