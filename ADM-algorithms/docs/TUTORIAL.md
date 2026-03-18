# ADM Judge 完整教程

本教程将带您一步步完成第一个练习，并深入理解判题系统的使用方法。

## 📚 目录

1. [环境准备](#环境准备)
2. [第一个练习](#第一个练习)
3. [理解练习结构](#理解练习结构)
4. [调试技巧](#调试技巧)
5. [进阶技巧](#进阶技巧)

---

## 环境准备

### 1. 安装依赖

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install g++ cmake make
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install gcc-c++ cmake make
```

**macOS:**
```bash
# 安装 Xcode Command Line Tools
xcode-select --install

# 安装 CMake (使用 Homebrew)
brew install cmake
```

### 2. 克隆并构建

```bash
# 克隆仓库
git clone https://github.com/GeoffreyWang1117/ADM-algorithms.git
cd ADM-algorithms

# 使用安装脚本（推荐）
bash tools/install.sh

# 或手动构建
mkdir build && cd build
cmake ..
make
```

### 3. 验证安装

```bash
cd build
./adm-judge help
```

如果看到帮助信息，说明安装成功！

---

## 第一个练习

让我们完成第一个练习：`intro01` - 运行时间分析

### 步骤 1: 查看练习

```bash
./adm-judge
```

你会看到：

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

### 步骤 2: 查看练习文件

打开 `exercises/01_analysis/intro01_runtime.cpp`：

```cpp
/*
 * 练习: intro01_runtime
 * 难度: Easy
 * 主题: 算法分析 - 运行时间分析
 *
 * 描述:
 * 分析以下几个函数的时间复杂度，并实现一个计数器来验证。
 * 这个练习帮助你理解如何分析算法的运行时间。
 *
 * 学习目标:
 * - 理解基本操作的计数
 * - 识别循环的迭代次数
 * - 计算算法的时间复杂度
 *
 * 参考: ADM 3rd Edition - Chapter 2
 */

#include <iostream>
#include <cassert>

// TODO: 分析这个函数的时间复杂度并实现它
long long countOperations_Linear(int n) {
    // 你的代码: 实现一个 O(n) 的函数
    return 0; // 替换这一行
}

// ... 更多函数

// I AM NOT DONE
```

### 步骤 3: 实现函数

理解题目要求后，实现 `countOperations_Linear` 函数：

```cpp
long long countOperations_Linear(int n) {
    long long count = 0;
    for (int i = 0; i < n; i++) {
        count++;  // 计数基本操作
    }
    return count;
}
```

**思路分析：**
- 我们需要一个 O(n) 的函数
- 最简单的方法就是一个循环执行 n 次
- 每次循环计数一次，最终返回总次数

### 步骤 4: 实现其他函数

继续实现 `countOperations_Quadratic`：

```cpp
long long countOperations_Quadratic(int n) {
    long long count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            count++;  // 嵌套循环，O(n²)
        }
    }
    return count;
}
```

实现 `countOperations_Logarithmic`：

```cpp
long long countOperations_Logarithmic(int n) {
    long long count = 0;
    while (n > 0) {
        count++;
        n /= 2;  // 每次减半，O(log n)
    }
    return count;
}
```

### 步骤 5: 删除 "I AM NOT DONE" 标记

找到文件中的这一行并删除它：

```cpp
// I AM NOT DONE  <-- 删除这一行
```

这告诉判题系统你已经完成了练习。

### 步骤 6: 保存并验证

保存文件后运行：

```bash
./adm-judge verify intro01
```

你会看到：

```
🔨 正在编译...

✅ 测试通过! 做得好！

Running Algorithm Analysis Tests...
====================================
✓ Linear time complexity test passed
✓ Quadratic time complexity test passed
✓ Logarithmic time complexity test passed

✅ All tests passed!
```

### 步骤 7: 查看进度

```bash
./adm-judge progress
```

你会看到你的进度更新了：

```
总进度: 1/58 (1.7%)
进行中: 0

主题统计:
Algorithm Analysis      1/3    33.3%
...
```

---

## 理解练习结构

每个练习文件都包含以下部分：

### 1. 头部注释

```cpp
/*
 * 练习: intro01_runtime
 * 难度: Easy
 * 主题: Algorithm Analysis
 * 描述: ...
 * 学习目标: ...
 * 参考: ADM 3rd Edition - Chapter 2
 */
```

这部分提供了：
- 练习名称和难度
- 主题分类
- 详细描述
- 学习目标
- 教材参考章节

### 2. TODO 部分

```cpp
// TODO: 实现这个函数
int yourFunction() {
    // 你的代码
    return 0;
}
```

这是你需要实现的代码。

### 3. I AM NOT DONE 标记

```cpp
// I AM NOT DONE
```

- 有这行：练习未完成，测试不会运行
- 删除这行：标记练习完成，可以测试

### 4. 测试代码

```cpp
// ===== 测试代码 =====

void test_basic() {
    assert(yourFunction() == expected);
    std::cout << "✓ Basic test passed\n";
}
```

测试代码验证你的实现是否正确。**不要修改测试代码！**

---

## 调试技巧

### 技巧 1: 添加调试输出

在你的代码中添加 `std::cout` 语句：

```cpp
long long countOperations_Linear(int n) {
    long long count = 0;
    std::cout << "Debug: n = " << n << std::endl;
    for (int i = 0; i < n; i++) {
        count++;
    }
    std::cout << "Debug: count = " << count << std::endl;
    return count;
}
```

### 技巧 2: 手动编译测试

```bash
# 进入项目根目录
cd /path/to/ADM-algorithms

# 手动编译
g++ -std=c++17 -Wall -Wextra -I. -o test exercises/01_analysis/intro01_runtime.cpp

# 运行
./test
```

### 技巧 3: 使用 GDB 调试器

```bash
# 编译时添加调试符号
g++ -std=c++17 -g -o test exercises/01_analysis/intro01_runtime.cpp

# 使用 gdb
gdb ./test

# 在 gdb 中:
(gdb) break main          # 在 main 设置断点
(gdb) run                 # 运行程序
(gdb) next                # 单步执行
(gdb) print count         # 查看变量值
(gdb) continue            # 继续执行
```

### 技巧 4: 检查编译警告

```bash
g++ -std=c++17 -Wall -Wextra -Wpedantic -o test yourfile.cpp
```

编译器警告通常能发现潜在问题。

---

## 进阶技巧

### 1. 使用监视模式

监视模式会自动检测文件变化并验证：

```bash
# 在一个终端启动监视模式
./adm-judge watch

# 在另一个终端编辑代码
# 每次保存后自动验证
```

### 2. 跳过练习

你不必按顺序完成练习：

```bash
# 列出所有练习
./adm-judge list

# 直接做某个练习
./adm-judge run dp01  # 跳到动态规划练习
```

### 3. 查看提示

卡住了？查看提示：

```bash
./adm-judge hint intro01
```

### 4. 对比多种实现

尝试用不同方法解决同一问题：

```cpp
// 方法1: 迭代
int fibonacci_iterative(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        int tmp = a + b;
        a = b;
        b = tmp;
    }
    return b;
}

// 方法2: 递归（供对比）
int fibonacci_recursive(int n) {
    if (n <= 1) return n;
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2);
}
```

比较它们的性能差异。

### 5. 阅读参考解答

完成练习后，查看 `solutions/` 目录的参考解答，学习更好的实现方法。

---

## 常见问题

### Q: 如何知道我的实现是否高效？

A:
1. 查看测试输出中的性能提示
2. 比较你的实现和参考解答
3. 分析时间和空间复杂度

### Q: 可以使用标准库吗？

A: 当然可以！实际上很多练习需要用到 `<vector>`, `<queue>` 等标准库。

### Q: 练习文件可以修改吗？

A: 可以修改 TODO 部分和添加辅助函数，但不要修改：
- 测试代码
- 函数签名
- 已有的结构定义

### Q: 如何重置练习？

A: 只需添加回 `// I AM NOT DONE` 标记，系统就会认为练习未完成。

---

## 下一步

完成第一个练习后：

1. **继续基础练习**：
   ```bash
   ./adm-judge  # 自动显示下一个
   ```

2. **查看学习路径**：参考 [README.md](../README.md) 中的学习路径建议

3. **深入某个主题**：
   ```bash
   ./adm-judge list  # 查看所有练习
   # 选择感兴趣的主题深入学习
   ```

4. **阅读 ADM 教材**：配合教材学习效果更好

---

## 🎉 开始你的算法学习之旅！

记住几个关键点：

- **动手实践**：看懂和写出来是两回事
- **理解原理**：不要死记硬背代码
- **坚持练习**：每天做一点，进步很快
- **参考学习**：完成后看看参考解答，学习更好的方法

祝你学习愉快！💪
