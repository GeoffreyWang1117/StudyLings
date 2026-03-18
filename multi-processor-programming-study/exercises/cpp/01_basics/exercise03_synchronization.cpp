/**
 * Exercise 03: Basic Synchronization
 *
 * CONCEPT: Using std::mutex and std::lock_guard for mutual exclusion
 *
 * C++20 provides std::mutex for mutual exclusion. RAII wrappers like
 * std::lock_guard and std::unique_lock ensure exception-safe locking.
 *
 * LEARNING OBJECTIVES:
 * - Use std::mutex for mutual exclusion
 * - Understand RAII and exception safety
 * - Use std::lock_guard and std::unique_lock
 *
 * TODO: Make the counter thread-safe using std::mutex
 */

#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>

namespace multiprocessor::basics {

/**
 * TODO: Implement a thread-safe counter using std::mutex
 */
class SafeCounter {
private:
    int count = 0;
    // TODO: Add a mutex member variable
    // HINT: std::mutex mtx;

public:
    /**
     * TODO: Make this method thread-safe using std::lock_guard
     */
    void increment() {
        // TODO: Lock the mutex using std::lock_guard
        // TODO: Increment the count
    }

    /**
     * TODO: Make this method thread-safe as well
     */
    int get_count() {
        // TODO: Should this be synchronized? Why or why not?
        return count;
    }

    /**
     * TODO: Implement a decrement method (also thread-safe)
     */
    void decrement() {
        // TODO: Implement this
    }
};

/**
 * TODO: Implement a thread-safe bank account
 *
 * This class represents a bank account that can be accessed by multiple threads.
 * It must ensure that:
 * - Balance never goes negative (if initial balance is non-negative)
 * - Deposits and withdrawals are atomic
 * - Balance queries are consistent
 */
class BankAccount {
private:
    double balance;
    // TODO: Add a mutex

public:
    explicit BankAccount(double initial_balance) : balance(initial_balance) {}

    /**
     * TODO: Implement thread-safe deposit
     * @param amount Amount to deposit (must be positive)
     */
    void deposit(double amount) {
        // TODO: Implement with synchronization
        // HINT: Validate amount is positive
    }

    /**
     * TODO: Implement thread-safe withdrawal
     * @param amount Amount to withdraw
     * @return true if withdrawal successful, false if insufficient funds
     */
    bool withdraw(double amount) {
        // TODO: Implement with synchronization
        // HINT: Check if balance >= amount before withdrawing
        return false;
    }

    /**
     * TODO: Implement thread-safe balance query
     */
    double get_balance() {
        // TODO: Implement with synchronization
        return 0.0;
    }
};

void test_safe_counter() {
    std::cout << "=== Testing SafeCounter ===\n";

    SafeCounter counter;
    const int num_threads = 10;
    const int increments_per_thread = 1000;

    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&counter, increments_per_thread]() {
            for (int j = 0; j < increments_per_thread; ++j) {
                counter.increment();
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    int expected = num_threads * increments_per_thread;
    int actual = counter.get_count();

    std::cout << "Expected: " << expected << "\n";
    std::cout << "Actual: " << actual << "\n";
    std::cout << (actual == expected ? "✅ PASS\n" : "❌ FAIL\n");
}

void test_bank_account() {
    std::cout << "\n=== Testing BankAccount ===\n";

    BankAccount account(1000.0);

    // Multiple threads depositing and withdrawing
    std::vector<std::thread> threads;

    // 10 threads depositing
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([&account]() {
            for (int j = 0; j < 100; ++j) {
                account.deposit(10.0);
            }
        });
    }

    // 10 threads withdrawing
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([&account]() {
            for (int j = 0; j < 100; ++j) {
                account.withdraw(10.0);
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    double expected_balance = 1000.0;
    double actual_balance = account.get_balance();

    std::cout << "Expected balance: $" << expected_balance << "\n";
    std::cout << "Actual balance: $" << actual_balance << "\n";
    std::cout << (std::abs(actual_balance - expected_balance) < 0.01 ? "✅ PASS\n" : "❌ FAIL\n");
}

} // namespace multiprocessor::basics

/**
 * Demonstration and testing
 */
int main() {
    using namespace multiprocessor::basics;

    test_safe_counter();
    test_bank_account();

    return 0;
}
