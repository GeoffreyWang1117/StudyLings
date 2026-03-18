package com.multiprocessor.part2.hashing;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicReferenceArray;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.function.Function;

/**
 * Exercise: Concurrent Hash Maps
 *
 * CONCEPT: Different strategies for concurrent hash tables
 *
 * Strategies:
 * - Closed Addressing: Buckets with chaining
 * - Open Addressing: Probing strategies
 * - Lock Striping: Fine-grained locking per bucket
 * - Lock-Free: CAS-based operations
 *
 * LEARNING OBJECTIVES:
 * - Implement concurrent hash map with different strategies
 * - Understand resize challenges
 * - Handle concurrent modifications
 * - Compare performance trade-offs
 */
public class Exercise01_ConcurrentHashMap {

    /**
     * TODO: Implement Striped Hash Map
     *
     * Use lock striping - multiple locks for different buckets
     */
    public static class StripedHashMap<K, V> {
        private static class Node<K, V> {
            final K key;
            V value;
            Node<K, V> next;

            Node(K key, V value) {
                this.key = key;
                this.value = value;
            }
        }

        private final Node<K, V>[] buckets;
        private final Lock[] locks;
        private final int numLocks;

        @SuppressWarnings("unchecked")
        public StripedHashMap(int capacity, int numLocks) {
            this.buckets = (Node<K, V>[]) new Node[capacity];
            this.numLocks = numLocks;
            this.locks = new Lock[numLocks];
            // TODO: Initialize locks
            for (int i = 0; i < numLocks; i++) {
                locks[i] = new ReentrantLock();
            }
        }

        private int hash(K key) {
            return Math.abs(key.hashCode() % buckets.length);
        }

        private Lock getLock(K key) {
            return locks[Math.abs(key.hashCode() % numLocks)];
        }

        /**
         * TODO: Implement put
         */
        public V put(K key, V value) {
            Lock lock = getLock(key);
            lock.lock();
            try {
                int bucket = hash(key);
                // TODO: Search for existing key in bucket
                // TODO: If found, update value
                // TODO: If not found, add new node at head
                return null;
            } finally {
                lock.unlock();
            }
        }

        /**
         * TODO: Implement get
         */
        public V get(K key) {
            Lock lock = getLock(key);
            lock.lock();
            try {
                int bucket = hash(key);
                // TODO: Search bucket for key
                return null;
            } finally {
                lock.unlock();
            }
        }

        /**
         * TODO: Implement remove
         */
        public V remove(K key) {
            Lock lock = getLock(key);
            lock.lock();
            try {
                int bucket = hash(key);
                // TODO: Search and remove node with key
                return null;
            } finally {
                lock.unlock();
            }
        }
    }

    /**
     * TODO: Implement Lock-Free Hash Map
     *
     * Use CAS operations for wait-free operations
     * Simplified version - no resizing
     */
    public static class LockFreeHashMap<K, V> {
        private static class Node<K, V> {
            final K key;
            final V value;
            final AtomicReference<Node<K, V>> next;

            Node(K key, V value) {
                this.key = key;
                this.value = value;
                this.next = new AtomicReference<>(null);
            }
        }

        private final AtomicReferenceArray<Node<K, V>> buckets;

        public LockFreeHashMap(int capacity) {
            this.buckets = new AtomicReferenceArray<>(capacity);
        }

        private int hash(K key) {
            return Math.abs(key.hashCode() % buckets.length());
        }

        /**
         * TODO: Implement lock-free put
         *
         * Use CAS to add node to bucket
         */
        public V put(K key, V value) {
            int bucket = hash(key);
            Node<K, V> newNode = new Node<>(key, value);

            while (true) {
                Node<K, V> head = buckets.get(bucket);

                // TODO: Search for existing key
                Node<K, V> current = head;
                while (current != null) {
                    if (current.key.equals(key)) {
                        // Key exists - for simplicity, don't update
                        return current.value;
                    }
                    current = current.next.get();
                }

                // TODO: Try to CAS new node as head
                newNode.next.set(head);
                if (buckets.compareAndSet(bucket, head, newNode)) {
                    return null;
                }
            }
        }

        /**
         * TODO: Implement get
         */
        public V get(K key) {
            int bucket = hash(key);
            Node<K, V> current = buckets.get(bucket);

            // TODO: Search bucket for key
            while (current != null) {
                if (current.key.equals(key)) {
                    return current.value;
                }
                current = current.next.get();
            }
            return null;
        }
    }

    /**
     * TODO: Implement Cuckoo Hash Map
     *
     * Uses two hash functions and two tables
     * Item is in one of two possible locations
     */
    public static class CuckooHashMap<K, V> {
        private static class Entry<K, V> {
            final K key;
            V value;

            Entry(K key, V value) {
                this.key = key;
                this.value = value;
            }
        }

        private final AtomicReferenceArray<Entry<K, V>> table1;
        private final AtomicReferenceArray<Entry<K, V>> table2;
        private final int capacity;
        private static final int MAX_ITERATIONS = 100;

        public CuckooHashMap(int capacity) {
            this.capacity = capacity;
            this.table1 = new AtomicReferenceArray<>(capacity);
            this.table2 = new AtomicReferenceArray<>(capacity);
        }

        private int hash1(K key) {
            return Math.abs(key.hashCode() % capacity);
        }

        private int hash2(K key) {
            return Math.abs((key.hashCode() * 31) % capacity);
        }

        /**
         * TODO: Implement cuckoo put
         *
         * Try table1 first, if occupied, displace it to table2
         * If table2 occupied, displace back to table1, etc.
         */
        public synchronized boolean put(K key, V value) {
            // TODO: Check if key already exists
            if (get(key) != null) {
                return true; // Update not implemented for simplicity
            }

            Entry<K, V> entry = new Entry<>(key, value);

            // TODO: Implement cuckoo hashing displacement logic
            for (int i = 0; i < MAX_ITERATIONS; i++) {
                // Try table1
                int pos1 = hash1(entry.key);
                Entry<K, V> displaced = table1.getAndSet(pos1, entry);
                if (displaced == null) {
                    return true;
                }

                // Try table2
                entry = displaced;
                int pos2 = hash2(entry.key);
                displaced = table2.getAndSet(pos2, entry);
                if (displaced == null) {
                    return true;
                }

                entry = displaced;
            }

            // Failed to place after MAX_ITERATIONS
            return false;
        }

        /**
         * TODO: Implement get
         */
        public V get(K key) {
            // TODO: Check both possible locations
            int pos1 = hash1(key);
            Entry<K, V> entry = table1.get(pos1);
            if (entry != null && entry.key.equals(key)) {
                return entry.value;
            }

            int pos2 = hash2(key);
            entry = table2.get(pos2);
            if (entry != null && entry.key.equals(key)) {
                return entry.value;
            }

            return null;
        }
    }

    /**
     * Performance comparison
     */
    static class PerformanceTest {
        static void testMap(String name, Function<Integer, Void> putOp,
                           Function<Integer, Integer> getOp,
                           int numThreads, int opsPerThread)
                throws InterruptedException {

            Thread[] threads = new Thread[numThreads];
            long startTime = System.nanoTime();

            // Half puts, half gets
            for (int i = 0; i < numThreads; i++) {
                final int id = i;
                threads[i] = new Thread(() -> {
                    if (id % 2 == 0) {
                        // Putter
                        for (int j = 0; j < opsPerThread; j++) {
                            putOp.apply(id * opsPerThread + j);
                        }
                    } else {
                        // Getter
                        for (int j = 0; j < opsPerThread; j++) {
                            getOp.apply((id - 1) * opsPerThread + j);
                        }
                    }
                });
                threads[i].start();
            }

            for (Thread t : threads) {
                t.join();
            }

            long endTime = System.nanoTime();
            long duration = (endTime - startTime) / 1_000_000; // ms

            System.out.printf("%-25s: %6dms%n", name, duration);
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrent Hash Map Test ===\n");

        testCorrectness();
        System.out.println("\n=== Performance Comparison ===");
        comparePerformance();
    }

    private static void testCorrectness() {
        System.out.println("Testing Striped Hash Map:");
        StripedHashMap<Integer, String> map = new StripedHashMap<>(16, 4);

        map.put(1, "one");
        map.put(2, "two");
        map.put(17, "seventeen"); // Same bucket as 1

        System.out.println("get(1) = " + map.get(1));
        System.out.println("get(2) = " + map.get(2));
        System.out.println("get(17) = " + map.get(17));
        System.out.println("get(99) = " + map.get(99));

        System.out.println(map.get(1).equals("one") ? "✅ Correct" : "❌ Incorrect");

        System.out.println("\nTesting Cuckoo Hash Map:");
        CuckooHashMap<Integer, String> cuckoo = new CuckooHashMap<>(16);

        cuckoo.put(1, "one");
        cuckoo.put(2, "two");

        System.out.println("get(1) = " + cuckoo.get(1));
        System.out.println("get(2) = " + cuckoo.get(2));
        System.out.println(cuckoo.get(1).equals("one") ? "✅ Correct" : "❌ Incorrect");
    }

    private static void comparePerformance() throws InterruptedException {
        int numThreads = 8;
        int opsPerThread = 10000;

        System.out.println("Threads: " + numThreads + ", Operations per thread: " + opsPerThread);
        System.out.println();

        // Striped
        StripedHashMap<Integer, Integer> striped = new StripedHashMap<>(1024, numThreads);
        PerformanceTest.testMap("StripedHashMap",
            key -> striped.put(key, key),
            key -> striped.get(key),
            numThreads, opsPerThread);

        // Lock-Free
        LockFreeHashMap<Integer, Integer> lockFree = new LockFreeHashMap<>(1024);
        PerformanceTest.testMap("LockFreeHashMap",
            key -> lockFree.put(key, key),
            key -> lockFree.get(key),
            numThreads, opsPerThread);

        // ConcurrentHashMap (Java's built-in)
        java.util.concurrent.ConcurrentHashMap<Integer, Integer> concurrent =
            new java.util.concurrent.ConcurrentHashMap<>(1024);
        PerformanceTest.testMap("ConcurrentHashMap (JDK)",
            key -> concurrent.put(key, key),
            key -> concurrent.get(key),
            numThreads, opsPerThread);

        System.out.println("\n💡 Java's ConcurrentHashMap uses advanced techniques:");
        System.out.println("   - Lock striping with dynamic resizing");
        System.out.println("   - Optimistic reading without locks");
        System.out.println("   - CAS for low-contention updates");
    }
}
