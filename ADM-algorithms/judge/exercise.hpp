#pragma once

#include <string>
#include <vector>

namespace adm_judge {

enum class Difficulty {
    Easy,
    Medium,
    Hard
};

enum class Status {
    NotStarted,
    InProgress,
    Done
};

struct Exercise {
    std::string name;
    std::string path;
    std::string topic;
    Difficulty difficulty;
    Status status;
    int order;

    std::string getDifficultyString() const {
        switch (difficulty) {
            case Difficulty::Easy: return "Easy";
            case Difficulty::Medium: return "Medium";
            case Difficulty::Hard: return "Hard";
        }
        return "Unknown";
    }

    std::string getStatusString() const {
        switch (status) {
            case Status::NotStarted: return "Not Started";
            case Status::InProgress: return "In Progress";
            case Status::Done: return "Done";
        }
        return "Unknown";
    }
};

// 练习列表配置
inline std::vector<Exercise> getAllExercises() {
    return {
        // 01 - Algorithm Analysis
        {"intro01", "exercises/01_analysis/intro01_runtime.cpp", "Algorithm Analysis", Difficulty::Easy, Status::NotStarted, 1},
        {"intro02", "exercises/01_analysis/intro02_big_o.cpp", "Algorithm Analysis", Difficulty::Easy, Status::NotStarted, 2},
        {"intro03", "exercises/01_analysis/intro03_recurrence.cpp", "Algorithm Analysis", Difficulty::Medium, Status::NotStarted, 3},

        // 02 - Data Structures
        {"ds01", "exercises/02_data_structures/ds01_vector.cpp", "Data Structures", Difficulty::Easy, Status::NotStarted, 4},
        {"ds02", "exercises/02_data_structures/ds02_linked_list.cpp", "Data Structures", Difficulty::Medium, Status::NotStarted, 5},
        {"ds03", "exercises/02_data_structures/ds03_stack.cpp", "Data Structures", Difficulty::Easy, Status::NotStarted, 6},
        {"ds04", "exercises/02_data_structures/ds04_queue.cpp", "Data Structures", Difficulty::Easy, Status::NotStarted, 7},
        {"ds05", "exercises/02_data_structures/ds05_binary_tree.cpp", "Data Structures", Difficulty::Medium, Status::NotStarted, 8},
        {"ds06", "exercises/02_data_structures/ds06_bst.cpp", "Data Structures", Difficulty::Medium, Status::NotStarted, 9},
        {"ds07", "exercises/02_data_structures/ds07_heap.cpp", "Data Structures", Difficulty::Medium, Status::NotStarted, 10},
        {"ds08", "exercises/02_data_structures/ds08_hash_table.cpp", "Data Structures", Difficulty::Medium, Status::NotStarted, 11},
        {"ds09", "exercises/02_data_structures/ds09_union_find.cpp", "Data Structures", Difficulty::Medium, Status::NotStarted, 12},

        // 03 - Sorting and Searching
        {"sort01", "exercises/03_sorting/sort01_bubble_sort.cpp", "Sorting", Difficulty::Easy, Status::NotStarted, 13},
        {"sort02", "exercises/03_sorting/sort02_merge_sort.cpp", "Sorting", Difficulty::Medium, Status::NotStarted, 14},
        {"sort03", "exercises/03_sorting/sort03_quick_sort.cpp", "Sorting", Difficulty::Medium, Status::NotStarted, 15},
        {"sort04", "exercises/03_sorting/sort04_heap_sort.cpp", "Sorting", Difficulty::Medium, Status::NotStarted, 16},
        {"sort05", "exercises/03_sorting/sort05_binary_search.cpp", "Searching", Difficulty::Easy, Status::NotStarted, 17},
        {"sort06", "exercises/03_sorting/sort06_quick_select.cpp", "Searching", Difficulty::Medium, Status::NotStarted, 18},

        // 04 - Graph Traversal
        {"graph01", "exercises/04_graph_traversal/graph01_representation.cpp", "Graph Basics", Difficulty::Medium, Status::NotStarted, 19},
        {"graph02", "exercises/04_graph_traversal/graph02_bfs.cpp", "Graph Traversal", Difficulty::Medium, Status::NotStarted, 20},
        {"graph03", "exercises/04_graph_traversal/graph03_dfs.cpp", "Graph Traversal", Difficulty::Medium, Status::NotStarted, 21},
        {"graph04", "exercises/04_graph_traversal/graph04_connected_components.cpp", "Graph Traversal", Difficulty::Medium, Status::NotStarted, 22},
        {"graph05", "exercises/04_graph_traversal/graph05_topological_sort.cpp", "Graph Traversal", Difficulty::Medium, Status::NotStarted, 23},
        {"graph06", "exercises/04_graph_traversal/graph06_cycle_detection.cpp", "Graph Traversal", Difficulty::Medium, Status::NotStarted, 24},

        // 05 - Weighted Graph Algorithms
        {"weighted01", "exercises/05_weighted_graphs/weighted01_dijkstra.cpp", "Shortest Path", Difficulty::Hard, Status::NotStarted, 25},
        {"weighted02", "exercises/05_weighted_graphs/weighted02_bellman_ford.cpp", "Shortest Path", Difficulty::Hard, Status::NotStarted, 26},
        {"weighted03", "exercises/05_weighted_graphs/weighted03_floyd_warshall.cpp", "Shortest Path", Difficulty::Hard, Status::NotStarted, 27},
        {"weighted04", "exercises/05_weighted_graphs/weighted04_prim.cpp", "MST", Difficulty::Hard, Status::NotStarted, 28},
        {"weighted05", "exercises/05_weighted_graphs/weighted05_kruskal.cpp", "MST", Difficulty::Hard, Status::NotStarted, 29},
        {"weighted06", "exercises/05_weighted_graphs/weighted06_max_flow.cpp", "Network Flow", Difficulty::Hard, Status::NotStarted, 30},

        // 06 - Combinatorial Search
        {"comb01", "exercises/06_combinatorial/comb01_backtracking.cpp", "Backtracking", Difficulty::Medium, Status::NotStarted, 31},
        {"comb02", "exercises/06_combinatorial/comb02_permutations.cpp", "Backtracking", Difficulty::Medium, Status::NotStarted, 32},
        {"comb03", "exercises/06_combinatorial/comb03_combinations.cpp", "Backtracking", Difficulty::Medium, Status::NotStarted, 33},
        {"comb04", "exercises/06_combinatorial/comb04_n_queens.cpp", "Backtracking", Difficulty::Hard, Status::NotStarted, 34},
        {"comb05", "exercises/06_combinatorial/comb05_sudoku_solver.cpp", "Backtracking", Difficulty::Hard, Status::NotStarted, 35},

        // 07 - Dynamic Programming
        {"dp01", "exercises/07_dynamic_programming/dp01_fibonacci.cpp", "DP Basics", Difficulty::Easy, Status::NotStarted, 36},
        {"dp02", "exercises/07_dynamic_programming/dp02_coin_change.cpp", "DP", Difficulty::Medium, Status::NotStarted, 37},
        {"dp03", "exercises/07_dynamic_programming/dp03_knapsack.cpp", "DP", Difficulty::Medium, Status::NotStarted, 38},
        {"dp04", "exercises/07_dynamic_programming/dp04_lcs.cpp", "DP", Difficulty::Medium, Status::NotStarted, 39},
        {"dp05", "exercises/07_dynamic_programming/dp05_lis.cpp", "DP", Difficulty::Medium, Status::NotStarted, 40},
        {"dp06", "exercises/07_dynamic_programming/dp06_edit_distance.cpp", "DP", Difficulty::Medium, Status::NotStarted, 41},
        {"dp07", "exercises/07_dynamic_programming/dp07_matrix_chain.cpp", "DP", Difficulty::Hard, Status::NotStarted, 42},
        {"dp08", "exercises/07_dynamic_programming/dp08_optimal_bst.cpp", "DP", Difficulty::Hard, Status::NotStarted, 43},

        // 08 - Greedy Algorithms
        {"greedy01", "exercises/08_greedy/greedy01_activity_selection.cpp", "Greedy", Difficulty::Medium, Status::NotStarted, 44},
        {"greedy02", "exercises/08_greedy/greedy02_huffman_coding.cpp", "Greedy", Difficulty::Hard, Status::NotStarted, 45},
        {"greedy03", "exercises/08_greedy/greedy03_interval_scheduling.cpp", "Greedy", Difficulty::Medium, Status::NotStarted, 46},

        // 09 - String Algorithms
        {"string01", "exercises/09_strings/string01_naive_matching.cpp", "String Matching", Difficulty::Easy, Status::NotStarted, 47},
        {"string02", "exercises/09_strings/string02_kmp.cpp", "String Matching", Difficulty::Hard, Status::NotStarted, 48},
        {"string03", "exercises/09_strings/string03_rabin_karp.cpp", "String Matching", Difficulty::Medium, Status::NotStarted, 49},
        {"string04", "exercises/09_strings/string04_trie.cpp", "String Data Structures", Difficulty::Medium, Status::NotStarted, 50},
        {"string05", "exercises/09_strings/string05_suffix_array.cpp", "String Data Structures", Difficulty::Hard, Status::NotStarted, 51},

        // 10 - Computational Geometry
        {"geo01", "exercises/10_geometry/geo01_convex_hull.cpp", "Geometry", Difficulty::Hard, Status::NotStarted, 52},
        {"geo02", "exercises/10_geometry/geo02_line_intersection.cpp", "Geometry", Difficulty::Medium, Status::NotStarted, 53},
        {"geo03", "exercises/10_geometry/geo03_closest_pair.cpp", "Geometry", Difficulty::Hard, Status::NotStarted, 54},

        // 11 - NP-Complete Problems
        {"np01", "exercises/11_np_complete/np01_tsp_backtrack.cpp", "NP-Complete", Difficulty::Hard, Status::NotStarted, 55},
        {"np02", "exercises/11_np_complete/np02_tsp_dp.cpp", "NP-Complete", Difficulty::Hard, Status::NotStarted, 56},
        {"np03", "exercises/11_np_complete/np03_vertex_cover_approx.cpp", "Approximation", Difficulty::Hard, Status::NotStarted, 57},
        {"np04", "exercises/11_np_complete/np04_knapsack_approx.cpp", "Approximation", Difficulty::Hard, Status::NotStarted, 58},

        // 12 - Divide and Conquer (ADM 3rd新增章节)
        {"divide01", "exercises/12_divide_conquer/divide01_binary_search_recursive.cpp", "Divide and Conquer", Difficulty::Easy, Status::NotStarted, 59},
        {"divide02", "exercises/12_divide_conquer/divide02_maximum_subarray.cpp", "Divide and Conquer", Difficulty::Medium, Status::NotStarted, 60},
        {"divide03", "exercises/12_divide_conquer/divide03_closest_pair_points.cpp", "Divide and Conquer", Difficulty::Hard, Status::NotStarted, 61},

        // 13 - Randomized Algorithms (ADM 3rd新增章节)
        {"random01", "exercises/13_randomized/random01_quicksort_randomized.cpp", "Randomized Algorithms", Difficulty::Medium, Status::NotStarted, 62},
        {"random02", "exercises/13_randomized/random02_bloom_filter.cpp", "Randomized Algorithms", Difficulty::Medium, Status::NotStarted, 63},
        {"random03", "exercises/13_randomized/random03_skip_list.cpp", "Randomized Algorithms", Difficulty::Hard, Status::NotStarted, 64},

        // 14 - Advanced Graph Algorithms
        {"adv_graph01", "exercises/14_advanced_graphs/adv_graph01_strongly_connected.cpp", "Advanced Graphs", Difficulty::Hard, Status::NotStarted, 65},
        {"adv_graph02", "exercises/14_advanced_graphs/adv_graph02_articulation_points.cpp", "Advanced Graphs", Difficulty::Hard, Status::NotStarted, 66},

        // 15 - Number Theory
        {"num01", "exercises/15_number_theory/num01_gcd_lcm.cpp", "Number Theory", Difficulty::Easy, Status::NotStarted, 67},
        {"num02", "exercises/15_number_theory/num02_primality_test.cpp", "Number Theory", Difficulty::Medium, Status::NotStarted, 68},
    };
}

} // namespace adm_judge
