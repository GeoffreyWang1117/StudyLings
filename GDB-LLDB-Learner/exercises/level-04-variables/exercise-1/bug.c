#include <stdio.h>
#include <string.h>

/*
 * 这个程序有一个 bug：它总是输出 "失败"
 * 你的任务是使用调试器找到问题并修复它
 */

typedef struct {
    char name[50];
    int score;
    int passed;
} Student;

int check_pass(Student *student) {
    // Bug: 应该是 >= 60
    if (student->score > 60) {
        student->passed = 1;
    } else {
        student->passed = 0;
    }
    return student->passed;
}

int main() {
    Student student;
    strcpy(student.name, "张三");
    student.score = 60;  // 刚好及格
    student.passed = 0;

    printf("学生姓名: %s\n", student.name);
    printf("分数: %d\n", student.score);

    check_pass(&student);

    if (student.passed) {
        printf("结果: 通过\n");
    } else {
        printf("结果: 失败\n");  // Bug 会导致这里被执行
    }

    return 0;
}
