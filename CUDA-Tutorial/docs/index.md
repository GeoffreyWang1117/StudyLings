# JAXlings 学习文档

<div align="center">

![JAXlings Logo](assets/logo.svg)

**从零开始，系统学习 JAX**

[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://jaxlings.readthedocs.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>

## 🎯 关于本文档

欢迎来到 **JAXlings 学习文档**！本文档是 JAXlings 练习系统的完整知识库，深入讲解每个练习背后的理论知识、数学原理和实践技巧。

### 📚 文档特色

- **理论与实践结合** - 每个主题都包含数学推导和代码示例
- **循序渐进** - 从基础概念到高级应用，系统化学习
- **数学公式详解** - 使用 MathJax 渲染，清晰展示数学推导
- **实战导向** - 结合真实的深度学习应用场景
- **中文原创** - 专为中文用户打造的学习资源

### 🗺️ 学习路线

<div class="grid cards" markdown>

-   :material-school: **初学者路径**

    ---

    1. [JAX 入门](01_intro/overview.md) - 了解 JAX 基础
    2. [数组操作](02_arrays/overview.md) - 掌握数组运算
    3. [JAX 变换](03_transformations/overview.md) - 学习核心变换

-   :material-chart-line: **中级路径**

    ---

    4. [神经网络](04_neural_networks/overview.md) - 构建网络
    5. [高级主题](05_advanced/overview.md) - CNN、注意力机制
    6. [随机数系统](06_random/overview.md) - PRNG 与采样

-   :material-rocket-launch: **高级路径**

    ---

    7. [PyTree 结构](07_pytrees/overview.md) - 参数管理
    8. [控制流](08_control_flow/overview.md) - cond 与 scan
    9. [并行计算](09_parallel/overview.md) - 多设备训练

-   :material-brain: **专家路径**

    ---

    10. [深度学习高级](10_deep_learning/overview.md) - ResNet、Transformer
    11. [性能优化](appendix/performance.md) - 生产级优化
    12. [最佳实践](appendix/best_practices.md) - 工程经验

</div>

## 🔬 核心内容

### 数学基础

深入理解 JAX 背后的数学原理：

- **[线性代数](math/linear_algebra.md)** - 向量、矩阵、张量运算
- **[微积分](math/calculus.md)** - 导数、梯度、自动微分
- **[概率论](math/probability.md)** - 随机变量、分布、采样
- **[优化理论](math/optimization.md)** - 梯度下降、优化算法

### JAX 核心概念

掌握 JAX 的独特设计：

- **函数式编程** - 纯函数、不可变性
- **变换组合** - grad、jit、vmap 的组合使用
- **并行计算** - pmap、设备管理
- **自动微分** - 前向与反向模式

### 深度学习实践

构建现代深度学习模型：

- **神经网络基础** - 线性层、激活、损失
- **卷积网络** - CNN、ResNet
- **序列模型** - RNN、LSTM (通过 scan)
- **注意力机制** - Self-Attention、Transformer

## 📖 如何使用本文档

### 💡 推荐学习方法

1. **顺序学习** - 按照章节顺序，逐步深入
2. **理论先行** - 先理解数学原理，再看代码
3. **动手实践** - 配合 JAXlings 练习系统
4. **重复复习** - 定期回顾关键概念

### 🎓 配套练习

本文档与 [JAXlings 练习系统](https://github.com/yourusername/jaxlings) 配套使用：

```bash
# 安装 JAXlings
git clone https://github.com/yourusername/jaxlings
cd jaxlings
pip install -r requirements.txt

# 开始练习
python jaxlings.py verify
```

### 📝 文档结构

每个主题包含：

- **概述** - 主题介绍和学习目标
- **理论知识** - 数学原理和算法讲解
- **代码示例** - JAX 实现和最佳实践
- **练习指导** - 配套练习的详细说明
- **延伸阅读** - 相关论文和资源

## 🌟 特色板块

### 数学推导

使用 MathJax 展示完整的数学推导过程：

$$
\nabla_\theta L = \frac{\partial L}{\partial \theta}
$$

### 代码示例

```python
import jax
import jax.numpy as jnp

# 自动微分示例
def f(x):
    return x ** 2

grad_f = jax.grad(f)
print(grad_f(3.0))  # 输出: 6.0
```

### 知识要点

!!! note "核心概念"
    JAX 的四大变换：grad、jit、vmap、pmap 是其核心优势

### 最佳实践

!!! tip "性能提示"
    始终在训练循环外部使用 jit 编译，避免重复编译开销

## 🔗 相关资源

- [JAX 官方文档](https://jax.readthedocs.io/)
- [JAX GitHub](https://github.com/google/jax)
- [Flax (JAX 神经网络库)](https://github.com/google/flax)
- [Optax (JAX 优化库)](https://github.com/deepmind/optax)

## 🤝 贡献

欢迎贡献文档改进：

- 修复错误和笔误
- 补充数学推导
- 添加代码示例
- 改进说明和图表

## 📄 许可证

本文档采用 [MIT License](LICENSE) 开源协议。

---

<div align="center">

**开始你的 JAX 学习之旅** 🚀

[快速开始](getting-started.md){ .md-button .md-button--primary }
[查看教程](01_intro/overview.md){ .md-button }

</div>
