# 自动微分（Automatic Differentiation）

## 📖 概述

自动微分（AD）是 JAX 最强大的特性之一，它能够自动计算任意可微函数的导数/梯度。本章深入讲解自动微分的数学原理、实现方式和应用场景。

## 🎯 学习目标

- 理解自动微分的数学原理
- 掌握前向模式和反向模式 AD
- 学会使用 `jax.grad` 计算梯度
- 理解高阶导数和雅可比矩阵
- 应用自动微分于机器学习

## 📚 理论基础

### 什么是自动微分？

自动微分是一种通过计算机程序自动计算导数的技术，它既不是：

- **数值微分** - 使用有限差分近似
- **符号微分** - 使用符号计算系统（如 Mathematica）

而是一种精确且高效的方法，基于**链式法则**的自动应用。

### 链式法则（Chain Rule）

这是自动微分的理论基础：

<div class="math-formula">

$$
\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)
$$

</div>

对于复合函数 $h(x) = f(g(x))$：

$$
\frac{dh}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}
$$

### 多元函数的梯度

对于函数 $f: \mathbb{R}^n \rightarrow \mathbb{R}$，其梯度定义为：

$$
\nabla f(x) = \begin{bmatrix}
\frac{\partial f}{\partial x_1} \\
\frac{\partial f}{\partial x_2} \\
\vdots \\
\frac{\partial f}{\partial x_n}
\end{bmatrix}
$$

**梯度的几何意义**：梯度方向是函数值增长最快的方向。

## 🔬 自动微分模式

### 前向模式（Forward Mode AD）

前向模式从输入向输出传播导数。

**计算图示例**：

对于函数 $f(x) = \sin(x^2)$：

```
x → x² → sin → f
```

**前向模式计算**：

1. 计算值：$v_1 = x^2$
2. 计算导数：$\dot{v}_1 = 2x$
3. 计算值：$v_2 = \sin(v_1)$
4. 计算导数：$\dot{v}_2 = \cos(v_1) \cdot \dot{v}_1 = \cos(x^2) \cdot 2x$

**数学表达**：

$$
\frac{df}{dx} = \frac{d\sin(v_1)}{dv_1} \cdot \frac{dv_1}{dx} = \cos(x^2) \cdot 2x
$$

**复杂度**：对于 $f: \mathbb{R}^n \rightarrow \mathbb{R}^m$，前向模式需要 $O(n)$ 次前向传播。

### 反向模式（Reverse Mode AD）

反向模式从输出向输入反向传播导数，这是深度学习中的**反向传播算法**。

**计算流程**：

1. **前向传播**：计算所有中间变量的值
2. **反向传播**：从输出开始，反向计算梯度

**反向模式计算**：

对于 $f(x) = \sin(x^2)$：

**前向阶段**：
- $v_1 = x^2$
- $v_2 = \sin(v_1)$
- $f = v_2$

**反向阶段**（从后往前）：
- $\bar{v}_2 = \frac{\partial f}{\partial v_2} = 1$
- $\bar{v}_1 = \frac{\partial f}{\partial v_1} = \bar{v}_2 \cdot \frac{\partial v_2}{\partial v_1} = 1 \cdot \cos(v_1) = \cos(x^2)$
- $\bar{x} = \frac{\partial f}{\partial x} = \bar{v}_1 \cdot \frac{\partial v_1}{\partial x} = \cos(x^2) \cdot 2x$

**复杂度**：对于 $f: \mathbb{R}^n \rightarrow \mathbb{R}$，反向模式只需 $O(1)$ 次反向传播，非常高效！

!!! note "为什么深度学习使用反向模式？"
    在深度学习中：
    - 输入维度 $n$ 很大（数百万参数）
    - 输出维度 $m = 1$（标量损失函数）
    - 反向模式 $O(1)$ vs 前向模式 $O(n)$
    - 反向模式效率高得多！

## 💻 JAX 中的自动微分

### 基本用法：`jax.grad`

```python
import jax
import jax.numpy as jnp

# 定义函数
def f(x):
    return x ** 2

# 创建梯度函数
grad_f = jax.grad(f)

# 计算梯度
print(grad_f(3.0))  # 输出: 6.0
```

**数学验证**：

$$
f(x) = x^2 \implies f'(x) = 2x \implies f'(3) = 6
$$

### 多元函数的梯度

```python
def f(x, y):
    return x**2 + 3*y**2

# 对第一个参数求梯度
grad_x = jax.grad(f, argnums=0)
print(grad_x(1.0, 2.0))  # 输出: 2.0

# 对第二个参数求梯度
grad_y = jax.grad(f, argnums=1)
print(grad_y(1.0, 2.0))  # 输出: 12.0
```

**数学验证**：

$$
\begin{align}
\frac{\partial f}{\partial x} &= 2x \implies \frac{\partial f}{\partial x}\bigg|_{(1,2)} = 2 \\
\frac{\partial f}{\partial y} &= 6y \implies \frac{\partial f}{\partial y}\bigg|_{(1,2)} = 12
\end{align}
$$

### 向量值函数的梯度

对于返回数组的函数，`grad` 默认对其求和：

```python
def f(x):
    return x ** 2  # x 是数组

grad_f = jax.grad(lambda x: jnp.sum(f(x)))

x = jnp.array([1.0, 2.0, 3.0])
print(grad_f(x))  # 输出: [2. 4. 6.]
```

**数学解释**：

$$
f(x) = \sum_i x_i^2 \implies \frac{\partial f}{\partial x_i} = 2x_i
$$

## 📐 高阶导数

### 二阶导数

```python
def f(x):
    return x ** 3

# 一阶导数
grad_f = jax.grad(f)

# 二阶导数
grad_grad_f = jax.grad(grad_f)

print(grad_f(2.0))        # 输出: 12.0 (3x² = 12)
print(grad_grad_f(2.0))   # 输出: 12.0 (6x = 12)
```

**数学推导**：

$$
\begin{align}
f(x) &= x^3 \\
f'(x) &= 3x^2 \\
f''(x) &= 6x \\
f''(2) &= 12
\end{align}
$$

### Hessian 矩阵

对于函数 $f: \mathbb{R}^n \rightarrow \mathbb{R}$，Hessian 矩阵为：

$$
H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}
$$

```python
def f(x):
    return jnp.sum(x ** 2)

# 计算 Hessian
hessian = jax.jacfwd(jax.grad(f))

x = jnp.array([1.0, 2.0])
print(hessian(x))
# 输出: [[2. 0.]
#        [0. 2.]]
```

**数学验证**：

$$
f(x_1, x_2) = x_1^2 + x_2^2 \implies H = \begin{bmatrix}
2 & 0 \\
0 & 2
\end{bmatrix}
$$

## 🎓 实际应用

### 1. 梯度下降优化

```python
def loss(params, x, y):
    """简单线性模型的损失函数"""
    pred = params['w'] * x + params['b']
    return jnp.mean((pred - y) ** 2)

# 计算梯度
grad_fn = jax.grad(loss)

# 初始参数
params = {'w': 0.0, 'b': 0.0}

# 训练数据
x = jnp.array([1.0, 2.0, 3.0])
y = jnp.array([2.0, 4.0, 6.0])  # y = 2x

# 一步梯度下降
grads = grad_fn(params, x, y)
learning_rate = 0.1

params['w'] -= learning_rate * grads['w']
params['b'] -= learning_rate * grads['b']
```

### 2. 神经网络训练

```python
def mlp_loss(params, x, y):
    """多层感知机损失"""
    # 前向传播
    h = jax.nn.relu(jnp.dot(x, params['W1']) + params['b1'])
    logits = jnp.dot(h, params['W2']) + params['b2']

    # 交叉熵损失
    return -jnp.mean(y * jax.nn.log_softmax(logits))

# 获取梯度
grad_fn = jax.grad(mlp_loss)
grads = grad_fn(params, x_batch, y_batch)
```

### 3. 物理模拟

求解微分方程：

```python
def physics_loss(state, t):
    """物理系统的能量"""
    x, v = state
    # 简谐振动：E = 1/2 mv² + 1/2 kx²
    return 0.5 * v**2 + 0.5 * x**2

# 计算力（梯度的负数）
force = jax.grad(lambda x: -physics_loss([x, 0], 0))
```

## ⚡ 性能考虑

### JIT 编译与自动微分

```python
@jax.jit
def fast_grad(x):
    return jax.grad(lambda x: jnp.sum(x**2))(x)

# 首次调用会编译
result = fast_grad(jnp.array([1.0, 2.0, 3.0]))

# 后续调用直接使用编译后的代码
result = fast_grad(jnp.array([4.0, 5.0, 6.0]))  # 很快！
```

### 梯度检查点（Gradient Checkpointing）

对于内存受限的大模型：

```python
from jax.experimental import checkpoint

@checkpoint
def expensive_layer(x):
    # 计算密集但不保存中间激活
    return jax.nn.relu(x)
```

## 🔍 常见陷阱

### 1. 非纯函数

❌ **错误**：使用全局状态

```python
counter = 0

def f(x):
    global counter
    counter += 1  # 副作用！
    return x ** 2

# grad 可能不按预期工作
```

✅ **正确**：纯函数

```python
def f(x):
    return x ** 2  # 纯函数，无副作用
```

### 2. 整数梯度

❌ **错误**：对整数求梯度

```python
x = 3  # 整数
grad_f = jax.grad(lambda x: x**2)
# grad_f(x)  # 错误！
```

✅ **正确**：使用浮点数

```python
x = 3.0  # 浮点数
grad_f = jax.grad(lambda x: x**2)
print(grad_f(x))  # 6.0
```

## 📊 性能对比

| 方法 | 精度 | 速度 | 内存 | 适用场景 |
|------|------|------|------|----------|
| 数值微分 | 近似 | 慢 | 低 | 验证、调试 |
| 符号微分 | 精确 | 中 | 高 | 简单函数 |
| 前向 AD | 精确 | 快 | 中 | $n \ll m$ |
| 反向 AD | 精确 | 快 | 高 | $n \gg m$ (深度学习) |

## 🎯 练习指导

### Exercise: `transform01_grad`

**目标**：掌握基本的梯度计算

**关键点**：
1. 理解链式法则
2. 正确使用 `jax.grad`
3. 处理多元函数

**提示**：
- 一阶导数：$\frac{d}{dx}x^2 = 2x$
- 多项式导数：$(ax^n)' = anx^{n-1}$
- 组合函数要应用链式法则

**数学验证**：
对于 $f(x) = 3x^3 + 2x^2 - 5x + 1$：

$$
f'(x) = 9x^2 + 4x - 5
$$

在 $x=2$：

$$
f'(2) = 9(4) + 4(2) - 5 = 36 + 8 - 5 = 39
$$

## 📚 延伸阅读

### 论文

- [Automatic Differentiation in Machine Learning: a Survey](https://arxiv.org/abs/1502.05767)
- [The Simple Essence of Automatic Differentiation](https://arxiv.org/abs/1804.00746)

### 书籍

- **Deep Learning** - Goodfellow et al. (Chapter 6)
- **Automatic Differentiation: Techniques and Applications** - Griewank & Walther

### 在线资源

- [JAX Autodiff Cookbook](https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html)
- [PyTorch Autograd Tutorial](https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html)

## ⏭️ 下一步

掌握了基础的自动微分后，继续学习：

- [值与梯度](value_and_grad.md) - 同时计算函数值和梯度
- [JIT 编译](jit.md) - 优化性能
- [组合变换](combining.md) - jit + grad + vmap

[继续学习 →](value_and_grad.md){ .md-button .md-button--primary }
