/**
 * SOLUTION: Hazard Pointers for Safe Memory Reclamation
 *
 * Complete reference implementation for Java.
 *
 * NOTE: While Java has GC and doesn't strictly need hazard pointers,
 * this implementation is educational for understanding:
 * 1. The memory reclamation problem in C++
 * 2. Cross-language concurrent programming
 * 3. What garbage collection does automatically
 */

package solutions;

import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicReferenceArray;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.ArrayList;
import java.util.List;

public class HazardPointers_Solution {

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

        public int acquireHazardPointerSlot() {
            int slot = threadCount.getAndIncrement();
            if (slot >= MAX_THREADS) {
                throw new RuntimeException("Too many threads!");
            }
            return slot;
        }

        public void setHazardPointer(int threadId, int hpIndex, T ptr) {
            HazardPointerRecord<T>[] records = hazardPointers.get(threadId);
            records[hpIndex].hazardPointer.set(ptr);
            records[hpIndex].active.set(true);
        }

        public void clearHazardPointer(int threadId, int hpIndex) {
            HazardPointerRecord<T>[] records = hazardPointers.get(threadId);
            records[hpIndex].active.set(false);
            records[hpIndex].hazardPointer.set(null);
        }

        public boolean isProtected(T ptr) {
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

        public boolean tryReclaim(T ptr) {
            return !isProtected(ptr);
        }
    }

    public static class HazardPointerContext<T> {
        private final HazardPointerManager<T> manager;
        private final int threadId;
        private final List<T> retiredList = new ArrayList<>();

        public HazardPointerContext(HazardPointerManager<T> manager) {
            this.manager = manager;
            this.threadId = manager.acquireHazardPointerSlot();
        }

        public T protect(int hpIndex, AtomicReference<T> atomicRef) {
            T ptr = null;
            T protectedPtr = atomicRef.get();

            do {
                ptr = protectedPtr;
                if (ptr == null) {
                    manager.clearHazardPointer(threadId, hpIndex);
                    return null;
                }
                manager.setHazardPointer(threadId, hpIndex, ptr);
                protectedPtr = atomicRef.get();
            } while (ptr != protectedPtr);

            return ptr;
        }

        public void unprotect(int hpIndex) {
            manager.clearHazardPointer(threadId, hpIndex);
        }

        public void retire(T ptr) {
            retiredList.add(ptr);
            if (retiredList.size() >= HazardPointerManager.RETIRED_LIST_MAX) {
                reclaim();
            }
        }

        public void reclaim() {
            List<T> stillProtected = new ArrayList<>();
            for (T ptr : retiredList) {
                if (!manager.tryReclaim(ptr)) {
                    stillProtected.add(ptr);
                }
            }
            retiredList.clear();
            retiredList.addAll(stillProtected);
        }
    }

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

        public void push(T value) {
            Node<T> node = new Node<>(value);
            Node<T> oldTop;

            do {
                oldTop = top.get();
                node.next.set(oldTop);
            } while (!top.compareAndSet(oldTop, node));
        }

        public T pop() {
            HazardPointerContext<Node<T>> context = hpContext.get();
            Node<T> oldTop;

            while (true) {
                oldTop = context.protect(0, top);

                if (oldTop == null) {
                    context.unprotect(0);
                    return null;
                }

                Node<T> next = oldTop.next.get();

                if (top.compareAndSet(oldTop, next)) {
                    T value = oldTop.value;
                    context.unprotect(0);
                    context.retire(oldTop);
                    return value;
                }
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("=== SOLUTION: Hazard Pointers ===\n");

        System.out.println("Key Implementation Points:\n");

        System.out.println("1. Protection Protocol:");
        System.out.println("   - Set hazard pointer to target node");
        System.out.println("   - Re-read atomic reference");
        System.out.println("   - If unchanged, protection successful");
        System.out.println("   - If changed, retry loop\n");

        System.out.println("2. Retirement and Reclamation:");
        System.out.println("   - Removed nodes go to retired list");
        System.out.println("   - When list grows, scan hazard pointers");
        System.out.println("   - Reclaim nodes not protected by any thread");
        System.out.println("   - Keep protected nodes in retired list\n");

        System.out.println("3. Thread-Local Design:");
        System.out.println("   - Each thread has its own hazard pointer slots");
        System.out.println("   - Each thread has its own retired list");
        System.out.println("   - Minimizes contention between threads\n");

        // Test
        LockFreeStackWithHP<Integer> stack = new LockFreeStackWithHP<>();
        stack.push(1);
        stack.push(2);
        stack.push(3);

        Integer value = stack.pop();
        System.out.println("Test pop: " + value + " (should be 3)\n");

        System.out.println("✅ Solution implements safe hazard pointer protocol");
        System.out.println("✅ In Java: Educational (GC handles this)");
        System.out.println("✅ In C++: CRITICAL for production lock-free code");
        System.out.println("✅ Cross-language understanding essential");
    }
}
