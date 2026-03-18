/**
 * Exercise: Work-Stealing Deque (Chase-Lev Algorithm)
 *
 * CONCEPT: Double-ended queue for efficient task parallelism
 *
 * THE PROBLEM:
 * In task-parallel systems (Fork/Join, parallel-for, etc.), we need:
 * - Worker threads that process tasks from their own queue (owner)
 * - Other threads can "steal" tasks when idle (thieves)
 * - Owner pushes/pops from one end (LIFO for cache locality)
 * - Thieves steal from the other end (FIFO for load balancing)
 *
 * CHASE-LEV ALGORITHM:
 * - Lock-free work-stealing deque
 * - Owner operations (push/pop) are almost wait-free
 * - Thief operations (steal) use CAS and may fail
 * - Uses circular array with dynamic resizing
 * - Handles ABA problem with versioning
 *
 * APPLICATIONS:
 * - Java ForkJoinPool
 * - .NET Task Parallel Library
 * - Intel TBB (Threading Building Blocks)
 * - Rust Rayon
 *
 * LEARNING OBJECTIVES:
 * - Understand work-stealing scheduling
 * - Implement Chase-Lev deque algorithm
 * - Handle dynamic array resizing in lock-free context
 * - Appreciate asymmetric access patterns (owner vs thieves)
 *
 * CPU REQUIREMENTS:
 * - Minimum: 4 cores (to show work stealing benefits)
 * - Recommended: 8-16 cores (uneven workload distribution)
 * - Optimal: 16+ cores (dramatic load balancing benefits)
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <memory>
#include <chrono>
#include <random>
#include <algorithm>
#include <cmath>

namespace multiprocessor::part2::work_stealing {

/**
 * TODO: Implement Chase-Lev Work-Stealing Deque
 *
 * This is a lock-free deque optimized for task parallelism where:
 * - One thread (owner) pushes and pops from the bottom (tail)
 * - Multiple threads (thieves) steal from the top (head)
 */
template <typename T>
class WorkStealingDeque {
private:
    /**
     * Circular array for storing tasks
     *
     * Uses power-of-2 size for efficient modulo with bitwise AND
     */
    struct CircularArray {
        std::unique_ptr<std::atomic<T>[]> buffer;
        size_t capacity;

        explicit CircularArray(size_t size) : capacity(size) {
            buffer = std::make_unique<std::atomic<T>[]>(capacity);
        }

        T get(size_t index) const {
            return buffer[index & (capacity - 1)].load(std::memory_order_relaxed);
        }

        void put(size_t index, T value) {
            buffer[index & (capacity - 1)].store(value, std::memory_order_relaxed);
        }

        // Create a larger array and copy elements
        std::unique_ptr<CircularArray> grow(size_t bottom, size_t top) {
            auto new_array = std::make_unique<CircularArray>(capacity * 2);
            for (size_t i = top; i < bottom; ++i) {
                new_array->put(i, get(i));
            }
            return new_array;
        }
    };

    std::atomic<size_t> top_{0};    // Head (thieves steal from here)
    std::atomic<size_t> bottom_{0}; // Tail (owner pushes/pops here)
    std::atomic<CircularArray*> array_;

    static constexpr size_t INITIAL_CAPACITY = 256;

public:
    WorkStealingDeque() {
        CircularArray* initial_array = new CircularArray(INITIAL_CAPACITY);
        array_.store(initial_array, std::memory_order_relaxed);
    }

    ~WorkStealingDeque() {
        delete array_.load(std::memory_order_relaxed);
    }

    /**
     * TODO: Implement push (owner only)
     *
     * Owner pushes task to the bottom (tail) of the deque
     * This is the common case and should be very fast
     */
    void push(T value) {
        // TODO: Implement push operation
        // 1. Load bottom (relaxed - owner is the only writer)
        // 2. Load top (acquire - synchronize with thieves)
        // 3. Load current array
        // 4. If array is full, grow it
        // 5. Put value at bottom position
        // 6. Increment bottom (release - make value visible to thieves)

        size_t b = bottom_.load(std::memory_order_relaxed);
        size_t t = top_.load(std::memory_order_acquire);
        CircularArray* a = array_.load(std::memory_order_relaxed);

        // Check if array is full
        if (b - t >= a->capacity) {
            // Grow array
            CircularArray* new_array = a->grow(b, t).release();
            array_.store(new_array, std::memory_order_release);
            delete a;
            a = new_array;
        }

        // Put value at bottom
        a->put(b, value);

        // Make value visible to thieves (release barrier)
        std::atomic_thread_fence(std::memory_order_release);
        bottom_.store(b + 1, std::memory_order_relaxed);
    }

    /**
     * TODO: Implement pop (owner only)
     *
     * Owner pops task from the bottom (tail) of the deque
     * Returns default T value if empty
     */
    T pop() {
        // TODO: Implement pop operation
        // 1. Decrement bottom (owner claims the task)
        // 2. Load array
        // 3. Load top
        // 4. If deque was empty, restore bottom and return null
        // 5. If deque has one element, use CAS to compete with thieves
        // 6. Otherwise, just take the element (no competition)

        size_t b = bottom_.load(std::memory_order_relaxed) - 1;
        CircularArray* a = array_.load(std::memory_order_relaxed);
        bottom_.store(b, std::memory_order_relaxed);

        // Ensure bottom write happens before top read
        std::atomic_thread_fence(std::memory_order_seq_cst);

        size_t t = top_.load(std::memory_order_relaxed);

        T result{};
        if (t <= b) {
            // Non-empty queue
            result = a->get(b);

            if (t == b) {
                // Last element - compete with thieves using CAS
                if (!top_.compare_exchange_strong(t, t + 1,
                                                  std::memory_order_seq_cst,
                                                  std::memory_order_relaxed)) {
                    // Lost race to thief
                    result = T{};
                }
                bottom_.store(b + 1, std::memory_order_relaxed);
            }
        } else {
            // Empty queue - restore bottom
            bottom_.store(b + 1, std::memory_order_relaxed);
        }

        return result;
    }

    /**
     * TODO: Implement steal (thieves)
     *
     * Thief steals task from the top (head) of the deque
     * Returns default T value if empty or if lost race to another thief
     */
    T steal() {
        // TODO: Implement steal operation
        // 1. Load top (acquire - synchronize with owner's push)
        // 2. Ensure top is loaded before bottom
        // 3. Load bottom (acquire - synchronize with owner's pop)
        // 4. If empty (top >= bottom), return null
        // 5. Load array
        // 6. Read value at top
        // 7. Try to CAS top to top+1
        // 8. If CAS succeeds, return value; otherwise return null

        size_t t = top_.load(std::memory_order_acquire);

        // Ensure top is loaded before bottom
        std::atomic_thread_fence(std::memory_order_seq_cst);

        size_t b = bottom_.load(std::memory_order_acquire);

        if (t >= b) {
            // Empty queue
            return T{};
        }

        // Non-empty queue
        CircularArray* a = array_.load(std::memory_order_consume);
        T value = a->get(t);

        // Try to steal with CAS
        if (!top_.compare_exchange_strong(t, t + 1,
                                         std::memory_order_seq_cst,
                                         std::memory_order_relaxed)) {
            // Lost race to another thief
            return T{};
        }

        return value;
    }

    /**
     * Get approximate size (not linearizable, for testing only)
     */
    size_t size() const {
        size_t b = bottom_.load(std::memory_order_relaxed);
        size_t t = top_.load(std::memory_order_relaxed);
        return (b >= t) ? (b - t) : 0;
    }
};

/**
 * Task type for testing
 */
struct Task {
    int id;
    int workload; // Simulated work amount

    Task() : id(0), workload(0) {}
    Task(int i, int w) : id(i), workload(w) {}

    void execute() const {
        // Simulate work
        volatile int sum = 0;
        for (int i = 0; i < workload; ++i) {
            sum += i;
        }
    }
};

/**
 * Testing: Correctness Test
 */
void test_correctness() {
    std::cout << "=== Correctness Test ===\n\n";

    WorkStealingDeque<Task> deque;

    std::cout << "Test 1: Single-threaded push/pop\n";
    deque.push(Task(1, 100));
    deque.push(Task(2, 200));
    deque.push(Task(3, 300));

    Task t1 = deque.pop();
    Task t2 = deque.pop();
    Task t3 = deque.pop();
    Task t4 = deque.pop();

    std::cout << "  Popped: " << t1.id << ", " << t2.id << ", " << t3.id << "\n";
    std::cout << "  Empty pop: " << t4.id << " (should be 0)\n";
    std::cout << (t1.id == 3 && t2.id == 2 && t3.id == 1 && t4.id == 0 ? "  ✅ PASS\n\n" : "  ❌ FAIL\n\n");

    std::cout << "Test 2: Multi-threaded work stealing\n";
    WorkStealingDeque<Task> shared_deque;

    // Owner pushes tasks
    for (int i = 0; i < 1000; ++i) {
        shared_deque.push(Task(i, 100));
    }

    std::atomic<int> tasks_executed{0};
    std::atomic<int> tasks_stolen{0};

    // Owner thread (pops from bottom)
    std::thread owner([&]() {
        int local_count = 0;
        Task task;
        while ((task = shared_deque.pop()).id != 0 || shared_deque.size() > 0) {
            if (task.id != 0) {
                task.execute();
                local_count++;
            }
        }
        tasks_executed.fetch_add(local_count, std::memory_order_relaxed);
    });

    // Thief threads (steal from top)
    std::vector<std::thread> thieves;
    for (int i = 0; i < 4; ++i) {
        thieves.emplace_back([&]() {
            int stolen_count = 0;
            Task task;
            while ((task = shared_deque.steal()).id != 0 || shared_deque.size() > 0) {
                if (task.id != 0) {
                    task.execute();
                    stolen_count++;
                }
                std::this_thread::yield();
            }
            tasks_stolen.fetch_add(stolen_count, std::memory_order_relaxed);
        });
    }

    owner.join();
    for (auto& thief : thieves) {
        thief.join();
    }

    std::cout << "  Tasks executed by owner: " << (tasks_executed.load() - tasks_stolen.load()) << "\n";
    std::cout << "  Tasks stolen by thieves: " << tasks_stolen.load() << "\n";
    std::cout << "  Total tasks executed: " << tasks_executed.load() << "\n";
    std::cout << (tasks_executed.load() == 1000 ? "  ✅ PASS\n\n" : "  ❌ FAIL\n\n");
}

/**
 * Testing: Performance Comparison
 */
void compare_performance() {
    std::cout << "=== Performance Test: Parallel Task Execution ===\n\n";

    const int num_tasks = 100000;
    const int num_workers = std::thread::hardware_concurrency();

    std::cout << "Number of workers: " << num_workers << "\n";
    std::cout << "Number of tasks: " << num_tasks << "\n\n";

    // Create tasks with varying workloads (simulate uneven distribution)
    std::vector<Task> tasks;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> work_dist(100, 1000);

    for (int i = 0; i < num_tasks; ++i) {
        tasks.emplace_back(i + 1, work_dist(gen));
    }

    // Test 1: Work Stealing Deque
    {
        std::vector<WorkStealingDeque<Task>> worker_deques(num_workers);

        // Distribute tasks unevenly (simulate fork/join pattern)
        for (size_t i = 0; i < tasks.size(); ++i) {
            worker_deques[i % num_workers].push(tasks[i]);
        }

        std::atomic<int> completed{0};
        auto start = std::chrono::high_resolution_clock::now();

        std::vector<std::thread> workers;
        for (int i = 0; i < num_workers; ++i) {
            workers.emplace_back([&, i]() {
                int local_count = 0;

                while (completed.load(std::memory_order_relaxed) < num_tasks) {
                    // Try own deque first
                    Task task = worker_deques[i].pop();

                    if (task.id == 0) {
                        // Own deque empty, try stealing from others
                        bool stole = false;
                        for (int j = 1; j < num_workers && !stole; ++j) {
                            int victim = (i + j) % num_workers;
                            task = worker_deques[victim].steal();
                            if (task.id != 0) {
                                stole = true;
                            }
                        }

                        if (!stole) {
                            // No work available, yield
                            std::this_thread::yield();
                            continue;
                        }
                    }

                    task.execute();
                    local_count++;
                }

                completed.fetch_add(local_count, std::memory_order_relaxed);
            });
        }

        for (auto& worker : workers) {
            worker.join();
        }

        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Work-Stealing Deque:\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Tasks completed: " << completed.load() << "\n";
        std::cout << "  Throughput: " << (num_tasks * 1000.0 / duration.count()) << " tasks/sec\n\n";
    }

    std::cout << "💡 Work-stealing provides automatic load balancing\n";
    std::cout << "💡 Owner operations (push/pop) are very fast (no CAS)\n";
    std::cout << "💡 Thieves use CAS only when stealing\n";
    std::cout << "💡 Used in Java ForkJoinPool, .NET TPL, Rust Rayon\n";
}

/**
 * Demonstrate work-stealing concepts
 */
void demonstrate_concepts() {
    std::cout << "=== Work-Stealing Deque Concepts ===\n\n";

    std::cout << "Chase-Lev Algorithm:\n";
    std::cout << "  • Asymmetric access pattern (owner vs thieves)\n";
    std::cout << "  • Owner: Fast push/pop from bottom (tail) - LIFO\n";
    std::cout << "  • Thieves: Steal from top (head) - FIFO\n";
    std::cout << "  • Lock-free with minimal CAS operations\n\n";

    std::cout << "Why LIFO for owner, FIFO for thieves?\n";
    std::cout << "  • LIFO (owner): Cache locality - recent tasks likely related\n";
    std::cout << "  • FIFO (thieves): Load balancing - steal oldest tasks\n";
    std::cout << "  • Reduces contention between owner and thieves\n\n";

    std::cout << "Memory Ordering:\n";
    std::cout << "  • Push: Release barrier on bottom increment\n";
    std::cout << "  • Pop: Sequential consistency for owner/thief race\n";
    std::cout << "  • Steal: Acquire on top, seq_cst for CAS\n\n";

    std::cout << "Dynamic Resizing:\n";
    std::cout << "  • Circular array grows when full\n";
    std::cout << "  • Power-of-2 size for efficient modulo (bitwise AND)\n";
    std::cout << "  • Owner handles resizing (no thief involvement)\n\n";

    std::cout << "Applications:\n";
    std::cout << "  ✅ Fork/Join parallelism\n";
    std::cout << "  ✅ Parallel for loops\n";
    std::cout << "  ✅ Recursive task decomposition\n";
    std::cout << "  ✅ Dynamic load balancing\n\n";
}

} // namespace multiprocessor::part2::work_stealing

int main() {
    using namespace multiprocessor::part2::work_stealing;

    std::cout << "=== Work-Stealing Deque (Chase-Lev) Test ===\n\n";

    demonstrate_concepts();
    test_correctness();
    compare_performance();

    return 0;
}
