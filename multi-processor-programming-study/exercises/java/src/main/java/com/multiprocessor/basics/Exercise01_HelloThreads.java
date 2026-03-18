package com.multiprocessor.basics;

/**
 * Exercise 01: Hello Threads!
 *
 * CONCEPT: Introduction to thread creation and execution
 *
 * In this exercise, you'll learn how to create and run threads in Java.
 * Threads are the fundamental unit of concurrent execution.
 *
 * LEARNING OBJECTIVES:
 * - Create threads using Thread class
 * - Implement the Runnable interface
 * - Understand thread lifecycle
 *
 * TODO: Complete the methods marked with TODO comments
 */
public class Exercise01_HelloThreads {

    /**
     * TODO: Create and return a thread that prints "Hello from Thread [id]!"
     *
     * @param threadId The ID to include in the message
     * @return A new Thread object
     */
    public static Thread createThread(int threadId) {
        // TODO: Implement this method
        // HINT: Use a lambda expression or anonymous Runnable
        return null;
    }

    /**
     * TODO: Create multiple threads and start them all
     *
     * @param count Number of threads to create
     * @return Array of started threads
     */
    public static Thread[] createAndStartThreads(int count) {
        // TODO: Implement this method
        // HINT: Create an array, populate it with threads, and start each one
        return null;
    }

    /**
     * TODO: Wait for all threads to complete
     *
     * @param threads Array of threads to wait for
     */
    public static void waitForAllThreads(Thread[] threads) {
        // TODO: Implement this method
        // HINT: Use the join() method on each thread
    }

    /**
     * Main method for testing (you can run this directly)
     */
    public static void main(String[] args) {
        System.out.println("Creating threads...");
        Thread[] threads = createAndStartThreads(5);

        System.out.println("Waiting for threads to complete...");
        waitForAllThreads(threads);

        System.out.println("All threads completed!");
    }
}
