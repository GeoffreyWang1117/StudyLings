/*
 * 练习: ds03_stack
 * 难度: Easy
 * 主题: 数据结构 - 栈
 * 描述: 实现栈并应用于括号匹配等问题
 * 参考: ADM 3rd Edition - Chapter 3.2
 */

#include <iostream>
#include <string>
#include <cassert>

template<typename T>
class Stack {
    // TODO: 实现栈
};

// TODO: 使用栈检查括号是否匹配
bool isValidParentheses(const std::string& s) {
    return false;
}

// I AM NOT DONE

void test_basic() {
    assert(isValidParentheses("()") == true);
    assert(isValidParentheses("(]") == false);
    std::cout << "✓ Basic test passed\n";
}

int main() {
    test_basic();
    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
