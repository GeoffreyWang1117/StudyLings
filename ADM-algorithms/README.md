# ADM Judge - Algorithm Design Manual 练习系统

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![C++17](https://img.shields.io/badge/C++-17-blue.svg)](https://isocpp.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

基于 Steve S. Skiena 的《The Algorithm Design Manual (3rd Edition)》的 C++ 算法练习判题系统，灵感来自 rustlings。

> **58 个精心设计的练习，覆盖 ADM 第三版所有核心主题** 📚

## ⚡ 快速开始

```bash
# 克隆仓库
git clone https://github.com/GeoffreyWang1117/ADM-algorithms.git
cd ADM-algorithms

# 一键安装
bash tools/install.sh

# 或使用 make
make

# 开始第一个练习！
cd build && ./adm-judge
```

📖 **详细指南**: [QUICKSTART.md](QUICKSTART.md) | **完整教程**: [docs/TUTORIAL.md](docs/TUTORIAL.md)

## 🎯 项目特点

- 📚 覆盖 ADM 第三版所有核心主题
- 🔄 交互式学习体验
- ✅ 自动编译和测试
- 📊 进度追踪
- 🎓 从基础到高级的渐进式学习路径

## 📖 涵盖主题

### 基础篇
1. **算法分析** (Algorithm Analysis)
   - 时间复杂度分析
   - 空间复杂度分析
   - 渐进符号 (Big-O, Theta, Omega)

2. **数据结构** (Data Structures)
   - 数组和链表
   - 栈和队列
   - 树 (二叉树、BST、AVL、红黑树)
   - 堆和优先队列
   - 哈希表
   - 并查集 (Union-Find)

3. **排序与搜索** (Sorting and Searching)
   - 快速排序、归并排序、堆排序
   - 二分搜索
   - 选择算法

### 图算法篇
4. **图遍历** (Graph Traversal)
   - BFS (广度优先搜索)
   - DFS (深度优先搜索)
   - 连通性
   - 拓扑排序

5. **加权图算法** (Weighted Graph Algorithms)
   - 最短路径 (Dijkstra, Bellman-Ford, Floyd-Warshall)
   - 最小生成树 (Prim, Kruskal)
   - 网络流 (Maximum Flow)

### 高级算法篇
6. **组合搜索** (Combinatorial Search)
   - 回溯法
   - 剪枝技术
   - 分支定界

7. **动态规划** (Dynamic Programming)
   - 记忆化搜索
   - 最长公共子序列
   - 背包问题
   - 矩阵链乘法
   - 最优二叉搜索树

8. **贪心算法** (Greedy Algorithms)
   - 区间调度
   - 霍夫曼编码
   - 最小化延迟

9. **字符串算法** (String Algorithms)
   - 字符串匹配 (KMP, Rabin-Karp)
   - 字典树 (Trie)
   - 后缀数组

10. **计算几何** (Computational Geometry)
    - 凸包
    - 线段相交
    - 最近点对

11. **NP完全问题** (NP-Complete Problems)
    - SAT、背包、旅行商问题
    - 近似算法
    - 启发式方法

## 🚀 快速开始

### 环境要求

- C++17 或更高版本
- CMake 3.15+
- GCC/Clang 编译器

### 安装

```bash
git clone https://github.com/GeoffreyWang1117/ADM-algorithms.git
cd ADM-algorithms
mkdir build && cd build
cmake ..
make
```

### 运行判题系统

```bash
# 运行判题系统
./adm-judge

# 监视模式（自动检测文件变化）
./adm-judge watch

# 验证特定练习
./adm-judge run <exercise-name>

# 查看提示
./adm-judge hint <exercise-name>

# 查看进度
./adm-judge progress
```

## 📝 使用方法

1. **开始练习**
   ```bash
   ./adm-judge
   ```
   系统会显示下一个需要完成的练习

2. **编辑代码**
   - 打开 `exercises/` 目录下对应的 `.cpp` 文件
   - 找到 `// TODO:` 注释，完成代码
   - 不要修改测试代码

3. **验证答案**
   ```bash
   ./adm-judge run <exercise-name>
   ```
   或在 watch 模式下保存文件自动验证

4. **获取帮助**
   - 每个练习文件都包含说明和提示
   - 使用 `./adm-judge hint <name>` 获取额外提示
   - 参考 `solutions/` 目录（仅在完成练习后）

## 📂 项目结构

```
ADM-algorithms/
├── exercises/           # 所有练习题
│   ├── 01_analysis/    # 算法分析
│   ├── 02_data_structures/  # 数据结构
│   ├── 03_sorting/     # 排序与搜索
│   ├── 04_graph_traversal/  # 图遍历
│   ├── 05_weighted_graphs/  # 加权图
│   ├── 06_combinatorial/    # 组合搜索
│   ├── 07_dynamic_programming/  # 动态规划
│   ├── 08_greedy/      # 贪心算法
│   ├── 09_strings/     # 字符串算法
│   ├── 10_geometry/    # 计算几何
│   └── 11_np_complete/ # NP完全问题
├── judge/              # 判题系统核心
│   ├── main.cpp
│   ├── runner.hpp
│   ├── parser.hpp
│   └── progress.hpp
├── solutions/          # 参考答案（可选）
├── tests/              # 测试用例
├── tools/              # 辅助工具
├── CMakeLists.txt
└── README.md
```

## 🎓 学习路径建议

1. **初学者** (Beginner)
   - 从算法分析开始
   - 掌握基本数据结构
   - 完成排序和搜索练习

2. **中级** (Intermediate)
   - 深入图算法
   - 学习动态规划
   - 掌握贪心策略

3. **高级** (Advanced)
   - 字符串算法
   - 计算几何
   - NP完全问题和近似算法

## 💡 练习格式

每个练习都包含：

```cpp
/*
 * 练习名称: two_sum
 * 难度: Easy
 * 主题: 数据结构 - 哈希表
 *
 * 描述:
 * 给定一个整数数组和目标值，找出数组中和为目标值的两个数的索引。
 *
 * 示例:
 * 输入: nums = [2,7,11,15], target = 9
 * 输出: [0,1]
 *
 * 提示:
 * - 使用哈希表可以将时间复杂度降到 O(n)
 * - 边遍历边存储已访问的元素
 */

#include <vector>
#include <unordered_map>

// TODO: 实现这个函数
std::vector<int> twoSum(std::vector<int>& nums, int target) {
    // 你的代码
}

// I AM NOT DONE

// ===== 测试代码 =====
#include <cassert>

void test_two_sum() {
    std::vector<int> nums1 = {2, 7, 11, 15};
    auto result1 = twoSum(nums1, 9);
    assert(result1.size() == 2);
    assert((result1[0] == 0 && result1[1] == 1) ||
           (result1[0] == 1 && result1[1] == 0));

    // 更多测试...
}
```

当你完成练习后，删除 `// I AM NOT DONE` 这一行。

## 🤝 贡献

欢迎贡献！请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📚 参考资料

- [The Algorithm Design Manual (3rd Edition)](https://www.algorist.com/) by Steven S. Skiena
- [算法设计手册官方网站](https://www3.cs.stonybrook.edu/~skiena/algorist/)

## 📄 许可证

MIT License

## 🙏 致谢

- Steven S. Skiena 的《Algorithm Design Manual》
- Rustlings 项目提供的灵感
