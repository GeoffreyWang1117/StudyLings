/**
 * Exercise 01: Hello Threads!
 *
 * CONCEPT: Introduction to thread creation and execution in C++20
 *
 * In this exercise, you'll learn how to create and manage threads using
 * the C++ standard library (std::thread, std::jthread).
 *
 * LEARNING OBJECTIVES:
 * - Create threads using std::thread or std::jthread
 * - Understand thread lifecycle and joining
 * - Use lambda expressions with threads
 *
 * TODO: Complete the functions marked with TODO comments
 */

#include <iostream>
#include <thread>
#include <vector>
#include <chrono>

namespace multiprocessor::basics {

/**
 * TODO: Create and return a thread that prints "Hello from Thread [id]!"
 *
 * @param thread_id The ID to include in the message
 * @return A new std::thread object
 */
std::thread create_thread(int thread_id) {
    // TODO: Implement this function
    // HINT: Use a lambda expression
    // HINT: Return std::thread with the lambda
    return std::thread([]() {
        // TODO: Implement the thread function
    });
}

/**
 * TODO: Create multiple threads and start them all
 *
 * @param count Number of threads to create
 * @return Vector of started threads
 */
std::vector<std::thread> create_and_start_threads(int count) {
    // TODO: Implement this function
    // HINT: Create a vector, populate it with threads
    std::vector<std::thread> threads;
    // TODO: Create 'count' threads and add them to the vector
    return threads;
}

/**
 * TODO: Wait for all threads to complete
 *
 * @param threads Vector of threads to wait for
 */
void wait_for_all_threads(std::vector<std::thread>& threads) {
    // TODO: Implement this function
    // HINT: Use the join() method on each thread
    // HINT: Check if thread is joinable before joining
}

} // namespace multiprocessor::basics

/**
 * Main function for testing (you can run this directly)
 */
int main() {
    using namespace multiprocessor::basics;

    std::cout << "Creating threads...\n";
    auto threads = create_and_start_threads(5);

    std::cout << "Waiting for threads to complete...\n";
    wait_for_all_threads(threads);

    std::cout << "All threads completed!\n";

    return 0;
}
