package com.multiprocessor.basics;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import java.util.concurrent.TimeUnit;

import static org.assertj.core.api.Assertions.*;

/**
 * Tests for Exercise 01: Hello Threads
 */
class Exercise01_HelloThreadsTest {

    @Test
    void testCreateThread() {
        Thread thread = Exercise01_HelloThreads.createThread(1);
        assertThat(thread).isNotNull();
        assertThat(thread.getState()).isEqualTo(Thread.State.NEW);
    }

    @Test
    @Timeout(value = 5, unit = TimeUnit.SECONDS)
    void testCreateAndStartThreads() {
        Thread[] threads = Exercise01_HelloThreads.createAndStartThreads(3);

        assertThat(threads).isNotNull();
        assertThat(threads).hasSize(3);

        for (Thread thread : threads) {
            assertThat(thread).isNotNull();
            // Thread should be started or already finished
            assertThat(thread.getState()).isNotEqualTo(Thread.State.NEW);
        }
    }

    @Test
    @Timeout(value = 5, unit = TimeUnit.SECONDS)
    void testWaitForAllThreads() throws InterruptedException {
        Thread[] threads = new Thread[3];
        for (int i = 0; i < 3; i++) {
            final int id = i;
            threads[i] = new Thread(() -> {
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            threads[i].start();
        }

        Exercise01_HelloThreads.waitForAllThreads(threads);

        // All threads should be terminated
        for (Thread thread : threads) {
            assertThat(thread.getState()).isEqualTo(Thread.State.TERMINATED);
        }
    }

    @Test
    @Timeout(value = 5, unit = TimeUnit.SECONDS)
    void testFullWorkflow() {
        Thread[] threads = Exercise01_HelloThreads.createAndStartThreads(5);
        Exercise01_HelloThreads.waitForAllThreads(threads);

        for (Thread thread : threads) {
            assertThat(thread.getState()).isEqualTo(Thread.State.TERMINATED);
        }
    }
}
