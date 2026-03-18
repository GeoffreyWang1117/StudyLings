/**
 * Exercise 01: Thread Pool Implementation (C++)
 *
 * This exercise implements various thread pool patterns, which are the most
 * commonly used concurrency patterns in production systems.
 *
 * Learning Objectives:
 * 1. Understand thread pool architecture and components
 * 2. Implement fixed-size thread pool with task queue
 * 3. Implement work-stealing thread pool
 * 4. Learn graceful shutdown protocols
 * 5. Compare with C++ thread management
 *
 * Real-World Applications:
 * - Web servers (request handling)
 * - Database systems (query execution)
 * - Background task processing
 * - Async I/O operations
 *
 * Hardware Requirements:
 * - Minimum: 4 cores
 * - Recommended: 8+ cores for observing load balancing
 *
 * Compilation:
 *   g++ -std=c++20 -pthread exercise01_thread_pool.cpp -o thread_pool
 */

#include <iostream>
#include <thread>
#include <vector>
#include <queue>
#include <deque>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <atomic>
#include <random>
#include <chrono>
#include <memory>

/**
 * Task 1: Fixed Thread Pool
 *
 * Implements a simple fixed-size thread pool with a shared task queue.
 * All worker threads compete for tasks from a single queue.
 */
class FixedThreadPool {
public:
    using Task = std::function<void()>;

    explicit FixedThreadPool(size_t pool_size)
        : shutdown_(false) {

        // TODO: Create and start worker threads
        // Hint: Each worker should continuously take tasks from the queue
        workers_.reserve(pool_size);
        for (size_t i = 0; i < pool_size; ++i) {
            workers_.emplace_back([this, i]() {
                this->worker_thread(i);
            });
        }
    }

    ~FixedThreadPool() {
        shutdown();
    }

    /**
     * Submit a task for execution
     */
    void submit(Task task) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            if (shutdown_) {
                throw std::runtime_error("Thread pool is shut down");
            }

            // TODO: Add task to queue
            // Hint: Push to task_queue_ and notify a worker
            task_queue_.push(std::move(task));
        }
        condition_.notify_one();
    }

    /**
     * Graceful shutdown: stop accepting new tasks, wait for existing tasks to complete
     */
    void shutdown() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            if (shutdown_) {
                return;
            }
            shutdown_ = true;
        }

        // TODO: Notify all workers and join them
        condition_.notify_all();

        for (auto& worker : workers_) {
            if (worker.joinable()) {
                worker.join();
            }
        }
    }

    size_t get_queue_size() const {
        std::unique_lock<std::mutex> lock(queue_mutex_);
        return task_queue_.size();
    }

    size_t get_pool_size() const {
        return workers_.size();
    }

private:
    /**
     * Worker thread function
     */
    void worker_thread(size_t worker_id) {
        // TODO: Implement worker thread logic
        // 1. Wait for tasks
        // 2. Execute tasks
        // 3. Handle shutdown signal

        while (true) {
            Task task;

            {
                std::unique_lock<std::mutex> lock(queue_mutex_);

                // Wait for task or shutdown
                condition_.wait(lock, [this]() {
                    return shutdown_ || !task_queue_.empty();
                });

                // Check if should exit
                if (shutdown_ && task_queue_.empty()) {
                    break;
                }

                if (!task_queue_.empty()) {
                    task = std::move(task_queue_.front());
                    task_queue_.pop();
                }
            }

            // Execute task outside the lock
            if (task) {
                try {
                    task();
                } catch (const std::exception& e) {
                    std::cerr << "Task execution failed in worker " << worker_id
                              << ": " << e.what() << std::endl;
                }
            }
        }
    }

    std::vector<std::thread> workers_;
    std::queue<Task> task_queue_;
    mutable std::mutex queue_mutex_;
    std::condition_variable condition_;
    std::atomic<bool> shutdown_;
};

/**
 * Task 2: Work-Stealing Thread Pool
 *
 * Advanced thread pool using work-stealing for better load balancing.
 * Each worker has its own deque and can steal tasks from others when idle.
 */
class WorkStealingThreadPool {
public:
    using Task = std::function<void()>;

    explicit WorkStealingThreadPool(size_t pool_size)
        : shutdown_(false), pool_size_(pool_size) {

        // TODO: Create work-stealing workers
        workers_.reserve(pool_size);
        for (size_t i = 0; i < pool_size; ++i) {
            workers_.emplace_back(std::make_unique<WorkStealingWorker>(i, this));
        }

        for (auto& worker : workers_) {
            worker->start();
        }
    }

    ~WorkStealingThreadPool() {
        shutdown();
    }

    /**
     * Submit task to a random worker's deque
     */
    void submit(Task task) {
        if (shutdown_) {
            throw std::runtime_error("Thread pool is shut down");
        }

        // TODO: Submit to random worker
        static thread_local std::mt19937 rng(std::random_device{}());
        std::uniform_int_distribution<size_t> dist(0, pool_size_ - 1);
        size_t worker_index = dist(rng);

        workers_[worker_index]->push_task(std::move(task));
    }

    void shutdown() {
        if (shutdown_.exchange(true)) {
            return;
        }

        for (auto& worker : workers_) {
            worker->shutdown();
        }

        for (auto& worker : workers_) {
            worker->join();
        }
    }

    size_t get_pool_size() const {
        return pool_size_;
    }

private:
    /**
     * Work-stealing worker with its own deque
     */
    class WorkStealingWorker {
    public:
        WorkStealingWorker(size_t worker_id, WorkStealingThreadPool* pool)
            : worker_id_(worker_id),
              pool_(pool),
              shutdown_(false),
              tasks_executed_(0),
              tasks_stolen_(0) {}

        ~WorkStealingWorker() {
            shutdown();
            join();
        }

        void start() {
            thread_ = std::thread([this]() {
                this->run();
            });
        }

        void push_task(Task task) {
            std::unique_lock<std::mutex> lock(deque_mutex_);
            // TODO: Push task to own deque (LIFO end)
            task_deque_.push_front(std::move(task));
        }

        void shutdown() {
            shutdown_ = true;
        }

        void join() {
            if (thread_.joinable()) {
                thread_.join();
            }
        }

        size_t get_tasks_executed() const {
            return tasks_executed_.load();
        }

        size_t get_tasks_stolen() const {
            return tasks_stolen_.load();
        }

    private:
        void run() {
            // TODO: Implement work-stealing logic
            // 1. Try to pop from own deque (LIFO)
            // 2. If empty, try to steal from random worker (FIFO)
            // 3. Execute task
            // 4. Repeat until shutdown

            while (!shutdown_ || has_tasks()) {
                Task task = pop_task();

                if (!task) {
                    task = steal_task();
                }

                if (task) {
                    try {
                        task();
                        tasks_executed_++;
                    } catch (const std::exception& e) {
                        std::cerr << "Task execution failed in worker " << worker_id_
                                  << ": " << e.what() << std::endl;
                    }
                } else {
                    // No work available, sleep briefly
                    std::this_thread::sleep_for(std::chrono::microseconds(100));
                }
            }
        }

        /**
         * Pop task from own deque (LIFO for cache locality)
         */
        Task pop_task() {
            std::unique_lock<std::mutex> lock(deque_mutex_);
            if (task_deque_.empty()) {
                return nullptr;
            }

            // TODO: Pop from own deque (LIFO)
            Task task = std::move(task_deque_.front());
            task_deque_.pop_front();
            return task;
        }

        /**
         * Steal task from a random victim's deque (FIFO for load distribution)
         */
        Task steal_task() {
            // TODO: Implement work stealing
            // 1. Pick random victim (not self)
            // 2. Steal from victim's deque (FIFO end)
            // 3. Return stolen task or nullptr

            if (pool_->pool_size_ <= 1) {
                return nullptr;
            }

            static thread_local std::mt19937 rng(std::random_device{}());
            std::uniform_int_distribution<size_t> dist(0, pool_->pool_size_ - 1);

            // Try stealing from random victims
            size_t attempts = pool_->pool_size_ * 2;
            for (size_t i = 0; i < attempts; ++i) {
                size_t victim_index = dist(rng);
                if (victim_index == worker_id_) {
                    continue;
                }

                auto& victim = pool_->workers_[victim_index];
                Task stolen = victim->steal_from_back();
                if (stolen) {
                    tasks_stolen_++;
                    return stolen;
                }
            }

            return nullptr;
        }

        /**
         * Allow other workers to steal from back of deque
         */
        Task steal_from_back() {
            std::unique_lock<std::mutex> lock(deque_mutex_);
            if (task_deque_.empty()) {
                return nullptr;
            }

            // Steal from back (FIFO)
            Task task = std::move(task_deque_.back());
            task_deque_.pop_back();
            return task;
        }

        bool has_tasks() const {
            std::unique_lock<std::mutex> lock(deque_mutex_);
            return !task_deque_.empty();
        }

        size_t worker_id_;
        WorkStealingThreadPool* pool_;
        std::thread thread_;
        std::deque<Task> task_deque_;
        mutable std::mutex deque_mutex_;
        std::atomic<bool> shutdown_;
        std::atomic<size_t> tasks_executed_;
        std::atomic<size_t> tasks_stolen_;
    };

    std::vector<std::unique_ptr<WorkStealingWorker>> workers_;
    std::atomic<bool> shutdown_;
    size_t pool_size_;
};

/**
 * Helper function to measure execution time
 */
template<typename Func>
double measure_time(Func&& func) {
    auto start = std::chrono::high_resolution_clock::now();
    func();
    auto end = std::chrono::high_resolution_clock::now();
    return std::chrono::duration<double, std::milli>(end - start).count();
}

/**
 * Test fixed thread pool
 */
void test_fixed_thread_pool() {
    std::cout << "=== Testing Fixed Thread Pool ===" << std::endl;

    FixedThreadPool pool(4);
    std::atomic<int> counter{0};
    const int task_count = 20;

    for (int i = 0; i < task_count; ++i) {
        pool.submit([&counter, i]() {
            std::cout << "Task " << i << " executing on thread "
                      << std::this_thread::get_id() << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            counter++;
        });
    }

    // Wait a bit for tasks to complete
    std::this_thread::sleep_for(std::chrono::seconds(3));

    std::cout << "Tasks completed: " << counter.load() << "/" << task_count << std::endl;
    std::cout << "Pool shut down successfully" << std::endl;
}

/**
 * Test work-stealing thread pool
 */
void test_work_stealing_thread_pool() {
    std::cout << "\n=== Testing Work-Stealing Thread Pool ===" << std::endl;

    WorkStealingThreadPool pool(4);
    std::atomic<int> counter{0};
    const int task_count = 20;

    for (int i = 0; i < task_count; ++i) {
        pool.submit([&counter, i]() {
            std::cout << "Task " << i << " executing on thread "
                      << std::this_thread::get_id() << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(50));
            counter++;
        });
    }

    std::this_thread::sleep_for(std::chrono::seconds(2));

    std::cout << "Tasks completed: " << counter.load() << "/" << task_count << std::endl;
    std::cout << "Pool shut down successfully" << std::endl;
}

/**
 * Performance comparison
 */
void performance_comparison() {
    std::cout << "\n=== Performance Comparison ===" << std::endl;

    const size_t pool_size = std::thread::hardware_concurrency();
    const size_t task_count = 10000;

    std::cout << "Pool Size: " << pool_size << std::endl;
    std::cout << "Task Count: " << task_count << std::endl << std::endl;

    // Test 1: Fixed Thread Pool
    {
        std::cout << "1. Fixed Thread Pool" << std::endl;
        std::atomic<size_t> completed{0};

        double time = measure_time([&]() {
            FixedThreadPool pool(pool_size);

            for (size_t i = 0; i < task_count; ++i) {
                pool.submit([&completed]() {
                    // Simulate work
                    volatile int sum = 0;
                    for (int j = 0; j < 1000; ++j) {
                        sum += j;
                    }
                    completed++;
                });
            }

            // Wait for completion
            while (completed.load() < task_count) {
                std::this_thread::sleep_for(std::chrono::milliseconds(1));
            }
        });

        std::cout << "Time: " << time << " ms" << std::endl;
        std::cout << "Tasks completed: " << completed.load() << std::endl;
    }

    // Test 2: Work-Stealing Thread Pool
    {
        std::cout << "\n2. Work-Stealing Thread Pool" << std::endl;
        std::atomic<size_t> completed{0};

        double time = measure_time([&]() {
            WorkStealingThreadPool pool(pool_size);

            for (size_t i = 0; i < task_count; ++i) {
                pool.submit([&completed]() {
                    volatile int sum = 0;
                    for (int j = 0; j < 1000; ++j) {
                        sum += j;
                    }
                    completed++;
                });
            }

            while (completed.load() < task_count) {
                std::this_thread::sleep_for(std::chrono::milliseconds(1));
            }
        });

        std::cout << "Time: " << time << " ms" << std::endl;
        std::cout << "Tasks completed: " << completed.load() << std::endl;
    }
}

/**
 * Main function
 */
int main() {
    std::cout << "Thread Pool Implementation Exercise (C++)\n" << std::endl;

    test_fixed_thread_pool();
    test_work_stealing_thread_pool();
    performance_comparison();

    return 0;
}
