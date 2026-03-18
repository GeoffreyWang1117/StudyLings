package com.multiprocessor.basics;

/**
 * Exercise 03: Basic Synchronization
 *
 * CONCEPT: Using synchronized keyword to prevent race conditions
 *
 * Java provides the 'synchronized' keyword to ensure mutual exclusion -
 * only one thread can execute a synchronized block/method at a time.
 *
 * LEARNING OBJECTIVES:
 * - Use synchronized methods
 * - Understand mutual exclusion
 * - Fix race conditions with synchronization
 *
 * TODO: Make the counter thread-safe using synchronization
 */
public class Exercise03_Synchronization {

    /**
     * TODO: Implement a thread-safe counter using synchronized
     */
    public static class SafeCounter {
        private int count = 0;

        /**
         * TODO: Make this method thread-safe using 'synchronized' keyword
         */
        public void increment() {
            // TODO: Add synchronized and implement increment
            // HINT: Use 'synchronized' keyword in the method signature
        }

        /**
         * TODO: Make this method thread-safe as well
         */
        public int getCount() {
            // TODO: Should this be synchronized too? Why or why not?
            return count;
        }

        /**
         * TODO: Implement a decrement method (also thread-safe)
         */
        public void decrement() {
            // TODO: Implement this
        }
    }

    /**
     * TODO: Implement a thread-safe bank account
     *
     * This class represents a bank account that can be accessed by multiple threads.
     * It must ensure that:
     * - Balance never goes negative (if initial balance is non-negative)
     * - Deposits and withdrawals are atomic
     * - Balance queries are consistent
     */
    public static class BankAccount {
        private double balance;

        public BankAccount(double initialBalance) {
            this.balance = initialBalance;
        }

        /**
         * TODO: Implement thread-safe deposit
         * @param amount Amount to deposit (must be positive)
         */
        public void deposit(double amount) {
            // TODO: Implement with synchronization
            // HINT: Validate amount is positive
        }

        /**
         * TODO: Implement thread-safe withdrawal
         * @param amount Amount to withdraw
         * @return true if withdrawal successful, false if insufficient funds
         */
        public boolean withdraw(double amount) {
            // TODO: Implement with synchronization
            // HINT: Check if balance >= amount before withdrawing
            return false;
        }

        /**
         * TODO: Implement thread-safe balance query
         */
        public double getBalance() {
            // TODO: Implement with synchronization
            return 0.0;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Testing SafeCounter ===");
        testSafeCounter();

        System.out.println("\n=== Testing BankAccount ===");
        testBankAccount();
    }

    private static void testSafeCounter() throws InterruptedException {
        SafeCounter counter = new SafeCounter();
        int numThreads = 10;
        int incrementsPerThread = 1000;

        Thread[] threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment();
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        int expected = numThreads * incrementsPerThread;
        int actual = counter.getCount();

        System.out.println("Expected: " + expected);
        System.out.println("Actual: " + actual);
        System.out.println(actual == expected ? "✅ PASS" : "❌ FAIL");
    }

    private static void testBankAccount() throws InterruptedException {
        BankAccount account = new BankAccount(1000.0);

        // Multiple threads depositing and withdrawing
        Thread[] threads = new Thread[20];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    account.deposit(10.0);
                }
            });
        }
        for (int i = 10; i < 20; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    account.withdraw(10.0);
                }
            });
        }

        for (Thread t : threads) {
            t.start();
        }
        for (Thread t : threads) {
            t.join();
        }

        double expectedBalance = 1000.0; // 10 threads * 100 * $10 - 10 threads * 100 * $10
        double actualBalance = account.getBalance();

        System.out.println("Expected balance: $" + expectedBalance);
        System.out.println("Actual balance: $" + actualBalance);
        System.out.println(Math.abs(actualBalance - expectedBalance) < 0.01 ? "✅ PASS" : "❌ FAIL");
    }
}
