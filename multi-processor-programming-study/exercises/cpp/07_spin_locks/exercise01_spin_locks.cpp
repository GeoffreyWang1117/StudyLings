/**
 * Exercise: Spin Locks (C++20)
 *
 * CONCEPT: Different implementations of spin locks and their trade-offs
 *
 * Spin lock types:
 * - TAS (Test-and-Set): Simple but causes bus traffic
 * - TTAS (Test-and-Test-and-Set): Better - spins locally
 * - Backoff: TTAS with exponential backoff
 * - MCS: Queue-based, truly scalable
 *
 * LEARNING OBJECTIVES:
 * - Implement various spin lock algorithms in C++
 * - Understand cache coherence implications
 * - Use std::atomic with different memory orderings
 * - Compare performance characteristics
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <chrono>
#include <iomanip>

namespace multiprocessor::spin_locks {

/**
 * TODO: Implement TAS Lock (Test-and-Set)
 *
 * Simple atomic test-and-set lock
 * Problem: Causes cache coherence traffic on every spin
 */
class TASLock {
private:
    // TODO: Add std::atomic<bool> state

public:
    TASLock() {
        // TODO: Initialize to false (unlocked)
    }

    /**
     * TODO: Implement lock using test-and-set
     *
     * Keep trying exchange(true) until it returns false
     */
    void lock() {
        // TODO: Implement
        // HINT: while (state.exchange(true, std::memory_order_acquire)) { }
    }

    /**
     * TODO: Implement unlock
     */
    void unlock() {
        // TODO: Set state to false with release semantics
        // HINT: state.store(false, std::memory_order_release)
    }
};

/**
 * TODO: Implement TTAS Lock (Test-and-Test-and-Set)
 *
 * Improvement over TAS: Test locally before test-and-set
 * Reduces bus traffic significantly
 */
class TTASLock {
private:
    // TODO: Add std::atomic<bool> state

public:
    TTASLock() {
        // TODO: Initialize
    }

    /**
     * TODO: Implement TTAS lock
     *
     * while (true) {
     *   while (state.load()) { } // Spin locally (read-only)
     *   if (!state.exchange(true)) return; // Try to acquire
     * }
     */
    void lock() {
        // TODO: Implement TTAS pattern
        // HINT: Use memory_order_relaxed for spinning
        // HINT: Use memory_order_acquire for exchange
    }

    void unlock() {
        // TODO: Implement
    }
};

/**
 * TODO: Implement Exponential Backoff Lock
 *
 * TTAS + exponential backoff on contention
 * Reduces contention by delaying retries
 */
class BackoffLock {
private:
    std::atomic<bool> state{false};
    static constexpr int MIN_DELAY = 1;
    static constexpr int MAX_DELAY = 1000;

public:
    /**
     * TODO: Implement lock with exponential backoff
     */
    void lock() {
        int delay = MIN_DELAY;
        while (true) {
            // TODO: Spin locally
            while (state.load(std::memory_order_relaxed)) {
                // Busy wait
            }

            // TODO: Try to acquire
            if (!state.exchange(true, std::memory_order_acquire)) {
                return; // Success!
            }

            // TODO: Exponential backoff on failure
            std::this_thread::sleep_for(std::chrono::microseconds(delay));
            delay = std::min(delay * 2, MAX_DELAY);
        }
    }

    void unlock() {
        state.store(false, std::memory_order_release);
    }
};

/**
 * TODO: Implement MCS Lock (Mellor-Crummey Scott)
 *
 * Queue-based lock with excellent scalability
 * Each thread spins on its own node (no cache coherence traffic)
 */
class MCSLock {
public:
    struct QNode {
        std::atomic<bool> locked{false};
        std::atomic<QNode*> next{nullptr};
    };

private:
    std::atomic<QNode*> tail{nullptr};

    // Thread-local storage for nodes (simplified version)
    // In real implementation, would use thread_local
    static QNode* get_my_node() {
        thread_local QNode node;
        return &node;
    }

public:
    /**
     * TODO: Implement MCS lock
     *
     * 1. Get my node, set locked = true
     * 2. Exchange my node into tail
     * 3. If tail was not null:
     *    - Set pred->next = myNode
     *    - Spin on myNode->locked
     */
    void lock() {
        QNode* my_node = get_my_node();
        my_node->locked.store(true, std::memory_order_relaxed);
        my_node->next.store(nullptr, std::memory_order_relaxed);

        // TODO: Implement MCS lock protocol
        // HINT: Use exchange to atomically get predecessor and enqueue
        QNode* pred = tail.exchange(my_node, std::memory_order_acquire);

        if (pred != nullptr) {
            // TODO: Link to predecessor and spin on own node
            pred->next.store(my_node, std::memory_order_release);

            // Spin on my own node (cache-friendly!)
            while (my_node->locked.load(std::memory_order_acquire)) {
                // Busy wait
            }
        }
    }

    /**
     * TODO: Implement MCS unlock
     *
     * If next == null:
     *   Try to CAS tail to null
     *   If fail, wait for next to be set
     * Set next->locked = false
     */
    void unlock() {
        QNode* my_node = get_my_node();
        QNode* successor = my_node->next.load(std::memory_order_acquire);

        if (successor == nullptr) {
            // TODO: Try to remove ourselves from queue
            if (tail.compare_exchange_strong(my_node, nullptr,
                                            std::memory_order_release,
                                            std::memory_order_relaxed)) {
                return; // We were last in queue
            }

            // Wait for successor to link
            while (successor == nullptr) {
                successor = my_node->next.load(std::memory_order_acquire);
            }
        }

        // TODO: Signal successor
        successor->locked.store(false, std::memory_order_release);
    }
};

/**
 * CLH Lock (Craig, Landin, and Hagersten)
 *
 * CRITICAL: Foundation of Java's AbstractQueuedSynchronizer (AQS)!
 *
 * Key differences from MCS:
 * - MCS: Explicit queue with successor pointers (spins on own node)
 * - CLH: Implicit queue with predecessor pointers (spins on predecessor's node)
 *
 * Benefits:
 * - Better cache behavior on cache-coherent systems
 * - Simpler to implement than MCS
 * - Used in Java's ReentrantLock, Semaphore, CountDownLatch
 *
 * How it works:
 * 1. Each thread has a QNode (initially locked=false)
 * 2. To acquire: swap my node into tail, spin on predecessor's locked field
 * 3. To release: set my node's locked=false
 * 4. Predecessor becomes garbage when next thread releases
 */
class CLHLock {
private:
    /**
     * Queue node for CLH lock
     * Each thread spins on its predecessor's locked field
     */
    struct QNode {
        std::atomic<bool> locked{false};
    };

    std::atomic<QNode*> tail;
    thread_local static QNode* my_node;
    thread_local static QNode* my_pred;

public:
    CLHLock() : tail(new QNode()) {}

    ~CLHLock() {
        // Clean up tail node
        delete tail.load();
    }

    /**
     * CLH lock acquisition
     *
     * Algorithm:
     * 1. Get my node, set locked = true
     * 2. Swap my node into tail, get predecessor
     * 3. Spin on predecessor's locked field
     * 4. When pred->locked becomes false, I have the lock
     */
    void lock() {
        // Get or create thread-local node
        if (my_node == nullptr) {
            my_node = new QNode();
        }

        my_node->locked.store(true, std::memory_order_relaxed);

        // Swap my node into tail, get predecessor
        QNode* pred = tail.exchange(my_node, std::memory_order_acq_rel);
        my_pred = pred;

        // Spin on predecessor's locked field
        // This is cache-friendly: each thread spins on different location
        while (pred->locked.load(std::memory_order_acquire)) {
            // Spin locally on predecessor's cached locked field
            std::this_thread::yield();
        }

        // When we exit the loop, we have acquired the lock
    }

    /**
     * CLH lock release
     *
     * Algorithm:
     * 1. Set my node's locked = false (releases successor)
     * 2. Reuse predecessor's node for next acquisition
     */
    void unlock() {
        // Release successor
        my_node->locked.store(false, std::memory_order_release);

        // Reuse predecessor's node (it's now garbage for the predecessor)
        // This is memory-efficient: nodes are recycled
        QNode* old_node = my_node;
        my_node = my_pred;

        // Note: old_node will be freed by the next thread that releases
        // This is a form of lock-free memory management
    }

    /**
     * Compare with MCS Lock:
     *
     * MCS:
     * - Spins on own node (node->locked)
     * - Explicit queue with successor pointers
     * - Better for NUMA systems
     * - More complex unlock
     *
     * CLH:
     * - Spins on predecessor node (pred->locked)
     * - Implicit queue (only tail pointer)
     * - Better for cache-coherent systems
     * - Simpler implementation
     * - Used in Java AQS!
     *
     * Performance:
     * - Similar scalability
     * - CLH better on most modern systems (cache-coherent)
     * - MCS better on NUMA systems
     */
};

// Thread-local storage definitions
thread_local CLHLock::QNode* CLHLock::my_node = nullptr;
thread_local CLHLock::QNode* CLHLock::my_pred = nullptr;

/**
 * Test counter for correctness verification
 */
class Counter {
private:
    int count = 0;

public:
    void increment() {
        count++;
    }

    int get() const {
        return count;
    }
};

/**
 * Performance testing framework
 */
class PerformanceTest {
public:
    template <typename Lock>
    static long test_lock(const std::string& name, Lock& lock,
                         int num_threads, int iterations) {
        Counter counter;
        std::vector<std::thread> threads;

        auto start_time = std::chrono::high_resolution_clock::now();

        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&lock, &counter, iterations]() {
                for (int j = 0; j < iterations; ++j) {
                    lock.lock();
                    counter.increment();
                    lock.unlock();
                }
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_time - start_time).count();

        std::cout << std::left << std::setw(20) << name << ": "
                  << std::right << std::setw(6) << duration << "ms"
                  << " (count=" << counter.get() << ")\n";

        return duration;
    }
};

void test_correctness() {
    std::cout << "Testing correctness of locks:\n\n";

    const int num_threads = 10;
    const int increments_per_thread = 1000;
    const int expected = num_threads * increments_per_thread;

    auto test_one_lock = [&](const std::string& name, auto& lock) {
        Counter counter;
        std::vector<std::thread> threads;

        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&lock, &counter, increments_per_thread]() {
                for (int j = 0; j < increments_per_thread; ++j) {
                    lock.lock();
                    counter.increment();
                    lock.unlock();
                }
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        std::cout << std::left << std::setw(15) << name << ": "
                  << "Expected=" << expected
                  << ", Actual=" << counter.get()
                  << (counter.get() == expected ? " ✅" : " ❌") << "\n";
    };

    TASLock tas;
    test_one_lock("TAS", tas);

    TTASLock ttas;
    test_one_lock("TTAS", ttas);

    BackoffLock backoff;
    test_one_lock("Backoff", backoff);

    MCSLock mcs;
    test_one_lock("MCS", mcs);

    CLHLock clh;
    test_one_lock("CLH", clh);
}

void compare_performance() {
    const int num_threads = 8;
    const int iterations = 10000;

    std::cout << "\n=== Performance Comparison ===\n";
    std::cout << "Threads: " << num_threads
              << ", Iterations per thread: " << iterations << "\n\n";

    TASLock tas;
    PerformanceTest::test_lock("TAS Lock", tas, num_threads, iterations);

    TTASLock ttas;
    PerformanceTest::test_lock("TTAS Lock", ttas, num_threads, iterations);

    BackoffLock backoff;
    PerformanceTest::test_lock("Backoff Lock", backoff, num_threads, iterations);

    MCSLock mcs;
    PerformanceTest::test_lock("MCS Lock", mcs, num_threads, iterations);

    CLHLock clh;
    PerformanceTest::test_lock("CLH Lock", clh, num_threads, iterations);

    std::cout << "\n💡 CLH and MCS locks both perform well under high contention\n";
    std::cout << "💡 CLH is the foundation of Java's AQS (AbstractQueuedSynchronizer)\n";
    std::cout << "💡 TTAS is simpler but causes more cache coherence traffic\n";
}

} // namespace multiprocessor::spin_locks

int main() {
    using namespace multiprocessor::spin_locks;

    std::cout << "=== Spin Locks Test (C++) ===\n\n";

    test_correctness();
    compare_performance();

    return 0;
}
