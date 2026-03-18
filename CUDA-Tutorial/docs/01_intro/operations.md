# 基本运算

学习 JAX 中的基本数组运算，这是所有数值计算的基础。

## 📚 知识要点

### 数组运算的分类

JAX 提供了丰富的数组运算：

1. **逐元素运算**：加减乘除、幂运算
2. **归约运算**：求和、求积、最大最小值
3. **矩阵运算**：矩阵乘法、点积
4. **统计运算**：均值、方差、标准差

## 🎯 学习目标

1. 掌握基本的算术运算
2. 理解向量化操作的优势
3. 学会使用归约函数
4. 掌握矩阵乘法的使用

## 💡 核心概念

### 逐元素运算（Element-wise Operations）

对数组的每个元素独立执行相同的操作。

### 广播（Broadcasting）

自动扩展数组形状以匹配操作（后续章节详细讲解）。

### 归约（Reduction）

将数组沿某个轴降维，得到聚合结果。

## 🔬 数学原理

### 向量的逐元素运算

给定向量 $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n$：

**加法**：
$$(\mathbf{x} + \mathbf{y})_i = x_i + y_i$$

**乘法**（Hadamard 积）：
$$(\mathbf{x} \odot \mathbf{y})_i = x_i \cdot y_i$$

```python
x = jnp.array([1, 2, 3])
y = jnp.array([4, 5, 6])

x + y  # [5, 7, 9]
x * y  # [4, 10, 18]
```

### 向量的点积（Dot Product）

数学定义：
$$\mathbf{x} \cdot \mathbf{y} = \sum_{i=1}^n x_i y_i = x_1 y_1 + x_2 y_2 + \cdots + x_n y_n$$

几何意义：
$$\mathbf{x} \cdot \mathbf{y} = \|\mathbf{x}\| \|\mathbf{y}\| \cos\theta$$

其中 $\theta$ 是两向量的夹角。

```python
x = jnp.array([1, 2, 3])
y = jnp.array([4, 5, 6])

dot_product = jnp.dot(x, y)  # 1*4 + 2*5 + 3*6 = 32
```

### 矩阵乘法（Matrix Multiplication）

对于矩阵 $\mathbf{A} \in \mathbb{R}^{m \times n}$ 和 $\mathbf{B} \in \mathbb{R}^{n \times p}$：

$$(\mathbf{A}\mathbf{B})_{ij} = \sum_{k=1}^n A_{ik} B_{kj}$$

结果矩阵 $\mathbf{C} \in \mathbb{R}^{m \times p}$。

**重要**：矩阵乘法不满足交换律：$\mathbf{AB} \neq \mathbf{BA}$

```python
A = jnp.array([[1, 2], [3, 4]])  # 2x2
B = jnp.array([[5, 6], [7, 8]])  # 2x2

C = jnp.dot(A, B)  # 或 A @ B
# [[19 22]
#  [43 50]]
```

验证计算：
- $C_{00} = 1 \times 5 + 2 \times 7 = 19$
- $C_{01} = 1 \times 6 + 2 \times 8 = 22$
- $C_{10} = 3 \times 5 + 4 \times 7 = 43$
- $C_{11} = 3 \times 6 + 4 \times 8 = 50$

### 归约运算

**求和**：
$$\sum_{i=1}^n x_i$$

**平均值**：
$$\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i$$

**方差**：
$$\sigma^2 = \frac{1}{n}\sum_{i=1}^n (x_i - \bar{x})^2$$

**标准差**：
$$\sigma = \sqrt{\sigma^2}$$

## 📝 代码示例

### 基本算术运算

```python
import jax.numpy as jnp

x = jnp.array([1, 2, 3, 4])

# 加减乘除
print(x + 10)    # [11 12 13 14]
print(x - 2)     # [-1  0  1  2]
print(x * 3)     # [3 6 9 12]
print(x / 2)     # [0.5 1.  1.5 2. ]

# 幂运算
print(x ** 2)    # [1 4 9 16]
print(jnp.sqrt(x))  # [1. 1.414... 1.732... 2.]

# 数组间运算
y = jnp.array([5, 6, 7, 8])
print(x + y)     # [6 8 10 12]
print(x * y)     # [5 12 21 32]
```

### 数学函数

```python
x = jnp.linspace(0, jnp.pi, 5)

# 三角函数
print(jnp.sin(x))
print(jnp.cos(x))
print(jnp.tan(x))

# 指数和对数
print(jnp.exp(x))
print(jnp.log(x + 1))  # 自然对数
print(jnp.log10(x + 1))  # 常用对数

# 绝对值和符号
x = jnp.array([-1, -2, 3, 4])
print(jnp.abs(x))   # [1 2 3 4]
print(jnp.sign(x))  # [-1 -1 1 1]
```

### 归约运算

```python
x = jnp.array([1, 2, 3, 4, 5])

# 求和
total = jnp.sum(x)  # 15

# 累积和
cumsum = jnp.cumsum(x)  # [1, 3, 6, 10, 15]

# 求积
product = jnp.prod(x)  # 120

# 最大最小值
max_val = jnp.max(x)  # 5
min_val = jnp.min(x)  # 1

# 最大最小值的索引
argmax = jnp.argmax(x)  # 4
argmin = jnp.argmin(x)  # 0
```

### 统计运算

```python
x = jnp.array([1.0, 2.0, 3.0, 4.0, 5.0])

# 平均值
mean = jnp.mean(x)  # 3.0

# 中位数
median = jnp.median(x)  # 3.0

# 方差
variance = jnp.var(x)  # 2.0

# 标准差
std = jnp.std(x)  # 1.414...

# 验证方差计算
manual_var = jnp.mean((x - jnp.mean(x)) ** 2)
print(manual_var)  # 2.0
```

### 多维数组的轴归约

```python
# 2D 数组
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6]])

# 全局求和
total = jnp.sum(matrix)  # 21

# 按行求和（沿 axis=0）
col_sums = jnp.sum(matrix, axis=0)  # [5, 7, 9]

# 按列求和（沿 axis=1）
row_sums = jnp.sum(matrix, axis=1)  # [6, 15]

# 保持维度
row_sums_kept = jnp.sum(matrix, axis=1, keepdims=True)
print(row_sums_kept.shape)  # (2, 1)
```

轴的理解：
```
matrix = [[1, 2, 3],    ← axis=1 (行)
          [4, 5, 6]]
          ↑ axis=0 (列)
```

### 矩阵运算

```python
# 向量点积
a = jnp.array([1, 2, 3])
b = jnp.array([4, 5, 6])
dot = jnp.dot(a, b)  # 32

# 矩阵-向量乘法
A = jnp.array([[1, 2], [3, 4]])
x = jnp.array([5, 6])
y = jnp.dot(A, x)  # [17, 39]

# 矩阵-矩阵乘法
B = jnp.array([[7, 8], [9, 10]])
C = jnp.dot(A, B)  # 或 A @ B

# matmul 运算符（推荐）
C = A @ B  # 与 jnp.dot(A, B) 相同

# 转置
A_T = A.T
print(A_T)
# [[1 3]
#  [2 4]]

# 矩阵的迹（对角线和）
trace = jnp.trace(A)  # 1 + 4 = 5
```

## 🎓 应用场景

### 线性回归

```python
# y = Wx + b
def linear_regression(W, x, b):
    """
    W: (output_dim, input_dim) 权重矩阵
    x: (input_dim,) 输入向量
    b: (output_dim,) 偏置向量
    """
    return jnp.dot(W, x) + b

W = jnp.array([[1, 2, 3], [4, 5, 6]])  # 2x3
x = jnp.array([1, 2, 3])                # 3
b = jnp.array([0.1, 0.2])               # 2

y = linear_regression(W, x, b)
print(y)  # [14.1, 32.2]
```

### 标准化

```python
# Z-score 标准化
def normalize(x):
    """将数据标准化为均值0，标准差1"""
    mean = jnp.mean(x)
    std = jnp.std(x)
    return (x - mean) / std

data = jnp.array([1.0, 2.0, 3.0, 4.0, 5.0])
normalized = normalize(data)
print(jnp.mean(normalized))  # ~0.0
print(jnp.std(normalized))   # ~1.0
```

### 余弦相似度

```python
def cosine_similarity(a, b):
    """
    计算两个向量的余弦相似度
    cos(θ) = (a·b) / (||a|| ||b||)
    """
    dot_product = jnp.dot(a, b)
    norm_a = jnp.linalg.norm(a)
    norm_b = jnp.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

a = jnp.array([1, 2, 3])
b = jnp.array([4, 5, 6])
similarity = cosine_similarity(a, b)
print(similarity)  # 0.974...（非常相似）
```

## ⚠️ 常见陷阱

### 1. 逐元素乘法 vs 矩阵乘法

```python
A = jnp.array([[1, 2], [3, 4]])
B = jnp.array([[5, 6], [7, 8]])

# 逐元素乘法（Hadamard 积）
elementwise = A * B
# [[5  12]
#  [21 32]]

# 矩阵乘法
matmul = A @ B
# [[19 22]
#  [43 50]]

# 完全不同！
```

### 2. 除零错误

```python
x = jnp.array([1, 2, 0, 4])

# 可能产生 inf
result = 1 / x  # [1., 0.5, inf, 0.25]

# 安全的做法
safe_result = jnp.where(x != 0, 1 / x, 0)
```

### 3. 轴的混淆

```python
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6]])

# axis=0：沿列方向（结果是行向量）
col_mean = jnp.mean(matrix, axis=0)  # [2.5, 3.5, 4.5]

# axis=1：沿行方向（结果是列向量）
row_mean = jnp.mean(matrix, axis=1)  # [2., 5.]

# 记忆技巧：axis=k 表示"消除"第 k 个维度
```

### 4. 浮点数精度

```python
# 浮点数比较
a = 0.1 + 0.2
b = 0.3
print(a == b)  # 可能是 False!

# 使用近似比较
print(jnp.allclose(a, b))  # True
```

## 🔬 性能优化

### 向量化 vs 循环

```python
import time

n = 1000000
x = jnp.arange(n)

# ❌ 慢：Python 循环
start = time.time()
result = jnp.array([xi ** 2 for xi in x])
print(f"循环: {time.time() - start:.4f}秒")

# ✅ 快：向量化
start = time.time()
result = x ** 2
result.block_until_ready()
print(f"向量化: {time.time() - start:.4f}秒")

# 向量化通常快 10-100 倍！
```

### 使用融合操作

```python
# ❌ 多次遍历数组
result = jnp.sqrt(jnp.abs(x)) + 1

# ✅ XLA 会自动融合这些操作
# 编译后只遍历一次
```

## 💪 练习提示

1. **验证形状**：矩阵乘法前检查维度是否匹配
2. **选择正确的操作**：清楚区分逐元素和矩阵运算
3. **理解轴参数**：在归约时明确指定 axis
4. **使用向量化**：避免显式循环

## 🔗 相关资源

- [JAX NumPy API 参考](https://jax.readthedocs.io/en/latest/jax.numpy.html)
- [线性代数基础](../math/linear_algebra.md)
- [NumPy 运算文档](https://numpy.org/doc/stable/reference/routines.math.html)

## ✅ 检查清单

- [ ] 掌握基本算术运算
- [ ] 理解逐元素乘法和矩阵乘法的区别
- [ ] 能够使用归约函数（sum, mean, max, min）
- [ ] 理解多维数组的 axis 参数
- [ ] 掌握矩阵运算（dot, @, transpose）
- [ ] 知道向量化的性能优势

---

完成理论学习后，打开 `exercises/01_intro/intro03_operations.py` 开始练习！
