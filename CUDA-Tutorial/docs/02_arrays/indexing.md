# 数组索引

数组索引是访问和提取数组元素的基本技能。掌握各种索引方式能让你灵活地处理数据。

## 📚 知识要点

### 索引的类型

1. **基础索引**：使用整数访问单个元素
2. **切片**：提取数组的连续部分
3. **布尔索引**：基于条件筛选元素
4. **整数数组索引**：使用整数数组提取特定位置的元素
5. **多维索引**：组合多个维度的索引

## 🎯 学习目标

1. 掌握一维和多维数组的索引
2. 熟练使用切片语法
3. 理解布尔索引的原理
4. 学会使用花式索引（Fancy Indexing）

## 💡 核心概念

### 索引从 0 开始

Python 和 JAX 使用 **0-based indexing**（零基索引）：

```python
arr = jnp.array([10, 20, 30, 40, 50])
#                 0   1   2   3   4  ← 索引
#                -5  -4  -3  -2  -1  ← 负索引
```

### 切片语法

```python
arr[start:stop:step]
```

- `start`：起始索引（包含）
- `stop`：结束索引（不包含）
- `step`：步长（默认为 1）

## 🔬 数学原理

### 向量的元素访问

给定向量 $\mathbf{x} = [x_0, x_1, x_2, \ldots, x_{n-1}]$：

- 访问第 $i$ 个元素：$x_i$ 对应 `x[i]`
- 访问最后一个元素：$x_{n-1}$ 对应 `x[-1]`

### 切片的数学表示

切片 `x[a:b]` 提取子向量：

$$\mathbf{y} = [x_a, x_{a+1}, \ldots, x_{b-1}]$$

长度为 $b - a$。

### 矩阵的元素访问

给定矩阵 $\mathbf{A} \in \mathbb{R}^{m \times n}$：

$$\mathbf{A} = \begin{bmatrix}
a_{0,0} & a_{0,1} & \cdots & a_{0,n-1} \\
a_{1,0} & a_{1,1} & \cdots & a_{1,n-1} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m-1,0} & a_{m-1,1} & \cdots & a_{m-1,n-1}
\end{bmatrix}$$

- 访问元素：$a_{i,j}$ 对应 `A[i, j]`
- 提取行：$\mathbf{A}_{i,:}$ 对应 `A[i, :]`
- 提取列：$\mathbf{A}_{:,j}$ 对应 `A[:, j]`

## 📝 代码示例

### 一维数组索引

```python
import jax.numpy as jnp

arr = jnp.array([10, 20, 30, 40, 50])

# 基础索引
print(arr[0])   # 10（第一个元素）
print(arr[2])   # 30（第三个元素）
print(arr[-1])  # 50（最后一个元素）
print(arr[-2])  # 40（倒数第二个元素）

# 切片
print(arr[1:4])    # [20 30 40]（索引 1, 2, 3）
print(arr[:3])     # [10 20 30]（前 3 个）
print(arr[2:])     # [30 40 50]（从索引 2 到末尾）
print(arr[::2])    # [10 30 50]（每隔一个）
print(arr[::-1])   # [50 40 30 20 10]（反转）
```

### 二维数组索引

```python
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]])

# 访问单个元素
print(matrix[0, 0])  # 1
print(matrix[1, 2])  # 6
print(matrix[-1, -1])  # 9

# 提取整行
print(matrix[0, :])  # [1 2 3]
print(matrix[1])     # [4 5 6]（简写）

# 提取整列
print(matrix[:, 0])  # [1 4 7]
print(matrix[:, 1])  # [2 5 8]

# 子矩阵
print(matrix[0:2, 1:3])
# [[2 3]
#  [5 6]]

# 行切片和列切片组合
print(matrix[::2, ::2])
# [[1 3]
#  [7 9]]
```

### 多维数组索引

```python
# 3D 数组：(depth, height, width)
arr_3d = jnp.arange(24).reshape(2, 3, 4)
print(arr_3d.shape)  # (2, 3, 4)

# 访问第一个"切片"
print(arr_3d[0])
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# 访问特定元素
print(arr_3d[0, 1, 2])  # 6

# 使用 ... (省略号)
print(arr_3d[..., 0])  # 所有深度和高度，第一列
# [[ 0  4  8]
#  [12 16 20]]

# 等价于
print(arr_3d[:, :, 0])
```

### 布尔索引

```python
arr = jnp.array([1, 2, 3, 4, 5, 6])

# 创建布尔掩码
mask = arr > 3
print(mask)  # [False False False True True True]

# 使用布尔索引提取元素
result = arr[mask]
print(result)  # [4 5 6]

# 一行写法
even_numbers = arr[arr % 2 == 0]
print(even_numbers)  # [2 4 6]

# 多条件
result = arr[(arr > 2) & (arr < 5)]
print(result)  # [3 4]
```

### 整数数组索引（花式索引）

```python
arr = jnp.array([10, 20, 30, 40, 50])

# 使用整数数组选择元素
indices = jnp.array([0, 2, 4])
result = arr[indices]
print(result)  # [10 30 50]

# 可以重复和重排
indices = jnp.array([1, 1, 3, 0])
result = arr[indices]
print(result)  # [20 20 40 10]

# 二维数组的花式索引
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]])

rows = jnp.array([0, 2, 1])
cols = jnp.array([1, 0, 2])
result = matrix[rows, cols]
print(result)  # [2, 7, 6]
# 提取 (0,1), (2,0), (1,2) 位置的元素
```

### 组合索引

```python
matrix = jnp.arange(20).reshape(4, 5)

# 基础索引 + 切片
print(matrix[0, 1:4])  # 第一行，列 1-3

# 切片 + 整数数组
indices = jnp.array([0, 2, 4])
print(matrix[0:2, indices])

# 布尔索引 + 切片
mask = jnp.array([True, False, True, False])
print(matrix[mask, :2])
```

## 🎓 应用场景

### 提取对角线

```python
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]])

# 主对角线
diag = jnp.diag(matrix)
print(diag)  # [1 5 9]

# 手动提取
indices = jnp.arange(3)
diag_manual = matrix[indices, indices]
print(diag_manual)  # [1 5 9]
```

### 数据筛选

```python
# 学生成绩数据
scores = jnp.array([85, 92, 78, 90, 88, 76, 95, 89])

# 找出优秀成绩（>= 90）
excellent = scores[scores >= 90]
print(excellent)  # [92 90 95]

# 找出不及格成绩的索引
failing_indices = jnp.where(scores < 60)[0]
print(failing_indices)  # []（没有不及格）
```

### 批量处理

```python
# 图像批次：(batch_size, height, width, channels)
images = jnp.ones((32, 224, 224, 3))

# 提取前 5 张图像
first_five = images[:5]
print(first_five.shape)  # (5, 224, 224, 3)

# 提取所有图像的红色通道
red_channel = images[:, :, :, 0]
print(red_channel.shape)  # (32, 224, 224)

# 提取中心 100x100 的区域
center = images[:, 62:162, 62:162, :]
print(center.shape)  # (32, 100, 100, 3)
```

### Top-K 选择

```python
arr = jnp.array([3, 1, 4, 1, 5, 9, 2, 6])

# 找出最大的 3 个元素的索引
k = 3
top_k_indices = jnp.argsort(arr)[-k:]
print(top_k_indices)  # [4 5 7]

# 提取最大的 3 个元素
top_k_values = arr[top_k_indices]
print(top_k_values)  # [5 9 6]

# 降序排列
top_k_values_sorted = arr[jnp.argsort(arr)[-k:][::-1]]
print(top_k_values_sorted)  # [9 6 5]
```

## ⚠️ 常见陷阱

### 1. 切片不包含结束索引

```python
arr = jnp.array([0, 1, 2, 3, 4])

# arr[1:4] 包含索引 1, 2, 3，不包含 4
print(arr[1:4])  # [1 2 3]

# 要包含索引 4，需要写 arr[1:5]
print(arr[1:5])  # [1 2 3 4]
```

### 2. 负索引的理解

```python
arr = jnp.array([0, 1, 2, 3, 4])

# arr[-1] 是最后一个元素
print(arr[-1])  # 4

# arr[:-1] 是除了最后一个元素的所有元素
print(arr[:-1])  # [0 1 2 3]

# arr[-3:] 是最后 3 个元素
print(arr[-3:])  # [2 3 4]
```

### 3. 多维索引的逗号

```python
matrix = jnp.arange(12).reshape(3, 4)

# ✅ 正确：使用逗号分隔维度
print(matrix[0, 1])  # 1

# ❌ 错误：使用多个方括号
# print(matrix[0][1])  # 在 JAX 中效率较低

# ✅ 正确：切片也使用逗号
print(matrix[0:2, 1:3])
```

### 4. 布尔索引的广播

```python
arr = jnp.array([1, 2, 3, 4, 5])

# ✅ 正确：掩码形状匹配
mask = arr > 2
result = arr[mask]  # [3 4 5]

# ❌ 错误：掩码形状不匹配
# mask = jnp.array([True, False])
# result = arr[mask]  # 错误！
```

### 5. JAX 的不可变性

```python
arr = jnp.array([1, 2, 3, 4, 5])

# ❌ 错误：不能直接修改
# arr[0] = 10  # TypeError!

# ✅ 正确：使用 .at[] 进行函数式更新
arr = arr.at[0].set(10)
print(arr)  # [10  2  3  4  5]
```

## 🔬 性能优化

### 使用切片而非循环

```python
arr = jnp.arange(1000000)

# ❌ 慢：使用循环
result = jnp.array([arr[i] for i in range(100)])

# ✅ 快：使用切片
result = arr[:100]
```

### 布尔索引 vs where

```python
arr = jnp.arange(1000)

# 布尔索引：提取满足条件的元素
result1 = arr[arr > 500]

# where：获取满足条件的索引
indices = jnp.where(arr > 500)[0]
result2 = arr[indices]

# 两者等价，但布尔索引更简洁
```

## 💪 练习提示

在完成练习时，注意：

1. **验证索引范围**：确保不越界
2. **检查结果形状**：索引后的形状是否符合预期
3. **理解切片语义**：start、stop、step 的含义
4. **熟悉负索引**：从数组末尾开始索引
5. **掌握多维索引**：每个维度独立索引

## 🔗 相关资源

- [NumPy 索引文档](https://numpy.org/doc/stable/user/basics.indexing.html)
- [JAX 数组 API](https://jax.readthedocs.io/en/latest/jax.numpy.html)
- [高级索引](advanced_indexing.md)

## ✅ 检查清单

- [ ] 掌握一维数组的索引和切片
- [ ] 能够索引多维数组
- [ ] 理解负索引的使用
- [ ] 掌握布尔索引
- [ ] 会使用整数数组索引
- [ ] 理解索引和切片的性能差异
- [ ] 知道 JAX 索引与 NumPy 的区别

---

掌握索引后，继续学习[形状变换](reshaping.md)！
