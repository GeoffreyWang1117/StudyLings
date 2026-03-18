#include "progress.h"
#include <iostream>
#include <fstream>
#include <filesystem>
#include <cstdlib>

namespace fs = std::filesystem;

ProgressTracker::ProgressTracker() {
    progress_file_ = get_progress_dir() + "/progress.txt";
    ensure_progress_dir();
    load();
}

std::string ProgressTracker::get_progress_dir() const {
    // 在用户主目录或当前目录创建 .cudalings 目录
    const char* home = std::getenv("HOME");
    if (home) {
        return std::string(home) + "/.cudalings";
    }
    return ".cudalings";
}

void ProgressTracker::ensure_progress_dir() {
    std::string dir = get_progress_dir();
    if (!fs::exists(dir)) {
        fs::create_directories(dir);
    }
}

bool ProgressTracker::load() {
    std::ifstream file(progress_file_);
    if (!file.is_open()) {
        // 文件不存在是正常的（首次运行）
        return true;
    }

    completed_exercises_.clear();
    int exercise_num;
    while (file >> exercise_num) {
        completed_exercises_.insert(exercise_num);
    }

    return true;
}

bool ProgressTracker::save() {
    std::ofstream file(progress_file_);
    if (!file.is_open()) {
        std::cerr << "⚠️  警告: 无法保存进度到 " << progress_file_ << std::endl;
        return false;
    }

    for (int num : completed_exercises_) {
        file << num << "\n";
    }

    return true;
}

void ProgressTracker::mark_completed(int exercise_number) {
    completed_exercises_.insert(exercise_number);
    save();
}

bool ProgressTracker::is_completed(int exercise_number) const {
    return completed_exercises_.find(exercise_number) != completed_exercises_.end();
}

int ProgressTracker::get_completed_count() const {
    return completed_exercises_.size();
}

void ProgressTracker::show() const {
    std::cout << "\n📊 学习进度统计\n" << std::endl;
    std::cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;

    int total = 100; // 总共约 100 个练习
    int completed = completed_exercises_.size();
    int percentage = (completed * 100) / total;

    std::cout << "已完成: " << completed << " / " << total << " (" << percentage << "%)" << std::endl;

    // 显示进度条
    std::cout << "\n[";
    int bar_width = 40;
    int filled = (completed * bar_width) / total;
    for (int i = 0; i < bar_width; ++i) {
        if (i < filled) {
            std::cout << "█";
        } else {
            std::cout << "░";
        }
    }
    std::cout << "] " << percentage << "%" << std::endl;

    std::cout << "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;

    if (completed == total) {
        std::cout << "\n🎉 恭喜！你已完成所有练习！" << std::endl;
    } else {
        std::cout << "\n💪 继续加油！还有 " << (total - completed) << " 个练习等待你完成。" << std::endl;
    }
}
