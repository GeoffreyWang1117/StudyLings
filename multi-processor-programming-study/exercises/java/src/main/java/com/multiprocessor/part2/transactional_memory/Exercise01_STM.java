package com.multiprocessor.part2.transactional_memory;

import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicReference;
import java.util.HashMap;
import java.util.Map;

/**
 * Exercise: Software Transactional Memory (STM)
 *
 * CONCEPT: Transaction-based synchronization
 *
 * STM provides:
 * - Atomic: All or nothing execution
 * - Consistent: Transactions see consistent state
 * - Isolated: Transactions don't interfere
 *
 * Implementation Strategies:
 * - Lock-based: Use locks with two-phase locking
 * - Lock-free: Use version numbers and CAS
 * - MVCC: Multi-version concurrency control
 *
 * LEARNING OBJECTIVES:
 * - Understand transactional memory concepts
 * - Implement simple STM
 * - Handle transaction conflicts
 * - Compare with traditional locking
 */
public class Exercise01_STM {

    /**
     * TODO: Implement TVar (Transactional Variable)
     *
     * A variable that can be read/written within transactions
     */
    public static class TVar<T> {
        private static class Version<T> {
            final long version;
            final T value;

            Version(long version, T value) {
                this.version = version;
                this.value = value;
            }
        }

        private final AtomicReference<Version<T>> ref;

        public TVar(T initialValue) {
            this.ref = new AtomicReference<>(new Version<>(0, initialValue));
        }

        /**
         * TODO: Read value at specific version
         */
        T read(long version) {
            Version<T> current = ref.get();
            if (current.version <= version) {
                return current.value;
            }
            // In real STM, would search version history
            return current.value;
        }

        /**
         * TODO: Try to commit new value
         */
        boolean commit(long readVersion, T newValue, long writeVersion) {
            Version<T> current = ref.get();
            // Check if anyone modified since we read
            if (current.version != readVersion) {
                return false; // Conflict!
            }

            // Try to CAS new version
            Version<T> newVersion = new Version<>(writeVersion, newValue);
            return ref.compareAndSet(current, newVersion);
        }

        T getValue() {
            return ref.get().value;
        }
    }

    /**
     * TODO: Implement Transaction
     *
     * Tracks reads and writes, handles commit/abort
     */
    public static class Transaction {
        private static final AtomicLong globalClock = new AtomicLong(0);

        private final long readVersion;
        private final Map<TVar<?>, Object> readSet;
        private final Map<TVar<?>, Object> writeSet;

        public Transaction() {
            this.readVersion = globalClock.get();
            this.readSet = new HashMap<>();
            this.writeSet = new HashMap<>();
        }

        /**
         * TODO: Read TVar within transaction
         */
        @SuppressWarnings("unchecked")
        public <T> T read(TVar<T> tvar) {
            // Check write set first (read-your-writes)
            if (writeSet.containsKey(tvar)) {
                return (T) writeSet.get(tvar);
            }

            // Check read set
            if (readSet.containsKey(tvar)) {
                return (T) readSet.get(tvar);
            }

            // TODO: Read from TVar and add to read set
            T value = tvar.read(readVersion);
            readSet.put(tvar, value);
            return value;
        }

        /**
         * TODO: Write TVar within transaction
         */
        public <T> void write(TVar<T> tvar, T value) {
            // TODO: Add to write set (doesn't modify TVar yet)
            writeSet.put(tvar, value);
        }

        /**
         * TODO: Commit transaction
         *
         * Validate read set, then apply writes
         */
        @SuppressWarnings("unchecked")
        public boolean commit() {
            // TODO: Get write version (increment global clock)
            long writeVersion = globalClock.incrementAndGet();

            // TODO: Validate read set (check no conflicts)
            for (Map.Entry<TVar<?>, Object> entry : readSet.entrySet()) {
                TVar<?> tvar = entry.getKey();
                // Skip if in write set
                if (writeSet.containsKey(tvar)) {
                    continue;
                }
                // Check version hasn't changed
                Object readValue = entry.getValue();
                Object currentValue = tvar.read(readVersion);
                if (!readValue.equals(currentValue)) {
                    return false; // Conflict! Abort
                }
            }

            // TODO: Apply writes using CAS
            for (Map.Entry<TVar<?>, Object> entry : writeSet.entrySet()) {
                TVar tvar = entry.getKey();
                Object newValue = entry.getValue();
                if (!tvar.commit(readVersion, newValue, writeVersion)) {
                    // Conflict! In real STM, would need to undo previous writes
                    return false;
                }
            }

            return true; // Success!
        }
    }

    /**
     * TODO: Implement STM runtime
     *
     * Provides retry logic for transactions
     */
    public static class STM {
        private static final int MAX_RETRIES = 1000;

        /**
         * TODO: Execute transaction with automatic retry
         */
        public static <T> T atomically(TransactionBody<T> body) {
            for (int retry = 0; retry < MAX_RETRIES; retry++) {
                Transaction tx = new Transaction();
                try {
                    T result = body.run(tx);
                    if (tx.commit()) {
                        return result;
                    }
                    // Commit failed, retry
                } catch (Exception e) {
                    // Transaction aborted, retry
                }

                // Exponential backoff
                if (retry > 0) {
                    try {
                        Thread.sleep(1 << Math.min(retry, 10));
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        throw new RuntimeException("Transaction interrupted");
                    }
                }
            }
            throw new RuntimeException("Transaction failed after " + MAX_RETRIES + " retries");
        }

        @FunctionalInterface
        public interface TransactionBody<T> {
            T run(Transaction tx) throws Exception;
        }
    }

    /**
     * Example: Bank account transfer using STM
     */
    static class BankAccount {
        private final TVar<Integer> balance;
        private final String name;

        public BankAccount(String name, int initialBalance) {
            this.name = name;
            this.balance = new TVar<>(initialBalance);
        }

        public void transfer(BankAccount to, int amount) {
            STM.atomically(tx -> {
                int fromBalance = tx.read(balance);
                int toBalance = tx.read(to.balance);

                if (fromBalance < amount) {
                    throw new RuntimeException("Insufficient funds");
                }

                tx.write(balance, fromBalance - amount);
                tx.write(to.balance, toBalance + amount);

                return null;
            });
        }

        public int getBalance() {
            return balance.getValue();
        }

        public String getName() {
            return name;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Software Transactional Memory Test ===\n");

        testBasicSTM();
        testBankTransfer();
        demonstrateSTMProperties();
    }

    private static void testBasicSTM() {
        System.out.println("Testing Basic STM Operations:");

        TVar<Integer> x = new TVar<>(10);
        TVar<Integer> y = new TVar<>(20);

        // Simple transaction
        STM.atomically(tx -> {
            int xVal = tx.read(x);
            int yVal = tx.read(y);
            tx.write(x, xVal + 5);
            tx.write(y, yVal - 5);
            return null;
        });

        System.out.println("x = " + x.getValue() + " (expected 15)");
        System.out.println("y = " + y.getValue() + " (expected 15)");
        System.out.println(x.getValue() == 15 && y.getValue() == 15 ?
                          "✅ PASS\n" : "❌ FAIL\n");
    }

    private static void testBankTransfer() throws InterruptedException {
        System.out.println("Testing Concurrent Bank Transfers:");

        BankAccount alice = new BankAccount("Alice", 1000);
        BankAccount bob = new BankAccount("Bob", 1000);

        int numThreads = 10;
        Thread[] threads = new Thread[numThreads];

        // Concurrent transfers
        for (int i = 0; i < numThreads; i++) {
            final int id = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    try {
                        if (id % 2 == 0) {
                            alice.transfer(bob, 10);
                        } else {
                            bob.transfer(alice, 10);
                        }
                    } catch (Exception e) {
                        // Ignore insufficient funds errors
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        int totalBalance = alice.getBalance() + bob.getBalance();
        System.out.println("Alice: $" + alice.getBalance());
        System.out.println("Bob: $" + bob.getBalance());
        System.out.println("Total: $" + totalBalance + " (expected 2000)");
        System.out.println(totalBalance == 2000 ? "✅ PASS\n" : "❌ FAIL\n");
    }

    private static void demonstrateSTMProperties() {
        System.out.println("=== STM Properties ===");
        System.out.println();
        System.out.println("Advantages:");
        System.out.println("  ✅ Composable - transactions can be nested");
        System.out.println("  ✅ No deadlocks - no lock ordering issues");
        System.out.println("  ✅ Automatic retry - conflicts handled transparently");
        System.out.println("  ✅ Clean syntax - looks like sequential code");
        System.out.println();
        System.out.println("Challenges:");
        System.out.println("  ⚠️  Performance overhead from version tracking");
        System.out.println("  ⚠️  Contention can cause many retries");
        System.out.println("  ⚠️  Side effects must be handled carefully");
        System.out.println();
        System.out.println("💡 STM is great for complex atomic operations");
        System.out.println("💡 Traditional locks may be better for simple operations");
    }
}
