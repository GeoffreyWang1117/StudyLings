# 向量化（vmap）

`jax.vmap` 是 JAX 的自动向量化工具，它可以将处理单个样本的函数自动转换为处理批量样本的函数。

## 📚 知识要点

### 什么是 vmap？

vmap（vectorizing map）自动向量化函数，避免显式编写循环：

```python
# ❌ 手动循环（慢）
results = []
for x in batch:
    results.append(process(x))
results = jnp.stack(results)

# ✅ 使用 vmap（快）
results = jax.vmap(process)(batch)
```

### 为什么重要？

1. **性能**：向量化操作比循环快得多
2. **简洁**：代码更清晰，更易维护
3. **硬件优化**：充分利用 SIMD、GPU 并行能力
4. **可组合**：可以嵌套和组合其他变换

## 🎯 学习目标

1. 理解向量化的概念和优势
2. 掌握 vmap 的基本用法
3. 学会使用 in_axes 和 out_axes
4. 理解嵌套 vmap
5. 掌握常见的向量化模式
6. 避免常见陷阱

## 💡 核心概念

### 批处理维度

vmap 在数组上添加一个"批处理维度"：

```python
# 单个样本
x_single = jnp.array([1, 2, 3])  # shape: (3,)
result_single = process(x_single)  # shape: (output_size,)

# 批处理
x_batch = jnp.array([[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]])  # shape: (batch, 3)
result_batch = jax.vmap(process)(x_batch)  # shape: (batch, output_size)
```

### in_axes 和 out_axes

控制哪个轴是批处理维度：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `in_axes` | 输入的批处理轴 | `0` |
| `out_axes` | 输出的批处理轴 | `0` |
| `None` | 不沿任何轴映射（广播） | - |

```python
# in_axes=0: 第0轴是批处理维度
vmap(f, in_axes=0)(arr)  # arr shape: (batch, ...)

# in_axes=1: 第1轴是批处理维度
vmap(f, in_axes=1)(arr)  # arr shape: (..., batch, ...)

# in_axes=None: 不映射，对所有批次广播
vmap(f, in_axes=(0, None))(arr1, arr2)
```

## 🔬 数学原理

### 向量化的数学表示

对于函数 $f: \mathbb{R}^n \to \mathbb{R}^m$：

**标量应用**（循环）：
$$\mathbf{y}_i = f(\mathbf{x}_i), \quad i = 1, 2, \ldots, k$$

计算复杂度：$O(k \cdot T(f))$，其中 $T(f)$ 是单次调用的时间。

**向量化应用**（vmap）：
$$\mathbf{Y} = \text{vmap}(f)(\mathbf{X})$$

其中：
- $\mathbf{X} \in \mathbb{R}^{k \times n}$ （$k$ 个输入向量）
- $\mathbf{Y} \in \mathbb{R}^{k \times m}$ （$k$ 个输出向量）

向量化后，所有 $k$ 次调用并行执行。

### 批量矩阵乘法示例

单个矩阵乘法：
$$\mathbf{y} = \mathbf{W}\mathbf{x}$$

批量矩阵乘法：
$$\mathbf{Y}_i = \mathbf{W}\mathbf{X}_i, \quad i = 1, 2, \ldots, k$$

使用 vmap：
```python
def matvec(W, x):
    return jnp.dot(W, x)

# 批量应用
batch_matvec = jax.vmap(matvec, in_axes=(None, 0))
Y = batch_matvec(W, X_batch)
```

## 📝 代码示例

### 基础使用

```python
import jax
import jax.numpy as jnp

def squared_norm(x):
    """计算向量的平方范数"""
    return jnp.sum(x ** 2)

# 单个向量
x = jnp.array([1.0, 2.0, 3.0])
result = squared_norm(x)
print(result)  # 14.0

# 批量向量（手动循环）
batch = jnp.array([[1.0, 2.0, 3.0],
                    [4.0, 5.0, 6.0],
                    [7.0, 8.0, 9.0]])

results_loop = jnp.array([squared_norm(x) for x in batch])
print(results_loop)  # [14. 77. 194.]

# 批量向量（vmap）
batch_squared_norm = jax.vmap(squared_norm)
results_vmap = batch_squared_norm(batch)
print(results_vmap)  # [14. 77. 194.]
```

### in_axes 参数

```python
def add(x, y):
    return x + y

a = jnp.array([[1, 2], [3, 4], [5, 6]])  # (3, 2)
b = jnp.array([10, 20])                   # (2,)

# in_axes=(0, None): 对 a 的第0轴映射，b 广播
result = jax.vmap(add, in_axes=(0, None))(a, b)
print(result)
# [[11 22]
#  [13 24]
#  [15 26]]

# in_axes=(None, 0): a 广播，对 b 的第0轴映射
c = jnp.array([[1, 2]])  # (1, 2)
d = jnp.array([[10, 20], [30, 40]])  # (2, 2)
result = jax.vmap(add, in_axes=(None, 0))(c, d)
print(result)
# [[11 22]
#  [31 42]]

# in_axes=(0, 0): 两个都沿第0轴映射
result = jax.vmap(add, in_axes=(0, 0))(a, d)
print(result)  # shape: (2, 2) - 取最小的批大小
```

### out_axes 参数

```python
def process(x):
    """返回 x 和 x^2"""
    return x, x ** 2

# out_axes=0: 输出的第0轴是批处理维度（默认）
batch_process = jax.vmap(process)
x_batch = jnp.array([1, 2, 3])
out1, out2 = batch_process(x_batch)
print(out1.shape)  # (3,)
print(out2.shape)  # (3,)

# out_axes=1: 输出的第1轴是批处理维度
batch_process_t = jax.vmap(process, out_axes=1)
out1, out2 = batch_process_t(x_batch)
print(out1.shape)  # (3,) - 1D 数组只有一个轴
print(out2.shape)  # (3,)

# 对于多维输出
def process_2d(x):
    return jnp.outer(x, x)  # 返回矩阵

batch_process_2d = jax.vmap(process_2d, out_axes=2)
result = batch_process_2d(jnp.array([[1, 2], [3, 4]]))
print(result.shape)  # (2, 2, 2) - 批处理维度在最后
```

### 嵌套 vmap

```python
# 处理 2D 批次（batch of batches）
def process(x):
    return x ** 2

# 数据: (outer_batch, inner_batch, features)
data = jnp.arange(24).reshape(2, 3, 4)

# 嵌套 vmap
result = jax.vmap(jax.vmap(process))(data)
print(result.shape)  # (2, 3, 4)

# 等价于
result = jax.vmap(process)(jax.vmap(process)(data))
```

### 字典参数

```python
def model(params, x):
    """使用参数字典的模型"""
    return params['W'] @ x + params['b']

params = {
    'W': jnp.array([[1, 2], [3, 4]]),  # (2, 2)
    'b': jnp.array([0.1, 0.2])         # (2,)
}

x_batch = jnp.array([[1, 1], [2, 2], [3, 3]])  # (3, 2)

# in_axes 可以是字典
batch_model = jax.vmap(
    model,
    in_axes=(None, 0)  # params 不映射，x 沿第0轴映射
)

results = batch_model(params, x_batch)
print(results.shape)  # (3, 2)
```

## 🎓 应用场景

### 批量梯度计算

```python
def loss_single(params, x, y):
    """单个样本的损失"""
    pred = model(params, x)
    return jnp.sum((pred - y) ** 2)

# 批量损失
def batch_loss(params, x_batch, y_batch):
    """批量损失的平均"""
    # 对每个样本计算损失
    losses = jax.vmap(
        loss_single,
        in_axes=(None, 0, 0)
    )(params, x_batch, y_batch)
    return jnp.mean(losses)

# 批量梯度
grad_fn = jax.grad(batch_loss)
grads = grad_fn(params, x_batch, y_batch)
```

### 批量前向传播

```python
def forward_single(params, x):
    """单个样本的前向传播"""
    for W, b in params:
        x = jnp.dot(W, x) + b
        x = jax.nn.relu(x)
    return x

# 批量前向传播
forward_batch = jax.vmap(forward_single, in_axes=(None, 0))

params = [(jnp.ones((10, 5)), jnp.zeros(10))]
x_batch = jnp.ones((32, 5))  # 32个样本，每个5维

predictions = forward_batch(params, x_batch)
print(predictions.shape)  # (32, 10)
```

### 成对距离计算

```python
def pairwise_distance(points):
    """计算所有点对之间的距离"""
    def distance_to_all(point):
        # 对每个点计算到所有点的距离
        return jax.vmap(
            lambda p: jnp.linalg.norm(point - p)
        )(points)

    # 对每个点应用
    return jax.vmap(distance_to_all)(points)

points = jnp.array([[0, 0], [1, 0], [0, 1]])
distances = pairwise_distance(points)
print(distances)
# [[0.   1.   1.  ]
#  [1.   0.   1.41]
#  [1.   1.41 0.  ]]
```

### Attention 机制

```python
def attention(query, keys, values):
    """单个查询的 attention"""
    # query: (d_k,)
    # keys: (n, d_k)
    # values: (n, d_v)

    # 计算注意力分数
    scores = jax.vmap(lambda k: jnp.dot(query, k))(keys)
    # softmax
    weights = jax.nn.softmax(scores)
    # 加权求和
    return jnp.dot(weights, values)

# 批量查询
batch_attention = jax.vmap(
    attention,
    in_axes=(0, None, None)  # 每个查询独立，keys/values共享
)

queries = jnp.ones((10, 64))   # 10个查询
keys = jnp.ones((20, 64))      # 20个键
values = jnp.ones((20, 128))   # 20个值

outputs = batch_attention(queries, keys, values)
print(outputs.shape)  # (10, 128)
```

### 蒙特卡洛采样

```python
def monte_carlo_sample(key):
    """单次蒙特卡洛采样"""
    sample = jax.random.normal(key, (1000,))
    return jnp.mean(sample ** 2)

# 批量采样
keys = jax.random.split(jax.random.PRNGKey(0), 10000)
samples = jax.vmap(monte_carlo_sample)(keys)

mean_estimate = jnp.mean(samples)
std_estimate = jnp.std(samples)
print(f"Mean: {mean_estimate:.4f}, Std: {std_estimate:.4f}")
```

## ⚠️ 常见陷阱

### 1. 形状不匹配

```python
def process(x, y):
    return x + y

a = jnp.ones((10, 5))
b = jnp.ones((10, 3))  # 不同的特征维度！

# ❌ 错误：形状不兼容
# result = jax.vmap(process)(a, b)  # ValueError!

# ✅ 确保非批处理维度匹配
b = jnp.ones((10, 5))
result = jax.vmap(process)(a, b)  # OK
```

### 2. in_axes 设置错误

```python
def add(x, y):
    return x + y

a = jnp.ones((3, 4))
b = jnp.ones(4)

# ❌ 错误：in_axes 不匹配
# result = jax.vmap(add, in_axes=(1, 0))(a, b)
# b 的第0轴大小是4，但 a 的第1轴大小也是4 - 会产生意外结果

# ✅ 正确
result = jax.vmap(add, in_axes=(0, None))(a, b)
print(result.shape)  # (3, 4)
```

### 3. 忘记 None 用于广播

```python
def scale(x, factor):
    return x * factor

batch = jnp.ones((10, 5))
scale_factor = 2.0

# ❌ 错误：尝试对标量进行 vmap
# result = jax.vmap(scale)(batch, scale_factor)  # 不会按预期工作

# ✅ 正确：对 factor 使用 None（广播）
result = jax.vmap(scale, in_axes=(0, None))(batch, scale_factor)
```

### 4. 嵌套时轴的混淆

```python
# 3D 数据: (batch, seq_len, features)
data = jnp.ones((2, 3, 4))

def process(x):
    return x ** 2

# 想要处理每个时间步
# ❌ 错误
result = jax.vmap(process)(data)  # 沿 batch 维度映射
print(result.shape)  # (2, 3, 4) - 处理了 batch

# ✅ 正确：需要嵌套 vmap
result = jax.vmap(jax.vmap(process))(data)  # 沿 batch 和 seq_len
print(result.shape)  # (2, 3, 4) - 处理了每个元素
```

## 🔬 性能对比

```python
import time

def process(x):
    return jnp.dot(x, x.T) + jnp.sin(x)

# 生成数据
batch_size = 1000
dim = 100
data = jnp.ones((batch_size, dim))

# 方法1：Python 循环
start = time.time()
results_loop = jnp.array([process(x) for x in data])
results_loop.block_until_ready()
print(f"循环: {time.time() - start:.4f}秒")

# 方法2：vmap
process_vmap = jax.vmap(process)
start = time.time()
results_vmap = process_vmap(data)
results_vmap.block_until_ready()
print(f"vmap: {time.time() - start:.4f}秒")

# 方法3：vmap + JIT
process_fast = jax.jit(jax.vmap(process))
start = time.time()
results_fast = process_fast(data)
results_fast.block_until_ready()
print(f"vmap + JIT: {time.time() - start:.4f}秒")

# vmap 通常快 10-100 倍！
# vmap + JIT 可能快 100-1000 倍！
```

## 💪 最佳实践

### 1. 总是优先使用 vmap

```python
# ❌ 避免循环
results = [process(x) for x in batch]

# ✅ 使用 vmap
results = jax.vmap(process)(batch)
```

### 2. 与 JIT 组合

```python
# 获得最佳性能
fast_batch_process = jax.jit(jax.vmap(process))
```

### 3. 明确 in_axes

```python
# 即使是默认值也明确写出，提高可读性
batch_fn = jax.vmap(fn, in_axes=(0, None, 0))
```

### 4. 使用描述性的函数名

```python
# ✅ 清晰
batch_forward = jax.vmap(forward_single, in_axes=(None, 0))

# ❌ 不清晰
f = jax.vmap(lambda x: x ** 2)
```

## 🔗 相关资源

- [JAX vmap 文档](https://jax.readthedocs.io/en/latest/jax-101/03-vectorization.html)
- [JAX 自动向量化教程](https://jax.readthedocs.io/en/latest/notebooks/quickstart.html#auto-vectorization-with-vmap)
- [组合变换](combining.md)
- [并行计算](../09_parallel/overview.md)

## ✅ 检查清单

- [ ] 理解 vmap 的作用和优势
- [ ] 掌握基本用法
- [ ] 会使用 in_axes 和 out_axes
- [ ] 理解何时使用 None（广播）
- [ ] 能够嵌套使用 vmap
- [ ] 知道如何与 JIT 组合
- [ ] 避免常见的形状和轴错误
- [ ] 在实际应用中灵活运用 vmap

---

完成 vmap 后，学习[组合变换](combining.md)来发挥 JAX 的全部威力！
