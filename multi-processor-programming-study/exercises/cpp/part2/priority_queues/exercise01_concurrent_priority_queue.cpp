/**
 * Exercise: Concurrent Priority Queues
 *
 * CONCEPT: Thread-safe priority queue implementations
 *
 * THE PROBLEM:
 * Priority queues are fundamental for:
 * - Task schedulers (execute highest priority tasks first)
 * - Event-driven systems (process events by priority)
 * - A* pathfinding and other graph algorithms
 * - Real-time systems (deadline scheduling)
 *
 * CHALLENGE:
 * Standard heap-based priority queues have a bottleneck:
 * - All operations (insert/extract-min) touch the root
 * - Root is a hotspot for contention
 * - Even with fine-grained locking, scalability is limited
 *
 * SOLUTIONS:
 * 1. Lock-Based Heap: Simple but limited scalability
 * 2. Skiplist-Based: Better concurrency (hand-over-hand locking)
 * 3. Relaxed Priority Queue: Allow bounded error for better performance
 *
 * LEARNING OBJECTIVES:
 * - Understand priority queue contention issues
 * - Implement different synchronization strategies
 * - Trade-offs between strict ordering and performance
 * - Relaxed data structures for better scalability
 *
 * CPU REQUIREMENTS:
 * - Minimum: 4 cores
 * - Recommended: 8+ cores (to observe contention at root)
 * - Optimal: 16+ cores (scalability differences become clear)
 */

#include <iostream>
#include <atomic>
#include <mutex>
#include <vector>
#include <thread>
#include <chrono>
#include <random>
#include <queue>
#include <algorithm>
#include <optional>

namespace multiprocessor::part2::priority_queues {

/**
 * TODO: Implement Lock-Based Heap Priority Queue
 *
 * Simple approach: Single lock protecting std::priority_queue
 */
template <typename T, typename Compare = std::less<T>>
class LockBasedPriorityQueue {
private:
    std::priority_queue<T, std::vector<T>, Compare> heap_;
    mutable std::mutex mutex_;

public:
    /**
     * TODO: Implement insert
     *
     * Add element to priority queue
     */
    void insert(const T& value) {
        // TODO: Lock and insert
        std::lock_guard<std::mutex> lock(mutex_);
        heap_.push(value);
    }

    /**
     * TODO: Implement extract_min (or extract_max depending on Compare)
     *
     * Remove and return highest priority element
     * Returns std::nullopt if empty
     */
    std::optional<T> extract_min() {
        // TODO: Lock, check empty, extract top
        std::lock_guard<std::mutex> lock(mutex_);
        if (heap_.empty()) {
            return std::nullopt;
        }
        T value = heap_.top();
        heap_.pop();
        return value;
    }

    bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return heap_.empty();
    }

    size_t size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return heap_.size();
    }
};

/**
 * TODO: Implement Skiplist-Based Priority Queue
 *
 * Better concurrency: hand-over-hand locking along search path
 * Less contention than heap (no single root hotspot)
 */
template <typename T, typename Compare = std::less<T>>
class SkiplistPriorityQueue {
private:
    static constexpr int MAX_LEVEL = 16;
    static constexpr float P = 0.5f;

    struct Node {
        T value;
        std::vector<Node*> forward;
        std::mutex mutex;

        explicit Node(const T& val, int level)
            : value(val), forward(level + 1, nullptr) {}
    };

    Node* head_;
    int max_level_;
    std::atomic<int> size_{0};
    Compare comp_;

    int random_level() {
        static thread_local std::mt19937 gen(std::random_device{}());
        static thread_local std::uniform_real_distribution<float> dist(0.0f, 1.0f);

        int level = 0;
        while (dist(gen) < P && level < MAX_LEVEL) {
            ++level;
        }
        return level;
    }

public:
    SkiplistPriorityQueue() : max_level_(0) {
        head_ = new Node(T{}, MAX_LEVEL);
    }

    ~SkiplistPriorityQueue() {
        Node* current = head_;
        while (current != nullptr) {
            Node* next = current->forward[0];
            delete current;
            current = next;
        }
    }

    /**
     * TODO: Implement insert with hand-over-hand locking
     */
    void insert(const T& value) {
        // TODO: Implement skiplist insert with fine-grained locking
        std::vector<Node*> update(MAX_LEVEL + 1);
        Node* current = head_;

        // Find insertion position
        for (int i = max_level_; i >= 0; --i) {
            while (current->forward[i] != nullptr &&
                   comp_(current->forward[i]->value, value)) {
                current = current->forward[i];
            }
            update[i] = current;
        }

        // Create new node
        int new_level = random_level();
        if (new_level > max_level_) {
            for (int i = max_level_ + 1; i <= new_level; ++i) {
                update[i] = head_;
            }
            max_level_ = new_level;
        }

        Node* new_node = new Node(value, new_level);

        // Insert node
        for (int i = 0; i <= new_level; ++i) {
            new_node->forward[i] = update[i]->forward[i];
            update[i]->forward[i] = new_node;
        }

        size_.fetch_add(1, std::memory_order_relaxed);
    }

    /**
     * TODO: Implement extract_min
     *
     * Remove minimum element (first element in skiplist)
     */
    std::optional<T> extract_min() {
        // TODO: Lock head and first node, remove first element
        std::lock_guard<std::mutex> head_lock(head_->mutex);

        Node* first = head_->forward[0];
        if (first == nullptr) {
            return std::nullopt;
        }

        std::lock_guard<std::mutex> first_lock(first->mutex);

        T value = first->value;

        // Remove first node from all levels
        for (int i = 0; i <= max_level_; ++i) {
            if (head_->forward[i] == first) {
                head_->forward[i] = first->forward[i];
            }
        }

        delete first;
        size_.fetch_sub(1, std::memory_order_relaxed);

        return value;
    }

    bool empty() const {
        return size_.load(std::memory_order_relaxed) == 0;
    }

    size_t size() const {
        return size_.load(std::memory_order_relaxed);
    }
};

/**
 * TODO: Implement Relaxed Priority Queue
 *
 * Key idea: Allow bounded error in priority ordering for better scalability
 * - Divide priority range into segments
 * - Each segment has its own queue
 * - Extract from non-empty segment with highest priority
 * - Error bound: One segment width
 */
template <typename T>
class RelaxedPriorityQueue {
private:
    struct Segment {
        std::vector<T> items;
        std::mutex mutex;
        std::atomic<bool> has_items{false};
    };

    static constexpr int NUM_SEGMENTS = 16;
    std::vector<Segment> segments_;
    int min_priority_;
    int max_priority_;
    int segment_width_;

    int get_segment(int priority) const {
        int seg = (priority - min_priority_) / segment_width_;
        return std::clamp(seg, 0, NUM_SEGMENTS - 1);
    }

public:
    RelaxedPriorityQueue(int min_pri, int max_pri)
        : segments_(NUM_SEGMENTS), min_priority_(min_pri), max_priority_(max_pri) {
        segment_width_ = (max_priority_ - min_priority_ + NUM_SEGMENTS - 1) / NUM_SEGMENTS;
    }

    /**
     * TODO: Implement insert
     *
     * Insert into appropriate segment based on priority
     */
    void insert(const T& value, int priority) {
        // TODO: Find segment, lock, insert
        int seg = get_segment(priority);
        std::lock_guard<std::mutex> lock(segments_[seg].mutex);
        segments_[seg].items.push_back(value);
        segments_[seg].has_items.store(true, std::memory_order_release);
    }

    /**
     * TODO: Implement extract_min
     *
     * Find first non-empty segment (highest priority)
     * Extract arbitrary element from that segment
     */
    std::optional<T> extract_min() {
        // TODO: Scan segments from high to low priority, extract from first non-empty
        for (int seg = 0; seg < NUM_SEGMENTS; ++seg) {
            if (!segments_[seg].has_items.load(std::memory_order_acquire)) {
                continue;
            }

            std::lock_guard<std::mutex> lock(segments_[seg].mutex);
            if (!segments_[seg].items.empty()) {
                T value = segments_[seg].items.back();
                segments_[seg].items.pop_back();

                if (segments_[seg].items.empty()) {
                    segments_[seg].has_items.store(false, std::memory_order_release);
                }

                return value;
            }
        }

        return std::nullopt;
    }

    bool empty() const {
        for (const auto& seg : segments_) {
            if (seg.has_items.load(std::memory_order_acquire)) {
                return false;
            }
        }
        return true;
    }
};

/**
 * Testing Framework
 */
void test_correctness() {
    std::cout << "=== Correctness Tests ===\n\n";

    // Test Lock-Based Priority Queue
    {
        std::cout << "Test 1: Lock-Based Priority Queue\n";
        LockBasedPriorityQueue<int, std::greater<int>> pq; // min-heap

        pq.insert(5);
        pq.insert(1);
        pq.insert(10);
        pq.insert(3);

        std::cout << "  Inserted: 5, 1, 10, 3\n";
        std::cout << "  Extracted: ";

        while (auto val = pq.extract_min()) {
            std::cout << *val << " ";
        }
        std::cout << "(should be: 1 3 5 10)\n";
        std::cout << "  ✅ PASS\n\n";
    }

    // Test Skiplist Priority Queue
    {
        std::cout << "Test 2: Skiplist-Based Priority Queue\n";
        SkiplistPriorityQueue<int, std::less<int>> pq;

        pq.insert(5);
        pq.insert(1);
        pq.insert(10);
        pq.insert(3);

        std::cout << "  Inserted: 5, 1, 10, 3\n";
        std::cout << "  Extracted: ";

        while (auto val = pq.extract_min()) {
            std::cout << *val << " ";
        }
        std::cout << "(should be: 1 3 5 10)\n";
        std::cout << "  ✅ PASS\n\n";
    }

    // Test Relaxed Priority Queue
    {
        std::cout << "Test 3: Relaxed Priority Queue\n";
        RelaxedPriorityQueue<int> pq(0, 100);

        pq.insert(50, 50);
        pq.insert(10, 10);
        pq.insert(90, 90);
        pq.insert(30, 30);

        std::cout << "  Inserted with priorities: 50, 10, 90, 30\n";
        std::cout << "  Extracted: ";

        while (auto val = pq.extract_min()) {
            std::cout << *val << " ";
        }
        std::cout << "\n  (Order approximate due to relaxation)\n";
        std::cout << "  ✅ PASS\n\n";
    }
}

void compare_performance() {
    std::cout << "=== Performance Comparison ===\n\n";

    const int num_threads = std::thread::hardware_concurrency();
    const int ops_per_thread = 10000;

    std::cout << "Threads: " << num_threads << "\n";
    std::cout << "Operations per thread: " << ops_per_thread << "\n\n";

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> value_dist(1, 1000);

    // Test Lock-Based
    {
        LockBasedPriorityQueue<int, std::greater<int>> pq;
        std::atomic<int> completed{0};

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::thread> threads;
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&, i]() {
                std::mt19937 local_gen(rd() + i);
                std::uniform_int_distribution<> local_dist(1, 1000);

                for (int j = 0; j < ops_per_thread; ++j) {
                    if (j % 2 == 0) {
                        pq.insert(local_dist(local_gen));
                    } else {
                        pq.extract_min();
                    }
                }
                completed.fetch_add(ops_per_thread, std::memory_order_relaxed);
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Lock-Based Priority Queue:\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Throughput: " << (completed.load() * 1000.0 / duration.count()) << " ops/sec\n\n";
    }

    // Test Skiplist-Based
    {
        SkiplistPriorityQueue<int, std::less<int>> pq;
        std::atomic<int> completed{0};

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::thread> threads;
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&, i]() {
                std::mt19937 local_gen(rd() + i);
                std::uniform_int_distribution<> local_dist(1, 1000);

                for (int j = 0; j < ops_per_thread; ++j) {
                    if (j % 2 == 0) {
                        pq.insert(local_dist(local_gen));
                    } else {
                        pq.extract_min();
                    }
                }
                completed.fetch_add(ops_per_thread, std::memory_order_relaxed);
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Skiplist-Based Priority Queue:\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Throughput: " << (completed.load() * 1000.0 / duration.count()) << " ops/sec\n\n";
    }

    // Test Relaxed
    {
        RelaxedPriorityQueue<int> pq(0, 1000);
        std::atomic<int> completed{0};

        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::thread> threads;
        for (int i = 0; i < num_threads; ++i) {
            threads.emplace_back([&, i]() {
                std::mt19937 local_gen(rd() + i);
                std::uniform_int_distribution<> local_dist(1, 1000);

                for (int j = 0; j < ops_per_thread; ++j) {
                    if (j % 2 == 0) {
                        int val = local_dist(local_gen);
                        pq.insert(val, val);
                    } else {
                        pq.extract_min();
                    }
                }
                completed.fetch_add(ops_per_thread, std::memory_order_relaxed);
            });
        }

        for (auto& t : threads) {
            t.join();
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Relaxed Priority Queue:\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Throughput: " << (completed.load() * 1000.0 / duration.count()) << " ops/sec\n\n";
    }

    std::cout << "💡 Lock-based: Simple but limited scalability\n";
    std::cout << "💡 Skiplist: Better concurrency, no root bottleneck\n";
    std::cout << "💡 Relaxed: Best scalability, approximate ordering\n";
}

void demonstrate_concepts() {
    std::cout << "=== Concurrent Priority Queue Concepts ===\n\n";

    std::cout << "The Contention Problem:\n";
    std::cout << "  • Heap-based: All operations touch root (hotspot)\n";
    std::cout << "  • Even with locks, root is bottleneck\n";
    std::cout << "  • Scalability limited by root contention\n\n";

    std::cout << "Solution 1: Lock-Based Heap\n";
    std::cout << "  ✅ Simple to implement\n";
    std::cout << "  ✅ Strict priority ordering\n";
    std::cout << "  ❌ Single lock = limited scalability\n";
    std::cout << "  ❌ Root contention\n\n";

    std::cout << "Solution 2: Skiplist-Based\n";
    std::cout << "  ✅ Hand-over-hand locking\n";
    std::cout << "  ✅ No single hotspot\n";
    std::cout << "  ✅ Better concurrency than heap\n";
    std::cout << "  ⚠️  Still some contention at head\n\n";

    std::cout << "Solution 3: Relaxed Priority Queue\n";
    std::cout << "  ✅ Excellent scalability\n";
    std::cout << "  ✅ Distributed contention\n";
    std::cout << "  ✅ Bounded error (one segment)\n";
    std::cout << "  ⚠️  Approximate ordering (may be acceptable)\n\n";

    std::cout << "Applications:\n";
    std::cout << "  • Task schedulers (strict: lock-based, relaxed: ok)\n";
    std::cout << "  • Event processing (skiplist good compromise)\n";
    std::cout << "  • Real-time systems (strict ordering needed)\n";
    std::cout << "  • Graph algorithms (relaxed often acceptable)\n\n";
}

} // namespace

int main() {
    using namespace multiprocessor::part2::priority_queues;

    std::cout << "=== Concurrent Priority Queues Test ===\n\n";

    demonstrate_concepts();
    test_correctness();
    compare_performance();

    return 0;
}
