/**
 * SOLUTION for Peterson's Lock Exercise (C++)
 *
 * This is a reference implementation of Peterson's two-thread mutual exclusion algorithm.
 */

#include <iostream>
#include <thread>
#include <atomic>
#include <array>
#include <chrono>

namespace multiprocessor::mutual_exclusion {

/**
 * SOLUTION: Peterson's Lock implementation
 */
class PetersonLock {
private:
    std::array<std::atomic<bool>, 2> flag;
    std::atomic<int> victim;

public:
    PetersonLock() {
        flag[0].store(false, std::memory_order_relaxed);
        flag[1].store(false, std::memory_order_relaxed);
        victim.store(0, std::memory_order_relaxed);
    }

    /**
     * SOLUTION: Peterson's lock protocol
     */
    void lock(int thread_id) {
        int other = 1 - thread_id;

        // Step 1: Indicate interest
        flag[thread_id].store(true, std::memory_order_seq_cst);

        // Step 2: Set yourself as victim (be polite!)
        victim.store(thread_id, std::memory_order_seq_cst);

        // Step 3: Wait while other is interested AND you are the victim
        while (flag[other].load(std::memory_order_seq_cst) &&
               victim.load(std::memory_order_seq_cst) == thread_id) {
            // Busy wait (spin)
        }
        // At this point, we have acquired the lock
    }

    /**
     * SOLUTION: Release the lock
     */
    void unlock(int thread_id) {
        // Simply indicate that we're no longer interested
        flag[thread_id].store(false, std::memory_order_seq_cst);
    }
};

/**
 * Test harness
 */
class Counter {
private:
    int count = 0;

public:
    void increment() {
        count++;
    }

    int get_count() const {
        return count;
    }
};

} // namespace multiprocessor::mutual_exclusion

/**
 * Demonstration
 */
int main() {
    using namespace multiprocessor::mutual_exclusion;

    std::cout << "=== Peterson Lock Test ===\n";

    PetersonLock lock;
    Counter counter;
    const int increments_per_thread = 100000;

    auto thread_func = [&](int thread_id) {
        for (int i = 0; i < increments_per_thread; ++i) {
            lock.lock(thread_id);
            counter.increment();
            lock.unlock(thread_id);
        }
    };

    auto start_time = std::chrono::high_resolution_clock::now();

    std::thread thread0(thread_func, 0);
    std::thread thread1(thread_func, 1);

    thread0.join();
    thread1.join();

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_time - start_time);

    int expected = increments_per_thread * 2;
    int actual = counter.get_count();

    std::cout << "Expected count: " << expected << "\n";
    std::cout << "Actual count: " << actual << "\n";
    std::cout << "Time taken: " << duration.count() << "ms\n";

    if (actual == expected) {
        std::cout << "✅ PASS - Mutual exclusion preserved!\n";
    } else {
        std::cout << "❌ FAIL - Race condition detected!\n";
        std::cout << "Difference: " << (expected - actual) << "\n";
    }

    return 0;
}
