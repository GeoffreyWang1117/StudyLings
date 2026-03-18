# Hyperparameter Tuning 完整指南：深度强化学习调参宝典

## 目录
1. [引言：为什么 RL 调参如此困难？](#1-引言为什么-rl-调参如此困难)
2. [关键超参数总览](#2-关键超参数总览)
3. [通用超参数详解](#3-通用超参数详解)
4. [算法特定超参数](#4-算法特定超参数)
5. [调优策略](#5-调优策略)
6. [实践技巧与经验法则](#6-实践技巧与经验法则)
7. [调优工具与框架](#7-调优工具与框架)
8. [常见问题诊断](#8-常见问题诊断)
9. [案例研究](#9-案例研究)
10. [面试常见问题](#10-面试常见问题)

---

## 1. 引言：为什么 RL 调参如此困难？

### 1.1 RL vs 监督学习

| 特性 | 监督学习 | 强化学习 |
|------|---------|---------|
| 目标函数 | 固定损失 | 期望回报（非稳态） |
| 数据分布 | 固定 i.i.d. | 变化（策略改进） |
| 反馈 | 即时标签 | 延迟奖励 |
| 超参数敏感性 | 中等 | 极高 |
| 调试难度 | 低-中 | 高 |

**RL 调参的挑战**：

1. **非平稳性**：数据分布随策略改变
2. **延迟反馈**：难以快速验证参数是否好
3. **高方差**：性能震荡大，难以判断趋势
4. **样本昂贵**：每次尝试需要大量 episode
5. **交互效应**：超参数之间相互影响

**结果**：
- 同样的算法，不同超参数可能差 10 倍性能
- 某些超参数在特定任务上工作，其他任务失败
- 需要大量经验和实验

---

### 1.2 调参的重要性

**论文复现的最大障碍**：
> "我们用了论文里的算法，但性能差得多"

**原因**：
- 论文可能未公开所有超参数
- 环境细节差异（状态归一化、奖励缩放等）
- 随机种子运气

**OpenAI 的观察**：
> "In RL, hyperparameters matter more than the algorithm."

**案例**：
- 调得好的 DQN > 调得差的 Rainbow
- 调得好的 REINFORCE > 调得差的 PPO

---

### 1.3 本指南的目标

1. **系统化知识**：每个超参数的作用和范围
2. **实践经验**：默认值、调优顺序、常见陷阱
3. **工具方法**：自动化调优工具
4. **诊断技巧**：如何快速定位问题

---

## 2. 关键超参数总览

### 2.1 超参数分类

**Level 1：核心超参数（必调）**
- Learning rate（学习率）
- Network architecture（网络架构）
- Discount factor γ（折扣因子）
- Batch size（批大小）

**Level 2：重要超参数（强烈建议调）**
- Exploration（探索策略）
- Replay buffer size（经验回放大小，off-policy）
- Target network update frequency（目标网络更新频率，DQN）
- Entropy coefficient（熵系数，Policy Gradient）
- GAE λ（PPO, A2C）

**Level 3：微调超参数（任务特定）**
- Gradient clipping（梯度裁剪）
- Reward scaling（奖励缩放）
- Frame skip / stacking（帧跳跃/堆叠）
- Optimizer parameters（优化器参数）

---

### 2.2 快速参考表

**DQN**：
| 超参数 | 默认值 | 调优范围 | 优先级 |
|--------|--------|----------|--------|
| Learning rate | 1e-4 | [1e-5, 1e-3] | ⭐⭐⭐ |
| Batch size | 32 | [16, 128] | ⭐⭐ |
| Replay buffer size | 1e6 | [1e4, 1e6] | ⭐⭐ |
| Target update freq | 1000 | [100, 10000] | ⭐⭐ |
| γ (discount) | 0.99 | [0.95, 0.999] | ⭐⭐⭐ |
| ε-greedy (start) | 1.0 | 固定 | ⭐ |
| ε-greedy (end) | 0.01 | [0.001, 0.1] | ⭐⭐ |
| ε-decay steps | 1e6 | [1e4, 1e6] | ⭐ |

**PPO**：
| 超参数 | 默认值 | 调优范围 | 优先级 |
|--------|--------|----------|--------|
| Learning rate | 3e-4 | [1e-5, 1e-3] | ⭐⭐⭐ |
| Batch size | 64 | [32, 256] | ⭐⭐ |
| Num epochs | 10 | [3, 30] | ⭐⭐ |
| GAE λ | 0.95 | [0.9, 0.99] | ⭐⭐ |
| γ (discount) | 0.99 | [0.95, 0.999] | ⭐⭐⭐ |
| Clip range | 0.2 | [0.1, 0.3] | ⭐⭐ |
| Entropy coef | 0.01 | [0, 0.1] | ⭐⭐ |
| Value loss coef | 0.5 | [0.25, 1.0] | ⭐ |

**SAC**：
| 超参数 | 默认值 | 调优范围 | 优先级 |
|--------|--------|----------|--------|
| Learning rate | 3e-4 | [1e-5, 1e-3] | ⭐⭐⭐ |
| Batch size | 256 | [64, 512] | ⭐⭐ |
| Replay buffer size | 1e6 | [1e5, 1e6] | ⭐⭐ |
| Target update τ | 0.005 | [0.001, 0.01] | ⭐ |
| γ (discount) | 0.99 | [0.95, 0.999] | ⭐⭐⭐ |
| α (entropy) | auto | [0.1, 0.5] or auto | ⭐⭐ |
| Update-to-data | 1.0 | [0.1, 1.0] | ⭐ |

---

## 3. 通用超参数详解

### 3.1 Learning Rate（学习率）⭐⭐⭐

**作用**：控制参数更新步长。

**理论**：
```
θ_{t+1} = θ_t + α ∇J(θ)
```
α 太大 → 不稳定、震荡、发散
α 太小 → 学习慢、可能卡在局部最优

**默认值**：
- DQN: 1e-4
- PPO: 3e-4
- SAC: 3e-4
- A2C: 7e-4

**调优范围**：[1e-5, 1e-3]

**调优策略**：

**1. 对数搜索**：
```python
learning_rates = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3]
for lr in learning_rates:
    train(lr=lr)
```

**2. 学习率调度**：

```python
# 线性衰减（PPO 常用）
lr_t = lr_init * (1 - t / T)

# 指数衰减
lr_t = lr_init * decay_rate^(t / decay_steps)

# Cosine annealing
lr_t = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(π * t / T))
```

**诊断**：

- **Loss 爆炸** → lr 太大
- **学习太慢** → lr 太小
- **震荡** → lr 太大 or need gradient clipping

**建议**：

- 从默认值开始（3e-4）
- 观察 loss curve
- 如果不稳定，减半；如果太慢，加倍
- PPO: 用 linear decay
- DQN/SAC: 通常固定 lr

---

### 3.2 Network Architecture（网络架构）⭐⭐⭐

**作用**：函数逼近器的表达能力。

**常见架构**：

**MLP（全连接，低维状态）**：
```python
# 简单任务（CartPole, MountainCar）
[state_dim, 64, 64, action_dim]

# 中等任务（MuJoCo）
[state_dim, 256, 256, action_dim]

# 复杂任务
[state_dim, 400, 300, action_dim]  # DDPG 论文
```

**CNN（图像输入，Atari）**：
```python
# Nature DQN
Conv2D(32, 8x8, stride=4) → ReLU
Conv2D(64, 4x4, stride=2) → ReLU
Conv2D(64, 3x3, stride=1) → ReLU
Flatten → FC(512) → ReLU → FC(action_dim)
```

**调优要点**：

**1. 层数**：
- 太浅：表达能力不足
- 太深：过拟合、梯度消失

通常 2-3 层隐藏层足够（RL 不像 CV 需要很深）。

**2. 宽度**：
- 小任务：64-128
- 中等：256-512
- 大任务：512-1024

**3. 激活函数**：
- **ReLU**：默认选择，简单有效
- **Tanh**：输出有界，适合策略网络
- **ELU/LeakyReLU**：减少死神经元

**4. 初始化**：
```python
# Orthogonal（PPO, A2C 常用）
nn.init.orthogonal_(layer.weight, gain=np.sqrt(2))

# Xavier（DQN 常用）
nn.init.xavier_uniform_(layer.weight)
```

**5. 归一化**：
```python
# Layer Normalization（有时帮助稳定性）
x = LayerNorm(x)

# 不推荐 Batch Norm（RL 数据非 i.i.d.）
```

**建议**：

- 从简单开始（2 层，64-128 单元）
- 性能不够再加深/加宽
- Actor 和 Critic 可以用不同架构
- 共享层（shared layers）可以提高效率

---

### 3.3 Discount Factor γ（折扣因子）⭐⭐⭐

**作用**：权衡短期 vs 长期奖励。

**理论**：
```
V(s) = E[∑_{t=0}^{∞} γ^t r_t]
```

γ = 0：只关心即时奖励（短视）
γ = 1：所有未来奖励同等重要（无折扣）
γ ∈ (0.9, 0.99)：平衡

**影响**：

1. **Effective horizon**（有效视野）：
   ```
   H_eff ≈ 1 / (1 - γ)
   ```
   - γ = 0.9 → H ≈ 10 步
   - γ = 0.99 → H ≈ 100 步
   - γ = 0.999 → H ≈ 1000 步

2. **值函数尺度**：
   - γ 大 → V(s) 大
   - 影响学习稳定性

3. **信用分配**：
   - γ 小 → 短期信用分配容易
   - γ 大 → 长期规划，但学习慢

**调优**：

**任务特性**：
- **短期任务**（几步完成）：γ = 0.9 - 0.95
- **中期任务**（10-100 步）：γ = 0.99
- **长期任务**（>100 步）：γ = 0.995 - 0.999

**诊断**：
- **短视行为**（只要即时奖励）→ γ 太小
- **学习不稳定、值爆炸** → γ 太大

**建议**：
- 默认 γ = 0.99（适用大多数任务）
- 调整范围：[0.95, 0.999]
- 通常不是第一优先级（先调 lr）

---

### 3.4 Batch Size（批大小）⭐⭐

**作用**：每次更新使用的样本数。

**影响**：

**梯度估计**：
- 小 batch：高方差、不稳定、但探索性强
- 大 batch：低方差、稳定、但可能陷入局部最优

**计算效率**：
- 小 batch：GPU 利用率低
- 大 batch：并行计算高效

**学习动态**：
- 小 batch：噪声梯度，类似 SGD
- 大 batch：接近全梯度

**推荐值**：

| 算法 | 默认 Batch Size | 说明 |
|------|----------------|------|
| DQN | 32 | 小 batch 足够 |
| PPO | 64 - 256 | 取决于 horizon |
| SAC | 256 | Off-policy 更大 batch |
| A2C | num_envs × horizon | 并行环境数 |

**调优**：

```python
# 对数搜索
batch_sizes = [16, 32, 64, 128, 256]
```

**权衡**：
- 计算资源充足 → 增大 batch（稳定性）
- 样本昂贵 → 减小 batch（更新频繁）

**与 Learning Rate 的关系**：

大 batch → 可能需要大 lr（线性缩放规则）

```python
lr_new = lr_base * (batch_size_new / batch_size_base)
```

---

### 3.5 Exploration（探索策略）⭐⭐⭐

**Value-based（DQN）：ε-greedy**

**参数**：
- ε_start：初始探索率（通常 1.0）
- ε_end：最终探索率（0.01 - 0.1）
- ε_decay：衰减步数（1e4 - 1e6）

```python
def epsilon(step):
    fraction = min(step / ε_decay, 1.0)
    return ε_start + fraction * (ε_end - ε_start)

action = random_action() if random() < epsilon(step) else argmax(Q(s))
```

**调优**：
- 简单任务：ε_end = 0.01，快速衰减
- 探索性任务：ε_end = 0.1，慢衰减
- 持续探索：ε_end = 0.05，长 decay

---

**Policy-based（PPO, SAC）：Entropy**

**Entropy Bonus**：
```
L = L_policy - c_entropy × H(π)
```

H(π) = -∑ π(a|s) log π(a|s)

**c_entropy（熵系数）**：
- 太小：策略过早确定性，探索不足
- 太大：策略始终随机，不收敛

**推荐值**：
- PPO: 0.01（离散），0.0（连续）
- SAC: 自适应（auto-tuning）

**调优**：
```python
# 固定
entropy_coef = 0.01

# 衰减（PPO 有时用）
entropy_coef_t = entropy_coef_init * decay^t

# 自适应（SAC）
α = log_α.exp()  # 学习 α
```

---

### 3.6 Gradient Clipping（梯度裁剪）⭐⭐

**作用**：防止梯度爆炸。

**方法**：

**Norm clipping**（推荐）：
```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
```

**Value clipping**：
```python
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=1.0)
```

**推荐值**：
- PPO: 0.5
- DQN: 1.0 或 10.0
- SAC: 通常不需要（off-policy 更稳定）

**诊断**：
- **Loss 突然爆炸** → 需要 clipping
- **梯度范数** >> 1 → 需要 clipping

```python
# 监控梯度范数
grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=float('inf'))
logger.log("grad_norm", grad_norm)
```

---

## 4. 算法特定超参数

### 4.1 DQN 特定

**Replay Buffer Size**：

**作用**：存储多少 transitions。

**影响**：
- 太小：样本相关性高、过拟合
- 太大：旧数据（off-policy 严重）、内存占用

**推荐**：
- Atari: 1e6
- 简单任务: 1e4 - 1e5
- 连续控制: 1e6

---

**Target Network Update Frequency**：

**作用**：多久更新一次目标网络 Q_target。

**Hard update**（原始 DQN）：
```python
if step % target_update_freq == 0:
    Q_target.load_state_dict(Q.state_dict())
```

**Soft update**（DDPG, SAC）：
```python
# 每步更新
for param, target_param in zip(Q.parameters(), Q_target.parameters()):
    target_param.data.copy_(τ * param.data + (1 - τ) * target_param.data)
```

**推荐**：
- Hard update: 1000 - 10000 步
- Soft update τ: 0.001 - 0.01

**影响**：
- 频繁更新：目标不稳定
- 稀疏更新：目标滞后、学习慢

---

**Double DQN**：

**超参数**：无额外超参数，但与 target network 交互。

建议：总是使用 Double DQN（减少高估，几乎无代价）。

---

### 4.2 PPO 特定

**Clip Range（ε）**：

**作用**：限制策略更新幅度。

```
L^{CLIP} = min(r_t A_t, clip(r_t, 1-ε, 1+ε) A_t)
```

**推荐**：ε = 0.2

**调优**：
- 保守更新：ε = 0.1
- 激进更新：ε = 0.3

**诊断**：
- **策略变化太小**（KL 散度小）→ 增大 ε
- **训练不稳定** → 减小 ε

---

**Number of Epochs**：

**作用**：每批数据重用几次。

**推荐**：3 - 10

**权衡**：
- 太少：样本效率低
- 太多：过拟合旧策略数据

**诊断**：
- 监控 KL 散度：
  ```python
  if kl > target_kl:
      break  # 提前停止 epoch
  ```

---

**GAE λ**：

**作用**：平衡偏差-方差（Advantage 估计）。

```
A^{GAE} = ∑_{l=0}^{∞} (γλ)^l δ_{t+l}
```

**推荐**：λ = 0.95

**调优**：
- 低方差任务：λ → 1.0（接近 MC）
- 高方差任务：λ → 0.9（接近 TD）

参见 `docs/math_theory/gae.md`。

---

**Value Loss Coefficient**：

**作用**：Critic 损失的权重。

```
L_total = L_policy - c_entropy × H + c_value × L_value
```

**推荐**：c_value = 0.5

通常不敏感，默认值即可。

---

### 4.3 SAC 特定

**Temperature α（熵权重）**：

**作用**：控制探索 vs 利用。

```
J = E[∑ r_t + α H(π)]
```

**Fixed α**：
- 推荐：0.2（连续）、0.1（离散）

**Auto-tuning**（推荐）：
```python
log_α = torch.tensor(0.0, requires_grad=True)
α = log_α.exp()

# 优化目标：H(π) ≈ -dim(A)（期望熵）
α_loss = -α * (log_prob + target_entropy).detach()
```

**建议**：
- 默认使用 auto-tuning
- 只在特殊任务手动调

---

**Soft Update τ**：

**作用**：目标网络软更新系数。

```
θ_target ← τ θ + (1 - τ) θ_target
```

**推荐**：τ = 0.005

**调优**：[0.001, 0.01]

**影响**：
- τ 大：目标更新快、不太稳定
- τ 小：目标滞后、稳定但慢

---

**Update-to-Data Ratio**：

**作用**：每收集一个样本，进行多少次梯度更新。

**推荐**：1.0（每步更新一次）

**调优**：
- 样本昂贵：1.0 - 4.0（多次更新）
- 计算受限：0.1 - 1.0

---

## 5. 调优策略

### 5.1 手动调优（Manual Tuning）

**阶段 1：建立 Baseline**

```python
# 使用默认超参数
config = {
    'lr': 3e-4,
    'gamma': 0.99,
    'batch_size': 64,
    # ... 其他默认值
}

baseline_performance = train(config)
```

**阶段 2：单变量调优**

```python
# 调 learning rate
for lr in [1e-4, 3e-4, 1e-3]:
    config['lr'] = lr
    performance = train(config)
    log(lr, performance)

# 选择最佳，固定
best_lr = select_best(...)
config['lr'] = best_lr

# 依次调其他超参数
```

**顺序建议**：
1. Learning rate
2. Network architecture
3. Discount γ
4. Exploration（ε, entropy）
5. Batch size
6. 算法特定（clip, GAE λ, etc.）

---

### 5.2 网格搜索（Grid Search）

**适用**：超参数少（1-2 个）、计算资源充足。

```python
learning_rates = [1e-4, 3e-4, 1e-3]
batch_sizes = [32, 64, 128]

for lr in learning_rates:
    for bs in batch_sizes:
        config = {'lr': lr, 'batch_size': bs, ...}
        performance = train(config)
        log(config, performance)
```

**优点**：
- 完整覆盖
- 容易并行

**缺点**：
- 组合爆炸（超参数多时不可行）
- 采样不均匀（中间值可能被跳过）

---

### 5.3 随机搜索（Random Search）

**推荐**：比网格搜索更高效！

```python
import numpy as np

n_trials = 50

for _ in range(n_trials):
    config = {
        'lr': 10 ** np.random.uniform(-5, -3),  # log-uniform [1e-5, 1e-3]
        'batch_size': np.random.choice([32, 64, 128, 256]),
        'gamma': np.random.uniform(0.95, 0.999),
        'entropy_coef': 10 ** np.random.uniform(-3, -1),
    }
    performance = train(config)
    log(config, performance)
```

**分布选择**：
- **Log-uniform**（学习率、熵系数等）：
  ```python
  10 ** np.random.uniform(log10(min), log10(max))
  ```

- **Uniform**（γ, λ 等）：
  ```python
  np.random.uniform(min, max)
  ```

- **Categorical**（离散选择）：
  ```python
  np.random.choice([32, 64, 128])
  ```

**优点**：
- 更好的覆盖（尤其高维）
- 容易扩展超参数数量
- 可以提前停止差的配置

**论文**：*Random Search for Hyper-Parameter Optimization* (Bergstra & Bengio, 2012)

---

### 5.4 贝叶斯优化（Bayesian Optimization）

**思想**：用高斯过程建模"超参数 → 性能"，智能选择下一个尝试的配置。

**工具**：
- Optuna
- Ray Tune
- Hyperopt

**例子（Optuna）**：

```python
import optuna

def objective(trial):
    config = {
        'lr': trial.suggest_loguniform('lr', 1e-5, 1e-3),
        'batch_size': trial.suggest_categorical('batch_size', [32, 64, 128]),
        'gamma': trial.suggest_uniform('gamma', 0.95, 0.999),
        'entropy_coef': trial.suggest_loguniform('entropy_coef', 1e-3, 1e-1),
    }

    performance = train(config)
    return performance  # 优化目标

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

print("Best config:", study.best_params)
```

**优点**：
- 样本效率高（智能选择）
- 自动平衡 exploration vs exploitation
- 可以提前停止（pruning）

**缺点**：
- 复杂度高
- 对噪声敏感（RL 性能方差大）
- 计算 GP 的开销

**适用**：
- 计算资源有限，需要高效
- 超参数空间大
- 任务稳定（方差不太大）

---

### 5.5 Population-Based Training (PBT)

**思想**：同时训练多个agent，动态调整超参数（进化算法）。

**流程**：

1. 初始化 N 个 agent，随机超参数
2. 定期评估所有 agent
3. 性能差的：
   - **Exploit**：复制性能好的 agent 的参数和超参数
   - **Explore**：随机扰动超参数
4. 继续训练
5. 重复 2-4

**优点**：
- 超参数随训练动态变化（如学习率衰减）
- 样本效率高（共享经验）
- 适合长期训练

**缺点**：
- 需要大量并行资源
- 实现复杂

**工具**：Ray Tune

**论文**：*Population Based Training of Neural Networks* (Jaderberg et al., 2017)

---

### 5.6 调优策略总结

| 方法 | 样本效率 | 计算开销 | 易用性 | 推荐场景 |
|------|---------|---------|--------|---------|
| Manual | 低 | 低 | 高 | 快速原型 |
| Grid Search | 低 | 高 | 高 | 1-2 个超参数 |
| Random Search | 中 | 中 | 高 | 3-5 个超参数，资源充足 |
| Bayesian Opt | 高 | 中-高 | 中 | 资源有限，需高效 |
| PBT | 高 | 很高 | 低 | 长期训练，大规模资源 |

**实践建议**：
1. **初期**：Manual（理解算法）
2. **中期**：Random Search（快速扫描）
3. **后期**：Bayesian Opt 或 PBT（精细调优）

---

## 6. 实践技巧与经验法则

### 6.1 快速验证技巧

**1. 简化环境**：

```python
# 原始任务：复杂迷宫
# 快速验证：小迷宫（3x3）

# 原始：MuJoCo Humanoid
# 快速：Reacher（简单控制）
```

几分钟内看到学习 → 超参数大概率OK → 再用完整任务。

---

**2. 短训练**：

```python
# 不要每次都跑到收敛
# 快速筛选：前 10-20% 训练

for config in configs:
    performance_early = train(config, max_steps=early_stop)
    if performance_early < threshold:
        skip  # 提前剪枝
    else:
        performance_full = train(config, max_steps=full_steps)
```

---

**3. 多种子平均**：

RL 方差大，单次运行可能误导。

```python
# 至少 3-5 个种子
performances = [train(config, seed=i) for i in range(5)]

mean_perf = np.mean(performances)
std_perf = np.std(performances)

# 比较时考虑不确定性
if mean_A - std_A > mean_B + std_B:
    print("A significantly better")
```

---

**4. 监控关键指标**：

不只看 episode reward！

```python
log("reward/episode", episode_reward)
log("loss/value", value_loss)
log("loss/policy", policy_loss)
log("entropy", entropy)
log("kl_divergence", kl)
log("grad_norm", grad_norm)
log("explained_variance", explained_var)  # Critic 质量
```

早期识别问题。

---

### 6.2 经验法则

**Learning Rate**：
- 起点：3e-4（几乎万能）
- On-policy（PPO）：3e-4，需要 decay
- Off-policy（DQN/SAC）：1e-4，固定

**Discount γ**：
- 默认：0.99
- 短任务（<10 步）：0.9 - 0.95
- 长任务（>100 步）：0.995 - 0.999

**Batch Size**：
- On-policy：horizon × num_envs
- Off-policy：越大越稳定（32-256）

**Network**：
- 起点：2 层 × 64 单元
- 复杂任务：3 层 × 256 单元
- 过大浪费，过小不够

**Exploration**：
- ε-greedy：从 1.0 衰减到 0.01-0.1
- Entropy：0.01（可选 decay）
- SAC：auto-tune α

---

### 6.3 算法选择经验

| 任务类型 | 推荐算法 | 关键超参数 |
|---------|---------|-----------|
| 离散动作，低维 | DQN, A2C | lr, γ, ε |
| 连续动作 | PPO, SAC | lr, γ, clip_range |
| 样本昂贵（真实机器人） | SAC, DDPG | replay size, τ |
| 样本便宜（模拟器） | PPO, A3C | lr, num_envs |
| 稀疏奖励 | PPO + Curiosity, DQN + HER | reward shaping |
| 需要稳定性（RLHF） | PPO | clip_range, lr_decay |
| Atari | DQN variants, PPO | ε_decay, frame_skip |
| MuJoCo | SAC, TD3 | α, batch_size |

---

### 6.4 常见陷阱

**陷阱 1：状态/奖励未归一化**

```python
# 错误
state = raw_observation  # 可能[-1000, 1000]

# 正确
state = (raw_observation - mean) / (std + 1e-8)
```

未归一化 → 不同尺度特征 → 难学习。

---

**陷阱 2：奖励缩放不当**

```python
# 如果奖励范围[-1000, 1000]
# Value network 输出会很大 → 数值不稳定

# 解决：Clip 或 normalize
reward = np.clip(reward, -10, 10)
# 或
reward = reward / reward_scale
```

---

**陷阱 3：忘记设置随机种子**

```python
# 每次运行结果不同 → 难以调试

# 正确
import random, np, torch
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
env.seed(seed)
```

---

**陷阱 4：过早判断"不work"**

RL 学习曲线常常：

```
Episode 0-1000:   没进展
Episode 1000-1500: 突然起飞
Episode 1500+:    稳定提升
```

耐心等待！特别是稀疏奖励任务。

---

**陷阱 5：只调一个超参数**

超参数有交互效应：

- 大 batch → 可能需要大 lr
- 长 horizon → 需要大 batch
- 大 γ → 可能需要小 lr（值范围大）

需要联合调优。

---

## 7. 调优工具与框架

### 7.1 Optuna

**安装**：
```bash
pip install optuna
```

**例子**：

```python
import optuna

def objective(trial):
    # 定义超参数空间
    lr = trial.suggest_loguniform('lr', 1e-5, 1e-3)
    batch_size = trial.suggest_categorical('batch_size', [32, 64, 128])
    gamma = trial.suggest_uniform('gamma', 0.95, 0.999)

    # 训练
    agent = create_agent(lr=lr, batch_size=batch_size, gamma=gamma)
    reward = train_and_evaluate(agent)

    return reward

# 优化
study = optuna.create_study(
    direction='maximize',
    pruner=optuna.pruners.MedianPruner()  # 提前停止差的试验
)

study.optimize(objective, n_trials=100, n_jobs=4)  # 并行

# 结果
print("Best params:", study.best_params)
print("Best value:", study.best_value)

# 可视化
optuna.visualization.plot_optimization_history(study)
optuna.visualization.plot_param_importances(study)
```

**特性**：
- Pruning（提前停止）
- 多目标优化
- 可视化
- 分布式支持

---

### 7.2 Ray Tune

**安装**：
```bash
pip install ray[tune]
```

**例子**：

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler

def train_rl(config):
    agent = create_agent(
        lr=config['lr'],
        batch_size=config['batch_size'],
        gamma=config['gamma']
    )

    for epoch in range(100):
        reward = train_one_epoch(agent)
        tune.report(mean_reward=reward)  # 报告中间结果

# 搜索空间
config = {
    'lr': tune.loguniform(1e-5, 1e-3),
    'batch_size': tune.choice([32, 64, 128]),
    'gamma': tune.uniform(0.95, 0.999)
}

# 调度器（提前停止差的试验）
scheduler = ASHAScheduler(
    metric='mean_reward',
    mode='max',
    max_t=100,
    grace_period=10
)

# 运行
analysis = tune.run(
    train_rl,
    config=config,
    num_samples=50,
    scheduler=scheduler,
    resources_per_trial={'cpu': 2, 'gpu': 0.25}
)

# 最佳配置
best_config = analysis.best_config
```

**特性**：
- 强大的调度器（ASHA, PBT, HyperBand）
- 分布式（跨机器）
- 与 RL 库集成（RLlib）

---

### 7.3 Weights & Biases (WandB) Sweeps

**安装**：
```bash
pip install wandb
```

**例子**：

```python
import wandb

# 定义 sweep 配置
sweep_config = {
    'method': 'bayes',  # or 'grid', 'random'
    'metric': {'name': 'reward', 'goal': 'maximize'},
    'parameters': {
        'lr': {'distribution': 'log_uniform', 'min': -5, 'max': -3},
        'batch_size': {'values': [32, 64, 128]},
        'gamma': {'distribution': 'uniform', 'min': 0.95, 'max': 0.999}
    }
}

# 创建 sweep
sweep_id = wandb.sweep(sweep_config, project='rl-tuning')

# 训练函数
def train():
    wandb.init()
    config = wandb.config

    agent = create_agent(lr=config.lr, batch_size=config.batch_size, gamma=config.gamma)

    for epoch in range(100):
        reward = train_one_epoch(agent)
        wandb.log({'reward': reward, 'epoch': epoch})

# 运行 sweep（可以并行多个 agent）
wandb.agent(sweep_id, function=train, count=50)
```

**特性**：
- 云端管理
- 实时可视化
- 团队协作
- 自动生成报告

---

### 7.4 Stable-Baselines3 + RL Baselines Zoo

**安装**：
```bash
pip install stable-baselines3
git clone https://github.com/DLR-RM/rl-baselines3-zoo
```

**使用**：

```bash
# 使用预调优的超参数
python train.py --algo ppo --env CartPole-v1

# 自动调优
python train.py --algo ppo --env CartPole-v1 --optimize --n-trials 100
```

**特性**：
- 预调优的超参数（大量环境）
- 一键调优
- Benchmark工具

**预调优配置库**：
https://github.com/DLR-RM/rl-baselines3-zoo/tree/master/hyperparams

```yaml
# hyperparams/ppo.yml
CartPole-v1:
  n_envs: 8
  n_timesteps: !!float 1e5
  policy: 'MlpPolicy'
  n_steps: 32
  batch_size: 256
  gae_lambda: 0.8
  gamma: 0.98
  n_epochs: 20
  ent_coef: 0.0
  learning_rate: lin_0.001
  clip_range: lin_0.2
```

---

## 8. 常见问题诊断

### 8.1 学习曲线诊断

**问题 1：完全不学习（平线）**

**可能原因**：
1. Learning rate 太小
2. Reward 太稀疏
3. 探索不足
4. Bug（梯度未更新等）

**诊断**：
```python
# 检查梯度
print(f"Grad norm: {grad_norm}")  # 应该 > 0

# 检查 reward
print(f"Non-zero rewards: {(rewards != 0).sum() / len(rewards)}")

# 检查探索
print(f"Action diversity: {len(set(actions)) / len(actions)}")
```

**解决**：
- 增大 lr（×10）
- 添加 reward shaping
- 增加探索（更大 ε or entropy）
- 检查代码

---

**问题 2：学习后崩溃（先升后降）**

**可能原因**：
1. Learning rate 太大（过拟合/发散）
2. Exploration 衰减太快（过早exploits）
3. Catastrophic forgetting（off-policy 数据失效）

**诊断**：
```python
# 检查 value loss
if value_loss > threshold:
    print("Value function exploding")

# 检查 policy change
if kl_divergence > threshold:
    print("Policy changing too fast")
```

**解决**：
- 减小 lr（÷2 or ÷10）
- 减慢 ε 衰减
- 增加 target network 更新频率
- 加 gradient clipping

---

**问题 3：高方差（剧烈震荡）**

**可能原因**：
1. Batch size 太小
2. 环境本身随机性大
3. Exploration 过强

**解决**：
- 增大 batch size
- 多种子平均
- 减小 ε or entropy
- 使用更稳定的算法（PPO > A2C）

---

**问题 4：plateaus（平台期，不再提升）**

**可能原因**：
1. Learning rate 太小（陷入局部最优）
2. Exploration 不足
3. Network capacity 不够
4. 确实接近最优

**解决**：
- 增大 lr（短期）
- 增加 exploration
- 更大 network
- 检查是否接近理论最优性能

---

### 8.2 快速诊断清单

```
□ Reward 有信号？（不是全0？）
□ Gradient 在更新？（norm > 0？）
□ Policy 在变化？（action分布变化？）
□ Value 稳定？（loss 不爆炸？）
□ Exploration 充分？（action diversity？）
□ 状态归一化了吗？
□ 奖励缩放合理吗？
□ 随机种子设置了吗？
□ 检查过简单环境吗？
```

---

## 9. 案例研究

### 9.1 案例：CartPole-v1（PPO）

**任务**：平衡杆子，目标 reward = 500。

**初始配置（默认）**：
```python
config = {
    'lr': 3e-4,
    'gamma': 0.99,
    'n_steps': 128,
    'batch_size': 64,
    'n_epochs': 10,
    'clip_range': 0.2,
    'ent_coef': 0.0
}
```

**结果**：3000 timesteps 达到 500

**调优 1：增大 learning rate**：
```python
config['lr'] = 1e-3
```
**结果**：1500 timesteps 达到 500（加速 2 倍！）

**调优 2：减小 GAE λ**（CartPole 短期任务）：
```python
config['gae_lambda'] = 0.8  # 默认 0.95
```
**结果**：1000 timesteps 达到 500

**最终配置**：
```python
{
    'lr': 1e-3,
    'gamma': 0.98,  # 短期任务
    'gae_lambda': 0.8,
    'n_epochs': 20,  # 更多 epoch（任务简单）
    'ent_coef': 0.0  # 确定性策略足够
}
```

**结果**：800 timesteps 达到 500（加速 3.75 倍）

**教训**：
- CartPole 简单 → 高 lr，低 γ，多 epoch
- 默认配置通常保守（适用复杂任务）
- 简单任务可以更激进

---

### 9.2 案例：Breakout（DQN）

**任务**：Atari Breakout。

**初始配置**：
```python
config = {
    'lr': 1e-4,
    'buffer_size': 1e6,
    'target_update_freq': 10000,
    'batch_size': 32,
    'epsilon_start': 1.0,
    'epsilon_end': 0.01,
    'epsilon_decay': 1e6
}
```

**结果**：10M frames，平均 score = 15（差）

**问题诊断**：
- Q 值爆炸（>1000）
- Loss 不稳定

**调优 1：Gradient clipping**：
```python
config['grad_clip'] = 10.0
```
**结果**：稳定了，但仍慢

**调优 2：增加 target update frequency**：
```python
config['target_update_freq'] = 1000  # 从 10000
```
**结果**：收敛更快，10M frames 达到 score = 50

**调优 3：使用 Double DQN + Dueling**：
```python
config['use_double_dqn'] = True
config['use_dueling'] = True
```
**结果**：10M frames 达到 score = 100

**调优 4：调整 ε decay**：
```python
config['epsilon_end'] = 0.05  # 保持更多探索
config['epsilon_decay'] = 2e6  # 更慢衰减
```
**结果**：10M frames 达到 score = 150

**教训**：
- Atari 需要稳定性技巧（clipping, target network）
- Double DQN + Dueling 几乎必需
- 探索很重要（不要过早 exploit）

---

### 9.3 案例：Humanoid（SAC）

**任务**：MuJoCo Humanoid 控制。

**初始配置（SAC 默认）**：
```python
config = {
    'lr': 3e-4,
    'batch_size': 256,
    'buffer_size': 1e6,
    'tau': 0.005,
    'alpha': 'auto',  # auto-tune
    'gamma': 0.99
}
```

**结果**：1M steps，reward = 2000（离最优 6000 还远）

**调优 1：增大 batch size**：
```python
config['batch_size'] = 512
```
**结果**：1M steps，reward = 3000

**调优 2：增加 update-to-data ratio**：
```python
config['gradient_steps'] = 1  # 每步环境交互，更新 1 次梯度
```
**结果**：1M steps，reward = 4000

**调优 3：调整 network size**：
```python
config['hidden_dims'] = [400, 300]  # DDPG 论文建议
```
**结果**：1M steps，reward = 5000

**调优 4：微调 α（虽然 auto）**：
```python
config['target_entropy'] = -dim(A)  # 默认
# 调整初始值
config['init_log_alpha'] = 0.0  # exp(0) = 1.0
```
**结果**：1M steps，reward = 5500

**教训**：
- 连续控制任务：大 batch, 更多 updates
- Network architecture 很重要（DDPG 的 400-300 是好起点）
- SAC auto-tuning α 通常够用

---

## 10. 面试常见问题

### Q1: RL 中哪些超参数最重要？如何调优它们？

**答案**：

**Top 3 最重要**：

**1. Learning Rate**：
- **作用**：控制参数更新步长
- **典型范围**：[1e-5, 1e-3]
- **调优**：对数搜索（1e-5, 3e-5, 1e-4, 3e-4, 1e-3）
- **诊断**：
  - 太大 → loss爆炸、不稳定
  - 太小 → 学习慢
- **建议**：从 3e-4 开始（通用默认值）

**2. Discount Factor γ**：
- **作用**：权衡短期 vs 长期奖励
- **典型值**：0.99（中期任务）
- **调优**：根据任务horizon
  - 短任务（<10步）：0.9-0.95
  - 长任务（>100步）：0.995-0.999
- **影响**：有效视野 H ≈ 1/(1-γ)

**3. Network Architecture**：
- **作用**：函数逼近能力
- **典型**：2-3层，64-256单元
- **调优**：从简单开始，逐步加深/加宽
- **诊断**：
  - 欠拟合 → 加大网络
  - 过拟合 → 减小网络或加正则

---

**算法特定重要参数**：

**DQN**：
- ε-greedy decay（探索）
- Target update频率（稳定性）
- Replay buffer size（样本多样性）

**PPO**：
- Clip range（更新幅度）
- GAE λ（偏差-方差）
- Entropy coefficient（探索）

**SAC**：
- Temperature α（auto-tune通常足够）
- Batch size（越大越稳定）

---

**调优策略**：

1. **单变量调优**（顺序）：
   - Learning rate（首先）
   - Network architecture
   - γ
   - 算法特定参数

2. **随机搜索**（3-5个参数同时）：
   - Log-uniform 采样 lr, entropy_coef
   - Uniform 采样 γ, λ
   - 50-100 trials

3. **贝叶斯优化**（资源有限时）：
   - Optuna, Ray Tune
   - 智能选择配置

---

### Q2: 如何诊断 RL 训练不稳定？

**答案**：

**不稳定的表现**：
1. Loss 爆炸
2. Reward 曲线剧烈震荡
3. 训练中途崩溃（先升后降）

---

**诊断步骤**：

**Step 1：检查梯度**

```python
grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float('inf'))
if grad_norm > 10:
    print("Warning: Large gradient norm")
```

**梯度过大** → Learning rate 太大 or 需要 clipping

---

**Step 2：检查 Value 函数**

```python
q_mean = Q_values.mean()
q_std = Q_values.std()

if q_mean > 1000 or q_std > 100:
    print("Warning: Value exploding")
```

**Value 爆炸** → Deadly Triad 问题（见 deadly_triad.md）
- 解决：target network, experience replay, gradient clipping

---

**Step 3：检查 Policy 变化**（Policy Gradient）

```python
kl = kl_divergence(old_policy, new_policy)
if kl > 0.05:  # 阈值
    print("Warning: Policy changing too fast")
```

**Policy 突变** → Learning rate 太大 or clip range 太大（PPO）
- 解决：减小 lr，减小 clip_range

---

**Step 4：检查数据分布**

```python
# Replay buffer 中奖励分布
rewards = [r for (s,a,r,s_) in buffer]
plt.hist(rewards, bins=50)
```

**高度不平衡** → 可能需要 reward normalization 或 prioritized replay

---

**常见原因与解决**：

| 症状 | 可能原因 | 解决方法 |
|------|---------|---------|
| Loss 爆炸 | lr太大 | 减小lr, 加gradient clipping |
| Q值爆炸 | Deadly Triad | Target network, replay, clipping |
| 剧烈震荡 | Batch太小, 高方差 | 增大batch, 多种子平均 |
| 先升后降 | 过拟合, lr太大 | Early stopping, 减小lr |
| 梯度消失 | lr太小, 网络太深 | 增大lr, 减少层数 |

---

**预防措施**：

1. **梯度裁剪**：
   ```python
   clip_grad_norm_(model.parameters(), max_norm=0.5)
   ```

2. **归一化**：
   ```python
   state = (state - mean) / (std + 1e-8)
   reward = reward / reward_scale
   ```

3. **监控关键指标**：
   - Gradient norm
   - Value mean/std
   - KL divergence
   - Explained variance

4. **稳定性技巧**：
   - Target network（DQN/SAC）
   - Clip range（PPO）
   - Entropy regularization

---

### Q3: Random Search vs Bayesian Optimization，如何选择？

**答案**：

**Random Search（随机搜索）**：

**原理**：
- 从预定义分布随机采样超参数
- 独立评估每个配置

**优点**：
- ✅ 简单易实现
- ✅ 容易并行（所有试验独立）
- ✅ 对噪声鲁棒（RL方差大）
- ✅ 高维也有效

**缺点**：
- ❌ 不利用历史信息（"盲目"搜索）
- ❌ 样本效率低（可能浪费很多试验）

**适用**：
- 计算资源充足（可以跑很多试验）
- 超参数空间3-5维
- 任务方差大（噪声掩盖优化信号）
- 快速原型（简单）

---

**Bayesian Optimization（贝叶斯优化）**：

**原理**：
- 用高斯过程（GP）建模"超参数 → 性能"
- 用 Acquisition Function 智能选择下一个配置
  - 平衡 exploration（不确定区域）vs exploitation（高性能区域）

**优点**：
- ✅ 样本效率高（智能选择）
- ✅ 需要更少试验
- ✅ 可以提前停止差的配置（pruning）

**缺点**：
- ❌ 复杂度高（GP计算开销）
- ❌ 对噪声敏感（RL方差大时可能失效）
- ❌ 高维（>10维）性能下降
- ❌ 并行化有限（需要历史信息）

**适用**：
- 计算资源有限（每次试验昂贵）
- 超参数空间≤5维
- 任务方差小（稳定环境）
- 需要快速找到好配置

---

**对比表**：

| 特性 | Random Search | Bayesian Opt |
|------|--------------|--------------|
| 样本效率 | 低 | 高 |
| 计算开销 | 低 | 中-高 |
| 并行能力 | 强（完全独立）| 弱（需要序列信息）|
| 噪声鲁棒性 | 强 | 弱 |
| 高维（>5） | 可行 | 困难 |
| 易用性 | 简单 | 中等 |

---

**实践建议**：

**阶段1：Random Search**
- 快速扫描超参数空间
- 识别大致范围
- 50-100 trials

**阶段2：Bayesian Opt**（可选）
- 在Random Search找到的好区域精细搜索
- 50 trials
- 使用Optuna或Ray Tune

---

**RL特殊考虑**：

RL任务方差大（同配置不同种子差异大）→ Random Search更鲁棒

**折中方案**：
- Random Search + Early stopping（Median pruning）
  ```python
  # Optuna example
  pruner = optuna.pruners.MedianPruner()  # 提前停止差的试验
  study = optuna.create_study(pruner=pruner)
  ```

这结合了Random Search的鲁棒性和Bayesian Opt的效率（通过pruning）。

---

**总结**：

- **资源充足** → Random Search（简单有效）
- **资源有限** → Bayesian Opt + Pruning
- **高方差RL任务** → Random Search + Early stopping
- **低方差RL任务** → Bayesian Opt

---

## 总结

**超参数调优的核心要点**：

1. **关键超参数**：Learning rate, γ, Network architecture（优先调这些）
2. **调优策略**：Manual → Random Search → Bayesian Opt（根据资源）
3. **诊断技巧**：监控 grad norm, value, KL, 多指标综合判断
4. **稳定性**：Gradient clipping, normalization, target network
5. **经验法则**：从默认值开始（3e-4, γ=0.99），简化环境快速验证，多种子平均

**实践流程**：

1. 建立 baseline（默认超参数）
2. 调 learning rate（对数搜索）
3. 调算法特定参数（ε, clip, λ等）
4. Random search 联合调优（3-5个参数）
5. 可选：Bayesian Opt 精细调优
6. 多种子验证，选最佳配置

**记住**：
> "In RL, hyperparameters can make a 10x difference. But patience and systematic tuning > luck."

希望这份指南能帮助你高效调优深度RL算法！
