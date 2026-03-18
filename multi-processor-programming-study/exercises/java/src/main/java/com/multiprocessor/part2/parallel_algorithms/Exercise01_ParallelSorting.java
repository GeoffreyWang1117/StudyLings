package com.multiprocessor.part2.parallel_algorithms;

import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

/**
 * Exercise: Parallel Sorting with ForkJoinPool
 *
 * Java provides excellent support for parallel algorithms through ForkJoinPool.
 * This exercise demonstrates parallel merge sort and quick sort implementations.
 */
public class Exercise01_ParallelSorting {

    /**
     * Parallel Merge Sort using ForkJoinPool
     */
    public static class ParallelMergeSort {
        private static final int SEQUENTIAL_CUTOFF = 10000;

        private static class SortTask extends RecursiveAction {
            private final int[] array;
            private final int left;
            private final int right;
            private final int[] temp;

            SortTask(int[] array, int left, int right, int[] temp) {
                this.array = array;
                this.left = left;
                this.right = right;
                this.temp = temp;
            }

            @Override
            protected void compute() {
                if (right - left <= 1) return;

                // Sequential cutoff
                if (right - left < SEQUENTIAL_CUTOFF) {
                    Arrays.sort(array, left, right);
                    return;
                }

                int mid = left + (right - left) / 2;

                // Fork left half
                SortTask leftTask = new SortTask(array, left, mid, temp);
                SortTask rightTask = new SortTask(array, mid, right, temp);

                invokeAll(leftTask, rightTask);

                // Merge
                merge(array, left, mid, right, temp);
            }

            private void merge(int[] arr, int left, int mid, int right, int[] temp) {
                System.arraycopy(arr, left, temp, left, right - left);

                int i = left, j = mid, k = left;

                while (i < mid && j < right) {
                    if (temp[i] <= temp[j]) {
                        arr[k++] = temp[i++];
                    } else {
                        arr[k++] = temp[j++];
                    }
                }

                while (i < mid) arr[k++] = temp[i++];
                while (j < right) arr[k++] = temp[j++];
            }
        }

        public static void sort(int[] array) {
            if (array == null || array.length <= 1) return;

            int[] temp = new int[array.length];
            ForkJoinPool pool = ForkJoinPool.commonPool();
            pool.invoke(new SortTask(array, 0, array.length, temp));
        }
    }

    /**
     * Parallel Quick Sort using ForkJoinPool
     */
    public static class ParallelQuickSort {
        private static final int SEQUENTIAL_CUTOFF = 10000;

        private static class SortTask extends RecursiveAction {
            private final int[] array;
            private final int left;
            private final int right;

            SortTask(int[] array, int left, int right) {
                this.array = array;
                this.left = left;
                this.right = right;
            }

            @Override
            protected void compute() {
                if (right - left <= 1) return;

                // Sequential cutoff
                if (right - left < SEQUENTIAL_CUTOFF) {
                    Arrays.sort(array, left, right);
                    return;
                }

                int pivotPos = partition(array, left, right);

                // Fork both halves
                SortTask leftTask = new SortTask(array, left, pivotPos);
                SortTask rightTask = new SortTask(array, pivotPos + 1, right);

                invokeAll(leftTask, rightTask);
            }

            private int partition(int[] arr, int left, int right) {
                int pivot = arr[right - 1];
                int i = left;

                for (int j = left; j < right - 1; j++) {
                    if (arr[j] <= pivot) {
                        int temp = arr[i];
                        arr[i] = arr[j];
                        arr[j] = temp;
                        i++;
                    }
                }

                int temp = arr[i];
                arr[i] = arr[right - 1];
                arr[right - 1] = temp;

                return i;
            }
        }

        public static void sort(int[] array) {
            if (array == null || array.length <= 1) return;

            ForkJoinPool pool = ForkJoinPool.commonPool();
            pool.invoke(new SortTask(array, 0, array.length));
        }
    }

    private static boolean isSorted(int[] array) {
        for (int i = 1; i < array.length; i++) {
            if (array[i] < array[i-1]) return false;
        }
        return true;
    }

    public static void testCorrectness() {
        System.out.println("=== Correctness Tests ===\n");

        // Test Parallel Merge Sort
        {
            int[] arr = {5, 2, 8, 1, 9, 3, 7, 4, 6};
            System.out.println("Parallel Merge Sort:");
            System.out.print("  Before: ");
            for (int x : arr) System.out.print(x + " ");
            System.out.println();

            ParallelMergeSort.sort(arr);

            System.out.print("  After:  ");
            for (int x : arr) System.out.print(x + " ");
            System.out.println();
            System.out.println("  " + (isSorted(arr) ? "✅ PASS" : "❌ FAIL") + "\n");
        }

        // Test Parallel Quick Sort
        {
            int[] arr = {5, 2, 8, 1, 9, 3, 7, 4, 6};
            System.out.println("Parallel Quick Sort:");
            System.out.print("  Before: ");
            for (int x : arr) System.out.print(x + " ");
            System.out.println();

            ParallelQuickSort.sort(arr);

            System.out.print("  After:  ");
            for (int x : arr) System.out.print(x + " ");
            System.out.println();
            System.out.println("  " + (isSorted(arr) ? "✅ PASS" : "❌ FAIL") + "\n");
        }
    }

    public static void comparePerformance() {
        System.out.println("=== Performance Comparison ===\n");

        final int size = 10000000;
        Random rand = new Random(42);

        System.out.println("Array size: " + size);
        System.out.println("Available processors: " + Runtime.getRuntime().availableProcessors());
        System.out.println("ForkJoinPool parallelism: " + ForkJoinPool.commonPool().getParallelism() + "\n");

        // Generate test data
        int[] original = new int[size];
        for (int i = 0; i < size; i++) {
            original[i] = rand.nextInt(1000000);
        }

        // Test Arrays.sort (sequential)
        {
            int[] arr = original.clone();
            long start = System.currentTimeMillis();
            Arrays.sort(arr);
            long duration = System.currentTimeMillis() - start;

            System.out.println("Arrays.sort (sequential):");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Sorted: " + (isSorted(arr) ? "✅" : "❌") + "\n");
        }

        // Test Arrays.parallelSort
        {
            int[] arr = original.clone();
            long start = System.currentTimeMillis();
            Arrays.parallelSort(arr);
            long duration = System.currentTimeMillis() - start;

            System.out.println("Arrays.parallelSort (built-in):");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Sorted: " + (isSorted(arr) ? "✅" : "❌") + "\n");
        }

        // Test Parallel Merge Sort
        {
            int[] arr = original.clone();
            long start = System.currentTimeMillis();
            ParallelMergeSort.sort(arr);
            long duration = System.currentTimeMillis() - start;

            System.out.println("Parallel Merge Sort:");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Sorted: " + (isSorted(arr) ? "✅" : "❌") + "\n");
        }

        // Test Parallel Quick Sort
        {
            int[] arr = original.clone();
            long start = System.currentTimeMillis();
            ParallelQuickSort.sort(arr);
            long duration = System.currentTimeMillis() - start;

            System.out.println("Parallel Quick Sort:");
            System.out.println("  Time: " + duration + "ms");
            System.out.println("  Sorted: " + (isSorted(arr) ? "✅" : "❌") + "\n");
        }

        System.out.println("💡 Java's Arrays.parallelSort uses similar approach");
        System.out.println("💡 ForkJoinPool provides work-stealing for load balance");
        System.out.println("💡 Speedup depends on cores and array size");
    }

    public static void demonstrateConcepts() {
        System.out.println("=== Parallel Sorting Concepts ===\n");

        System.out.println("ForkJoinPool Benefits:");
        System.out.println("  ✅ Work-stealing for load balancing");
        System.out.println("  ✅ Automatic thread management");
        System.out.println("  ✅ Efficient for recursive algorithms\n");

        System.out.println("Parallel Merge Sort:");
        System.out.println("  ✅ Stable sort");
        System.out.println("  ✅ Predictable divide");
        System.out.println("  ⚠️  Extra memory needed\n");

        System.out.println("Parallel Quick Sort:");
        System.out.println("  ✅ In-place sorting");
        System.out.println("  ✅ Good cache locality");
        System.out.println("  ⚠️  Pivot selection affects balance\n");

        System.out.println("Java Built-in:");
        System.out.println("  • Arrays.parallelSort() - production ready");
        System.out.println("  • Based on parallel merge sort");
        System.out.println("  • Uses ForkJoinPool internally");
        System.out.println("  • Recommended for production use\n");
    }

    public static void main(String[] args) {
        System.out.println("=== Parallel Sorting Algorithms Test ===\n");

        demonstrateConcepts();
        testCorrectness();
        comparePerformance();
    }
}
