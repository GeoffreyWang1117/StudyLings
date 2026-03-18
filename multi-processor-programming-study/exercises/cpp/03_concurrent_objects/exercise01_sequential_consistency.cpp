/**
 * Exercise: Sequential Consistency (C++20)
 *
 * CONCEPT: Sequential consistency and its properties
 *
 * Sequential Consistency: The result of any execution is the same as if
 * operations of all threads were executed in some sequential order, and
 * operations of each thread appear in this sequence in program order.
 *
 * LEARNING OBJECTIVES:
 * - Understand sequential consistency in C++
 * - Use std::atomic with seq_cst ordering
 * - Implement sequentially consistent counter
 */

#include <iostream>
#include <thread>
#include <vector>
#include <atomic>

namespace multiprocessor::concurrent_objects {

/**
 * TODO: Implement a sequentially consistent counter
 */
class SequentialCounter {
private:
    // TODO: Add std::atomic<int> value

public:
    SequentialCounter() {
        // TODO: Initialize
    }

    /**
     * TODO: Implement increment operation
     * Should be sequentially consistent
     *
     * @return the value BEFORE increment
     */
    int get_and_increment() {
        // TODO: Implement using fetch_add
        // HINT: Use std::memory_order_seq_cst (default)
        return 0;
    }

    /**
     * TODO: Implement get operation
     */
    int get() const {
        // TODO: Implement
        return 0;
    }

    /**
     * TODO: Implement set operation
     */
    void set(int new_value) {
        // TODO: Implement
    }
};

/**
 * TODO: Implement a sequentially consistent register
 */
template <typename T>
class SequentialRegister {
private:
    std::atomic<T*> value;

public:
    explicit SequentialRegister(T initial_value) {
        // TODO: Initialize
        // HINT: std::atomic<T*> for pointer types
        value.store(new T(initial_value));
    }

    ~SequentialRegister() {
        delete value.load();
    }

    /**
     * TODO: Implement read operation
     */
    T read() {
        // TODO: Implement
        T* ptr = value.load(std::memory_order_seq_cst);
        return ptr ? *ptr : T{};
    }

    /**
     * TODO: Implement write operation
     */
    void write(T new_value) {
        // TODO: Implement
        // HINT: Need to handle memory management carefully
        T* new_ptr = new T(new_value);
        T* old_ptr = value.exchange(new_ptr, std::memory_order_seq_cst);
        delete old_ptr;
    }
};

void test_sequential_counter() {
    std::cout << "Testing Sequential Counter:\n";

    SequentialCounter counter;
    const int num_threads = 10;
    const int increments_per_thread = 1000;

    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&counter, increments_per_thread]() {
            for (int j = 0; j < increments_per_thread; ++j) {
                counter.get_and_increment();
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    int expected = num_threads * increments_per_thread;
    int actual = counter.get();

    std::cout << "Expected: " << expected << "\n";
    std::cout << "Actual: " << actual << "\n";
    std::cout << (actual == expected ? "✅ PASS\n\n" : "❌ FAIL\n\n");
}

void test_sequential_register() {
    std::cout << "Testing Sequential Register:\n";

    SequentialRegister<int> reg(0);

    // Writer thread
    std::thread writer([&reg]() {
        for (int i = 0; i < 100; ++i) {
            reg.write(i);
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        }
    });

    // Reader threads
    std::vector<std::thread> readers;
    for (int i = 0; i < 3; ++i) {
        readers.emplace_back([&reg, i]() {
            for (int j = 0; j < 50; ++j) {
                int value = reg.read();
                std::cout << "Reader " << i << " read: " << value << "\n";
                std::this_thread::sleep_for(std::chrono::milliseconds(2));
            }
        });
    }

    writer.join();
    for (auto& t : readers) {
        t.join();
    }

    std::cout << "✅ Sequential register test completed\n\n";
}

} // namespace multiprocessor::concurrent_objects

int main() {
    using namespace multiprocessor::concurrent_objects;

    std::cout << "=== Sequential Consistency Test (C++) ===\n\n";

    test_sequential_counter();
    test_sequential_register();

    return 0;
}
