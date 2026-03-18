#ifndef RUNNER_H
#define RUNNER_H

#include "exercise_manager.h"
#include "progress.h"
#include <string>

class Runner {
public:
    Runner(ExerciseManager& manager, ProgressTracker& progress);

    // 运行和验证
    void run(int exercise_num = -1);
    bool verify(int exercise_num = -1);
    void show_hint(int exercise_num = -1);

    // 监视模式
    void watch_mode();

private:
    ExerciseManager& manager_;
    ProgressTracker& progress_;
    int current_hint_level_;

    // 编译和测试
    bool compile_exercise(const Exercise& ex, std::string& output);
    bool run_tests(const Exercise& ex, std::string& output);

    // 辅助函数
    void print_exercise_header(const Exercise& ex);
    void print_success(const Exercise& ex);
    void print_failure(const std::string& output);
    const Exercise* get_target_exercise(int exercise_num);
};

#endif // RUNNER_H
