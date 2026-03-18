# JAX 入门概述

## 📖 本章简介

欢迎来到 JAX 学习之旅的起点！本章将带你认识 JAX，了解它的设计哲学、核心特性和基本操作。完成本章后，你将能够：

- 理解 JAX 是什么，以及为什么要使用它
- 掌握 JAX 数组的创建和基本操作
- 熟悉 JAX 与 NumPy 的区别
- 为后续的高级主题打好基础

## 🎯 学习目标

### 知识目标

- 理解 JAX 的设计理念（函数式编程、可组合变换）
- 掌握 JAX 数组的不可变性
- 了解 JAX 的性能优势

### 技能目标

- 能够创建和操作 JAX 数组
- 能够使用 JAX 进行基本数值计算
- 能够编写符合 JAX 规范的纯函数

## 🔍 什么是 JAX？

### 官方定义

> JAX is NumPy on the CPU, GPU, and TPU, with great automatic differentiation for high-performance machine learning research.

JAX = **NumPy** + **自动微分** + **JIT 编译** + **GPU/TPU 支持**

### 核心特性

<div class="knowledge-point">

**1. NumPy 兼容的 API**

JAX 提供了与 NumPy 几乎完全相同的 API，学习曲线平缓：

```python
import numpy as np
import jax.numpy as jnp

# NumPy
x_np = np.array([1, 2, 3])
y_np = np.sum(x_np ** 2)

# JAX - 语法完全一样！
x_jax = jnp.array([1, 2, 3])
y_jax = jnp.sum(x_jax ** 2)
```

</div>

<div class="knowledge-point">

**2. 自动微分（Autograd）**

自动计算任意可微函数的导数：

```python
import jax

def f(x):
    return x ** 3 + 2 * x ** 2

grad_f = jax.grad(f)
print(grad_f(1.0))  # 7.0 = 3x² + 4x at x=1
```

</div>

<div class="knowledge-point">

**3. JIT 编译（Just-In-Time）**

使用 XLA 编译器加速代码：

```python
@jax.jit
def slow_function(x):
    for i in range(100):
        x = x * 2 + 1
    return x

# 首次调用会编译，后续调用非常快
result = slow_function(1.0)
```

</div>

<div class="knowledge-point">

**4. 向量化（Vectorization）**

自动批处理函数：

```python
# 处理单个样本的函数
def process_single(x):
    return x ** 2

# 自动向量化
process_batch = jax.vmap(process_single)

# 处理整个批次
batch = jnp.array([1, 2, 3, 4, 5])
results = process_batch(batch)
```

</div>

## 🆚 JAX vs NumPy

### 相似之处

- API 几乎完全相同
- 支持相同的数组操作
- 相同的数学函数

### 关键区别

| 特性 | NumPy | JAX |
|------|-------|-----|
| **可变性** | 可变 | 不可变 |
| **设备** | CPU | CPU/GPU/TPU |
| **自动微分** | ❌ | ✅ |
| **JIT 编译** | ❌ | ✅ |
| **随机数** | 全局状态 | 显式密钥 |

### 不可变性示例

```python
import numpy as np
import jax.numpy as jnp

# NumPy - 可变
x_np = np.array([1, 2, 3])
x_np[0] = 10  # ✅ 允许

# JAX - 不可变
x_jax = jnp.array([1, 2, 3])
# x_jax[0] = 10  # ❌ 错误！

# 正确方式：使用 .at[]
x_jax = x_jax.at[0].set(10)  # ✅ 返回新数组
```

## 💡 为什么使用 JAX？

### 优势

1. **性能**
   - GPU/TPU 加速
   - JIT 编译优化
   - 高效的内存使用

2. **灵活性**
   - 可组合的函数变换
   - 纯函数式设计
   - 易于调试和测试

3. **研究友好**
   - 快速原型开发
   - 易于实验新想法
   - 强大的自动微分

### 适用场景

- 机器学习研究
- 科学计算
- 数值优化
- 物理模拟
- 任何需要自动微分的场景

## 📚 本章内容

### [Exercise 01: Hello JAX](hello_jax.md)

**学习内容**：
- 导入 JAX 和 JAX NumPy
- 创建基本数组
- 理解数组的形状和数据类型

**知识点**：
- `jax.numpy` vs `numpy`
- 数组创建函数：`array()`, `zeros()`, `ones()`
- 数据类型：`float32`, `int32` 等

### [Exercise 02: 数组创建](arrays.md)

**学习内容**：
- 各种数组创建方法
- 理解数组的不可变性
- 数据类型转换

**知识点**：
- `arange()`, `linspace()`, `eye()`
- dtype 参数的使用
- 数组的内存布局

### [Exercise 03: 基本运算](operations.md)

**学习内容**：
- 元素级运算
- 数学函数
- 归约操作

**知识点**：
- 广播规则
- 通用函数（ufuncs）
- `sum()`, `mean()`, `max()` 等

## 🎓 学习建议

### 循序渐进

1. **先理解概念** - 阅读理论部分
2. **动手实践** - 完成练习
3. **对比验证** - 与 NumPy 对比
4. **总结归纳** - 记录关键要点

### 常见陷阱

!!! warning "注意"
    - 不要试图修改 JAX 数组（使用 `.at[]`）
    - 使用浮点数类型进行微分（不能对整数求导）
    - 避免在 JIT 编译的函数中使用 Python 控制流

### 学习资源

- [JAX 快速入门](https://jax.readthedocs.io/en/latest/notebooks/quickstart.html)
- [JAX NumPy API 文档](https://jax.readthedocs.io/en/latest/jax.numpy.html)
- [从 NumPy 迁移到 JAX](https://jax.readthedocs.io/en/latest/notebooks/thinking_in_jax.html)

## 📝 预备知识

在开始本章之前，建议你：

- 熟悉 Python 基础语法
- 了解 NumPy 的基本使用
- 有基本的线性代数知识

如果对这些内容不熟悉，可以先阅读：

- [Python 官方教程](https://docs.python.org/3/tutorial/)
- [NumPy 快速入门](https://numpy.org/doc/stable/user/quickstart.html)
- [线性代数基础](../math/linear_algebra.md)

## ⏭️ 下一步

准备好了吗？让我们从第一个练习开始！

[开始 Exercise 01: Hello JAX →](hello_jax.md){ .md-button .md-button--primary }
