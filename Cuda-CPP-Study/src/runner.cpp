#include "runner.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <filesystem>
#include <thread>
#include <chrono>
#include <sys/stat.h>

namespace fs = std::filesystem;

Runner::Runner(ExerciseManager& manager, ProgressTracker& progress)
    : manager_(manager), progress_(progress), current_hint_level_(0) {}

const Exercise* Runner::get_target_exercise(int exercise_num) {
    if (exercise_num == -1) {
        // 获取下一个未完成的练习
        const Exercise* ex = manager_.get_next_incomplete();
        if (!ex) {
            std::cout << "🎉 恭喜！你已完成所有练习！" << std::endl;
            progress_.show();
            return nullptr;
        }
        return ex;
    } else {
        const Exercise* ex = manager_.get_exercise(exercise_num);
        if (!ex) {
            std::cerr << "❌ 练习 " << exercise_num << " 不存在" << std::endl;
            return nullptr;
        }
        return ex;
    }
}

void Runner::run(int exercise_num) {
    const Exercise* ex = get_target_exercise(exercise_num);
    if (!ex) return;

    print_exercise_header(*ex);

    std::cout << "\n📝 描述:" << std::endl;
    std::cout << "   " << ex->description << std::endl;

    std::cout << "\n📂 文件: " << ex->file_path << std::endl;

    std::cout << "\n💡 提示: 编辑文件后运行 'cudalings verify' 来测试你的代码" << std::endl;
    std::cout << "   或使用 'cudalings watch' 启动自动验证模式" << std::endl;

    // 检查文件是否存在
    if (!fs::exists(ex->file_path)) {
        std::cout << "\n⚠️  警告: 练习文件不存在，可能需要先创建" << std::endl;
    }
}

bool Runner::verify(int exercise_num) {
    const Exercise* ex = get_target_exercise(exercise_num);
    if (!ex) return false;

    print_exercise_header(*ex);

    std::cout << "\n🔨 正在编译..." << std::endl;

    std::string compile_output;
    if (!compile_exercise(*ex, compile_output)) {
        std::cout << "❌ 编译失败\n" << std::endl;
        print_failure(compile_output);
        return false;
    }

    std::cout << "✅ 编译成功" << std::endl;
    std::cout << "\n🧪 正在运行测试..." << std::endl;

    std::string test_output;
    if (!run_tests(*ex, test_output)) {
        std::cout << "❌ 测试失败\n" << std::endl;
        print_failure(test_output);
        std::cout << "\n💡 提示: 使用 'cudalings hint " << ex->number
                  << "' 获取帮助" << std::endl;
        return false;
    }

    print_success(*ex);

    // 标记为已完成
    progress_.mark_completed(ex->number);

    // 提示下一个练习
    const Exercise* next = manager_.get_next_incomplete();
    if (next) {
        std::cout << "\n➡️  下一个练习: " << next->get_display_name() << std::endl;
        std::cout << "   运行 'cudalings run' 继续学习" << std::endl;
    } else {
        std::cout << "\n🏆 你已完成所有练习！太棒了！" << std::endl;
    }

    return true;
}

void Runner::show_hint(int exercise_num) {
    const Exercise* ex = get_target_exercise(exercise_num);
    if (!ex) return;

    print_exercise_header(*ex);

    if (ex->hints.empty()) {
        std::cout << "\n💡 此练习没有提示，试着自己解决吧！" << std::endl;
        return;
    }

    if (current_hint_level_ >= ex->hints.size()) {
        current_hint_level_ = 0; // 重置
    }

    std::cout << "\n💡 提示 " << (current_hint_level_ + 1) << "/" << ex->hints.size() << ":" << std::endl;
    std::cout << "   " << ex->hints[current_hint_level_] << std::endl;

    current_hint_level_++;

    if (current_hint_level_ < ex->hints.size()) {
        std::cout << "\n   (再次运行 'cudalings hint' 查看更多提示)" << std::endl;
    }
}

void Runner::watch_mode() {
    std::cout << "👀 监视模式已启动，等待文件变化..." << std::endl;
    std::cout << "   (按 Ctrl+C 退出)\n" << std::endl;

    std::map<std::string, std::time_t> file_times;

    // 初始化文件修改时间
    for (const auto& ex : manager_.get_all_exercises()) {
        if (fs::exists(ex.file_path)) {
            struct stat st;
            stat(ex.file_path.c_str(), &st);
            file_times[ex.file_path] = st.st_mtime;
        }
    }

    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(2));

        // 检查文件变化
        for (const auto& ex : manager_.get_all_exercises()) {
            if (!fs::exists(ex.file_path)) continue;

            struct stat st;
            stat(ex.file_path.c_str(), &st);

            if (file_times[ex.file_path] != st.st_mtime) {
                file_times[ex.file_path] = st.st_mtime;

                std::cout << "\n📝 检测到 " << ex.file_path << " 变化" << std::endl;
                verify(ex.number);
                std::cout << "\n👀 继续监视..." << std::endl;
            }
        }
    }
}

bool Runner::compile_exercise(const Exercise& ex, std::string& output) {
    // 创建临时构建目录
    std::string build_dir = ".cudalings/build";
    fs::create_directories(build_dir);

    // 编译命令
    std::string exe_path = build_dir + "/test_" + std::to_string(ex.number);
    std::string cmd = "nvcc -o " + exe_path + " " + ex.file_path +
                      " -std=c++14 -arch=sm_60 2>&1";

    // 执行编译
    FILE* pipe = popen(cmd.c_str(), "r");
    if (!pipe) {
        output = "无法执行编译命令";
        return false;
    }

    char buffer[256];
    while (fgets(buffer, sizeof(buffer), pipe)) {
        output += buffer;
    }

    int ret = pclose(pipe);
    return ret == 0;
}

bool Runner::run_tests(const Exercise& ex, std::string& output) {
    std::string exe_path = ".cudalings/build/test_" + std::to_string(ex.number);

    // 运行可执行文件
    std::string cmd = exe_path + " 2>&1";
    FILE* pipe = popen(cmd.c_str(), "r");
    if (!pipe) {
        output = "无法运行测试";
        return false;
    }

    char buffer[256];
    while (fgets(buffer, sizeof(buffer), pipe)) {
        output += buffer;
    }

    int ret = pclose(pipe);

    // 检查退出码和输出
    // 练习应该返回 0 表示成功
    if (ret != 0) {
        return false;
    }

    // 检查是否包含 "FAILED" 或错误信息
    if (output.find("FAILED") != std::string::npos ||
        output.find("ERROR") != std::string::npos) {
        return false;
    }

    return true;
}

void Runner::print_exercise_header(const Exercise& ex) {
    std::cout << "\n" << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;
    std::cout << "📚 练习 " << ex.get_display_name() << std::endl;
    std::cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;
}

void Runner::print_success(const Exercise& ex) {
    std::cout << "\n" << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;
    std::cout << "✅ 成功！练习 " << ex.number << " 已通过所有测试！" << std::endl;
    std::cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" << std::endl;
}

void Runner::print_failure(const std::string& output) {
    std::cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;
    std::cout << output << std::endl;
    std::cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;
}
