/**
 * Exercise: Bakery Algorithm (C++20)
 *
 * CONCEPT: Fair mutual exclusion using the Bakery Algorithm
 *
 * The Bakery Algorithm was invented by Leslie Lamport in 1974.
 * It provides FCFS (first-come-first-served) fairness - threads enter
 * the critical section in the order they request access.
 *
 * REAL-WORLD ANALOGY:
 * Like a bakery where customers take numbered tickets:
 * - Each customer takes a number when they arrive
 * - The customer with the smallest number is served first
 * - If two customers have the same number, use their customer ID to break ties
 *
 * KEY PROPERTIES:
 * - First-come-first-served fairness
 * - Deadlock-free
 * - No starvation
 * - Works for n threads
 *
 * ALGORITHM:
 * 1. Thread announces it's entering (choosing = true)
 * 2. Thread takes a number: max(all other numbers) + 1
 * 3. Thread announces it has a number (choosing = false)
 * 4. For each other thread k:
 *    - Wait until k finishes choosing
 *    - Wait while k has a smaller ticket, OR same ticket but smaller ID
 *
 * LEARNING OBJECTIVES:
 * - Implement ticket-based mutual exclusion in C++
 * - Use std::atomic for thread-safe operations
 * - Understand lexicographic ordering for tie-breaking
 * - Measure FCFS fairness guarantees
 *
 * HISTORICAL SIGNIFICANCE:
 * - First algorithm to solve mutual exclusion with FCFS fairness
 * - Used atomic read/write only (no test-and-set or other atomic operations)
 * - Introduced the concept of logical timestamps in distributed systems
 * - Influenced Lamport's later work on distributed systems and time
 *
 * Compilation:
 *   g++ -std=c++20 -pthread exercise04_bakery_lock.cpp -o bakery_lock
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <chrono>
#include <iomanip>
#include <algorithm>

namespace multiprocessor::bakery {

/**
 * TODO: Implement Bakery Lock
 *
 * The Bakery lock uses ticket numbers for FCFS fairness.
 */
class BakeryLock {
private:
    const size_t n; // number of threads

    // TODO: Declare the necessary arrays
    // HINT: choosing[i] = true when thread i is taking a number
    // HINT: number[i] = the ticket number of thread i (0 = not interested)
    // HINT: Use std::atomic<bool>* and std::atomic<int>* for thread safety

    std::atomic<bool>* choosing;
    std::atomic<int>* number;

public:
    BakeryLock(size_t num_threads) : n(num_threads) {
        // TODO: Initialize the arrays
        choosing = new std::atomic<bool>[n];
        number = new std::atomic<int>[n];

        for (size_t i = 0; i < n; i++) {
            choosing[i].store(false, std::memory_order_relaxed);
            number[i].store(0, std::memory_order_relaxed);
        }
    }

    ~BakeryLock() {
        delete[] choosing;
        delete[] number;
    }

    /**
     * TODO: Implement the lock method for Bakery lock
     *
     * @param thread_id The ID of the calling thread (0 to n-1)
     */
    void lock(size_t thread_id) {
        // TODO: Implement the Bakery lock protocol

        // Step 1: Announce we're taking a number
        choosing[thread_id].store(true, std::memory_order_relaxed);

        // Step 2: Take a number (max of all numbers + 1)
        int max_number = 0;
        for (size_t i = 0; i < n; i++) {
            int current_number = number[i].load(std::memory_order_acquire);
            if (current_number > max_number) {
                max_number = current_number;
            }
        }
        number[thread_id].store(max_number + 1, std::memory_order_release);

        // Step 3: Announce we've taken a number
        choosing[thread_id].store(false, std::memory_order_release);

        // Step 4: Wait for all threads with smaller tickets
        for (size_t k = 0; k < n; k++) {
            if (k == thread_id) continue;

            // Wait until thread k finishes choosing
            while (choosing[k].load(std::memory_order_acquire)) {
                // Busy wait
                std::this_thread::yield();
            }

            // Wait while thread k has priority over us
            // Priority: smaller number, or same number with smaller ID
            while (number[k].load(std::memory_order_acquire) != 0 &&
                   has_priority(k, thread_id)) {
                // Busy wait
                std::this_thread::yield();
            }
        }
    }

    /**
     * TODO: Implement the unlock method
     *
     * @param thread_id The ID of the calling thread
     */
    void unlock(size_t thread_id) {
        // TODO: Implement unlock
        // HINT: Set number[thread_id] to 0 (no longer interested)
        number[thread_id].store(0, std::memory_order_release);
    }

private:
    /**
     * Helper method: Does thread k have priority over thread j?
     *
     * Priority is determined by lexicographic ordering (number, thread_id):
     * - Thread k has priority if it has a smaller number
     * - If numbers are equal, thread k has priority if k < j
     */
    bool has_priority(size_t k, size_t j) const {
        int number_k = number[k].load(std::memory_order_acquire);
        int number_j = number[j].load(std::memory_order_acquire);

        // Lexicographic ordering: (number[k], k) < (number[j], j)
        return (number_k < number_j) ||
               (number_k == number_j && k < j);
    }
};

/**
 * Test harness with fairness verification
 */
class SharedResource {
private:
    int value = 0;
    int concurrent_access = 0;
    std::vector<size_t> entry_order;
    size_t entry_count = 0;
    std::mutex order_mutex; // Protect entry_order updates

public:
    SharedResource(size_t max_entries) {
        entry_order.resize(max_entries);
    }

    void critical_section(size_t thread_id) {
        // Check mutual exclusion
        if (concurrent_access > 0) {
            throw std::runtime_error(
                "Mutual exclusion violated! Thread " + std::to_string(thread_id) +
                " entered while another thread was in critical section");
        }
        concurrent_access++;

        // Track entry order for fairness verification
        {
            std::lock_guard<std::mutex> lock(order_mutex);
            if (entry_count < entry_order.size()) {
                entry_order[entry_count++] = thread_id;
            }
        }

        // Do some work
        value++;

        concurrent_access--;
    }

    int get_value() const {
        return value;
    }

    const std::vector<size_t>& get_entry_order() const {
        return entry_order;
    }

    size_t get_entry_count() const {
        return entry_count;
    }
};

/**
 * Test correctness: mutual exclusion
 */
void test_correctness() {
    const size_t num_threads = 8;
    const size_t iterations_per_thread = 10000;

    std::cout << "Test 1: Correctness (Mutual Exclusion)\n";
    std::cout << "Threads: " << num_threads << "\n";
    std::cout << "Iterations per thread: " << iterations_per_thread << "\n";

    BakeryLock lock(num_threads);
    SharedResource resource(num_threads * iterations_per_thread);
    std::vector<std::thread> threads;

    auto start_time = std::chrono::high_resolution_clock::now();

    for (size_t i = 0; i < num_threads; i++) {
        threads.emplace_back([&lock, &resource, i, iterations_per_thread]() {
            for (size_t j = 0; j < iterations_per_thread; j++) {
                lock.lock(i);
                try {
                    resource.critical_section(i);
                } catch (...) {
                    lock.unlock(i);
                    throw;
                }
                lock.unlock(i);
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
        end_time - start_time).count();

    size_t expected = num_threads * iterations_per_thread;
    size_t actual = resource.get_value();

    std::cout << "\nExpected value: " << expected << "\n";
    std::cout << "Actual value: " << actual << "\n";
    std::cout << "Time taken: " << duration << "ms\n";

    if (actual == expected) {
        std::cout << "✅ PASS - Bakery lock provides mutual exclusion!\n";
    } else {
        std::cout << "❌ FAIL - Mutual exclusion violated!\n";
    }
}

/**
 * Test fairness: FCFS property
 */
void test_fairness() {
    const size_t num_threads = 4;
    const size_t iterations = 100;

    std::cout << "\nTest 2: Fairness (FCFS)\n";
    std::cout << "Threads: " << num_threads << "\n";
    std::cout << "Iterations: " << iterations << "\n";

    BakeryLock lock(num_threads);
    SharedResource resource(num_threads * iterations);
    std::vector<std::thread> threads;

    for (size_t i = 0; i < num_threads; i++) {
        threads.emplace_back([&lock, &resource, i, iterations]() {
            for (size_t j = 0; j < iterations; j++) {
                lock.lock(i);
                try {
                    resource.critical_section(i);
                } catch (...) {
                    lock.unlock(i);
                    throw;
                }
                lock.unlock(i);
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    // Analyze entry order
    std::vector<size_t> entry_count(num_threads, 0);
    const auto& entry_order = resource.get_entry_order();
    size_t total_entries = resource.get_entry_count();

    for (size_t i = 0; i < total_entries; i++) {
        entry_count[entry_order[i]]++;
    }

    std::cout << "\nEntry distribution:\n";
    for (size_t i = 0; i < num_threads; i++) {
        std::cout << "  Thread " << i << ": " << entry_count[i] << " entries\n";
    }

    // Check fairness: no thread should be starved
    size_t min_entries = *std::min_element(entry_count.begin(), entry_count.end());
    size_t max_entries = *std::max_element(entry_count.begin(), entry_count.end());

    std::cout << "\nFairness analysis:\n";
    std::cout << "  Min entries: " << min_entries << "\n";
    std::cout << "  Max entries: " << max_entries << "\n";
    std::cout << "  Ratio: " << std::fixed << std::setprecision(2)
              << (double)max_entries / min_entries << "\n";

    if (min_entries > 0 && (double)max_entries / min_entries < 2.0) {
        std::cout << "✅ PASS - Good fairness (FCFS property observed)!\n";
    } else if (min_entries > 0) {
        std::cout << "⚠️  WARN - Some unfairness detected, but no starvation\n";
    } else {
        std::cout << "❌ FAIL - Thread starvation detected!\n";
    }
}

/**
 * Performance comparison
 */
void compare_performance() {
    const size_t num_threads = 4;
    const size_t iterations_per_thread = 5000;

    std::cout << "\nTest 3: Performance Comparison\n";
    std::cout << "Threads: " << num_threads << "\n";
    std::cout << "Iterations per thread: " << iterations_per_thread << "\n\n";

    // Bakery Lock
    {
        BakeryLock lock(num_threads);
        SharedResource resource(num_threads * iterations_per_thread);
        std::vector<std::thread> threads;

        auto start_time = std::chrono::high_resolution_clock::now();

        for (size_t i = 0; i < num_threads; i++) {
            threads.emplace_back([&lock, &resource, i, iterations_per_thread]() {
                for (size_t j = 0; j < iterations_per_thread; j++) {
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
            end_time - start_time).count();

        std::cout << "Bakery Lock: " << duration << "ms\n";
    }

    std::cout << "\n💡 Key Insights:\n";
    std::cout << "  • Bakery lock provides FCFS fairness\n";
    std::cout << "  • No thread starvation guaranteed\n";
    std::cout << "  • Overhead: O(n) for each lock/unlock\n";
    std::cout << "  • Best for: Small number of threads with fairness requirements\n";
    std::cout << "  • Comparison:\n";
    std::cout << "    - Peterson Lock: 2 threads only\n";
    std::cout << "    - Filter Lock: n threads, no fairness guarantee\n";
    std::cout << "    - Bakery Lock: n threads, FCFS fairness\n";
}

} // namespace multiprocessor::bakery

int main() {
    using namespace multiprocessor::bakery;

    std::cout << "=== Bakery Lock Test (C++) ===\n\n";

    test_correctness();
    test_fairness();
    compare_performance();

    return 0;
}
