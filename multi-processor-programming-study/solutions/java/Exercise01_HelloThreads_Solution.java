package com.multiprocessor.basics;

/**
 * SOLUTION for Exercise 01: Hello Threads!
 *
 * This file contains the reference implementation.
 * Try to solve the exercise yourself before looking at this!
 */
public class Exercise01_HelloThreads_Solution {

    /**
     * SOLUTION: Create and return a thread that prints "Hello from Thread [id]!"
     */
    public static Thread createThread(int threadId) {
        return new Thread(() -> {
            System.out.println("Hello from Thread " + threadId + "!");
        });
    }

    /**
     * SOLUTION: Create multiple threads and start them all
     */
    public static Thread[] createAndStartThreads(int count) {
        Thread[] threads = new Thread[count];
        for (int i = 0; i < count; i++) {
            threads[i] = createThread(i);
            threads[i].start();
        }
        return threads;
    }

    /**
     * SOLUTION: Wait for all threads to complete
     */
    public static void waitForAllThreads(Thread[] threads) {
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.err.println("Thread interrupted: " + e.getMessage());
            }
        }
    }

    /**
     * Main method for testing
     */
    public static void main(String[] args) {
        System.out.println("Creating threads...");
        Thread[] threads = createAndStartThreads(5);

        System.out.println("Waiting for threads to complete...");
        waitForAllThreads(threads);

        System.out.println("All threads completed!");
    }
}
