#pragma once

#include "exercise.hpp"
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <iostream>
#include <filesystem>

namespace adm_judge {

class ExerciseRunner {
public:
    static Status checkStatus(const std::string& filepath) {
        std::ifstream file(filepath);
        if (!file.is_open()) {
            return Status::NotStarted;
        }

        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string content = buffer.str();

        // 检查是否包含 "I AM NOT DONE" 标记
        if (content.find("I AM NOT DONE") != std::string::npos) {
            return Status::InProgress;
        }

        return Status::Done;
    }

    static bool compile(const std::string& filepath, std::string& error) {
        namespace fs = std::filesystem;

        if (!fs::exists(filepath)) {
            error = "文件不存在: " + filepath;
            return false;
        }

        // 创建临时编译目录
        std::string temp_dir = "/tmp/adm_judge_build";
        fs::create_directories(temp_dir);

        // 提取文件名
        fs::path p(filepath);
        std::string basename = p.stem().string();
        std::string output = temp_dir + "/" + basename;

        // 编译命令
        std::string compile_cmd = "g++ -std=c++17 -Wall -Wextra -I. -o " +
                                 output + " " + filepath + " 2>&1";

        FILE* pipe = popen(compile_cmd.c_str(), "r");
        if (!pipe) {
            error = "无法执行编译命令";
            return false;
        }

        char buffer[256];
        std::string result;
        while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
            result += buffer;
        }

        int return_code = pclose(pipe);

        if (return_code != 0) {
            error = "编译失败:\n" + result;
            return false;
        }

        return true;
    }

    static bool run(const std::string& filepath, std::string& output) {
        namespace fs = std::filesystem;

        // 先编译
        std::string compile_error;
        if (!compile(filepath, compile_error)) {
            output = compile_error;
            return false;
        }

        // 运行可执行文件
        fs::path p(filepath);
        std::string basename = p.stem().string();
        std::string executable = "/tmp/adm_judge_build/" + basename;

        std::string run_cmd = executable + " 2>&1";
        FILE* pipe = popen(run_cmd.c_str(), "r");
        if (!pipe) {
            output = "无法执行程序";
            return false;
        }

        char buffer[256];
        std::string result;
        while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
            result += buffer;
        }

        int return_code = pclose(pipe);
        output = result;

        if (return_code != 0) {
            return false;
        }

        return true;
    }

    static void printExerciseInfo(const Exercise& ex) {
        std::cout << "\n╔══════════════════════════════════════════════════════════════╗\n";
        std::cout << "║  练习: " << ex.name << std::string(52 - ex.name.length(), ' ') << "║\n";
        std::cout << "║  主题: " << ex.topic << std::string(52 - ex.topic.length(), ' ') << "║\n";
        std::cout << "║  难度: " << ex.getDifficultyString()
                  << std::string(52 - ex.getDifficultyString().length(), ' ') << "║\n";
        std::cout << "║  状态: " << ex.getStatusString()
                  << std::string(52 - ex.getStatusString().length(), ' ') << "║\n";
        std::cout << "║  文件: " << ex.path << std::string(52 - ex.path.length(), ' ') << "║\n";
        std::cout << "╚══════════════════════════════════════════════════════════════╝\n\n";
    }
};

} // namespace adm_judge
