/**
 * Exercise: Peterson's Algorithm
 *
 * CONCEPT: Two-thread mutual exclusion using Peterson's algorithm
 *
 * Peterson's algorithm is a classic solution to the mutual exclusion problem
 * for two threads. It uses two flags and a victim variable to ensure that
 * only one thread can enter the critical section at a time.
 *
 * KEY PROPERTIES:
 * 1. Mutual Exclusion: At most one thread in critical section
 * 2. Deadlock-free: Some thread eventually enters critical section
 * 3. Starvation-free: Every thread eventually enters critical section
 *
 * ALGORITHM:
 * - Each thread sets its flag to indicate interest
 * - Each thread sets itself as the victim
 * - Each thread waits while the other is interested AND it is the victim
 *
 * LEARNING OBJECTIVES:
 * - Understand classical mutual exclusion algorithms
 * - Learn about memory ordering and std::atomic
 * - Understand the C++ memory model
 *
 * NOTE: Use std::atomic with appropriate memory ordering for correctness
 */

#include <iostream>
#include <thread>
#include <atomic>
#include <array>
#include <chrono>

namespace multiprocessor::mutual_exclusion {

/**
 * TODO: Implement Peterson's Lock for two threads
 */
class PetersonLock {
private:
    // TODO: Declare the necessary member variables
    // HINT: You need two flags (one per thread) and a victim variable
    // HINT: Use std::atomic for proper memory ordering
    // std::array<std::atomic<bool>, 2> flag;
    // std::atomic<int> victim;

public:
    PetersonLock() {
        // TODO: Initialize the atomic variables
        // HINT: flag[0] = false, flag[1] = false
    }

    /**
     * TODO: Implement the lock method for Peterson's algorithm
     *
     * @param thread_id The ID of the calling thread (0 or 1)
     */
    void lock(int thread_id) {
        // TODO: Implement Peterson's lock protocol
        // Step 1: Set your flag to true (indicate interest)
        // Step 2: Set yourself as the victim
        // Step 3: Wait while the other thread is interested AND you are the victim
        // HINT: Use std::memory_order_seq_cst for simplicity (or experiment with relaxed/acquire/release)
    }

    /**
     * TODO: Implement the unlock method
     *
     * @param thread_id The ID of the calling thread (0 or 1)
     */
    void unlock(int thread_id) {
        // TODO: Implement unlock
        // HINT: Just set your flag to false
    }
};

/**
 * Test harness to verify mutual exclusion
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
 * Demonstration and testing
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
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);

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
