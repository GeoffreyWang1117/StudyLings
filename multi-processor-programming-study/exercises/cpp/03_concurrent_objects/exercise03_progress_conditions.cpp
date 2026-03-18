/**
 * Exercise: Progress Conditions (C++20)
 *
 * CONCEPT: Different guarantees about thread progress
 *
 * Progress conditions specify what happens when threads compete:
 *
 * WAIT-FREE: Every thread completes in finite steps (strongest)
 * LOCK-FREE: Some thread always makes progress (system-wide)
 * OBSTRUCTION-FREE: Thread makes progress when run alone
 * BLOCKING: Threads may wait for locks (weakest)
 *
 * LEARNING OBJECTIVES:
 * - Understand different progress conditions
 * - Implement wait-free, lock-free, and blocking algorithms in C++
 * - Compare their properties and performance
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <mutex>
#include <chrono>

namespace multiprocessor::concurrent_objects {

/**
 * TODO: Implement a WAIT-FREE counter
 *
 * Every thread completes increment in finite steps
 */
class WaitFreeCounter {
private:
    // TODO: Add std::atomic<int>

public:
    WaitFreeCounter(int initial_value) {
        // TODO: Initialize
    }

    /**
     * TODO: Implement wait-free increment
     *
     * WAIT-FREE property: This operation completes in O(1) steps
     * regardless of contention.
     *
     * @return value AFTER increment
     */
    int increment_and_get() {
        // TODO: Use fetch_add which is wait-free
        // HINT: fetch_add returns old value, so add 1
        return 0;
    }

    int get() const {
        // TODO: Implement
        return 0;
    }
};

/**
 * TODO: Implement a LOCK-FREE stack
 *
 * At least one thread makes progress
 */
template <typename T>
class LockFreeStack {
private:
    struct Node {
        T value;
        Node* next;

        Node(const T& val) : value(val), next(nullptr) {}
    };

    // TODO: Add std::atomic<Node*> for top

public:
    LockFreeStack() {
        // TODO: Initialize
    }

    ~LockFreeStack() {
        // TODO: Clean up
    }

    /**
     * TODO: Implement lock-free push
     *
     * LOCK-FREE property: Even if some threads are delayed,
     * at least one thread makes progress in finite steps.
     */
    void push(const T& value) {
        // TODO: Implement using CAS loop
    }

    /**
     * TODO: Implement lock-free pop
     */
    std::optional<T> pop() {
        // TODO: Implement using CAS loop
        return std::nullopt;
    }
};

/**
 * TODO: Implement a BLOCKING counter using mutex
 *
 * Threads may block waiting for locks
 */
class BlockingCounter {
private:
    int count;
    // TODO: Add std::mutex

public:
    BlockingCounter(int initial_value) : count(initial_value) {
        // TODO: Initialize
    }

    /**
     * TODO: Implement blocking increment
     *
     * BLOCKING property: Thread may wait indefinitely for lock
     *
     * @return value AFTER increment
     */
    int increment_and_get() {
        // TODO: Use std::lock_guard or std::unique_lock
        // TODO: Increment and return
        return 0;
    }

    int get() {
        // TODO: Implement with lock
        return 0;
    }
};

/**
 * Performance comparison
 */
class PerformanceTest {
public:
    template <typename CounterFunc>
    static long test_counter(const std::string& name, CounterFunc increment_op,
                            int num_threads, int ops_per_thread) {
        std::vector<std::thread> threads;

        auto start_time = std::chrono::high_resolution_clock::now();

        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&increment_op, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    increment_op();
                }
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_time - start_time).count();

        std::cout << name << ": " << duration << "ms\n";
        return duration;
    }
};

void test_correctness() {
    const int num_threads = 10;
    const int ops_per_thread = 1000;
    const int expected = num_threads * ops_per_thread;

    // Test Wait-Free
    std::cout << "Testing Wait-Free Counter:\n";
    WaitFreeCounter wf_counter(0);
    {
        std::vector<std::thread> threads;
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&wf_counter, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    wf_counter.increment_and_get();
                }
            });
        }
        for (auto& t : threads) t.join();
    }
    std::cout << "Expected: " << expected << ", Actual: " << wf_counter.get() << "\n";
    std::cout << (wf_counter.get() == expected ? "✅ PASS\n" : "❌ FAIL\n");

    // Test Lock-Free
    std::cout << "\nTesting Lock-Free Stack:\n";
    LockFreeStack<int> lf_stack;
    {
        std::vector<std::thread> pushers;
        for (int i = 0; i < num_threads; ++i) {
            pushers.emplace_back([&lf_stack, i, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    lf_stack.push(i * ops_per_thread + j);
                }
            });
        }
        for (auto& t : pushers) t.join();
    }

    int pop_count = 0;
    while (lf_stack.pop().has_value()) {
        pop_count++;
    }
    std::cout << "Expected: " << expected << ", Actual: " << pop_count << "\n";
    std::cout << (pop_count == expected ? "✅ PASS\n" : "❌ FAIL\n");

    // Test Blocking
    std::cout << "\nTesting Blocking Counter:\n";
    BlockingCounter b_counter(0);
    {
        std::vector<std::thread> threads;
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&b_counter, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    b_counter.increment_and_get();
                }
            });
        }
        for (auto& t : threads) t.join();
    }
    std::cout << "Expected: " << expected << ", Actual: " << b_counter.get() << "\n";
    std::cout << (b_counter.get() == expected ? "✅ PASS\n" : "❌ FAIL\n");
}

void compare_performance() {
    const int num_threads = 8;
    const int ops_per_thread = 100000;

    std::cout << "\n=== Performance Comparison ===\n";
    std::cout << "Threads: " << num_threads << ", Operations per thread: " << ops_per_thread << "\n\n";

    WaitFreeCounter wf_counter(0);
    BlockingCounter b_counter(0);

    PerformanceTest::test_counter("Wait-Free",
        [&wf_counter]() { wf_counter.increment_and_get(); },
        num_threads, ops_per_thread);

    PerformanceTest::test_counter("Blocking ",
        [&b_counter]() { b_counter.increment_and_get(); },
        num_threads, ops_per_thread);

    std::cout << "\n💡 Note: Results depend on contention level and hardware.\n";
    std::cout << "   Wait-free is typically faster under high contention.\n";
}

} // namespace multiprocessor::concurrent_objects

int main() {
    using namespace multiprocessor::concurrent_objects;

    std::cout << "=== Progress Conditions Test (C++) ===\n\n";

    test_correctness();
    compare_performance();

    return 0;
}
