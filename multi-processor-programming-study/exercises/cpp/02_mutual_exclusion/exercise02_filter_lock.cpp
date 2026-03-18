/**
 * Exercise: Filter Lock (C++20)
 *
 * CONCEPT: n-thread mutual exclusion using the Filter lock
 *
 * The Filter lock is a generalization of Peterson's algorithm for n threads.
 * It creates n-1 "levels" of exclusion. At each level, at least one thread
 * trying to get in is blocked. This ensures that only one thread can reach
 * level n-1 (the critical section).
 *
 * LEARNING OBJECTIVES:
 * - Understand how Peterson's algorithm generalizes to n threads
 * - Learn about levels of exclusion
 * - Use std::atomic with proper memory ordering
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <chrono>

namespace multiprocessor::mutual_exclusion {

/**
 * TODO: Implement the Filter Lock for n threads
 */
class FilterLock {
private:
    const int n; // number of threads

    // TODO: Declare the necessary arrays
    // HINT: level[i] is the current level of thread i
    // HINT: victim[L] is the victim thread at level L
    // std::vector<std::atomic<int>> level;
    // std::vector<std::atomic<int>> victim;

public:
    FilterLock(int num_threads) : n(num_threads) {
        // TODO: Initialize the arrays
        // HINT: level should have n elements (one per thread)
        // HINT: victim should have n elements (one per level)
    }

    /**
     * TODO: Implement the lock method for Filter lock
     *
     * @param thread_id The ID of the calling thread (0 to n-1)
     */
    void lock(int thread_id) {
        // TODO: Implement the Filter lock protocol
        // For each level L from 0 to n-2:
        //   1. Set level[thread_id] = L (announce your level)
        //   2. Set victim[L] = thread_id (become the victim at this level)
        //   3. Wait while (exists k != thread_id where level[k] >= L) AND victim[L] == thread_id
    }

    /**
     * TODO: Implement the unlock method
     *
     * @param thread_id The ID of the calling thread
     */
    void unlock(int thread_id) {
        // TODO: Implement unlock
        // HINT: Set level[thread_id] to 0 (exit all levels)
    }
};

/**
 * Test harness
 */
class SharedResource {
private:
    int value = 0;
    std::atomic<int> concurrent_access{0};

public:
    void critical_section(int thread_id) {
        // Check mutual exclusion
        int current = concurrent_access.fetch_add(1);
        if (current > 0) {
            std::cerr << "❌ Mutual exclusion violated! Thread " << thread_id
                     << " entered while another thread was in critical section\n";
            std::terminate();
        }

        // Do some work
        value++;

        concurrent_access.fetch_sub(1);
    }

    int get_value() const {
        return value;
    }
};

} // namespace multiprocessor::mutual_exclusion

/**
 * Demonstration and testing
 */
int main() {
    using namespace multiprocessor::mutual_exclusion;

    const int num_threads = 8;
    const int iterations_per_thread = 10000;

    std::cout << "=== Filter Lock Test ===\n";
    std::cout << "Threads: " << num_threads << "\n";
    std::cout << "Iterations per thread: " << iterations_per_thread << "\n\n";

    FilterLock lock(num_threads);
    SharedResource resource;
    std::vector<std::thread> threads;

    auto start_time = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&lock, &resource, i, iterations_per_thread]() {
            for (int j = 0; j < iterations_per_thread; ++j) {
                lock.lock(i);
                resource.critical_section(i);
                lock.unlock(i);
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_time - start_time);

    int expected = num_threads * iterations_per_thread;
    int actual = resource.get_value();

    std::cout << "Expected value: " << expected << "\n";
    std::cout << "Actual value: " << actual << "\n";
    std::cout << "Time taken: " << duration.count() << "ms\n\n";

    if (actual == expected) {
        std::cout << "✅ PASS - Filter lock working correctly!\n";
    } else {
        std::cout << "❌ FAIL - Mutual exclusion violated!\n";
    }

    return 0;
}
