/**
 * SOLUTION for Lock-Free Stack (Treiber Stack) (C++)
 *
 * Complete implementation of the Treiber stack algorithm
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <optional>

namespace multiprocessor::stacks {

/**
 * SOLUTION: Complete Treiber Stack implementation
 */
template <typename T>
class LockFreeStack {
private:
    struct Node {
        T value;
        Node* next;

        Node(const T& val) : value(val), next(nullptr) {}
    };

    std::atomic<Node*> top;

public:
    LockFreeStack() : top(nullptr) {}

    ~LockFreeStack() {
        // Clean up remaining nodes
        while (auto val = pop()) {
            // Pop all remaining elements
        }
    }

    /**
     * SOLUTION: Lock-free push using CAS
     */
    void push(const T& value) {
        Node* node = new Node(value);
        Node* old_top = top.load(std::memory_order_relaxed);

        do {
            node->next = old_top;
        } while (!top.compare_exchange_weak(old_top, node,
                                           std::memory_order_release,
                                           std::memory_order_relaxed));
    }

    /**
     * SOLUTION: Lock-free pop using CAS
     */
    std::optional<T> pop() {
        Node* old_top = top.load(std::memory_order_relaxed);

        while (old_top != nullptr) {
            Node* next = old_top->next;

            if (top.compare_exchange_weak(old_top, next,
                                         std::memory_order_acquire,
                                         std::memory_order_relaxed)) {
                T value = old_top->value;
                delete old_top;
                return value;
            }
        }

        return std::nullopt;
    }

    bool is_empty() const {
        return top.load(std::memory_order_relaxed) == nullptr;
    }
};

} // namespace multiprocessor::stacks

/**
 * Test the implementation
 */
int main() {
    using namespace multiprocessor::stacks;

    std::cout << "=== Lock-Free Stack Test ===\n";

    LockFreeStack<int> stack;
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

    std::cout << "Expected: " << expected << "\n";
    std::cout << "Actual: " << actual << "\n";
    std::cout << "Empty: " << (stack.is_empty() ? "yes" : "no") << "\n";

    if (actual == expected && stack.is_empty()) {
        std::cout << "✅ PASS - Lock-free stack working correctly!\n";
    } else {
        std::cout << "❌ FAIL\n";
    }

    return 0;
}
