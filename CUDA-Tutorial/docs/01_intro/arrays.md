# 数组创建

掌握各种数组创建方法是 JAX 编程的基础。

## 📚 知识要点

### 数组创建的重要性

在科学计算和机器学习中，我们需要各种类型的数组：

- **零数组**：初始化权重
- **全一数组**：创建掩码
- **等间距数组**：生成坐标网格
- **随机数组**：初始化神经网络参数

## 🎯 学习目标

1. 掌握常用的数组创建函数
2. 理解不同创建方法的应用场景
3. 学会控制数组的形状和数据类型

## 💡 核心概念

### 基础创建函数

JAX 提供了丰富的数组创建函数：

| 函数 | 用途 | 示例 |
|------|------|------|
| `zeros` | 创建全零数组 | `jnp.zeros((3, 4))` |
| `ones` | 创建全一数组 | `jnp.ones((2, 3))` |
| `full` | 创建填充指定值的数组 | `jnp.full((2, 2), 7)` |
| `eye` | 创建单位矩阵 | `jnp.eye(3)` |
| `arange` | 创建等差数列 | `jnp.arange(0, 10, 2)` |
| `linspace` | 创建线性空间 | `jnp.linspace(0, 1, 5)` |

## 🔬 数学原理

### 零矩阵

零矩阵是所有元素都为 0 的矩阵：

$$\mathbf{O} = \begin{bmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}$$

```python
O = jnp.zeros((2, 3))
```

在神经网络中常用于初始化偏置项。

### 单位矩阵

单位矩阵（Identity Matrix）是主对角线为 1，其余为 0 的方阵：

$$\mathbf{I}_3 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

数学性质：$\mathbf{A} \mathbf{I} = \mathbf{I} \mathbf{A} = \mathbf{A}$

```python
I = jnp.eye(3)
```

### 等差数列

等差数列的通项公式：

$$a_n = a_0 + n \cdot d$$

其中 $a_0$ 是起始值，$d$ 是公差。

```python
# 创建 [0, 2, 4, 6, 8]
arr = jnp.arange(0, 10, 2)  # start=0, stop=10, step=2
```

### 线性空间

`linspace` 在指定区间内生成等间距的 n 个点：

$$x_i = a + i \cdot \frac{b - a}{n - 1}, \quad i = 0, 1, \ldots, n-1$$

其中 $[a, b]$ 是区间，$n$ 是点的数量。

```python
# 在 [0, 1] 区间生成 5 个点：[0.0, 0.25, 0.5, 0.75, 1.0]
x = jnp.linspace(0, 1, 5)
```

## 📝 代码示例

### 零数组和全一数组

```python
import jax.numpy as jnp

# 创建 3x4 的零数组
zeros = jnp.zeros((3, 4))
print(zeros.shape)  # (3, 4)

# 创建 2x3 的全一数组
ones = jnp.ones((2, 3))
print(ones)
# [[1. 1. 1.]
#  [1. 1. 1.]]

# 指定数据类型
zeros_int = jnp.zeros((2, 2), dtype=jnp.int32)
```

### 填充特定值

```python
# 创建 3x3 的数组，填充值为 7
sevens = jnp.full((3, 3), 7)
print(sevens)
# [[7 7 7]
#  [7 7 7]
#  [7 7 7]]

# 填充浮点数
pi_array = jnp.full((2, 4), 3.14159)
```

### 单位矩阵

```python
# 创建 3x3 单位矩阵
I = jnp.eye(3)
print(I)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]

# 创建非方阵的对角矩阵
diag = jnp.eye(3, 5)  # 3 行 5 列
print(diag.shape)  # (3, 5)
```

### 等差数列

```python
# arange：类似 Python 的 range
arr1 = jnp.arange(5)          # [0, 1, 2, 3, 4]
arr2 = jnp.arange(2, 10)      # [2, 3, 4, 5, 6, 7, 8, 9]
arr3 = jnp.arange(0, 10, 2)   # [0, 2, 4, 6, 8]
arr4 = jnp.arange(1.0, 2.0, 0.1)  # 浮点数步长

# 注意：arange 不包含终止值
print(jnp.arange(10))  # 不包含 10
```

### 线性空间

```python
# linspace：生成等间距的点
x1 = jnp.linspace(0, 1, 5)
# [0.   0.25 0.5  0.75 1.  ]

x2 = jnp.linspace(0, 10, 11)
# [0. 1. 2. 3. 4. 5. 6. 7. 8. 9. 10.]

# 不包含终点
x3 = jnp.linspace(0, 1, 5, endpoint=False)
# [0.  0.2 0.4 0.6 0.8]

# 注意：linspace 默认包含终止值
```

### 对角矩阵

```python
# 从向量创建对角矩阵
v = jnp.array([1, 2, 3])
D = jnp.diag(v)
print(D)
# [[1 0 0]
#  [0 2 0]
#  [0 0 3]]

# 提取对角线
diag_elements = jnp.diag(D)
# [1 2 3]
```

## 🎓 应用场景

### 神经网络初始化

```python
# 权重初始化为小随机数（后续会学习）
# 偏置初始化为零
def init_layer(input_dim, output_dim):
    # W = random initialization (later)
    b = jnp.zeros(output_dim)
    return b

bias = init_layer(784, 128)
print(bias.shape)  # (128,)
```

### 网格生成

```python
# 生成 2D 网格
x = jnp.linspace(-5, 5, 100)
y = jnp.linspace(-5, 5, 100)

# 使用 meshgrid 创建坐标矩阵
X, Y = jnp.meshgrid(x, y)

# 计算函数值：z = x^2 + y^2
Z = X**2 + Y**2

print(Z.shape)  # (100, 100)
```

### 掩码创建

```python
# 创建注意力掩码（用于 Transformer）
seq_len = 5
mask = jnp.ones((seq_len, seq_len))

# 创建下三角掩码（因果掩码）
causal_mask = jnp.tril(mask)
print(causal_mask)
# [[1. 0. 0. 0. 0.]
#  [1. 1. 0. 0. 0.]
#  [1. 1. 1. 0. 0.]
#  [1. 1. 1. 1. 0.]
#  [1. 1. 1. 1. 1.]]
```

## 🔬 性能考虑

### 内存分配

```python
import time

# 大数组创建的性能
start = time.time()
large_array = jnp.zeros((10000, 10000))
print(f"创建时间: {time.time() - start:.4f}秒")

# JAX 的懒执行
# 实际计算可能延迟到首次使用
result = large_array + 1
result.block_until_ready()  # 等待计算完成
```

### 数据类型选择

```python
# float32 vs float64
arr_32 = jnp.ones((1000, 1000), dtype=jnp.float32)  # 4 MB
arr_64 = jnp.ones((1000, 1000), dtype=jnp.float64)  # 8 MB

# 对于深度学习，float32 通常足够
# 对于科学计算，可能需要 float64
```

## ⚠️ 常见陷阱

### 1. arange vs linspace

```python
# arange：指定步长，不包含终点
a = jnp.arange(0, 1, 0.1)    # [0.0, 0.1, ..., 0.9]
print(len(a))  # 10

# linspace：指定数量，包含终点
l = jnp.linspace(0, 1, 10)   # [0.0, 0.111..., ..., 1.0]
print(len(l))  # 10

# 什么时候用哪个？
# - 已知步长 → arange
# - 已知数量 → linspace
```

### 2. 浮点数精度

```python
# 浮点数 arange 可能有精度问题
arr = jnp.arange(0.0, 1.0, 0.1)
print(len(arr))  # 可能不是 10！

# 推荐使用 linspace
arr = jnp.linspace(0, 1, 10, endpoint=False)
```

### 3. 形状参数

```python
# ✅ 正确：传递元组
zeros = jnp.zeros((3, 4))

# ❌ 错误：传递多个参数
# zeros = jnp.zeros(3, 4)  # TypeError!

# 1D 数组也需要元组
arr = jnp.zeros((5,))  # 注意逗号
```

## 💪 练习提示

在完成练习时，注意：

1. **检查形状**：使用 `print(arr.shape)` 验证
2. **测试边界情况**：空数组、单元素数组
3. **数据类型**：明确指定 dtype
4. **使用正确的函数**：根据需求选择 arange 或 linspace

## 🔗 相关资源

- [JAX 数组创建 API](https://jax.readthedocs.io/en/latest/jax.numpy.html#array-creation)
- [NumPy 数组创建教程](https://numpy.org/doc/stable/user/basics.creation.html)

## ✅ 检查清单

- [ ] 掌握 zeros, ones, full 的使用
- [ ] 理解单位矩阵的性质
- [ ] 能够使用 arange 和 linspace
- [ ] 知道何时使用哪个创建函数
- [ ] 理解不同函数的数学含义

---

准备好后，打开 `exercises/01_intro/intro02_arrays.py` 开始练习！
