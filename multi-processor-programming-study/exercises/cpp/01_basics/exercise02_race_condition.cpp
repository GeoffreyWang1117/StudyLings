/**
 * Exercise 02: Race Condition
 *
 * CONCEPT: Understanding race conditions in concurrent C++ programs
 *
 * A race condition occurs when multiple threads access shared data concurrently
 * and at least one thread modifies it, leading to unpredictable results.
 *
 * LEARNING OBJECTIVES:
 * - Observe a race condition in action
 * - Understand why unsynchronized access to shared data is dangerous
 * - Learn to identify potential race conditions in C++
 *
 * TODO: Complete the implementation to demonstrate a race condition
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>

namespace multiprocessor::basics {

/**
 * A simple counter that is NOT thread-safe
 */
class UnsafeCounter {
private:
    int count = 0;

public:
    /**
     * TODO: Implement increment method (without synchronization)
     * This should simply add 1 to count
     */
    void increment() {
        // TODO: Implement this
        // HINT: Just read count, add 1, and write it back
        // This is intentionally unsafe to demonstrate the race condition
    }

    int get_count() const {
        return count;
    }
};

/**
 * TODO: Create threads that increment the counter concurrently
 *
 * @param counter Reference to the counter to increment
 * @param threads_count Number of threads to create
 * @param increments_per_thread Number of times each thread should increment
 * @return Vector of threads
 */
std::vector<std::thread> create_increment_threads(
    UnsafeCounter& counter,
    int threads_count,
    int increments_per_thread) {

    // TODO: Implement this function
    // Create threads that each call counter.increment() increments_per_thread times
    std::vector<std::thread> threads;

    // TODO: Create threads and add them to the vector

    return threads;
}

} // namespace multiprocessor::basics

/**
 * Demonstration main function
 */
int main() {
    using namespace multiprocessor::basics;

    UnsafeCounter counter;
    const int num_threads = 10;
    const int increments_per_thread = 1000;

    std::cout << "Starting race condition demonstration...\n";
    std::cout << "Expected final count: " << (num_threads * increments_per_thread) << "\n";

    auto threads = create_increment_threads(counter, num_threads, increments_per_thread);

    // Wait for all threads
    for (auto& t : threads) {
        if (t.joinable()) {
            t.join();
        }
    }

    std::cout << "Actual final count: " << counter.get_count() << "\n";
    std::cout << "Difference: " << (num_threads * increments_per_thread - counter.get_count()) << "\n";

    if (counter.get_count() != num_threads * increments_per_thread) {
        std::cout << "❌ Race condition detected! The count is incorrect.\n";
        std::cout << "💡 This happens because multiple threads read-modify-write without coordination.\n";
    } else {
        std::cout << "⚠️  No race condition observed this time (try running again)\n";
    }

    return 0;
}
