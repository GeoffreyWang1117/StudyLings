# Hello JAX

欢迎来到 JAX 的世界！这是你的第一个 JAX 练习。

## 📚 知识要点

### 什么是 JAX？

JAX 是 Google 开发的高性能数值计算库，它结合了：

- **NumPy 的易用性**：熟悉的 API 接口
- **自动微分**：可以对任意函数求导
- **JIT 编译**：接近 C/Fortran 的性能
- **GPU/TPU 支持**：充分利用硬件加速

### 为什么选择 JAX？

```python
# NumPy
import numpy as np
x = np.array([1, 2, 3])

# JAX - 几乎相同的 API！
import jax.numpy as jnp
x = jnp.array([1, 2, 3])
```

关键区别：
- JAX 数组是**不可变的**（immutable）
- JAX 可以自动求导
- JAX 可以 JIT 编译以获得更高性能

## 🎯 练习目标

在这个练习中，你将学习：

1. 导入 JAX 库
2. 创建你的第一个 JAX 数组
3. 理解 JAX 数组的基本属性

## 💡 核心概念

### JAX 数组创建

JAX 提供了 `jax.numpy` 模块，简称 `jnp`：

```python
import jax.numpy as jnp

# 从列表创建数组
arr = jnp.array([1, 2, 3, 4, 5])

# 查看数组属性
print(arr.shape)  # (5,)
print(arr.dtype)  # int32
print(arr.size)   # 5
```

### 数组属性

| 属性 | 说明 | 示例 |
|------|------|------|
| `shape` | 数组的形状 | `(3, 4)` |
| `dtype` | 数据类型 | `float32`, `int32` |
| `size` | 元素总数 | `12` |
| `ndim` | 维度数量 | `2` |

## 🔬 数学原理

### 数组的数学表示

一个一维数组可以表示为向量：

$$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}$$

在 JAX 中：

```python
x = jnp.array([1.0, 2.0, 3.0])  # 向量 [1, 2, 3]ᵀ
```

### 数组的索引

数组索引从 0 开始：

$$\mathbf{x} = [x_0, x_1, x_2, \ldots, x_{n-1}]$$

访问元素：$x_i$ 对应 `x[i]`

## 📝 代码示例

### 基础示例

```python
import jax.numpy as jnp

# 创建数组
x = jnp.array([1, 2, 3, 4, 5])

# 基本操作
print(x + 10)      # 每个元素加 10
print(x * 2)       # 每个元素乘以 2
print(jnp.sum(x))  # 求和：15
print(jnp.mean(x)) # 平均值：3.0
```

### 不同类型的数组

```python
# 整数数组
int_arr = jnp.array([1, 2, 3])
print(int_arr.dtype)  # int32

# 浮点数组
float_arr = jnp.array([1.0, 2.0, 3.0])
print(float_arr.dtype)  # float32

# 显式指定类型
arr = jnp.array([1, 2, 3], dtype=jnp.float64)
print(arr.dtype)  # float64
```

## 🎓 与 NumPy 的对比

| 特性 | NumPy | JAX |
|------|-------|-----|
| 数组可变性 | 可变（mutable） | 不可变（immutable） |
| 自动微分 | ❌ | ✅ |
| JIT 编译 | ❌ | ✅ |
| GPU 支持 | 有限 | 原生支持 |
| API 兼容性 | - | 98% 兼容 |

### NumPy 迁移示例

```python
# NumPy 代码
import numpy as np
x = np.array([1, 2, 3])
x[0] = 10  # 直接修改

# JAX 代码
import jax.numpy as jnp
x = jnp.array([1, 2, 3])
x = x.at[0].set(10)  # 函数式更新，返回新数组
```

## ⚠️ 常见陷阱

### 1. 数组不可变

```python
# ❌ 错误：JAX 数组不能直接修改
x = jnp.array([1, 2, 3])
x[0] = 10  # TypeError!

# ✅ 正确：使用 .at[] 进行函数式更新
x = jnp.array([1, 2, 3])
x = x.at[0].set(10)  # 返回新数组
```

### 2. 默认数据类型

JAX 默认使用 32 位浮点数（与 NumPy 的 64 位不同）：

```python
import jax
jax.config.update("jax_enable_x64", True)  # 启用 64 位
```

## 🔍 深入理解

### JAX 的设计哲学

1. **函数式编程**：鼓励纯函数，避免副作用
2. **可组合性**：变换（grad, jit, vmap）可以自由组合
3. **性能优先**：所有操作都针对性能优化

### 内存布局

JAX 数组在内存中的布局：

```
连续内存块：[1, 2, 3, 4, 5]
            ↑  ↑  ↑  ↑  ↑
索引：      0  1  2  3  4
```

这种布局使得向量化操作非常高效。

## 💪 实践建议

1. **始终使用 `jax.numpy`**，而不是普通的 `numpy`
2. **适应不可变性**：这是函数式编程的核心
3. **检查数组形状**：在调试时使用 `print(arr.shape)`
4. **注意数据类型**：32 位 vs 64 位会影响精度和性能

## 🔗 相关资源

- [JAX 快速入门](https://jax.readthedocs.io/en/latest/quickstart.html)
- [NumPy 到 JAX 迁移指南](https://jax.readthedocs.io/en/latest/jax-101/01-jax-basics.html)
- [JAX 数组 API 参考](https://jax.readthedocs.io/en/latest/jax.numpy.html)

## ✅ 练习检查清单

完成练习后，确认你已经掌握：

- [ ] 能够正确导入 JAX
- [ ] 可以创建 JAX 数组
- [ ] 理解数组的基本属性（shape, dtype, size）
- [ ] 知道 JAX 与 NumPy 的主要区别
- [ ] 理解数组的不可变性

---

现在打开 `exercises/01_intro/intro01_hello_jax.py` 开始你的第一个练习！
