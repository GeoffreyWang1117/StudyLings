# 快速开始

本指南将帮助你快速上手 JAXlings 学习系统。

## 📦 安装

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装 JAXlings

=== "从 GitHub 克隆"

    ```bash
    git clone https://github.com/yourusername/jaxlings.git
    cd jaxlings
    pip install -r requirements.txt
    ```

=== "开发模式安装"

    ```bash
    git clone https://github.com/yourusername/jaxlings.git
    cd jaxlings
    pip install -e .
    ```

### 验证安装

```bash
python -c "import jax; print(jax.__version__)"
```

## 🎯 第一个练习

### 运行练习

```bash
# 运行下一个待完成的练习
python jaxlings.py verify

# 或使用安装的命令
jaxlings verify
```

你会看到类似的输出：

```
============================================================
Running: intro01_hello_jax
Path: exercises/01_intro/intro01_hello_jax.py
============================================================

✗ Exercise intro01_hello_jax failed!
```

### 修复练习

1. 打开提示的文件：`exercises/01_intro/intro01_hello_jax.py`
2. 阅读注释和任务说明
3. 修复 TODO 标记的代码
4. 删除文件开头的 `# I AM NOT DONE` 注释
5. 再次运行 `jaxlings verify`

## 📚 使用文档

### 查看练习说明

每个练习对应本文档的一个章节：

- `intro01_hello_jax` → [Hello JAX](01_intro/hello_jax.md)
- `transform01_grad` → [自动微分](03_transformations/grad.md)
- 等等...

### 获取提示

```bash
# 当前练习的提示
jaxlings hint

# 特定练习的提示
jaxlings hint intro01_hello_jax
```

### 列出所有练习

```bash
jaxlings list
```

输出示例：

```
JAXlings Exercises:
============================================================
 1. ○ intro01_hello_jax
 2. ○ intro02_arrays
 3. ○ intro03_operations
...
Progress: 0/35 completed
```

## 🔄 工作流程

### 推荐工作流

<div class="mermaid">
graph LR
    A[运行 verify] --> B[阅读文档]
    B --> C[理解原理]
    C --> D[编写代码]
    D --> E[运行测试]
    E --> F{通过?}
    F -->|否| B
    F -->|是| G[下一题]
</div>

### 使用 Watch 模式

```bash
jaxlings watch
```

Watch 模式会自动监视文件变化并重新运行测试，非常适合快速迭代！

## 💡 学习建议

### 理论与实践结合

1. **先读文档** - 理解数学原理和概念
2. **查看示例** - 学习 JAX 的实现方式
3. **动手编码** - 完成练习巩固知识
4. **总结回顾** - 记录关键要点

### 循序渐进

- **不要跳过基础章节** - 每章都有重要概念
- **重复练习** - 遇到困难可以重做
- **做好笔记** - 记录学习心得
- **参与讨论** - 在 GitHub Issues 提问

### 数学准备

建议先复习：

- [线性代数基础](math/linear_algebra.md)
- [微积分基础](math/calculus.md)
- [概率论基础](math/probability.md)

## 🎓 学习路径

### 初学者（第 1-2 周）

- ✅ [01. JAX 入门](01_intro/overview.md)
- ✅ [02. 数组操作](02_arrays/overview.md)
- ✅ [03. JAX 变换](03_transformations/overview.md)

**目标**：理解 JAX 基础和核心变换

### 中级（第 3-4 周）

- ✅ [04. 神经网络](04_neural_networks/overview.md)
- ✅ [05. 高级主题](05_advanced/overview.md)
- ✅ [06. 随机数系统](06_random/overview.md)

**目标**：构建基础神经网络，理解 CNN 和注意力

### 高级（第 5-6 周）

- ✅ [07. PyTree 结构](07_pytrees/overview.md)
- ✅ [08. 控制流](08_control_flow/overview.md)
- ✅ [09. 并行计算](09_parallel/overview.md)

**目标**：掌握高级特性和并行训练

### 专家（第 7-8 周）

- ✅ [10. 深度学习高级](10_deep_learning/overview.md)
- ✅ [性能优化](appendix/performance.md)
- ✅ [最佳实践](appendix/best_practices.md)

**目标**：实现 ResNet 和 Transformer，优化生产代码

## 🛠️ 常用命令

### 练习管理

```bash
# 验证当前练习
jaxlings verify

# 运行特定练习
jaxlings run <exercise_name>

# 查看所有练习
jaxlings list

# 重置进度
jaxlings reset
```

### 获取帮助

```bash
# 查看帮助信息
jaxlings --help

# 查看提示
jaxlings hint [exercise_name]
```

### 测试

```bash
# 运行单个练习的测试
python exercises/01_intro/intro01_hello_jax.py

# 使用 pytest 运行所有测试
pytest exercises/
```

## 🐛 常见问题

### JAX 安装问题

如果遇到 JAX 安装问题，参考 [JAX 官方安装指南](https://github.com/google/jax#installation)。

对于 GPU 支持：

```bash
# CUDA 11 版本
pip install --upgrade "jax[cuda11_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

# CUDA 12 版本
pip install --upgrade "jax[cuda12_pip]" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```

### 练习无法通过

1. **仔细阅读错误信息** - 错误通常会指出问题所在
2. **查看文档** - 相关章节有详细讲解
3. **使用提示** - `jaxlings hint` 获取帮助
4. **参考测试用例** - 了解期望的输出

### 进度丢失

进度保存在 `~/.jaxlings_progress.json`，如果需要重置：

```bash
jaxlings reset
```

## 📚 额外资源

### 官方文档

- [JAX 官方文档](https://jax.readthedocs.io/)
- [JAX 教程](https://jax.readthedocs.io/en/latest/notebooks/quickstart.html)
- [JAX GitHub 仓库](https://github.com/google/jax)

### 相关库

- [Flax](https://flax.readthedocs.io/) - JAX 神经网络库
- [Optax](https://optax.readthedocs.io/) - JAX 优化库
- [Haiku](https://dm-haiku.readthedocs.io/) - DeepMind 的 JAX NN 库

### 论文和博客

- [JAX: Autograd and XLA](https://github.com/google/jax#reference-documentation)
- [JAX MD](https://github.com/google/jax-md) - 分子动力学
- [JAX 生态系统](https://github.com/n2cholas/awesome-jax)

## ⏭️ 下一步

准备好了吗？让我们从第一个练习开始！

[开始学习 JAX 入门 →](01_intro/overview.md){ .md-button .md-button--primary }
