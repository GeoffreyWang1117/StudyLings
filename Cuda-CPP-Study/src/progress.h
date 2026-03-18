#ifndef PROGRESS_H
#define PROGRESS_H

#include <set>
#include <string>

class ProgressTracker {
public:
    ProgressTracker();

    // 加载和保存进度
    bool load();
    bool save();

    // 进度操作
    void mark_completed(int exercise_number);
    bool is_completed(int exercise_number) const;
    int get_completed_count() const;

    // 显示进度
    void show() const;

private:
    std::set<int> completed_exercises_;
    std::string progress_file_;

    std::string get_progress_dir() const;
    void ensure_progress_dir();
};

#endif // PROGRESS_H
