package com.multiprocessor.part2.counting;

import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.LongAdder;
import java.util.Arrays;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

/**
 * Exercise: Parallel Counting and Reduction
 *
 * CONCEPT: Efficient parallel counting using various strategies
 *
 * Strategies:
 * - Combining: Threads combine their partial results
 * - Striping: Distribute counts across cache lines
 * - Tree-based: Hierarchical reduction
 *
 * LEARNING OBJECTIVES:
 * - Implement scalable counters
 * - Use LongAdder for high contention
 * - Understand false sharing and cache line padding
 * - Implement parallel reduction patterns
 */
public class Exercise01_ParallelCounting {

    /**
     * TODO: Implement Combining Counter
     *
     * Threads combine their increments before accessing shared counter
     */
    public static class CombiningCounter {
        private final AtomicLong counter = new AtomicLong(0);
        private static final int COMBINING_THRESHOLD = 100;

        // Thread-local buffer for combining
        private final ThreadLocal<Long> localBuffer = ThreadLocal.withInitial(() -> 0L);

        /**
         * TODO: Implement increment with combining
         */
        public void increment() {
            // TODO: Increment thread-local buffer
            // TODO: When buffer reaches threshold, flush to global counter
        }

        /**
         * TODO: Implement flush
         */
        private void flush() {
            // TODO: Add local buffer to global counter atomically
            // TODO: Reset local buffer
        }

        public long get() {
            // TODO: Sum global counter + all pending local buffers
            return counter.get();
        }
    }

    /**
     * TODO: Implement Cache-line Padded Counter
     *
     * Avoid false sharing by padding to cache line size
     */
    public static class PaddedCounter {
        // Cache line is typically 64 bytes
        // Java object header is ~16 bytes
        // long is 8 bytes
        // Need ~40 bytes padding

        private volatile long p0, p1, p2, p3, p4; // Padding before
        private volatile long value = 0;
        private volatile long p5, p6, p7, p8, p9; // Padding after

        /**
         * TODO: Implement thread-safe increment
         */
        public synchronized void increment() {
            // TODO: Increment value
        }

        public long get() {
            return value;
        }
    }

    /**
     * TODO: Implement Parallel Array Sum using Fork/Join
     *
     * Divide-and-conquer parallel reduction
     */
    public static class ParallelArraySum extends RecursiveTask<Long> {
        private static final int THRESHOLD = 1000;
        private final long[] array;
        private final int start;
        private final int end;

        public ParallelArraySum(long[] array, int start, int end) {
            this.array = array;
            this.start = start;
            this.end = end;
        }

        @Override
        protected Long compute() {
            // TODO: If range small enough, compute sequentially
            // TODO: Otherwise, split in half and fork both subtasks
            // TODO: Join results from both subtasks
            return 0L;
        }

        public static long sum(long[] array) {
            // TODO: Create ForkJoinPool and invoke task
            return 0L;
        }
    }

    /**
     * TODO: Implement Scalable Counter using Striping
     *
     * Distribute count across multiple counters to reduce contention
     */
    public static class StripedCounter {
        private final AtomicLong[] stripes;
        private final int numStripes;

        public StripedCounter(int numStripes) {
            this.numStripes = numStripes;
            this.stripes = new AtomicLong[numStripes];
            // TODO: Initialize each stripe
            for (int i = 0; i < numStripes; i++) {
                stripes[i] = new AtomicLong(0);
            }
        }

        /**
         * TODO: Implement increment
         *
         * Hash thread ID to stripe to reduce contention
         */
        public void increment() {
            // TODO: Get thread ID hash
            // TODO: Select stripe based on hash
            // TODO: Increment selected stripe
        }

        /**
         * TODO: Implement get
         */
        public long get() {
            // TODO: Sum all stripes
            long sum = 0;
            for (AtomicLong stripe : stripes) {
                sum += stripe.get();
            }
            return sum;
        }
    }

    /**
     * Performance comparison
     */
    static class PerformanceTest {
        static void testCounter(String name, Runnable incrementOp,
                               java.util.function.LongSupplier getOp,
                               int numThreads, int incrementsPerThread)
                throws InterruptedException {

            Thread[] threads = new Thread[numThreads];
            long startTime = System.nanoTime();

            for (int i = 0; i < numThreads; i++) {
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < incrementsPerThread; j++) {
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

            System.out.printf("%-20s: %6dms (count=%d)%n",
                            name, duration, getOp.getAsLong());
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Parallel Counting Test ===\n");

        testCorrectness();
        System.out.println("\n=== Performance Comparison ===");
        comparePerformance();
        System.out.println("\n=== Parallel Array Sum ===");
        testParallelSum();
    }

    private static void testCorrectness() throws InterruptedException {
        int numThreads = 10;
        int incrementsPerThread = 1000;
        int expected = numThreads * incrementsPerThread;

        System.out.println("Testing correctness (threads=" + numThreads +
                         ", increments=" + incrementsPerThread + "):\n");

        // Test Striped Counter
        StripedCounter striped = new StripedCounter(numThreads);
        Thread[] threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    striped.increment();
                }
            });
            threads[i].start();
        }
        for (Thread t : threads) t.join();

        System.out.println("Striped Counter: Expected=" + expected +
                         ", Actual=" + striped.get() +
                         (striped.get() == expected ? " ✅" : " ❌"));

        // Test LongAdder (Java's optimized counter)
        LongAdder adder = new LongAdder();
        threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    adder.increment();
                }
            });
            threads[i].start();
        }
        for (Thread t : threads) t.join();

        System.out.println("LongAdder:       Expected=" + expected +
                         ", Actual=" + adder.sum() +
                         (adder.sum() == expected ? " ✅" : " ❌"));
    }

    private static void comparePerformance() throws InterruptedException {
        int numThreads = 16;
        int incrementsPerThread = 100000;

        System.out.println("High contention test (threads=" + numThreads +
                         ", increments=" + incrementsPerThread + "):\n");

        // AtomicLong (baseline)
        AtomicLong atomicCounter = new AtomicLong(0);
        PerformanceTest.testCounter("AtomicLong",
            atomicCounter::incrementAndGet,
            atomicCounter::get,
            numThreads, incrementsPerThread);

        // Striped Counter
        StripedCounter striped = new StripedCounter(numThreads);
        PerformanceTest.testCounter("StripedCounter",
            striped::increment,
            striped::get,
            numThreads, incrementsPerThread);

        // LongAdder
        LongAdder adder = new LongAdder();
        PerformanceTest.testCounter("LongAdder",
            adder::increment,
            adder::sum,
            numThreads, incrementsPerThread);

        System.out.println("\n💡 LongAdder uses dynamic striping and is highly optimized");
        System.out.println("💡 StripedCounter shows the principle behind LongAdder");
    }

    private static void testParallelSum() {
        int size = 10_000_000;
        long[] array = new long[size];
        Arrays.fill(array, 1);

        System.out.println("Array size: " + size);

        // Sequential
        long start = System.nanoTime();
        long seqSum = 0;
        for (long value : array) {
            seqSum += value;
        }
        long seqTime = (System.nanoTime() - start) / 1_000_000;

        // Parallel
        start = System.nanoTime();
        long parSum = ParallelArraySum.sum(array);
        long parTime = (System.nanoTime() - start) / 1_000_000;

        System.out.println("Sequential sum: " + seqSum + " (" + seqTime + "ms)");
        System.out.println("Parallel sum:   " + parSum + " (" + parTime + "ms)");
        System.out.println("Speedup: " + String.format("%.2fx", (double)seqTime / parTime));
        System.out.println(seqSum == parSum ? "✅ Correct" : "❌ Incorrect");
    }
}
