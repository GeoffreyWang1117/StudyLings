package com.multiprocessor.synchronization;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Exercise: Compare-and-Swap (CAS)
 *
 * CONCEPT: CAS is a fundamental synchronization primitive
 *
 * CAS(location, expected, new):
 *   if location == expected:
 *       location = new
 *       return true
 *   else:
 *       return false
 *
 * Properties:
 * - Atomic operation (hardware supported)
 * - Consensus number: ∞ (can solve consensus for any number of threads)
 * - Foundation for lock-free algorithms
 *
 * LEARNING OBJECTIVES:
 * - Master CAS-based programming
 * - Implement lock-free data structures using CAS
 * - Understand ABA problem
 */
public class Exercise01_CompareAndSwap {

    /**
     * TODO: Implement a lock-free counter using CAS
     */
    public static class CASCounter {
        // TODO: Add AtomicInteger field

        public CASCounter(int initialValue) {
            // TODO: Initialize
        }

        /**
         * TODO: Implement increment using CAS loop
         *
         * Pattern:
         * 1. Read current value
         * 2. Compute new value
         * 3. Try CAS
         * 4. If failed, retry
         *
         * @return value AFTER increment
         */
        public int incrementAndGet() {
            // TODO: Implement CAS loop
            // HINT: while(!compareAndSet(expected, expected+1)) { update expected }
            return 0;
        }

        /**
         * TODO: Implement add using CAS
         *
         * @param delta amount to add
         * @return value AFTER addition
         */
        public int addAndGet(int delta) {
            // TODO: Implement CAS loop
            return 0;
        }

        public int get() {
            // TODO: Implement
            return 0;
        }
    }

    /**
     * TODO: Implement a lock-free stack using CAS
     *
     * This is the Treiber Stack algorithm
     */
    public static class CASStack<T> {
        private static class Node<T> {
            final T value;
            final Node<T> next;

            Node(T value, Node<T> next) {
                this.value = value;
                this.next = next;
            }
        }

        // TODO: Add AtomicReference<Node<T>> for top

        public CASStack() {
            // TODO: Initialize
        }

        /**
         * TODO: Implement lock-free push using CAS
         *
         * @param value value to push
         */
        public void push(T value) {
            // TODO: Implement CAS loop
            // 1. Create new node
            // 2. Read current top
            // 3. Set node.next = top
            // 4. CAS top from oldTop to node
            // 5. Retry if CAS fails
        }

        /**
         * TODO: Implement lock-free pop using CAS
         *
         * @return popped value, or null if empty
         */
        public T pop() {
            // TODO: Implement CAS loop
            // 1. Read current top
            // 2. If null, return null
            // 3. Try CAS top from top to top.next
            // 4. If success, return top.value
            // 5. Retry if CAS fails
            return null;
        }
    }

    /**
     * TODO: Implement a lock-free queue using CAS
     *
     * This is simplified Michael-Scott queue
     */
    public static class CASQueue<T> {
        private static class Node<T> {
            final T value;
            final AtomicReference<Node<T>> next;

            Node(T value) {
                this.value = value;
                this.next = new AtomicReference<>(null);
            }
        }

        // TODO: Add AtomicReference<Node<T>> for head and tail

        public CASQueue() {
            // TODO: Initialize with dummy node
            // HINT: Both head and tail point to dummy initially
        }

        /**
         * TODO: Implement lock-free enqueue
         *
         * @param value value to enqueue
         */
        public void enqueue(T value) {
            // TODO: Implement using CAS
            // HINT: This is tricky! Need to handle tail lag
            // 1. Create new node
            // 2. Loop:
            //    a. Read tail and tail.next
            //    b. If tail.next is null, try to CAS it to new node
            //    c. If successful, try to CAS tail
            //    d. If tail.next not null, try to advance tail
        }

        /**
         * TODO: Implement lock-free dequeue
         *
         * @return dequeued value, or null if empty
         */
        public T dequeue() {
            // TODO: Implement using CAS
            // HINT: Skip dummy node
            return null;
        }
    }

    /**
     * Demonstration of the ABA problem
     */
    public static class ABADemo {
        static class Node {
            String value;
            Node next;

            Node(String value) {
                this.value = value;
            }
        }

        /**
         * TODO: Demonstrate the ABA problem
         *
         * The ABA problem occurs when:
         * 1. Thread 1 reads value A
         * 2. Thread 2 changes A to B then back to A
         * 3. Thread 1's CAS succeeds even though value changed
         *
         * This can cause issues in lock-free data structures
         */
        public static void demonstrateABA() {
            System.out.println("=== ABA Problem Demonstration ===");
            // TODO: Create a scenario showing ABA problem
            // HINT: Use AtomicReference with Node objects
            System.out.println("💡 ABA problem can cause memory reclamation issues");
            System.out.println("💡 Solutions: version numbers, hazard pointers, epoch-based reclamation\n");
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Compare-and-Swap Test ===\n");

        testCASCounter();
        testCASStack();
        ABADemo.demonstrateABA();
    }

    private static void testCASCounter() throws InterruptedException {
        System.out.println("Testing CAS Counter:");

        CASCounter counter = new CASCounter(0);
        int numThreads = 10;
        int opsPerThread = 1000;

        Thread[] threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    counter.incrementAndGet();
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        int expected = numThreads * opsPerThread;
        int actual = counter.get();

        System.out.println("Expected: " + expected);
        System.out.println("Actual: " + actual);
        System.out.println(actual == expected ? "✅ PASS\n" : "❌ FAIL\n");
    }

    private static void testCASStack() throws InterruptedException {
        System.out.println("Testing CAS Stack:");

        CASStack<Integer> stack = new CASStack<>();
        int numThreads = 10;
        int opsPerThread = 1000;

        // Push phase
        Thread[] pushers = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            pushers[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    stack.push(threadId * opsPerThread + j);
                }
            });
            pushers[i].start();
        }

        for (Thread t : pushers) {
            t.join();
        }

        // Pop phase
        Thread[] poppers = new Thread[numThreads];
        int[] popCounts = new int[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            poppers[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    Integer value = stack.pop();
                    if (value != null) {
                        popCounts[threadId]++;
                    }
                }
            });
            poppers[i].start();
        }

        for (Thread t : poppers) {
            t.join();
        }

        int totalPopped = 0;
        for (int count : popCounts) {
            totalPopped += count;
        }

        System.out.println("Expected pops: " + (numThreads * opsPerThread));
        System.out.println("Actual pops: " + totalPopped);
        System.out.println(totalPopped == numThreads * opsPerThread ? "✅ PASS\n" : "❌ FAIL\n");
    }
}
