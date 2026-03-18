# 广播机制

广播（Broadcasting）是 JAX 和 NumPy 中最强大的特性之一，它允许不同形状的数组进行算术运算。

## 📚 知识要点

### 什么是广播？

广播是一种自动扩展数组形状的机制，使得不同形状的数组可以进行逐元素运算，而无需显式复制数据。

**核心优势**：
- **内存高效**：无需创建大型数组的副本
- **计算高效**：向量化操作比循环快得多
- **代码简洁**：自动处理形状匹配

## 🎯 学习目标

1. 理解广播的三条规则
2. 掌握常见的广播模式
3. 学会预测广播后的形状
4. 避免常见的广播错误
5. 在实际问题中灵活运用广播

## 🔬 数学原理

### 向量加标量的广播

数学上，向量 $\mathbf{x} \in \mathbb{R}^n$ 加标量 $c$：

$$\mathbf{x} + c = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix} + c = \begin{bmatrix} x_1 + c \\ x_2 + c \\ \vdots \\ x_n + c \end{bmatrix}$$

标量 $c$ 被"广播"到每个元素。

### 矩阵加向量的广播

矩阵 $\mathbf{A} \in \mathbb{R}^{m \times n}$ 加行向量 $\mathbf{b} \in \mathbb{R}^{1 \times n}$：

$$\mathbf{A} + \mathbf{b} = \begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{bmatrix} + \begin{bmatrix} b_1 & b_2 & \cdots & b_n \end{bmatrix}$$

$$= \begin{bmatrix}
a_{11}+b_1 & a_{12}+b_2 & \cdots & a_{1n}+b_n \\
a_{21}+b_1 & a_{22}+b_2 & \cdots & a_{2n}+b_n \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1}+b_1 & a_{m2}+b_2 & \cdots & a_{mn}+b_n
\end{bmatrix}$$

向量 $\mathbf{b}$ 被复制 $m$ 次以匹配矩阵的行数。

## 💡 广播规则

### 三条核心规则

广播遵循以下规则：

**规则 1**：如果两个数组的维度数不同，较小维度的数组在左侧填充 1。

**规则 2**：如果两个数组在某个维度上的尺寸不同，尺寸为 1 的维度会被扩展以匹配另一个数组。

**规则 3**：如果两个数组在某个维度上的尺寸都不是 1 且不相等，则报错。

### 规则应用示例

```python
# 示例 1: 标量与数组
a: (3, 4)
b: ()       # 标量
# 步骤1: b -> (1, 1)  # 填充维度
# 步骤2: b -> (3, 4)  # 扩展维度
# 结果: (3, 4)

# 示例 2: 一维与二维
a: (3, 4)
b: (4,)
# 步骤1: b -> (1, 4)  # 填充维度
# 步骤2: b -> (3, 4)  # 扩展维度
# 结果: (3, 4)

# 示例 3: 兼容的形状
a: (3, 1, 4)
b: (1, 5, 4)
# 步骤2: 维度0: 3 vs 1 -> 扩展为 3
#        维度1: 1 vs 5 -> 扩展为 5
#        维度2: 4 vs 4 -> 保持 4
# 结果: (3, 5, 4)

# 示例 4: 不兼容的形状
a: (3, 4)
b: (5, 4)
# 维度0: 3 vs 5 -> 都不是1，且不相等 -> 错误！
```

## 📝 代码示例

### 基础广播

```python
import jax.numpy as jnp

# 1. 标量广播
arr = jnp.array([1, 2, 3, 4])
result = arr + 10
print(result)  # [11 12 13 14]

# 等价于（但不会真的这样实现）：
# scalar_expanded = jnp.array([10, 10, 10, 10])
# result = arr + scalar_expanded

# 2. 一维广播到二维
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6]])  # (2, 3)
vector = jnp.array([10, 20, 30])  # (3,)

result = matrix + vector
print(result)
# [[11 22 33]
#  [14 25 36]]

# vector 被广播为:
# [[10 20 30]
#  [10 20 30]]
```

### 不同形状的广播

```python
# 行向量 + 列向量
row = jnp.array([[1, 2, 3]])        # (1, 3)
col = jnp.array([[10], [20], [30]]) # (3, 1)

result = row + col
print(result.shape)  # (3, 3)
print(result)
# [[11 12 13]
#  [21 22 23]
#  [31 32 33]]

# 广播过程：
# row: (1, 3) -> (3, 3)
# col: (3, 1) -> (3, 3)
```

### 三维广播

```python
# 三维数组与二维数组
a = jnp.ones((2, 3, 4))  # (2, 3, 4)
b = jnp.ones((3, 4))     # (3, 4)

result = a + b
print(result.shape)  # (2, 3, 4)

# b 的形状变化: (3, 4) -> (1, 3, 4) -> (2, 3, 4)

# 三维数组与一维数组
a = jnp.ones((2, 3, 4))  # (2, 3, 4)
b = jnp.ones((4,))       # (4,)

result = a + b
print(result.shape)  # (2, 3, 4)

# b 的形状变化: (4,) -> (1, 1, 4) -> (2, 3, 4)
```

### 显式形状准备

```python
# 有时需要显式调整形状以匹配广播需求

# 情况1: 列向量
vector = jnp.array([1, 2, 3])  # (3,)
col_vector = vector[:, jnp.newaxis]  # (3, 1)
# 或
col_vector = jnp.expand_dims(vector, axis=1)

matrix = jnp.ones((3, 4))
result = matrix + col_vector  # 每行加不同的值

# 情况2: 批量操作
batch_data = jnp.ones((32, 10))  # 32个样本，每个10维
mean = jnp.mean(batch_data, axis=0)  # (10,)

# 标准化：需要广播
normalized = batch_data - mean  # (32, 10) - (10,) = (32, 10)

# 如果要沿另一个轴
mean_per_sample = jnp.mean(batch_data, axis=1, keepdims=True)  # (32, 1)
normalized2 = batch_data - mean_per_sample  # (32, 10) - (32, 1) = (32, 10)
```

## 🎓 应用场景

### 批量归一化

```python
def batch_normalize(x):
    """
    对每个特征进行归一化
    x: (batch_size, num_features)
    """
    mean = jnp.mean(x, axis=0)      # (num_features,)
    std = jnp.std(x, axis=0)        # (num_features,)

    # 广播减法和除法
    normalized = (x - mean) / (std + 1e-8)
    return normalized

# 测试
x = jnp.array([[1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0],
                [7.0, 8.0, 9.0]])
result = batch_normalize(x)
print(jnp.mean(result, axis=0))  # ~[0, 0, 0]
print(jnp.std(result, axis=0))   # ~[1, 1, 1]
```

### 距离矩阵计算

```python
def pairwise_distance(x, y):
    """
    计算两组点之间的欧氏距离
    x: (n, d) - n个d维点
    y: (m, d) - m个d维点
    返回: (n, m) 距离矩阵
    """
    # 利用 ||a - b||^2 = ||a||^2 + ||b||^2 - 2*a·b

    # x: (n, d) -> (n, 1, d)
    # y: (m, d) -> (1, m, d)
    x_expanded = x[:, jnp.newaxis, :]  # (n, 1, d)
    y_expanded = y[jnp.newaxis, :, :]  # (1, m, d)

    # 广播相减和平方
    diff = x_expanded - y_expanded  # (n, m, d)
    dist_squared = jnp.sum(diff ** 2, axis=2)  # (n, m)
    return jnp.sqrt(dist_squared)

# 测试
x = jnp.array([[0, 0], [1, 1]])  # 2个2D点
y = jnp.array([[1, 0], [0, 1], [1, 1]])  # 3个2D点
distances = pairwise_distance(x, y)
print(distances.shape)  # (2, 3)
```

### 图像处理

```python
# 图像批次: (batch, height, width, channels)
images = jnp.ones((32, 224, 224, 3))

# 每个通道的均值和标准差
channel_mean = jnp.array([0.485, 0.456, 0.406])  # (3,)
channel_std = jnp.array([0.229, 0.224, 0.225])   # (3,)

# 标准化所有图像
# (32, 224, 224, 3) - (3,) -> 广播
normalized_images = (images - channel_mean) / channel_std

# channel_mean 被广播为 (1, 1, 1, 3) 然后扩展到 (32, 224, 224, 3)
```

### Softmax 温度缩放

```python
def softmax_with_temperature(logits, temperature=1.0):
    """
    logits: (batch, num_classes)
    temperature: 标量
    """
    # temperature 标量会广播到整个数组
    scaled_logits = logits / temperature

    # 数值稳定的 softmax
    max_logits = jnp.max(scaled_logits, axis=1, keepdims=True)  # (batch, 1)
    exp_logits = jnp.exp(scaled_logits - max_logits)  # 广播减法
    sum_exp = jnp.sum(exp_logits, axis=1, keepdims=True)  # (batch, 1)
    return exp_logits / sum_exp  # 广播除法

# 测试
logits = jnp.array([[1.0, 2.0, 3.0],
                     [1.0, 2.0, 3.0]])
probs = softmax_with_temperature(logits, temperature=2.0)
print(probs.sum(axis=1))  # [1., 1.]
```

### 注意力掩码

```python
def create_causal_mask(seq_len):
    """创建因果注意力掩码"""
    # 使用广播创建下三角矩阵
    i = jnp.arange(seq_len)[:, jnp.newaxis]  # (seq_len, 1)
    j = jnp.arange(seq_len)[jnp.newaxis, :]  # (1, seq_len)

    mask = i >= j  # 广播比较 (seq_len, seq_len)
    return mask

mask = create_causal_mask(5)
print(mask.astype(int))
# [[1 0 0 0 0]
#  [1 1 0 0 0]
#  [1 1 1 0 0]
#  [1 1 1 1 0]
#  [1 1 1 1 1]]
```

## ⚠️ 常见陷阱

### 1. 不兼容的形状

```python
a = jnp.ones((3, 4))
b = jnp.ones((3, 5))

# ❌ 错误：维度1不兼容 (4 vs 5)
# result = a + b  # ValueError!

# ✅ 正确：确保形状兼容
b = jnp.ones((3, 4))
result = a + b
```

### 2. 意外的广播方向

```python
matrix = jnp.ones((3, 4))
vector = jnp.ones((3,))

# 期望：向每一列加向量（列广播）
# 实际：向每一行加向量（行广播）
result = matrix + vector  # 错误的方向！

# ✅ 正确：调整向量形状
vector_col = vector[:, jnp.newaxis]  # (3, 1)
result = matrix + vector_col  # 每列加不同的值
```

### 3. 广播导致的内存问题

```python
# ❌ 低效：创建大型中间数组
a = jnp.ones((10000, 1))
b = jnp.ones((1, 10000))
result = a + b  # 创建 (10000, 10000) 的数组！

# ✅ 更好：避免不必要的大型广播
# 重新思考算法，可能不需要完整的矩阵
```

### 4. keepdims 的重要性

```python
matrix = jnp.ones((3, 4))

# ❌ 容易出错
mean = jnp.mean(matrix, axis=0)  # (4,)
# mean 会沿最后一个维度广播，不是你想要的！

# ✅ 正确：保持维度
mean = jnp.mean(matrix, axis=0, keepdims=True)  # (1, 4)
result = matrix - mean  # 正确的广播
```

### 5. 广播与性能

```python
import time

n = 1000
a = jnp.ones((n, n))
b = jnp.ones((n,))

# 两种写法在 JAX 中性能相似（都使用广播）
start = time.time()
result1 = a + b
result1.block_until_ready()
print(f"广播: {time.time() - start:.4f}秒")

start = time.time()
result2 = a + jnp.tile(b, (n, 1))
result2.block_until_ready()
print(f"显式平铺: {time.time() - start:.4f}秒")

# 广播通常更快，因为不需要实际复制数据
```

## 🔬 调试技巧

### 预测广播形状

```python
def broadcast_shapes(shape1, shape2):
    """预测两个形状广播后的结果"""
    # 填充到相同长度
    ndim = max(len(shape1), len(shape2))
    shape1 = (1,) * (ndim - len(shape1)) + tuple(shape1)
    shape2 = (1,) * (ndim - len(shape2)) + tuple(shape2)

    # 应用广播规则
    result_shape = []
    for s1, s2 in zip(shape1, shape2):
        if s1 == s2:
            result_shape.append(s1)
        elif s1 == 1:
            result_shape.append(s2)
        elif s2 == 1:
            result_shape.append(s1)
        else:
            raise ValueError(f"不兼容的维度: {s1} vs {s2}")

    return tuple(result_shape)

# 测试
print(broadcast_shapes((3, 4), (4,)))      # (3, 4)
print(broadcast_shapes((3, 1), (1, 4)))    # (3, 4)
print(broadcast_shapes((2, 3, 4), (3, 4))) # (2, 3, 4)
```

### 使用 jnp.broadcast_shapes

```python
# JAX 提供了内置函数
result = jnp.broadcast_shapes((3, 4), (4,))
print(result)  # (3, 4)

result = jnp.broadcast_shapes((3, 1, 4), (1, 5, 4))
print(result)  # (3, 5, 4)
```

## 💪 练习提示

1. **画图理解**：可视化广播过程
2. **预测形状**：在运行前先推理结果形状
3. **使用 keepdims**：归约操作时保持维度
4. **显式 expand_dims**：使意图更清晰
5. **测试边界情况**：标量、空数组、大型数组

## 🔗 相关资源

- [NumPy 广播文档](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [广播可视化工具](http://scipy.github.io/old-wiki/pages/EricsBroadcastingDoc)
- [形状变换](reshaping.md)

## ✅ 检查清单

- [ ] 理解广播的三条规则
- [ ] 能够预测广播后的形状
- [ ] 掌握 keepdims 的使用
- [ ] 知道如何避免意外的广播
- [ ] 能够在实际问题中运用广播
- [ ] 理解广播对性能的影响
- [ ] 会调试广播相关的错误

---

掌握广播后，学习[高级索引](advanced_indexing.md)来完成数组操作的学习！
