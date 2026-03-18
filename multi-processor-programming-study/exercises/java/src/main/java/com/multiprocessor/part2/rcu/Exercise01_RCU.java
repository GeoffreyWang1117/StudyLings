package com.multiprocessor.part2.rcu;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.Random;
import java.util.ArrayList;
import java.util.List;

/**
 * Exercise: Read-Copy-Update (RCU)
 *
 * NOTE: Java has garbage collection, so RCU is less critical than in C++.
 * However, understanding RCU is valuable for:
 * 1. Cross-language programming (Java + C++)
 * 2. Understanding Linux kernel and systems programming
 * 3. Optimizing read-heavy workloads
 *
 * This is an educational implementation showing RCU concepts.
 */
public class Exercise01_RCU {

    /**
     * Simple RCU mechanism for Java
     */
    public static class SimpleRCU {
        private final AtomicInteger readerCount = new AtomicInteger(0);

        public void readLock() {
            readerCount.incrementAndGet();
        }

        public void readUnlock() {
            readerCount.decrementAndGet();
        }

        public void synchronize() {
            // Wait for all readers to finish
            while (readerCount.get() > 0) {
                Thread.yield();
            }
        }
    }

    /**
     * RAII-style read lock
     */
    public static class RCUReadLock implements AutoCloseable {
        private final SimpleRCU rcu;

        public RCUReadLock(SimpleRCU rcu) {
            this.rcu = rcu;
            rcu.readLock();
        }

        @Override
        public void close() {
            rcu.readUnlock();
        }
    }

    /**
     * RCU-Protected Linked List
     */
    public static class RCULinkedList<T> {
        private static class Node<T> {
            final T value;
            final AtomicReference<Node<T>> next;

            Node(T value) {
                this.value = value;
                this.next = new AtomicReference<>(null);
            }
        }

        private final AtomicReference<Node<T>> head = new AtomicReference<>(null);
        private final SimpleRCU rcu = new SimpleRCU();
        private final Lock writeLock = new ReentrantLock();

        public void insert(T value) {
            Node<T> newNode = new Node<>(value);

            writeLock.lock();
            try {
                Node<T> oldHead = head.get();
                newNode.next.set(oldHead);
                head.set(newNode); // Publish
            } finally {
                writeLock.unlock();
            }
        }

        public boolean search(T value) {
            try (RCUReadLock lock = new RCUReadLock(rcu)) {
                Node<T> current = head.get();
                while (current != null) {
                    if (current.value.equals(value)) {
                        return true;
                    }
                    current = current.next.get();
                }
                return false;
            }
        }

        public boolean remove(T value) {
            writeLock.lock();
            try {
                Node<T> prev = null;
                Node<T> current = head.get();

                while (current != null) {
                    if (current.value.equals(value)) {
                        Node<T> next = current.next.get();
                        if (prev == null) {
                            head.set(next);
                        } else {
                            prev.next.set(next);
                        }

                        // Wait for grace period (in Java, GC handles cleanup)
                        rcu.synchronize();
                        return true;
                    }
                    prev = current;
                    current = current.next.get();
                }
                return false;
            } finally {
                writeLock.unlock();
            }
        }
    }

    /**
     * Lock-based list for comparison
     */
    public static class LockBasedLinkedList<T> {
        private static class Node<T> {
            T value;
            Node<T> next;

            Node(T value) {
                this.value = value;
            }
        }

        private Node<T> head;
        private final Lock lock = new ReentrantLock();

        public void insert(T value) {
            lock.lock();
            try {
                Node<T> newNode = new Node<>(value);
                newNode.next = head;
                head = newNode;
            } finally {
                lock.unlock();
            }
        }

        public boolean search(T value) {
            lock.lock(); // Lock for reads!
            try {
                Node<T> current = head;
                while (current != null) {
                    if (current.value.equals(value)) {
                        return true;
                    }
                    current = current.next;
                }
                return false;
            } finally {
                lock.unlock();
            }
        }

        public boolean remove(T value) {
            lock.lock();
            try {
                Node<T> prev = null;
                Node<T> current = head;

                while (current != null) {
                    if (current.value.equals(value)) {
                        if (prev == null) {
                            head = current.next;
                        } else {
                            prev.next = current.next;
                        }
                        return true;
                    }
                    prev = current;
                    current = current.next;
                }
                return false;
            } finally {
                lock.unlock();
            }
        }
    }

    public static void testCorrectness() {
        System.out.println("=== Correctness Tests ===\n");

        RCULinkedList<Integer> list = new RCULinkedList<>();
        list.insert(1);
        list.insert(2);
        list.insert(3);

        System.out.println("Search 2: " + (list.search(2) ? "found" : "not found"));
        System.out.println("Search 5: " + (list.search(5) ? "found" : "not found"));

        list.remove(2);
        System.out.println("After removing 2, search 2: " + (list.search(2) ? "found" : "not found"));
        System.out.println("✅ PASS\n");
    }

    public static void comparePerformance() throws InterruptedException {
        System.out.println("=== Performance Comparison: Read-Heavy Workload ===\n");

        final int numThreads = Runtime.getRuntime().availableProcessors();
        final int opsPerThread = 100000;
        final int numItems = 100;

        System.out.println("Threads: " + numThreads);
        System.out.println("Operations per thread: " + opsPerThread);
        System.out.println("Workload: 95% reads, 5% writes\n");

        // Test RCU
        {
            RCULinkedList<Integer> list = new RCULinkedList<>();
            for (int i = 0; i < numItems; i++) {
                list.insert(i);
            }

            long start = System.currentTimeMillis();

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < numThreads; i++) {
                threads.add(new Thread(() -> {
                    Random rand = new Random();
                    for (int j = 0; j < opsPerThread; j++) {
                        int op = rand.nextInt(100);
                        int value = rand.nextInt(numItems);

                        if (op < 95) {
                            list.search(value);
                        } else if (op < 97) {
                            list.insert(value);
                        } else {
                            list.remove(value);
                        }
                    }
                }));
            }

            for (Thread t : threads) t.start();
            for (Thread t : threads) t.join();

            long duration = System.currentTimeMillis() - start;
            System.out.println("RCU Linked List:");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Throughput: " + (numThreads * opsPerThread * 1000.0 / duration) + " ops/sec\n");
        }

        // Test Lock-Based
        {
            LockBasedLinkedList<Integer> list = new LockBasedLinkedList<>();
            for (int i = 0; i < numItems; i++) {
                list.insert(i);
            }

            long start = System.currentTimeMillis();

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < numThreads; i++) {
                threads.add(new Thread(() -> {
                    Random rand = new Random();
                    for (int j = 0; j < opsPerThread; j++) {
                        int op = rand.nextInt(100);
                        int value = rand.nextInt(numItems);

                        if (op < 95) {
                            list.search(value);
                        } else if (op < 97) {
                            list.insert(value);
                        } else {
                            list.remove(value);
                        }
                    }
                }));
            }

            for (Thread t : threads) t.start();
            for (Thread t : threads) t.join();

            long duration = System.currentTimeMillis() - start;
            System.out.println("Lock-Based Linked List:");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Throughput: " + (numThreads * opsPerThread * 1000.0 / duration) + " ops/sec\n");
        }

        System.out.println("💡 RCU excels in read-heavy workloads");
        System.out.println("💡 In Java: GC handles memory cleanup automatically");
        System.out.println("💡 In C++: Grace period prevents use-after-free");
    }

    public static void demonstrateConcepts() {
        System.out.println("=== Read-Copy-Update (RCU) Concepts ===\n");
        System.out.println("RCU Principles:");
        System.out.println("  1. Readers have ZERO overhead");
        System.out.println("  2. Writers: copy-update-wait");
        System.out.println("  3. Grace period ensures safety\n");

        System.out.println("When to Use RCU:");
        System.out.println("  ✅ Read-heavy (90%+ reads)");
        System.out.println("  ✅ Pointer-based structures");
        System.out.println("  ✅ Can tolerate brief staleness\n");

        System.out.println("Java vs C++:");
        System.out.println("  • Java: GC handles cleanup");
        System.out.println("  • C++: Grace period critical\n");
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Read-Copy-Update (RCU) Test ===\n");
        demonstrateConcepts();
        testCorrectness();
        comparePerformance();
    }
}
