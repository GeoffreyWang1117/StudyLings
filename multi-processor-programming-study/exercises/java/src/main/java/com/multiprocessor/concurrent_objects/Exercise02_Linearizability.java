package com.multiprocessor.concurrent_objects;

import java.util.concurrent.atomic.AtomicReference;

/**
 * Exercise: Linearizability
 *
 * CONCEPT: Linearizability - the gold standard for concurrent correctness
 *
 * Linearizability: Each operation appears to take effect instantaneously
 * at some point between its invocation and response (the linearization point).
 *
 * KEY PROPERTIES:
 * - Stronger than sequential consistency
 * - Respects real-time ordering
 * - Composable (linearizable objects compose to linearizable system)
 * - Local property (can verify objects in isolation)
 *
 * LEARNING OBJECTIVES:
 * - Understand linearizability and linearization points
 * - Implement linearizable data structures
 * - Identify linearization points in code
 */
public class Exercise02_Linearizability {

    /**
     * TODO: Implement a linearizable stack
     *
     * This stack should be linearizable:
     * - Each push/pop appears atomic at its linearization point
     * - Operations respect real-time ordering
     */
    public static class LinearizableStack<T> {
        private static class Node<T> {
            final T value;
            Node<T> next;

            Node(T value) {
                this.value = value;
            }
        }

        // TODO: Add necessary fields
        // HINT: Use AtomicReference for lock-free implementation
        private AtomicReference<Node<T>> top;

        public LinearizableStack() {
            // TODO: Initialize the stack
        }

        /**
         * TODO: Implement push operation
         *
         * The linearization point is the successful CAS operation
         *
         * @param value value to push
         */
        public void push(T value) {
            // TODO: Implement lock-free push using CAS
            // HINT: Create new node, set its next, CAS top
            // HINT: Retry on CAS failure
        }

        /**
         * TODO: Implement pop operation
         *
         * The linearization point is the successful CAS operation
         *
         * @return popped value, or null if empty
         */
        public T pop() {
            // TODO: Implement lock-free pop using CAS
            // HINT: Read top, if null return null
            // HINT: Try to CAS top to top.next
            // HINT: Retry on CAS failure
            return null;
        }

        /**
         * Check if stack is empty
         */
        public boolean isEmpty() {
            return top.get() == null;
        }
    }

    /**
     * TODO: Implement a linearizable counter with both increment and decrement
     */
    public static class LinearizableCounter {
        // TODO: Add necessary fields
        // HINT: Use AtomicInteger

        public LinearizableCounter(int initialValue) {
            // TODO: Initialize
        }

        /**
         * TODO: Implement atomic increment
         *
         * @return value AFTER increment
         */
        public int incrementAndGet() {
            // TODO: Implement this
            // HINT: Use compareAndSet in a loop
            return 0;
        }

        /**
         * TODO: Implement atomic decrement
         *
         * @return value AFTER decrement
         */
        public int decrementAndGet() {
            // TODO: Implement this
            return 0;
        }

        /**
         * TODO: Implement get
         */
        public int get() {
            // TODO: Implement this
            return 0;
        }
    }

    /**
     * TODO: Implement a linearizable swap operation
     *
     * This demonstrates a linearization point in a multi-step operation
     */
    public static class LinearizableSwap<T> {
        private AtomicReference<T> ref1;
        private AtomicReference<T> ref2;

        public LinearizableSwap(T initial1, T initial2) {
            ref1 = new AtomicReference<>(initial1);
            ref2 = new AtomicReference<>(initial2);
        }

        /**
         * TODO: Implement atomic swap of two references
         *
         * This is tricky! You need to ensure atomicity of swapping both references.
         * HINT: This might not be truly atomic without additional synchronization
         *
         * @return true if swap succeeded
         */
        public boolean swap() {
            // TODO: Implement this
            // Challenge: Can you make this linearizable?
            // Where is the linearization point?
            return false;
        }

        public T getFirst() {
            return ref1.get();
        }

        public T getSecond() {
            return ref2.get();
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Linearizability Test ===\n");

        testLinearizableStack();
        testLinearizableCounter();
    }

    private static void testLinearizableStack() throws InterruptedException {
        System.out.println("Testing Linearizable Stack:");

        LinearizableStack<Integer> stack = new LinearizableStack<>();
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
        int[] popCounts = new int[numThreads];
        Thread[] poppers = new Thread[numThreads];
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
        System.out.println("Stack empty: " + stack.isEmpty());
        System.out.println(totalPopped == numThreads * opsPerThread && stack.isEmpty() ?
                          "✅ PASS\n" : "❌ FAIL\n");
    }

    private static void testLinearizableCounter() throws InterruptedException {
        System.out.println("Testing Linearizable Counter:");

        LinearizableCounter counter = new LinearizableCounter(0);
        int numThreads = 10;
        int opsPerThread = 1000;

        Thread[] threads = new Thread[numThreads * 2];

        // Half increment, half decrement
        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    counter.incrementAndGet();
                }
            });

            threads[numThreads + i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    counter.decrementAndGet();
                }
            });
        }

        for (Thread t : threads) {
            t.start();
        }

        for (Thread t : threads) {
            t.join();
        }

        System.out.println("Expected final value: 0");
        System.out.println("Actual final value: " + counter.get());
        System.out.println(counter.get() == 0 ? "✅ PASS\n" : "❌ FAIL\n");
    }
}
