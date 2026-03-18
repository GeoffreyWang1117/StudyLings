#ifndef EXERCISE_MANAGER_H
#define EXERCISE_MANAGER_H

#include <string>
#include <vector>
#include <map>

struct Exercise {
    int number;
    std::string topic;
    std::string name;
    std::string file_path;
    std::string description;
    std::vector<std::string> hints;
    std::string solution_path;

    std::string get_display_name() const {
        return std::to_string(number) + ". " + topic + "/" + name;
    }
};

class ExerciseManager {
public:
    ExerciseManager();
    bool initialize();

    // 获取练习
    const Exercise* get_exercise(int number) const;
    const Exercise* get_next_incomplete() const;
    const std::vector<Exercise>& get_all_exercises() const { return exercises_; }

    // 操作
    void list_exercises() const;
    void reset_exercise(int number);
    void show_solution(int number) const;

    int get_total_count() const { return exercises_.size(); }

private:
    std::vector<Exercise> exercises_;
    void load_exercises();
    void add_intro_exercises();
    void add_kernel_exercises();
    void add_thread_exercises();
    void add_memory_exercises();
    void add_shared_memory_exercises();
    void add_sync_exercises();
    void add_optimization_exercises();
    void add_stream_exercises();
    void add_advanced_exercises();
    void add_algorithm_exercises();
    void add_image_processing_exercises();
    void add_deep_learning_exercises();
    void add_scientific_computing_exercises();
    void add_multi_gpu_exercises();
    void add_tensor_cores_exercises();
    void add_cuda_graphs_exercises();
    void add_cooperative_groups_exercises();
    void add_profiling_debugging_exercises();
    void add_cuda_libraries_exercises();
    void add_dynamic_parallelism_exercises();
    void add_projects_exercises();
    void add_unified_memory_exercises();
    void add_warp_primitives_exercises();
    void add_graph_algorithms_exercises();
    void add_sparse_matrices_exercises();
    void add_molecular_dynamics_exercises();
    void add_ray_tracing_exercises();
    void add_video_processing_exercises();
    void add_ml_operators_exercises();
};

#endif // EXERCISE_MANAGER_H
