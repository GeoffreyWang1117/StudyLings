package com.multiprocessor.part2.thread_pool;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.*;

/**
 * Exercise 01: Thread Pool Implementation
 *
 * This exercise implements various thread pool patterns, which are the most
 * commonly used concurrency patterns in production systems.
 *
 * Learning Objectives:
 * 1. Understand thread pool architecture and components
 * 2. Implement fixed-size thread pool with task queue
 * 3. Implement work-stealing thread pool using Chase-Lev deque
 * 4. Learn graceful shutdown protocols
 * 5. Compare with Java's ExecutorService
 *
 * Real-World Applications:
 * - Web servers (request handling)
 * - Database systems (query execution)
 * - Background task processing
 * - Async I/O operations
 *
 * Hardware Requirements:
 * - Minimum: 4 cores
 * - Recommended: 8+ cores for observing load balancing
 */
public class Exercise01_ThreadPool {

    /**
     * Task 1: Fixed Thread Pool
     *
     * Implements a simple fixed-size thread pool with a shared task queue.
     * All worker threads compete for tasks from a single queue.
     *
     * Key Concepts:
     * - Worker threads lifecycle
     * - Shared task queue (BlockingQueue)
     * - Graceful shutdown
     * - Task submission and execution
     */
    public static class FixedThreadPool {
        private final int poolSize;
        private final List<WorkerThread> workers;
        private final BlockingQueue<Runnable> taskQueue;
        private final AtomicBoolean shutdown;

        public FixedThreadPool(int poolSize) {
            this.poolSize = poolSize;
            this.workers = new ArrayList<>(poolSize);
            this.taskQueue = new LinkedBlockingQueue<>();
            this.shutdown = new AtomicBoolean(false);

            // TODO: Create and start worker threads
            // Hint: Each worker should continuously take tasks from the queue
            for (int i = 0; i < poolSize; i++) {
                WorkerThread worker = new WorkerThread(i);
                workers.add(worker);
                worker.start();
            }
        }

        /**
         * Submit a task for execution
         */
        public void submit(Runnable task) {
            if (shutdown.get()) {
                throw new RejectedExecutionException("Thread pool is shut down");
            }

            // TODO: Add task to queue
            // Hint: Use taskQueue.offer() or put()
            try {
                taskQueue.put(task);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RejectedExecutionException("Task submission interrupted", e);
            }
        }

        /**
         * Graceful shutdown: stop accepting new tasks, wait for existing tasks to complete
         */
        public void shutdown() {
            // TODO: Implement graceful shutdown
            // 1. Set shutdown flag
            // 2. Interrupt all worker threads
            // 3. Wait for workers to finish

            shutdown.set(true);

            for (WorkerThread worker : workers) {
                worker.interrupt();
            }
        }

        /**
         * Wait for all tasks to complete
         */
        public boolean awaitTermination(long timeout, TimeUnit unit) throws InterruptedException {
            long deadline = System.nanoTime() + unit.toNanos(timeout);

            for (WorkerThread worker : workers) {
                long remaining = deadline - System.nanoTime();
                if (remaining <= 0) {
                    return false;
                }
                worker.join(TimeUnit.NANOSECONDS.toMillis(remaining));
            }

            return true;
        }

        public int getActiveCount() {
            return (int) workers.stream().filter(Thread::isAlive).count();
        }

        public int getQueueSize() {
            return taskQueue.size();
        }

        /**
         * Worker thread that continuously processes tasks from the queue
         */
        private class WorkerThread extends Thread {
            private final int workerId;

            public WorkerThread(int workerId) {
                this.workerId = workerId;
                setName("Worker-" + workerId);
            }

            @Override
            public void run() {
                // TODO: Implement worker thread logic
                // 1. Continuously poll tasks from queue
                // 2. Execute tasks
                // 3. Handle shutdown signal
                // 4. Handle exceptions

                while (!shutdown.get() || !taskQueue.isEmpty()) {
                    try {
                        Runnable task = taskQueue.poll(100, TimeUnit.MILLISECONDS);
                        if (task != null) {
                            try {
                                task.run();
                            } catch (Exception e) {
                                // Log exception but keep worker alive
                                System.err.println("Task execution failed in " + getName() + ": " + e.getMessage());
                            }
                        }
                    } catch (InterruptedException e) {
                        if (shutdown.get()) {
                            break;
                        }
                    }
                }
            }
        }
    }

    /**
     * Task 2: Work-Stealing Thread Pool
     *
     * Advanced thread pool using work-stealing for better load balancing.
     * Each worker has its own deque and can steal tasks from others when idle.
     *
     * Key Concepts:
     * - Per-worker task deques
     * - Work stealing for load balancing
     * - Owner push/pop (LIFO for cache locality)
     * - Thief steal (FIFO for load distribution)
     *
     * Benefits over fixed pool:
     * - Better load balancing
     * - Better cache locality
     * - Reduces contention on shared queue
     */
    public static class WorkStealingThreadPool {
        private final int poolSize;
        private final List<WorkStealingWorker> workers;
        private final AtomicBoolean shutdown;
        private final Random random;  // For random victim selection

        public WorkStealingThreadPool(int poolSize) {
            this.poolSize = poolSize;
            this.workers = new ArrayList<>(poolSize);
            this.shutdown = new AtomicBoolean(false);
            this.random = new Random();

            // TODO: Create work-stealing workers
            for (int i = 0; i < poolSize; i++) {
                WorkStealingWorker worker = new WorkStealingWorker(i);
                workers.add(worker);
                worker.start();
            }
        }

        /**
         * Submit task to a random worker's deque
         */
        public void submit(Runnable task) {
            if (shutdown.get()) {
                throw new RejectedExecutionException("Thread pool is shut down");
            }

            // TODO: Submit to random worker
            // Hint: Pick a random worker and push to its deque
            int workerIndex = random.nextInt(poolSize);
            workers.get(workerIndex).pushTask(task);
        }

        public void shutdown() {
            shutdown.set(true);
            for (WorkStealingWorker worker : workers) {
                worker.interrupt();
            }
        }

        public boolean awaitTermination(long timeout, TimeUnit unit) throws InterruptedException {
            long deadline = System.nanoTime() + unit.toNanos(timeout);

            for (WorkStealingWorker worker : workers) {
                long remaining = deadline - System.nanoTime();
                if (remaining <= 0) {
                    return false;
                }
                worker.join(TimeUnit.NANOSECONDS.toMillis(remaining));
            }

            return true;
        }

        /**
         * Work-stealing worker with its own deque
         */
        private class WorkStealingWorker extends Thread {
            private final int workerId;
            private final Deque<Runnable> taskDeque;
            private final AtomicInteger tasksExecuted;
            private final AtomicInteger tasksStolen;

            public WorkStealingWorker(int workerId) {
                this.workerId = workerId;
                this.taskDeque = new ConcurrentLinkedDeque<>();
                this.tasksExecuted = new AtomicInteger(0);
                this.tasksStolen = new AtomicInteger(0);
                setName("WorkStealer-" + workerId);
            }

            public void pushTask(Runnable task) {
                // TODO: Push task to own deque (LIFO end)
                taskDeque.offerFirst(task);
            }

            @Override
            public void run() {
                // TODO: Implement work-stealing logic
                // 1. Try to pop from own deque (LIFO)
                // 2. If empty, try to steal from random worker (FIFO)
                // 3. Execute task
                // 4. Repeat until shutdown

                while (!shutdown.get() || !taskDeque.isEmpty()) {
                    Runnable task = popTask();

                    if (task == null) {
                        task = stealTask();
                    }

                    if (task != null) {
                        try {
                            task.run();
                            tasksExecuted.incrementAndGet();
                        } catch (Exception e) {
                            System.err.println("Task execution failed in " + getName() + ": " + e.getMessage());
                        }
                    } else {
                        // No work available, sleep briefly
                        try {
                            Thread.sleep(1);
                        } catch (InterruptedException e) {
                            if (shutdown.get()) {
                                break;
                            }
                        }
                    }
                }
            }

            /**
             * Pop task from own deque (LIFO for cache locality)
             */
            private Runnable popTask() {
                // TODO: Pop from own deque (LIFO)
                return taskDeque.pollFirst();
            }

            /**
             * Steal task from a random victim's deque (FIFO for load distribution)
             */
            private Runnable stealTask() {
                // TODO: Implement work stealing
                // 1. Pick random victim (not self)
                // 2. Steal from victim's deque (FIFO end)
                // 3. Return stolen task or null

                if (poolSize <= 1) {
                    return null;
                }

                // Try stealing from random victims
                int attempts = poolSize * 2;
                for (int i = 0; i < attempts; i++) {
                    int victimIndex = random.nextInt(poolSize);
                    if (victimIndex == workerId) {
                        continue;
                    }

                    WorkStealingWorker victim = workers.get(victimIndex);
                    Runnable stolen = victim.taskDeque.pollLast();
                    if (stolen != null) {
                        tasksStolen.incrementAndGet();
                        return stolen;
                    }
                }

                return null;
            }

            public int getTasksExecuted() {
                return tasksExecuted.get();
            }

            public int getTasksStolen() {
                return tasksStolen.get();
            }
        }
    }

    /**
     * Task 3: Comparison with Java's ExecutorService
     */
    public static void compareWithExecutorService() {
        int poolSize = Runtime.getRuntime().availableProcessors();
        int taskCount = 10000;

        System.out.println("=== Thread Pool Comparison ===");
        System.out.println("Pool Size: " + poolSize);
        System.out.println("Task Count: " + taskCount);
        System.out.println();

        // Test 1: Fixed Thread Pool
        System.out.println("1. Fixed Thread Pool");
        long start1 = System.currentTimeMillis();
        FixedThreadPool fixedPool = new FixedThreadPool(poolSize);
        CountDownLatch latch1 = new CountDownLatch(taskCount);

        for (int i = 0; i < taskCount; i++) {
            final int taskId = i;
            fixedPool.submit(() -> {
                // Simulate work
                int sum = 0;
                for (int j = 0; j < 1000; j++) {
                    sum += j;
                }
                latch1.countDown();
            });
        }

        try {
            latch1.await();
            long elapsed1 = System.currentTimeMillis() - start1;
            System.out.println("Time: " + elapsed1 + " ms");
            fixedPool.shutdown();
            fixedPool.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Test 2: Work-Stealing Thread Pool
        System.out.println("\n2. Work-Stealing Thread Pool");
        long start2 = System.currentTimeMillis();
        WorkStealingThreadPool stealingPool = new WorkStealingThreadPool(poolSize);
        CountDownLatch latch2 = new CountDownLatch(taskCount);

        for (int i = 0; i < taskCount; i++) {
            stealingPool.submit(() -> {
                int sum = 0;
                for (int j = 0; j < 1000; j++) {
                    sum += j;
                }
                latch2.countDown();
            });
        }

        try {
            latch2.await();
            long elapsed2 = System.currentTimeMillis() - start2;
            System.out.println("Time: " + elapsed2 + " ms");
            stealingPool.shutdown();
            stealingPool.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Test 3: Java's ExecutorService
        System.out.println("\n3. Java ExecutorService (FixedThreadPool)");
        long start3 = System.currentTimeMillis();
        ExecutorService javaPool = Executors.newFixedThreadPool(poolSize);
        CountDownLatch latch3 = new CountDownLatch(taskCount);

        for (int i = 0; i < taskCount; i++) {
            javaPool.submit(() -> {
                int sum = 0;
                for (int j = 0; j < 1000; j++) {
                    sum += j;
                }
                latch3.countDown();
            });
        }

        try {
            latch3.await();
            long elapsed3 = System.currentTimeMillis() - start3;
            System.out.println("Time: " + elapsed3 + " ms");
            javaPool.shutdown();
            javaPool.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Test 4: Java's ForkJoinPool (work-stealing)
        System.out.println("\n4. Java ForkJoinPool (work-stealing)");
        long start4 = System.currentTimeMillis();
        ForkJoinPool forkJoinPool = new ForkJoinPool(poolSize);
        CountDownLatch latch4 = new CountDownLatch(taskCount);

        for (int i = 0; i < taskCount; i++) {
            forkJoinPool.submit(() -> {
                int sum = 0;
                for (int j = 0; j < 1000; j++) {
                    sum += j;
                }
                latch4.countDown();
            });
        }

        try {
            latch4.await();
            long elapsed4 = System.currentTimeMillis() - start4;
            System.out.println("Time: " + elapsed4 + " ms");
            forkJoinPool.shutdown();
            forkJoinPool.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    /**
     * Main method for testing
     */
    public static void main(String[] args) {
        System.out.println("Thread Pool Implementation Exercise\n");

        // Test basic fixed thread pool
        System.out.println("=== Testing Fixed Thread Pool ===");
        testFixedThreadPool();

        System.out.println("\n=== Testing Work-Stealing Thread Pool ===");
        testWorkStealingThreadPool();

        System.out.println("\n=== Performance Comparison ===");
        compareWithExecutorService();
    }

    private static void testFixedThreadPool() {
        FixedThreadPool pool = new FixedThreadPool(4);
        CountDownLatch latch = new CountDownLatch(20);

        for (int i = 0; i < 20; i++) {
            final int taskId = i;
            pool.submit(() -> {
                System.out.println("Task " + taskId + " executing on " + Thread.currentThread().getName());
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                latch.countDown();
            });
        }

        try {
            latch.await();
            System.out.println("All tasks completed!");
            pool.shutdown();
            pool.awaitTermination(5, TimeUnit.SECONDS);
            System.out.println("Pool shut down successfully");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    private static void testWorkStealingThreadPool() {
        WorkStealingThreadPool pool = new WorkStealingThreadPool(4);
        CountDownLatch latch = new CountDownLatch(20);

        for (int i = 0; i < 20; i++) {
            final int taskId = i;
            pool.submit(() -> {
                System.out.println("Task " + taskId + " executing on " + Thread.currentThread().getName());
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                latch.countDown();
            });
        }

        try {
            latch.await();
            System.out.println("All tasks completed!");
            pool.shutdown();
            pool.awaitTermination(5, TimeUnit.SECONDS);
            System.out.println("Pool shut down successfully");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
