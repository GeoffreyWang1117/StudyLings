# Transformer 完整实现

## 📖 概述

Transformer 是现代深度学习最重要的架构之一，它彻底改变了自然语言处理领域，并在计算机视觉、语音等领域也取得了巨大成功。本章将从数学原理到代码实现，完整讲解 Transformer 架构。

## 🎯 学习目标

- 深入理解 Self-Attention 机制的数学原理
- 掌握 Multi-Head Attention 的实现
- 理解位置编码的设计和作用
- 学会实现完整的 Transformer Encoder
- 了解 Transformer 的各种变体

## 📚 理论基础

### Transformer 架构概览

<div class="knowledge-point">

**核心思想**：Transformer 完全基于注意力机制（Attention），抛弃了循环神经网络（RNN）的序列处理方式，实现了：

- **并行化处理** - 不再需要序列计算
- **长距离依赖** - 直接建模任意距离的关系
- **可解释性** - 注意力权重可视化

</div>

**Transformer Encoder 架构**：

```
Input Embeddings
    ↓
+ Positional Encoding
    ↓
┌─────────────────────┐  ×N 层
│  Multi-Head         │
│  Self-Attention     │
│        ↓            │
│  Add & Norm         │
│        ↓            │
│  Feed Forward       │
│        ↓            │
│  Add & Norm         │
└─────────────────────┘
    ↓
Output
```

## 🔬 Self-Attention 数学原理

### 基本概念

Self-Attention 允许模型在处理一个位置时，关注输入序列中的所有位置。

**三个核心矩阵**：

- **Query (Q)** - 查询：当前位置要寻找什么
- **Key (K)** - 键：各个位置提供的信息
- **Value (V)** - 值：实际的特征表示

### Scaled Dot-Product Attention

**数学公式**：

<div class="math-formula">

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

</div>

**详细推导**：

1. **计算注意力分数**：

$$
\text{Score}(q_i, k_j) = q_i \cdot k_j = \sum_{d=1}^{d_k} q_{i,d} \cdot k_{j,d}
$$

几何意义：Query 和 Key 的相似度（点积越大，越相关）

2. **缩放**（为什么要除以 $\sqrt{d_k}$？）：

当 $d_k$ 很大时，点积的方差会变大：

$$
\text{Var}(q \cdot k) = d_k \cdot \text{Var}(q) \cdot \text{Var}(k)
$$

缩放后方差稳定：

$$
\text{Var}\left(\frac{q \cdot k}{\sqrt{d_k}}\right) = \text{Var}(q) \cdot \text{Var}(k)
$$

这使得 softmax 的梯度更稳定！

3. **Softmax 归一化**：

$$
\alpha_{ij} = \frac{\exp(s_{ij})}{\sum_{k} \exp(s_{ik})}
$$

其中 $s_{ij} = \frac{q_i \cdot k_j}{\sqrt{d_k}}$

性质：
- $\sum_j \alpha_{ij} = 1$ （概率分布）
- $\alpha_{ij} \geq 0$

4. **加权求和**：

$$
\text{output}_i = \sum_j \alpha_{ij} v_j
$$

### 矩阵形式

对于序列长度 $n$，维度 $d$：

- $Q \in \mathbb{R}^{n \times d_k}$
- $K \in \mathbb{R}^{n \times d_k}$
- $V \in \mathbb{R}^{n \times d_v}$

**计算步骤**：

$$
\begin{align}
S &= QK^T \in \mathbb{R}^{n \times n} \\
A &= \text{softmax}(S / \sqrt{d_k}) \in \mathbb{R}^{n \times n} \\
\text{Output} &= AV \in \mathbb{R}^{n \times d_v}
\end{align}
$$

### JAX 实现

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Args:
        Q: Query [batch, seq_len, d_k]
        K: Key [batch, seq_len, d_k]
        V: Value [batch, seq_len, d_v]
        mask: 可选的掩码 [batch, seq_len, seq_len]

    Returns:
        output: [batch, seq_len, d_v]
        attention_weights: [batch, seq_len, seq_len]
    """
    d_k = Q.shape[-1]

    # 计算注意力分数
    scores = jnp.matmul(Q, K.transpose(0, 2, 1)) / jnp.sqrt(d_k)

    # 应用掩码（用于 causal attention）
    if mask is not None:
        scores = jnp.where(mask, scores, -1e9)

    # Softmax 归一化
    attention_weights = jax.nn.softmax(scores, axis=-1)

    # 加权求和
    output = jnp.matmul(attention_weights, V)

    return output, attention_weights
```

**时间复杂度**：$O(n^2 d)$，其中 $n$ 是序列长度

**空间复杂度**：$O(n^2)$ 用于存储注意力矩阵

## 🎭 Multi-Head Attention

### 为什么需要多头？

单个注意力头可能只关注某一种模式，多头注意力允许模型：

- 同时关注不同的表示子空间
- 学习不同类型的依赖关系
- 提升模型容量

### 数学公式

<div class="math-formula">

$$
\begin{align}
\text{MultiHead}(Q, K, V) &= \text{Concat}(\text{head}_1, \ldots, \text{head}_h)W^O \\
\text{where } \text{head}_i &= \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)
\end{align}
$$

</div>

**参数矩阵**：

- $W_i^Q \in \mathbb{R}^{d_{model} \times d_k}$ - 第 $i$ 个头的 Query 投影
- $W_i^K \in \mathbb{R}^{d_{model} \times d_k}$ - Key 投影
- $W_i^V \in \mathbb{R}^{d_{model} \times d_v}$ - Value 投影
- $W^O \in \mathbb{R}^{hd_v \times d_{model}}$ - 输出投影

通常设置：$d_k = d_v = d_{model} / h$

### 详细步骤

1. **线性投影**：

$$
\begin{align}
Q_i &= QW_i^Q \\
K_i &= KW_i^K \\
V_i &= VW_i^V
\end{align}
$$

2. **并行计算注意力**：

对每个头 $i$：
$$
\text{head}_i = \text{Attention}(Q_i, K_i, V_i)
$$

3. **拼接**：

$$
\text{Concat} = [head_1; head_2; \ldots; head_h]
$$

4. **输出投影**：

$$
\text{Output} = \text{Concat} \cdot W^O
$$

### JAX 实现

```python
def multi_head_attention(x, W_q, W_k, W_v, W_o, num_heads, mask=None):
    """
    Args:
        x: 输入 [batch, seq_len, d_model]
        W_q, W_k, W_v: 投影矩阵 [d_model, d_model]
        W_o: 输出投影 [d_model, d_model]
        num_heads: 注意力头数
        mask: 可选掩码

    Returns:
        output: [batch, seq_len, d_model]
    """
    batch_size, seq_len, d_model = x.shape
    d_k = d_model // num_heads

    # 1. 线性投影
    Q = jnp.dot(x, W_q)  # [batch, seq_len, d_model]
    K = jnp.dot(x, W_k)
    V = jnp.dot(x, W_v)

    # 2. 分割成多头: [batch, seq_len, num_heads, d_k]
    Q = Q.reshape(batch_size, seq_len, num_heads, d_k)
    K = K.reshape(batch_size, seq_len, num_heads, d_k)
    V = V.reshape(batch_size, seq_len, num_heads, d_k)

    # 转置: [batch, num_heads, seq_len, d_k]
    Q = Q.transpose(0, 2, 1, 3)
    K = K.transpose(0, 2, 1, 3)
    V = V.transpose(0, 2, 1, 3)

    # 3. 计算注意力
    # 重塑为 [batch*num_heads, seq_len, d_k]
    batch_heads = batch_size * num_heads
    Q = Q.reshape(batch_heads, seq_len, d_k)
    K = K.reshape(batch_heads, seq_len, d_k)
    V = V.reshape(batch_heads, seq_len, d_k)

    attention_output, _ = scaled_dot_product_attention(Q, K, V, mask)

    # 4. 拼接头
    attention_output = attention_output.reshape(batch_size, num_heads, seq_len, d_k)
    attention_output = attention_output.transpose(0, 2, 1, 3)
    attention_output = attention_output.reshape(batch_size, seq_len, d_model)

    # 5. 输出投影
    output = jnp.dot(attention_output, W_o)

    return output
```

## 📍 位置编码（Positional Encoding）

### 为什么需要位置编码？

Attention 机制是**位置不变的**（permutation-invariant），它不知道输入的顺序！

对于句子 "I love JAX" 和 "JAX love I"，纯 Attention 会给出相同的结果。

**解决方案**：在输入嵌入中添加位置信息。

### Sinusoidal 位置编码

**数学公式**：

<div class="math-formula">

$$
\begin{align}
PE_{(pos, 2i)} &= \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right) \\
PE_{(pos, 2i+1)} &= \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)
\end{align}
$$

</div>

其中：
- $pos$ - 位置索引（0, 1, 2, ...）
- $i$ - 维度索引（0, 1, 2, ...， $d_{model}/2$）
- $d_{model}$ - 模型维度

**关键性质**：

1. **唯一性**：每个位置有唯一的编码
2. **相对位置**：可以通过线性变换得到相对位置
3. **外推性**：可以处理训练时未见过的序列长度

**频率解释**：

不同维度使用不同频率：

$$
\text{wavelength} = 2\pi \cdot 10000^{2i/d_{model}}
$$

低维度：高频变化（捕捉局部模式）
高维度：低频变化（捕捉全局模式）

### JAX 实现

```python
def positional_encoding(seq_len, d_model):
    """
    生成 sinusoidal 位置编码

    Args:
        seq_len: 序列长度
        d_model: 模型维度

    Returns:
        pe: [seq_len, d_model]
    """
    position = jnp.arange(seq_len)[:, None]  # [seq_len, 1]
    div_term = jnp.exp(jnp.arange(0, d_model, 2) * -(jnp.log(10000.0) / d_model))

    pe = jnp.zeros((seq_len, d_model))

    # 偶数维度使用 sin
    pe = pe.at[:, 0::2].set(jnp.sin(position * div_term))

    # 奇数维度使用 cos
    pe = pe.at[:, 1::2].set(jnp.cos(position * div_term))

    return pe
```

**可视化**：

```python
import matplotlib.pyplot as plt

pe = positional_encoding(100, 128)
plt.imshow(pe, aspect='auto', cmap='RdBu')
plt.xlabel('Dimension')
plt.ylabel('Position')
plt.colorbar()
plt.title('Positional Encoding Pattern')
```

## 🏗️ Feed-Forward Network

### 结构

每个 Transformer 层包含一个简单的前馈网络：

<div class="math-formula">

$$
\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
$$

</div>

或者：

$$
\text{FFN}(x) = \text{GELU}(xW_1 + b_1)W_2 + b_2
$$

**维度变化**：

- 输入：$d_{model}$
- 隐藏层：$d_{ff} = 4 \times d_{model}$（通常）
- 输出：$d_{model}$

### 作用

- **非线性变换**：增加模型表达能力
- **位置级处理**：独立处理每个位置
- **特征混合**：整合不同维度的信息

### JAX 实现

```python
def feed_forward_network(x, W1, b1, W2, b2):
    """
    Position-wise FFN

    Args:
        x: [batch, seq_len, d_model]
        W1: [d_model, d_ff]
        b1: [d_ff]
        W2: [d_ff, d_model]
        b2: [d_model]

    Returns:
        output: [batch, seq_len, d_model]
    """
    # 第一层 + 激活
    hidden = jax.nn.gelu(jnp.dot(x, W1) + b1)

    # 第二层
    output = jnp.dot(hidden, W2) + b2

    return output
```

## 🔄 Layer Normalization

### 数学公式

<div class="math-formula">

$$
\text{LayerNorm}(x) = \gamma \odot \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} + \beta
$$

</div>

其中：
- $\mu = \frac{1}{d}\sum_{i=1}^d x_i$ - 均值
- $\sigma^2 = \frac{1}{d}\sum_{i=1}^d (x_i - \mu)^2$ - 方差
- $\gamma, \beta$ - 可学习的缩放和偏移参数
- $\epsilon$ - 数值稳定性常数（如 $10^{-5}$）

### 与 Batch Normalization 的区别

| 特性 | Layer Norm | Batch Norm |
|------|------------|------------|
| 归一化维度 | 特征维度 | Batch 维度 |
| 训练/推理 | 一致 | 不同（需要 running stats）|
| Batch 依赖 | 无 | 有 |
| 序列任务 | 适合 | 不适合 |

### JAX 实现

```python
def layer_norm(x, gamma, beta, eps=1e-5):
    """
    Layer Normalization

    Args:
        x: [batch, seq_len, d_model]
        gamma: [d_model] - 缩放参数
        beta: [d_model] - 偏移参数
        eps: 数值稳定性常数

    Returns:
        normed: [batch, seq_len, d_model]
    """
    # 在最后一个维度上计算均值和方差
    mean = jnp.mean(x, axis=-1, keepdims=True)
    var = jnp.var(x, axis=-1, keepdims=True)

    # 归一化
    x_norm = (x - mean) / jnp.sqrt(var + eps)

    # 缩放和偏移
    output = gamma * x_norm + beta

    return output
```

## 🎯 完整的 Transformer Encoder Layer

### 架构

```
Input
  ↓
Multi-Head Attention
  ↓
Residual + LayerNorm
  ↓
Feed Forward Network
  ↓
Residual + LayerNorm
  ↓
Output
```

### 数学公式

<div class="math-formula">

$$
\begin{align}
\text{Attention Output} &= \text{MultiHead}(x, x, x) \\
x_1 &= \text{LayerNorm}(x + \text{Dropout}(\text{Attention Output})) \\
\text{FFN Output} &= \text{FFN}(x_1) \\
x_2 &= \text{LayerNorm}(x_1 + \text{Dropout}(\text{FFN Output}))
\end{align}
$$

</div>

### JAX 实现

```python
def transformer_encoder_layer(
    x,
    attn_params,
    ffn_params,
    ln1_params,
    ln2_params,
    mask=None,
    dropout_rate=0.1,
    training=True,
    rng=None
):
    """
    单个 Transformer Encoder 层

    Args:
        x: [batch, seq_len, d_model]
        attn_params: 注意力层参数
        ffn_params: FFN 层参数
        ln1_params, ln2_params: Layer Norm 参数
        mask: 可选的注意力掩码
        dropout_rate: Dropout 比率
        training: 是否训练模式
        rng: 随机数生成器

    Returns:
        output: [batch, seq_len, d_model]
    """
    # 1. Multi-Head Self-Attention
    attn_output = multi_head_attention(
        x,
        attn_params['W_q'],
        attn_params['W_k'],
        attn_params['W_v'],
        attn_params['W_o'],
        num_heads=8,
        mask=mask
    )

    # Dropout (训练时)
    if training and dropout_rate > 0:
        rng, dropout_rng = jax.random.split(rng)
        keep_prob = 1 - dropout_rate
        mask = jax.random.bernoulli(dropout_rng, keep_prob, attn_output.shape)
        attn_output = jnp.where(mask, attn_output / keep_prob, 0)

    # Residual + LayerNorm
    x = layer_norm(x + attn_output, ln1_params['gamma'], ln1_params['beta'])

    # 2. Feed Forward Network
    ffn_output = feed_forward_network(
        x,
        ffn_params['W1'],
        ffn_params['b1'],
        ffn_params['W2'],
        ffn_params['b2']
    )

    # Dropout (训练时)
    if training and dropout_rate > 0:
        rng, dropout_rng = jax.random.split(rng)
        mask = jax.random.bernoulli(dropout_rng, keep_prob, ffn_output.shape)
        ffn_output = jnp.where(mask, ffn_output / keep_prob, 0)

    # Residual + LayerNorm
    output = layer_norm(x + ffn_output, ln2_params['gamma'], ln2_params['beta'])

    return output
```

## 🎓 练习指导

### Exercise: `dl02_transformer_complete`

**学习重点**：

1. **位置编码**
   - 理解 sinusoidal 函数的选择
   - 掌握位置编码的实现

2. **注意力机制**
   - 深入理解 Scaled Dot-Product Attention
   - 实现 Multi-Head Attention

3. **Layer Normalization**
   - 理解归一化的作用
   - Pre-LN vs Post-LN 的区别

4. **残差连接**
   - 理解残差连接如何帮助梯度流动
   - 实现 Add & Norm 模块

**常见错误**：

❌ 忘记缩放：使用 $QK^T$ 而不是 $\frac{QK^T}{\sqrt{d_k}}$

❌ 维度错误：Multi-Head 拼接时维度不匹配

❌ 位置编码：忘记加到输入嵌入上

## 📊 Transformer 变体

### 架构改进

| 变体 | 改进点 | 应用 |
|------|--------|------|
| **BERT** | 双向编码器、Masked LM | 文本理解 |
| **GPT** | 单向解码器、自回归 | 文本生成 |
| **T5** | 统一 Encoder-Decoder | 多任务学习 |
| **Vision Transformer** | 图像patch + Transformer | 计算机视觉 |

### 效率优化

- **Linformer** - 线性复杂度注意力
- **Reformer** - LSH 注意力
- **Longformer** - 稀疏注意力
- **Flash Attention** - IO 优化的注意力

## 📚 延伸阅读

### 必读论文

1. **Attention Is All You Need** - Vaswani et al., 2017
   - 原始 Transformer 论文

2. **BERT** - Devlin et al., 2018
   - 双向 Transformer 用于语言理解

3. **GPT-3** - Brown et al., 2020
   - 大规模语言模型

4. **Vision Transformer** - Dosovitskiy et al., 2020
   - Transformer 用于视觉

### 优秀资源

- [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
- [The Annotated Transformer](http://nlp.seas.harvard.edu/2018/04/03/attention.html)
- [Formal Algorithms for Transformers](https://arxiv.org/abs/2207.09238)

## ⏭️ 下一步

掌握 Transformer 后，你可以：

- 实现更高效的注意力机制
- 探索预训练语言模型
- 应用 Transformer 到其他领域（视觉、语音）

[返回深度学习高级概述](overview.md){ .md-button }
