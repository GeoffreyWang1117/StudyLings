# 组合变换

JAX 最强大的特性之一是变换的可组合性。你可以自由地嵌套和组合 grad、jit、vmap、pmap 等变换。

## 📚 知识要点

### 可组合性

JAX 变换可以任意组合：

```python
# 各种组合都是有效的！
jax.jit(jax.grad(f))              # JIT 编译的梯度
jax.vmap(jax.grad(f))             # 批量梯度
jax.grad(jax.jit(f))              # JIT 函数的梯度
jax.jit(jax.vmap(jax.grad(f)))    # 三者组合
jax.vmap(jax.vmap(jax.grad(f)))   # 嵌套 vmap + grad
```

### 为什么可组合？

因为 JAX 的设计哲学：
1. **纯函数**：变换输入纯函数，输出纯函数
2. **统一抽象**：所有变换遵循相同的接口
3. **数学基础**：基于扎实的数学理论

## 🎯 学习目标

1. 理解变换组合的原理
2. 掌握常见的组合模式
3. 理解组合顺序的影响
4. 学会在实际应用中灵活组合
5. 避免低效的组合方式
6. 掌握调试组合变换的技巧

## 💡 核心概念

### 变换的顺序

顺序很重要！不同的顺序可能有不同的含义和性能：

```python
# 这两个不同！
f1 = jax.jit(jax.vmap(process))      # 先向量化，再编译整体
f2 = jax.vmap(jax.jit(process))      # 先编译单个，再向量化

# 通常 f1 更快，因为 JIT 可以优化整个批处理
```

### 读取顺序

从内到外阅读组合：

```python
jax.jit(jax.vmap(jax.grad(f)))

# 阅读顺序：
# 1. grad(f) - 计算 f 的梯度函数
# 2. vmap(...) - 向量化梯度函数
# 3. jit(...) - 编译向量化的梯度函数
```

## 🔬 数学原理

### 组合的数学表示

对于函数 $f: \mathbb{R}^n \to \mathbb{R}$：

**grad**：
$$g(x) = \nabla f(x)$$

**vmap**（批量）：
$$V(g)(X) = [g(x_1), g(x_2), \ldots, g(x_k)]$$

**grad + vmap**：
$$\text{vmap}(\text{grad}(f))(X) = [\nabla f(x_1), \nabla f(x_2), \ldots, \nabla f(x_k)]$$

批量计算梯度！

### JIT 的作用

JIT 不改变数学语义，只优化执行：

$$\text{jit}(f) \equiv f \quad \text{(数学上等价)}$$

但执行速度：
$$T_{\text{jit}(f)} \ll T_f$$

## 📝 代码示例

### grad + jit

```python
import jax
import jax.numpy as jnp

def loss_fn(params, x, y):
    pred = jnp.dot(params, x)
    return jnp.mean((pred - y) ** 2)

# 方法1：先 grad 再 jit（推荐）
grad_fn = jax.grad(loss_fn)
fast_grad_fn = jax.jit(grad_fn)

# 方法2：先 jit 再 grad（也可以）
jit_loss = jax.jit(loss_fn)
grad_fn = jax.grad(jit_loss)

# 方法3：一步到位
fast_grad_fn = jax.jit(jax.grad(loss_fn))

# 测试
params = jnp.array([1.0, 2.0, 3.0])
x = jnp.array([1.0, 2.0, 3.0])
y = jnp.array([10.0])

grads = fast_grad_fn(params, x, y)
print(grads)
```

### vmap + grad

```python
def loss_single(params, x, y):
    """单个样本的损失"""
    pred = jnp.dot(params, x)
    return (pred - y) ** 2

# 批量梯度计算
batch_grad = jax.vmap(
    jax.grad(loss_single),
    in_axes=(None, 0, 0)  # params 共享，x 和 y 批处理
)

params = jnp.array([1.0, 2.0])
x_batch = jnp.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
y_batch = jnp.array([5.0, 11.0, 17.0])

grads_batch = batch_grad(params, x_batch, y_batch)
print(grads_batch.shape)  # (3, 2) - 每个样本的梯度
```

### jit + vmap + grad

```python
# 完整的训练步骤
@jax.jit
def train_step(params, x_batch, y_batch, lr):
    # 批量计算梯度
    grads_batch = jax.vmap(
        jax.grad(loss_single),
        in_axes=(None, 0, 0)
    )(params, x_batch, y_batch)

    # 平均梯度
    grads = jnp.mean(grads_batch, axis=0)

    # 更新参数
    params = params - lr * grads
    return params

# 使用
params = jnp.array([1.0, 2.0])
for _ in range(100):
    params = train_step(params, x_batch, y_batch, 0.01)

print(f"Final params: {params}")
```

### 嵌套 vmap

```python
def pairwise_distance(x, y):
    """计算两个点之间的距离"""
    return jnp.linalg.norm(x - y)

# 对两个点集计算所有点对距离
# points1: (n, d), points2: (m, d)
def all_pairwise_distances(points1, points2):
    # 第一层 vmap：遍历 points1
    # 第二层 vmap：遍历 points2
    return jax.vmap(
        lambda x: jax.vmap(
            lambda y: pairwise_distance(x, y)
        )(points2)
    )(points1)

points1 = jnp.array([[0, 0], [1, 0]])      # (2, 2)
points2 = jnp.array([[0, 1], [1, 1], [2, 2]])  # (3, 2)

distances = all_pairwise_distances(points1, points2)
print(distances.shape)  # (2, 3)
print(distances)
# [[1.   1.   2.82]
#  [1.   1.   1.41]]
```

### grad of vmap

```python
def batch_loss(params, x_batch):
    """批量数据的总损失"""
    def single_loss(x):
        return jnp.sum((params * x) ** 2)

    # vmap 计算每个样本的损失
    losses = jax.vmap(single_loss)(x_batch)
    return jnp.sum(losses)

# 对批量损失求导
grad_batch_loss = jax.grad(batch_loss)

params = jnp.array([1.0, 2.0])
x_batch = jnp.array([[1.0, 1.0], [2.0, 2.0]])

grads = grad_batch_loss(params, x_batch)
print(grads)
```

### value_and_grad + jit + vmap

```python
def loss_single(params, x, y):
    pred = jnp.dot(params, x)
    return (pred - y) ** 2

@jax.jit
def train_step_complete(params, x_batch, y_batch, lr):
    # 使用 vmap 包装 value_and_grad
    def single_value_and_grad(x, y):
        return jax.value_and_grad(
            lambda p: loss_single(p, x, y)
        )(params)

    # 批量计算损失和梯度
    losses, grads_batch = jax.vmap(single_value_and_grad)(x_batch, y_batch)

    # 平均
    avg_loss = jnp.mean(losses)
    avg_grad = jnp.mean(grads_batch, axis=0)

    # 更新
    params = params - lr * avg_grad

    return params, avg_loss

# 使用
params = jnp.array([1.0, 2.0])
params, loss = train_step_complete(params, x_batch, y_batch, 0.01)
print(f"Loss: {loss}, Params: {params}")
```

## 🎓 应用场景

### 完整的神经网络训练

```python
def forward(params, x):
    """前向传播"""
    for W, b in params[:-1]:
        x = jax.nn.relu(jnp.dot(x, W) + b)
    W, b = params[-1]
    return jnp.dot(x, W) + b

def loss_fn(params, x, y):
    """单个样本的损失"""
    pred = forward(params, x)
    return jnp.mean((pred - y) ** 2)

@jax.jit
def train_step(params, batch_x, batch_y, lr):
    """完整的训练步骤"""
    # 批量计算损失和梯度
    (loss, aux), grads_batch = jax.vmap(
        jax.value_and_grad(loss_fn, has_aux=False),
        in_axes=(None, 0, 0)
    )(params, batch_x, batch_y)

    # 平均梯度
    grads = jax.tree_map(lambda g: jnp.mean(g, axis=0), grads_batch)

    # 更新参数
    params = jax.tree_map(
        lambda p, g: p - lr * g,
        params, grads
    )

    return params, jnp.mean(loss)

# 初始化参数
params = [
    (jnp.ones((10, 20)), jnp.zeros(20)),
    (jnp.ones((20, 10)), jnp.zeros(10)),
    (jnp.ones((10, 1)), jnp.zeros(1))
]

# 训练
for epoch in range(10):
    batch_x = jnp.ones((32, 10))
    batch_y = jnp.ones((32, 1))
    params, loss = train_step(params, batch_x, batch_y, 0.01)
    print(f"Epoch {epoch}, Loss: {loss:.4f}")
```

### 二阶导数（Hessian）

```python
def f(x):
    return jnp.sum(x ** 3)

# 一阶导数
grad_f = jax.grad(f)

# 二阶导数（Hessian 的对角线）
hessian_diag = jax.grad(lambda x: jnp.sum(grad_f(x) * x))

x = jnp.array([1.0, 2.0, 3.0])
print(f"Gradient: {grad_f(x)}")           # [3, 12, 27]
print(f"Hessian diag: {hessian_diag(x)}")  # [6, 12, 18]

# 完整 Hessian
def hessian(f):
    return jax.jacfwd(jax.grad(f))

H = hessian(f)(x)
print(f"Full Hessian:\n{H}")
```

### Per-Example Gradients

```python
# 计算每个样本的梯度（用于差分隐私等）
def per_example_gradients(loss_fn, params, x_batch, y_batch):
    """计算每个样本的梯度"""
    # vmap over examples, return individual gradients
    return jax.vmap(
        jax.grad(loss_fn),
        in_axes=(None, 0, 0)
    )(params, x_batch, y_batch)

# 编译加速
fast_per_example_grads = jax.jit(per_example_gradients)

grads_per_example = fast_per_example_grads(
    loss_single, params, x_batch, y_batch
)
print(grads_per_example.shape)  # (batch_size, param_size)
```

### 批量 Jacobian

```python
def model(params, x):
    """向量值函数"""
    W, b = params
    return jnp.dot(W, x) + b

# 单个样本的 Jacobian
jacobian_fn = jax.jacfwd(model, argnums=1)

# 批量 Jacobian
batch_jacobian = jax.jit(jax.vmap(
    jacobian_fn,
    in_axes=(None, 0)
))

params = (jnp.ones((3, 4)), jnp.zeros(3))
x_batch = jnp.ones((10, 4))

jacobians = batch_jacobian(params, x_batch)
print(jacobians.shape)  # (10, 3, 4) - 每个样本一个 Jacobian
```

## ⚠️ 常见陷阱

### 1. 错误的组合顺序

```python
# ❌ 低效：对每个样本编译一次
slow_fn = jax.vmap(jax.jit(process))

# ✅ 高效：编译整个批处理
fast_fn = jax.jit(jax.vmap(process))

# 性能差异可能很大！
```

### 2. 不必要的嵌套

```python
# ❌ 过度嵌套
result = jax.jit(jax.jit(jax.jit(f)))(x)

# ✅ 一次就够
result = jax.jit(f)(x)
```

### 3. grad + vmap 的 in_axes

```python
# 对批量数据求梯度时，确保 in_axes 正确
batch_grad = jax.vmap(
    jax.grad(loss_fn),
    in_axes=(None, 0, 0)  # params 不批处理，x 和 y 批处理
)

# ❌ 错误：忘记 None
# batch_grad = jax.vmap(jax.grad(loss_fn))  # 会尝试对 params 也批处理！
```

### 4. JIT 中的动态形状

```python
# vmap 可能产生动态形状
@jax.jit
def process_dynamic(x):
    # x 的形状在 JIT 中必须是静态的
    return jax.vmap(some_fn)(x)

# 确保 x 的形状是固定的
```

## 🔬 性能对比

```python
import time

def benchmark_combinations():
    def process(x):
        return jnp.dot(x, x.T) + jnp.sum(x ** 2)

    batch = jnp.ones((100, 50))

    # 1. 无优化
    start = time.time()
    results = jnp.array([process(x) for x in batch])
    results.block_until_ready()
    print(f"循环: {time.time() - start:.4f}秒")

    # 2. 只用 vmap
    fn_vmap = jax.vmap(process)
    start = time.time()
    results = fn_vmap(batch)
    results.block_until_ready()
    print(f"vmap: {time.time() - start:.4f}秒")

    # 3. vmap + JIT
    fn_fast = jax.jit(jax.vmap(process))
    fn_fast(batch).block_until_ready()  # 预热
    start = time.time()
    results = fn_fast(batch)
    results.block_until_ready()
    print(f"jit + vmap: {time.time() - start:.4f}秒")

benchmark_combinations()
# 典型结果：
# 循环: 0.5000秒
# vmap: 0.0500秒 (10x 快)
# jit + vmap: 0.0050秒 (100x 快!)
```

## 💪 最佳实践

### 1. 推荐的组合顺序

```python
# ✅ 好的顺序（外到内）：
# jit -> vmap -> grad
fast_batch_grad = jax.jit(jax.vmap(jax.grad(f)))

# JIT 在最外层，可以优化整个计算
```

### 2. 使用装饰器链

```python
# 清晰易读
@jax.jit
@jax.vmap
def batch_process(x):
    return x ** 2 + jnp.sin(x)

# 等价于
batch_process = jax.jit(jax.vmap(lambda x: x ** 2 + jnp.sin(x)))
```

### 3. 逐步添加变换

```python
# 1. 先写基础函数
def process(x):
    return x ** 2

# 2. 测试基础函数
assert process(2.0) == 4.0

# 3. 添加 vmap
process_batch = jax.vmap(process)
assert process_batch(jnp.array([1., 2.])).shape == (2,)

# 4. 添加 JIT
process_fast = jax.jit(process_batch)
assert process_fast(jnp.array([1., 2.])).shape == (2,)

# 5. 如果需要，添加 grad
grad_process = jax.grad(lambda x: jnp.sum(process_fast(x)))
```

### 4. 明确变换的目的

```python
# ✅ 好：清晰的命名
batch_forward = jax.vmap(forward, in_axes=(None, 0))
fast_train_step = jax.jit(train_step)
compute_grads = jax.grad(loss_fn)

# ❌ 差：含糊的命名
f = jax.jit(jax.vmap(jax.grad(g)))
```

## 🔗 相关资源

- [JAX 变换组合文档](https://jax.readthedocs.io/en/latest/notebooks/thinking_in_jax.html)
- [自动微分](grad.md)
- [JIT 编译](jit.md)
- [向量化](vmap.md)
- [高级示例](../05_advanced/overview.md)

## ✅ 检查清单

- [ ] 理解变换可组合的原理
- [ ] 掌握常见的组合模式
- [ ] 理解组合顺序的影响
- [ ] 能够选择最优的组合顺序
- [ ] 知道如何调试组合变换
- [ ] 避免低效的组合方式
- [ ] 在实际应用中灵活运用组合
- [ ] 能够编写高性能的训练循环

---

恭喜完成 JAX 变换章节！这是 JAX 最核心和最强大的特性。

继续学习[神经网络](../04_neural_networks/overview.md)，将这些变换应用到实际的深度学习中！
