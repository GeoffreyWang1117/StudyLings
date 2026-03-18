package com.multiprocessor.linked_lists;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.atomic.AtomicMarkableReference;

/**
 * Exercise: Concurrent Linked Lists
 *
 * CONCEPT: Different synchronization strategies for linked lists
 *
 * Strategies (from coarse to fine-grained):
 * 1. Coarse-grained: Single lock for entire list
 * 2. Fine-grained: Lock per node, hand-over-hand locking
 * 3. Optimistic: Lock-free traversal, lock for modification
 * 4. Lazy: Mark-then-delete with validation
 * 5. Lock-free: CAS-based, no locks
 *
 * LEARNING OBJECTIVES:
 * - Implement different concurrent list algorithms
 * - Understand trade-offs between simplicity and performance
 * - Master hand-over-hand locking and optimistic techniques
 */
public class Exercise01_ConcurrentLists {

    /**
     * TODO: Implement Coarse-Grained Locking List
     *
     * Simple: One lock protects entire list
     * Low concurrency but correct and simple
     */
    public static class CoarseList<T> {
        private class Node {
            T item;
            int key;
            Node next;

            Node(int key) {
                this.key = key;
            }

            Node(T item) {
                this.item = item;
                this.key = item.hashCode();
            }
        }

        private Node head;
        // TODO: Add a lock to protect the entire list
        // HINT: Use ReentrantLock

        public CoarseList() {
            head = new Node(Integer.MIN_VALUE);
            head.next = new Node(Integer.MAX_VALUE);
            // TODO: Initialize lock
        }

        /**
         * TODO: Implement add with coarse-grained locking
         *
         * @param item item to add
         * @return true if added, false if already present
         */
        public boolean add(T item) {
            Node node = new Node(item);
            // TODO: Lock entire list
            // TODO: Find position and insert
            // TODO: Unlock
            return false;
        }

        /**
         * TODO: Implement remove with coarse-grained locking
         *
         * @param item item to remove
         * @return true if removed, false if not found
         */
        public boolean remove(T item) {
            // TODO: Implement
            return false;
        }

        /**
         * TODO: Implement contains
         */
        public boolean contains(T item) {
            // TODO: Implement
            return false;
        }
    }

    /**
     * TODO: Implement Fine-Grained Locking List
     *
     * Lock per node, use hand-over-hand locking
     * Better concurrency than coarse-grained
     */
    public static class FineList<T> {
        private class Node {
            T item;
            int key;
            Node next;
            Lock lock = new ReentrantLock();

            Node(int key) {
                this.key = key;
            }

            Node(T item) {
                this.item = item;
                this.key = item.hashCode();
            }

            void lock() {
                lock.lock();
            }

            void unlock() {
                lock.unlock();
            }
        }

        private final Node head;

        public FineList() {
            head = new Node(Integer.MIN_VALUE);
            head.next = new Node(Integer.MAX_VALUE);
        }

        /**
         * TODO: Implement add with fine-grained locking
         *
         * Use hand-over-hand locking:
         * 1. Lock head
         * 2. Lock next node
         * 3. Unlock previous
         * 4. Repeat until found position
         * 5. Insert and unlock
         */
        public boolean add(T item) {
            // TODO: Implement hand-over-hand locking
            int key = item.hashCode();
            head.lock();
            Node pred = head;
            try {
                Node curr = pred.next;
                curr.lock();
                try {
                    // TODO: Traverse with hand-over-hand
                    // TODO: Insert node
                    return false;
                } finally {
                    curr.unlock();
                }
            } finally {
                pred.unlock();
            }
        }

        /**
         * TODO: Implement remove with fine-grained locking
         */
        public boolean remove(T item) {
            // TODO: Implement
            return false;
        }

        /**
         * TODO: Implement contains
         *
         * Question: Does contains need to lock?
         */
        public boolean contains(T item) {
            // TODO: Implement
            return false;
        }
    }

    /**
     * TODO: Implement Optimistic List
     *
     * Lock-free traversal, lock only for modification
     * Validate before modifying
     */
    public static class OptimisticList<T> {
        private class Node {
            T item;
            int key;
            Node next;
            Lock lock = new ReentrantLock();

            Node(int key) {
                this.key = key;
            }

            Node(T item) {
                this.item = item;
                this.key = item.hashCode();
            }

            void lock() { lock.lock(); }
            void unlock() { lock.unlock(); }
        }

        private final Node head;

        public OptimisticList() {
            head = new Node(Integer.MIN_VALUE);
            head.next = new Node(Integer.MAX_VALUE);
        }

        /**
         * TODO: Implement validate
         *
         * Check that pred still points to curr
         * and both are still reachable from head
         */
        private boolean validate(Node pred, Node curr) {
            // TODO: Traverse from head to check reachability
            Node node = head;
            while (node.key <= pred.key) {
                if (node == pred) {
                    return pred.next == curr;
                }
                node = node.next;
            }
            return false;
        }

        /**
         * TODO: Implement add with optimistic locking
         *
         * 1. Traverse without locking
         * 2. Lock pred and curr
         * 3. Validate
         * 4. If valid, insert; else retry
         */
        public boolean add(T item) {
            int key = item.hashCode();
            while (true) {
                // TODO: Find position without locking
                Node pred = head;
                Node curr = pred.next;
                while (curr.key < key) {
                    pred = curr;
                    curr = curr.next;
                }

                // TODO: Lock and validate
                pred.lock();
                try {
                    curr.lock();
                    try {
                        if (validate(pred, curr)) {
                            if (curr.key == key) {
                                return false; // Already present
                            } else {
                                // TODO: Insert new node
                                Node node = new Node(item);
                                node.next = curr;
                                pred.next = node;
                                return true;
                            }
                        }
                    } finally {
                        curr.unlock();
                    }
                } finally {
                    pred.unlock();
                }
                // Validation failed, retry
            }
        }

        /**
         * TODO: Implement remove
         */
        public boolean remove(T item) {
            // TODO: Similar to add, but remove node
            return false;
        }

        /**
         * TODO: Implement contains
         *
         * Can traverse without locking!
         */
        public boolean contains(T item) {
            int key = item.hashCode();
            Node curr = head;
            while (curr.key < key) {
                curr = curr.next;
            }
            return curr.key == key && curr.item != null;
        }
    }

    /**
     * TODO: Implement Lazy List
     *
     * Logical deletion: mark node as deleted, then physically remove
     * Simpler validation than optimistic
     */
    public static class LazyList<T> {
        private class Node {
            T item;
            int key;
            Node next;
            Lock lock = new ReentrantLock();
            volatile boolean marked = false; // Logical deletion flag

            Node(int key) {
                this.key = key;
            }

            Node(T item) {
                this.item = item;
                this.key = item.hashCode();
            }

            void lock() { lock.lock(); }
            void unlock() { lock.unlock(); }
        }

        private final Node head;

        public LazyList() {
            head = new Node(Integer.MIN_VALUE);
            head.next = new Node(Integer.MAX_VALUE);
        }

        /**
         * TODO: Implement validate
         *
         * Check that neither node is marked and pred points to curr
         */
        private boolean validate(Node pred, Node curr) {
            // TODO: Check !pred.marked && !curr.marked && pred.next == curr
            return !pred.marked && !curr.marked && pred.next == curr;
        }

        /**
         * TODO: Implement add
         */
        public boolean add(T item) {
            int key = item.hashCode();
            while (true) {
                Node pred = head;
                Node curr = pred.next;

                // Traverse (skip marked nodes)
                while (curr.key < key) {
                    pred = curr;
                    curr = curr.next;
                }

                pred.lock();
                try {
                    curr.lock();
                    try {
                        if (validate(pred, curr)) {
                            if (curr.key == key) {
                                return false;
                            } else {
                                // TODO: Insert new node
                                Node node = new Node(item);
                                node.next = curr;
                                pred.next = node;
                                return true;
                            }
                        }
                    } finally {
                        curr.unlock();
                    }
                } finally {
                    pred.unlock();
                }
            }
        }

        /**
         * TODO: Implement remove with lazy deletion
         *
         * 1. Find node
         * 2. Lock pred and curr
         * 3. Validate
         * 4. Mark curr as deleted (logical)
         * 5. Unlink curr (physical)
         */
        public boolean remove(T item) {
            int key = item.hashCode();
            while (true) {
                Node pred = head;
                Node curr = pred.next;

                while (curr.key < key) {
                    pred = curr;
                    curr = curr.next;
                }

                pred.lock();
                try {
                    curr.lock();
                    try {
                        if (validate(pred, curr)) {
                            if (curr.key != key) {
                                return false;
                            } else {
                                // TODO: Mark as deleted
                                curr.marked = true;
                                // TODO: Physical deletion
                                pred.next = curr.next;
                                return true;
                            }
                        }
                    } finally {
                        curr.unlock();
                    }
                } finally {
                    pred.unlock();
                }
            }
        }

        /**
         * TODO: Implement contains
         */
        public boolean contains(T item) {
            int key = item.hashCode();
            Node curr = head;
            while (curr.key < key) {
                curr = curr.next;
            }
            return curr.key == key && !curr.marked;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrent Linked Lists Test ===\n");

        testList("Coarse-Grained", new CoarseList<Integer>());
        testList("Fine-Grained", new FineList<Integer>());
        testList("Optimistic", new OptimisticList<Integer>());
        testList("Lazy", new LazyList<Integer>());
    }

    interface ConcurrentList<T> {
        boolean add(T item);
        boolean remove(T item);
        boolean contains(T item);
    }

    private static void testList(String name, Object list) throws InterruptedException {
        System.out.println("Testing " + name + " List:");

        int numThreads = 8;
        int opsPerThread = 1000;

        Thread[] threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    int value = threadId * opsPerThread + j;
                    if (list instanceof CoarseList) {
                        ((CoarseList<Integer>) list).add(value);
                        ((CoarseList<Integer>) list).contains(value);
                        if (j % 2 == 0) ((CoarseList<Integer>) list).remove(value);
                    } else if (list instanceof FineList) {
                        ((FineList<Integer>) list).add(value);
                        ((FineList<Integer>) list).contains(value);
                        if (j % 2 == 0) ((FineList<Integer>) list).remove(value);
                    } else if (list instanceof OptimisticList) {
                        ((OptimisticList<Integer>) list).add(value);
                        ((OptimisticList<Integer>) list).contains(value);
                        if (j % 2 == 0) ((OptimisticList<Integer>) list).remove(value);
                    } else if (list instanceof LazyList) {
                        ((LazyList<Integer>) list).add(value);
                        ((LazyList<Integer>) list).contains(value);
                        if (j % 2 == 0) ((LazyList<Integer>) list).remove(value);
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        System.out.println("✅ " + name + " list test completed\n");
    }
}
