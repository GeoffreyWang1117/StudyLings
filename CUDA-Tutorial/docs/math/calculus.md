# 微积分基础

## 📖 概述

微积分是深度学习的数学基础，特别是**导数**和**梯度**的概念对于理解反向传播算法至关重要。本章回顾微积分的核心概念，并展示它们在 JAX 中的应用。

## 🎯 导数基础

### 定义

函数 $f(x)$ 在点 $x$ 处的导数定义为：

<div class="math-formula">

$$
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
$$

</div>

**几何意义**：切线的斜率

**物理意义**：瞬时变化率

### 常见导数公式

| 函数 | 导数 |
|------|------|
| $c$ (常数) | $0$ |
| $x^n$ | $nx^{n-1}$ |
| $e^x$ | $e^x$ |
| $\ln x$ | $\frac{1}{x}$ |
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $\tanh x$ | $1 - \tanh^2 x$ |

### 导数运算法则

**和差法则**：
$$
(f + g)' = f' + g'
$$

**积法则**：
$$
(fg)' = f'g + fg'
$$

**商法则**：
$$
\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}
$$

**链式法则**（最重要！）：
$$
(f \circ g)'(x) = f'(g(x)) \cdot g'(x)
$$

## 🎓 多元函数与梯度

### 偏导数

对于多元函数 $f(x_1, x_2, \ldots, x_n)$，关于 $x_i$ 的偏导数：

$$
\frac{\partial f}{\partial x_i} = \lim_{h \to 0} \frac{f(x_1, \ldots, x_i + h, \ldots, x_n) - f(x_1, \ldots, x_n)}{h}
$$

**例子**：

$$
f(x, y) = x^2 + 3xy + y^2
$$

$$
\begin{align}
\frac{\partial f}{\partial x} &= 2x + 3y \\
\frac{\partial f}{\partial y} &= 3x + 2y
\end{align}
$$

### 梯度向量

梯度是所有偏导数组成的向量：

$$
\nabla f = \begin{bmatrix}
\frac{\partial f}{\partial x_1} \\
\frac{\partial f}{\partial x_2} \\
\vdots \\
\frac{\partial f}{\partial x_n}
\end{bmatrix}
$$

**性质**：

1. **方向性**：梯度指向函数值增长最快的方向
2. **大小**：梯度的模是最大变化率
3. **正交性**：梯度垂直于等高线

### 例子：神经网络损失函数

$$
L(\mathbf{w}) = \frac{1}{m} \sum_{i=1}^m (y_i - \mathbf{w}^T \mathbf{x}_i)^2
$$

梯度：

$$
\nabla_{\mathbf{w}} L = -\frac{2}{m} \sum_{i=1}^m (y_i - \mathbf{w}^T \mathbf{x}_i) \mathbf{x}_i
$$

## 📐 雅可比矩阵

对于向量值函数 $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$：

$$
\mathbf{f}(\mathbf{x}) = \begin{bmatrix}
f_1(\mathbf{x}) \\
f_2(\mathbf{x}) \\
\vdots \\
f_m(\mathbf{x})
\end{bmatrix}
$$

雅可比矩阵：

$$
J = \begin{bmatrix}
\frac{\partial f_1}{\partial x_1} & \frac{\partial f_1}{\partial x_2} & \cdots & \frac{\partial f_1}{\partial x_n} \\
\frac{\partial f_2}{\partial x_1} & \frac{\partial f_2}{\partial x_2} & \cdots & \frac{\partial f_2}{\partial x_n} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial f_m}{\partial x_1} & \frac{\partial f_m}{\partial x_2} & \cdots & \frac{\partial f_m}{\partial x_n}
\end{bmatrix}
$$

## 🔄 链式法则（多元）

这是自动微分的核心！

对于复合函数 $h(\mathbf{x}) = f(g(\mathbf{x}))$：

$$
\frac{\partial h}{\partial x_i} = \sum_j \frac{\partial f}{\partial g_j} \cdot \frac{\partial g_j}{\partial x_i}
$$

**矩阵形式**：

$$
\nabla_{\mathbf{x}} h = J_g^T \nabla_{\ g} f
$$

## 💻 JAX 中的应用

### 计算梯度

```python
import jax
import jax.numpy as jnp

# 多元函数
def f(x, y):
    return x**2 + 3*x*y + y**2

# 计算梯度
grad_f = jax.grad(f, argnums=(0, 1))
print(grad_f(1.0, 2.0))  # (8.0, 7.0)
```

### 雅可比矩阵

```python
def f(x):
    return jnp.array([x[0]**2, x[0]*x[1], x[1]**2])

x = jnp.array([1.0, 2.0])

# 前向模式雅可比
jac_fwd = jax.jacfwd(f)(x)

# 反向模式雅可比
jac_rev = jax.jacrev(f)(x)

print(jac_fwd)
```

## 📊 优化理论

### 梯度下降

基本思想：沿着梯度的反方向移动，找到最小值。

$$
\mathbf{x}_{t+1} = \mathbf{x}_t - \alpha \nabla f(\mathbf{x}_t)
$$

其中 $\alpha$ 是学习率。

### 收敛性

对于凸函数，梯度下降保证收敛到全局最优。

对于非凸函数（深度学习），收敛到局部最优或鞍点。

## ⏭️ 下一步

- [优化理论](optimization.md)
- [线性代数](linear_algebra.md)
- [自动微分详解](../03_transformations/grad.md)
