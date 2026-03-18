# 数组操作概述

掌握数组操作是高效使用 JAX 的关键。本章将深入学习数组的索引、形状变换、广播机制等核心概念。

## 🎯 学习目标

通过本章的学习，你将掌握：

1. **数组索引**：灵活访问和提取数组元素
2. **形状变换**：重塑和转置多维数组
3. **广播机制**：理解 JAX 如何自动扩展数组形状
4. **函数式更新**：在不可变数组上执行修改操作

## 📚 章节内容

### 01. 数组索引

学习各种索引方式：
- 基础索引和切片
- 多维数组索引
- 布尔索引和整数数组索引
- 花式索引（Fancy Indexing）

### 02. 形状变换

掌握数组形状操作：
- `reshape`：改变数组形状
- `transpose`：转置和轴重排
- `squeeze` 和 `expand_dims`：维度操作
- `flatten` 和 `ravel`：数组扁平化

### 03. 广播机制

理解 JAX 的自动形状匹配：
- 广播规则
- 常见广播模式
- 广播在神经网络中的应用
- 避免广播错误

### 04. 高级索引

学习函数式数组更新：
- `.at[]` 语法
- 函数式 set、add、min、max
- 批量更新
- 与 NumPy 的区别

## 🔬 为什么数组操作很重要？

### 在深度学习中的应用

```python
# 批量处理图像
images = jnp.zeros((32, 224, 224, 3))  # (batch, height, width, channels)

# 重塑为线性层输入
flattened = images.reshape(32, -1)  # (32, 150528)

# 转置为通道优先
channels_first = images.transpose(0, 3, 1, 2)  # (32, 3, 224, 224)
```

### 在科学计算中的应用

```python
# 处理时间序列数据
timeseries = jnp.zeros((100, 50, 10))  # (time, sensors, features)

# 提取特定传感器的数据
sensor_1 = timeseries[:, 0, :]  # (100, 10)

# 计算所有传感器的均值
mean_values = jnp.mean(timeseries, axis=(0, 1))  # (10,)
```

## 💡 核心概念

### 数组的内存布局

理解数组在内存中的存储方式：

```
1D 数组: [1, 2, 3, 4]
内存: [1][2][3][4]

2D 数组 (C-contiguous):
[[1, 2, 3],
 [4, 5, 6]]
内存: [1][2][3][4][5][6]
```

### 视图 vs 副本

JAX 数组是不可变的，但某些操作可能返回视图（view）或副本（copy）：

```python
# 视图：共享底层数据（高效）
sliced = arr[1:3]

# 副本：创建新数组（内存开销）
reshaped = arr.reshape(new_shape)
```

**重要**：在 JAX 中，由于不可变性，这个区别不如 NumPy 中重要。

## 🎓 学习路径

建议按以下顺序学习：

```mermaid
graph LR
    A[数组索引] --> B[形状变换]
    B --> C[广播机制]
    C --> D[高级索引]
    D --> E[实战应用]
```

1. **基础**：先掌握索引和切片
2. **进阶**：学习形状变换
3. **核心**：理解广播机制
4. **高级**：掌握函数式更新
5. **应用**：在实际项目中运用

## 🔍 关键技能

### 形状推断

训练直觉判断操作后的形状：

```python
x = jnp.zeros((3, 4, 5))

# 能快速判断结果形状吗？
x[0].shape          # (4, 5)
x[:, 0].shape       # (3, 5)
x.T.shape           # (5, 4, 3)
x.reshape(-1).shape # (60,)
```

### 轴的理解

清晰理解多维数组的轴：

```python
arr = jnp.zeros((2, 3, 4, 5))
# axis 0: batch (2)
# axis 1: channels (3)
# axis 2: height (4)
# axis 3: width (5)

# 沿 height 求平均
mean_height = jnp.mean(arr, axis=2)  # (2, 3, 5)
```

## ⚡ 性能提示

### 1. 避免不必要的复制

```python
# ❌ 创建不必要的中间数组
temp = x.reshape(...)
result = temp.transpose(...)

# ✅ 链式操作
result = x.reshape(...).transpose(...)
```

### 2. 使用合适的操作

```python
# ❌ 使用循环
result = jnp.array([arr[i, i] for i in range(n)])

# ✅ 使用对角线提取
result = jnp.diag(arr)
```

### 3. 利用广播避免显式扩展

```python
# ❌ 显式平铺
x_tiled = jnp.tile(x, (10, 1))
result = x_tiled + y

# ✅ 利用广播
result = x + y  # 自动广播
```

## 🛠️ 调试技巧

### 使用 shape 属性

```python
print(f"Input shape: {x.shape}")
result = some_operation(x)
print(f"Output shape: {result.shape}")
```

### 使用断言验证形状

```python
def process_batch(images):
    assert images.shape[0] == 32, "Batch size must be 32"
    assert images.shape[-1] == 3, "Images must be RGB"
    return process(images)
```

### 可视化数组形状

```python
def print_array_info(arr, name="Array"):
    print(f"{name}:")
    print(f"  Shape: {arr.shape}")
    print(f"  Dtype: {arr.dtype}")
    print(f"  Size: {arr.size}")
    print(f"  NDim: {arr.ndim}")
```

## 🎯 实战场景

### 图像处理

```python
# 批量图像标准化
def normalize_batch(images):
    # images: (batch, height, width, channels)
    mean = jnp.mean(images, axis=(1, 2), keepdims=True)
    std = jnp.std(images, axis=(1, 2), keepdims=True)
    return (images - mean) / (std + 1e-8)
```

### 时间序列处理

```python
# 滑动窗口
def create_windows(data, window_size):
    # data: (time_steps, features)
    n = len(data) - window_size + 1
    windows = jnp.array([data[i:i+window_size] for i in range(n)])
    return windows  # (n, window_size, features)
```

### 注意力机制

```python
# Multi-head attention 的形状操作
def split_heads(x, num_heads):
    # x: (batch, seq_len, d_model)
    batch, seq_len, d_model = x.shape
    depth = d_model // num_heads

    x = x.reshape(batch, seq_len, num_heads, depth)
    return x.transpose(0, 2, 1, 3)  # (batch, num_heads, seq_len, depth)
```

## 📖 配套练习

| 练习 | 难度 | 重点 |
|------|------|------|
| arrays01_indexing | ⭐⭐ | 基础索引和切片 |
| arrays02_reshaping | ⭐⭐ | 形状变换 |
| arrays03_broadcasting | ⭐⭐⭐ | 广播规则 |
| arrays04_advanced_indexing | ⭐⭐⭐ | 函数式更新 |

## 🔗 相关资源

- [JAX 数组 API](https://jax.readthedocs.io/en/latest/jax.numpy.html)
- [NumPy 索引教程](https://numpy.org/doc/stable/user/basics.indexing.html)
- [广播机制详解](broadcasting.md)

## ✅ 学习检查清单

完成本章后，你应该能够：

- [ ] 熟练使用各种索引方式提取数据
- [ ] 灵活进行数组形状变换
- [ ] 理解并运用广播机制
- [ ] 使用 `.at[]` 进行函数式更新
- [ ] 在实际问题中选择合适的数组操作
- [ ] 预测操作后的数组形状
- [ ] 编写高效的向量化代码

---

准备好后，让我们从[数组索引](indexing.md)开始吧！
