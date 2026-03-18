# 形状变换

形状变换是深度学习和科学计算中的核心操作。掌握reshape、transpose等操作能让你灵活处理多维数据。

## 📚 知识要点

### 常用形状变换操作

| 操作 | 功能 | 使用场景 |
|------|------|----------|
| `reshape` | 改变数组形状 | 调整数据布局 |
| `transpose` | 转置数组 | 矩阵运算、通道变换 |
| `squeeze` | 删除尺寸为1的维度 | 简化数组结构 |
| `expand_dims` | 增加维度 | 广播准备 |
| `flatten` / `ravel` | 扁平化数组 | 向量化 |
| `swapaxes` | 交换两个轴 | 轴重排 |

## 🎯 学习目标

1. 理解数组形状变换的原理
2. 掌握 reshape 的使用和限制
3. 熟练进行矩阵转置
4. 学会维度的增加和删除
5. 理解内存布局的影响

## 🔬 数学原理

### 矩阵转置

对于矩阵 $\mathbf{A} \in \mathbb{R}^{m \times n}$，其转置 $\mathbf{A}^T \in \mathbb{R}^{n \times m}$ 定义为：

$$(\mathbf{A}^T)_{ij} = \mathbf{A}_{ji}$$

示例：

$$\mathbf{A} = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
\quad \Rightarrow \quad
\mathbf{A}^T = \begin{bmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{bmatrix}$$

性质：
- $(\mathbf{A}^T)^T = \mathbf{A}$
- $(\mathbf{AB})^T = \mathbf{B}^T\mathbf{A}^T$
- $(\mathbf{A} + \mathbf{B})^T = \mathbf{A}^T + \mathbf{B}^T$

### 向量化（Vectorization）

将矩阵 $\mathbf{A} \in \mathbb{R}^{m \times n}$ 转换为向量 $\text{vec}(\mathbf{A}) \in \mathbb{R}^{mn}$：

$$\text{vec}(\mathbf{A}) = \begin{bmatrix} a_{11} \\ a_{21} \\ \vdots \\ a_{m1} \\ a_{12} \\ \vdots \\ a_{mn} \end{bmatrix}$$

在 JAX 中对应 `flatten()` 或 `ravel()` 操作。

### Reshape 的数学解释

reshape 操作保持元素总数不变：

如果 $\mathbf{A}$ 形状为 $(m, n)$，reshape 为 $(p, q)$ 要求：

$$m \times n = p \times q$$

元素按行优先（C-order）或列优先（Fortran-order）重新排列。

## 📝 代码示例

### Reshape - 改变形状

```python
import jax.numpy as jnp

# 1D to 2D
arr = jnp.arange(12)
print(arr.shape)  # (12,)

# 重塑为 3x4
reshaped = arr.reshape(3, 4)
print(reshaped)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# 重塑为 2x6
reshaped2 = arr.reshape(2, 6)
print(reshaped2)
# [[ 0  1  2  3  4  5]
#  [ 6  7  8  9 10 11]]

# 使用 -1 自动推断维度
reshaped3 = arr.reshape(3, -1)  # 自动计算为 3x4
reshaped4 = arr.reshape(-1, 6)  # 自动计算为 2x6

# 扁平化
flattened = reshaped.reshape(-1)  # 或 reshaped.flatten()
print(flattened.shape)  # (12,)
```

### 多维 Reshape

```python
# 创建 3D 数组
arr_3d = jnp.arange(24).reshape(2, 3, 4)
print(arr_3d.shape)  # (2, 3, 4)

# 重塑为 2D
arr_2d = arr_3d.reshape(6, 4)
print(arr_2d.shape)  # (6, 4)

# 重塑为 4D
arr_4d = arr_3d.reshape(2, 3, 2, 2)
print(arr_4d.shape)  # (2, 3, 2, 2)

# 验证元素总数
print(2*3*4 == 6*4 == 2*3*2*2)  # True
```

### Transpose - 转置

```python
# 矩阵转置
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6]])
print(matrix.shape)  # (2, 3)

# 方法1: 使用 .T 属性
transposed = matrix.T
print(transposed.shape)  # (3, 2)
print(transposed)
# [[1 4]
#  [2 5]
#  [3 6]]

# 方法2: 使用 transpose()
transposed2 = jnp.transpose(matrix)  # 等价于 matrix.T
```

### 高维数组的轴转置

```python
# 3D 数组: (depth, height, width)
arr = jnp.arange(24).reshape(2, 3, 4)
print(arr.shape)  # (2, 3, 4)

# 默认转置：反转所有轴
transposed = arr.T
print(transposed.shape)  # (4, 3, 2)

# 指定轴的顺序
# 原始: (depth, height, width)
# 目标: (width, height, depth)
permuted = jnp.transpose(arr, (2, 1, 0))
print(permuted.shape)  # (4, 3, 2)

# 另一个例子: (batch, height, width, channels) -> (batch, channels, height, width)
images = jnp.zeros((32, 224, 224, 3))
channels_first = jnp.transpose(images, (0, 3, 1, 2))
print(channels_first.shape)  # (32, 3, 224, 224)
```

### Squeeze - 删除单维度

```python
# 创建包含单维度的数组
arr = jnp.ones((3, 1, 4, 1, 2))
print(arr.shape)  # (3, 1, 4, 1, 2)

# 删除所有尺寸为1的维度
squeezed = jnp.squeeze(arr)
print(squeezed.shape)  # (3, 4, 2)

# 删除指定轴的单维度
squeezed_axis1 = jnp.squeeze(arr, axis=1)
print(squeezed_axis1.shape)  # (3, 4, 1, 2)

squeezed_axis3 = jnp.squeeze(arr, axis=3)
print(squeezed_axis3.shape)  # (3, 1, 4, 2)

# 同时删除多个轴
squeezed_multi = jnp.squeeze(arr, axis=(1, 3))
print(squeezed_multi.shape)  # (3, 4, 2)
```

### Expand_dims - 增加维度

```python
# 1D 数组
arr = jnp.array([1, 2, 3])
print(arr.shape)  # (3,)

# 在前面增加维度
expanded = jnp.expand_dims(arr, axis=0)
print(expanded.shape)  # (1, 3)
print(expanded)  # [[1 2 3]]

# 在后面增加维度
expanded = jnp.expand_dims(arr, axis=1)
print(expanded.shape)  # (3, 1)
print(expanded)
# [[1]
#  [2]
#  [3]]

# 等价写法：使用 None 或 jnp.newaxis
expanded = arr[jnp.newaxis, :]  # (1, 3)
expanded = arr[:, jnp.newaxis]  # (3, 1)
expanded = arr[None, :]         # (1, 3)
```

### Flatten 和 Ravel

```python
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6]])

# flatten: 返回副本
flat1 = matrix.flatten()
print(flat1)  # [1 2 3 4 5 6]

# ravel: 可能返回视图（但在JAX中都是不可变的）
flat2 = jnp.ravel(matrix)
print(flat2)  # [1 2 3 4 5 6]

# 使用 reshape(-1) 也可以
flat3 = matrix.reshape(-1)
print(flat3)  # [1 2 3 4 5 6]

# 多维数组
arr_3d = jnp.arange(24).reshape(2, 3, 4)
flat = arr_3d.flatten()
print(flat.shape)  # (24,)
```

### Swapaxes - 交换轴

```python
arr = jnp.arange(24).reshape(2, 3, 4)
print(arr.shape)  # (2, 3, 4)

# 交换轴 0 和轴 2
swapped = jnp.swapaxes(arr, 0, 2)
print(swapped.shape)  # (4, 3, 2)

# 等价于 transpose
swapped2 = jnp.transpose(arr, (2, 1, 0))
print(jnp.allclose(swapped, swapped2))  # True
```

### Moveaxis - 移动轴

```python
arr = jnp.arange(24).reshape(2, 3, 4)
# shape: (2, 3, 4)

# 将轴 0 移动到最后
moved = jnp.moveaxis(arr, 0, -1)
print(moved.shape)  # (3, 4, 2)

# 将轴 2 移动到开头
moved = jnp.moveaxis(arr, 2, 0)
print(moved.shape)  # (4, 2, 3)

# 移动多个轴
moved = jnp.moveaxis(arr, [0, 2], [2, 0])
print(moved.shape)  # (4, 3, 2)
```

## 🎓 应用场景

### 图像数据格式转换

```python
# PyTorch: (batch, channels, height, width)
# TensorFlow: (batch, height, width, channels)

# PyTorch -> TensorFlow
pytorch_images = jnp.zeros((32, 3, 224, 224))
tf_images = jnp.transpose(pytorch_images, (0, 2, 3, 1))
print(tf_images.shape)  # (32, 224, 224, 3)

# TensorFlow -> PyTorch
tf_images = jnp.zeros((32, 224, 224, 3))
pytorch_images = jnp.transpose(tf_images, (0, 3, 1, 2))
print(pytorch_images.shape)  # (32, 3, 224, 224)
```

### 批量矩阵乘法准备

```python
# 准备批量矩阵乘法
batch_size = 10
A = jnp.ones((batch_size, 3, 4))  # 10个 3x4 矩阵
B = jnp.ones((batch_size, 4, 5))  # 10个 4x5 矩阵

# 使用 @ 进行批量矩阵乘法
C = A @ B  # (10, 3, 5)
```

### 全连接层输入准备

```python
# 卷积层输出: (batch, channels, height, width)
conv_output = jnp.ones((32, 128, 7, 7))

# 展平为全连接层输入
fc_input = conv_output.reshape(32, -1)
print(fc_input.shape)  # (32, 6272)

# 验证: 128 * 7 * 7 = 6272
```

### Attention 机制的形状操作

```python
def split_heads(x, num_heads):
    """
    将 (batch, seq_len, d_model) 分割为多头
    返回 (batch, num_heads, seq_len, depth)
    """
    batch, seq_len, d_model = x.shape
    depth = d_model // num_heads

    # 重塑并转置
    x = x.reshape(batch, seq_len, num_heads, depth)
    x = x.transpose(0, 2, 1, 3)
    return x

def merge_heads(x):
    """
    合并多头输出
    (batch, num_heads, seq_len, depth) -> (batch, seq_len, d_model)
    """
    batch, num_heads, seq_len, depth = x.shape

    # 转置并重塑
    x = x.transpose(0, 2, 1, 3)
    x = x.reshape(batch, seq_len, num_heads * depth)
    return x

# 测试
x = jnp.ones((2, 10, 512))  # batch=2, seq=10, d_model=512
split = split_heads(x, num_heads=8)
print(split.shape)  # (2, 8, 10, 64)

merged = merge_heads(split)
print(merged.shape)  # (2, 10, 512)
```

## ⚠️ 常见陷阱

### 1. Reshape 时元素总数必须匹配

```python
arr = jnp.arange(12)  # 12 个元素

# ✅ 正确: 3*4 = 12
reshaped = arr.reshape(3, 4)

# ❌ 错误: 3*5 = 15 ≠ 12
# reshaped = arr.reshape(3, 5)  # ValueError!
```

### 2. -1 只能出现一次

```python
arr = jnp.arange(12)

# ✅ 正确
reshaped = arr.reshape(3, -1)  # (3, 4)

# ❌ 错误
# reshaped = arr.reshape(-1, -1)  # ValueError!
```

### 3. Squeeze 只能删除尺寸为 1 的维度

```python
arr = jnp.ones((3, 4, 1))

# ✅ 正确：维度2的尺寸为1
squeezed = jnp.squeeze(arr, axis=2)  # (3, 4)

# ❌ 错误：维度0的尺寸为3
# squeezed = jnp.squeeze(arr, axis=0)  # ValueError!
```

### 4. Transpose 轴序号必须是排列

```python
arr = jnp.ones((2, 3, 4))

# ✅ 正确：(0, 1, 2) 的排列
transposed = jnp.transpose(arr, (2, 0, 1))

# ❌ 错误：重复的轴
# transposed = jnp.transpose(arr, (0, 0, 1))  # ValueError!

# ❌ 错误：缺少轴
# transposed = jnp.transpose(arr, (0, 1))  # ValueError!
```

### 5. 理解 flatten 的顺序

```python
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6]])

# C-order (行优先，默认)
flat_c = matrix.flatten()  # [1, 2, 3, 4, 5, 6]

# Fortran-order (列优先)
flat_f = matrix.flatten(order='F')  # [1, 4, 2, 5, 3, 6]
```

## 🔬 性能考虑

### Reshape vs Copy

```python
arr = jnp.arange(1000000)

# reshape 通常不复制数据（创建视图）
reshaped = arr.reshape(1000, 1000)

# 但在 JAX 中，由于不可变性，这个区别不如 NumPy 重要
# JAX 会自动优化内存使用
```

### 避免不必要的转置

```python
# ❌ 低效：多次转置
arr = jnp.ones((1000, 1000))
result = arr.T.T.T.T

# ✅ 高效：一次性转置
result = arr.T
```

## 💪 练习提示

1. **计算元素总数**：reshape 前后元素数量必须相等
2. **理解轴的含义**：特别是在高维数组中
3. **使用 -1 推断**：让 JAX 自动计算某个维度
4. **检查形状**：操作后验证 `result.shape`
5. **画图理解**：可视化形状变换过程

## 🔗 相关资源

- [NumPy 形状操作](https://numpy.org/doc/stable/reference/routines.array-manipulation.html)
- [深度学习中的形状变换](../04_neural_networks/overview.md)
- [广播机制](broadcasting.md)

## ✅ 检查清单

- [ ] 理解 reshape 的原理和限制
- [ ] 掌握矩阵转置的数学意义
- [ ] 能够操作高维数组的轴
- [ ] 理解 squeeze 和 expand_dims
- [ ] 知道何时使用 flatten/ravel
- [ ] 能够在不同数据格式间转换
- [ ] 理解形状变换对性能的影响

---

继续学习[广播机制](broadcasting.md)，这是形状操作的重要应用！
