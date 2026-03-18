# JIT 编译

JIT（Just-In-Time）编译是 JAX 最重要的性能优化特性，可以将 Python 函数编译成高效的 XLA（Accelerated Linear Algebra）代码。

## 📚 知识要点

### 什么是 JIT？

JIT 编译器将你的 Python/JAX 代码转换为优化的机器代码：

```python
@jax.jit
def fast_function(x):
    return x ** 2 + jnp.sin(x)

# 首次调用：编译（较慢）
result = fast_function(jnp.array([1.0, 2.0, 3.0]))

# 后续调用：使用缓存的编译代码（很快！）
result = fast_function(jnp.array([4.0, 5.0, 6.0]))
```

### 性能提升

- **典型加速**：10-100倍
- **最佳场景**：循环、复杂计算、重复调用
- **GPU/TPU**：必须使用 JIT 才能充分利用

## 🎯 学习目标

1. 理解 JIT 编译的原理
2. 掌握 @jax.jit 装饰器的使用
3. 了解静态和动态参数
4. 识别和避免 JIT 的限制
5. 学会调试编译后的代码
6. 掌握性能优化技巧

## 💡 核心概念

### XLA 编译器

XLA（Accelerated Linear Algebra）是 Google 开发的编译器：

**优化技术**：
1. **操作融合**：合并多个操作为一个核
2. **常量折叠**：编译时计算常量
3. **死代码消除**：移除不需要的代码
4. **内存优化**：减少内存分配和传输

### 静态 vs 动态

**静态参数**（编译时）：
- 数组形状
- 数据类型（dtype）
- 控制流条件（if/for 的条件）

**动态参数**（运行时）：
- 数组内容/值
- 计算结果

```python
@jax.jit
def f(x, n):
    # x 的值：动态 ✓
    # n 作为数据：动态 ✓
    # n 用于形状/控制流：必须静态 ✗
    return x[:n]  # 编译时不知道 n 的值 - 可能有问题！
```

## 🔬 数学原理

### 计算图优化

JIT 将函数转换为计算图（DAG），然后优化：

原始代码：
```python
y = x ** 2
z = jnp.sin(x)
result = y + z
```

计算图：
```
x --> square --> y -----
  |                     |
  └--> sin --> z --------+--> add --> result
```

XLA 优化后可能融合为单个操作，减少内存访问。

### 操作融合示例

未融合：
$$y_1 = x^2, \quad y_2 = \sin(x), \quad y_3 = y_1 + y_2$$

需要3次内存访问。

融合后：
$$y = x^2 + \sin(x)$$

只需1次内存访问！

## 📝 代码示例

### 基础使用

```python
import jax
import jax.numpy as jnp
import time

def slow_function(x):
    """未编译的函数"""
    for _ in range(100):
        x = x ** 2 + 1
        x = jnp.sin(x)
    return x

# 使用装饰器
@jax.jit
def fast_function(x):
    """编译的函数"""
    for _ in range(100):
        x = x ** 2 + 1
        x = jnp.sin(x)
    return x

x = jnp.ones((1000,))

# 未编译版本
start = time.time()
result_slow = slow_function(x)
result_slow.block_until_ready()
print(f"未编译: {time.time() - start:.4f}秒")

# 编译版本（首次调用）
start = time.time()
result_fast = fast_function(x)
result_fast.block_until_ready()
print(f"首次编译: {time.time() - start:.4f}秒")  # 包含编译时间

# 编译版本（使用缓存）
start = time.time()
result_fast = fast_function(x)
result_fast.block_until_ready()
print(f"缓存编译: {time.time() - start:.4f}秒")  # 很快！

# 通常快 10-100 倍
```

### 手动调用 JIT

```python
# 不使用装饰器
def my_function(x, y):
    return x ** 2 + y ** 2

# 手动编译
jitted_fn = jax.jit(my_function)

# 使用
result = jitted_fn(jnp.array([1.0]), jnp.array([2.0]))
```

### 静态参数（static_argnums）

```python
def power(x, n):
    """计算 x 的 n 次方"""
    result = x
    for _ in range(n):
        result = result * x
    return result

# ❌ 错误：n 用于循环次数，必须是静态的
# fast_power = jax.jit(power)
# result = fast_power(jnp.array([2.0]), 10)  # 编译时不知道循环次数

# ✅ 正确：指定 n 为静态参数
fast_power = jax.jit(power, static_argnums=(1,))
result = fast_power(jnp.array([2.0]), 10)
print(result)  # [1024.]

# 注意：不同的 n 值会触发重新编译
result = fast_power(jnp.array([2.0]), 5)   # 重新编译
result = fast_power(jnp.array([2.0]), 10)  # 使用缓存
```

### 条件语句

```python
# ❌ 错误：Python if 在 JIT 中只执行一次
@jax.jit
def wrong_conditional(x, flag):
    if flag:  # Python if：编译时决定
        return x ** 2
    else:
        return x ** 3

# 第一次调用 flag=True，编译为 x ** 2
result1 = wrong_conditional(jnp.array([2.0]), True)   # 4.0
# 第二次调用 flag=False，仍然执行 x ** 2！
result2 = wrong_conditional(jnp.array([2.0]), False)  # 4.0（错误！）

# ✅ 正确：使用 jax.lax.cond
@jax.jit
def correct_conditional(x, flag):
    return jax.lax.cond(
        flag,
        lambda x: x ** 2,  # True 分支
        lambda x: x ** 3,  # False 分支
        x
    )

result1 = correct_conditional(jnp.array([2.0]), True)   # 4.0
result2 = correct_conditional(jnp.array([2.0]), False)  # 8.0（正确）
```

### 循环语句

```python
# ❌ Python for 循环：在编译时展开
@jax.jit
def sum_python_loop(arr):
    total = 0
    for i in range(len(arr)):  # 编译时展开！
        total += arr[i]
    return total

# 如果数组很大，编译会很慢

# ✅ 使用 lax.scan 或向量化
@jax.jit
def sum_vectorized(arr):
    return jnp.sum(arr)  # 高效！

# 或使用 lax.fori_loop
@jax.jit
def sum_lax_loop(arr):
    def body_fun(i, val):
        return val + arr[i]

    return jax.lax.fori_loop(0, len(arr), body_fun, 0.0)
```

## 🎓 应用场景

### 神经网络前向传播

```python
def forward(params, x):
    """多层感知机"""
    for W, b in params:
        x = jnp.dot(x, W) + b
        x = jax.nn.relu(x)
    return x

# JIT 编译整个前向传播
forward_jit = jax.jit(forward)

params = [(jnp.ones((10, 20)), jnp.zeros(20)),
          (jnp.ones((20, 10)), jnp.zeros(10))]
x = jnp.ones((5, 10))

# 快速推理
predictions = forward_jit(params, x)
```

### 优化训练步骤

```python
@jax.jit
def train_step(params, x, y, learning_rate):
    """完整的训练步骤"""
    # 计算损失和梯度
    (loss, metrics), grads = jax.value_and_grad(
        loss_fn, has_aux=True
    )(params, x, y)

    # 更新参数
    params = jax.tree_map(
        lambda p, g: p - learning_rate * g,
        params, grads
    )

    return params, loss, metrics

# 整个训练步骤被编译为单个优化的操作
params, loss, metrics = train_step(params, batch_x, batch_y, 0.01)
```

### 模拟和蒙特卡洛

```python
@jax.jit
def monte_carlo_pi(key, n_samples):
    """估计 π 的值"""
    # 生成随机点
    points = jax.random.uniform(key, (n_samples, 2))

    # 检查是否在圆内
    inside_circle = jnp.sum(
        points[:, 0]**2 + points[:, 1]**2 <= 1.0
    )

    # 估计 π
    return 4.0 * inside_circle / n_samples

# 快速运行百万次采样
key = jax.random.PRNGKey(0)
pi_estimate = monte_carlo_pi(key, 1_000_000)
print(f"π ≈ {pi_estimate}")
```

## ⚠️ 常见陷阱

### 1. 副作用

```python
# ❌ 错误：print 只在编译时执行一次
@jax.jit
def debug_fn(x):
    print(f"x = {x}")  # 只打印一次！
    return x ** 2

debug_fn(jnp.array([1.0]))  # 打印：x = Traced<...>
debug_fn(jnp.array([2.0]))  # 不打印！
debug_fn(jnp.array([3.0]))  # 不打印！

# ✅ 正确：使用 jax.debug.print
@jax.jit
def debug_fn_correct(x):
    jax.debug.print("x = {}", x)  # 每次都打印
    return x ** 2
```

### 2. 形状变化导致重新编译

```python
@jax.jit
def process(x):
    return x ** 2

# 不同形状会重新编译
process(jnp.ones(10))   # 编译
process(jnp.ones(20))   # 重新编译
process(jnp.ones(10))   # 使用缓存
process(jnp.ones((5, 2)))  # 重新编译（不同形状）

# 每次重新编译都有开销！
```

### 3. 修改全局状态

```python
counter = 0

# ❌ 错误：修改全局变量
@jax.jit
def increment():
    global counter
    counter += 1  # 不会按预期工作！
    return counter

# ✅ 正确：返回新状态
@jax.jit
def increment_functional(counter):
    return counter + 1

counter = increment_functional(counter)
```

### 4. NumPy 操作

```python
# ❌ 错误：NumPy 操作不能 JIT
import numpy as np

@jax.jit
def wrong_fn(x):
    return np.sum(x)  # 使用 NumPy！

# ✅ 正确：使用 jax.numpy
@jax.jit
def correct_fn(x):
    return jnp.sum(x)  # 使用 JAX NumPy
```

### 5. 动态切片

```python
# ❌ 错误：动态大小的切片
@jax.jit
def dynamic_slice_wrong(x, n):
    return x[:n]  # n 必须是静态的！

# ✅ 正确：使用 lax.dynamic_slice
@jax.jit
def dynamic_slice_correct(x, n):
    return jax.lax.dynamic_slice(
        x,
        start_indices=(0,),
        slice_sizes=(n,)
    )
```

## 🔬 性能优化

### 1. 避免不必要的重新编译

```python
# ❌ 每次不同的形状都重新编译
shapes = [10, 20, 30, 40, 50]
for shape in shapes:
    process(jnp.ones(shape))  # 5次编译！

# ✅ 使用固定形状或 padding
max_shape = 50
for shape in shapes:
    data = jnp.ones(shape)
    padded = jnp.pad(data, (0, max_shape - shape))
    process(padded)  # 只编译1次！
```

### 2. 批量处理优于循环

```python
# ❌ 低效：逐个处理
@jax.jit
def process_one(x):
    return x ** 2 + jnp.sin(x)

results = [process_one(x) for x in data_list]  # 多次调用

# ✅ 高效：批量处理
@jax.jit
def process_batch(xs):
    return xs ** 2 + jnp.sin(xs)

results = process_batch(jnp.array(data_list))  # 单次调用
```

### 3. 与其他变换组合

```python
# 组合 JIT + vmap 获得最佳性能
@jax.jit
@jax.vmap
def process_vectorized(x):
    return x ** 2 + jnp.sin(x)

# 或
process_fast = jax.jit(jax.vmap(process_single))
```

## 🛠️ 调试技巧

### 查看编译后的代码

```python
from jax import make_jaxpr

def f(x):
    return x ** 2 + 1

# 查看 JAX 的中间表示
jaxpr = make_jaxpr(f)(2.0)
print(jaxpr)

# 输出类似：
# { lambda ; a:f32[]. let
#     b:f32[] = integer_pow[y=2] a
#     c:f32[] = add b 1.0
#   in (c,) }
```

### 条件性禁用 JIT

```python
# 开发时禁用 JIT 以便调试
JAX_DISABLE_JIT = True

if JAX_DISABLE_JIT:
    train_step = train_step_fn  # 不编译
else:
    train_step = jax.jit(train_step_fn)  # 编译

# 或使用环境变量
# export JAX_DISABLE_JIT=1
```

### 编译时间分析

```python
import time

@jax.jit
def expensive_fn(x):
    for _ in range(1000):
        x = x ** 2 + jnp.sin(x)
    return x

# 测量编译时间
start = time.time()
result = expensive_fn(jnp.ones(100))
result.block_until_ready()
compile_time = time.time() - start
print(f"首次调用（含编译）: {compile_time:.4f}秒")

# 测量执行时间
start = time.time()
result = expensive_fn(jnp.ones(100))
result.block_until_ready()
execution_time = time.time() - start
print(f"执行时间: {execution_time:.4f}秒")

print(f"加速比: {compile_time / execution_time:.1f}x")
```

## 💪 最佳实践

1. **默认使用 JIT**：除非调试，否则始终 JIT 编译
2. **批量处理**：尽可能使用 vmap 而非循环
3. **静态参数**：使用 static_argnums 明确静态参数
4. **纯函数**：避免副作用和全局状态
5. **使用 JAX 操作**：用 `jax.lax` 替代 Python 控制流
6. **监控重新编译**：避免频繁的形状变化
7. **组合变换**：`jit(vmap(grad(...)))` 获得最佳性能

## 🔗 相关资源

- [JAX JIT 文档](https://jax.readthedocs.io/en/latest/jax-101/02-jitting.html)
- [XLA 编译器](https://www.tensorflow.org/xla)
- [JAX 控制流](../08_control_flow/overview.md)
- [性能优化技巧](../appendix/performance.md)

## ✅ 检查清单

- [ ] 理解 JIT 编译的原理和优势
- [ ] 能够正确使用 @jax.jit 装饰器
- [ ] 知道静态和动态参数的区别
- [ ] 掌握 static_argnums 的使用
- [ ] 理解常见陷阱（副作用、控制流等）
- [ ] 会使用 jax.lax 替代 Python 控制流
- [ ] 能够调试和优化 JIT 编译的代码
- [ ] 知道如何与其他变换组合使用

---

继续学习[向量化（vmap）](vmap.md)，实现自动批处理！
