# Policy Gradient 定理完整证明与深入理解

## 目录
1. [引言与动机](#1-引言与动机)
2. [问题设定](#2-问题设定)
3. [Policy Gradient 定理](#3-policy-gradient-定理)
4. [定理证明（完整推导）](#4-定理证明完整推导)
5. [Baseline 理论](#5-baseline-理论)
6. [Compatible Function Approximation](#6-compatible-function-approximation)
7. [不同形式的 Policy Gradient](#7-不同形式的-policy-gradient)
8. [实际应用考虑](#8-实际应用考虑)
9. [与其他方法的联系](#9-与其他方法的联系)
10. [面试常见问题](#10-面试常见问题)

---

## 1. 引言与动机

### 1.1 为什么需要 Policy Gradient？

**Value-based 方法的局限性**：
- Q-learning、DQN 等方法学习 Q(s,a)，然后通过 π(s) = argmax_a Q(s,a) 得到策略
- **问题 1**：动作空间连续时，argmax 难以计算
- **问题 2**：策略是确定性的，无法表示随机策略
- **问题 3**：策略微小变化可能导致 argmax 结果完全不同（不平滑）

**Policy-based 方法的优势**：
- 直接参数化策略 π_θ(a|s)
- 自然支持连续动作空间
- 可以学习随机策略（例如 Rock-Paper-Scissors 游戏）
- 策略平滑变化，更好的收敛性质

### 1.2 核心问题

给定参数化策略 π_θ(a|s)，如何优化参数 θ 来最大化期望回报？

**目标函数**：
```
J(θ) = E_{τ~π_θ}[R(τ)]
     = E_{s_0~μ}[V^{π_θ}(s_0)]
```

**核心问题**：如何计算 ∇_θ J(θ)？

**困难**：
- 期望是对轨迹 τ = (s_0, a_0, r_0, s_1, a_1, r_1, ...) 的，轨迹分布依赖于 θ
- 环境转移概率 P(s'|s,a) 未知且不依赖于 θ
- 不能简单地交换梯度和期望

---

## 2. 问题设定

### 2.1 基本符号

- **状态空间**：S
- **动作空间**：A（离散或连续）
- **策略**：π_θ(a|s)，参数为 θ ∈ ℝ^d
- **状态转移**：P(s'|s,a)
- **奖励函数**：r(s,a) 或 r(s,a,s')
- **折扣因子**：γ ∈ [0,1]

### 2.2 目标函数的三种形式

**Episodic（片段式）**：
```
J(θ) = E_{τ~π_θ}[∑_{t=0}^{T} r_t]
```

**Continuing with discounting（折扣）**：
```
J(θ) = E_{s_0~μ}[V^{π_θ}(s_0)]
     = E_{s_0~μ}[E_{τ~π_θ}[∑_{t=0}^{∞} γ^t r_t | s_0]]
```

**Average reward（平均奖励）**：
```
J(θ) = lim_{T→∞} (1/T) E_{τ~π_θ}[∑_{t=0}^{T} r_t]
```

本文主要讨论折扣形式。

### 2.3 轨迹分布

轨迹 τ = (s_0, a_0, r_0, s_1, a_1, r_1, ...) 的概率：

```
p_θ(τ) = μ(s_0) ∏_{t=0}^{∞} π_θ(a_t|s_t) P(s_{t+1}|s_t,a_t)
```

**关键观察**：
- π_θ(a|s) 依赖于 θ → 可以求导
- P(s'|s,a) 不依赖于 θ → 梯度中会消失
- μ(s_0) 不依赖于 θ

---

## 3. Policy Gradient 定理

### 3.1 定理陈述（Sutton & Barto 版本）

**定理（Policy Gradient Theorem）**：

对于任意可微策略 π_θ(a|s) 和目标函数 J(θ) = E_{s~μ}[V^{π_θ}(s)]，有：

```
∇_θ J(θ) ∝ E_{s~d^{π_θ}, a~π_θ}[Q^{π_θ}(s,a) ∇_θ log π_θ(a|s)]
```

其中：
- d^{π_θ}(s) 是策略 π_θ 下的状态访问分布（on-policy state distribution）
- Q^{π_θ}(s,a) 是状态-动作值函数
- log π_θ(a|s) 的梯度称为 **score function**

**更精确的形式**：

```
∇_θ J(θ) = E_{s~d^{π_θ}, a~π_θ}[Q^{π_θ}(s,a) ∇_θ log π_θ(a|s)]
```

其中 d^{π_θ}(s) 定义为：

```
d^{π_θ}(s) = ∑_{t=0}^{∞} γ^t P(s_t=s|s_0~μ, π_θ)
```

（归一化后除以 ∑_s d^{π_θ}(s) = 1/(1-γ)）

### 3.2 为什么这个定理重要？

**关键洞察**：

1. **环境动力学消失**：梯度中不包含 P(s'|s,a)，无需知道环境模型！
2. **可采样估计**：右边是期望形式，可以用蒙特卡洛采样估计
3. **适用于连续动作**：不需要对动作空间枚举或求 argmax
4. **理论基础**：REINFORCE、Actor-Critic、PPO、TRPO 等算法的基础

**实际应用**：

```python
# 蒙特卡洛估计
∇_θ J(θ) ≈ (1/N) ∑_{i=1}^{N} ∑_{t=0}^{T} Q^π(s_t^i, a_t^i) ∇_θ log π_θ(a_t^i|s_t^i)
```

---

## 4. 定理证明（完整推导）

### 4.1 证明思路概述

**核心思想**：

1. 将 J(θ) 写成对轨迹的期望
2. 利用 log-derivative trick: ∇_θ p_θ(τ) = p_θ(τ) ∇_θ log p_θ(τ)
3. 观察到环境转移概率的梯度为 0
4. 重新整理期望，从轨迹分布转换为状态-动作分布

### 4.2 完整证明

**Step 1：目标函数展开**

```
J(θ) = E_{τ~p_θ}[R(τ)]
     = E_{τ~p_θ}[∑_{t=0}^{∞} γ^t r(s_t, a_t)]
     = ∫ p_θ(τ) R(τ) dτ
```

**Step 2：求梯度**

```
∇_θ J(θ) = ∇_θ ∫ p_θ(τ) R(τ) dτ
         = ∫ ∇_θ p_θ(τ) R(τ) dτ         [交换积分与微分]
```

**Step 3：Log-derivative trick**

这是关键技巧：

```
∇_θ p_θ(τ) = p_θ(τ) ∇_θ log p_θ(τ)
```

**证明**：
```
∇_θ log p_θ(τ) = (1/p_θ(τ)) ∇_θ p_θ(τ)
⟹ ∇_θ p_θ(τ) = p_θ(τ) ∇_θ log p_θ(τ)
```

代入：

```
∇_θ J(θ) = ∫ p_θ(τ) ∇_θ log p_θ(τ) R(τ) dτ
         = E_{τ~p_θ}[R(τ) ∇_θ log p_θ(τ)]
```

**Step 4：展开 log p_θ(τ)**

回忆轨迹概率：

```
p_θ(τ) = μ(s_0) ∏_{t=0}^{∞} π_θ(a_t|s_t) P(s_{t+1}|s_t,a_t)
```

取对数：

```
log p_θ(τ) = log μ(s_0) + ∑_{t=0}^{∞} log π_θ(a_t|s_t) + ∑_{t=0}^{∞} log P(s_{t+1}|s_t,a_t)
```

求梯度：

```
∇_θ log p_θ(τ) = 0 + ∑_{t=0}^{∞} ∇_θ log π_θ(a_t|s_t) + 0
                = ∑_{t=0}^{∞} ∇_θ log π_θ(a_t|s_t)
```

**关键**：μ(s_0) 和 P(s'|s,a) 不依赖于 θ，梯度为 0！

**Step 5：代入得到初步结果**

```
∇_θ J(θ) = E_{τ~p_θ}[R(τ) ∑_{t=0}^{∞} ∇_θ log π_θ(a_t|s_t)]
         = E_{τ~p_θ}[(∑_{t=0}^{∞} γ^t r_t) (∑_{t=0}^{∞} ∇_θ log π_θ(a_t|s_t))]
```

**Step 6：展开双求和**

```
∇_θ J(θ) = E_{τ~p_θ}[∑_{t=0}^{∞} ∑_{t'=0}^{∞} γ^{t'} r_{t'} ∇_θ log π_θ(a_t|s_t)]
```

**Step 7：利用因果性（Causality）**

**关键观察**：时刻 t 的动作 a_t 只影响 t 时刻及之后的奖励，不影响过去的奖励！

即：E[r_{t'} | a_t] 当 t' < t 时与 a_t 无关。

因此，t' < t 时的项期望为 0（更严格地说，通过条件期望分析）。

```
∇_θ J(θ) = E_{τ~p_θ}[∑_{t=0}^{∞} ∇_θ log π_θ(a_t|s_t) (∑_{t'=t}^{∞} γ^{t'} r_{t'})]
```

**Step 8：定义 Q 函数**

注意到：

```
Q^π(s_t, a_t) = E[∑_{t'=t}^{∞} γ^{t'-t} r_{t'} | s_t, a_t]
              = E[∑_{k=0}^{∞} γ^k r_{t+k} | s_t, a_t]
```

而我们有：

```
∑_{t'=t}^{∞} γ^{t'} r_{t'} = γ^t ∑_{k=0}^{∞} γ^k r_{t+k}
                            = γ^t Q^π(s_t, a_t)  [近似]
```

更准确地，定义 Q^π(s,a) = E[∑_{k=0}^{∞} γ^k r_{t+k} | s_t=s, a_t=a]，则：

```
∇_θ J(θ) = E_{τ~p_θ}[∑_{t=0}^{∞} γ^t ∇_θ log π_θ(a_t|s_t) Q^π(s_t, a_t)]
```

**Step 9：改写为状态-动作分布**

```
∇_θ J(θ) = ∑_{t=0}^{∞} γ^t E_{s_t,a_t~p_θ}[Q^π(s_t, a_t) ∇_θ log π_θ(a_t|s_t)]
         = E_{t~Geom(1-γ)} E_{s_t~d^π, a_t~π}[Q^π(s_t, a_t) ∇_θ log π_θ(a_t|s_t)]
```

其中 d^π(s) = ∑_{t=0}^{∞} γ^t P(s_t=s|π_θ) 是折扣状态访问分布。

**归一化后**（忽略常数 1/(1-γ)）：

```
∇_θ J(θ) = E_{s~d^π, a~π}[Q^π(s,a) ∇_θ log π_θ(a|s)]
```

**证毕！** ∎

---

## 5. Baseline 理论

### 5.1 为什么需要 Baseline？

**问题**：直接使用 Q^π(s,a) 会导致高方差。

**原因**：
- Q 值可能总是正的（或总是负的）
- 即使某个动作比平均差，如果 Q > 0，仍然会被鼓励
- 需要一个参考点来判断动作的"相对好坏"

### 5.2 Baseline 定理

**定理**：对于任意函数 b(s)（只依赖于状态），有：

```
E_{s~d^π, a~π}[b(s) ∇_θ log π_θ(a|s)] = 0
```

**因此**，减去 baseline 不改变梯度期望：

```
∇_θ J(θ) = E_{s~d^π, a~π}[(Q^π(s,a) - b(s)) ∇_θ log π_θ(a|s)]
```

**证明**：

```
E_{a~π}[b(s) ∇_θ log π_θ(a|s)]
= b(s) E_{a~π}[∇_θ log π_θ(a|s)]
= b(s) ∑_a π_θ(a|s) ∇_θ log π_θ(a|s)
= b(s) ∑_a π_θ(a|s) · (∇_θ π_θ(a|s) / π_θ(a|s))
= b(s) ∑_a ∇_θ π_θ(a|s)
= b(s) ∇_θ (∑_a π_θ(a|s))
= b(s) ∇_θ 1
= 0
```

（因为 ∑_a π_θ(a|s) = 1 是常数）

**证毕！** ∎

### 5.3 Baseline 减少方差（但不改变期望）

**方差分析**：

设 g = Q^π(s,a) ∇_θ log π_θ(a|s)，我们想减少 Var(g)。

```
Var(g) = E[g²] - (E[g])²
```

加入 baseline b(s) 后：

```
g_b = (Q^π(s,a) - b(s)) ∇_θ log π_θ(a|s)
```

我们有 E[g_b] = E[g]（期望不变），但 Var(g_b) 可以更小！

**最优 baseline**：

最小化方差的 b(s) 是：

```
b*(s) = E_a[(Q^π(s,a) · ||∇_θ log π_θ(a|s)||²)] / E_a[||∇_θ log π_θ(a|s)||²]
```

**实践中**，常用 **V^π(s)** 作为 baseline：

```
∇_θ J(θ) ≈ E[A^π(s,a) ∇_θ log π_θ(a|s)]
```

其中 **Advantage** A^π(s,a) = Q^π(s,a) - V^π(s)。

**直觉**：
- A > 0：动作比平均好，增加概率
- A < 0：动作比平均差，减少概率
- A = 0：动作是平均水平，不改变

### 5.4 数值示例

**例子**：某状态 s 下有 3 个动作，Q 值为：
- Q(s,a₁) = 10
- Q(s,a₂) = 8
- Q(s,a₃) = 12

**Without baseline**：
- 所有动作都被鼓励（Q > 0）
- a₂ 是最差的，但仍然 +8

**With baseline V(s) = 10**：
- A(s,a₁) = 0（不变）
- A(s,a₂) = -2（减少概率）
- A(s,a₃) = +2（增加概率）

清晰地反映了相对优劣！

---

## 6. Compatible Function Approximation

### 6.1 问题设定

在实际中，我们无法精确计算 Q^π(s,a)，需要用函数逼近：

```
Q_w(s,a) ≈ Q^π(s,a)
```

**问题**：用近似的 Q_w 替代真实 Q^π，会引入 bias 吗？

### 6.2 Compatible Function Approximation 定理

**定理（Sutton 2000）**：

如果函数逼近器 Q_w(s,a) 满足以下两个条件：

1. **Compatible condition（兼容性条件）**：
   ```
   ∇_w Q_w(s,a) = ∇_θ log π_θ(a|s)
   ```

2. **Minimum error（最小误差）**：
   ```
   w = argmin_w E_{s~d^π, a~π}[(Q_w(s,a) - Q^π(s,a))²]
   ```

则使用 Q_w 代替 Q^π 时，梯度估计是**无偏的**：

```
E[Q_w(s,a) ∇_θ log π_θ(a|s)] = E[Q^π(s,a) ∇_θ log π_θ(a|s)]
```

### 6.3 证明

**证明**：

设 w* 是最小化均方误差的参数，则梯度为 0：

```
∇_w E[(Q_w(s,a) - Q^π(s,a))²]|_{w=w*} = 0
```

展开：

```
E[2(Q_{w*}(s,a) - Q^π(s,a)) ∇_w Q_{w*}(s,a)] = 0
E[(Q_{w*}(s,a) - Q^π(s,a)) ∇_w Q_{w*}(s,a)] = 0
```

利用兼容性条件 ∇_w Q_w(s,a) = ∇_θ log π_θ(a|s)：

```
E[(Q_{w*}(s,a) - Q^π(s,a)) ∇_θ log π_θ(a|s)] = 0
```

因此：

```
E[Q_{w*}(s,a) ∇_θ log π_θ(a|s)] = E[Q^π(s,a) ∇_θ log π_θ(a|s)]
```

**证毕！** ∎

### 6.4 实际意义

**兼容性条件的形式**：

如果 Q_w 是线性函数：

```
Q_w(s,a) = w^T ∇_θ log π_θ(a|s)
```

则自动满足 ∇_w Q_w = ∇_θ log π_θ！

**Actor-Critic 算法**：
- Actor：策略 π_θ
- Critic：Q_w 或 V_v
- 如果 Q_w 满足兼容性，梯度估计无偏

**实践**：
- 线性 Q：Q_w(s,a) = ϕ(s,a)^T w，其中 ϕ(s,a) = ∇_θ log π_θ(a|s)
- 神经网络：通常不满足严格兼容性，但实践中仍有效（有偏但方差小）

---

## 7. 不同形式的 Policy Gradient

### 7.1 REINFORCE（蒙特卡洛 Policy Gradient）

**最简单形式**：

```
∇_θ J(θ) = E_τ[(∑_{t=0}^T γ^t r_t) (∑_{t=0}^T ∇_θ log π_θ(a_t|s_t))]
```

**因果性改进**（Reward-to-go）：

```
∇_θ J(θ) = E_τ[∑_{t=0}^T ∇_θ log π_θ(a_t|s_t) (∑_{t'=t}^T γ^{t'-t} r_{t'})]
```

**With baseline**：

```
∇_θ J(θ) = E_τ[∑_{t=0}^T (∑_{t'=t}^T γ^{t'-t} r_{t'} - b(s_t)) ∇_θ log π_θ(a_t|s_t)]
```

**算法**：
```python
for episode in episodes:
    τ = rollout(π_θ)  # 采样轨迹
    for t in range(T):
        G_t = sum(γ^k * r_{t+k} for k in range(T-t))
        θ += α * G_t * ∇_θ log π_θ(a_t|s_t)
```

### 7.2 Actor-Critic

**用 V(s) 作为 baseline**：

```
∇_θ J(θ) = E[A(s,a) ∇_θ log π_θ(a|s)]
         = E[(r + γV(s') - V(s)) ∇_θ log π_θ(a|s)]  [TD error]
```

**算法**：
```python
# Critic: 学习 V_v(s)
td_error = r + γ * V_v(s') - V_v(s)
v += α_v * td_error * ∇_v V_v(s)

# Actor: 更新策略
θ += α_θ * td_error * ∇_θ log π_θ(a|s)
```

### 7.3 A2C / A3C

**Advantage Actor-Critic**：

```
A(s,a) = Q(s,a) - V(s)
       ≈ r + γV(s') - V(s)  [1-step]
       ≈ ∑_{k=0}^{n-1} γ^k r_{t+k} + γ^n V(s_{t+n}) - V(s_t)  [n-step]
```

**A3C**：异步并行版本（多个 worker 并行采样）。

### 7.4 GAE (Generalized Advantage Estimation)

**结合不同 n-step advantage**：

```
A^{GAE(λ)}(s_t,a_t) = ∑_{l=0}^{∞} (γλ)^l δ_{t+l}
```

其中 δ_t = r_t + γV(s_{t+1}) - V(s_t) 是 TD error。

**λ 参数**：
- λ = 0：A = δ_t（纯 TD，低方差高偏差）
- λ = 1：A = ∑ γ^k r_k - V(s)（蒙特卡洛，高方差低偏差）
- λ ∈ (0,1)：平衡

参见 `docs/math_theory/gae.md` 详细推导。

### 7.5 PPO (Proximal Policy Optimization)

**Clipped objective**：

```
L^{CLIP}(θ) = E[min(r_t(θ) Â_t, clip(r_t(θ), 1-ε, 1+ε) Â_t)]
```

其中 r_t(θ) = π_θ(a_t|s_t) / π_{θ_old}(a_t|s_t)。

**或者 KL penalty**：

```
L^{KL}(θ) = E[A_t ∇_θ log π_θ(a_t|s_t) - β * KL(π_{θ_old} || π_θ)]
```

参见 `exercises/ch13_policy_gradient/ex03_ppo.py`。

### 7.6 TRPO (Trust Region Policy Optimization)

**约束优化**：

```
maximize_θ  E[A_t ∇_θ log π_θ(a|s)]
subject to  E[KL(π_{θ_old}(·|s) || π_θ(·|s))] ≤ δ
```

使用二阶优化（Natural Gradient，Fisher Information Matrix）。

参见 `exercises/ch13_policy_gradient/ex07_trpo.py`。

---

## 8. 实际应用考虑

### 8.1 方差问题

**Policy Gradient 的方差非常高**！

**原因**：
- 蒙特卡洛估计（轨迹采样）
- 信用分配问题（哪个动作导致了奖励？）

**解决方法**：
1. **Baseline**（减少 30-50% 方差）
2. **Critic**（用 V(s) 或 Q(s,a) 函数逼近）
3. **GAE**（平衡偏差-方差）
4. **Large batch**（增加样本量）
5. **Causality**（reward-to-go，去掉过去奖励）

### 8.2 样本效率

**Policy Gradient 是 on-policy 的**：
- 每次更新后，旧数据不能再用
- 需要重新采样
- 样本效率低

**改进**：
- **PPO**：允许少量 off-policy（importance sampling）
- **Off-policy PG**：使用 importance sampling 完全 off-policy
- **DDPG/TD3/SAC**：确定性策略梯度 + off-policy

### 8.3 步长选择

**问题**：步长太大导致策略崩溃。

**解决**：
- **TRPO**：约束 KL 散度
- **PPO**：clip 比率
- **Adaptive learning rate**：根据 KL 散度调整

### 8.4 探索问题

**策略梯度自然支持探索**（随机策略），但仍可能陷入局部最优。

**改进**：
- **Entropy bonus**：H(π) = -∑ π log π，鼓励探索
- **Temperature**：π_θ(a|s) ∝ exp(logits / τ)
- **Intrinsic motivation**（ICM, RND 等）

---

## 9. 与其他方法的联系

### 9.1 Policy Gradient vs Q-learning

| 特性 | Policy Gradient | Q-learning |
|------|----------------|------------|
| 学习对象 | π_θ(a\|s) | Q(s,a) |
| 动作空间 | 连续/离散 | 主要是离散 |
| 策略类型 | 随机 | 确定性（ε-greedy 除外） |
| 样本效率 | 低（on-policy） | 高（off-policy） |
| 方差 | 高 | 低 |
| 收敛性 | 局部最优 | 全局最优（表格） |

### 9.2 Actor-Critic：结合两者

- **Actor**：策略 π_θ（Policy Gradient）
- **Critic**：价值 V_v 或 Q_w（Q-learning）
- **优势**：降低方差，提高样本效率

### 9.3 Deterministic Policy Gradient (DPG)

**确定性策略**：μ_θ(s) 输出单个动作（而非分布）。

**梯度公式**：

```
∇_θ J(θ) = E_s[∇_θ μ_θ(s) ∇_a Q(s,a)|_{a=μ_θ(s)}]
```

**链式法则**：
1. 改变 θ → 改变 μ_θ(s)
2. 改变 a → 改变 Q(s,a)

**应用**：DDPG, TD3（连续控制）。

### 9.4 Natural Policy Gradient

**问题**：参数空间的欧式距离不等于策略空间的距离。

**解决**：使用 **Fisher Information Matrix** F：

```
θ_{t+1} = θ_t + α F^{-1} ∇_θ J(θ)
```

其中：

```
F = E[∇_θ log π_θ(a|s) ∇_θ log π_θ(a|s)^T]
```

**优势**：
- 策略空间的自然度量
- 更快收敛
- TRPO 使用此思想

---

## 10. 面试常见问题

### Q1: 请解释 Policy Gradient 定理，并说明为什么梯度中没有环境模型？

**答案**：

Policy Gradient 定理表明：

```
∇_θ J(θ) = E_{s~d^π, a~π}[Q^π(s,a) ∇_θ log π_θ(a|s)]
```

**关键**：梯度中不包含环境转移概率 P(s'|s,a)。

**原因**：

在推导中，我们有：

```
log p_θ(τ) = log μ(s_0) + ∑_t log π_θ(a_t|s_t) + ∑_t log P(s_{t+1}|s_t,a_t)
```

求梯度时，P(s'|s,a) 不依赖于 θ，所以：

```
∇_θ log p_θ(τ) = ∑_t ∇_θ log π_θ(a_t|s_t)
```

这意味着我们可以在**不知道环境模型**的情况下计算梯度，只需要能够：
1. 采样轨迹
2. 计算策略的对数概率及其梯度

这是 **model-free** 强化学习的基础。

---

### Q2: 为什么加入 baseline 不改变梯度的期望，但能减少方差？

**答案**：

**Part 1：为什么期望不变？**

对于任意 b(s)，有：

```
E_a[b(s) ∇_θ log π_θ(a|s)] = b(s) ∑_a π_θ(a|s) ∇_θ log π_θ(a|s)
                             = b(s) ∑_a ∇_θ π_θ(a|s)
                             = b(s) ∇_θ (∑_a π_θ(a|s))
                             = b(s) ∇_θ 1 = 0
```

因此：E[(Q - b) ∇ log π] = E[Q ∇ log π] - E[b ∇ log π] = E[Q ∇ log π]。

**Part 2：为什么方差减少？**

考虑梯度估计 g = Q ∇ log π：
- 如果所有 Q 值都很大且为正，g 的值会很大
- 不同动作的 Q 值差异才是我们关心的

加入 baseline V(s) 后，使用 Advantage A = Q - V：
- A 可正可负，围绕 0
- E[A] = 0（期望优势为 0）
- 数值范围更小 → 方差更小

**直觉**：baseline 把"绝对好坏"转换为"相对好坏"。

---

### Q3: Compatible Function Approximation 是什么？为什么重要？

**答案**：

**定义**：函数逼近器 Q_w(s,a) 是 compatible 的，如果：

```
∇_w Q_w(s,a) = ∇_θ log π_θ(a|s)
```

且 w 最小化均方误差。

**重要性**：

1. **无偏性**：即使用近似的 Q_w 代替真实 Q^π，梯度估计仍然无偏
2. **理论保证**：Actor-Critic 算法的收敛性保证
3. **实践指导**：提示我们如何设计 Critic 网络

**实现**：

线性形式：Q_w(s,a) = w^T ∇_θ log π_θ(a|s)

神经网络中通常不严格满足，但：
- 实践中仍有效（有偏但低方差）
- 现代方法（PPO, TRPO）通过其他手段保证稳定性

---

### Q4: REINFORCE 算法有什么优缺点？

**答案**：

**优点**：

1. **简单直观**：直接实现 Policy Gradient 定理
2. **无偏**：梯度估计是无偏的
3. **通用性**：适用于任何可微策略
4. **支持连续动作**：不需要 argmax

**缺点**：

1. **高方差**：
   - 蒙特卡洛估计（完整轨迹）
   - 需要大量样本才能收敛

2. **样本效率低**：
   - On-policy（每次更新后必须重新采样）
   - 每个样本只用一次

3. **学习慢**：
   - 信用分配问题（难以确定哪个动作导致奖励）
   - 稀疏奖励环境尤其困难

**改进方向**：
- 加 baseline → Actor-Critic
- 使用 TD 估计 → A2C
- 使用 GAE → PPO
- Off-policy 版本 → 重要性采样

---

### Q5: 解释 Policy Gradient 中的"因果性"（Causality）是什么？

**答案**：

**因果性**：时刻 t 的动作 a_t 只影响 t 时刻及之后的奖励，不影响过去的奖励。

**数学表示**：

原始形式：

```
∇_θ J(θ) = E[(∑_{t=0}^T r_t) (∑_{t=0}^T ∇_θ log π_θ(a_t|s_t))]
```

利用因果性简化为（reward-to-go）：

```
∇_θ J(θ) = E[∑_{t=0}^T ∇_θ log π_θ(a_t|s_t) (∑_{t'=t}^T r_{t'})]
```

**为什么有用？**

1. **减少方差**：
   - 原始形式中，每个 ∇ log π 都乘以所有奖励
   - reward-to-go 只乘以未来奖励
   - 减少了无关项，降低方差

2. **更准确的信用分配**：
   - 动作 a_t 只对未来负责
   - 过去的奖励不应影响当前动作的梯度

**实践**：

```python
# 错误（未使用因果性）
for t in range(T):
    G = sum(rewards)  # 所有奖励
    grad += G * grad_log_pi[t]

# 正确（使用因果性）
for t in range(T):
    G = sum(rewards[t:])  # 只有未来奖励
    grad += G * grad_log_pi[t]
```

---

### Q6: 为什么 Policy Gradient 方法比 Q-learning 更适合连续动作空间？

**答案**：

**Q-learning 在连续动作空间的问题**：

1. **argmax 难以计算**：
   ```
   π(s) = argmax_a Q(s,a)
   ```
   当 a ∈ ℝ^d 时，需要优化求解（非凸）

2. **动作空间离散化**：
   - 将连续空间离散化 → 维度灾难
   - 例如：10 维动作，每维 10 个离散值 → 10^10 个动作

3. **表示困难**：
   - Q(s,a) 需要对每个 (s,a) 对估计
   - 连续 a 意味着无限个值

**Policy Gradient 的优势**：

1. **直接输出动作**：
   ```
   π_θ(a|s) = N(μ_θ(s), σ²)  # 高斯策略
   ```
   参数化均值和方差，直接采样

2. **自然支持连续分布**：
   - 输出概率密度，而非离散概率
   - 梯度可以通过重参数化技巧计算

3. **平滑优化**：
   - θ 的微小变化 → π 的平滑变化
   - Q-learning 中 θ 微小变化可能导致 argmax 突变

**实际算法**：
- DDPG, TD3, SAC：确定性策略梯度 + off-policy
- PPO：随机策略 + 高斯分布

---

### Q7: 解释 Actor-Critic 中 Actor 和 Critic 分别做什么？

**答案**：

**Actor（演员）**：
- **功能**：学习策略 π_θ(a|s)
- **目标**：最大化期望回报 J(θ)
- **更新**：使用 Policy Gradient
  ```
  θ += α * A(s,a) * ∇_θ log π_θ(a|s)
  ```

**Critic（评论家）**：
- **功能**：学习价值函数 V_v(s) 或 Q_w(s,a)
- **目标**：准确估计状态/动作的价值
- **更新**：使用 TD learning
  ```
  v += β * (r + γV(s') - V(s)) * ∇_v V_v(s)
  ```

**两者关系**：

1. **Critic 评估 Actor**：
   - Critic 计算 Advantage：A = Q(s,a) - V(s) 或 TD error：δ = r + γV(s') - V(s)
   - 告诉 Actor 这个动作比平均好多少

2. **Actor 提供数据**：
   - Actor 执行策略，生成轨迹 (s,a,r,s')
   - Critic 用这些数据学习价值函数

**优势**：

- **降低方差**：Critic 提供低方差的价值估计（相比 Monte Carlo）
- **提高效率**：不需要等到 episode 结束
- **Bootstrap**：TD learning 加速学习

**代码示意**：

```python
# Critic update
td_error = r + gamma * V(s_next) - V(s)
V_params -= lr_v * td_error * grad_V(s)

# Actor update
advantage = td_error  # 或 Q(s,a) - V(s)
theta += lr_theta * advantage * grad_log_pi(a, s)
```

---

### Q8: Natural Policy Gradient 和普通 Policy Gradient 有什么区别？

**答案**：

**普通 Policy Gradient**：

```
θ_{t+1} = θ_t + α ∇_θ J(θ)
```

在**参数空间**的欧式度量下梯度上升。

**问题**：
- 参数空间的距离 ||Δθ|| 不等于策略空间的距离 KL(π_θ || π_{θ+Δθ})
- 相同的 Δθ 在不同位置可能导致策略的巨大或微小变化
- 步长难以选择

**Natural Policy Gradient**：

```
θ_{t+1} = θ_t + α F^{-1} ∇_θ J(θ)
```

其中 F 是 **Fisher Information Matrix**：

```
F = E[∇_θ log π_θ(a|s) (∇_θ log π_θ(a|s))^T]
```

**几何解释**：

- F 定义了策略空间的**黎曼度量**
- F^{-1} ∇J 是策略空间中的最陡方向
- 保证相同的"策略距离"下更新

**优势**：

1. **更好的收敛性**：参数化无关（reparametrization invariant）
2. **自动步长调整**：在策略空间中均匀前进
3. **理论保证**：单调改进（TRPO 利用此性质）

**实践**：

- **精确计算**：F 是 d×d 矩阵，计算和求逆昂贵（O(d³)）
- **近似**：
  - Conjugate Gradient（TRPO）
  - Kronecker-factored（K-FAC）
  - 对角近似

**关系**：
- TRPO ≈ Natural PG + 信赖域约束
- PPO ≈ 简化版 TRPO（一阶方法）

---

### Q9: 如何在 Policy Gradient 中处理离散和连续动作空间？

**答案**：

**离散动作空间**（例如 Atari 游戏，围棋）：

**策略参数化**：Softmax

```
π_θ(a|s) = exp(f_θ(s,a)) / ∑_{a'} exp(f_θ(s,a'))
```

**梯度**：

```
∇_θ log π_θ(a|s) = ∇_θ f_θ(s,a) - E_a'[∇_θ f_θ(s,a')]
                  = ∇_θ f_θ(s,a) - ∑_a' π_θ(a'|s) ∇_θ f_θ(s,a')
```

**实现**：

```python
logits = neural_net(state)  # shape: (batch, num_actions)
probs = softmax(logits)
action = sample(probs)
log_prob = log(probs[action])
grad = grad_log_prob  # 自动微分
```

---

**连续动作空间**（例如机器人控制，自动驾驶）：

**策略参数化**：高斯分布

```
π_θ(a|s) = N(a | μ_θ(s), σ_θ²(s))
```

或者对角协方差：

```
π_θ(a|s) = ∏_i N(a_i | μ_θ,i(s), σ_θ,i²(s))
```

**对数概率**：

```
log π_θ(a|s) = -∑_i [(a_i - μ_i)² / (2σ_i²) + log σ_i + const]
```

**梯度**：

```
∇_μ log π = (a - μ) / σ²
∇_σ log π = [(a - μ)² / σ³ - 1/σ]
```

**实现**：

```python
mu, sigma = neural_net(state)  # 输出均值和标准差
dist = Normal(mu, sigma)
action = dist.sample()
log_prob = dist.log_prob(action).sum()  # 多维独立
grad = grad_log_prob  # 自动微分
```

**其他分布**：
- **Beta 分布**：有界动作（例如 [0,1]）
- **混合高斯**：多模态策略
- **确定性策略**：DDPG, TD3（μ_θ(s) 直接输出动作）

---

### Q10: 手推一个简单的 Policy Gradient 更新例子

**问题设置**：

- 状态 s（2 维特征）
- 动作 a ∈ {0, 1}（二分类）
- 线性策略：logit(a=1|s) = θ^T s
- 策略：π_θ(a=1|s) = sigmoid(θ^T s)
- 单步奖励 r = 10（a=1）或 -5（a=0）

**目标**：更新 θ 来增加 a=1 的概率。

---

**Step 1：采样**

采样一个样本：
- s = [1, 2]
- θ = [0.5, 0.3]
- logit = θ^T s = 0.5×1 + 0.3×2 = 1.1
- π_θ(a=1|s) = sigmoid(1.1) ≈ 0.75
- 采样得到 a = 1，奖励 r = 10

---

**Step 2：计算 log π**

```
log π_θ(a=1|s) = log(0.75) ≈ -0.288
```

或者用公式：

```
log π(a=1|s) = log sigmoid(θ^T s) = -log(1 + exp(-θ^T s))
             = -log(1 + exp(-1.1)) ≈ -0.288
```

---

**Step 3：计算梯度**

```
∇_θ log π_θ(a=1|s) = ∇_θ [-log(1 + exp(-θ^T s))]
                    = exp(-θ^T s) / (1 + exp(-θ^T s)) · s
                    = (1 - sigmoid(θ^T s)) · s
                    = (1 - 0.75) · [1, 2]
                    = 0.25 · [1, 2]
                    = [0.25, 0.5]
```

---

**Step 4：Policy Gradient 更新**

REINFORCE 公式（无 baseline）：

```
∇_θ J(θ) ≈ r · ∇_θ log π_θ(a|s)
         = 10 · [0.25, 0.5]
         = [2.5, 5.0]
```

更新（学习率 α = 0.1）：

```
θ_new = θ + α · ∇J
      = [0.5, 0.3] + 0.1 · [2.5, 5.0]
      = [0.5, 0.3] + [0.25, 0.5]
      = [0.75, 0.8]
```

---

**Step 5：验证**

新策略下：

```
logit_new = [0.75, 0.8]^T [1, 2] = 0.75 + 1.6 = 2.35
π_new(a=1|s) = sigmoid(2.35) ≈ 0.91
```

概率从 0.75 增加到 0.91，成功！

---

**如果用 baseline**（假设 V(s) = 3）：

```
Advantage = r - V(s) = 10 - 3 = 7
∇J = 7 · [0.25, 0.5] = [1.75, 3.5]
```

更新幅度减小，但方向相同（因为 Advantage > 0）。

---

## 总结

**Policy Gradient 定理的核心价值**：

1. **理论突破**：证明了策略梯度可以在不知道环境模型的情况下计算
2. **实践基础**：现代深度 RL 算法（PPO, TRPO, SAC 等）的数学基础
3. **通用性**：适用于离散/连续、确定性/随机策略

**关键要点**：

- ∇J = E[Q^π(s,a) ∇ log π(a|s)]
- Baseline 不改变期望但减少方差
- Compatible FA 保证无偏性
- 因果性减少方差
- Actor-Critic 结合 PG 和 value-based 方法

**学习建议**：

1. **先理解直觉**：为什么 ∇ log π 是"梯度方向"？
2. **掌握推导**：至少能推导一次完整证明
3. **实现 REINFORCE**：从最简单开始
4. **理解变体**：A2C, PPO, TRPO 的改进点
5. **实践调参**：学习率、baseline、entropy bonus

希望这份文档能帮助你深入理解 Policy Gradient 的数学原理和实践技巧！
