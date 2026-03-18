package com.multiprocessor.concurrent_objects;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * Exercise: Sequential Consistency
 *
 * CONCEPT: Sequential consistency and its properties
 *
 * Sequential Consistency: The result of any execution is the same as if
 * operations of all threads were executed in some sequential order, and
 * operations of each thread appear in this sequence in program order.
 *
 * KEY PROPERTIES:
 * - Method calls appear to happen in a one-at-a-time sequential order
 * - Method calls of each individual thread appear in program order
 * - Weaker than linearizability (no real-time ordering requirement)
 *
 * LEARNING OBJECTIVES:
 * - Understand sequential consistency
 * - Implement a sequentially consistent counter
 * - Compare with linearizability
 */
public class Exercise01_SequentialConsistency {

    /**
     * TODO: Implement a sequentially consistent counter
     *
     * This counter should maintain sequential consistency:
     * - All threads see a consistent order of operations
     * - Operations from each thread appear in program order
     */
    public static class SequentialCounter {
        private AtomicInteger value;

        public SequentialCounter() {
            // TODO: Initialize the counter
        }

        /**
         * TODO: Implement increment operation
         * Should be sequentially consistent
         *
         * @return the value BEFORE increment
         */
        public int getAndIncrement() {
            // TODO: Implement this
            // HINT: Use AtomicInteger's getAndIncrement
            return 0;
        }

        /**
         * TODO: Implement get operation
         *
         * @return current value
         */
        public int get() {
            // TODO: Implement this
            return 0;
        }

        /**
         * TODO: Implement set operation
         *
         * @param newValue the new value
         */
        public void set(int newValue) {
            // TODO: Implement this
        }
    }

    /**
     * TODO: Implement a sequentially consistent register
     *
     * A register supports read() and write() operations.
     * This implementation should be sequentially consistent.
     */
    public static class SequentialRegister<T> {
        private volatile T value;

        public SequentialRegister(T initialValue) {
            this.value = initialValue;
        }

        /**
         * TODO: Implement read operation
         *
         * @return current value
         */
        public T read() {
            // TODO: Implement this
            // HINT: Simply return the volatile field
            return null;
        }

        /**
         * TODO: Implement write operation
         *
         * @param newValue value to write
         */
        public void write(T newValue) {
            // TODO: Implement this
            // HINT: Simply set the volatile field
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Sequential Consistency Test ===\n");

        testSequentialCounter();
        testSequentialRegister();
    }

    private static void testSequentialCounter() throws InterruptedException {
        System.out.println("Testing Sequential Counter:");

        SequentialCounter counter = new SequentialCounter();
        int numThreads = 10;
        int incrementsPerThread = 1000;

        Thread[] threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.getAndIncrement();
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        int expected = numThreads * incrementsPerThread;
        int actual = counter.get();

        System.out.println("Expected: " + expected);
        System.out.println("Actual: " + actual);
        System.out.println(actual == expected ? "✅ PASS\n" : "❌ FAIL\n");
    }

    private static void testSequentialRegister() throws InterruptedException {
        System.out.println("Testing Sequential Register:");

        SequentialRegister<String> register = new SequentialRegister<>("initial");

        // Writer thread
        Thread writer = new Thread(() -> {
            for (int i = 0; i < 100; i++) {
                register.write("value-" + i);
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        // Reader threads
        Thread[] readers = new Thread[3];
        for (int i = 0; i < readers.length; i++) {
            final int readerId = i;
            readers[i] = new Thread(() -> {
                for (int j = 0; j < 50; j++) {
                    String value = register.read();
                    System.out.println("Reader " + readerId + " read: " + value);
                    try {
                        Thread.sleep(2);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }

        writer.start();
        for (Thread reader : readers) {
            reader.start();
        }

        writer.join();
        for (Thread reader : readers) {
            reader.join();
        }

        System.out.println("✅ Sequential register test completed\n");
    }
}
