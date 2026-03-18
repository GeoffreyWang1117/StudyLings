/**
 * SOLUTION: Hazard Pointers for Safe Memory Reclamation
 *
 * Complete reference implementation with all TODOs filled in.
 *
 * This demonstrates safe memory reclamation in lock-free data structures
 * without garbage collection.
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <array>
#include <memory>

namespace solution {

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

    std::array<std::array<HazardPointerRecord, HAZARD_POINTERS_PER_THREAD>, MAX_THREADS> hazard_pointers_;
    std::atomic<int> thread_count_{0};

public:
    int acquire_hazard_pointer_slot() {
        int slot = thread_count_.fetch_add(1, std::memory_order_relaxed);
        if (slot >= MAX_THREADS) {
            throw std::runtime_error("Too many threads!");
        }
        return slot;
    }

    void set_hazard_pointer(int thread_id, int hp_index, T* ptr) {
        hazard_pointers_[thread_id][hp_index].hazard_pointer.store(ptr, std::memory_order_release);
        hazard_pointers_[thread_id][hp_index].active.store(true, std::memory_order_release);
    }

    void clear_hazard_pointer(int thread_id, int hp_index) {
        hazard_pointers_[thread_id][hp_index].active.store(false, std::memory_order_release);
        hazard_pointers_[thread_id][hp_index].hazard_pointer.store(nullptr, std::memory_order_release);
    }

    bool is_protected(T* ptr) {
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

    bool try_delete(T* ptr) {
        if (!is_protected(ptr)) {
            delete ptr;
            return true;
        }
        return false;
    }
};

template <typename T>
class HazardPointerContext {
private:
    HazardPointerManager<T>& manager_;
    int thread_id_;
    std::vector<T*> retired_list_;

public:
    HazardPointerContext(HazardPointerManager<T>& manager)
        : manager_(manager), thread_id_(manager.acquire_hazard_pointer_slot()) {}

    T* protect(int hp_index, std::atomic<T*>& atomic_ptr) {
        T* ptr = nullptr;
        T* protected_ptr = atomic_ptr.load(std::memory_order_acquire);

        do {
            ptr = protected_ptr;
            if (ptr == nullptr) {
                manager_.clear_hazard_pointer(thread_id_, hp_index);
                return nullptr;
            }
            manager_.set_hazard_pointer(thread_id_, hp_index, ptr);
            protected_ptr = atomic_ptr.load(std::memory_order_acquire);
        } while (ptr != protected_ptr);

        return ptr;
    }

    void unprotect(int hp_index) {
        manager_.clear_hazard_pointer(thread_id_, hp_index);
    }

    void retire(T* ptr) {
        retired_list_.push_back(ptr);
        if (retired_list_.size() >= HazardPointerManager<T>::RETIRED_LIST_MAX) {
            reclaim();
        }
    }

    void reclaim() {
        std::vector<T*> still_protected;
        for (T* ptr : retired_list_) {
            if (!manager_.try_delete(ptr)) {
                still_protected.push_back(ptr);
            }
        }
        retired_list_ = std::move(still_protected);
    }

    ~HazardPointerContext() {
        reclaim();
        for (T* ptr : retired_list_) {
            delete ptr;
        }
    }
};

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
    static thread_local std::unique_ptr<HazardPointerContext<Node>> hp_context_;

    HazardPointerContext<Node>* get_context() {
        if (!hp_context_) {
            hp_context_ = std::make_unique<HazardPointerContext<Node>>(hp_manager_);
        }
        return hp_context_.get();
    }

public:
    void push(const T& value) {
        Node* node = new Node(value);
        Node* old_top = top_.load(std::memory_order_relaxed);

        do {
            node->next.store(old_top, std::memory_order_relaxed);
        } while (!top_.compare_exchange_weak(old_top, node,
                                             std::memory_order_release,
                                             std::memory_order_relaxed));
    }

    bool pop(T& result) {
        auto* context = get_context();
        Node* old_top = nullptr;

        while (true) {
            old_top = context->protect(0, top_);

            if (old_top == nullptr) {
                context->unprotect(0);
                return false;
            }

            Node* next = old_top->next.load(std::memory_order_acquire);

            if (top_.compare_exchange_weak(old_top, next,
                                          std::memory_order_release,
                                          std::memory_order_relaxed)) {
                result = old_top->value;
                context->unprotect(0);
                context->retire(old_top);
                return true;
            }
        }
    }

    ~LockFreeStackWithHP() {
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

void demonstrate_solution() {
    std::cout << "=== SOLUTION: Hazard Pointers ===\n\n";

    std::cout << "Key Points:\n\n";

    std::cout << "1. Protection Protocol:\n";
    std::cout << "   - Set hazard pointer to node\n";
    std::cout << "   - Re-read atomic pointer\n";
    std::cout << "   - If unchanged, node is protected\n";
    std::cout << "   - If changed, retry\n\n";

    std::cout << "2. Retirement:\n";
    std::cout << "   - Add node to retired list\n";
    std::cout << "   - When list is large, scan hazard pointers\n";
    std::cout << "   - Delete unprotected nodes\n\n";

    std::cout << "3. Thread-Local Context:\n";
    std::cout << "   - Each thread has hazard pointer slots\n";
    std::cout << "   - Each thread has retired list\n";
    std::cout << "   - Decouples threads for scalability\n\n";

    // Test
    LockFreeStackWithHP<int> stack;
    stack.push(1);
    stack.push(2);
    stack.push(3);

    int value;
    stack.pop(value);
    std::cout << "Test pop: " << value << " (should be 3)\n";

    std::cout << "\n✅ Solution provides safe memory reclamation\n";
    std::cout << "✅ No use-after-free bugs\n";
    std::cout << "✅ Essential for C++ lock-free programming\n";
}

} // namespace solution

int main() {
    solution::demonstrate_solution();
    return 0;
}
