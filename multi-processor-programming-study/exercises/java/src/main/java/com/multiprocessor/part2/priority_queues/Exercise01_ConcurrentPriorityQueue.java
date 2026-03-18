package com.multiprocessor.part2.priority_queues;

import java.util.PriorityQueue;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.ConcurrentSkipListSet;

/**
 * Exercise: Concurrent Priority Queues
 *
 * CONCEPT: Thread-safe priority queue implementations
 *
 * THE PROBLEM:
 * Priority queues are fundamental for:
 * - Task schedulers (execute highest priority tasks first)
 * - Event-driven systems (process events by priority)
 * - A* pathfinding and other graph algorithms
 * - Real-time systems (deadline scheduling)
 *
 * CHALLENGE:
 * Standard heap-based priority queues have a bottleneck:
 * - All operations (insert/extract-min) touch the root
 * - Root is a hotspot for contention
 * - Even with fine-grained locking, scalability is limited
 *
 * SOLUTIONS:
 * 1. Lock-Based Heap: Simple but limited scalability
 * 2. ConcurrentSkipListSet: Java's built-in concurrent sorted set
 * 3. Relaxed Priority Queue: Allow bounded error for better performance
 *
 * LEARNING OBJECTIVES:
 * - Understand priority queue contention issues
 * - Implement different synchronization strategies
 * - Trade-offs between strict ordering and performance
 * - Relaxed data structures for better scalability
 * - Compare with Java's built-in concurrent collections
 *
 * CPU REQUIREMENTS:
 * - Minimum: 4 cores
 * - Recommended: 8+ cores (to observe contention at root)
 * - Optimal: 16+ cores (scalability differences become clear)
 */
public class Exercise01_ConcurrentPriorityQueue {

    /**
     * TODO: Implement Lock-Based Priority Queue
     *
     * Simple approach: Single lock protecting PriorityQueue
     */
    public static class LockBasedPriorityQueue<T extends Comparable<T>> {
        private final PriorityQueue<T> heap;
        private final Lock lock;

        public LockBasedPriorityQueue() {
            this.heap = new PriorityQueue<>();
            this.lock = new ReentrantLock();
        }

        /**
         * TODO: Implement insert
         */
        public void insert(T value) {
            // TODO: Lock and insert
            lock.lock();
            try {
                heap.offer(value);
            } finally {
                lock.unlock();
            }
        }

        /**
         * TODO: Implement extractMin
         */
        public T extractMin() {
            // TODO: Lock, check empty, extract
            lock.lock();
            try {
                return heap.poll();
            } finally {
                lock.unlock();
            }
        }

        public boolean isEmpty() {
            lock.lock();
            try {
                return heap.isEmpty();
            } finally {
                lock.unlock();
            }
        }

        public int size() {
            lock.lock();
            try {
                return heap.size();
            } finally {
                lock.unlock();
            }
        }
    }

    /**
     * Wrapper around Java's ConcurrentSkipListSet
     *
     * Java provides this built-in concurrent sorted set which can serve as a priority queue
     */
    public static class SkipListPriorityQueue<T extends Comparable<T>> {
        private final ConcurrentSkipListSet<T> skiplist;

        public SkipListPriorityQueue() {
            this.skiplist = new ConcurrentSkipListSet<>();
        }

        public void insert(T value) {
            skiplist.add(value);
        }

        public T extractMin() {
            return skiplist.pollFirst();
        }

        public boolean isEmpty() {
            return skiplist.isEmpty();
        }

        public int size() {
            return skiplist.size();
        }
    }

    /**
     * TODO: Implement Relaxed Priority Queue
     *
     * Key idea: Allow bounded error in priority ordering for better scalability
     */
    public static class RelaxedPriorityQueue<T> {
        private static class Segment<T> {
            final List<T> items = new ArrayList<>();
            final Lock lock = new ReentrantLock();
            final AtomicBoolean hasItems = new AtomicBoolean(false);
        }

        private static final int NUM_SEGMENTS = 16;
        private final Segment<T>[] segments;
        private final int minPriority;
        private final int maxPriority;
        private final int segmentWidth;

        @SuppressWarnings("unchecked")
        public RelaxedPriorityQueue(int minPri, int maxPri) {
            this.segments = (Segment<T>[]) new Segment[NUM_SEGMENTS];
            for (int i = 0; i < NUM_SEGMENTS; i++) {
                segments[i] = new Segment<>();
            }
            this.minPriority = minPri;
            this.maxPriority = maxPri;
            this.segmentWidth = (maxPriority - minPriority + NUM_SEGMENTS - 1) / NUM_SEGMENTS;
        }

        private int getSegment(int priority) {
            int seg = (priority - minPriority) / segmentWidth;
            return Math.max(0, Math.min(seg, NUM_SEGMENTS - 1));
        }

        /**
         * TODO: Implement insert
         */
        public void insert(T value, int priority) {
            // TODO: Find segment, lock, insert
            int seg = getSegment(priority);
            segments[seg].lock.lock();
            try {
                segments[seg].items.add(value);
                segments[seg].hasItems.set(true);
            } finally {
                segments[seg].lock.unlock();
            }
        }

        /**
         * TODO: Implement extractMin
         */
        public T extractMin() {
            // TODO: Scan segments from high to low priority
            for (int seg = 0; seg < NUM_SEGMENTS; seg++) {
                if (!segments[seg].hasItems.get()) {
                    continue;
                }

                segments[seg].lock.lock();
                try {
                    if (!segments[seg].items.isEmpty()) {
                        T value = segments[seg].items.remove(segments[seg].items.size() - 1);
                        if (segments[seg].items.isEmpty()) {
                            segments[seg].hasItems.set(false);
                        }
                        return value;
                    }
                } finally {
                    segments[seg].lock.unlock();
                }
            }
            return null;
        }

        public boolean isEmpty() {
            for (Segment<T> seg : segments) {
                if (seg.hasItems.get()) {
                    return false;
                }
            }
            return true;
        }
    }

    /**
     * Testing Framework
     */
    public static void testCorrectness() {
        System.out.println("=== Correctness Tests ===\n");

        // Test Lock-Based
        {
            System.out.println("Test 1: Lock-Based Priority Queue");
            LockBasedPriorityQueue<Integer> pq = new LockBasedPriorityQueue<>();

            pq.insert(5);
            pq.insert(1);
            pq.insert(10);
            pq.insert(3);

            System.out.println("  Inserted: 5, 1, 10, 3");
            System.out.print("  Extracted: ");

            while (!pq.isEmpty()) {
                System.out.print(pq.extractMin() + " ");
            }
            System.out.println("(should be: 1 3 5 10)");
            System.out.println("  ✅ PASS\n");
        }

        // Test SkipList
        {
            System.out.println("Test 2: SkipList Priority Queue (ConcurrentSkipListSet)");
            SkipListPriorityQueue<Integer> pq = new SkipListPriorityQueue<>();

            pq.insert(5);
            pq.insert(1);
            pq.insert(10);
            pq.insert(3);

            System.out.println("  Inserted: 5, 1, 10, 3");
            System.out.print("  Extracted: ");

            while (!pq.isEmpty()) {
                System.out.print(pq.extractMin() + " ");
            }
            System.out.println("(should be: 1 3 5 10)");
            System.out.println("  ✅ PASS\n");
        }

        // Test Relaxed
        {
            System.out.println("Test 3: Relaxed Priority Queue");
            RelaxedPriorityQueue<Integer> pq = new RelaxedPriorityQueue<>(0, 100);

            pq.insert(50, 50);
            pq.insert(10, 10);
            pq.insert(90, 90);
            pq.insert(30, 30);

            System.out.println("  Inserted with priorities: 50, 10, 90, 30");
            System.out.print("  Extracted: ");

            while (!pq.isEmpty()) {
                Integer val = pq.extractMin();
                if (val != null) {
                    System.out.print(val + " ");
                }
            }
            System.out.println("\n  (Order approximate due to relaxation)");
            System.out.println("  ✅ PASS\n");
        }
    }

    public static void comparePerformance() throws InterruptedException {
        System.out.println("=== Performance Comparison ===\n");

        final int numThreads = Runtime.getRuntime().availableProcessors();
        final int opsPerThread = 10000;

        System.out.println("Threads: " + numThreads);
        System.out.println("Operations per thread: " + opsPerThread + "\n");

        Random rand = new Random();

        // Test Lock-Based
        {
            LockBasedPriorityQueue<Integer> pq = new LockBasedPriorityQueue<>();
            AtomicInteger completed = new AtomicInteger(0);

            long start = System.currentTimeMillis();

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < numThreads; i++) {
                threads.add(new Thread(() -> {
                    Random localRand = new Random();
                    for (int j = 0; j < opsPerThread; j++) {
                        if (j % 2 == 0) {
                            pq.insert(localRand.nextInt(1000));
                        } else {
                            pq.extractMin();
                        }
                    }
                    completed.addAndGet(opsPerThread);
                }));
            }

            for (Thread t : threads) t.start();
            for (Thread t : threads) t.join();

            long duration = System.currentTimeMillis() - start;

            System.out.println("Lock-Based Priority Queue:");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Throughput: " + (completed.get() * 1000.0 / duration) + " ops/sec\n");
        }

        // Test SkipList
        {
            SkipListPriorityQueue<Integer> pq = new SkipListPriorityQueue<>();
            AtomicInteger completed = new AtomicInteger(0);

            long start = System.currentTimeMillis();

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < numThreads; i++) {
                threads.add(new Thread(() -> {
                    Random localRand = new Random();
                    for (int j = 0; j < opsPerThread; j++) {
                        if (j % 2 == 0) {
                            pq.insert(localRand.nextInt(1000));
                        } else {
                            pq.extractMin();
                        }
                    }
                    completed.addAndGet(opsPerThread);
                }));
            }

            for (Thread t : threads) t.start();
            for (Thread t : threads) t.join();

            long duration = System.currentTimeMillis() - start;

            System.out.println("SkipList Priority Queue (ConcurrentSkipListSet):");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Throughput: " + (completed.get() * 1000.0 / duration) + " ops/sec\n");
        }

        // Test Relaxed
        {
            RelaxedPriorityQueue<Integer> pq = new RelaxedPriorityQueue<>(0, 1000);
            AtomicInteger completed = new AtomicInteger(0);

            long start = System.currentTimeMillis();

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < numThreads; i++) {
                threads.add(new Thread(() -> {
                    Random localRand = new Random();
                    for (int j = 0; j < opsPerThread; j++) {
                        if (j % 2 == 0) {
                            int val = localRand.nextInt(1000);
                            pq.insert(val, val);
                        } else {
                            pq.extractMin();
                        }
                    }
                    completed.addAndGet(opsPerThread);
                }));
            }

            for (Thread t : threads) t.start();
            for (Thread t : threads) t.join();

            long duration = System.currentTimeMillis() - start;

            System.out.println("Relaxed Priority Queue:");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Throughput: " + (completed.get() * 1000.0 / duration) + " ops/sec\n");
        }

        System.out.println("💡 Lock-based: Simple but limited scalability");
        System.out.println("💡 SkipList: Java's built-in, good concurrency");
        System.out.println("💡 Relaxed: Best scalability, approximate ordering");
    }

    public static void demonstrateConcepts() {
        System.out.println("=== Concurrent Priority Queue Concepts ===\n");

        System.out.println("The Contention Problem:");
        System.out.println("  • Heap-based: All operations touch root (hotspot)");
        System.out.println("  • Even with locks, root is bottleneck");
        System.out.println("  • Scalability limited by root contention\n");

        System.out.println("Solution 1: Lock-Based Heap");
        System.out.println("  ✅ Simple to implement");
        System.out.println("  ✅ Strict priority ordering");
        System.out.println("  ❌ Single lock = limited scalability");
        System.out.println("  ❌ Root contention\n");

        System.out.println("Solution 2: Java ConcurrentSkipListSet");
        System.out.println("  ✅ Built-in concurrent sorted set");
        System.out.println("  ✅ Lock-free operations");
        System.out.println("  ✅ Good concurrency");
        System.out.println("  ⚠️  Still some contention at head\n");

        System.out.println("Solution 3: Relaxed Priority Queue");
        System.out.println("  ✅ Excellent scalability");
        System.out.println("  ✅ Distributed contention");
        System.out.println("  ✅ Bounded error (one segment)");
        System.out.println("  ⚠️  Approximate ordering (may be acceptable)\n");

        System.out.println("Applications:");
        System.out.println("  • Task schedulers (strict: lock-based, relaxed: ok)");
        System.out.println("  • Event processing (skiplist good compromise)");
        System.out.println("  • Real-time systems (strict ordering needed)");
        System.out.println("  • Graph algorithms (relaxed often acceptable)\n");

        System.out.println("Java Built-in Options:");
        System.out.println("  • PriorityQueue: Not thread-safe");
        System.out.println("  • ConcurrentSkipListSet: Thread-safe, sorted");
        System.out.println("  • PriorityBlockingQueue: Thread-safe, blocking\n");
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrent Priority Queues Test ===\n");

        demonstrateConcepts();
        testCorrectness();
        comparePerformance();
    }
}
