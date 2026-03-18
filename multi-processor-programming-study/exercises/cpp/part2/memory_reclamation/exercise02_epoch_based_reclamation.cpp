/**
 * Exercise: Epoch-Based Reclamation (EBR) for Safe Memory Reclamation (C++20)
 *
 * CONCEPT: Safe memory reclamation using global epochs
 *
 * Epoch-Based Reclamation is an alternative to Hazard Pointers for solving
 * the memory reclamation problem in lock-free data structures.
 *
 * KEY DIFFERENCES FROM HAZARD POINTERS:
 * - Hazard Pointers: Per-pointer protection (fine-grained)
 * - EBR: Epoch-based protection (coarse-grained)
 *
 * HOW EBR WORKS:
 * 1. Global epoch counter (cycles through 0, 1, 2, 0, 1, 2, ...)
 * 2. Each thread announces which epoch it's in before accessing shared data
 * 3. Memory is retired to the current epoch's retired list
 * 4. Periodically advance global epoch
 * 5. Reclaim memory from epoch e when ALL threads have moved beyond epoch e
 *
 * ALGORITHM:
 * - Global epoch: Shared counter (0, 1, 2)
 * - Thread local epoch: Each thread's announced epoch
 * - Retired lists: One list per epoch (3 lists total)
 * - Reclamation: Safe to reclaim epoch e when all threads are in epoch (e+1) or (e+2)
 *
 * ADVANTAGES OVER HAZARD POINTERS:
 * ✓ Simpler implementation
 * ✓ Lower overhead per operation
 * ✓ Better for high-throughput scenarios
 * ✓ Batch reclamation (better cache behavior)
 *
 * DISADVANTAGES:
 * ✗ Coarser granularity (may delay reclamation longer)
 * ✗ Unbounded memory if threads stall
 * ✗ Requires periodic epoch advancement
 *
 * REAL-WORLD USAGE:
 * - Used in many production systems (userspace RCU, Crossbeam in Rust)
 * - Excellent for high-throughput lock-free data structures
 * - Popular in systems programming (databases, runtime systems)
 *
 * LEARNING OBJECTIVES:
 * - Understand epoch-based memory reclamation in C++
 * - Implement EBR manager with global epoch
 * - Use EBR with lock-free stack
 * - Compare with Hazard Pointers approach
 * - Proper memory management with delete
 *
 * Compilation:
 *   g++ -std=c++20 -pthread exercise02_epoch_based_reclamation.cpp -o ebr
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <array>
#include <queue>
#include <mutex>
#include <chrono>
#include <random>
#include <functional>

namespace multiprocessor::ebr {

/**
 * TODO: Implement Epoch-Based Reclamation Manager
 *
 * Manages global epoch and per-thread epoch tracking
 */
template<typename T>
class EpochManager {
private:
    static constexpr int NUM_EPOCHS = 3;
    static constexpr int MAX_THREADS = 128;
    static constexpr int64_t INACTIVE_EPOCH = -1;

    /**
     * Thread-local epoch information
     */
    struct ThreadEpochInfo {
        std::atomic<int64_t> local_epoch{INACTIVE_EPOCH};
        int thread_id;

        ThreadEpochInfo() : thread_id(0) {}
    };

    // Global epoch counter
    std::atomic<int64_t> global_epoch_{0};

    // Per-thread epoch tracking
    std::array<ThreadEpochInfo, MAX_THREADS> thread_epochs_;
    std::atomic<int> thread_count_{0};

    // Retired lists: one per epoch
    std::array<std::queue<T*>, NUM_EPOCHS> retired_lists_;
    std::array<std::mutex, NUM_EPOCHS> retired_mutexes_;

    // Custom deleter
    std::function<void(T*)> deleter_;

public:
    EpochManager() {
        // Initialize thread epoch info
        for (int i = 0; i < MAX_THREADS; i++) {
            thread_epochs_[i].thread_id = i;
            thread_epochs_[i].local_epoch.store(INACTIVE_EPOCH, std::memory_order_relaxed);
        }

        // Default deleter
        deleter_ = [](T* ptr) {
            delete ptr;
        };
    }

    ~EpochManager() {
        // Clean up any remaining retired nodes
        for (int i = 0; i < NUM_EPOCHS; i++) {
            std::lock_guard<std::mutex> lock(retired_mutexes_[i]);
            while (!retired_lists_[i].empty()) {
                T* node = retired_lists_[i].front();
                retired_lists_[i].pop();
                deleter_(node);
            }
        }
    }

    /**
     * Set custom deleter for cleanup
     */
    void set_deleter(std::function<void(T*)> deleter) {
        deleter_ = deleter;
    }

    /**
     * TODO: Register a thread to get its thread ID
     */
    int register_thread() {
        int thread_id = thread_count_.fetch_add(1, std::memory_order_relaxed);
        if (thread_id >= MAX_THREADS) {
            throw std::runtime_error("Too many threads!");
        }
        return thread_id;
    }

    /**
     * TODO: Enter critical section - announce current epoch
     *
     * Thread must call this before accessing shared data
     */
    void enter_critical_section(int thread_id) {
        // TODO: Set thread's local epoch to current global epoch
        int64_t current_epoch = global_epoch_.load(std::memory_order_acquire);
        thread_epochs_[thread_id].local_epoch.store(current_epoch, std::memory_order_release);
    }

    /**
     * TODO: Exit critical section - mark as inactive
     *
     * Thread must call this after done accessing shared data
     */
    void exit_critical_section(int thread_id) {
        // TODO: Set thread's local epoch to INACTIVE
        thread_epochs_[thread_id].local_epoch.store(INACTIVE_EPOCH, std::memory_order_release);
    }

    /**
     * TODO: Retire a node to the current epoch's retired list
     *
     * @param node The node to retire
     */
    void retire(T* node) {
        // TODO: Add node to retired list for current global epoch
        int64_t current_epoch = global_epoch_.load(std::memory_order_acquire);
        int epoch_index = static_cast<int>(current_epoch % NUM_EPOCHS);

        std::lock_guard<std::mutex> lock(retired_mutexes_[epoch_index]);
        retired_lists_[epoch_index].push(node);
    }

    /**
     * TODO: Try to advance global epoch
     *
     * Advances epoch if safe, and reclaims memory from old epochs
     *
     * @return true if epoch was advanced
     */
    bool try_advance_epoch() {
        int64_t current_epoch = global_epoch_.load(std::memory_order_acquire);

        // Check if all threads have moved beyond the old epoch
        if (!can_advance_epoch(current_epoch)) {
            return false;
        }

        // Try to advance global epoch (CAS to handle concurrent attempts)
        int64_t new_epoch = current_epoch + 1;
        if (!global_epoch_.compare_exchange_strong(current_epoch, new_epoch,
                                                   std::memory_order_acq_rel,
                                                   std::memory_order_acquire)) {
            return false; // Another thread advanced it
        }

        // Successfully advanced! Now reclaim memory from the old epoch
        reclaim_old_epoch(new_epoch);

        return true;
    }

    /**
     * Get current global epoch (for debugging/testing)
     */
    int64_t get_global_epoch() const {
        return global_epoch_.load(std::memory_order_acquire);
    }

    /**
     * Get number of retired nodes (for testing)
     */
    size_t get_retired_count() const {
        size_t count = 0;
        for (int i = 0; i < NUM_EPOCHS; i++) {
            std::lock_guard<std::mutex> lock(retired_mutexes_[i]);
            count += retired_lists_[i].size();
        }
        return count;
    }

private:
    /**
     * Helper: Check if we can safely advance from current_epoch
     *
     * Safe to advance if all active threads are at current_epoch or newer
     */
    bool can_advance_epoch(int64_t current_epoch) const {
        int active_threads = thread_count_.load(std::memory_order_acquire);

        for (int i = 0; i < active_threads; i++) {
            int64_t thread_epoch = thread_epochs_[i].local_epoch.load(std::memory_order_acquire);

            // Skip inactive threads
            if (thread_epoch == INACTIVE_EPOCH) {
                continue;
            }

            // If any thread is in an old epoch, cannot advance
            if (thread_epoch < current_epoch) {
                return false;
            }
        }

        return true;
    }

    /**
     * Helper: Reclaim memory from epochs that are now safe
     *
     * After advancing to new_epoch, we can reclaim epoch (new_epoch - NUM_EPOCHS)
     * because all threads have moved at least NUM_EPOCHS forward
     */
    void reclaim_old_epoch(int64_t new_epoch) {
        // Calculate which epoch is now safe to reclaim
        if (new_epoch < NUM_EPOCHS) {
            return; // Not enough epochs have passed yet
        }

        int64_t safe_epoch = new_epoch - NUM_EPOCHS;
        int reclaim_index = static_cast<int>(safe_epoch % NUM_EPOCHS);

        // Reclaim all nodes from this epoch
        std::lock_guard<std::mutex> lock(retired_mutexes_[reclaim_index]);
        while (!retired_lists_[reclaim_index].empty()) {
            T* node = retired_lists_[reclaim_index].front();
            retired_lists_[reclaim_index].pop();
            deleter_(node);
        }
    }
};

/**
 * Lock-free Stack using Epoch-Based Reclamation
 *
 * Demonstrates how to use EBR in a lock-free data structure
 */
template<typename T>
class EBRStack {
private:
    struct Node {
        T value;
        std::atomic<Node*> next;

        explicit Node(const T& val) : value(val), next(nullptr) {}
    };

    std::atomic<Node*> head_{nullptr};
    EpochManager<Node> epoch_manager_;
    thread_local static int thread_id_;
    std::atomic<bool> thread_registered_{false};

public:
    EBRStack() = default;

    ~EBRStack() {
        // Clean up remaining nodes
        Node* current = head_.load();
        while (current != nullptr) {
            Node* next = current->next.load();
            delete current;
            current = next;
        }
    }

    /**
     * Get or register thread ID
     */
    int get_thread_id() {
        if (thread_id_ == -1) {
            thread_id_ = epoch_manager_.register_thread();
        }
        return thread_id_;
    }

    /**
     * Push a value onto the stack
     */
    void push(const T& value) {
        Node* new_node = new Node(value);

        // No need for epoch protection during push (no reads)
        while (true) {
            Node* old_head = head_.load(std::memory_order_acquire);
            new_node->next.store(old_head, std::memory_order_relaxed);

            if (head_.compare_exchange_weak(old_head, new_node,
                                           std::memory_order_release,
                                           std::memory_order_acquire)) {
                return;
            }
        }
    }

    /**
     * Pop a value from the stack (using EBR)
     */
    bool pop(T& value) {
        int tid = get_thread_id();

        // Enter critical section (announce current epoch)
        epoch_manager_.enter_critical_section(tid);

        bool success = false;
        try {
            while (true) {
                Node* old_head = head_.load(std::memory_order_acquire);

                if (old_head == nullptr) {
                    break; // Stack is empty
                }

                Node* new_head = old_head->next.load(std::memory_order_acquire);

                if (head_.compare_exchange_weak(old_head, new_head,
                                               std::memory_order_release,
                                               std::memory_order_acquire)) {
                    value = old_head->value;
                    success = true;

                    // Retire the old head node
                    epoch_manager_.retire(old_head);

                    // Periodically try to advance epoch
                    static thread_local std::mt19937 rng(std::random_device{}());
                    static thread_local std::uniform_real_distribution<> dist(0.0, 1.0);
                    if (dist(rng) < 0.1) { // 10% chance
                        epoch_manager_.try_advance_epoch();
                    }

                    break;
                }
            }
        } catch (...) {
            epoch_manager_.exit_critical_section(tid);
            throw;
        }

        // Exit critical section (mark as inactive)
        epoch_manager_.exit_critical_section(tid);

        return success;
    }

    /**
     * Check if stack is empty (uses EBR)
     */
    bool is_empty() {
        int tid = get_thread_id();

        epoch_manager_.enter_critical_section(tid);
        bool empty = (head_.load(std::memory_order_acquire) == nullptr);
        epoch_manager_.exit_critical_section(tid);

        return empty;
    }

    /**
     * Force epoch advancement (for testing)
     */
    void advance_epoch() {
        epoch_manager_.try_advance_epoch();
    }

    /**
     * Get number of retired nodes (for testing)
     */
    size_t get_retired_count() const {
        return epoch_manager_.get_retired_count();
    }

    /**
     * Get global epoch (for testing)
     */
    int64_t get_global_epoch() const {
        return epoch_manager_.get_global_epoch();
    }
};

// Thread-local storage definition
template<typename T>
thread_local int EBRStack<T>::thread_id_ = -1;

/**
 * Test basic correctness
 */
void test_correctness() {
    std::cout << "Test 1: Basic Correctness\n";

    EBRStack<int> stack;

    // Push some values
    for (int i = 0; i < 10; i++) {
        stack.push(i);
    }

    // Pop and verify LIFO order
    bool correct = true;
    for (int i = 9; i >= 0; i--) {
        int value;
        if (!stack.pop(value) || value != i) {
            correct = false;
            std::cout << "  ❌ Expected " << i << ", got " << value << "\n";
        }
    }

    if (correct && stack.is_empty()) {
        std::cout << "  ✅ PASS - Stack operations work correctly!\n";
    } else {
        std::cout << "  ❌ FAIL - Stack operations incorrect!\n";
    }
}

/**
 * Test memory reclamation
 */
void test_memory_reclamation() {
    std::cout << "\nTest 2: Memory Reclamation\n";

    EBRStack<int> stack;

    // Push and pop to create retired nodes
    for (int i = 0; i < 100; i++) {
        stack.push(i);
    }

    for (int i = 0; i < 100; i++) {
        int value;
        stack.pop(value);
    }

    std::cout << "  Retired nodes before reclamation: " << stack.get_retired_count() << "\n";
    std::cout << "  Global epoch: " << stack.get_global_epoch() << "\n";

    // Force epoch advancements to trigger reclamation
    for (int i = 0; i < 10; i++) {
        stack.advance_epoch();
    }

    std::cout << "  Retired nodes after reclamation: " << stack.get_retired_count() << "\n";
    std::cout << "  Global epoch: " << stack.get_global_epoch() << "\n";

    if (stack.get_retired_count() < 100) {
        std::cout << "  ✅ PASS - Memory is being reclaimed!\n";
    } else {
        std::cout << "  ⚠️  WARN - Memory reclamation may not be working\n";
    }
}

/**
 * Test concurrent operations
 */
void test_concurrent_operations() {
    std::cout << "\nTest 3: Concurrent Operations\n";

    const int num_threads = 8;
    const int operations_per_thread = 10000;

    EBRStack<int> stack;
    std::vector<std::thread> threads;

    // Half push, half pop
    for (int i = 0; i < num_threads; i++) {
        threads.emplace_back([&stack, i, operations_per_thread]() {
            for (int j = 0; j < operations_per_thread; j++) {
                if (i % 2 == 0) {
                    stack.push(i * 1000000 + j);
                } else {
                    int value;
                    stack.pop(value); // May fail if empty
                }
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    // Force reclamation
    for (int i = 0; i < 10; i++) {
        stack.advance_epoch();
    }

    std::cout << "  Threads: " << num_threads << "\n";
    std::cout << "  Operations per thread: " << operations_per_thread << "\n";
    std::cout << "  Final retired count: " << stack.get_retired_count() << "\n";
    std::cout << "  Final global epoch: " << stack.get_global_epoch() << "\n";
    std::cout << "  ✅ PASS - No crashes! EBR works under concurrency!\n";

    std::cout << "\n💡 Key Insights:\n";
    std::cout << "  • EBR provides safe memory reclamation\n";
    std::cout << "  • Simpler than Hazard Pointers (coarse-grained)\n";
    std::cout << "  • Better throughput for high-contention scenarios\n";
    std::cout << "  • Widely used in production (userspace RCU, Crossbeam)\n";
}

} // namespace multiprocessor::ebr

int main() {
    using namespace multiprocessor::ebr;

    std::cout << "=== Epoch-Based Reclamation Test (C++) ===\n\n";

    test_correctness();
    test_memory_reclamation();
    test_concurrent_operations();

    return 0;
}
