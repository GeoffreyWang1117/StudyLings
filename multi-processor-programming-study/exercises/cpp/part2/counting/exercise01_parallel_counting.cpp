/**
 * Exercise: Parallel Counting (C++20)
 *
 * CONCEPT: Efficient parallel counting using various strategies
 *
 * Strategies:
 * - Cache-line padding to avoid false sharing
 * - Thread-local aggregation
 * - Striping across multiple counters
 *
 * LEARNING OBJECTIVES:
 * - Understand false sharing and cache lines
 * - Implement scalable counters in C++
 * - Use thread_local storage
 * - Compare performance under contention
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <chrono>
#include <iomanip>
#include <numeric>

namespace multiprocessor::part2::counting {

/**
 * TODO: Implement Cache-Line Padded Counter
 *
 * Avoid false sharing by padding to cache line size (64 bytes)
 */
class alignas(64) PaddedCounter {
private:
    std::atomic<long> value{0};
    // Padding to fill cache line
    char padding[64 - sizeof(std::atomic<long>)];

public:
    void increment() {
        value.fetch_add(1, std::memory_order_relaxed);
    }

    long get() const {
        return value.load(std::memory_order_relaxed);
    }
};

/**
 * TODO: Implement Striped Counter
 *
 * Distribute count across multiple counters to reduce contention
 */
class StripedCounter {
private:
    std::vector<PaddedCounter> stripes;

public:
    StripedCounter(int num_stripes) : stripes(num_stripes) {}

    /**
     * TODO: Implement increment
     *
     * Hash thread ID to stripe to reduce contention
     */
    void increment() {
        // TODO: Get thread ID and hash to stripe
        size_t thread_id = std::hash<std::thread::id>{}(std::this_thread::get_id());
        size_t stripe_id = thread_id % stripes.size();
        stripes[stripe_id].increment();
    }

    /**
     * TODO: Implement get
     */
    long get() const {
        // TODO: Sum all stripes
        long sum = 0;
        for (const auto& stripe : stripes) {
            sum += stripe.get();
        }
        return sum;
    }
};

/**
 * TODO: Implement Thread-Local Counter with Combining
 */
class CombiningCounter {
private:
    std::atomic<long> global_counter{0};
    static constexpr int COMBINING_THRESHOLD = 100;

    struct ThreadLocalData {
        long local_count = 0;
    };

    static thread_local ThreadLocalData tl_data;

public:
    /**
     * TODO: Implement increment with combining
     */
    void increment() {
        // TODO: Increment thread-local counter
        tl_data.local_count++;

        // TODO: When threshold reached, flush to global
        if (tl_data.local_count >= COMBINING_THRESHOLD) {
            global_counter.fetch_add(tl_data.local_count, std::memory_order_relaxed);
            tl_data.local_count = 0;
        }
    }

    long get() const {
        // Note: This doesn't account for unflushed thread-local counts
        // In production, would need to iterate all thread-local data
        return global_counter.load(std::memory_order_relaxed);
    }
};

thread_local CombiningCounter::ThreadLocalData CombiningCounter::tl_data;

/**
 * Performance testing framework
 */
class PerformanceTest {
public:
    template <typename Counter>
    static long test_counter(const std::string& name, Counter& counter,
                            int num_threads, int increments_per_thread) {
        std::vector<std::thread> threads;

        auto start_time = std::chrono::high_resolution_clock::now();

        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&counter, increments_per_thread]() {
                for (int j = 0; j < increments_per_thread; ++j) {
                    counter.increment();
                }
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_time - start_time).count();

        std::cout << std::left << std::setw(25) << name << ": "
                  << std::right << std::setw(6) << duration << "ms"
                  << " (count=" << counter.get() << ")\n";

        return duration;
    }
};

void test_correctness() {
    const int num_threads = 10;
    const int increments_per_thread = 1000;
    const long expected = num_threads * increments_per_thread;

    std::cout << "Testing correctness (threads=" << num_threads
              << ", increments=" << increments_per_thread << "):\n\n";

    // Test Striped Counter
    StripedCounter striped(num_threads);
    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&striped, increments_per_thread]() {
            for (int j = 0; j < increments_per_thread; ++j) {
                striped.increment();
            }
        });
    }
    for (auto& t : threads) t.join();

    std::cout << "Striped Counter: Expected=" << expected
              << ", Actual=" << striped.get()
              << (striped.get() == expected ? " ✅\n" : " ❌\n");
}

void compare_performance() {
    const int num_threads = 16;
    const int increments_per_thread = 100000;

    std::cout << "\n=== Performance Comparison ===\n";
    std::cout << "High contention test (threads=" << num_threads
              << ", increments=" << increments_per_thread << "):\n\n";

    // Baseline: Single atomic counter
    std::atomic<long> atomic_counter{0};
    PerformanceTest::test_counter("std::atomic<long>",
        [&](){ atomic_counter.fetch_add(1); return atomic_counter.load(); },
        num_threads, increments_per_thread);

    // Padded Counter (array of one)
    std::vector<PaddedCounter> padded_array(1);
    auto padded_inc = [&padded_array]() { padded_array[0].increment(); };
    auto padded_get = [&padded_array]() { return padded_array[0].get(); };

    std::vector<std::thread> threads;
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&padded_inc, increments_per_thread]() {
            for (int j = 0; j < increments_per_thread; ++j) {
                padded_inc();
            }
        });
    }
    for (auto& t : threads) t.join();
    auto padded_time = std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::high_resolution_clock::now() - start).count();
    std::cout << std::left << std::setw(25) << "Padded Counter" << ": "
              << std::right << std::setw(6) << padded_time << "ms"
              << " (count=" << padded_get() << ")\n";

    // Striped Counter
    StripedCounter striped(num_threads);
    PerformanceTest::test_counter("Striped Counter", striped,
        num_threads, increments_per_thread);

    std::cout << "\n💡 Striping reduces contention by distributing load\n";
    std::cout << "💡 Padding prevents false sharing between cache lines\n";
}

} // namespace multiprocessor::part2::counting

int main() {
    using namespace multiprocessor::part2::counting;

    std::cout << "=== Parallel Counting Test (C++) ===\n\n";

    test_correctness();
    compare_performance();

    return 0;
}
