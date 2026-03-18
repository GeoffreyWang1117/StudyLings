# 值与梯度

`jax.value_and_grad` 同时计算函数值和梯度，这是训练神经网络时的高效模式。

## 📚 知识要点

### 为什么需要 value_and_grad？

在训练神经网络时，我们经常需要：
1. **函数值**（损失）：用于监控训练进度
2. **梯度**：用于更新参数

分别计算会导致重复的前向传播！

```python
# ❌ 低效：计算两次
loss_value = loss_fn(params, x, y)      # 前向传播1次
grads = jax.grad(loss_fn)(params, x, y) # 前向传播1次 + 反向传播

# ✅ 高效：只计算一次
loss_value, grads = jax.value_and_grad(loss_fn)(params, x, y)
# 前向传播1次 + 反向传播
```

## 🎯 学习目标

1. 理解 value_and_grad 的优势
2. 掌握基本用法和参数
3. 学会在训练循环中应用
4. 理解多参数梯度的处理
5. 掌握 has_aux 参数的使用

## 💡 核心概念

### 基本语法

```python
value_and_grad_fn = jax.value_and_grad(f)
value, grad = value_and_grad_fn(x)
```

### 主要参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `fun` | 要求导的函数 | 必需 |
| `argnums` | 对哪些参数求导 | `0` |
| `has_aux` | 是否返回辅助输出 | `False` |
| `holomorphic` | 复数函数求导 | `False` |

## 🔬 数学原理

### 前向和反向传播

对于损失函数 $L(\theta)$：

**前向传播**：
$$L = f(\theta)$$

**反向传播**（链式法则）：
$$\frac{\partial L}{\partial \theta_i} = \frac{\partial L}{\partial z} \frac{\partial z}{\partial \theta_i}$$

`value_and_grad` 在一次前向传播中记录计算图，然后执行反向传播：

1. 前向传播：计算 $L$ 并记录中间值
2. 反向传播：利用记录的中间值计算梯度

**效率提升**：避免重复计算中间结果。

### 计算复杂度

假设前向传播复杂度为 $O(n)$：

- `grad` 单独使用：$O(n) + O(n) = O(2n)$（前向+反向）
- `value_and_grad`：$O(n) + O(n) = O(2n)$（但只做一次前向）
- 分别调用 `f` 和 `grad(f)`：$O(n) + O(2n) = O(3n)$（**浪费！**）

## 📝 代码示例

### 基础使用

```python
import jax
import jax.numpy as jnp

def loss_fn(x):
    """简单的二次损失"""
    return jnp.sum(x ** 2)

# 方法1：分别计算（低效）
x = jnp.array([1.0, 2.0, 3.0])
value = loss_fn(x)
grad = jax.grad(loss_fn)(x)
print(f"Loss: {value}")  # 14.0
print(f"Grad: {grad}")   # [2. 4. 6.]

# 方法2：使用 value_and_grad（高效）
value_and_grad_fn = jax.value_and_grad(loss_fn)
value, grad = value_and_grad_fn(x)
print(f"Loss: {value}")  # 14.0
print(f"Grad: {grad}")   # [2. 4. 6.]
```

### 神经网络损失

```python
def mse_loss(params, x, y):
    """均方误差损失"""
    # 简单的线性模型：y_pred = W @ x + b
    W, b = params
    pred = jnp.dot(W, x) + b
    return jnp.mean((pred - y) ** 2)

# 初始化参数
W = jnp.array([[1.0, 2.0], [3.0, 4.0]])  # (2, 2)
b = jnp.array([0.1, 0.2])                 # (2,)
params = (W, b)

# 数据
x = jnp.array([1.0, 2.0])  # (2,)
y = jnp.array([3.0, 4.0])  # (2,)

# 计算损失和梯度
loss_value, grads = jax.value_and_grad(mse_loss)(params, x, y)
print(f"Loss: {loss_value}")
print(f"Gradients: {grads}")

# grads 的结构与 params 相同：(W_grad, b_grad)
W_grad, b_grad = grads
```

### 多参数梯度（argnums）

```python
def loss_with_regularization(params, x, y, reg_coef):
    """带正则化的损失"""
    W, b = params
    pred = jnp.dot(W, x) + b
    mse = jnp.mean((pred - y) ** 2)
    reg = jnp.sum(W ** 2)
    return mse + reg_coef * reg

params = (W, b)
x = jnp.array([1.0, 2.0])
y = jnp.array([3.0, 4.0])
reg_coef = 0.01

# 只对 params 求导（默认 argnums=0）
loss_value, grads = jax.value_and_grad(
    loss_with_regularization
)(params, x, y, reg_coef)
print(f"Gradients w.r.t. params: {grads}")

# 对 params 和 reg_coef 都求导
loss_value, (params_grad, reg_grad) = jax.value_and_grad(
    loss_with_regularization,
    argnums=(0, 3)  # 对第0和第3个参数求导
)(params, x, y, reg_coef)
print(f"Params grad: {params_grad}")
print(f"Reg coef grad: {reg_grad}")
```

### has_aux 参数

当函数返回额外的信息时使用：

```python
def loss_with_metrics(params, x, y):
    """返回损失和额外指标"""
    W, b = params
    pred = jnp.dot(W, x) + b
    loss = jnp.mean((pred - y) ** 2)

    # 额外指标
    metrics = {
        'mae': jnp.mean(jnp.abs(pred - y)),
        'max_error': jnp.max(jnp.abs(pred - y))
    }

    return loss, metrics  # 返回 (value, aux)

# 使用 has_aux=True
(loss_value, metrics), grads = jax.value_and_grad(
    loss_with_metrics,
    has_aux=True  # 告诉 JAX 函数返回 (value, aux)
)(params, x, y)

print(f"Loss: {loss_value}")
print(f"Metrics: {metrics}")
print(f"Grads: {grads}")
```

## 🎓 应用场景

### 完整的训练步骤

```python
def create_train_step(loss_fn):
    """创建训练步骤函数"""

    def train_step(params, x, y, learning_rate):
        # 计算损失和梯度
        loss, grads = jax.value_and_grad(loss_fn)(params, x, y)

        # 梯度下降更新
        params = jax.tree_map(
            lambda p, g: p - learning_rate * g,
            params, grads
        )

        return params, loss

    return train_step

# 使用
train_step = create_train_step(mse_loss)
params, loss = train_step(params, x, y, learning_rate=0.01)
print(f"Updated params, loss: {loss}")
```

### 带动量的优化器

```python
def sgd_with_momentum(loss_fn, learning_rate=0.01, momentum=0.9):
    """SGD + 动量"""

    def init(params):
        """初始化优化器状态"""
        velocity = jax.tree_map(jnp.zeros_like, params)
        return velocity

    def update(params, grads, velocity):
        """更新参数"""
        # 更新速度
        velocity = jax.tree_map(
            lambda v, g: momentum * v + g,
            velocity, grads
        )

        # 更新参数
        params = jax.tree_map(
            lambda p, v: p - learning_rate * v,
            params, velocity
        )

        return params, velocity

    def step(params, velocity, x, y):
        """训练步骤"""
        loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
        params, velocity = update(params, grads, velocity)
        return params, velocity, loss

    return init, step

# 使用
init, step = sgd_with_momentum(mse_loss)
velocity = init(params)

for epoch in range(10):
    params, velocity, loss = step(params, velocity, x, y)
    print(f"Epoch {epoch}, Loss: {loss:.4f}")
```

### 训练循环with早停

```python
def train_with_early_stopping(
    params, train_data, val_data,
    loss_fn, max_epochs=100, patience=10
):
    """带早停的训练"""
    best_val_loss = float('inf')
    patience_counter = 0
    best_params = params

    value_and_grad_fn = jax.value_and_grad(loss_fn)

    for epoch in range(max_epochs):
        # 训练
        for x, y in train_data:
            train_loss, grads = value_and_grad_fn(params, x, y)
            params = jax.tree_map(
                lambda p, g: p - 0.01 * g,
                params, grads
            )

        # 验证
        val_losses = []
        for x, y in val_data:
            val_loss, _ = value_and_grad_fn(params, x, y)
            val_losses.append(val_loss)
        val_loss = jnp.mean(jnp.array(val_losses))

        print(f"Epoch {epoch}: Val Loss = {val_loss:.4f}")

        # 早停检查
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_params = params
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch}")
                break

    return best_params
```

### 梯度裁剪

```python
def train_step_with_clip(params, x, y, learning_rate, max_norm=1.0):
    """带梯度裁剪的训练步骤"""
    loss, grads = jax.value_and_grad(mse_loss)(params, x, y)

    # 计算梯度范数
    grad_norm = jnp.sqrt(sum(
        jnp.sum(jnp.square(g)) for g in jax.tree_leaves(grads)
    ))

    # 裁剪梯度
    clip_coef = jnp.minimum(1.0, max_norm / (grad_norm + 1e-6))
    grads = jax.tree_map(lambda g: g * clip_coef, grads)

    # 更新参数
    params = jax.tree_map(
        lambda p, g: p - learning_rate * g,
        params, grads
    )

    return params, loss, grad_norm

# 使用
params, loss, grad_norm = train_step_with_clip(params, x, y, 0.01)
print(f"Loss: {loss:.4f}, Grad norm: {grad_norm:.4f}")
```

## ⚠️ 常见陷阱

### 1. 忘记 has_aux

```python
def loss_with_acc(params, x, y):
    pred = model(params, x)
    loss = jnp.mean((pred - y) ** 2)
    acc = jnp.mean(pred == y)
    return loss, acc  # 返回两个值

# ❌ 错误：没有指定 has_aux
# (loss, acc), grads = jax.value_and_grad(loss_with_acc)(params, x, y)
# 这会把 acc 当作梯度！

# ✅ 正确
(loss, acc), grads = jax.value_and_grad(
    loss_with_acc,
    has_aux=True  # 告诉 JAX 第二个返回值不是梯度
)(params, x, y)
```

### 2. argnums 的索引

```python
def loss(params, x, y, reg):
    # params: 索引0
    # x: 索引1
    # y: 索引2
    # reg: 索引3
    pass

# ✅ 对 params 求导
grads = jax.grad(loss, argnums=0)(params, x, y, reg)

# ✅ 对 params 和 reg 求导
grads = jax.grad(loss, argnums=(0, 3))(params, x, y, reg)
# grads 是一个元组: (params_grad, reg_grad)
```

### 3. 返回值的结构

```python
# 无 has_aux
value, grad = jax.value_and_grad(f)(x)

# 有 has_aux
(value, aux), grad = jax.value_and_grad(f, has_aux=True)(x)

# 多参数梯度 + has_aux
(value, aux), (grad0, grad1) = jax.value_and_grad(
    f, argnums=(0, 1), has_aux=True
)(x, y)
```

## 🔬 性能对比

```python
import time

def benchmark():
    params = (jnp.ones((100, 100)), jnp.zeros(100))
    x = jnp.ones(100)
    y = jnp.ones(100)

    # 方法1：分别计算
    start = time.time()
    for _ in range(1000):
        loss = mse_loss(params, x, y)
        grads = jax.grad(mse_loss)(params, x, y)
    print(f"分别计算: {time.time() - start:.4f}秒")

    # 方法2：value_and_grad
    value_and_grad_fn = jax.value_and_grad(mse_loss)
    start = time.time()
    for _ in range(1000):
        loss, grads = value_and_grad_fn(params, x, y)
    print(f"value_and_grad: {time.time() - start:.4f}秒")

benchmark()
# value_and_grad 通常快 1.5-2 倍！
```

## 💪 最佳实践

### 1. 总是使用 value_and_grad 在训练中

```python
# ✅ 推荐
def train_step(params, x, y):
    loss, grads = jax.value_and_grad(loss_fn)(params, x, y)
    # ... 更新参数
    return params, loss

# ❌ 不推荐
def train_step(params, x, y):
    loss = loss_fn(params, x, y)
    grads = jax.grad(loss_fn)(params, x, y)  # 重复计算！
    return params, loss
```

### 2. 合理使用 has_aux

```python
# 将所有指标放在 aux 中
def loss_with_all_metrics(params, x, y):
    pred = model(params, x)
    loss = jnp.mean((pred - y) ** 2)

    metrics = {
        'accuracy': compute_accuracy(pred, y),
        'mae': jnp.mean(jnp.abs(pred - y)),
        'predictions': pred,  # 也可以返回预测值
    }

    return loss, metrics

(loss, metrics), grads = jax.value_and_grad(
    loss_with_all_metrics, has_aux=True
)(params, x, y)
```

### 3. 与 JIT 结合

```python
# 编译整个训练步骤
@jax.jit
def train_step_jit(params, x, y, lr):
    (loss, metrics), grads = jax.value_and_grad(
        loss_with_metrics, has_aux=True
    )(params, x, y)

    params = jax.tree_map(
        lambda p, g: p - lr * g,
        params, grads
    )

    return params, loss, metrics

# 首次调用会编译
params, loss, metrics = train_step_jit(params, x, y, 0.01)
# 后续调用很快
params, loss, metrics = train_step_jit(params, x, y, 0.01)
```

## 🔗 相关资源

- [JAX 自动微分](grad.md)
- [JAX 官方文档 - value_and_grad](https://jax.readthedocs.io/en/latest/_autosummary/jax.value_and_grad.html)
- [优化器实现](../05_advanced/optimizers.md)

## ✅ 检查清单

- [ ] 理解 value_and_grad 的效率优势
- [ ] 掌握基本用法
- [ ] 会使用 argnums 参数
- [ ] 理解 has_aux 的作用
- [ ] 能在训练循环中正确使用
- [ ] 知道如何与 JIT 结合
- [ ] 避免常见的返回值结构错误

---

继续学习 [JIT 编译](jit.md)，进一步提升代码性能！
