# RL 训练 Tricks 总结：从入门到精通

## 目录
1. [数据预处理Tricks](#1-数据预处理tricks)
2. [网络架构Tricks](#2-网络架构tricks)
3. [训练稳定性Tricks](#3-训练稳定性tricks)
4. [探索策略Tricks](#4-探索策略tricks)
5. [样本效率Tricks](#5-样本效率tricks)
6. [收敛加速Tricks](#6-收敛加速tricks)
7. [算法特定Tricks](#7-算法特定tricks)
8. [工程实践Tricks](#8-工程实践tricks)
9. [调试与监控Tricks](#9-调试与监控tricks)
10. [进阶Tricks](#10-进阶tricks)

---

## 1. 数据预处理Tricks

### 1.1 状态归一化（State Normalization）⭐⭐⭐

**为什么重要**：
- 不同特征可能量纲不同（位置 [0, 100], 速度 [-10, 10]）
- 神经网络对输入尺度敏感
- 归一化加速收敛

**方法 1：Running Mean/Std**

```python
class RunningMeanStd:
    def __init__(self, epsilon=1e-4, shape=()):
        self.mean = np.zeros(shape, dtype=np.float64)
        self.var = np.ones(shape, dtype=np.float64)
        self.count = epsilon

    def update(self, x):
        batch_mean = np.mean(x, axis=0)
        batch_var = np.var(x, axis=0)
        batch_count = x.shape[0]

        delta = batch_mean - self.mean
        tot_count = self.count + batch_count

        new_mean = self.mean + delta * batch_count / tot_count
        m_a = self.var * self.count
        m_b = batch_var * batch_count
        M2 = m_a + m_b + np.square(delta) * self.count * batch_count / tot_count
        new_var = M2 / tot_count

        self.mean = new_mean
        self.var = new_var
        self.count = tot_count

    def normalize(self, x):
        return (x - self.mean) / np.sqrt(self.var + 1e-8)

# 使用
state_normalizer = RunningMeanStd(shape=(state_dim,))

# 训练中
state_normalizer.update(states)
normalized_state = state_normalizer.normalize(state)
```

**方法 2：MinMax Normalization**

```python
def normalize_minmax(x, min_val, max_val):
    return (x - min_val) / (max_val - min_val + 1e-8)

# 例如：Atari pixel [0, 255] → [0, 1]
normalized_frame = frame / 255.0
```

**方法 3：标准化到 [-1, 1]**

```python
def normalize_symmetric(x, mean, std):
    return (x - mean) / (std + 1e-8)
```

**何时使用**：
- MuJoCo, Gym 等连续控制：Running Mean/Std ✅
- Atari 图像：除以 255 ✅
- 已知范围的特征：MinMax ✅

---

### 1.2 奖励缩放（Reward Scaling/Clipping）⭐⭐⭐

**为什么重要**：
- 不同环境奖励范围差异大（Atari: 0-1000, MuJoCo: -100-100）
- 大奖励 → 大 Q 值 → 数值不稳定
- 统一尺度便于超参数通用

**方法 1：Reward Clipping**

```python
# Atari 常用
reward = np.sign(reward)  # 限制到 {-1, 0, 1}

# 或
reward = np.clip(reward, -1, 1)
```

**方法 2：Reward Scaling**

```python
# 除以常数
reward = reward / reward_scale  # reward_scale = 100

# 或自适应
reward_std = np.std(reward_history)
reward = reward / (reward_std + 1e-8)
```

**方法 3：Reward Normalization（Running）**

```python
class RewardNormalizer:
    def __init__(self, gamma=0.99):
        self.returns = 0
        self.mean = 0
        self.std = 1
        self.gamma = gamma

    def __call__(self, reward, done):
        self.returns = self.returns * self.gamma + reward

        # 更新统计量
        self.mean = 0.99 * self.mean + 0.01 * self.returns
        self.std = 0.99 * self.std + 0.01 * abs(self.returns - self.mean)

        if done:
            self.returns = 0

        return reward / (self.std + 1e-8)

# 使用
reward_normalizer = RewardNormalizer()
normalized_reward = reward_normalizer(reward, done)
```

**推荐**：
- Atari: Clip to [-1, 1] ✅
- MuJoCo: Running normalization ✅
- 自定义环境：根据范围选择

---

### 1.3 Frame Stacking（帧堆叠）⭐⭐

**为什么重要**（Atari等）：
- 单帧图像无法推断运动方向
- 堆叠多帧提供时序信息

**实现**：

```python
from collections import deque

class FrameStack:
    def __init__(self, env, k=4):
        self.env = env
        self.k = k
        self.frames = deque([], maxlen=k)

    def reset(self):
        obs = self.env.reset()
        for _ in range(self.k):
            self.frames.append(obs)
        return self._get_obs()

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        self.frames.append(obs)
        return self._get_obs(), reward, done, info

    def _get_obs(self):
        return np.stack(self.frames, axis=0)  # (k, H, W)

# 使用
env = FrameStack(gym.make('Breakout-v0'), k=4)
```

**常用**：k = 4（DQN Nature 论文）

---

### 1.4 Observation Preprocessing（观测预处理，Atari）⭐⭐

**步骤**：

```python
import cv2

def preprocess_atari(frame):
    # 1. 灰度化
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # 2. 缩放到 84x84
    resized = cv2.resize(gray, (84, 84), interpolation=cv2.INTER_AREA)

    # 3. 归一化到 [0, 1]
    normalized = resized / 255.0

    return normalized
```

**或使用 Gym wrapper**：

```python
from stable_baselines3.common.atari_wrappers import AtariWrapper

env = AtariWrapper(gym.make('BreakoutNoFrameskip-v4'))
```

---

## 2. 网络架构Tricks

### 2.1 Initialization（权重初始化）⭐⭐

**Orthogonal Initialization（PPO/A2C 常用）**：

```python
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.orthogonal_(m.weight, gain=np.sqrt(2))
        nn.init.constant_(m.bias, 0.0)

model.apply(init_weights)
```

**Xavier/He Initialization**：

```python
def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.xavier_uniform_(m.weight)  # Xavier
        # 或
        nn.init.kaiming_uniform_(m.weight, nonlinearity='relu')  # He
        nn.init.constant_(m.bias, 0.0)
```

**最后一层小初始化**：

```python
# Policy 输出层：小初始化 → 接近均匀策略
nn.init.orthogonal_(policy_head.weight, gain=0.01)

# Value 输出层：小初始化 → 接近 0
nn.init.orthogonal_(value_head.weight, gain=1.0)
```

---

### 2.2 Activation Functions（激活函数）⭐⭐

**ReLU（默认）**：
```python
nn.ReLU()
```
- 简单高效
- 可能有"死神经元"

**Tanh（策略网络输出）**：
```python
nn.Tanh()
```
- 输出有界 [-1, 1]
- 适合连续动作（配合缩放）

**ELU / SELU**：
```python
nn.ELU(alpha=1.0)
nn.SELU()
```
- 缓解梯度消失
- 负值也有梯度（vs ReLU）

**Swish / Mish**（近年流行）：
```python
class Swish(nn.Module):
    def forward(self, x):
        return x * torch.sigmoid(x)
```

**推荐**：
- 隐藏层：ReLU（简单有效）
- Policy 输出：Tanh（连续动作）
- 深网络：ELU/SELU

---

### 2.3 Network Architecture Patterns⭐⭐

**Dueling Architecture（DQN）**：

```python
class DuelingQNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super().__init__()

        # Shared feature extractor
        self.feature = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )

        # Value stream
        self.value = nn.Linear(hidden_dim, 1)

        # Advantage stream
        self.advantage = nn.Linear(hidden_dim, action_dim)

    def forward(self, state):
        features = self.feature(state)
        value = self.value(features)
        advantage = self.advantage(features)

        # Combine: Q = V + (A - mean(A))
        q_values = value + (advantage - advantage.mean(dim=-1, keepdim=True))
        return q_values
```

**Shared vs Separate Networks（Actor-Critic）**：

```python
# 方案 1：Separate（独立网络）
class SeparateActorCritic(nn.Module):
    def __init__(self):
        self.actor = MLP(...)  # 独立
        self.critic = MLP(...)  # 独立

# 方案 2：Shared（共享特征）
class SharedActorCritic(nn.Module):
    def __init__(self):
        self.shared = MLP(...)  # 共享
        self.actor_head = nn.Linear(...)
        self.critic_head = nn.Linear(...)

    def forward(self, state):
        features = self.shared(state)
        action_logits = self.actor_head(features)
        value = self.critic_head(features)
        return action_logits, value
```

**权衡**：
- Separate：灵活，不互相干扰，但参数多
- Shared：参数少，特征共享，但可能冲突

**推荐**：Shared（PPO常用），除非任务差异大

---

### 2.4 Normalization Layers⭐

**Layer Normalization**（有时帮助稳定性）：

```python
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim):
        super().__init__()
        layers = []

        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.LayerNorm(hidden_dim))  # LayerNorm
            layers.append(nn.ReLU())
            prev_dim = hidden_dim

        layers.append(nn.Linear(prev_dim, output_dim))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)
```

**注意**：
- Batch Norm 在 RL 中不推荐（数据非 i.i.d.）
- Layer Norm 可以试试（LSTM/Transformer 中常用）

---

## 3. 训练稳定性Tricks

### 3.1 Gradient Clipping⭐⭐⭐

**By Norm**（推荐）：

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
```

**By Value**：

```python
torch.nn.utils.clip_grad_value_(model.parameters(), clip_value=1.0)
```

**推荐值**：
- PPO: 0.5
- DQN: 1.0 或 10.0
- SAC: 通常不需要

---

### 3.2 Target Network⭐⭐⭐（DQN/SAC）

**Hard Update**（DQN）：

```python
if step % target_update_freq == 0:
    target_network.load_state_dict(q_network.state_dict())
```

**Soft Update**（DDPG/SAC/TD3）：

```python
# 每步软更新
tau = 0.005
for param, target_param in zip(q_network.parameters(), target_network.parameters()):
    target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)
```

**为什么有效**：
- 稳定 TD 目标
- 减少正反馈循环
- 核心稳定性技巧（见 deadly_triad.md）

---

### 3.3 Entropy Regularization⭐⭐（Policy Gradient）

**添加熵 bonus**：

```python
# PPO loss
policy_loss = -advantages * log_probs
entropy = -(probs * log_probs).sum(-1)

total_loss = policy_loss.mean() - entropy_coef * entropy.mean()
```

**效果**：
- 鼓励探索（策略保持随机性）
- 防止过早收敛到确定性策略
- 提高鲁棒性

**推荐值**：
- 离散动作：0.01
- 连续动作：0.001 - 0.01
- 或 auto-tuning（SAC）

---

### 3.4 Value Clipping（PPO）⭐⭐

**Clip Value Loss**：

```python
# 防止 value 突变
value_pred_clipped = value_old + torch.clamp(
    value_pred - value_old,
    -clip_range,
    clip_range
)

value_loss = torch.max(
    (value_pred - returns)**2,
    (value_pred_clipped - returns)**2
).mean()
```

**效果**：
- 限制 value 更新幅度
- 增强稳定性

---

### 3.5 Learning Rate Scheduling⭐⭐

**Linear Decay**（PPO 常用）：

```python
def linear_schedule(initial_lr, final_lr=0):
    def lr_schedule(progress):
        # progress: 0 → 1
        return initial_lr + progress * (final_lr - initial_lr)
    return lr_schedule

# 使用
lr_schedule = linear_schedule(3e-4, 0)

for epoch in range(num_epochs):
    progress = epoch / num_epochs
    current_lr = lr_schedule(progress)

    for param_group in optimizer.param_groups:
        param_group['lr'] = current_lr
```

**Cosine Annealing**：

```python
from torch.optim.lr_scheduler import CosineAnnealingLR

scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs)

for epoch in range(num_epochs):
    train(...)
    scheduler.step()
```

**何时使用**：
- PPO: Linear decay ✅
- DQN/SAC: 固定 lr 通常够用

---

## 4. 探索策略Tricks

### 4.1 ε-Greedy 改进（DQN）⭐⭐

**Linear Decay**：

```python
def epsilon_schedule(step, start=1.0, end=0.01, decay_steps=1e6):
    fraction = min(step / decay_steps, 1.0)
    return start + fraction * (end - start)

epsilon = epsilon_schedule(current_step)
```

**Exponential Decay**：

```python
epsilon = max(epsilon_end, epsilon_start * decay_rate ** step)
```

**推荐**：
- start = 1.0（完全探索）
- end = 0.01 - 0.1
- decay_steps = 1e6（Atari）或 1e4-1e5（简单任务）

---

### 4.2 Noisy Networks⭐

**思想**：给网络参数添加可学习的噪声（而非 action）。

```python
class NoisyLinear(nn.Module):
    def __init__(self, in_features, out_features, sigma_init=0.5):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features

        # Learnable parameters
        self.weight_mu = nn.Parameter(torch.FloatTensor(out_features, in_features))
        self.weight_sigma = nn.Parameter(torch.FloatTensor(out_features, in_features))
        self.bias_mu = nn.Parameter(torch.FloatTensor(out_features))
        self.bias_sigma = nn.Parameter(torch.FloatTensor(out_features))

        # Noise
        self.register_buffer('weight_epsilon', torch.FloatTensor(out_features, in_features))
        self.register_buffer('bias_epsilon', torch.FloatTensor(out_features))

        self.reset_parameters()
        self.reset_noise()

    def forward(self, x):
        if self.training:
            weight = self.weight_mu + self.weight_sigma * self.weight_epsilon
            bias = self.bias_mu + self.bias_sigma * self.bias_epsilon
        else:
            weight = self.weight_mu
            bias = self.bias_mu

        return F.linear(x, weight, bias)

    def reset_noise(self):
        self.weight_epsilon.normal_()
        self.bias_epsilon.normal_()
```

**优点**：
- 自动学习探索程度
- 参数空间探索（vs 动作空间）

**缺点**：
- 实现复杂
- 计算开销略大

**适用**：Rainbow DQN

---

### 4.3 Curiosity-driven Exploration⭐⭐

**ICM（Intrinsic Curiosity Module）**：

奖励 = 外部奖励 + β × 预测误差

```python
class ICM(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super().__init__()

        # Feature network
        self.feature = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU()
        )

        # Forward model: φ(s), a → φ(s')
        self.forward_model = nn.Sequential(
            nn.Linear(hidden_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

        # Inverse model: φ(s), φ(s') → a
        self.inverse_model = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim)
        )

    def forward(self, state, action, next_state):
        phi_state = self.feature(state)
        phi_next_state = self.feature(next_state)

        # Forward loss（预测误差 = 内在奖励）
        pred_next_state = self.forward_model(torch.cat([phi_state, action], dim=-1))
        forward_loss = F.mse_loss(pred_next_state, phi_next_state.detach())

        # Inverse loss（辅助训练）
        pred_action = self.inverse_model(torch.cat([phi_state, phi_next_state], dim=-1))
        inverse_loss = F.cross_entropy(pred_action, action)

        intrinsic_reward = forward_loss.detach()  # 预测误差作为内在奖励

        return intrinsic_reward, forward_loss, inverse_loss

# 使用
total_reward = external_reward + beta * intrinsic_reward
```

**适用**：稀疏奖励环境（如 Montezuma's Revenge）

---

## 5. 样本效率Tricks

### 5.1 Experience Replay⭐⭐⭐（Off-policy）

**基础版**：

```python
from collections import deque
import random

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(dones)

    def __len__(self):
        return len(self.buffer)

# 使用
buffer = ReplayBuffer(capacity=100000)

# 收集
buffer.push(state, action, reward, next_state, done)

# 训练
if len(buffer) > batch_size:
    batch = buffer.sample(batch_size)
    train(batch)
```

**优点**：
- 打破样本相关性
- 重用数据（样本效率高）

**缺点**：
- 只适用于 off-policy

---

### 5.2 Prioritized Experience Replay⭐⭐

**思想**：重要的样本（TD error 大）多采样。

```python
class PrioritizedReplayBuffer:
    def __init__(self, capacity, alpha=0.6, beta=0.4):
        self.capacity = capacity
        self.alpha = alpha  # 优先级指数
        self.beta = beta    # 重要性采样指数
        self.buffer = []
        self.priorities = np.zeros(capacity, dtype=np.float32)
        self.pos = 0

    def push(self, transition):
        max_priority = self.priorities.max() if self.buffer else 1.0

        if len(self.buffer) < self.capacity:
            self.buffer.append(transition)
        else:
            self.buffer[self.pos] = transition

        self.priorities[self.pos] = max_priority
        self.pos = (self.pos + 1) % self.capacity

    def sample(self, batch_size):
        if len(self.buffer) == self.capacity:
            priorities = self.priorities
        else:
            priorities = self.priorities[:len(self.buffer)]

        # 根据优先级采样
        probabilities = priorities ** self.alpha
        probabilities /= probabilities.sum()

        indices = np.random.choice(len(self.buffer), batch_size, p=probabilities)
        samples = [self.buffer[idx] for idx in indices]

        # 重要性采样权重
        total = len(self.buffer)
        weights = (total * probabilities[indices]) ** (-self.beta)
        weights /= weights.max()

        return samples, indices, weights

    def update_priorities(self, indices, priorities):
        for idx, priority in zip(indices, priorities):
            self.priorities[idx] = priority

# 使用
buffer = PrioritizedReplayBuffer(capacity=100000)

# 训练时
samples, indices, weights = buffer.sample(batch_size)
td_errors = compute_td_errors(samples)

# 更新优先级
buffer.update_priorities(indices, td_errors)
```

**效果**：加速学习 2-3 倍（Rainbow DQN）

参见 `exercises/ch14_advanced/ex10_prioritized_replay.py`

---

### 5.3 n-step Returns⭐⭐

**思想**：结合多步奖励（介于 TD 和 MC 之间）。

```python
def compute_n_step_returns(rewards, values, dones, gamma=0.99, n=3):
    """
    rewards: [T]
    values: [T+1]  # 包含 V(s_{T+1})
    dones: [T]
    """
    returns = np.zeros_like(rewards)

    for t in range(len(rewards)):
        n_step_return = 0
        for k in range(n):
            if t + k >= len(rewards):
                break
            if dones[t + k]:
                n_step_return += (gamma ** k) * rewards[t + k]
                break
            else:
                n_step_return += (gamma ** k) * rewards[t + k]

        # Bootstrap
        if t + n < len(rewards) and not dones[t + n - 1]:
            n_step_return += (gamma ** n) * values[t + n]

        returns[t] = n_step_return

    return returns

# 使用
n_step_returns = compute_n_step_returns(rewards, values, dones, n=5)
```

**推荐值**：n = 3 - 5

**适用**：DQN, PPO（结合 GAE）

---

### 5.4 Hindsight Experience Replay (HER)⭐

**思想**：失败的轨迹也有价值（假装另一个目标成功了）。

```python
# 原始轨迹：目标 g，失败
trajectory = [(s0, a0, r=0, s1), (s1, a1, r=0, s2), ...]

# HER：假装最后到达的状态 sT 就是目标
for (s, a, r, s_next) in trajectory:
    # 原始目标
    buffer.push(s, a, r, s_next, goal=g)

    # Hindsight 目标（假装 sT 是目标）
    r_new = 1 if s_next == sT else 0
    buffer.push(s, a, r_new, s_next, goal=sT)
```

**效果**：
- 将失败轨迹转化为成功轨迹（对于另一个目标）
- 样本效率提升 10 倍+

**适用**：稀疏奖励 + 多目标环境

---

## 6. 收敛加速Tricks

### 6.1 Parallel Environments⭐⭐⭐

**Vectorized Env**（并行采样）：

```python
from stable_baselines3.common.vec_env import SubprocVecEnv

def make_env(env_id, seed):
    def _init():
        env = gym.make(env_id)
        env.seed(seed)
        return env
    return _init

num_envs = 8
env = SubprocVecEnv([make_env('CartPole-v1', i) for i in range(num_envs)])

# 并行 step
states = env.reset()  # (num_envs, state_dim)
next_states, rewards, dones, infos = env.step(actions)  # (num_envs, ...)
```

**效果**：
- 加速数据收集 N 倍（N = num_envs）
- 增加样本多样性

**适用**：A2C, PPO（on-policy 算法受益最大）

---

### 6.2 Learning from Demonstrations⭐⭐

**Pre-training with BC**（行为克隆）：

```python
# 1. 收集专家演示
expert_demos = collect_expert_data()

# 2. 用监督学习预训练
for state, action in expert_demos:
    loss = F.cross_entropy(policy(state), action)
    loss.backward()
    optimizer.step()

# 3. RL 微调
for episode in range(num_episodes):
    rl_train(...)
```

**效果**：
- 快速学会基本策略
- 减少探索时间

**适用**：复杂任务（机器人操作等）

---

### 6.3 Curriculum Learning⭐⭐

**思想**：从简单到难逐步学习。

**例子 1：难度递增**

```python
# 阶段 1：简单迷宫（3x3）
env = SimpleMaze(size=3)
train(env, steps=10000)

# 阶段 2：中等迷宫（5x5）
env = SimpleMaze(size=5)
train(env, steps=20000)

# 阶段 3：复杂迷宫（10x10）
env = SimpleMaze(size=10)
train(env, steps=50000)
```

**例子 2：自适应难度**

```python
# 根据性能调整难度
if avg_reward > threshold_easy:
    env.set_difficulty('medium')
elif avg_reward > threshold_medium:
    env.set_difficulty('hard')
```

**效果**：
- 避免陷入局部最优
- 加速收敛

---

### 6.4 Transfer Learning / Fine-tuning⭐

**思想**：从相关任务迁移知识。

```python
# 1. 在任务 A 上训练
model = train_on_task_a()

# 2. 保存参数
torch.save(model.state_dict(), 'model_task_a.pth')

# 3. 加载到任务 B（可能冻结部分层）
model_b = Model()
model_b.load_state_dict(torch.load('model_task_a.pth'))

# 可选：冻结特征层
for param in model_b.feature_extractor.parameters():
    param.requires_grad = False

# 4. 微调
train_on_task_b(model_b)
```

**适用**：
- 任务相似（如不同 Atari 游戏）
- 有预训练模型可用

---

## 7. 算法特定Tricks

### 7.1 DQN Tricks

**Double DQN**⭐⭐⭐：

```python
# 选择动作（主网络）
action = q_network(next_state).argmax()

# 评估价值（目标网络）
target = reward + gamma * target_network(next_state)[action]
```

**效果**：减少 Q 值高估

---

**Dueling DQN**⭐⭐⭐：

分离 V(s) 和 A(s,a)（见 2.3 网络架构）

**效果**：更快学习，泛化更好

---

**Frame Skip**⭐（Atari）：

```python
# 每 k 帧执行一次动作，其他帧重复
class FrameSkipEnv:
    def __init__(self, env, skip=4):
        self.env = env
        self.skip = skip

    def step(self, action):
        total_reward = 0
        for _ in range(self.skip):
            obs, reward, done, info = self.env.step(action)
            total_reward += reward
            if done:
                break
        return obs, total_reward, done, info
```

**效果**：
- 加速训练（减少决策次数）
- 更符合人类玩游戏（不是每帧都反应）

---

### 7.2 PPO Tricks

**GAE（Generalized Advantage Estimation）**⭐⭐⭐：

```python
def compute_gae(rewards, values, next_values, dones, gamma=0.99, lambda_=0.95):
    advantages = np.zeros_like(rewards)
    last_advantage = 0

    for t in reversed(range(len(rewards))):
        if dones[t]:
            delta = rewards[t] - values[t]
            last_advantage = delta
        else:
            delta = rewards[t] + gamma * next_values[t] - values[t]
            last_advantage = delta + gamma * lambda_ * last_advantage

        advantages[t] = last_advantage

    returns = advantages + values
    return advantages, returns
```

参见 `docs/math_theory/gae.md`

---

**Value Function Clipping**⭐：

见 3.4 稳定性 Tricks

---

**Early Stopping（KL Divergence）**⭐：

```python
for epoch in range(num_epochs):
    # 训练一个 epoch
    kl = compute_kl_divergence(old_policy, new_policy)

    if kl > target_kl:  # 例如 0.015
        print(f"Early stopping at epoch {epoch}, KL = {kl}")
        break
```

**效果**：防止策略变化太大

---

### 7.3 SAC Tricks

**Automatic Entropy Tuning**⭐⭐⭐：

```python
# 学习温度参数 α
log_alpha = torch.tensor(0.0, requires_grad=True)
alpha_optimizer = Adam([log_alpha], lr=3e-4)

# 目标熵（启发式）
target_entropy = -torch.prod(torch.Tensor(action_space.shape)).item()

# 更新
alpha_loss = -(log_alpha.exp() * (log_probs + target_entropy).detach()).mean()
alpha_optimizer.zero_grad()
alpha_loss.backward()
alpha_optimizer.step()

alpha = log_alpha.exp()
```

**效果**：自动调节探索 vs 利用

---

**Twin Q-Networks（减少高估）**⭐⭐：

```python
# 两个独立的 Q 网络
q1_value = q1_network(state, action)
q2_value = q2_network(state, action)

# 取最小值（保守估计）
min_q = torch.min(q1_value, q2_value)

# Target
target = reward + gamma * min_q_next
```

**效果**：减少 Q 值高估（类似 Double DQN）

---

## 8. 工程实践Tricks

### 8.1 Mixed Precision Training⭐

**使用 FP16 加速**：

```python
from torch.cuda.amp import autocast, GradScaler

model = model.cuda()
optimizer = Adam(model.parameters(), lr=3e-4)
scaler = GradScaler()

for batch in data_loader:
    optimizer.zero_grad()

    # Forward in FP16
    with autocast():
        loss = compute_loss(batch)

    # Backward with scaling
    scaler.scale(loss).backward()

    # Update with unscaling
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)

    scaler.step(optimizer)
    scaler.update()
```

**效果**：
- 加速 2-3 倍（GPU）
- 减少显存占用

---

### 8.2 Checkpointing & Early Stopping⭐⭐

**定期保存**：

```python
if episode % save_freq == 0:
    checkpoint = {
        'episode': episode,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'rewards': episode_rewards,
    }
    torch.save(checkpoint, f'checkpoint_ep{episode}.pth')
```

**Early stopping**：

```python
best_reward = -float('inf')
patience = 10
patience_counter = 0

for episode in range(num_episodes):
    reward = train_episode()

    if reward > best_reward:
        best_reward = reward
        patience_counter = 0
        save_checkpoint('best_model.pth')
    else:
        patience_counter += 1

    if patience_counter >= patience:
        print("Early stopping!")
        break
```

---

### 8.3 Logging & Visualization⭐⭐⭐

**Weights & Biases**：

```python
import wandb

wandb.init(project='rl-project', config=config)

for episode in range(num_episodes):
    reward = train_episode()

    wandb.log({
        'reward': reward,
        'loss': loss,
        'q_mean': q_values.mean(),
        'entropy': entropy
    })
```

**TensorBoard**：

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment')

writer.add_scalar('Reward/train', reward, episode)
writer.add_histogram('Q_values', q_values, episode)
```

---

### 8.4 Hyperparameter Management⭐

**使用配置文件**：

```yaml
# config.yaml
agent:
  lr: 3e-4
  gamma: 0.99
  batch_size: 64

training:
  num_episodes: 1000
  save_freq: 100

env:
  name: 'CartPole-v1'
  normalize: true
```

```python
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

agent = Agent(lr=config['agent']['lr'], ...)
```

**优点**：
- 易于管理和版本控制
- 清晰记录实验配置

---

## 9. 调试与监控Tricks

### 9.1 Sanity Checks⭐⭐⭐

**过拟合测试**：

```python
# 固定小数据集
small_dataset = create_fixed_dataset(size=10)

# 训练直到过拟合
for _ in range(1000):
    loss = train_on(small_dataset)

# 应该能过拟合到 loss < 0.01
assert loss < 0.01, "Cannot overfit small dataset!"
```

**Random policy baseline**：

```python
random_reward = test_random_policy(env)
print(f"Random baseline: {random_reward}")

# 训练后的 agent 应该 > random
assert agent_reward > random_reward
```

---

### 9.2 监控关键指标⭐⭐⭐

**必看指标**：

```python
# 1. Episode reward（性能）
log('reward/episode', episode_reward)

# 2. Loss（学习）
log('loss/value', value_loss)
log('loss/policy', policy_loss)

# 3. Gradient norm（稳定性）
grad_norm = get_grad_norm(model)
log('grad_norm', grad_norm)

# 4. Explained variance（Critic质量）
explained_var = 1 - (returns - values).var() / returns.var()
log('explained_variance', explained_var)

# 5. Entropy（探索）
log('entropy', entropy)

# 6. KL divergence（策略变化，PPO）
log('kl', kl_divergence)

# 7. Q values（DQN）
log('q_mean', q_values.mean())
log('q_std', q_values.std())
```

---

### 9.3 Debugging Mode⭐

```python
class Agent:
    def __init__(self, debug=False):
        self.debug = debug

    def train(self, batch):
        if self.debug:
            print(f"Batch size: {len(batch)}")
            print(f"State range: [{states.min()}, {states.max()}]")
            print(f"Reward range: [{rewards.min()}, {rewards.max()}]")

        loss = self.compute_loss(batch)

        if self.debug:
            print(f"Loss: {loss.item()}")

            for name, param in self.model.named_parameters():
                if param.grad is not None:
                    print(f"{name}: grad_norm = {param.grad.norm().item()}")

        self.optimizer.step()

# 使用
agent = Agent(debug=True)  # 开发时
agent = Agent(debug=False)  # 生产时
```

---

## 10. 进阶Tricks

### 10.1 Population-Based Training (PBT)⭐

**思想**：多个 agent 并行训练，动态调整超参数（进化）。

**流程**：
1. 初始化 N 个 agent，随机超参数
2. 定期评估所有 agent
3. 差的 agent：
   - Exploit：复制好 agent 的参数和超参数
   - Explore：扰动超参数
4. 继续训练

**工具**：Ray Tune

**适用**：长期训练，大规模资源

---

### 10.2 Self-Play⭐⭐

**思想**：Agent 与自己的历史版本对战（多Agent游戏）。

```python
# 保存历史策略
historical_policies = []

for iteration in range(num_iterations):
    # 训练当前策略
    for episode in range(episodes_per_iteration):
        # 选择对手（历史策略）
        opponent = random.choice(historical_policies + [current_policy])

        # Self-play
        play_game(current_policy, opponent)

    # 保存当前策略
    historical_policies.append(copy.deepcopy(current_policy))
```

**例子**：AlphaGo, OpenAI Five

---

### 10.3 Distributional RL⭐

**思想**：学习回报的分布（而非期望）。

**C51（Categorical DQN）**：

离散化回报分布为 51 个 atoms。

```python
class C51Network(nn.Module):
    def __init__(self, state_dim, action_dim, num_atoms=51, v_min=-10, v_max=10):
        super().__init__()
        self.action_dim = action_dim
        self.num_atoms = num_atoms
        self.v_min = v_min
        self.v_max = v_max
        self.delta_z = (v_max - v_min) / (num_atoms - 1)
        self.z = torch.linspace(v_min, v_max, num_atoms)

        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim * num_atoms)
        )

    def forward(self, state):
        logits = self.network(state).view(-1, self.action_dim, self.num_atoms)
        probs = F.softmax(logits, dim=-1)  # (batch, actions, atoms)
        return probs

    def get_q_values(self, state):
        probs = self.forward(state)
        q_values = (probs * self.z).sum(dim=-1)  # 期望
        return q_values
```

**效果**：
- 更准确的价值估计
- 更好的性能（Rainbow DQN 组件）

**复杂度**：实现较复杂

---

### 10.4 Model-Based RL⭐

**思想**：学习环境模型，用于规划或数据增强。

**Dyna-Q（简单版）**：

```python
# 学习模型：(s, a) → (r, s')
model = {}

for episode in range(num_episodes):
    # 真实交互
    next_state, reward, done = env.step(action)

    # 更新模型
    model[(state, action)] = (reward, next_state)

    # 使用真实经验训练
    q_learning_update(state, action, reward, next_state)

    # Planning：使用模型生成虚拟经验
    for _ in range(planning_steps):
        s = random_state()
        a = random_action()
        if (s, a) in model:
            r, s_next = model[(s, a)]
            q_learning_update(s, a, r, s_next)  # 用虚拟经验训练
```

**复杂版**：
- World Models（学习 latent dynamics）
- MBPO（Model-Based Policy Optimization）

**适用**：样本昂贵的任务

---

## 总结

**最重要的 Tricks（⭐⭐⭐）**：

1. **数据预处理**：
   - State normalization（Running Mean/Std）
   - Reward clipping/scaling

2. **网络**：
   - Proper initialization（Orthogonal）
   - Dueling architecture（DQN）

3. **稳定性**：
   - Gradient clipping
   - Target network（DQN/SAC）
   - Entropy regularization（PPO）

4. **探索**：
   - ε-greedy decay（DQN）
   - Entropy bonus（PPO）

5. **样本效率**：
   - Experience replay（DQN）
   - Parallel environments（PPO/A2C）

6. **监控**：
   - 全面 logging（WandB/TensorBoard）
   - Sanity checks

**实践建议**：

1. **从简单开始**：先用默认配置，确保基本可用
2. **逐步添加**：一次添加一个 trick，验证效果
3. **不要盲目堆叠**：并非所有 tricks 都适用所有任务
4. **监控效果**：A/B 测试，量化收益
5. **记录一切**：配置、性能、trick 组合

**Tricks 优先级**：

| 优先级 | Tricks |
|--------|--------|
| 必须 | State norm, Gradient clip, Logging |
| 强烈推荐 | Target network（off-policy）, Entropy（on-policy）, Replay buffer（off-policy）|
| 推荐 | GAE（PPO）, Double DQN, Parallel envs |
| 可选 | Noisy nets, ICM, PER, HER |
| 进阶 | PBT, Distributional RL, Model-based |

**记住**：
> "Simple tricks well executed > complex tricks poorly understood."

希望这份 Tricks 总结能帮助你高效训练 RL 算法！
