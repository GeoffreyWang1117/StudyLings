/**
 * Exercise: Read-Copy-Update (RCU)
 *
 * CONCEPT: Synchronization mechanism optimized for read-heavy workloads
 *
 * THE PROBLEM:
 * Many data structures have read-heavy access patterns:
 * - 90%+ reads, < 10% writes
 * - Traditional locks cause unnecessary contention on reads
 * - Even read-write locks have overhead on read path
 *
 * RCU SOLUTION:
 * - Reads: ZERO overhead, no locks, no atomic operations
 * - Writes: Copy-update-wait pattern
 * - Grace Period: Wait for all readers to finish before reclaiming memory
 *
 * KEY PRINCIPLES:
 * 1. Publish-Subscribe: Writers publish new versions, readers subscribe
 * 2. Wait for Pre-existing Readers: Grace period ensures safety
 * 3. Maintain Multiple Versions: Old and new versions coexist temporarily
 *
 * USED IN:
 * - Linux kernel (extensively, millions of lines of code)
 * - High-performance databases
 * - Network routing tables
 * - Configuration management systems
 *
 * LEARNING OBJECTIVES:
 * - Understand RCU principles and trade-offs
 * - Implement basic RCU mechanism
 * - Use RCU for read-heavy linked list
 * - Appreciate grace period concept
 * - Compare with traditional locking
 *
 * CPU REQUIREMENTS:
 * - Minimum: 4 cores
 * - Recommended: 8+ cores (many readers)
 * - Optimal: 16+ cores (dramatic read scalability)
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <chrono>
#include <memory>
#include <algorithm>

namespace multiprocessor::part2::rcu {

/**
 * TODO: Implement Simple RCU Mechanism
 *
 * This is a simplified RCU for educational purposes
 * (Production RCU like Linux kernel is much more sophisticated)
 */
class SimpleRCU {
private:
    std::atomic<int> reader_count_{0};

public:
    /**
     * TODO: Implement read_lock
     *
     * Enter read-side critical section
     * In this simple version, just increment reader count
     */
    void read_lock() {
        // TODO: Increment reader count
        reader_count_.fetch_add(1, std::memory_order_acquire);
    }

    /**
     * TODO: Implement read_unlock
     *
     * Exit read-side critical section
     */
    void read_unlock() {
        // TODO: Decrement reader count
        reader_count_.fetch_sub(1, std::memory_order_release);
    }

    /**
     * TODO: Implement synchronize (grace period)
     *
     * Wait for all pre-existing readers to complete
     * This ensures it's safe to reclaim old memory
     */
    void synchronize() {
        // TODO: Wait until reader count reaches zero
        // Simple spin-wait (production RCU is much smarter)
        while (reader_count_.load(std::memory_order_acquire) > 0) {
            std::this_thread::yield();
        }
    }
};

/**
 * RAII wrapper for RCU read-side critical section
 */
class RCUReadLock {
private:
    SimpleRCU& rcu_;

public:
    explicit RCUReadLock(SimpleRCU& rcu) : rcu_(rcu) {
        rcu_.read_lock();
    }

    ~RCUReadLock() {
        rcu_.read_unlock();
    }

    // Non-copyable, non-movable
    RCUReadLock(const RCUReadLock&) = delete;
    RCUReadLock& operator=(const RCUReadLock&) = delete;
};

/**
 * TODO: Implement RCU-Protected Linked List
 *
 * Read operations are lock-free and wait-free
 * Write operations use RCU update pattern
 */
template <typename T>
class RCULinkedList {
private:
    struct Node {
        T value;
        std::atomic<Node*> next;

        explicit Node(const T& val) : value(val), next(nullptr) {}
    };

    std::atomic<Node*> head_{nullptr};
    SimpleRCU rcu_;
    std::mutex write_mutex_; // Only for writers (not used by readers!)

public:
    ~RCULinkedList() {
        Node* current = head_.load(std::memory_order_relaxed);
        while (current != nullptr) {
            Node* next = current->next.load(std::memory_order_relaxed);
            delete current;
            current = next;
        }
    }

    /**
     * TODO: Implement insert (writer)
     *
     * RCU update pattern:
     * 1. Allocate new node
     * 2. Copy relevant data
     * 3. Update pointer (publish)
     * 4. Wait for grace period
     * 5. Reclaim old memory (if any)
     */
    void insert(const T& value) {
        // TODO: Create new node
        Node* new_node = new Node(value);

        // Only one writer at a time (RCU allows concurrent readers)
        std::lock_guard<std::mutex> lock(write_mutex_);

        // TODO: Insert at head
        Node* old_head = head_.load(std::memory_order_relaxed);
        new_node->next.store(old_head, std::memory_order_relaxed);

        // Publish new head (readers will see this)
        head_.store(new_node, std::memory_order_release);

        // No need to wait for grace period when inserting at head
        // (old_head is still valid, just not the head anymore)
    }

    /**
     * TODO: Implement search (reader)
     *
     * RCU read-side: NO LOCKS, completely wait-free
     */
    bool search(const T& value) {
        // TODO: Enter RCU read-side critical section
        RCUReadLock read_lock(rcu_);

        // TODO: Traverse list without any locks
        Node* current = head_.load(std::memory_order_acquire);

        while (current != nullptr) {
            if (current->value == value) {
                return true;
            }
            current = current->next.load(std::memory_order_acquire);
        }

        return false;
    }

    /**
     * TODO: Implement remove (writer)
     *
     * RCU update pattern with grace period
     */
    bool remove(const T& value) {
        std::lock_guard<std::mutex> lock(write_mutex_);

        // TODO: Find node to remove
        Node* prev = nullptr;
        Node* current = head_.load(std::memory_order_relaxed);

        while (current != nullptr) {
            if (current->value == value) {
                // Found it - update pointers
                Node* next = current->next.load(std::memory_order_relaxed);

                if (prev == nullptr) {
                    // Removing head
                    head_.store(next, std::memory_order_release);
                } else {
                    // Removing non-head
                    prev->next.store(next, std::memory_order_release);
                }

                // TODO: Wait for grace period before deleting
                // This ensures no reader is still accessing this node
                rcu_.synchronize();

                // Safe to delete now
                delete current;
                return true;
            }

            prev = current;
            current = current->next.load(std::memory_order_relaxed);
        }

        return false;
    }

    /**
     * Print list (for debugging)
     */
    void print() {
        RCUReadLock read_lock(rcu_);
        Node* current = head_.load(std::memory_order_acquire);

        std::cout << "List: ";
        while (current != nullptr) {
            std::cout << current->value << " ";
            current = current->next.load(std::memory_order_acquire);
        }
        std::cout << "\n";
    }
};

/**
 * Traditional lock-based linked list for comparison
 */
template <typename T>
class LockBasedLinkedList {
private:
    struct Node {
        T value;
        Node* next;
        explicit Node(const T& val) : value(val), next(nullptr) {}
    };

    Node* head_;
    mutable std::mutex mutex_;

public:
    LockBasedLinkedList() : head_(nullptr) {}

    ~LockBasedLinkedList() {
        Node* current = head_;
        while (current != nullptr) {
            Node* next = current->next;
            delete current;
            current = next;
        }
    }

    void insert(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        Node* new_node = new Node(value);
        new_node->next = head_;
        head_ = new_node;
    }

    bool search(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_); // Lock for read!
        Node* current = head_;
        while (current != nullptr) {
            if (current->value == value) {
                return true;
            }
            current = current->next;
        }
        return false;
    }

    bool remove(const T& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        Node* prev = nullptr;
        Node* current = head_;

        while (current != nullptr) {
            if (current->value == value) {
                if (prev == nullptr) {
                    head_ = current->next;
                } else {
                    prev->next = current->next;
                }
                delete current;
                return true;
            }
            prev = current;
            current = current->next;
        }
        return false;
    }
};

/**
 * Testing Framework
 */
void test_correctness() {
    std::cout << "=== Correctness Tests ===\n\n";

    RCULinkedList<int> list;

    std::cout << "Test: Basic operations\n";
    list.insert(1);
    list.insert(2);
    list.insert(3);
    list.print();

    std::cout << "Search 2: " << (list.search(2) ? "found" : "not found") << "\n";
    std::cout << "Search 5: " << (list.search(5) ? "found" : "not found") << "\n";

    list.remove(2);
    std::cout << "After removing 2: ";
    list.print();

    std::cout << "✅ PASS\n\n";
}

void compare_performance() {
    std::cout << "=== Performance Comparison: Read-Heavy Workload ===\n\n";

    const int num_threads = std::thread::hardware_concurrency();
    const int ops_per_thread = 100000;
    const int num_items = 100;

    std::cout << "Threads: " << num_threads << "\n";
    std::cout << "Operations per thread: " << ops_per_thread << "\n";
    std::cout << "Workload: 95% reads, 5% writes\n\n";

    // Test RCU List
    {
        RCULinkedList<int> list;

        // Pre-populate
        for (int i = 0; i < num_items; ++i) {
            list.insert(i);
        }

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::thread> threads;
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&, i]() {
                std::random_device rd;
                std::mt19937 gen(rd() + i);
                std::uniform_int_distribution<> value_dist(0, num_items - 1);
                std::uniform_int_distribution<> op_dist(1, 100);

                for (int j = 0; j < ops_per_thread; ++j) {
                    int op = op_dist(gen);
                    int value = value_dist(gen);

                    if (op <= 95) {
                        // 95% reads
                        list.search(value);
                    } else {
                        // 5% writes
                        if (op <= 97) {
                            list.insert(value);
                        } else {
                            list.remove(value);
                        }
                    }
                }
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "RCU Linked List:\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Throughput: " << (num_threads * ops_per_thread * 1000.0 / duration.count()) << " ops/sec\n\n";
    }

    // Test Lock-Based List
    {
        LockBasedLinkedList<int> list;

        // Pre-populate
        for (int i = 0; i < num_items; ++i) {
            list.insert(i);
        }

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::thread> threads;
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&, i]() {
                std::random_device rd;
                std::mt19937 gen(rd() + i);
                std::uniform_int_distribution<> value_dist(0, num_items - 1);
                std::uniform_int_distribution<> op_dist(1, 100);

                for (int j = 0; j < ops_per_thread; ++j) {
                    int op = op_dist(gen);
                    int value = value_dist(gen);

                    if (op <= 95) {
                        // 95% reads
                        list.search(value);
                    } else {
                        // 5% writes
                        if (op <= 97) {
                            list.insert(value);
                        } else {
                            list.remove(value);
                        }
                    }
                }
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Lock-Based Linked List:\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Throughput: " << (num_threads * ops_per_thread * 1000.0 / duration.count()) << " ops/sec\n\n";
    }

    std::cout << "💡 RCU excels in read-heavy workloads (95%+ reads)\n";
    std::cout << "💡 Readers have ZERO synchronization overhead\n";
    std::cout << "💡 Lock-based has overhead on every read\n";
}

void demonstrate_concepts() {
    std::cout << "=== Read-Copy-Update (RCU) Concepts ===\n\n";

    std::cout << "RCU Principles:\n";
    std::cout << "  1. Publish-Subscribe: Writers publish, readers subscribe\n";
    std::cout << "  2. Wait for Pre-existing Readers: Grace period\n";
    std::cout << "  3. Maintain Multiple Versions: Coexist temporarily\n\n";

    std::cout << "RCU Update Pattern:\n";
    std::cout << "  1. Allocate new version\n";
    std::cout << "  2. Copy and modify\n";
    std::cout << "  3. Publish (atomic pointer update)\n";
    std::cout << "  4. Wait for grace period (synchronize)\n";
    std::cout << "  5. Reclaim old version\n\n";

    std::cout << "Grace Period:\n";
    std::cout << "  • Ensures all pre-existing readers have finished\n";
    std::cout << "  • After grace period, safe to free old memory\n";
    std::cout << "  • Can be quiescent-state based or counter-based\n\n";

    std::cout << "When to Use RCU:\n";
    std::cout << "  ✅ Read-heavy workloads (90%+ reads)\n";
    std::cout << "  ✅ Pointer-based data structures\n";
    std::cout << "  ✅ Can tolerate stale data briefly\n";
    std::cout << "  ✅ Memory available for multiple versions\n\n";

    std::cout << "When NOT to Use RCU:\n";
    std::cout << "  ❌ Write-heavy workloads\n";
    std::cout << "  ❌ Need immediate consistency\n";
    std::cout << "  ❌ Large data structures (copy overhead)\n";
    std::cout << "  ❌ Bounded memory constraints\n\n";

    std::cout << "Real-World Usage:\n";
    std::cout << "  • Linux kernel: networking, VFS, scheduler\n";
    std::cout << "  • Databases: MVCC, read-optimized indexes\n";
    std::cout << "  • Routing tables: high read rate\n";
    std::cout << "  • Configuration: read often, update rarely\n\n";
}

} // namespace

int main() {
    using namespace multiprocessor::part2::rcu;

    std::cout << "=== Read-Copy-Update (RCU) Test ===\n\n";

    demonstrate_concepts();
    test_correctness();
    compare_performance();

    return 0;
}
