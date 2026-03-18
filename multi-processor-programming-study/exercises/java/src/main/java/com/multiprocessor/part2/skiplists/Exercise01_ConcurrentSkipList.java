package com.multiprocessor.part2.skiplists;

import java.util.concurrent.atomic.AtomicMarkableReference;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Exercise: Concurrent Skip List
 *
 * CONCEPT: Lock-free concurrent skip list
 *
 * Skip List Properties:
 * - Probabilistic balanced search structure
 * - O(log n) search, insert, delete expected time
 * - Easier to implement than balanced trees
 *
 * Concurrent Skip List:
 * - Lock-free using CAS
 * - Lazy deletion with marking
 * - Multiple levels for fast search
 *
 * LEARNING OBJECTIVES:
 * - Implement lock-free skip list
 * - Handle concurrent search/insert/delete
 * - Use probabilistic level generation
 * - Implement lazy deletion pattern
 */
public class Exercise01_ConcurrentSkipList {

    /**
     * TODO: Implement Lock-Free Skip List
     */
    public static class LockFreeSkipList<T extends Comparable<T>> {
        static final int MAX_LEVEL = 32;
        private final Node<T> head;
        private final Node<T> tail;

        static class Node<T> {
            final T value;
            final AtomicMarkableReference<Node<T>>[] next;
            final int topLevel;

            @SuppressWarnings("unchecked")
            public Node(T value, int height) {
                this.value = value;
                this.topLevel = height;
                this.next = new AtomicMarkableReference[height + 1];
                for (int i = 0; i <= height; i++) {
                    next[i] = new AtomicMarkableReference<>(null, false);
                }
            }

            // Sentinel constructor
            @SuppressWarnings("unchecked")
            public Node(int height) {
                this.value = null;
                this.topLevel = height;
                this.next = new AtomicMarkableReference[height + 1];
                for (int i = 0; i <= height; i++) {
                    next[i] = new AtomicMarkableReference<>(null, false);
                }
            }
        }

        public LockFreeSkipList() {
            head = new Node<>(MAX_LEVEL);
            tail = new Node<>(MAX_LEVEL);
            for (int i = 0; i <= MAX_LEVEL; i++) {
                head.next[i] = new AtomicMarkableReference<>(tail, false);
            }
        }

        /**
         * TODO: Generate random level
         *
         * Higher levels are exponentially less likely
         */
        private int randomLevel() {
            int level = 0;
            while (level < MAX_LEVEL &&
                   ThreadLocalRandom.current().nextBoolean()) {
                level++;
            }
            return level;
        }

        /**
         * TODO: Find predecessors and successors at all levels
         *
         * This is the core search operation
         */
        @SuppressWarnings("unchecked")
        private boolean find(T value, Node<T>[] preds, Node<T>[] succs) {
            // TODO: Start from head at highest level
            // TODO: For each level from top to bottom:
            //   - Move forward while current < value
            //   - Skip marked nodes
            //   - Record predecessor and successor
            // TODO: Return true if value found
            return false;
        }

        /**
         * TODO: Implement add
         *
         * Use find to locate position, then CAS to insert
         */
        public boolean add(T value) {
            int topLevel = randomLevel();
            @SuppressWarnings("unchecked")
            Node<T>[] preds = (Node<T>[]) new Node[MAX_LEVEL + 1];
            @SuppressWarnings("unchecked")
            Node<T>[] succs = (Node<T>[]) new Node[MAX_LEVEL + 1];

            while (true) {
                // TODO: Find position
                boolean found = find(value, preds, succs);
                if (found) {
                    return false; // Already exists
                }

                // TODO: Create new node
                Node<T> newNode = new Node<>(value, topLevel);

                // TODO: Link node at all levels using CAS
                // Start from bottom level
                for (int level = 0; level <= topLevel; level++) {
                    Node<T> succ = succs[level];
                    newNode.next[level].set(succ, false);
                }

                // TODO: Try to CAS at bottom level
                Node<T> pred = preds[0];
                Node<T> succ = succs[0];
                newNode.next[0].set(succ, false);
                if (!pred.next[0].compareAndSet(succ, newNode, false, false)) {
                    continue; // Retry
                }

                // TODO: Link at upper levels
                for (int level = 1; level <= topLevel; level++) {
                    while (true) {
                        pred = preds[level];
                        succ = succs[level];
                        if (pred.next[level].compareAndSet(succ, newNode, false, false)) {
                            break;
                        }
                        find(value, preds, succs);
                    }
                }
                return true;
            }
        }

        /**
         * TODO: Implement remove with lazy deletion
         *
         * Mark node as deleted, then physically remove
         */
        public boolean remove(T value) {
            @SuppressWarnings("unchecked")
            Node<T>[] preds = (Node<T>[]) new Node[MAX_LEVEL + 1];
            @SuppressWarnings("unchecked")
            Node<T>[] succs = (Node<T>[]) new Node[MAX_LEVEL + 1];

            while (true) {
                boolean found = find(value, preds, succs);
                if (!found) {
                    return false;
                }

                // TODO: Mark node as deleted from top to bottom
                Node<T> victim = succs[0];

                // Mark from top down
                for (int level = victim.topLevel; level >= 1; level--) {
                    boolean[] marked = {false};
                    Node<T> succ = victim.next[level].get(marked);
                    while (!marked[0]) {
                        victim.next[level].compareAndSet(succ, succ, false, true);
                        succ = victim.next[level].get(marked);
                    }
                }

                // TODO: Mark bottom level
                boolean[] marked = {false};
                Node<T> succ = victim.next[0].get(marked);
                while (true) {
                    boolean iMarkedIt = victim.next[0].compareAndSet(succ, succ, false, true);
                    succ = victim.next[0].get(marked);
                    if (iMarkedIt) {
                        // Try to physically remove
                        find(value, preds, succs);
                        return true;
                    } else if (marked[0]) {
                        return false;
                    }
                }
            }
        }

        /**
         * TODO: Implement contains
         */
        public boolean contains(T value) {
            @SuppressWarnings("unchecked")
            Node<T>[] preds = (Node<T>[]) new Node[MAX_LEVEL + 1];
            @SuppressWarnings("unchecked")
            Node<T>[] succs = (Node<T>[]) new Node[MAX_LEVEL + 1];
            return find(value, preds, succs);
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrent Skip List Test ===\n");

        testBasicOperations();
        testConcurrentOperations();
    }

    private static void testBasicOperations() {
        System.out.println("Testing Basic Operations:");

        LockFreeSkipList<Integer> list = new LockFreeSkipList<>();

        // Add elements
        for (int i = 0; i < 10; i++) {
            list.add(i * 10);
        }

        // Test contains
        System.out.println("Contains 50: " + list.contains(50));
        System.out.println("Contains 55: " + list.contains(55));

        // Remove element
        System.out.println("Remove 50: " + list.remove(50));
        System.out.println("Contains 50 after removal: " + list.contains(50));

        System.out.println("✅ Basic operations test completed\n");
    }

    private static void testConcurrentOperations() throws InterruptedException {
        System.out.println("Testing Concurrent Operations:");

        LockFreeSkipList<Integer> list = new LockFreeSkipList<>();
        int numThreads = 8;
        int opsPerThread = 1000;

        Thread[] threads = new Thread[numThreads];

        // Mixed operations
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    int value = id * opsPerThread + j;
                    list.add(value);

                    if (j % 10 == 0) {
                        list.contains(value);
                    }

                    if (j % 2 == 0) {
                        list.remove(value);
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        System.out.println("✅ Concurrent operations test completed");
        System.out.println("💡 Skip list provides O(log n) operations with high concurrency");
    }
}
