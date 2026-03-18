package com.multiprocessor.mutual_exclusion;

/**
 * SOLUTION for Peterson's Lock Exercise
 *
 * This is a reference implementation of Peterson's two-thread mutual exclusion algorithm.
 */
public class Exercise01_PetersonLock_Solution {

    public static class PetersonLock {
        // Flags indicate if a thread wants to enter critical section
        private volatile boolean[] flag = new boolean[2];

        // Victim is the thread that will defer to the other
        private volatile int victim;

        /**
         * SOLUTION: Peterson's lock protocol
         */
        public void lock(int threadId) {
            int other = 1 - threadId;

            // Step 1: Indicate interest
            flag[threadId] = true;

            // Step 2: Set yourself as victim (be polite!)
            victim = threadId;

            // Step 3: Wait while other is interested AND you are the victim
            // If you're not the victim, you can proceed
            // If other is not interested, you can proceed
            while (flag[other] && victim == threadId) {
                // Busy wait (spin)
                // This is where the waiting happens
            }
            // At this point, we have acquired the lock
        }

        /**
         * SOLUTION: Release the lock
         */
        public void unlock(int threadId) {
            // Simply indicate that we're no longer interested
            flag[threadId] = false;
        }
    }

    /**
     * Test harness
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
     * Demonstration
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
