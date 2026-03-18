/**
 * Exercise: Linearizability (C++20)
 *
 * CONCEPT: Linearizability - the gold standard for concurrent correctness
 *
 * Linearizability: Each operation appears to take effect instantaneously
 * at some point between its invocation and response (the linearization point).
 *
 * LEARNING OBJECTIVES:
 * - Understand linearizability and linearization points
 * - Implement linearizable data structures using std::atomic
 * - Identify linearization points in code
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <memory>
#include <optional>

namespace multiprocessor::concurrent_objects {

/**
 * TODO: Implement a linearizable lock-free stack (Treiber Stack)
 *
 * This stack should be linearizable:
 * - Each push/pop appears atomic at its linearization point
 * - Operations respect real-time ordering
 */
template <typename T>
class LinearizableStack {
private:
    struct Node {
        T value;
        Node* next;

        Node(const T& val) : value(val), next(nullptr) {}
    };

    // TODO: Add std::atomic<Node*> for top

public:
    LinearizableStack() {
        // TODO: Initialize top to nullptr
    }

    ~LinearizableStack() {
        // TODO: Clean up remaining nodes
        // Warning: In a real implementation, need to handle memory reclamation carefully
    }

    /**
     * TODO: Implement lock-free push using CAS
     *
     * The linearization point is the successful CAS operation
     *
     * @param value value to push
     */
    void push(const T& value) {
        // TODO: Implement lock-free push
        // 1. Create new node
        // 2. Loop:
        //    - Read current top
        //    - Set node->next = top
        //    - Try CAS(top, old_top, node)
        //    - If success, return
        //    - Else retry
    }

    /**
     * TODO: Implement lock-free pop using CAS
     *
     * The linearization point is the successful CAS operation
     *
     * @return optional containing popped value, or nullopt if empty
     */
    std::optional<T> pop() {
        // TODO: Implement lock-free pop
        // 1. Loop:
        //    - Read current top
        //    - If nullptr, return nullopt
        //    - Try CAS(top, old_top, old_top->next)
        //    - If success, return old_top->value
        //    - Else retry
        return std::nullopt;
    }

    bool is_empty() const {
        // TODO: Implement
        return true;
    }
};

/**
 * TODO: Implement a linearizable counter
 */
class LinearizableCounter {
private:
    // TODO: Add std::atomic<int>

public:
    LinearizableCounter(int initial_value) {
        // TODO: Initialize
    }

    /**
     * TODO: Implement atomic increment using CAS loop
     *
     * @return value AFTER increment
     */
    int increment_and_get() {
        // TODO: Implement using compare_exchange loop
        return 0;
    }

    /**
     * TODO: Implement atomic decrement
     *
     * @return value AFTER decrement
     */
    int decrement_and_get() {
        // TODO: Implement
        return 0;
    }

    int get() const {
        // TODO: Implement
        return 0;
    }
};

void test_linearizable_stack() {
    std::cout << "Testing Linearizable Stack:\n";

    LinearizableStack<int> stack;
    const int num_threads = 10;
    const int ops_per_thread = 1000;

    // Push phase
    std::vector<std::thread> pushers;
    for (int i = 0; i < num_threads; ++i) {
        pushers.emplace_back([&stack, i, ops_per_thread]() {
            for (int j = 0; j < ops_per_thread; ++j) {
                stack.push(i * ops_per_thread + j);
            }
        });
    }

    for (auto& t : pushers) {
        t.join();
    }

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

    for (auto& t : poppers) {
        t.join();
    }

    std::cout << "Expected pops: " << (num_threads * ops_per_thread) << "\n";
    std::cout << "Actual pops: " << pop_count.load() << "\n";
    std::cout << "Stack empty: " << (stack.is_empty() ? "yes" : "no") << "\n";

    bool pass = (pop_count.load() == num_threads * ops_per_thread) && stack.is_empty();
    std::cout << (pass ? "✅ PASS\n\n" : "❌ FAIL\n\n");
}

void test_linearizable_counter() {
    std::cout << "Testing Linearizable Counter:\n";

    LinearizableCounter counter(0);
    const int num_threads = 10;
    const int ops_per_thread = 1000;

    std::vector<std::thread> threads;

    // Half increment, half decrement
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&counter, ops_per_thread]() {
            for (int j = 0; j < ops_per_thread; ++j) {
                counter.increment_and_get();
            }
        });
    }

    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&counter, ops_per_thread]() {
            for (int j = 0; j < ops_per_thread; ++j) {
                counter.decrement_and_get();
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Expected final value: 0\n";
    std::cout << "Actual final value: " << counter.get() << "\n";
    std::cout << (counter.get() == 0 ? "✅ PASS\n\n" : "❌ FAIL\n\n");
}

} // namespace multiprocessor::concurrent_objects

int main() {
    using namespace multiprocessor::concurrent_objects;

    std::cout << "=== Linearizability Test (C++) ===\n\n";

    test_linearizable_stack();
    test_linearizable_counter();

    return 0;
}
