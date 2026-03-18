package com.multiprocessor.part2.memory_reclamation;

import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicReferenceArray;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.ArrayList;
import java.util.List;

/**
 * Exercise: Hazard Pointers for Safe Memory Reclamation
 *
 * CONCEPT: Safe memory reclamation in lock-free data structures
 *
 * NOTE: Java has automatic garbage collection, so hazard pointers are not
 * strictly necessary. However, this exercise is educational for:
 * 1. Understanding the memory reclamation problem in languages without GC (C++)
 * 2. Learning the hazard pointer protocol
 * 3. Appreciating what Java's GC does for you
 * 4. Cross-language understanding (if implementing in C++ later)
 *
 * THE PROBLEM (in languages without GC):
 * Lock-free data structures use CAS to modify shared pointers. After a
 * successful CAS removes a node, when is it safe to delete that node?
 *
 * - Thread A removes node N (CAS succeeds)
 * - Thread B may still hold a pointer to N (loaded before CAS)
 * - If A deletes N, B will dereference freed memory (use-after-free)
 *
 * HAZARD POINTERS SOLUTION:
 * - Each thread has "hazard pointer" slots
 * - Before dereferencing a pointer, thread stores it in hazard pointer
 * - Before deleting a node, check if any hazard pointer protects it
 * - If protected, defer deletion until safe
 *
 * LEARNING OBJECTIVES:
 * - Understand the memory reclamation problem in lock-free structures
 * - Implement hazard pointer protocol
 * - Use hazard pointers with lock-free stack
 * - Handle retired node lists and safe reclamation
 *
 * CPU REQUIREMENTS:
 * - Minimum: 4 cores
 * - Recommended: 8+ cores (higher contention makes protocol more important)
 */
public class Exercise01_HazardPointers {

    /**
     * TODO: Implement Hazard Pointer Manager
     *
     * Manages hazard pointers for all threads in the system
     */
    public static class HazardPointerManager<T> {
        private static final int MAX_THREADS = 128;
        private static final int HAZARD_POINTERS_PER_THREAD = 2;
        private static final int RETIRED_LIST_MAX = 100;

        private static class HazardPointerRecord<T> {
            final AtomicReference<T> hazardPointer = new AtomicReference<>(null);
            final AtomicBoolean active = new AtomicBoolean(false);
        }

        private final AtomicReferenceArray<HazardPointerRecord<T>[]> hazardPointers;
        private final AtomicInteger threadCount = new AtomicInteger(0);

        @SuppressWarnings("unchecked")
        public HazardPointerManager() {
            this.hazardPointers = new AtomicReferenceArray<>(MAX_THREADS);
            for (int i = 0; i < MAX_THREADS; i++) {
                HazardPointerRecord<T>[] records = (HazardPointerRecord<T>[])
                    new HazardPointerRecord[HAZARD_POINTERS_PER_THREAD];
                for (int j = 0; j < HAZARD_POINTERS_PER_THREAD; j++) {
                    records[j] = new HazardPointerRecord<>();
                }
                hazardPointers.set(i, records);
            }
        }

        /**
         * TODO: Implement acquireHazardPointerSlot
         *
         * Each thread calls this once to get its thread-local slot index
         */
        public int acquireHazardPointerSlot() {
            int slot = threadCount.getAndIncrement();
            if (slot >= MAX_THREADS) {
                throw new RuntimeException("Too many threads!");
            }
            return slot;
        }

        /**
         * TODO: Implement setHazardPointer
         *
         * Thread sets one of its hazard pointers to protect a node
         */
        public void setHazardPointer(int threadId, int hpIndex, T ptr) {
            // TODO: Set hazard pointer at [threadId][hpIndex] to ptr
            HazardPointerRecord<T>[] records = hazardPointers.get(threadId);
            records[hpIndex].hazardPointer.set(ptr);
            records[hpIndex].active.set(true);
        }

        /**
         * TODO: Implement clearHazardPointer
         *
         * Thread clears its hazard pointer when done with protected node
         */
        public void clearHazardPointer(int threadId, int hpIndex) {
            // TODO: Clear hazard pointer
            HazardPointerRecord<T>[] records = hazardPointers.get(threadId);
            records[hpIndex].active.set(false);
            records[hpIndex].hazardPointer.set(null);
        }

        /**
         * TODO: Implement isProtected
         *
         * Check if any thread's hazard pointer protects this node
         */
        public boolean isProtected(T ptr) {
            // TODO: Scan all hazard pointers to see if ptr is protected
            int count = threadCount.get();
            for (int tid = 0; tid < count; tid++) {
                HazardPointerRecord<T>[] records = hazardPointers.get(tid);
                for (int hpIdx = 0; hpIdx < HAZARD_POINTERS_PER_THREAD; hpIdx++) {
                    if (records[hpIdx].active.get()) {
                        T hazard = records[hpIdx].hazardPointer.get();
                        if (hazard == ptr) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        /**
         * TODO: Implement tryReclaim
         *
         * Return true if ptr is not protected (would be safe to delete in C++)
         */
        public boolean tryReclaim(T ptr) {
            // In Java, we don't actually delete (GC does it)
            // But we return whether it would be safe to delete
            return !isProtected(ptr);
        }
    }

    /**
     * TODO: Implement Thread-local context for hazard pointers
     */
    public static class HazardPointerContext<T> {
        private final HazardPointerManager<T> manager;
        private final int threadId;
        private final List<T> retiredList = new ArrayList<>();

        public HazardPointerContext(HazardPointerManager<T> manager) {
            this.manager = manager;
            this.threadId = manager.acquireHazardPointerSlot();
        }

        /**
         * TODO: Implement protect
         *
         * Acquire hazard pointer protection for a node
         * Returns protected reference (may differ if node was modified)
         */
        public T protect(int hpIndex, AtomicReference<T> atomicRef) {
            T ptr = null;
            T protectedPtr = atomicRef.get();

            // TODO: Implement protection protocol
            // 1. Set hazard pointer to protect node
            // 2. Re-read atomicRef to check it hasn't changed
            // 3. If changed, clear hazard pointer and retry
            // 4. If unchanged, node is now protected

            do {
                ptr = protectedPtr;
                if (ptr == null) {
                    manager.clearHazardPointer(threadId, hpIndex);
                    return null;
                }
                manager.setHazardPointer(threadId, hpIndex, ptr);
                // Re-read to ensure ptr is still valid
                protectedPtr = atomicRef.get();
            } while (ptr != protectedPtr);

            return ptr;
        }

        /**
         * TODO: Implement unprotect
         *
         * Release hazard pointer protection
         */
        public void unprotect(int hpIndex) {
            manager.clearHazardPointer(threadId, hpIndex);
        }

        /**
         * TODO: Implement retire
         *
         * Add node to retired list for eventual reclamation check
         */
        public void retire(T ptr) {
            // TODO: Add to retired list
            retiredList.add(ptr);

            // TODO: If retired list is large, try to reclaim
            if (retiredList.size() >= HazardPointerManager.RETIRED_LIST_MAX) {
                reclaim();
            }
        }

        /**
         * TODO: Implement reclaim
         *
         * Check which retired nodes are no longer protected
         * In Java, we just remove them from list (GC will collect)
         * In C++, we would actually delete them
         */
        public void reclaim() {
            List<T> stillProtected = new ArrayList<>();
            int reclaimed = 0;
            for (T ptr : retiredList) {
                if (!manager.tryReclaim(ptr)) {
                    stillProtected.add(ptr);
                } else {
                    reclaimed++;
                    // In C++, would: delete ptr;
                    // In Java, just let GC handle it
                }
            }
            retiredList.clear();
            retiredList.addAll(stillProtected);

            if (reclaimed > 0) {
                System.out.println("Thread " + threadId + " reclaimed " + reclaimed + " nodes");
            }
        }
    }

    /**
     * TODO: Implement Lock-Free Stack with Hazard Pointer Protection
     *
     * This is the classic Treiber stack, now with hazard pointer protocol
     */
    public static class LockFreeStackWithHP<T> {
        private static class Node<T> {
            final T value;
            final AtomicReference<Node<T>> next;

            Node(T value) {
                this.value = value;
                this.next = new AtomicReference<>(null);
            }
        }

        private final AtomicReference<Node<T>> top = new AtomicReference<>(null);
        private final HazardPointerManager<Node<T>> hpManager = new HazardPointerManager<>();
        private final ThreadLocal<HazardPointerContext<Node<T>>> hpContext =
            ThreadLocal.withInitial(() -> new HazardPointerContext<>(hpManager));

        /**
         * TODO: Implement push
         *
         * No hazard pointers needed - we're creating a new node
         */
        public void push(T value) {
            Node<T> node = new Node<>(value);
            Node<T> oldTop;

            // TODO: Standard Treiber stack push with CAS loop
            do {
                oldTop = top.get();
                node.next.set(oldTop);
            } while (!top.compareAndSet(oldTop, node));
        }

        /**
         * TODO: Implement pop with hazard pointer protection
         *
         * This is where hazard pointers are critical (in C++)!
         */
        public T pop() {
            HazardPointerContext<Node<T>> context = hpContext.get();
            Node<T> oldTop;

            // TODO: Implement pop with hazard pointer protection
            // 1. Protect top node with hazard pointer
            // 2. If null, return null (empty)
            // 3. Read next pointer
            // 4. Try to CAS top to next
            // 5. If success, copy value, retire old_top, return value
            // 6. If fail, retry

            while (true) {
                // Protect current top node
                oldTop = context.protect(0, top);

                if (oldTop == null) {
                    context.unprotect(0);
                    return null; // Empty stack
                }

                // Read next pointer (safe because oldTop is protected)
                Node<T> next = oldTop.next.get();

                // Try to CAS
                if (top.compareAndSet(oldTop, next)) {
                    // Success! Copy value and retire node
                    T value = oldTop.value;
                    context.unprotect(0);

                    // Retire node (in C++ would eventually delete)
                    context.retire(oldTop);
                    return value;
                }
                // CAS failed, retry
            }
        }

        /**
         * Get current size (not linearizable, for testing only)
         */
        public int unsafeSize() {
            int count = 0;
            Node<T> current = top.get();
            while (current != null) {
                count++;
                current = current.next.get();
            }
            return count;
        }
    }

    /**
     * Testing and demonstration
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Hazard Pointers Memory Reclamation Test ===\n");

        demonstrateSafety();
        testCorrectness();
        System.out.println("\n=== Note on Java vs C++ ===");
        System.out.println("In Java, garbage collection handles memory automatically.");
        System.out.println("Hazard pointers are CRITICAL in C++ for safe lock-free code.");
        System.out.println("This exercise demonstrates the protocol used in C++ systems.");
    }

    private static void demonstrateSafety() {
        System.out.println("=== Memory Safety Demonstration ===\n");

        System.out.println("Without hazard pointers (C++):");
        System.out.println("  ❌ Use-after-free bugs possible");
        System.out.println("  ❌ Undefined behavior with concurrent access");
        System.out.println("  ❌ No safe way to reclaim memory\n");

        System.out.println("With hazard pointers (C++):");
        System.out.println("  ✅ Protected nodes cannot be deleted");
        System.out.println("  ✅ Deferred deletion until safe");
        System.out.println("  ✅ No garbage collector required");
        System.out.println("  ✅ Suitable for production code\n");

        System.out.println("Hazard Pointer Protocol:");
        System.out.println("  1. Before dereferencing, set hazard pointer");
        System.out.println("  2. Re-read atomic reference to verify unchanged");
        System.out.println("  3. If unchanged, node is protected");
        System.out.println("  4. After use, clear hazard pointer");
        System.out.println("  5. Before delete, check all hazard pointers\n");

        System.out.println("In Java:");
        System.out.println("  ✅ Garbage collection handles everything");
        System.out.println("  ✅ No manual memory management needed");
        System.out.println("  💡 But understanding hazard pointers helps with:");
        System.out.println("     - Cross-language programming (Java + C++)");
        System.out.println("     - Understanding lock-free literature");
        System.out.println("     - Appreciating what GC does for you\n");
    }

    private static void testCorrectness() throws InterruptedException {
        System.out.println("=== Correctness Test ===\n");

        LockFreeStackWithHP<Integer> stack = new LockFreeStackWithHP<>();
        int numThreads = 8;
        int opsPerThread = 1000;

        AtomicInteger pushCount = new AtomicInteger(0);
        AtomicInteger popCount = new AtomicInteger(0);

        Thread[] threads = new Thread[numThreads];

        // Half pushers, half poppers
        for (int i = 0; i < numThreads; i++) {
            if (i % 2 == 0) {
                // Pusher
                final int id = i;
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < opsPerThread; j++) {
                        stack.push(id * opsPerThread + j);
                        pushCount.incrementAndGet();
                    }
                });
            } else {
                // Popper
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < opsPerThread; j++) {
                        Integer value = stack.pop();
                        if (value != null) {
                            popCount.incrementAndGet();
                        }
                    }
                });
            }
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        // Pop remaining items
        while (stack.pop() != null) {
            popCount.incrementAndGet();
        }

        System.out.println("Pushes: " + pushCount.get());
        System.out.println("Pops: " + popCount.get());
        System.out.println("Remaining in stack: " + stack.unsafeSize());
        System.out.println(pushCount.get() == popCount.get() ? "✅ PASS\n" : "❌ FAIL\n");

        System.out.println("💡 Hazard pointers ensure safe concurrent access");
        System.out.println("💡 No node is deleted while another thread uses it");
        System.out.println("💡 Essential pattern for C++ lock-free programming");
    }
}
