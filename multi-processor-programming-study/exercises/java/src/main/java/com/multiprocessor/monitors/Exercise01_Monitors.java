package com.multiprocessor.monitors;

import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.Semaphore;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * Exercise: Monitors and Blocking Synchronization
 *
 * CONCEPT: High-level synchronization using monitors
 *
 * Monitors provide:
 * - Mutual exclusion (lock)
 * - Condition variables (wait/signal)
 * - Easier reasoning than low-level locks
 *
 * LEARNING OBJECTIVES:
 * - Use Lock and Condition in Java
 * - Implement classic synchronization problems
 * - Understand reader-writer locks
 * - Use semaphores correctly
 */
public class Exercise01_Monitors {

    /**
     * TODO: Implement Bounded Buffer using Lock and Condition
     *
     * Classic producer-consumer problem
     */
    public static class BoundedBuffer<T> {
        private final Queue<T> queue;
        private final int capacity;
        // TODO: Add Lock and two Conditions (notFull, notEmpty)

        public BoundedBuffer(int capacity) {
            this.capacity = capacity;
            this.queue = new LinkedList<>();
            // TODO: Initialize lock and conditions
        }

        /**
         * TODO: Implement put (producer)
         *
         * Wait while full, then add item
         */
        public void put(T item) throws InterruptedException {
            // TODO: Acquire lock
            // TODO: While queue is full, wait on notFull
            // TODO: Add item to queue
            // TODO: Signal notEmpty
            // TODO: Release lock
        }

        /**
         * TODO: Implement take (consumer)
         *
         * Wait while empty, then remove item
         */
        public T take() throws InterruptedException {
            // TODO: Acquire lock
            // TODO: While queue is empty, wait on notEmpty
            // TODO: Remove item from queue
            // TODO: Signal notFull
            // TODO: Release lock
            return null;
        }

        public int size() {
            return queue.size();
        }
    }

    /**
     * TODO: Implement Readers-Writers Lock
     *
     * Multiple readers OR single writer
     */
    public static class ReadersWritersLock {
        private int readers = 0;
        private boolean writer = false;
        // TODO: Add Lock and Conditions

        public ReadersWritersLock() {
            // TODO: Initialize
        }

        /**
         * TODO: Implement read lock
         */
        public void readLock() throws InterruptedException {
            // TODO: Wait while writer is active
            // TODO: Increment readers count
        }

        /**
         * TODO: Implement read unlock
         */
        public void readUnlock() {
            // TODO: Decrement readers count
            // TODO: Signal if no more readers
        }

        /**
         * TODO: Implement write lock
         */
        public void writeLock() throws InterruptedException {
            // TODO: Wait while any readers OR writer active
            // TODO: Set writer flag
        }

        /**
         * TODO: Implement write unlock
         */
        public void writeUnlock() {
            // TODO: Clear writer flag
            // TODO: Signal all waiting threads
        }
    }

    /**
     * TODO: Implement Dining Philosophers using Semaphores
     *
     * Classic deadlock avoidance problem
     */
    public static class DiningPhilosophers {
        private final int numPhilosophers;
        // TODO: Add semaphores for forks

        public DiningPhilosophers(int n) {
            this.numPhilosophers = n;
            // TODO: Initialize fork semaphores
        }

        /**
         * TODO: Implement pickUpForks
         *
         * Philosopher picks up left and right fork
         * Must avoid deadlock!
         */
        public void pickUpForks(int philosopherId) throws InterruptedException {
            // TODO: Implement deadlock-free solution
            // HINT: One approach - odd philosophers pick left first,
            //       even philosophers pick right first
        }

        /**
         * TODO: Implement putDownForks
         */
        public void putDownForks(int philosopherId) {
            // TODO: Release both forks
        }

        public void dine(int philosopherId) throws InterruptedException {
            System.out.println("Philosopher " + philosopherId + " thinking...");
            Thread.sleep(100);

            pickUpForks(philosopherId);
            System.out.println("Philosopher " + philosopherId + " eating...");
            Thread.sleep(100);
            putDownForks(philosopherId);

            System.out.println("Philosopher " + philosopherId + " done eating");
        }
    }

    /**
     * TODO: Implement Barrier using Condition Variables
     *
     * All threads wait until all arrive
     */
    public static class Barrier {
        private final int numThreads;
        private int count = 0;
        private int generation = 0;
        // TODO: Add Lock and Condition

        public Barrier(int n) {
            this.numThreads = n;
            // TODO: Initialize lock and condition
        }

        /**
         * TODO: Implement await
         *
         * Thread waits here until all threads arrive
         */
        public void await() throws InterruptedException {
            // TODO: Lock
            // TODO: Increment count
            // TODO: If count == numThreads:
            //   - Increment generation
            //   - Reset count
            //   - Signal all
            // TODO: Else wait on condition
            // TODO: Unlock
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Monitors and Blocking Test ===\n");

        testBoundedBuffer();
        testReadersWritersLock();
        testBarrier();
    }

    private static void testBoundedBuffer() throws InterruptedException {
        System.out.println("Testing Bounded Buffer:");

        BoundedBuffer<Integer> buffer = new BoundedBuffer<>(5);

        // Producers
        Thread[] producers = new Thread[3];
        for (int i = 0; i < producers.length; i++) {
            final int id = i;
            producers[i] = new Thread(() -> {
                try {
                    for (int j = 0; j < 10; j++) {
                        buffer.put(id * 100 + j);
                        System.out.println("Producer " + id + " put: " + (id * 100 + j));
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            producers[i].start();
        }

        // Consumers
        Thread[] consumers = new Thread[2];
        for (int i = 0; i < consumers.length; i++) {
            final int id = i;
            consumers[i] = new Thread(() -> {
                try {
                    for (int j = 0; j < 15; j++) {
                        Integer item = buffer.take();
                        System.out.println("Consumer " + id + " took: " + item);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            consumers[i].start();
        }

        for (Thread t : producers) t.join();
        for (Thread t : consumers) t.join();

        System.out.println("✅ Bounded buffer test completed\n");
    }

    private static void testReadersWritersLock() throws InterruptedException {
        System.out.println("Testing Readers-Writers Lock:");

        ReadersWritersLock rwLock = new ReadersWritersLock();
        int[] sharedData = {0};

        // Readers
        Thread[] readers = new Thread[5];
        for (int i = 0; i < readers.length; i++) {
            final int id = i;
            readers[i] = new Thread(() -> {
                try {
                    rwLock.readLock();
                    System.out.println("Reader " + id + " read: " + sharedData[0]);
                    Thread.sleep(50);
                    rwLock.readUnlock();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }

        // Writer
        Thread writer = new Thread(() -> {
            try {
                for (int i = 0; i < 3; i++) {
                    rwLock.writeLock();
                    sharedData[0]++;
                    System.out.println("Writer updated to: " + sharedData[0]);
                    Thread.sleep(100);
                    rwLock.writeUnlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        writer.start();
        for (Thread r : readers) r.start();

        writer.join();
        for (Thread r : readers) r.join();

        System.out.println("✅ Readers-Writers test completed\n");
    }

    private static void testBarrier() throws InterruptedException {
        System.out.println("Testing Barrier:");

        int numThreads = 5;
        Barrier barrier = new Barrier(numThreads);

        Thread[] threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            threads[i] = new Thread(() -> {
                try {
                    System.out.println("Thread " + id + " working...");
                    Thread.sleep((id + 1) * 100);
                    System.out.println("Thread " + id + " reached barrier");
                    barrier.await();
                    System.out.println("Thread " + id + " passed barrier");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) t.join();

        System.out.println("✅ Barrier test completed\n");
    }
}
