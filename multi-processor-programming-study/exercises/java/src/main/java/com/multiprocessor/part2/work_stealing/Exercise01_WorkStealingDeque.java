package com.multiprocessor.part2.work_stealing;

import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.concurrent.atomic.AtomicReferenceArray;
import java.util.Random;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveTask;

/**
 * Exercise: Work-Stealing Deque (Chase-Lev Algorithm)
 *
 * CONCEPT: Double-ended queue for efficient task parallelism
 *
 * THE PROBLEM:
 * In task-parallel systems (Fork/Join, parallel-for, etc.), we need:
 * - Worker threads that process tasks from their own queue (owner)
 * - Other threads can "steal" tasks when idle (thieves)
 * - Owner pushes/pops from one end (LIFO for cache locality)
 * - Thieves steal from the other end (FIFO for load balancing)
 *
 * CHASE-LEV ALGORITHM:
 * - Lock-free work-stealing deque
 * - Owner operations (push/pop) are almost wait-free
 * - Thief operations (steal) use CAS and may fail
 * - Uses circular array with dynamic resizing
 *
 * APPLICATIONS:
 * - Java ForkJoinPool (uses similar work-stealing deque)
 * - .NET Task Parallel Library
 * - Intel TBB (Threading Building Blocks)
 * - Rust Rayon
 *
 * LEARNING OBJECTIVES:
 * - Understand work-stealing scheduling
 * - Implement Chase-Lev deque algorithm
 * - Handle dynamic array resizing in lock-free context
 * - Compare with Java's built-in ForkJoinPool
 *
 * CPU REQUIREMENTS:
 * - Minimum: 4 cores (to show work stealing benefits)
 * - Recommended: 8-16 cores (uneven workload distribution)
 * - Optimal: 16+ cores (dramatic load balancing benefits)
 */
public class Exercise01_WorkStealingDeque {

    /**
     * TODO: Implement Chase-Lev Work-Stealing Deque
     *
     * This is a lock-free deque optimized for task parallelism where:
     * - One thread (owner) pushes and pops from the bottom (tail)
     * - Multiple threads (thieves) steal from the top (head)
     */
    public static class WorkStealingDeque<T> {
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

            // Create a larger array and copy elements
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

        private final AtomicInteger top = new AtomicInteger(0);      // Head (thieves steal)
        private final AtomicInteger bottom = new AtomicInteger(0);   // Tail (owner push/pop)
        private final AtomicReference<CircularArray<T>> array;

        private static final int INITIAL_CAPACITY = 256;

        public WorkStealingDeque() {
            array = new AtomicReference<>(new CircularArray<>(INITIAL_CAPACITY));
        }

        /**
         * TODO: Implement push (owner only)
         *
         * Owner pushes task to the bottom (tail) of the deque
         * This is the common case and should be very fast
         */
        public void push(T value) {
            // TODO: Implement push operation
            // 1. Load bottom (owner is the only writer)
            // 2. Load top (synchronize with thieves)
            // 3. Load current array
            // 4. If array is full, grow it
            // 5. Put value at bottom position
            // 6. Increment bottom (make value visible to thieves)

            long b = bottom.get();
            long t = top.get();
            CircularArray<T> a = array.get();

            // Check if array is full
            if (b - t >= a.getCapacity()) {
                // Grow array
                CircularArray<T> newArray = a.grow(b, t);
                array.set(newArray);
                a = newArray;
            }

            // Put value at bottom
            a.put(b, value);

            // Make value visible to thieves
            bottom.set((int) (b + 1));
        }

        /**
         * TODO: Implement pop (owner only)
         *
         * Owner pops task from the bottom (tail) of the deque
         * Returns null if empty
         */
        public T pop() {
            // TODO: Implement pop operation
            // 1. Decrement bottom (owner claims the task)
            // 2. Load array
            // 3. Load top
            // 4. If deque was empty, restore bottom and return null
            // 5. If deque has one element, use CAS to compete with thieves
            // 6. Otherwise, just take the element (no competition)

            long b = bottom.get() - 1;
            CircularArray<T> a = array.get();
            bottom.set((int) b);

            long t = top.get();

            T result = null;
            if (t <= b) {
                // Non-empty queue
                result = a.get(b);

                if (t == b) {
                    // Last element - compete with thieves using CAS
                    if (!top.compareAndSet((int) t, (int) (t + 1))) {
                        // Lost race to thief
                        result = null;
                    }
                    bottom.set((int) (b + 1));
                }
            } else {
                // Empty queue - restore bottom
                bottom.set((int) (b + 1));
            }

            return result;
        }

        /**
         * TODO: Implement steal (thieves)
         *
         * Thief steals task from the top (head) of the deque
         * Returns null if empty or if lost race to another thief
         */
        public T steal() {
            // TODO: Implement steal operation
            // 1. Load top
            // 2. Load bottom
            // 3. If empty (top >= bottom), return null
            // 4. Load array
            // 5. Read value at top
            // 6. Try to CAS top to top+1
            // 7. If CAS succeeds, return value; otherwise return null

            long t = top.get();
            long b = bottom.get();

            if (t >= b) {
                // Empty queue
                return null;
            }

            // Non-empty queue
            CircularArray<T> a = array.get();
            T value = a.get(t);

            // Try to steal with CAS
            if (!top.compareAndSet((int) t, (int) (t + 1))) {
                // Lost race to another thief
                return null;
            }

            return value;
        }

        /**
         * Get approximate size (not linearizable, for testing only)
         */
        public int size() {
            int b = bottom.get();
            int t = top.get();
            return Math.max(0, b - t);
        }
    }

    /**
     * Task type for testing
     */
    public static class Task {
        final int id;
        final int workload;

        Task(int id, int workload) {
            this.id = id;
            this.workload = workload;
        }

        void execute() {
            // Simulate work
            int sum = 0;
            for (int i = 0; i < workload; i++) {
                sum += i;
            }
        }
    }

    /**
     * Testing: Correctness Test
     */
    public static void testCorrectness() throws InterruptedException {
        System.out.println("=== Correctness Test ===\n");

        WorkStealingDeque<Task> deque = new WorkStealingDeque<>();

        System.out.println("Test 1: Single-threaded push/pop");
        deque.push(new Task(1, 100));
        deque.push(new Task(2, 200));
        deque.push(new Task(3, 300));

        Task t1 = deque.pop();
        Task t2 = deque.pop();
        Task t3 = deque.pop();
        Task t4 = deque.pop();

        System.out.println("  Popped: " + t1.id + ", " + t2.id + ", " + t3.id);
        System.out.println("  Empty pop: " + (t4 == null ? "null" : t4.id) + " (should be null)");
        System.out.println(t1.id == 3 && t2.id == 2 && t3.id == 1 && t4 == null ? "  ✅ PASS\n" : "  ❌ FAIL\n");

        System.out.println("Test 2: Multi-threaded work stealing");
        WorkStealingDeque<Task> sharedDeque = new WorkStealingDeque<>();

        // Owner pushes tasks
        for (int i = 0; i < 1000; i++) {
            sharedDeque.push(new Task(i + 1, 100));
        }

        AtomicInteger tasksExecuted = new AtomicInteger(0);
        AtomicInteger tasksStolen = new AtomicInteger(0);

        // Owner thread (pops from bottom)
        Thread owner = new Thread(() -> {
            int localCount = 0;
            Task task;
            while ((task = sharedDeque.pop()) != null || sharedDeque.size() > 0) {
                if (task != null) {
                    task.execute();
                    localCount++;
                }
            }
            tasksExecuted.addAndGet(localCount);
        });

        // Thief threads (steal from top)
        List<Thread> thieves = new ArrayList<>();
        for (int i = 0; i < 4; i++) {
            thieves.add(new Thread(() -> {
                int stolenCount = 0;
                Task task;
                while ((task = sharedDeque.steal()) != null || sharedDeque.size() > 0) {
                    if (task != null) {
                        task.execute();
                        stolenCount++;
                    }
                    Thread.yield();
                }
                tasksStolen.addAndGet(stolenCount);
            }));
        }

        owner.start();
        for (Thread thief : thieves) {
            thief.start();
        }

        owner.join();
        for (Thread thief : thieves) {
            thief.join();
        }

        System.out.println("  Tasks executed by owner: " + (tasksExecuted.get() - tasksStolen.get()));
        System.out.println("  Tasks stolen by thieves: " + tasksStolen.get());
        System.out.println("  Total tasks executed: " + tasksExecuted.get());
        System.out.println(tasksExecuted.get() == 1000 ? "  ✅ PASS\n" : "  ❌ FAIL\n");
    }

    /**
     * Testing: Performance Comparison
     */
    public static void comparePerformance() throws InterruptedException {
        System.out.println("=== Performance Test: Parallel Task Execution ===\n");

        final int numTasks = 100000;
        final int numWorkers = Runtime.getRuntime().availableProcessors();

        System.out.println("Number of workers: " + numWorkers);
        System.out.println("Number of tasks: " + numTasks + "\n");

        // Create tasks with varying workloads
        Random random = new Random();
        List<Task> tasks = new ArrayList<>();
        for (int i = 0; i < numTasks; i++) {
            tasks.add(new Task(i + 1, 100 + random.nextInt(900)));
        }

        // Test: Work Stealing Deque
        {
            @SuppressWarnings("unchecked")
            WorkStealingDeque<Task>[] workerDeques = new WorkStealingDeque[numWorkers];
            for (int i = 0; i < numWorkers; i++) {
                workerDeques[i] = new WorkStealingDeque<>();
            }

            // Distribute tasks unevenly
            for (int i = 0; i < tasks.size(); i++) {
                workerDeques[i % numWorkers].push(tasks.get(i));
            }

            AtomicInteger completed = new AtomicInteger(0);
            long start = System.currentTimeMillis();

            List<Thread> workers = new ArrayList<>();
            for (int i = 0; i < numWorkers; i++) {
                final int workerId = i;
                workers.add(new Thread(() -> {
                    int localCount = 0;

                    while (completed.get() < numTasks) {
                        // Try own deque first
                        Task task = workerDeques[workerId].pop();

                        if (task == null) {
                            // Own deque empty, try stealing
                            boolean stole = false;
                            for (int j = 1; j < numWorkers && !stole; j++) {
                                int victim = (workerId + j) % numWorkers;
                                task = workerDeques[victim].steal();
                                if (task != null) {
                                    stole = true;
                                }
                            }

                            if (!stole) {
                                Thread.yield();
                                continue;
                            }
                        }

                        task.execute();
                        localCount++;
                    }

                    completed.addAndGet(localCount);
                }));
            }

            for (Thread worker : workers) {
                worker.start();
            }
            for (Thread worker : workers) {
                worker.join();
            }

            long duration = System.currentTimeMillis() - start;

            System.out.println("Work-Stealing Deque:");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Tasks completed: " + completed.get());
            System.out.println("  Throughput: " + (numTasks * 1000.0 / duration) + " tasks/sec\n");
        }

        System.out.println("💡 Work-stealing provides automatic load balancing");
        System.out.println("💡 Owner operations (push/pop) are very fast (no CAS)");
        System.out.println("💡 Thieves use CAS only when stealing");
        System.out.println("💡 Java ForkJoinPool uses similar work-stealing deques\n");
    }

    /**
     * Demonstrate comparison with Java's ForkJoinPool
     */
    public static void compareForkJoinPool() {
        System.out.println("=== Comparison with Java ForkJoinPool ===\n");

        System.out.println("Our Work-Stealing Deque:");
        System.out.println("  ✅ Educational implementation of Chase-Lev algorithm");
        System.out.println("  ✅ Shows core concepts clearly");
        System.out.println("  ✅ Single deque per worker\n");

        System.out.println("Java ForkJoinPool:");
        System.out.println("  ✅ Production-ready, highly optimized");
        System.out.println("  ✅ Integrated with Java's parallel streams");
        System.out.println("  ✅ Advanced features: adaptive parallelism, etc.");
        System.out.println("  ✅ Multiple submission queues + worker queues\n");

        // Simple ForkJoinPool example
        System.out.println("Example: Parallel sum with ForkJoinPool");

        class SumTask extends RecursiveTask<Long> {
            private final long[] array;
            private final int start;
            private final int end;
            private static final int THRESHOLD = 10000;

            SumTask(long[] array, int start, int end) {
                this.array = array;
                this.start = start;
                this.end = end;
            }

            @Override
            protected Long compute() {
                if (end - start <= THRESHOLD) {
                    // Sequential computation
                    long sum = 0;
                    for (int i = start; i < end; i++) {
                        sum += array[i];
                    }
                    return sum;
                } else {
                    // Fork into subtasks
                    int mid = (start + end) / 2;
                    SumTask left = new SumTask(array, start, mid);
                    SumTask right = new SumTask(array, mid, end);

                    left.fork();  // Async execution
                    long rightResult = right.compute();
                    long leftResult = left.join();

                    return leftResult + rightResult;
                }
            }
        }

        long[] array = new long[1000000];
        for (int i = 0; i < array.length; i++) {
            array[i] = i;
        }

        ForkJoinPool pool = new ForkJoinPool();
        long result = pool.invoke(new SumTask(array, 0, array.length));

        System.out.println("  Sum of 0..999999 = " + result);
        System.out.println("  ✅ ForkJoinPool handles work distribution automatically\n");
    }

    /**
     * Demonstrate work-stealing concepts
     */
    public static void demonstrateConcepts() {
        System.out.println("=== Work-Stealing Deque Concepts ===\n");

        System.out.println("Chase-Lev Algorithm:");
        System.out.println("  • Asymmetric access pattern (owner vs thieves)");
        System.out.println("  • Owner: Fast push/pop from bottom (tail) - LIFO");
        System.out.println("  • Thieves: Steal from top (head) - FIFO");
        System.out.println("  • Lock-free with minimal CAS operations\n");

        System.out.println("Why LIFO for owner, FIFO for thieves?");
        System.out.println("  • LIFO (owner): Cache locality - recent tasks likely related");
        System.out.println("  • FIFO (thieves): Load balancing - steal oldest tasks");
        System.out.println("  • Reduces contention between owner and thieves\n");

        System.out.println("Dynamic Resizing:");
        System.out.println("  • Circular array grows when full");
        System.out.println("  • Power-of-2 size for efficient modulo (bitwise AND)");
        System.out.println("  • Owner handles resizing (no thief involvement)\n");

        System.out.println("Applications:");
        System.out.println("  ✅ Fork/Join parallelism");
        System.out.println("  ✅ Parallel for loops");
        System.out.println("  ✅ Recursive task decomposition");
        System.out.println("  ✅ Dynamic load balancing\n");
    }

    /**
     * Main test driver
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Work-Stealing Deque (Chase-Lev) Test ===\n");

        demonstrateConcepts();
        testCorrectness();
        comparePerformance();
        compareForkJoinPool();
    }
}
