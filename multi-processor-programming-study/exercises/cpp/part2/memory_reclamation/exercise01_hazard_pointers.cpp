/**
 * Exercise: Hazard Pointers for Safe Memory Reclamation
 *
 * CONCEPT: Safe memory reclamation in lock-free data structures
 *
 * THE PROBLEM:
 * Lock-free data structures use CAS to modify shared pointers. After a
 * successful CAS removes a node, when is it safe to delete that node?
 *
 * - Thread A removes node N (CAS succeeds)
 * - Thread B may still hold a pointer to N (loaded before CAS)
 * - If A deletes N, B will dereference freed memory (use-after-free)
 *
 * HAZARD POINTERS SOLUTION:
 * - Each thread has "hazard pointer" slots
 * - Before dereferencing a pointer, thread stores it in hazard pointer
 * - Before deleting a node, check if any hazard pointer protects it
 * - If protected, defer deletion until safe
 *
 * LEARNING OBJECTIVES:
 * - Understand the memory reclamation problem in lock-free structures
 * - Implement hazard pointer protocol
 * - Use hazard pointers with lock-free stack
 * - Handle retired node lists and safe reclamation
 *
 * CPU REQUIREMENTS:
 * - Minimum: 4 cores
 * - Recommended: 8+ cores (higher contention makes reclamation more critical)
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <array>
#include <algorithm>
#include <memory>
#include <chrono>

namespace multiprocessor::part2::memory_reclamation {

/**
 * Hazard Pointer Manager
 *
 * Manages hazard pointers for all threads in the system
 */
template <typename T>
class HazardPointerManager {
public:
    static constexpr int MAX_THREADS = 128;
    static constexpr int HAZARD_POINTERS_PER_THREAD = 2;
    static constexpr int RETIRED_LIST_MAX = 100;

private:
    struct HazardPointerRecord {
        std::atomic<T*> hazard_pointer{nullptr};
        std::atomic<bool> active{false};
    };

    /**
     * TODO: Global hazard pointer array
     *
     * Each thread has HAZARD_POINTERS_PER_THREAD slots
     */
    std::array<std::array<HazardPointerRecord, HAZARD_POINTERS_PER_THREAD>, MAX_THREADS> hazard_pointers_;
    std::atomic<int> thread_count_{0};

public:
    /**
     * TODO: Implement acquire_hazard_pointer_slot
     *
     * Each thread calls this once to get its thread-local slot index
     */
    int acquire_hazard_pointer_slot() {
        // TODO: Atomically allocate a slot for this thread
        int slot = thread_count_.fetch_add(1, std::memory_order_relaxed);
        if (slot >= MAX_THREADS) {
            throw std::runtime_error("Too many threads!");
        }
        return slot;
    }

    /**
     * TODO: Implement set_hazard_pointer
     *
     * Thread sets one of its hazard pointers to protect a node
     */
    void set_hazard_pointer(int thread_id, int hp_index, T* ptr) {
        // TODO: Set hazard pointer at [thread_id][hp_index] to ptr
        hazard_pointers_[thread_id][hp_index].hazard_pointer.store(ptr, std::memory_order_release);
        hazard_pointers_[thread_id][hp_index].active.store(true, std::memory_order_release);
    }

    /**
     * TODO: Implement clear_hazard_pointer
     *
     * Thread clears its hazard pointer when done with protected node
     */
    void clear_hazard_pointer(int thread_id, int hp_index) {
        // TODO: Clear hazard pointer
        hazard_pointers_[thread_id][hp_index].active.store(false, std::memory_order_release);
        hazard_pointers_[thread_id][hp_index].hazard_pointer.store(nullptr, std::memory_order_release);
    }

    /**
     * TODO: Implement is_protected
     *
     * Check if any thread's hazard pointer protects this node
     */
    bool is_protected(T* ptr) {
        // TODO: Scan all hazard pointers to see if ptr is protected
        for (int tid = 0; tid < thread_count_.load(std::memory_order_acquire); ++tid) {
            for (int hp_idx = 0; hp_idx < HAZARD_POINTERS_PER_THREAD; ++hp_idx) {
                if (hazard_pointers_[tid][hp_idx].active.load(std::memory_order_acquire)) {
                    T* hazard = hazard_pointers_[tid][hp_idx].hazard_pointer.load(std::memory_order_acquire);
                    if (hazard == ptr) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    /**
     * TODO: Implement safe_delete
     *
     * Delete ptr if not protected, otherwise return false
     */
    bool try_delete(T* ptr) {
        // TODO: Check if protected, if not, delete and return true
        if (!is_protected(ptr)) {
            delete ptr;
            return true;
        }
        return false;
    }
};

/**
 * Thread-local context for hazard pointers
 */
template <typename T>
class HazardPointerContext {
private:
    HazardPointerManager<T>& manager_;
    int thread_id_;
    std::vector<T*> retired_list_;

public:
    HazardPointerContext(HazardPointerManager<T>& manager)
        : manager_(manager), thread_id_(manager.acquire_hazard_pointer_slot()) {}

    /**
     * TODO: Implement protect
     *
     * Acquire hazard pointer protection for a node
     * Returns protected pointer (may differ if node was modified)
     */
    T* protect(int hp_index, std::atomic<T*>& atomic_ptr) {
        T* ptr = nullptr;
        T* protected_ptr = atomic_ptr.load(std::memory_order_acquire);

        // TODO: Implement protection protocol
        // 1. Set hazard pointer to protect node
        // 2. Re-read atomic_ptr to check it hasn't changed
        // 3. If changed, clear hazard pointer and retry
        // 4. If unchanged, node is now protected

        do {
            ptr = protected_ptr;
            if (ptr == nullptr) {
                manager_.clear_hazard_pointer(thread_id_, hp_index);
                return nullptr;
            }
            manager_.set_hazard_pointer(thread_id_, hp_index, ptr);
            // Re-read to ensure ptr is still valid
            protected_ptr = atomic_ptr.load(std::memory_order_acquire);
        } while (ptr != protected_ptr);

        return ptr;
    }

    /**
     * TODO: Implement unprotect
     *
     * Release hazard pointer protection
     */
    void unprotect(int hp_index) {
        // TODO: Clear hazard pointer
        manager_.clear_hazard_pointer(thread_id_, hp_index);
    }

    /**
     * TODO: Implement retire
     *
     * Add node to retired list for eventual deletion
     */
    void retire(T* ptr) {
        // TODO: Add to retired list
        retired_list_.push_back(ptr);

        // TODO: If retired list is large, try to reclaim memory
        if (retired_list_.size() >= HazardPointerManager<T>::RETIRED_LIST_MAX) {
            reclaim();
        }
    }

    /**
     * TODO: Implement reclaim
     *
     * Attempt to delete retired nodes that are no longer protected
     */
    void reclaim() {
        // TODO: For each retired node, try to delete if not protected
        std::vector<T*> still_protected;
        for (T* ptr : retired_list_) {
            if (!manager_.try_delete(ptr)) {
                still_protected.push_back(ptr);
            }
        }
        retired_list_ = std::move(still_protected);
    }

    ~HazardPointerContext() {
        // Final reclamation attempt
        reclaim();
        // Force delete any remaining nodes (on program exit)
        for (T* ptr : retired_list_) {
            delete ptr;
        }
    }
};

/**
 * Lock-Free Stack with Hazard Pointer Memory Reclamation
 *
 * This is the classic Treiber stack, now made safe with hazard pointers
 */
template <typename T>
class LockFreeStackWithHP {
private:
    struct Node {
        T value;
        std::atomic<Node*> next;

        explicit Node(const T& val) : value(val), next(nullptr) {}
    };

    std::atomic<Node*> top_{nullptr};
    HazardPointerManager<Node> hp_manager_;

    // Thread-local hazard pointer context
    static thread_local std::unique_ptr<HazardPointerContext<Node>> hp_context_;

    HazardPointerContext<Node>* get_context() {
        if (!hp_context_) {
            hp_context_ = std::make_unique<HazardPointerContext<Node>>(hp_manager_);
        }
        return hp_context_.get();
    }

public:
    /**
     * TODO: Implement push
     *
     * No hazard pointers needed - we're creating a new node
     */
    void push(const T& value) {
        Node* node = new Node(value);
        Node* old_top = top_.load(std::memory_order_relaxed);

        // TODO: Standard Treiber stack push with CAS loop
        do {
            node->next.store(old_top, std::memory_order_relaxed);
        } while (!top_.compare_exchange_weak(old_top, node,
                                             std::memory_order_release,
                                             std::memory_order_relaxed));
    }

    /**
     * TODO: Implement pop with hazard pointer protection
     *
     * This is where hazard pointers are critical!
     */
    bool pop(T& result) {
        auto* context = get_context();
        Node* old_top = nullptr;

        // TODO: Implement pop with hazard pointer protection
        // 1. Protect top node with hazard pointer
        // 2. If null, return false (empty)
        // 3. Read next pointer
        // 4. Try to CAS top to next
        // 5. If success, copy value, retire old_top, return true
        // 6. If fail, retry

        while (true) {
            // Protect current top node
            old_top = context->protect(0, top_);

            if (old_top == nullptr) {
                context->unprotect(0);
                return false; // Empty stack
            }

            // Read next pointer (safe because old_top is protected)
            Node* next = old_top->next.load(std::memory_order_acquire);

            // Try to CAS
            if (top_.compare_exchange_weak(old_top, next,
                                          std::memory_order_release,
                                          std::memory_order_relaxed)) {
                // Success! Copy value and retire node
                result = old_top->value;
                context->unprotect(0);

                // Retire node for eventual deletion
                context->retire(old_top);
                return true;
            }
            // CAS failed, retry (old_top updated by compare_exchange_weak)
        }
    }

    /**
     * Get current size (not linearizable, for testing only)
     */
    size_t unsafe_size() const {
        size_t count = 0;
        Node* current = top_.load(std::memory_order_relaxed);
        while (current != nullptr) {
            ++count;
            current = current->next.load(std::memory_order_relaxed);
        }
        return count;
    }

    ~LockFreeStackWithHP() {
        // Delete all remaining nodes
        Node* current = top_.load(std::memory_order_relaxed);
        while (current != nullptr) {
            Node* next = current->next.load(std::memory_order_relaxed);
            delete current;
            current = next;
        }
    }
};

template <typename T>
thread_local std::unique_ptr<HazardPointerContext<typename LockFreeStackWithHP<T>::Node>>
    LockFreeStackWithHP<T>::hp_context_;

/**
 * Testing framework
 */
void test_correctness() {
    std::cout << "Testing Lock-Free Stack with Hazard Pointers:\n\n";

    LockFreeStackWithHP<int> stack;
    const int num_threads = 8;
    const int ops_per_thread = 1000;

    std::vector<std::thread> threads;
    std::atomic<int> push_count{0};
    std::atomic<int> pop_count{0};

    // Half pushers, half poppers
    for (int i = 0; i < num_threads; ++i) {
        if (i % 2 == 0) {
            // Pusher
            threads.emplace_back([&stack, &push_count, i, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    stack.push(i * ops_per_thread + j);
                    push_count.fetch_add(1, std::memory_order_relaxed);
                }
            });
        } else {
            // Popper
            threads.emplace_back([&stack, &pop_count, ops_per_thread]() {
                for (int j = 0; j < ops_per_thread; ++j) {
                    int value;
                    if (stack.pop(value)) {
                        pop_count.fetch_add(1, std::memory_order_relaxed);
                    }
                }
            });
        }
    }

    for (auto& t : threads) {
        t.join();
    }

    // Pop remaining items
    int value;
    while (stack.pop(value)) {
        pop_count.fetch_add(1, std::memory_order_relaxed);
    }

    std::cout << "Pushes: " << push_count.load() << "\n";
    std::cout << "Pops: " << pop_count.load() << "\n";
    std::cout << "Remaining in stack: " << stack.unsafe_size() << "\n";
    std::cout << (push_count.load() == pop_count.load() ? "✅ PASS" : "❌ FAIL") << "\n\n";
}

void compare_performance() {
    std::cout << "=== Performance Test ===\n";
    std::cout << "High contention scenario (many pushes and pops)\n\n";

    const int num_threads = 16;
    const int ops_per_thread = 50000;

    LockFreeStackWithHP<int> stack;
    std::vector<std::thread> threads;

    auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&stack, i, ops_per_thread]() {
            for (int j = 0; j < ops_per_thread; ++j) {
                if (j % 2 == 0) {
                    stack.push(i * ops_per_thread + j);
                } else {
                    int value;
                    stack.pop(value);
                }
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    std::cout << "Time: " << duration.count() << "ms\n";
    std::cout << "Throughput: " << (num_threads * ops_per_thread * 1000.0 / duration.count()) << " ops/sec\n";
    std::cout << "\n💡 Hazard pointers allow safe memory reclamation without GC\n";
    std::cout << "💡 Small performance overhead compared to unsafe version\n";
    std::cout << "💡 Critical for production lock-free code in C++\n";
}

void demonstrate_safety() {
    std::cout << "=== Memory Safety Demonstration ===\n\n";

    std::cout << "Without hazard pointers:\n";
    std::cout << "  ❌ Use-after-free bugs possible\n";
    std::cout << "  ❌ Undefined behavior with concurrent access\n";
    std::cout << "  ❌ No safe way to reclaim memory\n\n";

    std::cout << "With hazard pointers:\n";
    std::cout << "  ✅ Protected nodes cannot be deleted\n";
    std::cout << "  ✅ Deferred deletion until safe\n";
    std::cout << "  ✅ No garbage collector required\n";
    std::cout << "  ✅ Suitable for C++ production code\n\n";

    std::cout << "Hazard Pointer Protocol:\n";
    std::cout << "  1. Before dereferencing, set hazard pointer\n";
    std::cout << "  2. Re-read atomic pointer to verify unchanged\n";
    std::cout << "  3. If unchanged, node is protected\n";
    std::cout << "  4. After use, clear hazard pointer\n";
    std::cout << "  5. Before delete, check all hazard pointers\n\n";
}

} // namespace multiprocessor::part2::memory_reclamation

int main() {
    using namespace multiprocessor::part2::memory_reclamation;

    std::cout << "=== Hazard Pointers Memory Reclamation Test ===\n\n";

    demonstrate_safety();
    test_correctness();
    compare_performance();

    return 0;
}
