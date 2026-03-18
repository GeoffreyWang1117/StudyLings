/*
 * 练习: dp03_knapsack
 * 难度: Medium
 * 主题: 动态规划 - 0/1 背包问题
 *
 * 描述:
 * 实现经典的 0/1 背包问题，这是动态规划的核心应用之一。
 *
 * 问题描述:
 * 给定 n 个物品，每个物品有重量 w[i] 和价值 v[i]。
 * 有一个容量为 W 的背包，求能装入背包的物品的最大价值。
 * 每个物品只能选择装或不装（不能分割）。
 *
 * 学习目标:
 * - 掌握二维 DP 问题的建模
 * - 理解状态转移方程
 * - 学习空间优化技巧
 *
 * 参考: ADM 3rd Edition - Chapter 8.10
 */

#include <iostream>
#include <vector>
#include <cassert>
#include <algorithm>

// TODO: 实现 0/1 背包问题
// weights: 物品重量数组
// values:  物品价值数组
// W:       背包容量
// 返回: 最大价值
int knapsack(const std::vector<int>& weights, const std::vector<int>& values, int W) {
    int n = weights.size();
    // 你的代码
    // 提示: 使用二维 DP 数组
    // dp[i][w] = 前 i 个物品，背包容量为 w 时的最大价值
    // 状态转移:
    //   如果 weights[i-1] > w: dp[i][w] = dp[i-1][w] (装不下)
    //   否则: dp[i][w] = max(dp[i-1][w], dp[i-1][w-weights[i-1]] + values[i-1])
    return 0;
}

// TODO: 实现空间优化的版本（一维 DP）
int knapsack_optimized(const std::vector<int>& weights, const std::vector<int>& values, int W) {
    // 你的代码
    // 提示: 只需要一维数组，但要从后向前更新
    return 0;
}

// TODO: 实现返回选择的物品
std::vector<int> knapsack_items(const std::vector<int>& weights,
                                 const std::vector<int>& values, int W) {
    // 你的代码
    // 提示: 需要保存完整的 DP 表，然后回溯找出选择的物品
    return {};
}

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic() {
    std::vector<int> weights = {2, 1, 3, 2};
    std::vector<int> values = {12, 10, 20, 15};
    int W = 5;

    // 最优解: 选择物品 1 (w=1, v=10) 和物品 2 (w=3, v=20) 和物品 3 (w=2, v=15)
    // 但是 1+3+2=6 > 5，所以实际是选择物品 2 和 3: v=20+15=35
    // 或者 1+2: 10+20=30, 或者 0+2+3: 12+20=15... 需要重新计算
    // 正确答案: 选 items 0,3 (w=2+2=4, v=12+15=27) 或 items 1,2 (w=1+3=4, v=10+20=30)
    // 最优是 items 1,2: value=30 或者items 0,1,3 (w=2+1+2=5, v=12+10+15=37)

    int result = knapsack(weights, values, W);
    assert(result == 37);

    result = knapsack_optimized(weights, values, W);
    assert(result == 37);

    std::cout << "✓ Basic test passed\n";
}

void test_no_items_fit() {
    std::vector<int> weights = {10, 20, 30};
    std::vector<int> values = {100, 200, 300};
    int W = 5;

    int result = knapsack(weights, values, W);
    assert(result == 0);

    std::cout << "✓ No items fit test passed\n";
}

void test_all_items_fit() {
    std::vector<int> weights = {1, 2, 3};
    std::vector<int> values = {10, 20, 30};
    int W = 10;

    int result = knapsack(weights, values, W);
    assert(result == 60); // 所有物品都能装下

    std::cout << "✓ All items fit test passed\n";
}

void test_classic_example() {
    std::vector<int> weights = {10, 20, 30};
    std::vector<int> values = {60, 100, 120};
    int W = 50;

    int result = knapsack(weights, values, W);
    assert(result == 220); // 选择物品 1 和 2: 20+30=50, 100+120=220

    std::cout << "✓ Classic example test passed\n";
}

void test_items_selection() {
    std::vector<int> weights = {10, 20, 30};
    std::vector<int> values = {60, 100, 120};
    int W = 50;

    auto items = knapsack_items(weights, values, W);

    int total_weight = 0;
    int total_value = 0;
    for (int idx : items) {
        total_weight += weights[idx];
        total_value += values[idx];
    }

    assert(total_weight <= W);
    assert(total_value == 220);

    std::cout << "✓ Items selection test passed\n";
}

int main() {
    std::cout << "Running Knapsack DP Tests...\n";
    std::cout << "============================\n";

    test_basic();
    test_no_items_fit();
    test_all_items_fit();
    test_classic_example();
    test_items_selection();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 背包问题分析:\n";
    std::cout << "   - 时间复杂度: O(nW)\n";
    std::cout << "   - 空间复杂度: O(nW) 或 O(W) (优化版)\n";
    std::cout << "   - 这是伪多项式时间算法\n";
    std::cout << "   - 背包问题是 NP-Complete\n";

    return 0;
}
