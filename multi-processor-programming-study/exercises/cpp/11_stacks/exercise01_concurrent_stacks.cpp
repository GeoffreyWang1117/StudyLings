/**
 * Exercise: Concurrent Stacks (C++20)
 *
 * CONCEPT: Lock-free concurrent stacks using CAS
 *
 * Stack implementations:
 * - Lock-based: Simple with mutex
 * - Lock-free: Treiber stack using CAS
 *
 * LEARNING OBJECTIVES:
 * - Implement lock-free stack (Treiber algorithm) in C++
 * - Understand memory reclamation challenges
 * - Use std::atomic with compare_exchange
 * - Compare performance under contention
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <mutex>
#include <optional>
#include <chrono>
#include <iomanip>

namespace multiprocessor::stacks {

/**
 * TODO: Implement simple lock-based stack
 */
template <typename T>
class LockBasedStack {
private:
    struct Node {
        T value;
        Node* next;

        Node(const T& val) : value(val), next(nullptr) {}
    };

    Node* top = nullptr;
    // TODO: Add std::mutex

public:
    ~LockBasedStack() {
        // TODO: Clean up remaining nodes
    }

    /**
     * TODO: Implement synchronized push
     */
    void push(const T& value) {
        // TODO: Use std::lock_guard
        // TODO: Create node and add to top
    }

    /**
     * TODO: Implement synchronized pop
     */
    std::optional<T> pop() {
        // TODO: Use std::lock_guard
        // TODO: Remove and return top node
        return std::nullopt;
    }

    bool is_empty() const {
        // TODO: Implement (needs lock!)
        return true;
    }
};

/**
 * TODO: Implement Lock-Free Stack (Treiber Stack)
 *
 * Classic lock-free stack using CAS
 * Simple and efficient under low contention
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
        // TODO: Initialize top to nullptr
    }

    ~LockFreeStack() {
        // TODO: Clean up remaining nodes
        // Warning: In production, need proper memory reclamation
    }

    /**
     * TODO: Implement lock-free push (Treiber algorithm)
     *
     * 1. Create new node
     * 2. Read current top
     * 3. Set node->next = top
     * 4. Try compare_exchange(top, node)
     * 5. Retry if CAS fails
     */
    void push(const T& value) {
        Node* node = new Node(value);
        // TODO: Implement Treiber push
        // HINT: Use compare_exchange_weak in a loop
    }

    /**
     * TODO: Implement lock-free pop
     *
     * 1. Read current top
     * 2. If null, return nullopt
     * 3. Try compare_exchange(top, top->next)
     * 4. If success, return top->value
     * 5. Retry if CAS fails
     */
    std::optional<T> pop() {
        // TODO: Implement Treiber pop
        // HINT: Need to handle memory reclamation carefully
        return std::nullopt;
    }

    bool is_empty() const {
        // TODO: Implement
        return true;
    }
};

/**
 * Performance testing framework
 */
class PerformanceTest {
public:
    template <typename Stack>
    static long test_stack(const std::string& name, Stack& stack,
                          int num_threads, int ops_per_thread) {
        std::vector<std::thread> threads;

        auto start_time = std::chrono::high_resolution_clock::now();

        // Each thread does push then pop repeatedly
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&stack, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    stack.push(j);
                    stack.pop();
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
                  << std::right << std::setw(6) << duration << "ms\n";

        return duration;
    }
};

void test_correctness() {
    std::cout << "Testing correctness:\n\n";

    const int num_threads = 10;
    const int ops_per_thread = 1000;

    auto test_one_stack = [&](const std::string& name, auto& stack) {
        // Push phase
        std::vector<std::thread> pushers;
        for (int i = 0; i < num_threads; ++i) {
            pushers.emplace_back([&stack, i, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    stack.push(i * ops_per_thread + j);
                }
            });
        }
        for (auto& t : pushers) t.join();

        // Pop phase
        std::atomic<int> pop_count{0};
        std::vector<std::thread> poppers;
        for (int i = 0; i < num_threads; ++i) {
            poppers.emplace_back([&stack, &pop_count, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    auto value = stack.pop();
                    if (value.has_value()) {
                        pop_count.fetch_add(1);
                    }
                }
            });
        }
        for (auto& t : poppers) t.join();

        int expected = num_threads * ops_per_thread;
        int actual = pop_count.load();

        std::cout << std::left << std::setw(20) << name << ": "
                  << "Expected=" << expected
                  << ", Actual=" << actual
                  << (actual == expected ? " ✅" : " ❌") << "\n";
    };

    LockBasedStack<int> lock_based;
    test_one_stack("Lock-Based", lock_based);

    LockFreeStack<int> lock_free;
    test_one_stack("Lock-Free", lock_free);
}

void compare_performance() {
    const int num_threads = 16;
    const int ops_per_thread = 50000;

    std::cout << "\n=== Performance Comparison ===\n";
    std::cout << "High contention (" << num_threads << " threads, "
              << ops_per_thread << " ops each):\n\n";

    LockBasedStack<int> lock_based;
    PerformanceTest::test_stack("Lock-Based Stack", lock_based,
                                num_threads, ops_per_thread);

    LockFreeStack<int> lock_free;
    PerformanceTest::test_stack("Lock-Free Stack", lock_free,
                               num_threads, ops_per_thread);

    std::cout << "\n💡 Lock-free stack typically performs better under contention\n";
    std::cout << "💡 But requires careful memory reclamation in production\n";
}

} // namespace multiprocessor::stacks

int main() {
    using namespace multiprocessor::stacks;

    std::cout << "=== Concurrent Stacks Test (C++) ===\n\n";

    test_correctness();
    compare_performance();

    return 0;
}
