package com.multiprocessor.queues;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Exercise: Concurrent Queues
 *
 * CONCEPT: Producer-consumer queues with different synchronization strategies
 *
 * Queue types:
 * - Bounded Blocking: Fixed capacity, threads block when full/empty
 * - Unbounded Lock-Based: Dynamic capacity, uses locks
 * - Lock-Free: Michael-Scott queue using CAS
 * - Array-Based: Circular array, cache-friendly
 *
 * LEARNING OBJECTIVES:
 * - Implement blocking and non-blocking queues
 * - Handle the ABA problem
 * - Master the Michael-Scott algorithm
 */
public class Exercise01_ConcurrentQueues {

    /**
     * TODO: Implement Bounded Blocking Queue
     *
     * Fixed-size array-based queue with blocking
     * Threads block when queue is full (enqueue) or empty (dequeue)
     */
    public static class BoundedQueue<T> {
        private final T[] items;
        private int head = 0;
        private int tail = 0;
        private int size = 0;
        // TODO: Add lock and conditions
        // HINT: Use Lock, Condition for notFull and notEmpty

        @SuppressWarnings("unchecked")
        public BoundedQueue(int capacity) {
            items = (T[]) new Object[capacity];
            // TODO: Initialize lock and conditions
        }

        /**
         * TODO: Implement blocking enqueue
         *
         * Wait while full, then add item
         *
         * @param item item to enqueue
         * @throws InterruptedException if interrupted while waiting
         */
        public void enqueue(T item) throws InterruptedException {
            // TODO: Implement
            // Lock
            // While full: wait on notFull condition
            // Add item
            // Update tail and size
            // Signal notEmpty
            // Unlock
        }

        /**
         * TODO: Implement blocking dequeue
         *
         * Wait while empty, then remove item
         *
         * @return dequeued item
         * @throws InterruptedException if interrupted while waiting
         */
        public T dequeue() throws InterruptedException {
            // TODO: Implement
            // Lock
            // While empty: wait on notEmpty condition
            // Remove item
            // Update head and size
            // Signal notFull
            // Unlock
            return null;
        }

        public int size() {
            return size;
        }
    }

    /**
     * TODO: Implement Unbounded Lock-Based Queue
     *
     * Uses linked nodes, separate locks for head and tail
     * Better concurrency than single lock
     */
    public static class UnboundedQueue<T> {
        private class Node {
            T value;
            Node next;

            Node(T value) {
                this.value = value;
            }
        }

        private Node head;
        private Node tail;
        // TODO: Add separate locks for head and tail
        // HINT: enqLock for tail operations, deqLock for head operations

        public UnboundedQueue() {
            Node sentinel = new Node(null);
            head = sentinel;
            tail = sentinel;
            // TODO: Initialize locks
        }

        /**
         * TODO: Implement enqueue with tail lock
         *
         * Lock tail, add node, unlock
         */
        public void enqueue(T item) {
            Node node = new Node(item);
            // TODO: Lock tail
            // TODO: Add node
            // TODO: Update tail
            // TODO: Unlock
        }

        /**
         * TODO: Implement dequeue with head lock
         *
         * Lock head, remove node, unlock
         * Return null if empty
         */
        public T dequeue() {
            // TODO: Lock head
            // TODO: Check if queue is empty (head == tail)
            // TODO: If not empty, remove first real node
            // TODO: Update head
            // TODO: Unlock
            return null;
        }
    }

    /**
     * TODO: Implement Michael-Scott Lock-Free Queue
     *
     * Classic lock-free queue using CAS
     * Handles concurrent enqueue and dequeue operations
     */
    public static class LockFreeQueue<T> {
        private class Node {
            final T value;
            final AtomicReference<Node> next;

            Node(T value) {
                this.value = value;
                this.next = new AtomicReference<>(null);
            }
        }

        private final AtomicReference<Node> head;
        private final AtomicReference<Node> tail;

        public LockFreeQueue() {
            Node sentinel = new Node(null);
            head = new AtomicReference<>(sentinel);
            tail = new AtomicReference<>(sentinel);
        }

        /**
         * TODO: Implement lock-free enqueue
         *
         * Michael-Scott algorithm:
         * 1. Create new node
         * 2. Loop:
         *    a. Read tail and next
         *    b. If tail.next is null, try CAS it to new node
         *    c. If CAS succeeds, try to swing tail forward
         *    d. If tail.next not null, help other thread by swinging tail
         */
        public void enqueue(T item) {
            Node node = new Node(item);
            while (true) {
                Node last = tail.get();
                Node next = last.next.get();

                if (last == tail.get()) { // Consistency check
                    if (next == null) {
                        // TODO: Try to link new node
                        if (last.next.compareAndSet(next, node)) {
                            // TODO: Try to swing tail
                            tail.compareAndSet(last, node);
                            return;
                        }
                    } else {
                        // TODO: Help advance tail
                        tail.compareAndSet(last, next);
                    }
                }
            }
        }

        /**
         * TODO: Implement lock-free dequeue
         *
         * 1. Loop:
         *    a. Read head, tail, and first real node
         *    b. Check consistency
         *    c. If queue empty (head == tail), return null
         *    d. If tail falling behind, help advance it
         *    e. Try to swing head forward with CAS
         */
        public T dequeue() {
            while (true) {
                Node first = head.get();
                Node last = tail.get();
                Node next = first.next.get();

                if (first == head.get()) { // Consistency check
                    if (first == last) {
                        // Queue empty or tail falling behind
                        if (next == null) {
                            return null; // Empty
                        }
                        // TODO: Help advance tail
                        tail.compareAndSet(last, next);
                    } else {
                        // TODO: Read value before CAS
                        T value = next.value;
                        // TODO: Try to swing head forward
                        if (head.compareAndSet(first, next)) {
                            return value;
                        }
                    }
                }
            }
        }
    }

    /**
     * Demonstration of the ABA problem
     */
    public static class ABADemo {
        /**
         * The ABA problem:
         * - Thread 1 reads A
         * - Thread 2 changes A->B->A
         * - Thread 1's CAS succeeds but state changed
         *
         * Solutions:
         * - Version numbers (stamps)
         * - Hazard pointers
         * - Epoch-based reclamation
         */
        public static void demonstrate() {
            System.out.println("=== ABA Problem in Queues ===");
            System.out.println("Problem: Node reuse can cause ABA issues");
            System.out.println("Thread 1: Reads node A");
            System.out.println("Thread 2: Dequeues A, dequeues B, enqueues A (reused)");
            System.out.println("Thread 1: CAS succeeds, but A is different!");
            System.out.println();
            System.out.println("Solutions:");
            System.out.println("- Don't reuse nodes immediately");
            System.out.println("- Use version numbers with AtomicStampedReference");
            System.out.println("- Use hazard pointers or epoch-based reclamation");
            System.out.println();
        }
    }

    /**
     * Performance comparison
     */
    static class PerformanceTest {
        static void testQueue(String name, Runnable test) throws InterruptedException {
            long startTime = System.nanoTime();
            test.run();
            long endTime = System.nanoTime();
            long duration = (endTime - startTime) / 1_000_000; // ms
            System.out.printf("%20s: %6dms%n", name, duration);
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrent Queues Test ===\n");

        testBoundedQueue();
        testUnboundedQueue();
        testLockFreeQueue();
        ABADemo.demonstrate();
    }

    private static void testBoundedQueue() throws InterruptedException {
        System.out.println("Testing Bounded Queue:");

        BoundedQueue<Integer> queue = new BoundedQueue<>(100);
        int numProducers = 5;
        int numConsumers = 5;
        int itemsPerProducer = 1000;

        Thread[] producers = new Thread[numProducers];
        for (int i = 0; i < numProducers; i++) {
            final int id = i;
            producers[i] = new Thread(() -> {
                try {
                    for (int j = 0; j < itemsPerProducer; j++) {
                        queue.enqueue(id * itemsPerProducer + j);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            producers[i].start();
        }

        AtomicInteger consumedCount = new AtomicInteger(0);
        Thread[] consumers = new Thread[numConsumers];
        for (int i = 0; i < numConsumers; i++) {
            consumers[i] = new Thread(() -> {
                try {
                    for (int j = 0; j < itemsPerProducer; j++) {
                        Integer item = queue.dequeue();
                        if (item != null) {
                            consumedCount.incrementAndGet();
                        }
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            consumers[i].start();
        }

        for (Thread t : producers) t.join();
        for (Thread t : consumers) t.join();

        System.out.println("Produced: " + (numProducers * itemsPerProducer));
        System.out.println("Consumed: " + consumedCount.get());
        System.out.println(consumedCount.get() == numProducers * itemsPerProducer ?
                          "✅ PASS\n" : "❌ FAIL\n");
    }

    private static void testUnboundedQueue() throws InterruptedException {
        System.out.println("Testing Unbounded Queue:");

        UnboundedQueue<Integer> queue = new UnboundedQueue<>();
        int numThreads = 10;
        int itemsPerThread = 1000;

        // Enqueue phase
        Thread[] enqueuers = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            enqueuers[i] = new Thread(() -> {
                for (int j = 0; j < itemsPerThread; j++) {
                    queue.enqueue(id * itemsPerThread + j);
                }
            });
            enqueuers[i].start();
        }

        for (Thread t : enqueuers) t.join();

        // Dequeue phase
        AtomicInteger dequeueCount = new AtomicInteger(0);
        Thread[] dequeuers = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            dequeuers[i] = new Thread(() -> {
                for (int j = 0; j < itemsPerThread; j++) {
                    Integer item = queue.dequeue();
                    if (item != null) {
                        dequeueCount.incrementAndGet();
                    }
                }
            });
            dequeuers[i].start();
        }

        for (Thread t : dequeuers) t.join();

        System.out.println("Expected: " + (numThreads * itemsPerThread));
        System.out.println("Dequeued: " + dequeueCount.get());
        System.out.println(dequeueCount.get() == numThreads * itemsPerThread ?
                          "✅ PASS\n" : "❌ FAIL\n");
    }

    private static void testLockFreeQueue() throws InterruptedException {
        System.out.println("Testing Lock-Free Queue:");

        LockFreeQueue<Integer> queue = new LockFreeQueue<>();
        int numThreads = 10;
        int itemsPerThread = 1000;

        // Mixed operations
        Thread[] threads = new Thread[numThreads * 2];

        // Half enqueue
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < itemsPerThread; j++) {
                    queue.enqueue(id * itemsPerThread + j);
                }
            });
        }

        // Half dequeue
        AtomicInteger dequeueCount = new AtomicInteger(0);
        for (int i = 0; i < numThreads; i++) {
            threads[numThreads + i] = new Thread(() -> {
                for (int j = 0; j < itemsPerThread; j++) {
                    Integer item = queue.dequeue();
                    if (item != null) {
                        dequeueCount.incrementAndGet();
                    }
                }
            });
        }

        for (Thread t : threads) t.start();
        for (Thread t : threads) t.join();

        System.out.println("Enqueued: " + (numThreads * itemsPerThread));
        System.out.println("Dequeued: " + dequeueCount.get());
        System.out.println(dequeueCount.get() <= numThreads * itemsPerThread ?
                          "✅ PASS (some items may remain in queue)\n" : "❌ FAIL\n");
    }
}
