#include <iostream>
#include <string>
#include <vector>
#include "exercise_manager.h"
#include "runner.h"
#include "progress.h"

void print_usage() {
    std::cout << R"(
CUDAlings - CUDA C++ Learning System

用法:
  cudalings <命令> [选项]

命令:
  list              列出所有练习
  run [N]           运行第 N 个练习（不指定则运行下一个未完成的）
  verify [N]        验证第 N 个练习（不指定则验证当前）
  hint [N]          显示第 N 个练习的提示
  progress          显示学习进度
  watch             监视模式：自动检测文件变化并验证
  reset [N]         重置第 N 个练习（恢复初始状态）
  solution [N]      查看参考答案（谨慎使用）
  help              显示此帮助信息

示例:
  cudalings run              # 运行下一个练习
  cudalings verify 5         # 验证第 5 个练习
  cudalings watch            # 启动监视模式

)" << std::endl;
}

void print_welcome() {
    std::cout << R"(
╔═══════════════════════════════════════════════════╗
║                                                   ║
║      🚀 欢迎来到 CUDA C++ 学习系统！              ║
║                                                   ║
║   通过实践练习掌握 GPU 并行编程                    ║
║                                                   ║
╚═══════════════════════════════════════════════════╝

)" << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_welcome();
        print_usage();
        return 0;
    }

    std::string command = argv[1];

    // 初始化系统
    ExerciseManager manager;
    if (!manager.initialize()) {
        std::cerr << "❌ 错误: 无法初始化练习管理器" << std::endl;
        return 1;
    }

    ProgressTracker progress;
    Runner runner(manager, progress);

    try {
        if (command == "list") {
            manager.list_exercises();
        }
        else if (command == "run") {
            int exercise_num = -1;
            if (argc > 2) {
                exercise_num = std::stoi(argv[2]);
            }
            runner.run(exercise_num);
        }
        else if (command == "verify") {
            int exercise_num = -1;
            if (argc > 2) {
                exercise_num = std::stoi(argv[2]);
            }
            runner.verify(exercise_num);
        }
        else if (command == "hint") {
            int exercise_num = -1;
            if (argc > 2) {
                exercise_num = std::stoi(argv[2]);
            }
            runner.show_hint(exercise_num);
        }
        else if (command == "progress") {
            progress.show();
        }
        else if (command == "watch") {
            runner.watch_mode();
        }
        else if (command == "reset") {
            if (argc < 3) {
                std::cerr << "❌ 错误: 请指定要重置的练习编号" << std::endl;
                return 1;
            }
            int exercise_num = std::stoi(argv[2]);
            manager.reset_exercise(exercise_num);
        }
        else if (command == "solution") {
            if (argc < 3) {
                std::cerr << "❌ 错误: 请指定要查看答案的练习编号" << std::endl;
                return 1;
            }
            int exercise_num = std::stoi(argv[2]);
            manager.show_solution(exercise_num);
        }
        else if (command == "help") {
            print_usage();
        }
        else {
            std::cerr << "❌ 未知命令: " << command << std::endl;
            print_usage();
            return 1;
        }
    }
    catch (const std::exception& e) {
        std::cerr << "❌ 错误: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
