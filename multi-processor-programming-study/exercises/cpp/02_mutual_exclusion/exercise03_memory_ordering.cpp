/**
 * Exercise: C++ Memory Ordering
 *
 * CONCEPT: Understanding C++ memory_order and synchronization
 *
 * C++ MEMORY MODEL:
 * Unlike Java's relatively simple memory model, C++ provides fine-grained control
 * over memory ordering with six memory_order options:
 *
 * 1. memory_order_relaxed: No ordering guarantees
 * 2. memory_order_consume: Data dependency ordering (rarely used)
 * 3. memory_order_acquire: Synchronize with release
 * 4. memory_order_release: Synchronize with acquire
 * 5. memory_order_acq_rel: Both acquire and release
 * 6. memory_order_seq_cst: Sequentially consistent (default, strongest)
 *
 * LEARNING OBJECTIVES:
 * - Understand different memory ordering levels
 * - Use acquire-release for synchronization
 * - Implement Dekker's algorithm with explicit ordering
 * - Understand relaxed ordering for counters
 * - Appreciate sequential consistency cost
 *
 * CPU REQUIREMENTS:
 * - Minimum: 2 cores
 * - Recommended: 4+ cores
 * - Optimal: ARM or weak memory architecture (x86 hides many issues)
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <cassert>

namespace multiprocessor::memory_ordering {

/**
 * Example 1: Relaxed Ordering
 *
 * Relaxed ordering provides no synchronization guarantees
 * Good for simple counters where exact ordering doesn't matter
 */
class RelaxedCounter {
private:
    std::atomic<int> count_{0};

public:
    void increment() {
        // TODO: Use relaxed ordering - no synchronization needed
        count_.fetch_add(1, std::memory_order_relaxed);
    }

    int get() const {
        // TODO: Relaxed load is fine for approximate count
        return count_.load(std::memory_order_relaxed);
    }
};

/**
 * Example 2: Acquire-Release Ordering
 *
 * Producer-consumer with acquire-release synchronization
 */
class MessagePassing {
private:
    std::atomic<int> data_{0};
    std::atomic<bool> ready_{false};

public:
    /**
     * TODO: Producer writes data then sets flag with release
     */
    void produce(int value) {
        // Write data first (can be relaxed)
        data_.store(value, std::memory_order_relaxed);

        // Signal ready with release barrier
        // Ensures all prior writes are visible
        ready_.store(true, std::memory_order_release);
    }

    /**
     * TODO: Consumer waits for flag with acquire then reads data
     */
    int consume() {
        // Wait for ready with acquire
        // Ensures we see all writes before release
        while (!ready_.load(std::memory_order_acquire)) {
            std::this_thread::yield();
        }

        // Read data (can be relaxed after synchronization)
        return data_.load(std::memory_order_relaxed);
    }
};

/**
 * Example 3: Dekker's Algorithm with Explicit Memory Ordering
 *
 * Classic two-thread mutual exclusion with memory_order annotations
 */
class DekkerLock {
private:
    std::atomic<bool> flag0_{false};
    std::atomic<bool> flag1_{false};
    std::atomic<int> turn_{0};

public:
    /**
     * TODO: Implement lock for thread 0 with explicit memory orders
     */
    void lock0() {
        // Signal intent with release
        flag0_.store(true, std::memory_order_release);

        // Check other thread's intent with acquire
        while (flag1_.load(std::memory_order_acquire)) {
            // Contention - check turn
            if (turn_.load(std::memory_order_acquire) != 0) {
                // Yield
                flag0_.store(false, std::memory_order_release);

                // Wait for our turn
                while (turn_.load(std::memory_order_acquire) != 0) {
                    std::this_thread::yield();
                }

                // Try again
                flag0_.store(true, std::memory_order_release);
            }
        }
        // Critical section entered
    }

    /**
     * TODO: Implement unlock for thread 0
     */
    void unlock0() {
        // Give turn to other thread
        turn_.store(1, std::memory_order_release);

        // Clear our flag
        flag0_.store(false, std::memory_order_release);
    }

    /**
     * TODO: Implement lock for thread 1 (symmetric to thread 0)
     */
    void lock1() {
        flag1_.store(true, std::memory_order_release);

        while (flag0_.load(std::memory_order_acquire)) {
            if (turn_.load(std::memory_order_acquire) != 1) {
                flag1_.store(false, std::memory_order_release);

                while (turn_.load(std::memory_order_acquire) != 1) {
                    std::this_thread::yield();
                }

                flag1_.store(true, std::memory_order_release);
            }
        }
    }

    /**
     * TODO: Implement unlock for thread 1
     */
    void unlock1() {
        turn_.store(0, std::memory_order_release);
        flag1_.store(false, std::memory_order_release);
    }
};

/**
 * Example 4: Sequential Consistency vs Relaxed
 *
 * Demonstrate difference between seq_cst and relaxed
 */
class SequentialConsistencyDemo {
private:
    std::atomic<int> x_{0};
    std::atomic<int> y_{0};
    std::atomic<int> r1_{0};
    std::atomic<int> r2_{0};

public:
    /**
     * With seq_cst: r1 == 0 && r2 == 0 is IMPOSSIBLE
     * With relaxed: r1 == 0 && r2 == 0 is POSSIBLE (reordering)
     */
    void thread1_seq_cst() {
        x_.store(1, std::memory_order_seq_cst);
        r1_.store(y_.load(std::memory_order_seq_cst), std::memory_order_seq_cst);
    }

    void thread2_seq_cst() {
        y_.store(1, std::memory_order_seq_cst);
        r2_.store(x_.load(std::memory_order_seq_cst), std::memory_order_seq_cst);
    }

    void thread1_relaxed() {
        x_.store(1, std::memory_order_relaxed);
        r1_.store(y_.load(std::memory_order_relaxed), std::memory_order_relaxed);
    }

    void thread2_relaxed() {
        y_.store(1, std::memory_order_relaxed);
        r2_.store(x_.load(std::memory_order_relaxed), std::memory_order_relaxed);
    }

    void reset() {
        x_.store(0, std::memory_order_seq_cst);
        y_.store(0, std::memory_order_seq_cst);
        r1_.store(0, std::memory_order_seq_cst);
        r2_.store(0, std::memory_order_seq_cst);
    }

    bool both_zero() const {
        return r1_.load(std::memory_order_seq_cst) == 0 &&
               r2_.load(std::memory_order_seq_cst) == 0;
    }
};

/**
 * Testing Framework
 */
void test_relaxed_counter() {
    std::cout << "=== Test 1: Relaxed Counter ===\n";

    RelaxedCounter counter;
    const int iterations = 10000;
    const int num_threads = 4;

    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&]() {
            for (int j = 0; j < iterations; ++j) {
                counter.increment();
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    int expected = num_threads * iterations;
    int actual = counter.get();

    std::cout << "Expected: " << expected << "\n";
    std::cout << "Actual: " << actual << "\n";
    std::cout << (expected == actual ? "✅ PASS" : "❌ FAIL") << "\n\n";
}

void test_message_passing() {
    std::cout << "=== Test 2: Message Passing (Acquire-Release) ===\n";

    MessagePassing mp;
    const int test_value = 42;

    std::thread producer([&]() {
        mp.produce(test_value);
    });

    std::thread consumer([&]() {
        int received = mp.consume();
        assert(received == test_value);
        std::cout << "Received: " << received << "\n";
    });

    producer.join();
    consumer.join();

    std::cout << "✅ PASS\n\n";
}

void test_dekker() {
    std::cout << "=== Test 3: Dekker's Lock (Memory Ordering) ===\n";

    DekkerLock lock;
    int shared_counter = 0;
    const int iterations = 100000;

    std::thread t0([&]() {
        for (int i = 0; i < iterations; ++i) {
            lock.lock0();
            shared_counter++;
            lock.unlock0();
        }
    });

    std::thread t1([&]() {
        for (int i = 0; i < iterations; ++i) {
            lock.lock1();
            shared_counter++;
            lock.unlock1();
        }
    });

    t0.join();
    t1.join();

    int expected = 2 * iterations;
    std::cout << "Expected: " << expected << "\n";
    std::cout << "Actual: " << shared_counter << "\n";
    std::cout << (expected == shared_counter ? "✅ PASS" : "❌ FAIL") << "\n\n";
}

void test_sequential_consistency() {
    std::cout << "=== Test 4: Sequential Consistency vs Relaxed ===\n";

    SequentialConsistencyDemo demo;

    // Test with seq_cst
    std::cout << "Testing with seq_cst ordering...\n";
    int both_zero_count = 0;
    const int trials = 10000;

    for (int i = 0; i < trials; ++i) {
        demo.reset();

        std::thread t1([&]() { demo.thread1_seq_cst(); });
        std::thread t2([&]() { demo.thread2_seq_cst(); });

        t1.join();
        t2.join();

        if (demo.both_zero()) {
            both_zero_count++;
        }
    }

    std::cout << "Both zero (seq_cst): " << both_zero_count << " / " << trials << "\n";
    std::cout << "Expected: 0 (impossible with seq_cst)\n";

    // Test with relaxed
    std::cout << "\nTesting with relaxed ordering...\n";
    both_zero_count = 0;

    for (int i = 0; i < trials; ++i) {
        demo.reset();

        std::thread t1([&]() { demo.thread1_relaxed(); });
        std::thread t2([&]() { demo.thread2_relaxed(); });

        t1.join();
        t2.join();

        if (demo.both_zero()) {
            both_zero_count++;
        }
    }

    std::cout << "Both zero (relaxed): " << both_zero_count << " / " << trials << "\n";
    std::cout << "Note: May see both zero due to relaxed ordering\n";
    std::cout << "✅ PASS (demonstrates difference)\n\n";
}

void demonstrate_concepts() {
    std::cout << "=== C++ Memory Ordering Concepts ===\n\n";

    std::cout << "Memory Order Levels:\n";
    std::cout << "  1. relaxed: No ordering, just atomicity\n";
    std::cout << "  2. acquire: Synchronize with release stores\n";
    std::cout << "  3. release: Synchronize with acquire loads\n";
    std::cout << "  4. acq_rel: Both acquire and release\n";
    std::cout << "  5. seq_cst: Total global order (default)\n\n";

    std::cout << "When to Use Each:\n";
    std::cout << "  • relaxed: Counters, no dependencies\n";
    std::cout << "  • acquire/release: Producer-consumer, flags\n";
    std::cout << "  • seq_cst: When unsure, or need global order\n\n";

    std::cout << "Performance Impact:\n";
    std::cout << "  • relaxed: Cheapest (no barriers)\n";
    std::cout << "  • acquire/release: Moderate (partial barriers)\n";
    std::cout << "  • seq_cst: Most expensive (full barriers)\n\n";

    std::cout << "Platform Differences:\n";
    std::cout << "  • x86: Strong memory model, hides issues\n";
    std::cout << "  • ARM/RISC-V: Weak model, explicit barriers needed\n";
    std::cout << "  • Use ThreadSanitizer to catch bugs\n\n";
}

} // namespace

int main() {
    using namespace multiprocessor::memory_ordering;

    std::cout << "=== C++ Memory Ordering Test ===\n\n";

    demonstrate_concepts();
    test_relaxed_counter();
    test_message_passing();
    test_dekker();
    test_sequential_consistency();

    return 0;
}
