#pragma once

#include "exercise.hpp"
#include "runner.hpp"
#include <iostream>
#include <iomanip>
#include <map>

namespace adm_judge {

class ProgressTracker {
public:
    static void updateStatuses(std::vector<Exercise>& exercises) {
        for (auto& ex : exercises) {
            ex.status = ExerciseRunner::checkStatus(ex.path);
        }
    }

    static void printProgress(const std::vector<Exercise>& exercises) {
        int total = exercises.size();
        int done = 0;
        int in_progress = 0;

        std::map<std::string, std::pair<int, int>> topic_stats; // topic -> (total, done)

        for (const auto& ex : exercises) {
            topic_stats[ex.topic].first++;
            if (ex.status == Status::Done) {
                done++;
                topic_stats[ex.topic].second++;
            } else if (ex.status == Status::InProgress) {
                in_progress++;
            }
        }

        std::cout << "\n╔════════════════════════════════════════════════════════════════╗\n";
        std::cout << "║                          学习进度                              ║\n";
        std::cout << "╠════════════════════════════════════════════════════════════════╣\n";

        // 总体进度
        double percentage = (total > 0) ? (100.0 * done / total) : 0.0;
        std::cout << "║  总进度: " << done << "/" << total
                  << " (" << std::fixed << std::setprecision(1) << percentage << "%)"
                  << std::string(43 - std::to_string(done).length() - std::to_string(total).length(), ' ')
                  << "║\n";
        std::cout << "║  进行中: " << in_progress
                  << std::string(52 - std::to_string(in_progress).length(), ' ') << "║\n";

        std::cout << "╠════════════════════════════════════════════════════════════════╣\n";
        std::cout << "║  主题统计                                                      ║\n";
        std::cout << "╠════════════════════════════════════════════════════════════════╣\n";

        for (const auto& [topic, stats] : topic_stats) {
            double topic_pct = (stats.first > 0) ? (100.0 * stats.second / stats.first) : 0.0;
            std::cout << "║  " << std::setw(30) << std::left << topic
                      << std::setw(8) << std::right << (std::to_string(stats.second) + "/" + std::to_string(stats.first))
                      << "  " << std::setw(5) << std::fixed << std::setprecision(1) << topic_pct << "%"
                      << "  ║\n";
        }

        std::cout << "╚════════════════════════════════════════════════════════════════╝\n\n";
    }

    static Exercise* getNextExercise(std::vector<Exercise>& exercises) {
        updateStatuses(exercises);

        // 首先找进行中的练习
        for (auto& ex : exercises) {
            if (ex.status == Status::InProgress) {
                return &ex;
            }
        }

        // 然后找第一个未开始的练习
        for (auto& ex : exercises) {
            if (ex.status == Status::NotStarted) {
                return &ex;
            }
        }

        return nullptr;
    }

    static void listExercises(const std::vector<Exercise>& exercises) {
        std::cout << "\n所有练习:\n";
        std::cout << "────────────────────────────────────────────────────────────────\n";

        std::string current_topic = "";
        for (const auto& ex : exercises) {
            if (ex.topic != current_topic) {
                current_topic = ex.topic;
                std::cout << "\n【" << current_topic << "】\n";
            }

            std::string status_icon;
            switch (ex.status) {
                case Status::Done: status_icon = "✓"; break;
                case Status::InProgress: status_icon = "●"; break;
                case Status::NotStarted: status_icon = "○"; break;
            }

            std::cout << "  " << status_icon << " "
                      << std::setw(15) << std::left << ex.name
                      << std::setw(10) << ex.getDifficultyString()
                      << " - " << ex.path << "\n";
        }
        std::cout << "\n";
    }
};

} // namespace adm_judge
