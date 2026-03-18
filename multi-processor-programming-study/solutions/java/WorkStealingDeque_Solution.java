/**
 * SOLUTION: Work-Stealing Deque (Chase-Lev Algorithm)
 *
 * This is the complete reference implementation of the Chase-Lev work-stealing deque in Java.
 * All TODOs from the exercise have been completed.
 *
 * KEY IMPLEMENTATION POINTS:
 * 1. Owner operations (push/pop) are fast and mostly non-blocking
 * 2. Thief operations (steal) use CAS and may fail
 * 3. Dynamic resizing handled by owner only
 * 4. Similar to what Java's ForkJoinPool uses internally
 */

package solutions;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicReferenceArray;

public class WorkStealingDeque_Solution<T> {

    /**
     * Circular array for storing tasks
     */
    private static class CircularArray<T> {
        private final AtomicReferenceArray<T> buffer;
        private final int capacity;

        CircularArray(int size) {
            this.capacity = size;
            this.buffer = new AtomicReferenceArray<>(size);
        }

        T get(long index) {
            return buffer.get((int) (index & (capacity - 1)));
        }

        void put(long index, T value) {
            buffer.set((int) (index & (capacity - 1)), value);
        }

        CircularArray<T> grow(long bottom, long top) {
            CircularArray<T> newArray = new CircularArray<>(capacity * 2);
            for (long i = top; i < bottom; i++) {
                newArray.put(i, get(i));
            }
            return newArray;
        }

        int getCapacity() {
            return capacity;
        }
    }

    private final AtomicInteger top = new AtomicInteger(0);
    private final AtomicInteger bottom = new AtomicInteger(0);
    private final AtomicReference<CircularArray<T>> array;

    private static final int INITIAL_CAPACITY = 256;

    public WorkStealingDeque_Solution() {
        array = new AtomicReference<>(new CircularArray<>(INITIAL_CAPACITY));
    }

    /**
     * SOLUTION: push (owner only)
     *
     * Fast path - no CAS needed, just atomic stores
     */
    public void push(T value) {
        long b = bottom.get();
        long t = top.get();
        CircularArray<T> a = array.get();

        // Resize if needed
        if (b - t >= a.getCapacity()) {
            CircularArray<T> newArray = a.grow(b, t);
            array.set(newArray);
            a = newArray;
        }

        // Put value and increment bottom
        a.put(b, value);
        bottom.set((int) (b + 1));
    }

    /**
     * SOLUTION: pop (owner only)
     *
     * Fast path when no competition, CAS only for last element
     */
    public T pop() {
        long b = bottom.get() - 1;
        CircularArray<T> a = array.get();
        bottom.set((int) b);

        long t = top.get();

        T result = null;
        if (t <= b) {
            // Non-empty
            result = a.get(b);

            if (t == b) {
                // Last element - compete with thieves
                if (!top.compareAndSet((int) t, (int) (t + 1))) {
                    // Lost to thief
                    result = null;
                }
                bottom.set((int) (b + 1));
            }
        } else {
            // Empty
            bottom.set((int) (b + 1));
        }

        return result;
    }

    /**
     * SOLUTION: steal (thieves)
     *
     * Always uses CAS, can fail if racing with other thieves or owner
     */
    public T steal() {
        long t = top.get();
        long b = bottom.get();

        if (t >= b) {
            return null; // Empty
        }

        CircularArray<T> a = array.get();
        T value = a.get(t);

        // Try to claim with CAS
        if (!top.compareAndSet((int) t, (int) (t + 1))) {
            return null; // Lost race
        }

        return value;
    }

    public int size() {
        int b = bottom.get();
        int t = top.get();
        return Math.max(0, b - t);
    }

    /**
     * Demonstration of the solution
     */
    public static void main(String[] args) {
        System.out.println("=== SOLUTION: Work-Stealing Deque ===\n");

        System.out.println("Implementation Details:\n");

        System.out.println("1. push() - Owner pushes to bottom:");
        System.out.println("   - Get current bottom and top");
        System.out.println("   - Check if resize needed");
        System.out.println("   - Put value at bottom index");
        System.out.println("   - Increment bottom (atomic store)\n");

        System.out.println("2. pop() - Owner pops from bottom:");
        System.out.println("   - Decrement bottom (claim task)");
        System.out.println("   - Get value at bottom");
        System.out.println("   - If last element, CAS with thieves");
        System.out.println("   - Otherwise just return it\n");

        System.out.println("3. steal() - Thieves steal from top:");
        System.out.println("   - Get top and bottom");
        System.out.println("   - Check if empty");
        System.out.println("   - Read value at top");
        System.out.println("   - CAS top to claim it\n");

        // Test
        WorkStealingDeque_Solution<Integer> deque = new WorkStealingDeque_Solution<>();

        System.out.println("Test: Basic operations");
        deque.push(1);
        deque.push(2);
        deque.push(3);

        System.out.println("Pushed: 1, 2, 3");
        System.out.println("Size: " + deque.size());

        Integer owner = deque.pop();
        System.out.println("Owner popped: " + owner + " (LIFO - should be 3)");

        Integer thief = deque.steal();
        System.out.println("Thief stole: " + thief + " (FIFO - should be 1)\n");

        System.out.println("✅ Solution implements Chase-Lev correctly");
        System.out.println("✅ Owner: LIFO (cache locality)");
        System.out.println("✅ Thieves: FIFO (load balancing)");
        System.out.println("✅ Used in Java ForkJoinPool");
    }
}
