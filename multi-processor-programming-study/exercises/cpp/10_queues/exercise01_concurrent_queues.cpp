/**
 * Exercise: Concurrent Queues (C++20)
 *
 * CONCEPT: Lock-free and blocking concurrent queues
 *
 * Queue implementations:
 * - Bounded Blocking: Fixed capacity with condition variables
 * - Lock-Free: Michael-Scott queue using CAS
 *
 * LEARNING OBJECTIVES:
 * - Implement blocking queue with condition variables
 * - Implement Michael-Scott lock-free queue
 * - Handle the ABA problem
 * - Understand producer-consumer patterns
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>
#include <mutex>
#include <condition_variable>
#include <optional>
#include <chrono>
#include <iomanip>

namespace multiprocessor::queues {

/**
 * TODO: Implement Bounded Blocking Queue
 *
 * Fixed-size array-based queue with blocking
 */
template <typename T>
class BoundedQueue {
private:
    std::vector<T> items;
    int head = 0;
    int tail = 0;
    int size = 0;
    const int capacity;

    // TODO: Add mutex and condition variables
    // HINT: std::mutex, std::condition_variable for not_full and not_empty

public:
    explicit BoundedQueue(int cap) : items(cap), capacity(cap) {
        // TODO: Initialize
    }

    /**
     * TODO: Implement blocking enqueue
     *
     * Wait while full, then add item
     */
    void enqueue(const T& item) {
        // TODO: Lock mutex
        // TODO: Wait on not_full while size == capacity
        // TODO: Add item to items[tail]
        // TODO: Update tail and size
        // TODO: Notify not_empty
    }

    /**
     * TODO: Implement blocking dequeue
     *
     * Wait while empty, then remove item
     */
    T dequeue() {
        // TODO: Lock mutex
        // TODO: Wait on not_empty while size == 0
        // TODO: Get item from items[head]
        // TODO: Update head and size
        // TODO: Notify not_full
        // TODO: Return item
        return T{};
    }

    int get_size() const {
        return size;
    }
};

/**
 * TODO: Implement Michael-Scott Lock-Free Queue
 *
 * Classic lock-free queue using CAS
 * Handles concurrent enqueue and dequeue operations
 */
template <typename T>
class LockFreeQueue {
private:
    struct Node {
        T value;
        std::atomic<Node*> next;

        Node() : next(nullptr) {}
        explicit Node(const T& val) : value(val), next(nullptr) {}
    };

    // TODO: Add std::atomic<Node*> for head and tail

public:
    LockFreeQueue() {
        // TODO: Initialize with dummy node
        // HINT: Both head and tail point to dummy initially
    }

    ~LockFreeQueue() {
        // TODO: Clean up remaining nodes
    }

    /**
     * TODO: Implement lock-free enqueue (Michael-Scott algorithm)
     *
     * 1. Create new node
     * 2. Loop:
     *    a. Read tail and next
     *    b. Check consistency (tail hasn't changed)
     *    c. If tail.next is null, try CAS it to new node
     *    d. If CAS succeeds, try to swing tail forward
     *    e. If tail.next not null, help other thread by swinging tail
     */
    void enqueue(const T& item) {
        Node* node = new Node(item);
        // TODO: Implement Michael-Scott enqueue
    }

    /**
     * TODO: Implement lock-free dequeue
     *
     * 1. Loop:
     *    a. Read head, tail, and first real node
     *    b. Check consistency
     *    c. If queue empty (head == tail), return nullopt
     *    d. If tail falling behind, help advance it
     *    e. Read value before CAS (important!)
     *    f. Try to swing head forward with CAS
     */
    std::optional<T> dequeue() {
        // TODO: Implement Michael-Scott dequeue
        // HINT: Skip dummy node, return first real node's value
        return std::nullopt;
    }
};

/**
 * Performance testing
 */
class PerformanceTest {
public:
    template <typename Queue>
    static void test_queue(const std::string& name, Queue& queue,
                          int num_producers, int num_consumers,
                          int items_per_producer) {
        std::vector<std::thread> threads;

        auto start_time = std::chrono::high_resolution_clock::now();

        // Producers
        for (int i = 0; i < num_producers; ++i) {
            threads.emplace_back([&queue, i, items_per_producer]() {
                for (int j = 0; j < items_per_producer; ++j) {
                    queue.enqueue(i * items_per_producer + j);
                }
            });
        }

        // Consumers
        std::atomic<int> consumed{0};
        for (int i = 0; i < num_consumers; ++i) {
            threads.emplace_back([&queue, &consumed, items_per_producer]() {
                for (int j = 0; j < items_per_producer; ++j) {
                    auto item = queue.dequeue();
                    if constexpr (std::is_same_v<Queue, LockFreeQueue<int>>) {
                        if (item.has_value()) {
                            consumed.fetch_add(1);
                        }
                    } else {
                        consumed.fetch_add(1);
                    }
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
                  << " (consumed=" << consumed.load() << ")\n";
    }
};

void test_bounded_queue() {
    std::cout << "Testing Bounded Queue:\n";

    BoundedQueue<int> queue(100);
    const int num_producers = 5;
    const int num_consumers = 5;
    const int items_per_producer = 1000;

    std::vector<std::thread> threads;

    // Producers
    for (int i = 0; i < num_producers; ++i) {
        threads.emplace_back([&queue, i, items_per_producer]() {
            for (int j = 0; j < items_per_producer; ++j) {
                queue.enqueue(i * items_per_producer + j);
            }
        });
    }

    // Consumers
    std::atomic<int> consumed{0};
    for (int i = 0; i < num_consumers; ++i) {
        threads.emplace_back([&queue, &consumed, items_per_producer]() {
            for (int j = 0; j < items_per_producer; ++j) {
                queue.dequeue();
                consumed.fetch_add(1);
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    int expected = num_producers * items_per_producer;
    int actual = consumed.load();

    std::cout << "Produced: " << expected << "\n";
    std::cout << "Consumed: " << actual << "\n";
    std::cout << (actual == expected ? "✅ PASS\n\n" : "❌ FAIL\n\n");
}

void test_lock_free_queue() {
    std::cout << "Testing Lock-Free Queue:\n";

    LockFreeQueue<int> queue;
    const int num_threads = 10;
    const int items_per_thread = 1000;

    // Enqueue phase
    std::vector<std::thread> enqueuers;
    for (int i = 0; i < num_threads; ++i) {
        enqueuers.emplace_back([&queue, i, items_per_thread]() {
            for (int j = 0; j < items_per_thread; ++j) {
                queue.enqueue(i * items_per_thread + j);
            }
        });
    }
    for (auto& t : enqueuers) t.join();

    // Dequeue phase
    std::atomic<int> dequeue_count{0};
    std::vector<std::thread> dequeuers;
    for (int i = 0; i < num_threads; ++i) {
        dequeuers.emplace_back([&queue, &dequeue_count, items_per_thread]() {
            for (int j = 0; j < items_per_thread; ++j) {
                auto item = queue.dequeue();
                if (item.has_value()) {
                    dequeue_count.fetch_add(1);
                }
            }
        });
    }
    for (auto& t : dequeuers) t.join();

    int expected = num_threads * items_per_thread;
    int actual = dequeue_count.load();

    std::cout << "Expected: " << expected << "\n";
    std::cout << "Dequeued: " << actual << "\n";
    std::cout << (actual == expected ? "✅ PASS\n\n" : "❌ FAIL\n\n");
}

void demonstrate_aba_problem() {
    std::cout << "=== ABA Problem in Queues ===\n";
    std::cout << "Problem: Node reuse can cause ABA issues\n";
    std::cout << "Thread 1: Reads node A\n";
    std::cout << "Thread 2: Dequeues A, dequeues B, enqueues A (reused)\n";
    std::cout << "Thread 1: CAS succeeds, but A is different!\n\n";
    std::cout << "Solutions:\n";
    std::cout << "- Don't reuse nodes immediately\n";
    std::cout << "- Use version numbers/stamps\n";
    std::cout << "- Use hazard pointers\n";
    std::cout << "- Use epoch-based reclamation\n\n";
}

} // namespace multiprocessor::queues

int main() {
    using namespace multiprocessor::queues;

    std::cout << "=== Concurrent Queues Test (C++) ===\n\n";

    test_bounded_queue();
    test_lock_free_queue();
    demonstrate_aba_problem();

    return 0;
}
