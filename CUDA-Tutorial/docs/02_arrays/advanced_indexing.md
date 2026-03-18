# 高级索引

JAX 的高级索引使用函数式更新语法，这是 JAX 不可变性设计的核心特性。

## 📚 知识要点

### JAX vs NumPy 的关键区别

| 特性 | NumPy | JAX |
|------|-------|-----|
| 数组可变性 | 可变 | **不可变** |
| 直接赋值 | `arr[i] = val` ✅ | `arr[i] = val` ❌ |
| 函数式更新 | 不支持 | `.at[]` 语法 ✅ |
| 返回值 | 修改原数组 | 返回新数组 |

### 函数式更新的优势

1. **线程安全**：没有竞态条件
2. **可预测**：没有隐藏的副作用
3. **可组合**：容易与 JAX 变换（jit, grad, vmap）配合
4. **支持 GPU/TPU**：硬件加速器要求不可变性

## 🎯 学习目标

1. 理解 JAX 的不可变性设计
2. 掌握 `.at[]` 语法
3. 学会各种函数式更新操作
4. 了解更新操作的性能特性
5. 避免常见的陷阱

## 💡 核心概念

### .at[] 语法

JAX 提供了 `.at[index]` 语法来进行函数式更新：

```python
# 基本形式
new_array = array.at[index].set(value)
new_array = array.at[index].add(value)
new_array = array.at[index].multiply(value)
new_array = array.at[index].divide(value)
new_array = array.at[index].min(value)
new_array = array.at[index].max(value)
```

**关键点**：所有操作都返回新数组，不修改原数组。

### 函数式编程思想

```python
# 命令式（NumPy 风格）- JAX 不支持
arr[0] = 10
arr[1] = 20

# 函数式（JAX 风格）
arr = arr.at[0].set(10)
arr = arr.at[1].set(20)

# 或链式调用
arr = arr.at[0].set(10).at[1].set(20)
```

## 🔬 数学原理

### 函数式更新的数学表示

对于向量 $\mathbf{x} = [x_0, x_1, \ldots, x_{n-1}]$，更新操作可以表示为：

**Set 操作**：
$$\mathbf{x}' = \mathbf{x} \text{ with } x_i = v$$

**Add 操作**：
$$\mathbf{x}' = \mathbf{x} \text{ with } x_i = x_i + v$$

**Multiply 操作**：
$$\mathbf{x}' = \mathbf{x} \text{ with } x_i = x_i \cdot v$$

在矩阵更新中：

$$\mathbf{A}'_{ij} = v \quad \text{(set)}$$
$$\mathbf{A}'_{ij} = \mathbf{A}_{ij} + v \quad \text{(add)}$$

### 梯度计算中的重要性

函数式更新对于自动微分至关重要：

```python
def f(x, idx, val):
    return x.at[idx].set(val).sum()

# 可以对这个函数求导
grad_f = jax.grad(f)
```

如果允许原地修改，梯度计算会变得困难甚至不可能。

## 📝 代码示例

### 基本 set 操作

```python
import jax.numpy as jnp

# 创建数组
arr = jnp.array([1, 2, 3, 4, 5])

# ❌ NumPy 风格（在 JAX 中不工作）
# arr[0] = 10  # TypeError!

# ✅ JAX 风格
new_arr = arr.at[0].set(10)
print(new_arr)  # [10  2  3  4  5]
print(arr)      # [1  2  3  4  5]  # 原数组不变！

# 多个索引
new_arr = arr.at[jnp.array([0, 2, 4])].set(100)
print(new_arr)  # [100   2 100   4 100]

# 切片
new_arr = arr.at[1:4].set(0)
print(new_arr)  # [1 0 0 0 5]
```

### add、multiply 等操作

```python
arr = jnp.array([1, 2, 3, 4, 5])

# add: 在指定位置加上值
new_arr = arr.at[0].add(10)
print(new_arr)  # [11  2  3  4  5]

# multiply: 在指定位置乘以值
new_arr = arr.at[1].multiply(10)
print(new_arr)  # [1 20  3  4  5]

# divide: 在指定位置除以值
new_arr = arr.at[2].divide(3)
print(new_arr)  # [1. 2. 1. 4. 5.]

# min: 取最小值
new_arr = arr.at[3].min(2)
print(new_arr)  # [1 2 3 2 5]

# max: 取最大值
new_arr = arr.at[4].max(10)
print(new_arr)  # [1 2 3 4 10]
```

### 二维数组更新

```python
matrix = jnp.array([[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]])

# 更新单个元素
new_matrix = matrix.at[0, 0].set(100)
print(new_matrix)
# [[100   2   3]
#  [  4   5   6]
#  [  7   8   9]]

# 更新整行
new_matrix = matrix.at[1, :].set(0)
print(new_matrix)
# [[1 2 3]
#  [0 0 0]
#  [7 8 9]]

# 更新整列
new_matrix = matrix.at[:, 2].set(0)
print(new_matrix)
# [[1 2 0]
#  [4 5 0]
#  [7 8 0]]

# 更新子矩阵
new_matrix = matrix.at[0:2, 1:3].set(0)
print(new_matrix)
# [[1 0 0]
#  [4 0 0]
#  [7 8 9]]
```

### 布尔索引更新

```python
arr = jnp.array([1, 2, 3, 4, 5, 6])

# 将所有大于 3 的元素设为 0
mask = arr > 3
new_arr = arr.at[mask].set(0)
print(new_arr)  # [1 2 3 0 0 0]

# 将所有偶数加倍
mask = arr % 2 == 0
new_arr = arr.at[mask].multiply(2)
print(new_arr)  # [1 4 3 8 5 12]
```

### 整数数组索引更新

```python
arr = jnp.arange(10)

# 使用整数数组索引
indices = jnp.array([0, 2, 5, 7])
new_arr = arr.at[indices].set(100)
print(new_arr)  # [100   1 100   3   4 100   6 100   8   9]

# 累加操作（重复索引会累加）
indices = jnp.array([0, 0, 1, 1, 1])
values = jnp.array([1, 2, 3, 4, 5])
new_arr = jnp.zeros(5).at[indices].add(values)
print(new_arr)  # [3. 12. 0. 0. 0.]  # 0位置: 1+2=3, 1位置: 3+4+5=12
```

### 链式更新

```python
arr = jnp.array([1, 2, 3, 4, 5])

# 多个更新可以链式调用
new_arr = arr.at[0].set(10).at[2].add(100).at[4].multiply(2)
print(new_arr)  # [10   2 103   4  10]

# 等价于
new_arr = arr.at[0].set(10)
new_arr = new_arr.at[2].add(100)
new_arr = new_arr.at[4].multiply(2)
```

### 高级：scatter 操作

```python
# scatter 是更通用的更新操作
arr = jnp.zeros(10)
indices = jnp.array([1, 3, 5, 7])
values = jnp.array([10, 20, 30, 40])

# 使用 .at[] 实现 scatter
new_arr = arr.at[indices].set(values)
print(new_arr)  # [ 0. 10.  0. 20.  0. 30.  0. 40.  0.  0.]

# scatter-add（常用于梯度累加）
new_arr = arr.at[indices].add(values)
print(new_arr)  # [ 0. 10.  0. 20.  0. 30.  0. 40.  0.  0.]
```

## 🎓 应用场景

### 梯度累积

```python
def accumulate_gradients(params, grads, indices):
    """
    将梯度累积到参数的特定位置
    params: 参数数组
    grads: 梯度值
    indices: 要更新的索引
    """
    return params.at[indices].add(grads)

params = jnp.zeros(100)
indices = jnp.array([10, 20, 30])
grads = jnp.array([0.1, 0.2, 0.3])

updated_params = accumulate_gradients(params, grads, indices)
```

### 嵌入层更新

```python
def embed_and_update(embedding_table, token_ids, updates):
    """
    更新嵌入表中的特定 token
    embedding_table: (vocab_size, embedding_dim)
    token_ids: (num_tokens,) 要更新的 token
    updates: (num_tokens, embedding_dim) 更新值
    """
    return embedding_table.at[token_ids].set(updates)

vocab_size, emb_dim = 1000, 128
embeddings = jnp.zeros((vocab_size, emb_dim))
token_ids = jnp.array([5, 10, 15])
new_embeddings = jnp.random.normal(size=(3, emb_dim))

updated_table = embed_and_update(embeddings, token_ids, new_embeddings)
```

### 稀疏更新

```python
def sparse_update(dense_array, sparse_indices, sparse_values):
    """
    稀疏更新：只更新少数元素
    在优化器中常用（如 Adam 的稀疏梯度）
    """
    return dense_array.at[sparse_indices].add(sparse_values)

# 模拟稀疏梯度更新
weights = jnp.ones(10000)
# 只有 10 个位置有梯度
sparse_idx = jnp.array([100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000])
sparse_grads = jnp.random.normal(size=10) * 0.01

updated_weights = sparse_update(weights, sparse_idx, -sparse_grads)
```

### 图像掩码应用

```python
def apply_mask(image, mask, fill_value=0):
    """
    对图像应用掩码
    image: (H, W, C)
    mask: (H, W) 布尔数组
    """
    # 扩展掩码以匹配通道维度
    mask_expanded = mask[:, :, jnp.newaxis]  # (H, W, 1)

    # 使用 where 而非 .at[]（更适合这个场景）
    return jnp.where(mask_expanded, fill_value, image)

# 或使用 .at[]
def apply_mask_at(image, mask, fill_value=0):
    result = image
    for c in range(image.shape[2]):
        result = result.at[mask, c].set(fill_value)
    return result
```

### Softmax 的数值稳定版本中的应用

```python
def stable_softmax(logits):
    """数值稳定的 softmax"""
    # 减去最大值以避免溢出
    max_logits = jnp.max(logits, axis=-1, keepdims=True)
    shifted_logits = logits - max_logits

    # 计算 exp 和归一化
    exp_logits = jnp.exp(shifted_logits)
    sum_exp = jnp.sum(exp_logits, axis=-1, keepdims=True)
    return exp_logits / sum_exp

# 如果需要原地替换某些值（如掩码位置）
def masked_softmax(logits, mask):
    """
    带掩码的 softmax
    mask: True 表示有效位置
    """
    # 将无效位置设为很小的数
    logits = jnp.where(mask, logits, -1e9)
    return stable_softmax(logits)
```

## ⚠️ 常见陷阱

### 1. 忘记赋值给新变量

```python
arr = jnp.array([1, 2, 3, 4, 5])

# ❌ 错误：没有保存结果
arr.at[0].set(10)
print(arr)  # [1 2 3 4 5]  # 原数组未变！

# ✅ 正确：赋值给变量（可以是原变量名）
arr = arr.at[0].set(10)
print(arr)  # [10  2  3  4  5]
```

### 2. 期望原地修改

```python
def update_array(arr):
    arr.at[0].set(10)  # ❌ 返回值被丢弃
    return arr

arr = jnp.array([1, 2, 3])
result = update_array(arr)
print(result)  # [1 2 3]  # 没有被更新！

# ✅ 正确
def update_array(arr):
    return arr.at[0].set(10)  # 返回新数组

result = update_array(arr)
print(result)  # [10  2  3]
```

### 3. 性能：大量小更新 vs 批量更新

```python
import time

arr = jnp.zeros(10000)
indices = jnp.arange(1000)
values = jnp.ones(1000)

# ❌ 低效：逐个更新
start = time.time()
result = arr
for i, v in zip(indices, values):
    result = result.at[i].set(v)
result.block_until_ready()
print(f"逐个更新: {time.time() - start:.4f}秒")

# ✅ 高效：批量更新
start = time.time()
result = arr.at[indices].set(values)
result.block_until_ready()
print(f"批量更新: {time.time() - start:.4f}秒")

# 批量更新快得多！
```

### 4. 重复索引的行为

```python
# add 操作会累加重复索引
arr = jnp.zeros(5)
indices = jnp.array([0, 0, 1, 1, 1])
values = jnp.array([1, 2, 3, 4, 5])

result = arr.at[indices].add(values)
print(result)  # [3. 12. 0. 0. 0.]  # 累加了重复的索引

# set 操作只保留最后一个值
result = arr.at[indices].set(values)
print(result)  # [2. 5. 0. 0. 0.]  # 最后的值
```

### 5. 在 JIT 中的限制

```python
# 动态索引在 JIT 中可能有限制
@jax.jit
def dynamic_update(arr, idx, val):
    return arr.at[idx].set(val)

arr = jnp.arange(10)

# ✅ 静态索引：可以
result = dynamic_update(arr, 0, 100)

# ⚠️ 动态索引：依赖于运行时值
# 在某些情况下可能需要特殊处理
```

## 🔬 性能优化

### 批量操作

```python
# 优先使用向量化的批量操作
arr = jnp.zeros(1000)

# ✅ 好：批量更新
indices = jnp.arange(100)
values = jnp.ones(100)
result = arr.at[indices].set(values)

# ❌ 差：循环更新
result = arr
for i in range(100):
    result = result.at[i].set(1.0)
```

### 选择合适的操作

```python
arr = jnp.array([1, 2, 3, 4, 5])

# 如果要设置为0，使用 set
new_arr = arr.at[0].set(0)

# 不要使用 multiply(0)（虽然结果相同）
# new_arr = arr.at[0].multiply(0)  # 低效
```

## 💪 练习提示

1. **记住不可变性**：始终赋值更新结果
2. **使用批量操作**：避免循环中的更新
3. **理解重复索引**：add 累加，set 覆盖
4. **与 NumPy 对比**：加深理解差异
5. **测试边界情况**：空索引、越界索引

## 🔗 相关资源

- [JAX pytree 文档](https://jax.readthedocs.io/en/latest/jax-101/05.1-pytrees.html)
- [函数式编程与 JAX](https://jax.readthedocs.io/en/latest/notebooks/thinking_in_jax.html)
- [JAX 常见陷阱](https://jax.readthedocs.io/en/latest/notebooks/Common_Gotchas_in_JAX.html)

## ✅ 检查清单

- [ ] 理解 JAX 的不可变性设计
- [ ] 掌握 `.at[]` 的各种操作（set, add, multiply 等）
- [ ] 能够进行多维数组的函数式更新
- [ ] 理解重复索引的行为
- [ ] 知道何时使用批量更新
- [ ] 避免常见的陷阱（忘记赋值等）
- [ ] 理解函数式更新对性能的影响

---

恭喜完成数组操作章节！接下来学习 [JAX 变换](../03_transformations/overview.md)，这是 JAX 最强大的特性！
