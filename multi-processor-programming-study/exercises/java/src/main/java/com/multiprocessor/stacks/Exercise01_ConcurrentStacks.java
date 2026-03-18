package com.multiprocessor.stacks;

import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicReferenceArray;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Exercise: Concurrent Stacks
 *
 * CONCEPT: Lock-free and elimination-based concurrent stacks
 *
 * Stack implementations:
 * - Lock-based: Simple with global lock
 * - Lock-free: Treiber stack using CAS
 * - Elimination: Reduces contention by pairing operations
 *
 * LEARNING OBJECTIVES:
 * - Implement lock-free stack (Treiber algorithm)
 * - Understand elimination backoff optimization
 * - Compare performance under contention
 */
public class Exercise01_ConcurrentStacks {

    /**
     * TODO: Implement simple lock-based stack
     */
    public static class LockBasedStack<T> {
        private class Node {
            final T value;
            Node next;

            Node(T value) {
                this.value = value;
            }
        }

        private Node top = null;
        // TODO: Add lock

        /**
         * TODO: Implement synchronized push
         */
        public synchronized void push(T value) {
            // TODO: Implement
        }

        /**
         * TODO: Implement synchronized pop
         */
        public synchronized T pop() {
            // TODO: Implement
            return null;
        }
    }

    /**
     * TODO: Implement Lock-Free Stack (Treiber Stack)
     *
     * Classic lock-free stack using CAS
     * Simple and efficient under low contention
     */
    public static class LockFreeStack<T> {
        private class Node {
            final T value;
            final Node next;

            Node(T value, Node next) {
                this.value = value;
                this.next = next;
            }
        }

        // TODO: Add AtomicReference<Node> for top

        public LockFreeStack() {
            // TODO: Initialize top to null
        }

        /**
         * TODO: Implement lock-free push
         *
         * 1. Create new node
         * 2. Read current top
         * 3. Set node.next = top
         * 4. Try CAS(top, oldTop, node)
         * 5. Retry if CAS fails
         */
        public void push(T value) {
            // TODO: Implement Treiber push
        }

        /**
         * TODO: Implement lock-free pop
         *
         * 1. Read current top
         * 2. If null, return null
         * 3. Try CAS(top, oldTop, oldTop.next)
         * 4. If success, return oldTop.value
         * 5. Retry if CAS fails
         */
        public T pop() {
            // TODO: Implement Treiber pop
            return null;
        }
    }

    /**
     * TODO: Implement Elimination Backoff Stack
     *
     * Optimization: Pair push/pop operations to eliminate contention
     * Under high contention, operations can complete without accessing the stack!
     */
    public static class EliminationStack<T> {
        private class Node {
            final T value;
            final Node next;

            Node(T value, Node next) {
                this.value = value;
                this.next = next;
            }
        }

        private final AtomicReference<Node> top;
        private final EliminationArray<T> eliminationArray;

        public EliminationStack(int eliminationSize) {
            top = new AtomicReference<>(null);
            eliminationArray = new EliminationArray<>(eliminationSize);
        }

        /**
         * TODO: Implement push with elimination
         *
         * 1. Try normal push
         * 2. If CAS fails, try elimination
         */
        public void push(T value) {
            Node node = new Node(value, null);
            while (true) {
                // Try normal push
                Node oldTop = top.get();
                node.next = oldTop;
                if (top.compareAndSet(oldTop, node)) {
                    return;
                }

                // TODO: If contention, try elimination
                try {
                    T otherValue = eliminationArray.visit(value, true);
                    if (otherValue == null) {
                        // Eliminated with a pop!
                        return;
                    }
                } catch (TimeoutException e) {
                    // Continue to retry
                }
            }
        }

        /**
         * TODO: Implement pop with elimination
         */
        public T pop() {
            while (true) {
                // Try normal pop
                Node oldTop = top.get();
                if (oldTop == null) {
                    return null;
                }
                if (top.compareAndSet(oldTop, oldTop.next)) {
                    return oldTop.value;
                }

                // TODO: If contention, try elimination
                try {
                    T value = eliminationArray.visit(null, false);
                    if (value != null) {
                        // Eliminated with a push!
                        return value;
                    }
                } catch (TimeoutException e) {
                    // Continue to retry
                }
            }
        }
    }

    /**
     * Elimination Array for pairing operations
     */
    static class EliminationArray<T> {
        private final AtomicReferenceArray<Exchanger<T>> exchangers;
        private final int size;
        private static final int TIMEOUT_MS = 10;

        public EliminationArray(int size) {
            this.size = size;
            this.exchangers = new AtomicReferenceArray<>(size);
            for (int i = 0; i < size; i++) {
                exchangers.set(i, new Exchanger<>());
            }
        }

        /**
         * Try to exchange with another thread
         *
         * @param value value to exchange (null for pop)
         * @param isPush true if push, false if pop
         * @return exchanged value, or null if timeout
         */
        public T visit(T value, boolean isPush) throws TimeoutException {
            int slot = ThreadLocalRandom.current().nextInt(size);
            Exchanger<T> exchanger = exchangers.get(slot);
            return exchanger.exchange(value, TIMEOUT_MS);
        }
    }

    /**
     * Simple exchanger for elimination
     */
    static class Exchanger<T> {
        private enum State { EMPTY, WAITING, BUSY }

        private static class Slot<T> {
            volatile T value;
            volatile State state = State.EMPTY;
        }

        private final AtomicReference<Slot<T>> slot;

        public Exchanger() {
            this.slot = new AtomicReference<>(new Slot<>());
        }

        public T exchange(T myValue, long timeoutMs) throws TimeoutException {
            long startTime = System.currentTimeMillis();
            Slot<T> s = slot.get();

            while (true) {
                if (System.currentTimeMillis() - startTime > timeoutMs) {
                    throw new TimeoutException();
                }

                if (s.state == State.EMPTY) {
                    // Try to offer my value
                    s.value = myValue;
                    s.state = State.WAITING;

                    // Wait for exchange
                    while (System.currentTimeMillis() - startTime < timeoutMs) {
                        if (s.state == State.BUSY) {
                            T result = s.value;
                            s.state = State.EMPTY;
                            return result;
                        }
                        Thread.yield();
                    }
                    // Timeout, revert
                    s.state = State.EMPTY;
                    throw new TimeoutException();

                } else if (s.state == State.WAITING) {
                    // Try to exchange
                    T herValue = s.value;
                    s.value = myValue;
                    s.state = State.BUSY;
                    return herValue;
                }

                Thread.yield();
            }
        }
    }

    static class TimeoutException extends Exception {}

    /**
     * Performance comparison
     */
    static class PerformanceTest {
        static long testStack(String name, Runnable test) throws InterruptedException {
            long startTime = System.nanoTime();
            test.run();
            long endTime = System.nanoTime();
            long duration = (endTime - startTime) / 1_000_000; // ms
            System.out.printf("%25s: %6dms%n", name, duration);
            return duration;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrent Stacks Test ===\n");

        testCorrectness();
        System.out.println("\n=== Performance Comparison ===");
        comparePerformance();
    }

    private static void testCorrectness() throws InterruptedException {
        System.out.println("Testing correctness:");

        testOneStack("Lock-Based", new LockBasedStack<>());
        testOneStack("Lock-Free", new LockFreeStack<>());
        testOneStack("Elimination", new EliminationStack<>(10));
    }

    private static void testOneStack(String name, Object stack) throws InterruptedException {
        int numThreads = 10;
        int opsPerThread = 1000;

        // Push phase
        Thread[] pushers = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            pushers[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    if (stack instanceof LockBasedStack) {
                        ((LockBasedStack<Integer>) stack).push(id * opsPerThread + j);
                    } else if (stack instanceof LockFreeStack) {
                        ((LockFreeStack<Integer>) stack).push(id * opsPerThread + j);
                    } else if (stack instanceof EliminationStack) {
                        ((EliminationStack<Integer>) stack).push(id * opsPerThread + j);
                    }
                }
            });
            pushers[i].start();
        }

        for (Thread t : pushers) t.join();

        // Pop phase
        int[] popCounts = new int[numThreads];
        Thread[] poppers = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            poppers[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    Integer value = null;
                    if (stack instanceof LockBasedStack) {
                        value = ((LockBasedStack<Integer>) stack).pop();
                    } else if (stack instanceof LockFreeStack) {
                        value = ((LockFreeStack<Integer>) stack).pop();
                    } else if (stack instanceof EliminationStack) {
                        value = ((EliminationStack<Integer>) stack).pop();
                    }
                    if (value != null) {
                        popCounts[id]++;
                    }
                }
            });
            poppers[i].start();
        }

        for (Thread t : poppers) t.join();

        int totalPopped = 0;
        for (int count : popCounts) {
            totalPopped += count;
        }

        System.out.printf("%15s: Expected=%d, Actual=%d %s%n",
                         name, numThreads * opsPerThread, totalPopped,
                         totalPopped == numThreads * opsPerThread ? "✅" : "❌");
    }

    private static void comparePerformance() throws InterruptedException {
        int numThreads = 16;
        int opsPerThread = 50000;

        System.out.println("High contention (" + numThreads + " threads, " +
                          opsPerThread + " ops each):\n");

        // Lock-based
        PerformanceTest.testStack("Lock-Based Stack", () -> {
            LockBasedStack<Integer> stack = new LockBasedStack<>();
            try {
                runStackTest(stack, numThreads, opsPerThread);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        // Lock-free
        PerformanceTest.testStack("Lock-Free Stack", () -> {
            LockFreeStack<Integer> stack = new LockFreeStack<>();
            try {
                runStackTest(stack, numThreads, opsPerThread);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        // Elimination
        PerformanceTest.testStack("Elimination Stack", () -> {
            EliminationStack<Integer> stack = new EliminationStack<>(20);
            try {
                runStackTest(stack, numThreads, opsPerThread);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        System.out.println("\n💡 Elimination stack shines under high contention!");
        System.out.println("💡 Lock-free is simpler but suffers from CAS retries");
    }

    private static void runStackTest(Object stack, int numThreads, int opsPerThread)
            throws InterruptedException {
        Thread[] threads = new Thread[numThreads];

        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    if (stack instanceof LockBasedStack) {
                        LockBasedStack<Integer> s = (LockBasedStack<Integer>) stack;
                        s.push(j);
                        s.pop();
                    } else if (stack instanceof LockFreeStack) {
                        LockFreeStack<Integer> s = (LockFreeStack<Integer>) stack;
                        s.push(j);
                        s.pop();
                    } else if (stack instanceof EliminationStack) {
                        EliminationStack<Integer> s = (EliminationStack<Integer>) stack;
                        s.push(j);
                        s.pop();
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }
    }
}
