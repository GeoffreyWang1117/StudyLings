/**
 * Exercise: Parallel Sorting Algorithms
 *
 * CONCEPT: Divide-and-conquer sorting with parallelism
 *
 * THE PROBLEM:
 * Sequential sorting is a bottleneck for large datasets
 * Modern multi-core systems can parallelize sorting operations
 *
 * PARALLEL SORTING STRATEGIES:
 * 1. Parallel Merge Sort: Recursively divide, sort in parallel, merge
 * 2. Parallel Quick Sort: Partition in parallel, recurse on sub-arrays
 * 3. Sample Sort: Partition into buckets, sort buckets in parallel
 *
 * LEARNING OBJECTIVES:
 * - Understand parallel divide-and-conquer
 * - Implement parallel merge sort
 * - Implement parallel quick sort
 * - Compare with std::sort and sequential versions
 * - Understand work-stealing for load balancing
 *
 * CPU REQUIREMENTS:
 * - Minimum: 4 cores
 * - Recommended: 8-16 cores
 * - Optimal: 16+ cores (better speedup)
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <thread>
#include <future>
#include <random>
#include <chrono>
#include <functional>

namespace multiprocessor::part2::parallel_algorithms {

/**
 * TODO: Implement Parallel Merge Sort
 */
template <typename T>
class ParallelMergeSort {
private:
    static constexpr size_t SEQUENTIAL_CUTOFF = 10000;

    static void merge(std::vector<T>& arr, size_t left, size_t mid, size_t right) {
        std::vector<T> temp(right - left);
        size_t i = left, j = mid, k = 0;

        while (i < mid && j < right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }

        while (i < mid) temp[k++] = arr[i++];
        while (j < right) temp[k++] = arr[j++];

        for (size_t i = 0; i < temp.size(); ++i) {
            arr[left + i] = temp[i];
        }
    }

    static void sequential_sort(std::vector<T>& arr, size_t left, size_t right) {
        if (right - left <= 1) return;

        size_t mid = left + (right - left) / 2;
        sequential_sort(arr, left, mid);
        sequential_sort(arr, mid, right);
        merge(arr, left, mid, right);
    }

    static void parallel_sort_helper(std::vector<T>& arr, size_t left, size_t right, int depth) {
        if (right - left <= 1) return;

        // Switch to sequential for small arrays or deep recursion
        if (right - left < SEQUENTIAL_CUTOFF || depth <= 0) {
            sequential_sort(arr, left, right);
            return;
        }

        size_t mid = left + (right - left) / 2;

        // TODO: Sort left and right halves in parallel
        auto future_left = std::async(std::launch::async,
                                      parallel_sort_helper,
                                      std::ref(arr), left, mid, depth - 1);

        parallel_sort_helper(arr, mid, right, depth - 1);

        future_left.get();

        // Merge the sorted halves
        merge(arr, left, mid, right);
    }

public:
    static void sort(std::vector<T>& arr) {
        if (arr.empty()) return;

        int max_depth = std::thread::hardware_concurrency();
        parallel_sort_helper(arr, 0, arr.size(), max_depth);
    }
};

/**
 * TODO: Implement Parallel Quick Sort
 */
template <typename T>
class ParallelQuickSort {
private:
    static constexpr size_t SEQUENTIAL_CUTOFF = 10000;

    static size_t partition(std::vector<T>& arr, size_t left, size_t right) {
        T pivot = arr[right - 1];
        size_t i = left;

        for (size_t j = left; j < right - 1; ++j) {
            if (arr[j] <= pivot) {
                std::swap(arr[i], arr[j]);
                ++i;
            }
        }

        std::swap(arr[i], arr[right - 1]);
        return i;
    }

    static void sequential_sort(std::vector<T>& arr, size_t left, size_t right) {
        if (right - left <= 1) return;

        size_t pivot_pos = partition(arr, left, right);
        sequential_sort(arr, left, pivot_pos);
        sequential_sort(arr, pivot_pos + 1, right);
    }

    static void parallel_sort_helper(std::vector<T>& arr, size_t left, size_t right, int depth) {
        if (right - left <= 1) return;

        // Switch to sequential for small arrays or deep recursion
        if (right - left < SEQUENTIAL_CUTOFF || depth <= 0) {
            sequential_sort(arr, left, right);
            return;
        }

        // TODO: Partition and sort sub-arrays in parallel
        size_t pivot_pos = partition(arr, left, right);

        auto future_left = std::async(std::launch::async,
                                      parallel_sort_helper,
                                      std::ref(arr), left, pivot_pos, depth - 1);

        parallel_sort_helper(arr, pivot_pos + 1, right, depth - 1);

        future_left.get();
    }

public:
    static void sort(std::vector<T>& arr) {
        if (arr.empty()) return;

        int max_depth = std::thread::hardware_concurrency();
        parallel_sort_helper(arr, 0, arr.size(), max_depth);
    }
};

/**
 * Testing Framework
 */
template <typename T>
bool is_sorted(const std::vector<T>& arr) {
    for (size_t i = 1; i < arr.size(); ++i) {
        if (arr[i] < arr[i-1]) return false;
    }
    return true;
}

void test_correctness() {
    std::cout << "=== Correctness Tests ===\n\n";

    // Test Parallel Merge Sort
    {
        std::vector<int> arr = {5, 2, 8, 1, 9, 3, 7, 4, 6};
        std::cout << "Parallel Merge Sort:\n";
        std::cout << "  Before: ";
        for (int x : arr) std::cout << x << " ";
        std::cout << "\n";

        ParallelMergeSort<int>::sort(arr);

        std::cout << "  After:  ";
        for (int x : arr) std::cout << x << " ";
        std::cout << "\n";
        std::cout << "  " << (is_sorted(arr) ? "✅ PASS" : "❌ FAIL") << "\n\n";
    }

    // Test Parallel Quick Sort
    {
        std::vector<int> arr = {5, 2, 8, 1, 9, 3, 7, 4, 6};
        std::cout << "Parallel Quick Sort:\n";
        std::cout << "  Before: ";
        for (int x : arr) std::cout << x << " ";
        std::cout << "\n";

        ParallelQuickSort<int>::sort(arr);

        std::cout << "  After:  ";
        for (int x : arr) std::cout << x << " ";
        std::cout << "\n";
        std::cout << "  " << (is_sorted(arr) ? "✅ PASS" : "❌ FAIL") << "\n\n";
    }
}

void compare_performance() {
    std::cout << "=== Performance Comparison ===\n\n";

    const size_t size = 10000000;
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(1, 1000000);

    std::cout << "Array size: " << size << "\n";
    std::cout << "Hardware threads: " << std::thread::hardware_concurrency() << "\n\n";

    // Generate test data
    std::vector<int> original(size);
    for (auto& x : original) {
        x = dist(gen);
    }

    // Test std::sort (sequential)
    {
        auto arr = original;
        auto start = std::chrono::high_resolution_clock::now();
        std::sort(arr.begin(), arr.end());
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "std::sort (sequential):\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Sorted: " << (is_sorted(arr) ? "✅" : "❌") << "\n\n";
    }

    // Test Parallel Merge Sort
    {
        auto arr = original;
        auto start = std::chrono::high_resolution_clock::now();
        ParallelMergeSort<int>::sort(arr);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Parallel Merge Sort:\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Sorted: " << (is_sorted(arr) ? "✅" : "❌") << "\n\n";
    }

    // Test Parallel Quick Sort
    {
        auto arr = original;
        auto start = std::chrono::high_resolution_clock::now();
        ParallelQuickSort<int>::sort(arr);
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

        std::cout << "Parallel Quick Sort:\n";
        std::cout << "  Time: " << duration.count() << "ms\n";
        std::cout << "  Sorted: " << (is_sorted(arr) ? "✅" : "❌") << "\n\n";
    }

    std::cout << "💡 Speedup depends on number of cores and array size\n";
    std::cout << "💡 Overhead for small arrays may exceed benefits\n";
    std::cout << "💡 Load balancing important for irregular data\n";
}

void demonstrate_concepts() {
    std::cout << "=== Parallel Sorting Concepts ===\n\n";

    std::cout << "Divide-and-Conquer Parallelism:\n";
    std::cout << "  1. Divide problem into sub-problems\n";
    std::cout << "  2. Solve sub-problems in parallel\n";
    std::cout << "  3. Combine results\n\n";

    std::cout << "Parallel Merge Sort:\n";
    std::cout << "  ✅ Stable sort\n";
    std::cout << "  ✅ Predictable divide (always halves)\n";
    std::cout << "  ⚠️  Merge phase sequential\n";
    std::cout << "  ⚠️  Extra memory for merging\n\n";

    std::cout << "Parallel Quick Sort:\n";
    std::cout << "  ✅ In-place (less memory)\n";
    std::cout << "  ✅ Good average case\n";
    std::cout << "  ⚠️  Unstable sort\n";
    std::cout << "  ⚠️  Load imbalance with bad pivots\n\n";

    std::cout << "Considerations:\n";
    std::cout << "  • Sequential cutoff: Avoid overhead on small arrays\n";
    std::cout << "  • Depth limit: Prevent thread explosion\n";
    std::cout << "  • Load balancing: Work stealing helps\n";
    std::cout << "  • Cache locality: Sequential portions benefit\n\n";
}

} // namespace

int main() {
    using namespace multiprocessor::part2::parallel_algorithms;

    std::cout << "=== Parallel Sorting Algorithms Test ===\n\n";

    demonstrate_concepts();
    test_correctness();
    compare_performance();

    return 0;
}
