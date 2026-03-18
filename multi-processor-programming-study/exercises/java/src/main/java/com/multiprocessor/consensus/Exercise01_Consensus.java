package com.multiprocessor.consensus;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Exercise: Consensus and Universality
 *
 * CONCEPT: Consensus problem and its hierarchy
 *
 * Consensus Problem: Multiple threads propose values, must agree on one.
 * - Agreement: All decide on the same value
 * - Validity: Decided value must be proposed
 * - Wait-freedom: Every thread eventually decides
 *
 * Consensus Hierarchy:
 * - Atomic registers: consensus number 1
 * - Test-and-Set, Swap: consensus number 2
 * - CAS, LL/SC: consensus number ∞
 *
 * LEARNING OBJECTIVES:
 * - Understand the consensus problem
 * - Implement consensus using different primitives
 * - Learn about universality of consensus
 */
public class Exercise01_Consensus {

    /**
     * TODO: Implement consensus for 2 threads using atomic swap
     *
     * Consensus number of swap is 2 - can solve for 2 threads only
     */
    public static class TwoThreadConsensus<T> {
        // TODO: Add AtomicReference for the decision
        // HINT: Use AtomicReference<T>

        /**
         * TODO: Implement decide method
         *
         * @param value The value proposed by this thread
         * @return The consensus value (might be from this or other thread)
         */
        public T decide(T value) {
            // TODO: Use getAndSet (atomic swap)
            // If swap returns null, we won the race
            // Otherwise, return what was swapped in
            return null;
        }
    }

    /**
     * TODO: Implement consensus using Compare-and-Swap
     *
     * CAS has consensus number ∞ - can solve for any number of threads
     */
    public static class UniversalConsensus<T> {
        // TODO: Add AtomicReference<T> for decision

        public UniversalConsensus() {
            // TODO: Initialize to null (undecided state)
        }

        /**
         * TODO: Implement decide using CAS
         *
         * @param value The value proposed by this thread
         * @return The consensus value
         */
        public T decide(T value) {
            // TODO: Try CAS from null to value
            // If CAS succeeds, we won
            // If CAS fails, someone else won, return their value
            return null;
        }
    }

    /**
     * TODO: Implement a universal construction
     *
     * Using consensus, we can make any sequential object wait-free!
     * This is a simplified version.
     */
    public static class UniversalConstruction<T> {
        /**
         * Represents an invocation of a method
         */
        interface Invocation<T> {
            T apply(T state);
        }

        static class Node<T> {
            final Invocation<T> invocation;
            final AtomicReference<Node<T>> next;
            final int seq;

            Node(Invocation<T> inv, int seq) {
                this.invocation = inv;
                this.next = new AtomicReference<>(null);
                this.seq = seq;
            }
        }

        private final AtomicReference<Node<T>> tail;
        private final T initialState;

        public UniversalConstruction(T initialState) {
            this.initialState = initialState;
            this.tail = new AtomicReference<>(new Node<>(state -> state, 0));
        }

        /**
         * TODO: Implement universal apply
         *
         * This method allows any thread to apply any operation
         * in a wait-free manner using consensus
         */
        public T apply(Invocation<T> invocation) {
            // TODO: Create new node with invocation
            // TODO: Try to append to tail using CAS
            // TODO: Compute result by replaying all operations
            return null;
        }
    }

    /**
     * Test consensus with counter
     */
    static class ConsensusCounter {
        private final UniversalConsensus<Integer> consensus = new UniversalConsensus<>();
        private final AtomicInteger proposals = new AtomicInteger(0);

        public int propose() {
            int myValue = proposals.incrementAndGet();
            return consensus.decide(myValue);
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Consensus Test ===\n");

        testTwoThreadConsensus();
        testUniversalConsensus();
        demonstrateConsensusHierarchy();
    }

    private static void testTwoThreadConsensus() throws InterruptedException {
        System.out.println("Testing Two-Thread Consensus:");

        TwoThreadConsensus<String> consensus = new TwoThreadConsensus<>();
        String[] results = new String[2];

        Thread t1 = new Thread(() -> {
            results[0] = consensus.decide("Thread-1");
            System.out.println("Thread 1 decided: " + results[0]);
        });

        Thread t2 = new Thread(() -> {
            results[1] = consensus.decide("Thread-2");
            System.out.println("Thread 2 decided: " + results[1]);
        });

        t1.start();
        t2.start();
        t1.join();
        t2.join();

        System.out.println("Agreement: " + (results[0].equals(results[1]) ? "✅ YES" : "❌ NO"));
        System.out.println();
    }

    private static void testUniversalConsensus() throws InterruptedException {
        System.out.println("Testing Universal Consensus (n threads):");

        UniversalConsensus<Integer> consensus = new UniversalConsensus<>();
        int numThreads = 10;
        Integer[] results = new Integer[numThreads];

        Thread[] threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            threads[i] = new Thread(() -> {
                results[id] = consensus.decide(id);
                System.out.println("Thread " + id + " decided: " + results[id]);
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        // Check agreement
        boolean agreement = true;
        Integer firstDecision = results[0];
        for (Integer result : results) {
            if (!result.equals(firstDecision)) {
                agreement = false;
                break;
            }
        }

        System.out.println("Agreement: " + (agreement ? "✅ YES" : "❌ NO"));
        System.out.println("Consensus value: " + firstDecision);
        System.out.println();
    }

    private static void demonstrateConsensusHierarchy() {
        System.out.println("=== Consensus Hierarchy ===");
        System.out.println();
        System.out.println("Consensus Number:");
        System.out.println("  1: Atomic registers (read/write)");
        System.out.println("     - Can't solve consensus even for 2 threads");
        System.out.println();
        System.out.println("  2: Test-and-Set, Swap, Fetch-and-Add");
        System.out.println("     - Can solve consensus for 2 threads only");
        System.out.println();
        System.out.println("  ∞: Compare-and-Swap, Load-Linked/Store-Conditional");
        System.out.println("     - Can solve consensus for any number of threads");
        System.out.println();
        System.out.println("💡 Universality Theorem:");
        System.out.println("   Any object with consensus number n can implement");
        System.out.println("   any object for n threads in a wait-free manner!");
        System.out.println();
    }
}
