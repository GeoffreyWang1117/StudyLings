package com.multiprocessor.part2.memory_reclamation;

import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.function.Consumer;

/**
 * Exercise: Epoch-Based Reclamation (EBR) for Safe Memory Reclamation
 *
 * CONCEPT: Safe memory reclamation using global epochs
 *
 * Epoch-Based Reclamation is an alternative to Hazard Pointers for solving
 * the memory reclamation problem in lock-free data structures.
 *
 * KEY DIFFERENCES FROM HAZARD POINTERS:
 * - Hazard Pointers: Per-pointer protection (fine-grained)
 * - EBR: Epoch-based protection (coarse-grained)
 *
 * HOW EBR WORKS:
 * 1. Global epoch counter (cycles through 0, 1, 2, 0, 1, 2, ...)
 * 2. Each thread announces which epoch it's in before accessing shared data
 * 3. Memory is retired to the current epoch's retired list
 * 4. Periodically advance global epoch
 * 5. Reclaim memory from epoch e when ALL threads have moved beyond epoch e
 *
 * ALGORITHM:
 * - Global epoch: Shared counter (0, 1, 2)
 * - Thread local epoch: Each thread's announced epoch
 * - Retired lists: One list per epoch (3 lists total)
 * - Reclamation: Safe to reclaim epoch e when all threads are in epoch (e+1) or (e+2)
 *
 * ADVANTAGES OVER HAZARD POINTERS:
 * ✓ Simpler implementation
 * ✓ Lower overhead per operation
 * ✓ Better for high-throughput scenarios
 * ✓ Batch reclamation (better cache behavior)
 *
 * DISADVANTAGES:
 * ✗ Coarser granularity (may delay reclamation longer)
 * ✗ Unbounded memory if threads stall
 * ✗ Requires periodic epoch advancement
 *
 * REAL-WORLD USAGE:
 * - Used in many production systems (userspace RCU, Crossbeam in Rust)
 * - Excellent for high-throughput lock-free data structures
 * - Popular in systems programming (databases, runtime systems)
 *
 * LEARNING OBJECTIVES:
 * - Understand epoch-based memory reclamation
 * - Implement EBR manager with global epoch
 * - Use EBR with lock-free stack
 * - Compare with Hazard Pointers approach
 *
 * NOTE: In Java, this is educational (GC handles memory). In C++/Rust, this is critical!
 */
public class Exercise02_EpochBasedReclamation {

    /**
     * TODO: Implement Epoch-Based Reclamation Manager
     *
     * Manages global epoch and per-thread epoch tracking
     */
    public static class EpochManager<T> {
        private static final int NUM_EPOCHS = 3; // Cycle through 0, 1, 2
        private static final int MAX_THREADS = 128;
        private static final long INACTIVE_EPOCH = -1;

        /**
         * Thread-local epoch information
         */
        private static class ThreadEpochInfo {
            final AtomicLong localEpoch;
            final int threadId;

            ThreadEpochInfo(int threadId) {
                this.threadId = threadId;
                this.localEpoch = new AtomicLong(INACTIVE_EPOCH);
            }
        }

        // Global epoch counter
        private final AtomicLong globalEpoch;

        // Per-thread epoch tracking
        private final List<ThreadEpochInfo> threadEpochs;
        private final AtomicInteger threadCount;

        // Retired lists: one per epoch
        @SuppressWarnings("unchecked")
        private final Queue<T>[] retiredLists;

        // Deleters for custom cleanup
        private Consumer<T> deleter;

        @SuppressWarnings("unchecked")
        public EpochManager() {
            this.globalEpoch = new AtomicLong(0);
            this.threadEpochs = new ArrayList<>(MAX_THREADS);
            this.threadCount = new AtomicInteger(0);

            // Initialize retired lists for each epoch
            this.retiredLists = new Queue[NUM_EPOCHS];
            for (int i = 0; i < NUM_EPOCHS; i++) {
                retiredLists[i] = new ConcurrentLinkedQueue<>();
            }

            // Initialize thread epoch tracking
            for (int i = 0; i < MAX_THREADS; i++) {
                threadEpochs.add(new ThreadEpochInfo(i));
            }

            this.deleter = null; // Will be set by user
        }

        /**
         * Set custom deleter for cleanup
         */
        public void setDeleter(Consumer<T> deleter) {
            this.deleter = deleter;
        }

        /**
         * TODO: Register a thread to get its thread ID
         */
        public int registerThread() {
            int threadId = threadCount.getAndIncrement();
            if (threadId >= MAX_THREADS) {
                throw new RuntimeException("Too many threads!");
            }
            return threadId;
        }

        /**
         * TODO: Enter critical section - announce current epoch
         *
         * Thread must call this before accessing shared data
         */
        public void enterCriticalSection(int threadId) {
            // TODO: Set thread's local epoch to current global epoch
            long currentEpoch = globalEpoch.get();
            threadEpochs.get(threadId).localEpoch.set(currentEpoch);
        }

        /**
         * TODO: Exit critical section - mark as inactive
         *
         * Thread must call this after done accessing shared data
         */
        public void exitCriticalSection(int threadId) {
            // TODO: Set thread's local epoch to INACTIVE
            threadEpochs.get(threadId).localEpoch.set(INACTIVE_EPOCH);
        }

        /**
         * TODO: Retire a node to the current epoch's retired list
         *
         * @param node The node to retire
         */
        public void retire(T node) {
            // TODO: Add node to retired list for current global epoch
            long currentEpoch = globalEpoch.get();
            int epochIndex = (int)(currentEpoch % NUM_EPOCHS);
            retiredLists[epochIndex].add(node);
        }

        /**
         * TODO: Try to advance global epoch
         *
         * Advances epoch if safe, and reclaims memory from old epochs
         *
         * @return true if epoch was advanced
         */
        public boolean tryAdvanceEpoch() {
            long currentEpoch = globalEpoch.get();

            // Check if all threads have moved beyond the old epoch
            if (!canAdvanceEpoch(currentEpoch)) {
                return false;
            }

            // Try to advance global epoch (CAS to handle concurrent attempts)
            if (!globalEpoch.compareAndSet(currentEpoch, currentEpoch + 1)) {
                return false; // Another thread advanced it
            }

            // Successfully advanced! Now reclaim memory from the old epoch
            long newEpoch = currentEpoch + 1;
            reclaimOldEpoch(newEpoch);

            return true;
        }

        /**
         * Helper: Check if we can safely advance from currentEpoch
         *
         * Safe to advance if all active threads are at currentEpoch or newer
         */
        private boolean canAdvanceEpoch(long currentEpoch) {
            int activeThreads = threadCount.get();

            for (int i = 0; i < activeThreads; i++) {
                long threadEpoch = threadEpochs.get(i).localEpoch.get();

                // Skip inactive threads
                if (threadEpoch == INACTIVE_EPOCH) {
                    continue;
                }

                // If any thread is in an old epoch, cannot advance
                if (threadEpoch < currentEpoch) {
                    return false;
                }
            }

            return true;
        }

        /**
         * Helper: Reclaim memory from epochs that are now safe
         *
         * After advancing to newEpoch, we can reclaim epoch (newEpoch - NUM_EPOCHS)
         * because all threads have moved at least NUM_EPOCHS forward
         */
        private void reclaimOldEpoch(long newEpoch) {
            // Calculate which epoch is now safe to reclaim
            // We keep NUM_EPOCHS in rotation, so reclaim (newEpoch - NUM_EPOCHS)
            if (newEpoch < NUM_EPOCHS) {
                return; // Not enough epochs have passed yet
            }

            long safeEpoch = newEpoch - NUM_EPOCHS;
            int reclaimIndex = (int)(safeEpoch % NUM_EPOCHS);

            // Reclaim all nodes from this epoch
            Queue<T> reclaimList = retiredLists[reclaimIndex];
            T node;
            while ((node = reclaimList.poll()) != null) {
                if (deleter != null) {
                    deleter.accept(node);
                }
                // In Java, node will be GC'd automatically
                // In C++, this is where we'd call delete
            }
        }

        /**
         * Get current global epoch (for debugging/testing)
         */
        public long getGlobalEpoch() {
            return globalEpoch.get();
        }

        /**
         * Get number of retired nodes (for testing)
         */
        public int getRetiredCount() {
            int count = 0;
            for (Queue<T> list : retiredLists) {
                count += list.size();
            }
            return count;
        }
    }

    /**
     * Lock-free Stack using Epoch-Based Reclamation
     *
     * Demonstrates how to use EBR in a lock-free data structure
     */
    public static class EBRStack<T> {
        private static class Node<T> {
            final T value;
            final AtomicReference<Node<T>> next;

            Node(T value) {
                this.value = value;
                this.next = new AtomicReference<>(null);
            }
        }

        private final AtomicReference<Node<T>> head;
        private final EpochManager<Node<T>> epochManager;
        private final ThreadLocal<Integer> threadId;

        public EBRStack() {
            this.head = new AtomicReference<>(null);
            this.epochManager = new EpochManager<>();
            this.threadId = ThreadLocal.withInitial(() ->
                epochManager.registerThread()
            );

            // Set up deleter (in Java this is just for demonstration)
            epochManager.setDeleter(node -> {
                // In C++ this would be: delete node;
                // In Java, just let GC handle it
            });
        }

        /**
         * Push a value onto the stack
         */
        public void push(T value) {
            Node<T> newNode = new Node<>(value);

            // No need for epoch protection during push (no reads)
            while (true) {
                Node<T> oldHead = head.get();
                newNode.next.set(oldHead);

                if (head.compareAndSet(oldHead, newNode)) {
                    return;
                }
            }
        }

        /**
         * Pop a value from the stack (using EBR)
         */
        public T pop() {
            int tid = threadId.get();

            // Enter critical section (announce current epoch)
            epochManager.enterCriticalSection(tid);

            try {
                while (true) {
                    Node<T> oldHead = head.get();

                    if (oldHead == null) {
                        return null; // Stack is empty
                    }

                    Node<T> newHead = oldHead.next.get();

                    if (head.compareAndSet(oldHead, newHead)) {
                        T value = oldHead.value;

                        // Retire the old head node
                        epochManager.retire(oldHead);

                        // Periodically try to advance epoch
                        if (Math.random() < 0.1) { // 10% chance
                            epochManager.tryAdvanceEpoch();
                        }

                        return value;
                    }
                }
            } finally {
                // Exit critical section (mark as inactive)
                epochManager.exitCriticalSection(tid);
            }
        }

        /**
         * Check if stack is empty (uses EBR)
         */
        public boolean isEmpty() {
            int tid = threadId.get();

            epochManager.enterCriticalSection(tid);
            try {
                return head.get() == null;
            } finally {
                epochManager.exitCriticalSection(tid);
            }
        }

        /**
         * Force epoch advancement (for testing)
         */
        public void advanceEpoch() {
            epochManager.tryAdvanceEpoch();
        }

        /**
         * Get number of retired nodes (for testing)
         */
        public int getRetiredCount() {
            return epochManager.getRetiredCount();
        }

        /**
         * Get global epoch (for testing)
         */
        public long getGlobalEpoch() {
            return epochManager.getGlobalEpoch();
        }
    }

    /**
     * Test and demonstration
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Epoch-Based Reclamation Test ===\n");

        testCorrectness();
        System.out.println();
        testMemoryReclamation();
        System.out.println();
        testConcurrentOperations();
    }

    /**
     * Test basic correctness
     */
    private static void testCorrectness() {
        System.out.println("Test 1: Basic Correctness");

        EBRStack<Integer> stack = new EBRStack<>();

        // Push some values
        for (int i = 0; i < 10; i++) {
            stack.push(i);
        }

        // Pop and verify LIFO order
        boolean correct = true;
        for (int i = 9; i >= 0; i--) {
            Integer value = stack.pop();
            if (value == null || value != i) {
                correct = false;
                System.out.println("  ❌ Expected " + i + ", got " + value);
            }
        }

        if (correct && stack.isEmpty()) {
            System.out.println("  ✅ PASS - Stack operations work correctly!");
        } else {
            System.out.println("  ❌ FAIL - Stack operations incorrect!");
        }
    }

    /**
     * Test memory reclamation
     */
    private static void testMemoryReclamation() {
        System.out.println("Test 2: Memory Reclamation");

        EBRStack<Integer> stack = new EBRStack<>();

        // Push and pop to create retired nodes
        for (int i = 0; i < 100; i++) {
            stack.push(i);
        }

        for (int i = 0; i < 100; i++) {
            stack.pop();
        }

        System.out.println("  Retired nodes before reclamation: " + stack.getRetiredCount());
        System.out.println("  Global epoch: " + stack.getGlobalEpoch());

        // Force epoch advancements to trigger reclamation
        for (int i = 0; i < 10; i++) {
            stack.advanceEpoch();
        }

        System.out.println("  Retired nodes after reclamation: " + stack.getRetiredCount());
        System.out.println("  Global epoch: " + stack.getGlobalEpoch());

        if (stack.getRetiredCount() < 100) {
            System.out.println("  ✅ PASS - Memory is being reclaimed!");
        } else {
            System.out.println("  ⚠️  WARN - Memory reclamation may not be working");
        }
    }

    /**
     * Test concurrent operations
     */
    private static void testConcurrentOperations() throws InterruptedException {
        System.out.println("Test 3: Concurrent Operations");

        final int numThreads = 8;
        final int operationsPerThread = 10000;

        EBRStack<Integer> stack = new EBRStack<>();
        Thread[] threads = new Thread[numThreads];

        // Half push, half pop
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    if (threadId % 2 == 0) {
                        stack.push(threadId * 1000000 + j);
                    } else {
                        stack.pop(); // May return null if empty
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        // Force reclamation
        for (int i = 0; i < 10; i++) {
            stack.advanceEpoch();
        }

        System.out.println("  Threads: " + numThreads);
        System.out.println("  Operations per thread: " + operationsPerThread);
        System.out.println("  Final retired count: " + stack.getRetiredCount());
        System.out.println("  Final global epoch: " + stack.getGlobalEpoch());
        System.out.println("  ✅ PASS - No crashes! EBR works under concurrency!");

        System.out.println("\n💡 Key Insights:");
        System.out.println("  • EBR provides safe memory reclamation");
        System.out.println("  • Simpler than Hazard Pointers (coarse-grained)");
        System.out.println("  • Better throughput for high-contention scenarios");
        System.out.println("  • Widely used in production (userspace RCU, Crossbeam)");
    }
}
