#include "exercise.hpp"
#include "runner.hpp"
#include "progress.hpp"
#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <filesystem>
#include <map>
#include <sys/inotify.h>
#include <unistd.h>

using namespace adm_judge;

void printHelp() {
    std::cout << R"(
ADM Judge - Algorithm Design Manual 练习系统

用法:
    adm-judge                    运行下一个练习
    adm-judge watch              监视模式（自动检测文件变化）
    adm-judge run <name>         运行指定练习
    adm-judge verify <name>      验证指定练习
    adm-judge list               列出所有练习
    adm-judge progress           查看学习进度
    adm-judge hint <name>        查看练习提示
    adm-judge reset <name>       重置练习（删除进度标记）
    adm-judge help               显示此帮助信息

示例:
    adm-judge                    # 开始下一个练习
    adm-judge watch              # 启动监视模式
    adm-judge run ds01           # 运行 ds01 练习
    adm-judge progress           # 查看进度
)";
}

void printHint(const std::string& name) {
    auto exercises = getAllExercises();
    for (const auto& ex : exercises) {
        if (ex.name == name) {
            std::cout << "\n💡 提示:\n";
            std::cout << "────────────────────────────────────────────────────────────────\n";
            std::cout << "1. 仔细阅读练习文件中的注释和说明\n";
            std::cout << "2. 理解问题的时间和空间复杂度要求\n";
            std::cout << "3. 可以参考《Algorithm Design Manual》相关章节\n";
            std::cout << "4. 完成代码后，删除 '// I AM NOT DONE' 这一行\n";
            std::cout << "5. 保存文件后运行: adm-judge verify " << name << "\n\n";
            std::cout << "文件位置: " << ex.path << "\n\n";
            return;
        }
    }
    std::cout << "❌ 找不到练习: " << name << "\n";
}

bool verifyExercise(Exercise& ex) {
    ExerciseRunner::printExerciseInfo(ex);

    // 检查状态
    ex.status = ExerciseRunner::checkStatus(ex.path);

    if (ex.status == Status::NotStarted) {
        std::cout << "⚠️  此练习尚未开始。请编辑文件:\n";
        std::cout << "   " << ex.path << "\n\n";
        return false;
    }

    if (ex.status == Status::InProgress) {
        std::cout << "⚠️  请完成练习并删除 '// I AM NOT DONE' 标记\n\n";
        return false;
    }

    // 编译并运行
    std::cout << "🔨 正在编译...\n";
    std::string output;
    if (!ExerciseRunner::run(ex.path, output)) {
        std::cout << "\n❌ 测试失败!\n\n";
        std::cout << output << "\n";
        return false;
    }

    std::cout << "\n✅ 测试通过! 做得好！\n\n";
    if (!output.empty()) {
        std::cout << "输出:\n" << output << "\n";
    }
    return true;
}

void runNext() {
    auto exercises = getAllExercises();
    Exercise* next = ProgressTracker::getNextExercise(exercises);

    if (next == nullptr) {
        std::cout << "\n🎉 恭喜！你已经完成了所有练习！\n\n";
        ProgressTracker::printProgress(exercises);
        return;
    }

    ExerciseRunner::printExerciseInfo(*next);

    if (next->status == Status::NotStarted) {
        std::cout << "📝 开始这个练习:\n";
        std::cout << "   编辑文件: " << next->path << "\n";
        std::cout << "   完成后运行: adm-judge verify " << next->name << "\n\n";
    } else if (next->status == Status::InProgress) {
        std::cout << "⏳ 继续完成这个练习:\n";
        std::cout << "   编辑文件: " << next->path << "\n";
        std::cout << "   完成后删除 '// I AM NOT DONE' 并运行: adm-judge verify " << next->name << "\n\n";
    }
}

void watchMode() {
    std::cout << "👀 监视模式已启动...\n";
    std::cout << "   修改练习文件后会自动验证\n";
    std::cout << "   按 Ctrl+C 退出\n\n";

    auto exercises = getAllExercises();
    std::map<std::string, time_t> lastModified;

    // 初始化最后修改时间
    for (const auto& ex : exercises) {
        if (std::filesystem::exists(ex.path)) {
            lastModified[ex.path] = std::filesystem::last_write_time(ex.path).time_since_epoch().count();
        }
    }

    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(2));

        for (auto& ex : exercises) {
            if (!std::filesystem::exists(ex.path)) {
                continue;
            }

            auto currentTime = std::filesystem::last_write_time(ex.path).time_since_epoch().count();

            if (lastModified[ex.path] != currentTime) {
                lastModified[ex.path] = currentTime;

                std::cout << "\n📝 检测到文件变化: " << ex.path << "\n";

                // 自动验证
                Status oldStatus = ex.status;
                ex.status = ExerciseRunner::checkStatus(ex.path);

                if (ex.status == Status::Done && oldStatus != Status::Done) {
                    std::cout << "🎯 检测到完成标记，开始验证...\n";
                    verifyExercise(ex);
                }
            }
        }
    }
}

int main(int argc, char* argv[]) {
    std::cout << "╔════════════════════════════════════════════════════════════════╗\n";
    std::cout << "║      ADM Judge - Algorithm Design Manual 练习系统             ║\n";
    std::cout << "║              基于《算法设计手册》第三版                         ║\n";
    std::cout << "╚════════════════════════════════════════════════════════════════╝\n";

    if (argc < 2) {
        runNext();
        return 0;
    }

    std::string command = argv[1];

    if (command == "help" || command == "-h" || command == "--help") {
        printHelp();
    }
    else if (command == "list") {
        auto exercises = getAllExercises();
        ProgressTracker::updateStatuses(exercises);
        ProgressTracker::listExercises(exercises);
    }
    else if (command == "progress") {
        auto exercises = getAllExercises();
        ProgressTracker::updateStatuses(exercises);
        ProgressTracker::printProgress(exercises);
    }
    else if (command == "watch") {
        watchMode();
    }
    else if (command == "run" || command == "verify") {
        if (argc < 3) {
            std::cout << "❌ 请指定练习名称\n";
            std::cout << "   用法: adm-judge " << command << " <name>\n";
            return 1;
        }

        std::string name = argv[2];
        auto exercises = getAllExercises();

        bool found = false;
        for (auto& ex : exercises) {
            if (ex.name == name) {
                verifyExercise(ex);
                found = true;
                break;
            }
        }

        if (!found) {
            std::cout << "❌ 找不到练习: " << name << "\n";
            std::cout << "   运行 'adm-judge list' 查看所有练习\n";
            return 1;
        }
    }
    else if (command == "hint") {
        if (argc < 3) {
            std::cout << "❌ 请指定练习名称\n";
            std::cout << "   用法: adm-judge hint <name>\n";
            return 1;
        }
        printHint(argv[2]);
    }
    else {
        std::cout << "❌ 未知命令: " << command << "\n";
        printHelp();
        return 1;
    }

    return 0;
}
