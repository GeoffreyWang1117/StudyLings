# RL Debug 完整指南：常见问题诊断与解决

## 目录
1. [引言：RL 调试为什么困难？](#1-引言rl-调试为什么困难)
2. [系统化调试流程](#2-系统化调试流程)
3. [常见症状诊断](#3-常见症状诊断)
4. [组件级调试](#4-组件级调试)
5. [可视化与监控](#5-可视化与监控)
6. [单元测试与验证](#6-单元测试与验证)
7. [性能剖析](#7-性能剖析)
8. [复现性保证](#8-复现性保证)
9. [调试工具箱](#9-调试工具箱)
10. [面试常见问题](#10-面试常见问题)

---

## 1. 引言：RL 调试为什么困难？

### 1.1 监督学习 vs RL 调试

| 特性 | 监督学习 | 强化学习 |
|------|---------|---------|
| 反馈 | 即时loss | 延迟reward |
| 数据分布 | 固定 i.i.d. | 动态（策略改变）|
| 错误可见性 | 明显（loss上升）| 隐蔽（可能局部最优）|
| Bug影响 | 训练失败 | 可能仍能学，但次优 |
| 调试时间 | 分钟-小时 | 小时-天 |

**RL 特有挑战**：

1. **延迟反馈**：
   - Bug 可能在数千步后才体现
   - 难以定位根本原因

2. **非稳态性**：
   - 数据分布变化 → 难以重现
   - "working yesterday, broken today"

3. **高方差**：
   - 随机性大 → 难以区分 bug vs 运气

4. **多组件交互**：
   - Environment + Agent + Algorithm
   - Bug 可能在任何组件

5. **没有"ground truth"**：
   - 不知道最优性能是多少
   - 难以判断"够好"了没有

---

### 1.2 常见 RL Bug 类别

**实现 Bug（30%）**：
- 代码逻辑错误
- 数学公式写错
- 状态/动作索引错误

**概念 Bug（20%）**：
- 理解算法错误
- 参数意义混淆

**环境 Bug（15%）**：
- 环境实现错误
- Reward 设计问题

**数值 Bug（15%）**：
- 梯度爆炸/消失
- 数值不稳定

**超参数 Bug（10%）**：
- Learning rate 不合适
- Network 太小/大

**复现性 Bug（10%）**：
- 随机种子未设置
- 非确定性操作

---

### 1.3 调试的黄金法则

**规则 1：从简单开始**
```
简单环境 → 复杂环境
小网络 → 大网络
已知算法 → 新算法
```

**规则 2：隔离组件测试**
```
单独测试 Environment
单独测试 Network
单独测试 Loss计算
```

**规则 3：可视化一切**
```
Reward curve
Q values
Policy distribution
Gradient norms
```

**规则 4：对比已知基准**
```
复现论文结果
使用标准实现（Stable-Baselines3）
对比性能
```

**规则 5：使用断言和检查**
```python
assert reward.shape == (batch_size,)
assert 0 <= prob <= 1
assert not torch.isnan(loss)
```

---

## 2. 系统化调试流程

### 2.1 调试检查清单（Debugging Checklist）

**阶段 0：准备**
```
□ 设置随机种子（reproducibility）
□ 简化环境（CartPole 而非 Humanoid）
□ 记录所有超参数
□ 版本控制（git commit）
```

**阶段 1：Sanity Checks（基础检查）**
```
□ Environment 能手动玩？
□ Random policy 能得到非零 reward？
□ Network forward pass 正常？
□ Loss 计算不是 NaN/Inf？
□ Gradient 存在且非零？
```

**阶段 2：组件测试**
```
□ Environment reset/step 正确？
□ Reward function 符合预期？
□ State preprocessing 正确？
□ Network 输出范围正确？
□ Optimizer 在更新参数？
```

**阶段 3：算法验证**
```
□ 能过拟合小数据集？（过拟合测试）
□ 能在简单任务上学习？（CartPole）
□ 能复现论文结果？（已知环境）
□ 性能合理？（接近已知基准）
```

**阶段 4：性能调优**
```
□ Learning curve 正常？
□ 探索充分？
□ Value估计合理？
□ Policy改进单调？（PPO等）
```

---

### 2.2 二分查找调试法

**思想**：逐步缩小 bug 范围。

**Step 1：确认问题存在**
```python
# 运行完整训练
result = train(env, agent, steps=100000)
if result < expected:
    print("Problem confirmed")
```

**Step 2：二分：哪一半有问题？**
```python
# 测试前半段
result_early = train(env, agent, steps=50000)

if result_early < expected_early:
    # Bug在前半段（初始化/早期训练）
    investigate_initialization()
else:
    # Bug在后半段（后期训练/收敛）
    investigate_convergence()
```

**Step 3：继续二分直到定位**

**例子**：

```
训练10000步，reward不增长
→ 测试5000步：不增长
  → 测试2500步：不增长
    → 测试1000步：不增长
      → 测试100步：不增长
        → 测试10步：发现gradient是0
          → 找到bug：loss没有反向传播！
```

---

## 3. 常见症状诊断

### 3.1 症状：完全不学习（平线）

**Reward curve**：
```
Episode:  0  50  100 150 200 250
Reward:   5   5   5   5   5   5
```

**可能原因**：

**1. Gradient 未更新**

```python
# 检查
for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"{name}: grad_norm = {param.grad.norm()}")
    else:
        print(f"{name}: NO GRADIENT!")
```

**常见错误**：
```python
# 错误：忘记 backward
loss = compute_loss(...)
# loss.backward()  # 忘了！
optimizer.step()

# 错误：detach了不该detach的
target = reward + gamma * value.detach()  # ✅ 目标detach正确
loss = (value.detach() - target)^2  # ❌ value也detach了，无梯度！
```

---

**2. Learning Rate 太小**

```python
# 检查
print(f"Learning rate: {optimizer.param_groups[0]['lr']}")

# 如果 lr < 1e-6，可能太小
# 尝试 lr = 1e-3 看是否有改善
```

---

**3. Reward 全是 0（太稀疏）**

```python
# 检查
print(f"Non-zero rewards: {(rewards != 0).sum() / len(rewards)}")

# 如果 > 95% 是 0 → 太稀疏
# 解决：reward shaping, curriculum learning
```

---

**4. 探索不足**

```python
# 检查 action diversity
unique_actions = len(set(actions))
total_actions = len(actions)
print(f"Action diversity: {unique_actions / total_actions}")

# 如果 < 0.1（只用10%的动作）→ 探索不足
# 解决：增大 ε, entropy bonus
```

---

**5. Network 初始化错误**

```python
# 检查 network 输出
with torch.no_grad():
    for i in range(10):
        state = env.reset()
        q_values = model(state)
        print(f"Q values: {q_values}")

# 如果全是同一个值 → 初始化可能有问题
# 或者范围异常（如全是1e6）
```

---

### 3.2 症状：学习后崩溃（先升后降）

**Reward curve**：
```
Episode:  0   50  100 150 200 250
Reward:   10  50  80  90  40  10
```

**可能原因**：

**1. Learning Rate 太大**

```python
# 诊断：检查 loss
if max(losses[-100:]) > 10 * min(losses[-100:]):
    print("Loss unstable, lr might be too large")

# 解决
optimizer = Adam(model.parameters(), lr=lr/10)
```

---

**2. Gradient 爆炸**

```python
# 诊断
grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float('inf'))
print(f"Grad norm: {grad_norm}")

if grad_norm > 100:
    print("Gradient exploding!")

# 解决
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
```

---

**3. Q 值/Value 爆炸**

```python
# 诊断
q_values = model(states)
if q_values.abs().max() > 1000:
    print("Q values exploding!")

# 原因：Deadly Triad（见 deadly_triad.md）
# 解决：target network, double DQN, clip
```

---

**4. Catastrophic Forgetting（灾难性遗忘）**

**现象**：学会任务 A，开始学任务 B，忘记任务 A

**解决**：
- Experience replay（重放旧数据）
- Elastic Weight Consolidation（保护重要权重）
- Multi-task learning

---

**5. Exploration decay 太快**

```python
# DQN: ε 过早降到 0
# 解决：延长 ε_decay
epsilon_decay_steps = 1e6  # 从 1e5 增加

# PPO: entropy 过早降到 0
# 解决：增大 entropy_coef
entropy_coef = 0.01  # 从 0 增加
```

---

### 3.3 症状：高方差（剧烈震荡）

**Reward curve**：
```
Episode:  0   50  100 150 200 250
Reward:   10  80  20  70  30  60
```

**可能原因**：

**1. Batch Size 太小**

```python
# 当前 batch_size = 16 → 高方差
# 增大到 64 或 128
```

**2. 环境本身随机性大**

```python
# 解决：多 episode 平均
avg_reward = np.mean(episode_rewards[-100:])  # 滑动平均
```

**3. Exploration 太强**

```python
# ε-greedy: ε_final太大
epsilon_final = 0.01  # 从 0.1 减小

# Entropy: 系数太大
entropy_coef = 0.001  # 从 0.01 减小
```

---

### 3.4 症状：Plateaus（卡在局部最优）

**Reward curve**：
```
Episode:  0   100  200  300  400  500
Reward:   10  40   50   50   50   50
```

**可能原因**：

**1. 探索不足**

```python
# 卡在局部最优，无法发现更好策略

# 解决
# 增加探索：ε-greedy, entropy bonus, curiosity
# 或 Curriculum learning（先简单任务，再难任务）
```

**2. Network Capacity 不够**

```python
# 网络太小，无法表示复杂策略

# 诊断：增大网络
model = MLP(input_dim, [256, 256], output_dim)  # 从 [64, 64]

# 如果性能提升 → capacity 是瓶颈
```

**3. Learning Rate 太小（后期）**

```python
# 后期 lr 衰减太小，更新幅度不足跳出局部最优

# 解决：调整 lr schedule 或短期增大 lr
```

**4. 确实接近最优**

```python
# 检查：环境的理论最优是多少？
# 如果接近，可能已经够好了
```

---

## 4. 组件级调试

### 4.1 Environment 调试

**测试 1：手动测试**

```python
env = gym.make('CartPole-v1')

# 手动玩几步
state = env.reset()
env.render()

for _ in range(100):
    action = env.action_space.sample()  # 或手动选择
    next_state, reward, done, info = env.step(action)
    env.render()

    print(f"State: {next_state}, Reward: {reward}, Done: {done}")

    if done:
        state = env.reset()
```

**检查**：
- 状态范围合理？
- Reward 符合预期？
- Done 条件正确？
- Render 显示正常？

---

**测试 2：Random Policy Baseline**

```python
def random_policy_test(env, episodes=100):
    rewards = []
    for _ in range(episodes):
        state = env.reset()
        episode_reward = 0
        done = False

        while not done:
            action = env.action_space.sample()
            state, reward, done, _ = env.step(action)
            episode_reward += reward

        rewards.append(episode_reward)

    print(f"Random policy avg reward: {np.mean(rewards)}")
    return np.mean(rewards)

random_baseline = random_policy_test(env)

# 如果 random_baseline > 0，环境至少可用
# 如果 random_baseline = 0，可能环境有问题
```

---

**测试 3：Reward 分布**

```python
rewards = []
for _ in range(1000):
    env.reset()
    _, r, done, _ = env.step(env.action_space.sample())
    rewards.append(r)

plt.hist(rewards, bins=50)
plt.title("Reward Distribution")
plt.show()

print(f"Reward range: [{min(rewards)}, {max(rewards)}]")
print(f"Non-zero: {(np.array(rewards) != 0).mean()}")
```

---

### 4.2 Network 调试

**测试 1：Forward Pass**

```python
model = QNetwork(state_dim, action_dim)

# 测试单个样本
state = torch.randn(state_dim)
q_values = model(state)

assert q_values.shape == (action_dim,), "Output shape wrong!"
assert not torch.isnan(q_values).any(), "NaN in output!"
assert not torch.isinf(q_values).any(), "Inf in output!"

print(f"Q values: {q_values}")
```

---

**测试 2：Batch Forward Pass**

```python
batch_size = 32
states = torch.randn(batch_size, state_dim)
q_values = model(states)

assert q_values.shape == (batch_size, action_dim)
print(f"Q values shape: {q_values.shape}")
```

---

**测试 3：Gradient Flow**

```python
optimizer = Adam(model.parameters(), lr=1e-3)

# 随机输入和目标
states = torch.randn(32, state_dim)
targets = torch.randn(32, action_dim)

q_values = model(states)
loss = F.mse_loss(q_values, targets)

loss.backward()

# 检查梯度
for name, param in model.named_parameters():
    if param.grad is not None:
        print(f"{name}: grad_norm = {param.grad.norm().item()}")
    else:
        print(f"{name}: NO GRADIENT!")

optimizer.step()
```

---

**测试 4：Overfitting Test（过拟合测试）**

**思想**：如果网络无法过拟合小数据集，说明网络或优化有问题。

```python
# 创建小数据集（10个样本）
small_dataset = [
    (torch.randn(state_dim), torch.randn(action_dim))
    for _ in range(10)
]

model = QNetwork(state_dim, action_dim)
optimizer = Adam(model.parameters(), lr=1e-3)

# 训练直到过拟合
for epoch in range(1000):
    total_loss = 0
    for state, target in small_dataset:
        q_values = model(state)
        loss = F.mse_loss(q_values, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}, Loss: {total_loss/10}")

# 如果 loss < 1e-3，说明网络能过拟合
# 如果 loss 卡在高位，网络或优化有问题
```

---

### 4.3 Loss 计算调试

**测试：手工计算对比**

```python
# DQN Loss example
states = torch.tensor([[1.0, 2.0]])
actions = torch.tensor([0])
rewards = torch.tensor([1.0])
next_states = torch.tensor([[1.5, 2.5]])
dones = torch.tensor([0.0])
gamma = 0.99

# Model forward
q_values = q_network(states)  # 假设输出 [3.0, 2.0]
q_value = q_values[0, actions[0]]  # 3.0

next_q_values = target_network(next_states)  # 假设 [4.0, 3.0]
target = rewards[0] + gamma * next_q_values.max()  # 1.0 + 0.99 * 4.0 = 4.96

loss = (q_value - target)**2  # (3.0 - 4.96)^2 = 3.8416

# 手工计算
expected_loss = (3.0 - (1.0 + 0.99 * 4.0))**2  # 3.8416

assert abs(loss.item() - expected_loss) < 1e-6, "Loss computation wrong!"
```

---

**常见错误**：

```python
# 错误 1：索引错误
q_value = q_values[actions]  # ❌ Wrong shape
q_value = q_values[range(len(actions)), actions]  # ✅ Correct

# 错误 2：Detach 错误
target = reward + gamma * next_q.detach()  # ✅ Detach target
loss = (q.detach() - target)**2  # ❌ Detach q，no gradient!

# 错误 3：Done 处理错误
target = reward + gamma * next_q  # ❌ 终止状态也有 next_q
target = reward + gamma * next_q * (1 - done)  # ✅ 终止时 target=reward
```

---

## 5. 可视化与监控

### 5.1 关键指标监控

**必监控指标**：

```python
import wandb  # 或 tensorboard

# 1. Episode Reward（最重要）
wandb.log({'reward/episode': episode_reward})

# 2. Loss
wandb.log({'loss/value': value_loss, 'loss/policy': policy_loss})

# 3. Gradient Norm
grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float('inf'))
wandb.log({'grad_norm': grad_norm})

# 4. Q 值 / Value（值函数大小）
wandb.log({'q_mean': q_values.mean(), 'q_std': q_values.std()})

# 5. Entropy（策略多样性）
entropy = -(probs * log_probs).sum(-1).mean()
wandb.log({'entropy': entropy})

# 6. KL Divergence（策略变化，PPO）
kl = kl_divergence(old_policy, new_policy)
wandb.log({'kl': kl})

# 7. Explained Variance（Critic质量）
explained_var = 1 - (returns - values).var() / returns.var()
wandb.log({'explained_variance': explained_var})

# 8. Learning Rate（如果有schedule）
wandb.log({'lr': optimizer.param_groups[0]['lr']})
```

---

### 5.2 可视化技巧

**Reward Curve with Smoothing**：

```python
import matplotlib.pyplot as plt
import pandas as pd

# 原始数据
episode_rewards = [...]

# 滑动平均
window = 100
smoothed = pd.Series(episode_rewards).rolling(window).mean()

plt.figure(figsize=(10, 6))
plt.plot(episode_rewards, alpha=0.3, label='Raw')
plt.plot(smoothed, label=f'Smoothed (window={window})')
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.legend()
plt.title('Training Curve')
plt.show()
```

---

**Action Distribution（策略多样性）**：

```python
# 收集一个 episode 的 actions
actions_in_episode = [...]

plt.hist(actions_in_episode, bins=action_dim, range=(0, action_dim))
plt.xlabel('Action')
plt.ylabel('Frequency')
plt.title('Action Distribution')
plt.show()

# 如果分布极度不均（如99%一个动作）→ 探索不足或策略退化
```

---

**Q 值热图（Q-table，小状态空间）**：

```python
# 对于 GridWorld 等
q_table = np.zeros((grid_height, grid_width, action_dim))

for i in range(grid_height):
    for j in range(grid_width):
        state = (i, j)
        q_table[i, j] = agent.Q[state]

# 绘制每个动作的 Q 值
fig, axes = plt.subplots(1, action_dim, figsize=(15, 5))
for a in range(action_dim):
    im = axes[a].imshow(q_table[:, :, a], cmap='viridis')
    axes[a].set_title(f'Action {a}')
    plt.colorbar(im, ax=axes[a])
plt.show()
```

---

**Policy Visualization（连续动作）**：

```python
# 对于 1D state, 1D action
states = np.linspace(-3, 3, 100)
actions = []

for s in states:
    state_tensor = torch.tensor([s], dtype=torch.float32)
    with torch.no_grad():
        action = policy_network(state_tensor).item()
    actions.append(action)

plt.plot(states, actions)
plt.xlabel('State')
plt.ylabel('Action')
plt.title('Policy Visualization')
plt.show()
```

---

### 5.3 实时监控面板

**使用 TensorBoard**：

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment_1')

for episode in range(num_episodes):
    # 训练...

    writer.add_scalar('Reward/episode', episode_reward, episode)
    writer.add_scalar('Loss/value', value_loss, episode)
    writer.add_scalar('Entropy', entropy, episode)

    # 直方图
    writer.add_histogram('Q_values', q_values, episode)

    # 图像（如 env rendering）
    img = env.render(mode='rgb_array')
    writer.add_image('Environment', img, episode, dataformats='HWC')

writer.close()
```

**启动 TensorBoard**：
```bash
tensorboard --logdir=runs
```

---

## 6. 单元测试与验证

### 6.1 Environment 单元测试

```python
import unittest

class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.env = MyCustomEnv()

    def test_reset(self):
        """测试 reset 返回正确形状"""
        state = self.env.reset()
        self.assertEqual(state.shape, (state_dim,))

    def test_step_shape(self):
        """测试 step 返回正确形状"""
        state = self.env.reset()
        next_state, reward, done, info = self.env.step(0)

        self.assertEqual(next_state.shape, (state_dim,))
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)
        self.assertIsInstance(info, dict)

    def test_reward_range(self):
        """测试 reward 在合理范围"""
        for _ in range(100):
            self.env.reset()
            _, reward, _, _ = self.env.step(self.env.action_space.sample())
            self.assertGreaterEqual(reward, -1000)  # 下界
            self.assertLessEqual(reward, 1000)  # 上界

    def test_done_condition(self):
        """测试终止条件"""
        self.env.reset()
        # 执行应该导致终止的动作
        _, _, done, _ = self.env.step(action_to_fail)
        self.assertTrue(done)

if __name__ == '__main__':
    unittest.main()
```

---

### 6.2 Network 单元测试

```python
class TestQNetwork(unittest.TestCase):

    def test_forward_single(self):
        """测试单个输入"""
        model = QNetwork(state_dim=4, action_dim=2)
        state = torch.randn(4)
        q_values = model(state)

        self.assertEqual(q_values.shape, (2,))
        self.assertFalse(torch.isnan(q_values).any())

    def test_forward_batch(self):
        """测试批量输入"""
        model = QNetwork(state_dim=4, action_dim=2)
        states = torch.randn(32, 4)
        q_values = model(states)

        self.assertEqual(q_values.shape, (32, 2))

    def test_gradient_flow(self):
        """测试梯度流"""
        model = QNetwork(state_dim=4, action_dim=2)
        state = torch.randn(4, requires_grad=True)
        q_values = model(state)
        loss = q_values.sum()
        loss.backward()

        # 检查所有参数都有梯度
        for param in model.parameters():
            self.assertIsNotNone(param.grad)
            self.assertFalse(torch.isnan(param.grad).any())
```

---

### 6.3 算法单元测试

```python
class TestDQN(unittest.TestCase):

    def test_simple_environment(self):
        """测试在简单环境（CartPole）上能学习"""
        env = gym.make('CartPole-v1')
        agent = DQNAgent(state_dim=4, action_dim=2)

        # 训练 1000 步
        train(agent, env, steps=1000)

        # 评估
        avg_reward = evaluate(agent, env, episodes=10)

        # 应该比 random 好
        random_reward = 20  # CartPole random 基准
        self.assertGreater(avg_reward, random_reward)

    def test_overfitting(self):
        """测试能过拟合小数据集"""
        # 创建固定数据集
        dataset = create_small_dataset(size=10)

        agent = DQNAgent(state_dim=4, action_dim=2)

        # 训练直到过拟合
        for _ in range(1000):
            batch = random.sample(dataset, 10)
            loss = agent.update(batch)

        # Loss 应该很小
        final_loss = agent.compute_loss(dataset)
        self.assertLess(final_loss, 0.01)
```

---

## 7. 性能剖析

### 7.1 识别瓶颈

**使用 Python Profiler**：

```python
import cProfile
import pstats

def train_episode():
    # 你的训练代码
    ...

# Profile
profiler = cProfile.Profile()
profiler.enable()

for _ in range(100):
    train_episode()

profiler.disable()

# 分析
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # 前 20 个最慢的函数
```

**输出示例**：
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      100    0.050    0.001    5.234    0.052 agent.py:42(update)
    10000    2.135    0.000    2.135    0.000 network.py:15(forward)
     5000    1.823    0.000    1.823    0.000 replay_buffer.py:28(sample)
```

**瓶颈**：network.forward 和 replay_buffer.sample

---

**使用 PyTorch Profiler**：

```python
import torch.profiler as profiler

with profiler.profile(
    activities=[
        profiler.ProfilerActivity.CPU,
        profiler.ProfilerActivity.CUDA,
    ],
    record_shapes=True,
    profile_memory=True,
    with_stack=True
) as prof:
    for _ in range(100):
        train_step()

print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))

# 导出 Chrome trace
prof.export_chrome_trace("trace.json")
```

---

### 7.2 常见性能问题

**问题 1：GPU 未被充分利用**

```python
# 检查
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Current device: {torch.cuda.current_device()}")

# 监控 GPU 使用率
# nvidia-smi
```

**解决**：
- 增大 batch size（充分利用 GPU）
- 检查数据传输（CPU→GPU 是瓶颈？）
- 异步数据加载

---

**问题 2：数据采样慢**

```python
# 如果 replay_buffer.sample() 很慢

# 优化 1：预分配内存
class ReplayBuffer:
    def __init__(self, capacity):
        self.states = np.zeros((capacity, state_dim))  # 预分配
        self.actions = np.zeros(capacity, dtype=np.int64)
        # ...

# 优化 2：使用更快的数据结构（如 deque）
from collections import deque
self.buffer = deque(maxlen=capacity)
```

---

**问题 3：环境交互慢**

```python
# 并行环境（Vectorized Env）
from stable_baselines3.common.vec_env import SubprocVecEnv

def make_env():
    def _init():
        return gym.make('CartPole-v1')
    return _init

num_envs = 8
env = SubprocVecEnv([make_env() for _ in range(num_envs)])

# 现在一次 step 返回 num_envs 个 transitions
states = env.reset()  # (num_envs, state_dim)
next_states, rewards, dones, infos = env.step(actions)
```

---

## 8. 复现性保证

### 8.1 设置所有随机种子

```python
def set_seed(seed):
    """设置所有随机种子以确保复现性"""
    import random
    import numpy as np
    import torch

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # 确定性算法（可能降低性能）
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    # Environment seed
    # env.seed(seed)  # Gym 0.26+ 使用 env.reset(seed=seed)

set_seed(42)
```

---

### 8.2 记录超参数和版本

```python
import json
import sys
import torch

config = {
    'seed': 42,
    'lr': 3e-4,
    'gamma': 0.99,
    'batch_size': 64,
    # ... 所有超参数
}

# 记录环境
env_info = {
    'python_version': sys.version,
    'torch_version': torch.__version__,
    'cuda_available': torch.cuda.is_available(),
    'cuda_version': torch.version.cuda if torch.cuda.is_available() else None,
}

# 保存
with open('config.json', 'w') as f:
    json.dump({'config': config, 'env_info': env_info}, f, indent=2)
```

---

### 8.3 版本控制

```bash
# Git commit before experiment
git add .
git commit -m "Experiment: DQN on CartPole with lr=3e-4"

# 记录 commit hash
git rev-parse HEAD > experiment_commit.txt

# 依赖版本
pip freeze > requirements.txt
```

---

## 9. 调试工具箱

### 9.1 断言（Assertions）

**大量使用断言**：

```python
def update(self, states, actions, rewards, next_states, dones):
    # Shape assertions
    assert states.shape[0] == actions.shape[0] == rewards.shape[0]
    assert states.shape[1] == self.state_dim
    assert actions.max() < self.action_dim
    assert actions.min() >= 0

    # Value range assertions
    assert torch.all((dones == 0) | (dones == 1)), "Done must be 0 or 1"

    # 计算...
    q_values = self.q_network(states)

    # Output assertions
    assert not torch.isnan(q_values).any(), "NaN in Q values!"
    assert not torch.isinf(q_values).any(), "Inf in Q values!"

    # ...
```

---

### 9.2 调试模式（Debug Mode）

```python
class Agent:
    def __init__(self, debug=False):
        self.debug = debug

    def update(self, batch):
        if self.debug:
            print(f"Batch size: {len(batch)}")
            print(f"State range: [{states.min()}, {states.max()}]")
            print(f"Reward range: [{rewards.min()}, {rewards.max()}]")

        loss = self.compute_loss(batch)

        if self.debug:
            print(f"Loss: {loss.item()}")

            # 检查梯度
            self.optimizer.zero_grad()
            loss.backward()

            for name, param in self.model.named_parameters():
                if param.grad is not None:
                    print(f"{name}: grad_norm = {param.grad.norm().item()}")

        self.optimizer.step()
```

---

### 9.3 Checkpointing

**保存中间结果**：

```python
def save_checkpoint(episode, agent, optimizer, rewards):
    checkpoint = {
        'episode': episode,
        'model_state_dict': agent.q_network.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'rewards': rewards,
    }

    torch.save(checkpoint, f'checkpoint_ep{episode}.pth')

# 训练中定期保存
if episode % 1000 == 0:
    save_checkpoint(episode, agent, optimizer, episode_rewards)
```

**加载检查点继续训练**：

```python
def load_checkpoint(filename):
    checkpoint = torch.load(filename)

    agent.q_network.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    start_episode = checkpoint['episode']
    rewards = checkpoint['rewards']

    return start_episode, rewards
```

---

## 10. 面试常见问题

### Q1: 如果 RL agent 完全不学习，如何调试？

**答案**：

**系统化诊断流程**：

**Step 1：Sanity Checks（5分钟）**

```python
# 1. Random policy baseline
random_reward = test_random_policy(env, episodes=10)
print(f"Random reward: {random_reward}")

# 如果 random = 0 → 环境可能有问题

# 2. Gradient 检查
loss.backward()
print(f"Grad norm: {get_grad_norm(model)}")

# 如果 grad_norm = 0 → 梯度未流动

# 3. 简单环境测试
# 换成 CartPole 等已知环境，看是否学习
```

---

**Step 2：逐个排查常见原因**

**1. Learning rate 太小**：
```python
# 尝试 lr = 1e-3（较大）
optimizer = Adam(params, lr=1e-3)
```

**2. Reward 太稀疏**：
```python
# 检查
non_zero_ratio = (rewards != 0).mean()
if non_zero_ratio < 0.05:
    print("Reward too sparse!")
    # 添加 reward shaping
```

**3. 探索不足**：
```python
# 增大 ε（DQN）或 entropy（PPO）
epsilon = 1.0  # 保持高探索
entropy_coef = 0.1
```

**4. Network 初始化**：
```python
# 检查输出
for _ in range(10):
    print(model(random_state))

# 如果输出全一样 → 初始化有问题
# 重新初始化
model.apply(init_weights)
```

**5. Bug in implementation**：
```python
# 过拟合测试：能否过拟合小数据集？
small_data = create_fixed_dataset(size=10)
for _ in range(1000):
    loss = train_on(small_data)

if loss > 0.01:
    print("Cannot overfit → bug in network or optimizer")
```

---

**Step 3：对比已知实现**

```python
# 使用 Stable-Baselines3 作为 baseline
from stable_baselines3 import DQN

model = DQN('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=10000)

# 如果 SB3 能学习，但你的不能 → implementation bug
# 逐个组件对比
```

---

**总结清单**：

```
□ Random policy 有非零 reward？
□ Gradient 存在且非零？
□ Learning rate 合理（1e-4 ~ 1e-3）？
□ Reward 不是太稀疏（>5% non-zero）？
□ Exploration 充分（ε > 0.1 或 entropy > 0）？
□ Network 输出合理（不全是同一个值）？
□ 能过拟合小数据集？
□ 能在简单环境（CartPole）学习？
□ 对比 SB3 等已知实现？
```

---

### Q2: 如何判断性能瓶颈在哪里？

**答案**：

**性能瓶颈可能出现的地方**：

1. **Environment interaction**（环境交互）
2. **Network forward/backward**（网络计算）
3. **Data sampling**（数据采样）
4. **Logging/Visualization**（记录和可视化）

---

**诊断方法**：

**1. Profiling**

```python
import cProfile

profiler = cProfile.Profile()
profiler.enable()

# 运行一部分训练
for _ in range(100):
    train_step()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(10)  # Top 10 slowest
```

**输出示例**：
```
Function                   Calls   TotTime   PerCall
env.step()                 10000   5.2s      0.52ms   ← 环境慢
network.forward()          5000    3.1s      0.62ms
replay_buffer.sample()     100     1.8s      18ms     ← 采样慢
logger.log()               100     0.5s      5ms
```

---

**2. 逐个模块计时**

```python
import time

# Environment
t0 = time.time()
for _ in range(1000):
    env.step(env.action_space.sample())
env_time = time.time() - t0
print(f"Env: {env_time:.2f}s for 1000 steps")

# Network forward
states = torch.randn(1000, state_dim).to(device)
t0 = time.time()
for _ in range(100):
    model(states)
net_time = time.time() - t0
print(f"Network: {net_time:.2f}s for 100 batches")

# Replay buffer sampling
buffer = ReplayBuffer(100000)
# ... fill buffer
t0 = time.time()
for _ in range(1000):
    buffer.sample(batch_size=64)
sample_time = time.time() - t0
print(f"Sampling: {sample_time:.2f}s for 1000 samples")
```

---

**3. 常见优化**

**环境慢**：
```python
# 并行环境
from stable_baselines3.common.vec_env import SubprocVecEnv
env = SubprocVecEnv([make_env for _ in range(8)])
```

**网络慢**：
```python
# GPU
model = model.to('cuda')
states = states.to('cuda')

# Mixed precision（混合精度）
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()

with autocast():
    loss = compute_loss(...)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

**采样慢**：
```python
# NumPy array（预分配）而非 list
# 或使用更快的数据结构
```

**记录慢**：
```python
# 减少记录频率
if episode % 10 == 0:  # 每 10 个 episode 记录一次
    logger.log(...)
```

---

**总结**：

1. **Profile** 找到最慢的函数
2. **针对性优化**：
   - Env 慢 → 并行
   - Network 慢 → GPU, mixed precision
   - Sampling 慢 → 优化数据结构
3. **衡量加速比**：优化前后对比

---

## 总结

**RL 调试的核心要点**：

1. **系统化流程**：Sanity checks → 组件测试 → 算法验证 → 性能调优
2. **关键诊断**：监控 gradient, loss, reward, Q values, entropy
3. **可视化**：Learning curve, action distribution, Q heatmap
4. **单元测试**：Environment, Network, Algorithm 分别测试
5. **复现性**：设置种子、记录超参数、版本控制
6. **性能优化**：Profiling, 并行环境, GPU, 异步数据加载

**调试黄金法则**：

> "Start simple, isolate components, visualize everything, compare with baselines."

**常用工具**：
- WandB / TensorBoard（监控）
- Stable-Baselines3（已知基准）
- cProfile（性能分析）
- Unit tests（组件验证）
- Assertions（运行时检查）

**记住**：
> "Most RL bugs are not in the algorithm, but in the implementation details. Patience and systematic debugging > guesswork."

希望这份指南能帮助你快速定位和解决 RL 训练中的问题！
