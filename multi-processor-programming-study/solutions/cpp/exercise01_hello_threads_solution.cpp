/**
 * SOLUTION for Exercise 01: Hello Threads! (C++)
 *
 * This file contains the reference implementation.
 * Try to solve the exercise yourself before looking at this!
 */

#include <iostream>
#include <thread>
#include <vector>

namespace multiprocessor::basics {

/**
 * SOLUTION: Create and return a thread that prints message
 */
std::thread create_thread(int thread_id) {
    return std::thread([thread_id]() {
        std::cout << "Hello from Thread " << thread_id << "!\n";
    });
}

/**
 * SOLUTION: Create multiple threads and start them
 */
std::vector<std::thread> create_and_start_threads(int count) {
    std::vector<std::thread> threads;
    for (int i = 0; i < count; ++i) {
        threads.push_back(create_thread(i));
    }
    return threads;
}

/**
 * SOLUTION: Wait for all threads to complete
 */
void wait_for_all_threads(std::vector<std::thread>& threads) {
    for (auto& t : threads) {
        if (t.joinable()) {
            t.join();
        }
    }
}

} // namespace multiprocessor::basics

int main() {
    using namespace multiprocessor::basics;

    std::cout << "Creating threads...\n";
    auto threads = create_and_start_threads(5);

    std::cout << "Waiting for threads to complete...\n";
    wait_for_all_threads(threads);

    std::cout << "All threads completed!\n";

    return 0;
}
