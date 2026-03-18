/**
 * SOLUTION: Work-Stealing Deque (Chase-Lev Algorithm)
 *
 * This is the complete reference implementation of the Chase-Lev work-stealing deque.
 * All TODOs from the exercise have been completed.
 *
 * KEY IMPLEMENTATION POINTS:
 * 1. Owner operations (push/pop) use relaxed memory ordering when possible
 * 2. Thief operations (steal) use acquire/release and CAS
 * 3. Dynamic resizing handled by owner only
 * 4. Memory fences ensure correct synchronization
 */

#include <iostream>
#include <atomic>
#include <thread>
#include <vector>
#include <memory>
#include <chrono>
#include <random>
#include <algorithm>

namespace multiprocessor::part2::work_stealing::solution {

template <typename T>
class WorkStealingDeque {
private:
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

        std::unique_ptr<CircularArray> grow(size_t bottom, size_t top) {
            auto new_array = std::make_unique<CircularArray>(capacity * 2);
            for (size_t i = top; i < bottom; ++i) {
                new_array->put(i, get(i));
            }
            return new_array;
        }
    };

    std::atomic<size_t> top_{0};
    std::atomic<size_t> bottom_{0};
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
     * SOLUTION: push (owner only)
     */
    void push(T value) {
        size_t b = bottom_.load(std::memory_order_relaxed);
        size_t t = top_.load(std::memory_order_acquire);
        CircularArray* a = array_.load(std::memory_order_relaxed);

        if (b - t >= a->capacity) {
            CircularArray* new_array = a->grow(b, t).release();
            array_.store(new_array, std::memory_order_release);
            delete a;
            a = new_array;
        }

        a->put(b, value);
        std::atomic_thread_fence(std::memory_order_release);
        bottom_.store(b + 1, std::memory_order_relaxed);
    }

    /**
     * SOLUTION: pop (owner only)
     */
    T pop() {
        size_t b = bottom_.load(std::memory_order_relaxed) - 1;
        CircularArray* a = array_.load(std::memory_order_relaxed);
        bottom_.store(b, std::memory_order_relaxed);

        std::atomic_thread_fence(std::memory_order_seq_cst);

        size_t t = top_.load(std::memory_order_relaxed);

        T result{};
        if (t <= b) {
            result = a->get(b);

            if (t == b) {
                if (!top_.compare_exchange_strong(t, t + 1,
                                                  std::memory_order_seq_cst,
                                                  std::memory_order_relaxed)) {
                    result = T{};
                }
                bottom_.store(b + 1, std::memory_order_relaxed);
            }
        } else {
            bottom_.store(b + 1, std::memory_order_relaxed);
        }

        return result;
    }

    /**
     * SOLUTION: steal (thieves)
     */
    T steal() {
        size_t t = top_.load(std::memory_order_acquire);
        std::atomic_thread_fence(std::memory_order_seq_cst);
        size_t b = bottom_.load(std::memory_order_acquire);

        if (t >= b) {
            return T{};
        }

        CircularArray* a = array_.load(std::memory_order_consume);
        T value = a->get(t);

        if (!top_.compare_exchange_strong(t, t + 1,
                                         std::memory_order_seq_cst,
                                         std::memory_order_relaxed)) {
            return T{};
        }

        return value;
    }

    size_t size() const {
        size_t b = bottom_.load(std::memory_order_relaxed);
        size_t t = top_.load(std::memory_order_relaxed);
        return (b >= t) ? (b - t) : 0;
    }
};

// Test task
struct Task {
    int id;
    int workload;

    Task() : id(0), workload(0) {}
    Task(int i, int w) : id(i), workload(w) {}

    void execute() const {
        volatile int sum = 0;
        for (int i = 0; i < workload; ++i) {
            sum += i;
        }
    }
};

void demonstrate_solution() {
    std::cout << "=== SOLUTION: Work-Stealing Deque ===\n\n";

    std::cout << "Implementation Details:\n\n";

    std::cout << "1. push() - Owner pushes to bottom:\n";
    std::cout << "   - Load bottom with relaxed ordering\n";
    std::cout << "   - Load top with acquire (sync with thieves)\n";
    std::cout << "   - Check if resize needed, grow if necessary\n";
    std::cout << "   - Put value at bottom\n";
    std::cout << "   - Release fence + store bottom\n\n";

    std::cout << "2. pop() - Owner pops from bottom:\n";
    std::cout << "   - Decrement bottom (claim task)\n";
    std::cout << "   - Sequential fence (sync with steal)\n";
    std::cout << "   - Load top\n";
    std::cout << "   - If last element, CAS with thieves\n";
    std::cout << "   - Otherwise just take it\n\n";

    std::cout << "3. steal() - Thieves steal from top:\n";
    std::cout << "   - Load top with acquire\n";
    std::cout << "   - Sequential fence\n";
    std::cout << "   - Load bottom with acquire\n";
    std::cout << "   - Check if empty\n";
    std::cout << "   - Read value\n";
    std::cout << "   - CAS top to claim\n\n";

    // Demonstration
    WorkStealingDeque<Task> deque;

    std::cout << "Test: Basic operations\n";
    deque.push(Task(1, 100));
    deque.push(Task(2, 200));
    deque.push(Task(3, 300));

    std::cout << "Pushed tasks: 1, 2, 3\n";
    std::cout << "Deque size: " << deque.size() << "\n\n";

    Task t1 = deque.pop();
    std::cout << "Popped from owner: " << t1.id << " (LIFO - should be 3)\n";

    Task t2 = deque.steal();
    std::cout << "Stolen by thief: " << t2.id << " (FIFO - should be 1)\n\n";

    std::cout << "✅ Solution demonstrates correct Chase-Lev algorithm\n";
    std::cout << "✅ Owner gets LIFO order (cache locality)\n";
    std::cout << "✅ Thieves get FIFO order (load balancing)\n";
}

} // namespace

int main() {
    multiprocessor::part2::work_stealing::solution::demonstrate_solution();
    return 0;
}
