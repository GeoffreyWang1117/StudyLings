# ADM Judge 快速开始指南

欢迎使用 ADM Judge！这份指南将帮助您快速上手。

## 🎯 5分钟快速开始

### 步骤 1: 克隆并构建

```bash
# 克隆仓库
git clone https://github.com/GeoffreyWang1117/ADM-algorithms.git
cd ADM-algorithms

# 构建判题系统
mkdir build && cd build
cmake ..
make

# 运行判题系统
./adm-judge
```

### 步骤 2: 开始第一个练习

系统会显示：

```
╔══════════════════════════════════════════════════════════════╗
║  练习: intro01
║  主题: Algorithm Analysis
║  难度: Easy
║  状态: Not Started
║  文件: exercises/01_analysis/intro01_runtime.cpp
╚══════════════════════════════════════════════════════════════╝

📝 开始这个练习:
   编辑文件: exercises/01_analysis/intro01_runtime.cpp
   完成后运行: adm-judge verify intro01
```

### 步骤 3: 编辑练习文件

打开 `exercises/01_analysis/intro01_runtime.cpp`：

```cpp
// 找到 TODO 标记
long long countOperations_Linear(int n) {
    // 你的代码: 实现一个 O(n) 的函数
    // 返回基本操作执行的次数
    return 0; // 替换这一行
}
```

实现函数：

```cpp
long long countOperations_Linear(int n) {
    long long count = 0;
    for (int i = 0; i < n; i++) {
        count++;  // 基本操作
    }
    return count;
}
```

### 步骤 4: 完成练习

1. **删除 "I AM NOT DONE" 标记**：找到文件中的这一行并删除它
2. **保存文件**
3. **验证答案**：

```bash
./adm-judge verify intro01
```

如果成功，你会看到：

```
✅ 测试通过! 做得好！
```

### 步骤 5: 查看进度

```bash
./adm-judge progress
```

## 🔄 工作流程

### 方式 1: 手动模式（推荐新手）

```bash
# 1. 查看下一个练习
./adm-judge

# 2. 编辑文件
vim exercises/01_analysis/intro01_runtime.cpp

# 3. 验证
./adm-judge verify intro01

# 4. 重复
```

### 方式 2: 监视模式（推荐熟练用户）

```bash
# 启动监视模式
./adm-judge watch

# 在另一个终端编辑文件
# 保存后自动验证
```

## 📚 练习类型说明

### Easy 难度
- 适合初学者
- 基础数据结构和算法
- 通常 10-30 行代码

### Medium 难度
- 需要理解算法原理
- 可能需要多个函数配合
- 通常 30-100 行代码

### Hard 难度
- 复杂算法实现
- 需要深入理解
- 可能需要 100+ 行代码

## 💡 学习建议

### 第一周：基础篇
```bash
# 算法分析
./adm-judge run intro01
./adm-judge run intro02

# 基础数据结构
./adm-judge run ds01
./adm-judge run ds02
./adm-judge run ds03
```

### 第二周：排序和搜索
```bash
./adm-judge run sort01
./adm-judge run sort02
./adm-judge run sort05
```

### 第三周：图算法
```bash
./adm-judge run graph02  # BFS
./adm-judge run graph03  # DFS
```

### 第四周及以后：高级主题
- 动态规划
- 图算法进阶
- NP完全问题

## 🆘 遇到困难？

### 获取提示

```bash
./adm-judge hint intro01
```

### 查看所有练习

```bash
./adm-judge list
```

### 检查进度

```bash
./adm-judge progress
```

### 跳过某个练习

你可以按任意顺序完成练习：

```bash
./adm-judge run ds05  # 跳到二叉树练习
```

## 🎓 学习资源

1. **教材参考**：
   - The Algorithm Design Manual (3rd Edition) by Steven S. Skiena
   - 每个练习都标注了对应的章节

2. **在线资源**：
   - [算法设计手册官网](https://www.algorist.com/)
   - [作者的视频讲座](https://www3.cs.stonybrook.edu/~skiena/373/)

3. **练习提示**：
   - 每个文件都包含详细的注释
   - 使用 `adm-judge hint <name>` 获取额外提示

## 🐛 常见问题

### Q: 编译失败怎么办？

A: 检查：
1. 是否使用了 C++17 特性
2. 是否包含了必要的头文件
3. 语法是否正确

### Q: 测试失败但我觉得代码是对的？

A:
1. 检查边界情况
2. 检查返回值类型
3. 重新阅读题目要求

### Q: 可以修改测试代码吗？

A: 不建议。测试代码是验证你实现的标准。

### Q: 如何重置练习？

A: 如果你想重新开始某个练习，只需添加回 `// I AM NOT DONE` 标记。

## ✅ 完成清单

- [ ] 完成所有 Algorithm Analysis 练习
- [ ] 完成所有 Data Structures 练习
- [ ] 完成所有 Sorting 练习
- [ ] 完成所有 Graph Traversal 练习
- [ ] 完成所有 Weighted Graphs 练习
- [ ] 完成所有 Dynamic Programming 练习
- [ ] 完成所有其他高级主题练习

## 🎉 下一步

完成所有练习后，你可以：

1. 优化你的解答以提高性能
2. 尝试不同的实现方法
3. 查看参考解答 (`solutions/` 目录)
4. 为项目贡献新的练习

祝学习愉快！记住：**坚持练习，算法会越来越简单！** 💪
