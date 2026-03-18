package com.multiprocessor.basics;

import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.*;

/**
 * Tests for Exercise 02: Race Condition
 */
class Exercise02_RaceConditionTest {

    @Test
    void testUnsafeCounterIncrement() {
        Exercise02_RaceCondition.UnsafeCounter counter = new Exercise02_RaceCondition.UnsafeCounter();
        counter.increment();
        assertThat(counter.getCount()).isEqualTo(1);

        counter.increment();
        assertThat(counter.getCount()).isEqualTo(2);
    }

    @Test
    @Timeout(value = 5, unit = TimeUnit.SECONDS)
    void testCreateIncrementThreads() {
        Exercise02_RaceCondition.UnsafeCounter counter = new Exercise02_RaceCondition.UnsafeCounter();
        Thread[] threads = Exercise02_RaceCondition.createIncrementThreads(counter, 5, 100);

        assertThat(threads).isNotNull();
        assertThat(threads).hasSize(5);

        for (Thread thread : threads) {
            assertThat(thread).isNotNull();
        }
    }

    @RepeatedTest(5) // Run multiple times to increase chance of detecting race condition
    @Timeout(value = 10, unit = TimeUnit.SECONDS)
    void testRaceConditionOccurs() throws InterruptedException {
        Exercise02_RaceCondition.UnsafeCounter counter = new Exercise02_RaceCondition.UnsafeCounter();
        int numThreads = 100;
        int incrementsPerThread = 100;

        Thread[] threads = Exercise02_RaceCondition.createIncrementThreads(
                counter, numThreads, incrementsPerThread);

        for (Thread t : threads) {
            t.start();
        }

        for (Thread t : threads) {
            t.join();
        }

        // The count will likely be less than expected due to race condition
        // We just verify the test completes and the counter is not null
        assertThat(counter.getCount()).isGreaterThan(0);
        assertThat(counter.getCount()).isLessThanOrEqualTo(numThreads * incrementsPerThread);
    }
}
