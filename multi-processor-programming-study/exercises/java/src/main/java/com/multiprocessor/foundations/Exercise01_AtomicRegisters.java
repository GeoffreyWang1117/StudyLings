package com.multiprocessor.foundations;

import java.util.concurrent.atomic.AtomicReference;

/**
 * Exercise: Atomic Registers
 *
 * CONCEPT: Building blocks of shared memory - atomic registers
 *
 * Register classifications:
 * - SRSW: Single Reader, Single Writer
 * - MRSW: Multiple Readers, Single Writer
 * - MRMW: Multiple Readers, Multiple Writers
 *
 * Register types:
 * - Safe: Read not concurrent with write returns old or new value
 * - Regular: Safe + read returns most recently written value or newer
 * - Atomic: Regular + linearizable
 *
 * LEARNING OBJECTIVES:
 * - Understand register abstractions
 * - Implement different register types
 * - Build MRMW from MRSW registers
 */
public class Exercise01_AtomicRegisters {

    /**
     * TODO: Implement a Simple SRSW Safe Register
     *
     * Single reader, single writer, safe semantics:
     * - Read concurrent with write may return any value
     * - Read not concurrent with write returns correct value
     */
    public static class SRSWSafeRegister<T> {
        // TODO: Add field to store value
        // HINT: Simple volatile variable is sufficient

        public SRSWSafeRegister(T initialValue) {
            // TODO: Initialize
        }

        /**
         * TODO: Implement write (called by single writer)
         */
        public void write(T value) {
            // TODO: Implement
        }

        /**
         * TODO: Implement read (called by single reader)
         */
        public T read() {
            // TODO: Implement
            return null;
        }
    }

    /**
     * TODO: Implement SRSW Regular Register
     *
     * Regular semantics: Read returns most recently written value or newer.
     * For SRSW, regular = atomic (with proper memory synchronization).
     */
    public static class SRSWRegularRegister<T> {
        private volatile T value;

        public SRSWRegularRegister(T initialValue) {
            this.value = initialValue;
        }

        public void write(T newValue) {
            this.value = newValue;
        }

        public T read() {
            return this.value;
        }
    }

    /**
     * TODO: Implement MRSW Regular Register
     *
     * Multiple readers, single writer.
     * Can be implemented using array of SRSW registers.
     */
    public static class MRSWRegularRegister<T> {
        private final int numReaders;
        // TODO: Array of SRSW registers, one per reader
        // HINT: Use SRSWRegularRegister<T>[] or AtomicReferenceArray

        public MRSWRegularRegister(int numReaders, T initialValue) {
            this.numReaders = numReaders;
            // TODO: Initialize array of SRSW registers
        }

        /**
         * TODO: Implement write
         *
         * Writer writes to all reader's registers
         *
         * @param value value to write
         */
        public void write(T value) {
            // TODO: Write value to all SRSW registers
        }

        /**
         * TODO: Implement read
         *
         * Reader reads from its own register
         *
         * @param readerId ID of the reader (0 to numReaders-1)
         * @return value read
         */
        public T read(int readerId) {
            // TODO: Read from the reader's dedicated register
            return null;
        }
    }

    /**
     * TODO: Implement MRMW Atomic Register using timestamps
     *
     * Multiple readers and writers.
     * Uses timestamps to order writes.
     */
    public static class MRMWAtomicRegister<T> {
        private static class StampedValue<T> {
            final long timestamp;
            final T value;

            StampedValue(long timestamp, T value) {
                this.timestamp = timestamp;
                this.value = value;
            }
        }

        // TODO: Add necessary fields
        // HINT: Use AtomicReference<StampedValue<T>>

        public MRMWAtomicRegister(T initialValue) {
            // TODO: Initialize with timestamp 0
        }

        /**
         * TODO: Implement atomic write
         *
         * Each write gets a unique timestamp (higher than all previous)
         *
         * @param value value to write
         */
        public void write(T value) {
            // TODO: Implement using timestamps
            // HINT: Read current timestamp, increment, CAS with new value
        }

        /**
         * TODO: Implement atomic read
         *
         * Returns value with highest timestamp
         *
         * @return current value
         */
        public T read() {
            // TODO: Implement
            return null;
        }
    }

    /**
     * TODO: Implement bounded MRMW register
     *
     * Uses bounded timestamps (wraps around).
     * More practical than unbounded.
     */
    public static class BoundedMRMWRegister<T> {
        private static class StampedValue<T> {
            final int timestamp; // Bounded timestamp
            final T value;

            StampedValue(int timestamp, T value) {
                this.timestamp = timestamp;
                this.value = value;
            }
        }

        private static final int MAX_TIMESTAMP = 1000000;
        private AtomicReference<StampedValue<T>> register;

        public BoundedMRMWRegister(T initialValue) {
            this.register = new AtomicReference<>(new StampedValue<>(0, initialValue));
        }

        /**
         * TODO: Implement write with bounded timestamp
         */
        public void write(T value) {
            // TODO: Implement
            // HINT: Increment timestamp modulo MAX_TIMESTAMP
        }

        /**
         * TODO: Implement read
         */
        public T read() {
            return register.get().value;
        }
    }

    /**
     * Demonstration and testing
     */
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Atomic Registers Test ===\n");

        testSRSWRegister();
        testMRSWRegister();
        testMRMWRegister();
    }

    private static void testSRSWRegister() throws InterruptedException {
        System.out.println("Testing SRSW Regular Register:");

        SRSWRegularRegister<Integer> register = new SRSWRegularRegister<>(0);

        Thread writer = new Thread(() -> {
            for (int i = 1; i <= 100; i++) {
                register.write(i);
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        Thread reader = new Thread(() -> {
            Integer lastValue = 0;
            for (int i = 0; i < 50; i++) {
                Integer value = register.read();
                if (value != null && value >= lastValue) {
                    lastValue = value;
                }
                try {
                    Thread.sleep(20);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            System.out.println("Last value read: " + lastValue);
        });

        writer.start();
        reader.start();
        writer.join();
        reader.join();

        System.out.println("✅ SRSW test completed\n");
    }

    private static void testMRSWRegister() throws InterruptedException {
        System.out.println("Testing MRSW Regular Register:");

        int numReaders = 3;
        MRSWRegularRegister<String> register = new MRSWRegularRegister<>(numReaders, "initial");

        Thread writer = new Thread(() -> {
            for (int i = 0; i < 50; i++) {
                register.write("value-" + i);
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        Thread[] readers = new Thread[numReaders];
        for (int i = 0; i < numReaders; i++) {
            final int readerId = i;
            readers[i] = new Thread(() -> {
                for (int j = 0; j < 30; j++) {
                    String value = register.read(readerId);
                    System.out.println("Reader " + readerId + " read: " + value);
                    try {
                        Thread.sleep(15);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }

        writer.start();
        for (Thread reader : readers) {
            reader.start();
        }

        writer.join();
        for (Thread reader : readers) {
            reader.join();
        }

        System.out.println("✅ MRSW test completed\n");
    }

    private static void testMRMWRegister() throws InterruptedException {
        System.out.println("Testing MRMW Atomic Register:");

        MRMWAtomicRegister<Integer> register = new MRMWAtomicRegister<>(0);
        int numThreads = 5;
        int opsPerThread = 100;

        Thread[] threads = new Thread[numThreads];
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < opsPerThread; j++) {
                    register.write(threadId * opsPerThread + j);
                    Integer value = register.read();
                    // Value should be valid (not null)
                    if (value == null) {
                        System.err.println("Read null value!");
                    }
                }
            });
            threads[i].start();
        }

        for (Thread t : threads) {
            t.join();
        }

        Integer finalValue = register.read();
        System.out.println("Final value: " + finalValue);
        System.out.println(finalValue != null ? "✅ PASS" : "❌ FAIL");
    }
}
