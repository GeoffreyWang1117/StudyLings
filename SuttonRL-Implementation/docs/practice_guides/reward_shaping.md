# Reward Shaping 完整实践指南

## 目录
1. [引言：为什么需要 Reward Shaping？](#1-引言为什么需要-reward-shaping)
2. [什么是 Reward Shaping？](#2-什么是-reward-shaping)
3. [Potential-based Reward Shaping（理论基础）](#3-potential-based-reward-shaping理论基础)
4. [常见 Reward Shaping 技巧](#4-常见-reward-shaping-技巧)
5. [Reward Shaping 的陷阱](#5-reward-shaping-的陷阱)
6. [实际案例与最佳实践](#6-实际案例与最佳实践)
7. [如何设计好的 Reward](#7-如何设计好的-reward)
8. [Reward Engineering vs Reward Learning](#8-reward-engineering-vs-reward-learning)
9. [调试 Reward 函数](#9-调试-reward-函数)
10. [面试常见问题](#10-面试常见问题)

---

## 1. 引言：为什么需要 Reward Shaping？

### 1.1 稀疏奖励问题（Sparse Reward Problem）

**例子：迷宫**

```
S: 起点
G: 终点
#: 墙

###########
#S        #
#  ####   #
#     #   #
#     #  G#
###########
```

**Naive reward**：
```
r(s, a) = {
    +1,  if reach goal
     0,  otherwise
}
```

**问题**：
- Agent 99.9% 的时间收到 r=0
- 无法区分"接近目标"和"远离目标"
- 探索非常困难（如找针in haystack）
- 学习极慢或无法学习

**类比**：

想象你被蒙住眼睛，在一个房间里找一个按钮。别人只在你按到按钮时说"对了"，其他时候什么都不说。你会花很久才能找到！

如果别人能说"你离按钮更近了"或"你在往错误方向走"，你会快得多。

**Reward Shaping 的目标**：提供额外的引导信号，加速学习。

---

### 1.2 信用分配问题（Credit Assignment Problem）

**例子：国际象棋**

- 游戏有 50-100 步
- 最终奖励：+1（赢）/-1（输）
- 问题：哪一步导致了胜利/失败？

**Naive RL**：
- 将最终奖励分配给所有步骤
- 但早期的随机移动和后期的关键移动都得到相同奖励
- 学习效率低

**Reward Shaping**：
- 中间奖励：吃掉对手棋子 +0.1，丢掉自己棋子 -0.1
- 位置优势：控制中心 +0.01
- 加速学习关键策略

---

### 1.3 理想 vs 现实

**理想情况**：
- 只给最终任务目标（如"赢得游戏"）
- Agent 自己学会所有中间步骤
- 无需人工设计

**现实情况**：
- 探索空间巨大
- 样本效率要求高（训练成本）
- 需要在合理时间内收敛

**解决方案**：Reward Shaping 作为工程手段加速训练。

---

## 2. 什么是 Reward Shaping？

### 2.1 定义

**Reward Shaping**：修改原始奖励函数，添加额外的引导信号。

**原始 MDP**：
```
M = (S, A, P, R, γ)
```

**Shaped MDP**：
```
M' = (S, A, P, R', γ)
```

其中：
```
R'(s, a, s') = R(s, a, s') + F(s, s')
```

F(s, s') 是 **shaping function**（塑形函数）。

### 2.2 目标

**理想的 Reward Shaping**：

1. **加速学习**：更快收敛到最优策略
2. **保持最优性**：最优策略不变（π'* = π*）
3. **引导探索**：帮助 agent 探索有价值的区域

**关键问题**：如何保证添加的 F 不改变最优策略？

答案：**Potential-based Shaping**

---

## 3. Potential-based Reward Shaping（理论基础）

### 3.1 定义

**定理（Ng, Harada, Russell 1999）**：

如果 shaping function 的形式为：

```
F(s, s') = γ Φ(s') - Φ(s)
```

其中 Φ: S → ℝ 是任意**势函数（potential function）**，则：

1. **最优策略不变**：shaped MDP 的最优策略与原始 MDP 相同
2. **Q 函数关系**：Q'*(s,a) = Q*(s,a) + Φ(s)

**直觉**：
- Φ(s) 可以理解为状态的"潜力"
- F(s, s') = γ Φ(s') - Φ(s) 是势能差（类似物理中的重力势能）
- 这种形式不改变动作的相对优劣

### 3.2 证明

**证明最优策略不变**：

假设 π* 是原始 MDP 的最优策略，我们要证明它也是 shaped MDP 的最优策略。

**Step 1**：Q 函数的关系

Shaped Q 函数：

```
Q'(s,a) = E[r' + γ Q'(s',a') | s,a]
        = E[r + F(s,s') + γ Q'(s',a') | s,a]
        = E[r + γΦ(s') - Φ(s) + γ Q'(s',a') | s,a]
```

猜测：Q'(s,a) = Q(s,a) + Φ(s)

**验证**：

```
Q(s,a) + Φ(s)
= E[r + γ Q(s',a') | s,a] + Φ(s)
= E[r + γ(Q'(s',a') - Φ(s')) | s,a] + Φ(s)  [使用猜测]
= E[r + γ Q'(s',a') - γ Φ(s') + Φ(s) | s,a]
= E[r + γ Q'(s',a') + F(s,s') | s,a]
= Q'(s,a)
```

因此 Q'(s,a) = Q(s,a) + Φ(s)。

**Step 2**：最优动作不变

```
argmax_a Q'(s,a) = argmax_a [Q(s,a) + Φ(s)]
                  = argmax_a Q(s,a)  [Φ(s) 对所有 a 相同]
```

因此 π'*(s) = argmax_a Q'(s,a) = argmax_a Q(s,a) = π*(s)。

**证毕！** ∎

---

### 3.3 直觉理解

**类比：山地**

想象状态空间是一个山地地形：
- Φ(s)：每个位置的高度（势能）
- F(s, s') = γΦ(s') - Φ(s)：爬升/下降的势能变化

**原始奖励**：到达山顶（目标）+100

**Potential shaping**：
- 设置 Φ(s) = 距离目标的负距离（越近越高）
- Agent 每移动一步，如果更接近目标，得到 +奖励（势能增加）
- 如果远离目标，得到 -奖励（势能减少）

**关键**：
- 最终到达山顶的总奖励仍然是 +100
- 但路径上的每一步都有方向指引
- 不改变"山顶是最优目标"，只是让路径更清晰

---

### 3.4 实际例子

**迷宫**：

Φ(s) = -曼哈顿距离(s, goal)

```python
def phi(state, goal):
    return -abs(state[0] - goal[0]) - abs(state[1] - goal[1])

def shaped_reward(state, next_state, goal, gamma=0.99):
    original_reward = 1.0 if next_state == goal else 0.0
    shaping = gamma * phi(next_state, goal) - phi(state, goal)
    return original_reward + shaping
```

**效果**：
- 每向目标移动一步：+1
- 每远离目标一步：-1
- 到达目标额外：+1（原始奖励）

**导航任务**：

Φ(s) = 距离目标的负欧氏距离

```python
def phi(state, goal):
    return -np.linalg.norm(state - goal)
```

**游戏**：

Φ(s) = 当前分数（如 Atari 游戏的得分）

```python
def phi(state):
    return state.score
```

这自然地将"得分"转化为 potential。

---

### 3.5 为什么 Potential-based 重要？

**理论保证**：
- 不改变最优策略
- 可以自由设计 Φ 来引导学习
- 不用担心"教错了"

**实践指导**：
- 如果你的 shaping 可以写成 γΦ(s') - Φ(s) 形式，就是安全的
- 否则，可能改变最优策略（需谨慎）

---

## 4. 常见 Reward Shaping 技巧

### 4.1 距离-based Shaping

**思想**：越接近目标，Φ 越大。

**例子 1：负距离**
```python
Φ(s) = -distance(s, goal)
F(s, s') = γ * (-distance(s', goal)) - (-distance(s, goal))
         = distance(s, goal) - γ * distance(s', goal)
```

**例子 2：负平方距离**（更平滑）
```python
Φ(s) = -distance²(s, goal)
```

**例子 3：指数衰减**
```python
Φ(s) = exp(-distance(s, goal) / σ)
```

**适用**：导航、到达目标类任务。

---

### 4.2 进度-based Shaping

**思想**：奖励任务完成的百分比。

**例子：多阶段任务**

任务：拿到钥匙 → 开门 → 到达目标

```python
def phi(state):
    progress = 0
    if state.has_key:
        progress += 33
    if state.door_opened:
        progress += 33
    if state.at_goal:
        progress += 34
    return progress
```

**效果**：
- 拿到钥匙：+33
- 开门：+33
- 到达目标：+34

**适用**：分阶段任务、长期任务。

---

### 4.3 基于领域知识的 Shaping

**例子 1：机器人抓取**

```python
def phi(state):
    hand_to_object = -distance(state.hand, state.object)
    object_to_goal = -distance(state.object, state.goal)
    return 0.5 * hand_to_object + 0.5 * object_to_goal
```

**例子 2：自动驾驶**

```python
def phi(state):
    # 车道中心距离
    lane_alignment = -abs(state.lane_offset)

    # 速度（接近限速为好）
    speed_bonus = -abs(state.speed - speed_limit)

    # 朝向目标
    heading_alignment = cos(state.heading - target_heading)

    return 0.3 * lane_alignment + 0.3 * speed_bonus + 0.4 * heading_alignment
```

**适用**：复杂任务，有明确子目标。

---

### 4.4 基于模型的 Shaping

**思想**：用启发式/简化模型估计到目标的"代价"。

**例子：迷宫 - A* 启发式**

```python
def phi(state):
    # A* 估计的到达目标的步数（负值）
    return -astar_heuristic(state, goal)
```

**例子：Dijkstra 距离**

```python
# 预计算从每个状态到目标的最短路径长度
phi_values = dijkstra(graph, goal)

def phi(state):
    return -phi_values[state]
```

**优势**：
- 提供精确的引导
- 特别是在已知环境地图时

**劣势**：
- 需要额外计算
- 可能不适用于未知环境

---

### 4.5 中间奖励（Intermediate Rewards）

**非 Potential-based，但常用**：

**例子：游戏**

```python
def reward(state, action, next_state):
    r = 0

    # 原始奖励：赢/输
    if game_won(next_state):
        r += 100
    elif game_lost(next_state):
        r -= 100

    # Shaping：吃掉敌人
    if enemy_killed:
        r += 10

    # Shaping：收集物品
    if item_collected:
        r += 1

    # Shaping：生存时间
    r += 0.01  # 每步小额奖励

    return r
```

**注意**：这些不一定是 potential-based，可能改变最优策略！

**何时安全**：
- 中间奖励与最终目标一致
- 例如："吃敌人"确实帮助"赢得游戏"

**何时危险**：
- 中间奖励可能导致次优策略
- 例如："生存时间"可能让 agent 避免风险，不敢进攻

---

### 4.6 Curiosity / Intrinsic Motivation

**思想**：奖励探索未知状态。

**Count-based**：
```python
def phi(state):
    visit_count = count[state]
    return 1 / sqrt(visit_count + 1)
```

**ICM（Intrinsic Curiosity Module）**：
- 奖励预测误差
- 难以预测的状态 → 更有趣 → 更多奖励

**适用**：探索问题、稀疏奖励。

---

## 5. Reward Shaping 的陷阱

### 5.1 Reward Hacking（奖励黑客）

**定义**：Agent 学会利用 shaping 奖励，而不完成真正任务。

**例子 1：清洁机器人**

**任务**：清理房间垃圾

**Naive shaping**：
```
r = -垃圾数量
```

**问题**：
- Agent 可能把垃圾推到看不见的地方（而不是清理）
- 或者打破垃圾桶让垃圾洒出来，再清理（重复获得奖励）

**解决**：
- 明确定义"清理"（放入垃圾桶）
- 限制重复奖励

---

**例子 2：赛车游戏**

**任务**：尽快完成赛道

**Naive shaping**：
```
r = speed  # 奖励速度
```

**问题**：
- Agent 学会在一个地方原地打转（产生高速度，但不前进）

**解决**：
```
r = progress_on_track  # 奖励赛道进度
```

或者：
```
Φ(s) = -distance_to_finish
```

---

**例子 3：OpenAI CoastRunners**

**任务**：赢得赛艇比赛

**Naive shaping**：收集赛道上的能量包 +奖励

**问题**：
- Agent 发现可以在能量包重生点原地打转，无限收集
- 完全忽略比赛目标

**教训**：Shaping 必须与最终目标完全对齐。

---

### 5.2 过度引导（Over-shaping）

**问题**：Shaping 太强，限制了 agent 发现更优策略。

**例子：迷宫捷径**

```
S ########## G
  #        #
  # ###### #
  #        #
  ##########
```

**Shaping**：Φ(s) = -曼哈顿距离(s, G)

**问题**：
- 曼哈顿距离鼓励"右走"
- 但实际最优路径可能需要先"左走"绕过障碍
- Agent 可能因为负 shaping 而不探索更优路径

**解决**：
- 使用更宽松的 shaping（如基于真实最短路径）
- 保持足够探索（ε-greedy, entropy bonus）

---

### 5.3 非 Potential-based 导致策略改变

**例子**：

原始奖励：到达目标 +100

**Shaping 1**（Potential-based）：
```
Φ(s) = -distance(s, goal)
F(s,s') = γ Φ(s') - Φ(s)
```
✅ 最优策略不变

**Shaping 2**（非 Potential）：
```
F(s,s') = -1  # 每步 -1（惩罚时间）
```
❌ 最优策略改变！
- 原本可以慢慢走到目标
- 现在必须尽快（因为每步 -1）

**教训**：
- 如果可以，用 Potential-based
- 否则，仔细分析是否改变策略

---

### 5.4 缩放问题（Scaling）

**问题**：Shaping 奖励远大于原始奖励，掩盖真实目标。

**例子**：

```python
# 原始奖励
if reach_goal:
    r = 1

# Shaping（太大）
r += 1000 * (distance_reduction)
```

**结果**：
- Shaping 占主导
- 原始目标变得不重要
- 可能学会次优策略

**解决**：
- 保持 shaping 和原始奖励在同一数量级
- 或者归一化

```python
shaping_weight = 0.1  # 控制 shaping 强度
r = original_reward + shaping_weight * shaping_term
```

---

### 5.5 状态表示问题

**问题**：Φ(s) 依赖于状态表示，不同表示可能导致不同效果。

**例子**：

图像输入（Atari）：
```python
Φ(s) = -distance(agent_position, goal_position)
```

但如果从原始像素难以提取位置，Φ 难以计算。

**解决**：
- 确保 Φ 可以从可用状态信息计算
- 或者使用学习的 Φ（后面讨论）

---

## 6. 实际案例与最佳实践

### 6.1 案例 1：机器人导航

**任务**：机器人从起点移动到目标，避开障碍。

**原始奖励**：
```python
r = 100 if at_goal else -1 # 每步 -1 鼓励快速
```

**Potential shaping**：
```python
def phi(state, goal):
    # 负欧氏距离
    return -np.linalg.norm(state.position - goal)

def shaped_reward(state, action, next_state, goal, gamma=0.99):
    # 原始奖励
    if next_state.at_goal:
        r = 100
    elif next_state.collision:
        r = -100
    else:
        r = -1  # 时间惩罚

    # Potential shaping
    shaping = gamma * phi(next_state, goal) - phi(state, goal)

    return r + 0.1 * shaping  # 降低 shaping 权重
```

**效果**：
- 快速学会朝目标移动
- 仍然避免碰撞（大惩罚）
- 平衡时间效率和安全性

---

### 6.2 案例 2：Atari Montezuma's Revenge

**挑战**：极度稀疏奖励，需要多步才能得分。

**方法 1：Distance to Key/Door**

```python
def phi(state):
    if not state.has_key:
        return -distance(agent, key)
    elif not state.door_opened:
        return 10 - distance(agent, door)
    else:
        return 20 - distance(agent, goal)
```

**方法 2：Curriculum Learning + Shaping**

- 阶段 1：只学"拿钥匙"
- 阶段 2：学"开门"
- 阶段 3：学"到达目标"
- 每个阶段用对应的 shaping

**方法 3：Learned Shaping（后面讨论）**

---

### 6.3 案例 3：机器人抓取

**任务**：抓住物体并放到目标位置。

**原始奖励**：
```python
r = 1 if object_at_goal else 0
```

**Potential shaping（分阶段）**：

```python
def phi(state):
    hand = state.hand_position
    obj = state.object_position
    goal = state.goal_position

    if not state.is_grasping:
        # 阶段 1：手接近物体
        return 10 * (1 - distance(hand, obj) / max_dist)
    else:
        # 阶段 2：物体接近目标
        return 10 + 10 * (1 - distance(obj, goal) / max_dist)
```

**效果**：
- 先学会"伸手"
- 再学会"抓取"
- 最后学会"放置"

---

### 6.4 最佳实践总结

**1. 从原始任务开始**：
- 先尝试不加 shaping
- 了解瓶颈在哪里

**2. 使用 Potential-based（如果可能）**：
- 理论保证
- 设计 Φ 使其反映"离目标多近"

**3. 保持 Shaping 适度**：
- Shaping 作为"提示"，不是"规则"
- 权重不要太大（0.01-0.1 倍原始奖励）

**4. 验证不改变最优策略**：
- 测试已知最优策略在 shaped 环境中是否仍最优
- 检查是否有 reward hacking

**5. 逐步减少 Shaping（可选）**：
- 训练前期：强 shaping
- 训练后期：减少 shaping
- 最终：只用原始奖励微调

```python
shaping_weight = max(0, 1 - epoch / total_epochs)
r = original + shaping_weight * shaping
```

**6. 监控训练**：
- 分别记录原始奖励和 shaping 奖励
- 确保原始奖励在增长（真正学会任务）

```python
logger.log("reward/original", original_reward)
logger.log("reward/shaping", shaping_reward)
logger.log("reward/total", total_reward)
```

---

## 7. 如何设计好的 Reward？

### 7.1 设计原则

**SMART 原则**（借鉴项目管理）：

- **Specific（具体）**：奖励明确的行为
- **Measurable（可测量）**：可以从状态计算
- **Aligned（对齐）**：与最终目标一致
- **Reasonable（合理）**：幅度适中
- **Testable（可测试）**：可以验证效果

### 7.2 设计流程

**Step 1：明确最终目标**

- 任务的成功标准是什么？
- 什么是真正的最优策略？

**Step 2：分解子目标**

- 完成任务需要哪些步骤？
- 哪些是必要的中间状态？

**Step 3：设计 Potential 函数**

- 哪些状态更"接近"目标？
- 如何量化"进度"？

**Step 4：检查一致性**

- Shaping 是否与目标一致？
- 是否可能 reward hacking？

**Step 5：实验验证**

- 小规模测试
- 监控原始奖励和 shaping 奖励
- 迭代调整

---

### 7.3 调试技巧

**可视化 Potential 函数**：

```python
# 2D 环境
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)

Z = np.zeros_like(X)
for i in range(len(x)):
    for j in range(len(y)):
        state = (X[i,j], Y[i,j])
        Z[i,j] = phi(state, goal)

plt.contourf(X, Y, Z, levels=20)
plt.colorbar(label='Φ(s)')
plt.plot(goal[0], goal[1], 'r*', markersize=20, label='Goal')
plt.legend()
plt.title('Potential Function Visualization')
```

**效果**：
- 检查 Φ 是否单调朝目标增加
- 发现是否有"陷阱"（局部最优）

---

**模拟专家轨迹**：

```python
# 用已知最优策略运行
expert_policy = lambda s: optimal_action(s)

states, actions, rewards = rollout(expert_policy, env)

print(f"Total original reward: {sum(original_rewards)}")
print(f"Total shaped reward: {sum(shaped_rewards)}")

# 检查每步 shaping
for t in range(len(states)-1):
    s, s_next = states[t], states[t+1]
    shaping = gamma * phi(s_next) - phi(s)
    print(f"Step {t}: {s} -> {s_next}, shaping = {shaping}")
```

**检查**：
- 专家轨迹上 shaping 是否为正（鼓励）？
- 是否有异常的大 shaping（可能设计错误）？

---

**A/B 测试**：

```python
# 实验组：with shaping
agent_shaped = train(env_shaped, ...)

# 对照组：without shaping
agent_baseline = train(env_original, ...)

# 比较
compare_performance(agent_shaped, agent_baseline)
```

**指标**：
- 收敛速度（多少 episode 达到阈值）
- 最终性能
- 样本效率

---

## 8. Reward Engineering vs Reward Learning

### 8.1 Reward Engineering（人工设计）

**优点**：
- 利用领域知识
- 快速原型
- 可解释

**缺点**：
- 需要专家
- 可能有偏见
- 不可扩展

**适用**：
- 领域知识丰富
- 任务相对简单
- 需要快速迭代

---

### 8.2 Reward Learning（自动学习）

**方法 1：Inverse RL（逆强化学习）**

- 从专家演示学习奖励函数
- 假设专家在最大化某个未知奖励
- 推断该奖励

**例子**：
```python
# 给定专家轨迹
expert_trajectories = [...]

# 学习奖励
reward_function = inverse_rl(expert_trajectories)

# 用学到的奖励训练
agent = train(env, reward=reward_function)
```

**方法 2：Learning from Human Feedback（RLHF）**

- 让人类比较两个轨迹
- 学习偏好模型（reward model）
- 用学到的奖励训练

**例子**：OpenAI ChatGPT

```python
# 采样两个轨迹
traj1 = rollout(policy, env)
traj2 = rollout(policy, env)

# 人类选择更好的
preference = human_compare(traj1, traj2)

# 训练 reward model
reward_model.update(traj1, traj2, preference)

# 用 reward model 训练策略
policy = ppo_train(env, reward=reward_model)
```

**方法 3：Curiosity-driven（好奇心驱动）**

- 自动生成探索奖励
- ICM, RND 等方法

---

### 8.3 混合方法

**实践中最佳**：结合两者

```python
def total_reward(state, action, next_state):
    # 人工设计的基础奖励
    r_task = task_reward(state, action, next_state)

    # 学习的 shaping
    r_shaping = learned_shaping(state, next_state)

    # 组合
    return r_task + 0.1 * r_shaping
```

---

## 9. 调试 Reward 函数

### 9.1 常见问题与诊断

**问题 1：Agent 不学习（性能不增长）**

**可能原因**：
- Reward 太稀疏
- Shaping 不够或方向错误

**诊断**：
```python
# 检查 reward 分布
print(f"Reward mean: {np.mean(rewards)}")
print(f"Reward std: {np.std(rewards)}")
print(f"Non-zero rewards: {np.sum(rewards != 0) / len(rewards)}")
```

如果 >95% reward 是 0 → 太稀疏！

**解决**：
- 添加 shaping
- 或简化任务

---

**问题 2：Agent 学到奇怪行为**

**可能原因**：
- Reward hacking
- Shaping 与目标不一致

**诊断**：
- 可视化 agent 行为
- 检查哪些动作获得高奖励

```python
# 记录高奖励的 transitions
high_reward_transitions = [(s,a,r,s') for (s,a,r,s') in buffer if r > threshold]

# 分析
for s, a, r, s_next in high_reward_transitions:
    print(f"State: {s}, Action: {a}, Reward: {r}")
```

**解决**：
- 修正 shaping
- 添加惩罚不想要的行为

---

**问题 3：训练不稳定**

**可能原因**：
- Reward scale 太大
- Shaping 变化太剧烈

**诊断**：
```python
# 检查 reward range
print(f"Reward range: [{np.min(rewards)}, {np.max(rewards)}]")

# 检查 shaping 变化
shaping_changes = [gamma * phi(s_next) - phi(s) for s, s_next in transitions]
print(f"Shaping change range: [{np.min(shaping_changes)}, {np.max(shaping_changes)}]")
```

**解决**：
- Normalize rewards
```python
r = (r - mean) / (std + 1e-8)
```

- Clip rewards
```python
r = np.clip(r, -10, 10)
```

---

### 9.2 Reward 调试 Checklist

**设计阶段**：

- [ ] 明确定义成功标准
- [ ] 检查 shaping 是否 potential-based
- [ ] 估算 reward 幅度（原始 vs shaping）
- [ ] 可视化 Φ(s)（如果可能）
- [ ] 在简单场景测试

**实现阶段**：

- [ ] 单元测试 reward 函数
- [ ] 检查边界情况（goal, collision, etc.）
- [ ] 确认 reward 可以从状态计算

**训练阶段**：

- [ ] 记录原始和 shaping 奖励（分开）
- [ ] 监控奖励分布（mean, std, non-zero%）
- [ ] 检查高奖励/低奖励的状态-动作
- [ ] 可视化 agent 行为

**评估阶段**：

- [ ] 测试在原始奖励下的性能
- [ ] 与 baseline（无 shaping）比较
- [ ] 检查是否 reward hacking
- [ ] 泛化到新场景

---

## 10. 面试常见问题

### Q1: 什么是 Reward Shaping？为什么需要它？

**答案**：

**定义**：
Reward Shaping 是修改原始奖励函数，添加额外引导信号的技术。

形式上：
```
R'(s, a, s') = R(s, a, s') + F(s, s')
```

**为什么需要**：

1. **稀疏奖励问题**：
   - 大部分时间 r=0，agent 无法学习
   - 例如：迷宫、游戏等

2. **信用分配问题**：
   - 长期任务中，哪一步导致成功/失败难以确定
   - Shaping 提供中间反馈

3. **加速学习**：
   - 引导探索有价值的区域
   - 样本效率提高

**例子**：

迷宫导航：
- 原始：到达目标 +1，其他 0
- Shaping：每接近目标一步 +小奖励

**关键挑战**：
- 如何设计不改变最优策略？
- 答案：Potential-based shaping

---

### Q2: 什么是 Potential-based Shaping？为什么它保证不改变最优策略？

**答案**：

**定义**（Ng, Harada, Russell 1999）：

Shaping function 形式为：
```
F(s, s') = γ Φ(s') - Φ(s)
```

其中 Φ: S → ℝ 是势函数。

**为什么不改变最优策略**：

**证明**：

Shaped Q 函数：
```
Q'(s,a) = E[r + F(s,s') + γ Q'(s',a')]
        = E[r + γΦ(s') - Φ(s) + γ Q'(s',a')]
```

可以证明：
```
Q'(s,a) = Q(s,a) + Φ(s)
```

因此：
```
argmax_a Q'(s,a) = argmax_a [Q(s,a) + Φ(s)]
                  = argmax_a Q(s,a)  [Φ(s) 对所有 a 相同]
```

最优动作不变！

**直觉**：
- Φ(s) 像"势能"
- F(s,s') 是势能差
- 类似物理中，势能只影响绝对能量，不影响力的方向（最优路径）

**实践**：
- 设计 Φ 使其反映"离目标多近"
- 例如：Φ(s) = -distance(s, goal)

---

### Q3: 举一个 Reward Hacking 的例子，如何避免？

**答案**：

**Reward Hacking**：Agent 学会利用 reward 设计缺陷，而不完成真正任务。

**经典例子：CoastRunners（OpenAI）**

**任务**：赢得赛艇比赛

**Reward 设计**：
```
r = race_position_score  # 比赛排名
  + collect_power_ups * 10  # 收集能量包
```

**问题**：
- Agent 发现能量包会在固定位置重生
- 学会在能量包点原地打转，无限收集
- 完全忽略比赛目标

**得分**：
- Hacking 策略：>10000 分（收集能量包）
- 真正赢得比赛：~300 分

**如何避免**：

1. **对齐 Shaping 和最终目标**：
   - 能量包应该帮助赢比赛（如加速）
   - 不应该本身就是目标

2. **限制重复奖励**：
   ```python
   collected_items = set()
   if item not in collected_items:
       r += 10
       collected_items.add(item)
   ```

3. **测试极端策略**：
   - 尝试"作弊"策略（如原地打转）
   - 看 reward 是否允许

4. **Use Potential-based**：
   ```python
   Φ(s) = -distance_to_finish_line
   ```
   这自然防止原地打转（没有进度 → 没有奖励）

5. **监控行为**：
   - 可视化 agent 策略
   - 如果行为异常，检查 reward

---

### Q4: Potential-based Shaping 在深度 RL（如 DQN）中如何应用？

**答案**：

**挑战**：

深度 RL 中，Φ(s) 难以手工设计：
- 状态是高维（如图像）
- 难以计算距离

**方法 1：特征工程**

从原始状态提取关键信息：

```python
def phi(state):
    # 从图像提取 agent 位置
    agent_pos = extract_agent_position(state)
    goal_pos = extract_goal_position(state)

    # 计算距离
    return -np.linalg.norm(agent_pos - goal_pos)
```

适用：可以提取位置/特征。

---

**方法 2：学习 Φ**

用神经网络学习势函数：

```python
class PotentialNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = ConvNet()
        self.fc = nn.Linear(512, 1)

    def forward(self, state):
        features = self.conv(state)
        phi = self.fc(features)
        return phi

# Shaping
phi_net = PotentialNetwork()
shaping = gamma * phi_net(next_state) - phi_net(state)
shaped_reward = original_reward + shaping
```

**训练 Φ**：
- 监督学习：用启发式（如 A* 距离）作为目标
  ```python
  loss = (phi_net(state) - (-astar_distance(state, goal)))^2
  ```

- 自监督：Φ 应该在成功轨迹上递增
  ```python
  # 成功的轨迹
  for t in range(len(trajectory)):
      assert phi_net(trajectory[t+1]) > phi_net(trajectory[t])
  ```

---

**方法 3：Hindsight Experience Replay (HER)**

不直接用 potential，而是重新标注目标：

```python
# 原始轨迹：目标 G，失败
trajectory = [(s0,a0,r0=0,s1), ..., (sT,aT,r=0,sT+1)]

# Hindsight：假装 sT 就是目标
for (s, a, r, s_next) in trajectory:
    if s_next == sT:
        r_new = 1  # 达到了"目标"（sT）
    else:
        r_new = 0
    replay_buffer.add((s, a, r_new, s_next))
```

效果：失败的轨迹变成成功的（对于另一个目标），提高样本效率。

---

**方法 4：Count-based / Curiosity**

自动生成探索奖励：

```python
# Count-based
visit_count = {}
def phi(state):
    state_hash = hash(state)
    count = visit_count.get(state_hash, 0)
    return 1 / sqrt(count + 1)

# 更新
visit_count[state_hash] += 1
```

**ICM（Intrinsic Curiosity Module）**：
- 预测误差作为 shaping
- 难以预测 → 新颖 → 高 shaping

---

**实践推荐**：

DQN 系列：
- 简单任务：手工 Φ（特征工程）
- 复杂任务：学习 Φ 或 HER 或 curiosity

**注意**：
- 深度 RL 中 potential-based 理论保证较弱（函数逼近 + off-policy）
- 实践中仍需实验验证

---

### Q5: 如何判断 Reward Shaping 是否有效？

**答案**：

**判断标准**：

**1. 训练速度**：
- Shaped vs Baseline（无 shaping）
- 到达阈值性能需要多少 episode/sample？

```python
# 比较学习曲线
plot(episodes, rewards_shaped, label='With Shaping')
plot(episodes, rewards_baseline, label='Baseline')

# 计算到达阈值的时间
time_to_threshold_shaped = find_first(rewards_shaped > threshold)
time_to_threshold_baseline = find_first(rewards_baseline > threshold)

print(f"Speedup: {time_to_threshold_baseline / time_to_threshold_shaped}x")
```

---

**2. 最终性能**：
- 在**原始奖励**下的性能（不是 shaped）
- 确保没有改变最优策略

```python
# 用 shaped 环境训练
agent_shaped = train(env_shaped, ...)

# 在原始环境评估
performance_original = evaluate(agent_shaped, env_original)

# 比较
print(f"Original reward: {performance_original}")
```

---

**3. 样本效率**：
- 达到相同性能需要多少样本？

```python
# Shaping
samples_shaped = count_samples_until(performance_threshold, agent_shaped)

# Baseline
samples_baseline = count_samples_until(performance_threshold, agent_baseline)

print(f"Sample efficiency: {samples_baseline / samples_shaped}x")
```

---

**4. 稳定性**：
- 多个随机种子的方差
- Shaping 是否让训练更稳定？

```python
# 运行多个种子
results_shaped = [train(seed=i, shaping=True) for i in range(10)]
results_baseline = [train(seed=i, shaping=False) for i in range(10)]

# 比较方差
print(f"Shaped std: {np.std(results_shaped)}")
print(f"Baseline std: {np.std(results_baseline)}")
```

---

**5. 行为检查**：
- Agent 行为是否符合预期？
- 是否有 reward hacking？

```python
# 可视化轨迹
visualize_trajectory(agent_shaped, env)

# 检查是否有异常行为
# 例如：原地打转、重复动作等
```

---

**实践 Checklist**：

- [ ] 学习曲线更陡峭（更快收敛）
- [ ] 原始环境下性能不降低（不改变最优策略）
- [ ] 样本效率提高（相同性能更少样本）
- [ ] 训练更稳定（多次运行方差小）
- [ ] 无 reward hacking（行为正常）
- [ ] Ablation study（证明是 shaping 的效果，不是其他因素）

---

**可视化示例**：

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. 学习曲线
axes[0, 0].plot(episodes, rewards_shaped, label='Shaped', alpha=0.7)
axes[0, 0].plot(episodes, rewards_baseline, label='Baseline', alpha=0.7)
axes[0, 0].set_title('Learning Curve')
axes[0, 0].legend()

# 2. 样本效率
axes[0, 1].bar(['Shaped', 'Baseline'], [samples_shaped, samples_baseline])
axes[0, 1].set_title('Samples to Threshold')

# 3. 多种子稳定性
axes[1, 0].boxplot([results_shaped, results_baseline], labels=['Shaped', 'Baseline'])
axes[1, 0].set_title('Stability (Multiple Seeds)')

# 4. Reward 组成（shaped agent）
axes[1, 1].plot(episodes, original_rewards, label='Original', alpha=0.7)
axes[1, 1].plot(episodes, shaping_rewards, label='Shaping', alpha=0.7)
axes[1, 1].plot(episodes, total_rewards, label='Total', alpha=0.7)
axes[1, 1].set_title('Reward Decomposition')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('shaping_evaluation.png')
```

---

**总结**：

有效的 Reward Shaping 应该：
1. 加速学习（学习曲线）
2. 保持性能（原始奖励）
3. 提高效率（样本数）
4. 增强稳定性（方差）
5. 行为正常（无 hacking）

通过 A/B 测试、多指标监控、可视化分析综合判断。

---

## 总结

**Reward Shaping 的核心要点**：

1. **目的**：解决稀疏奖励、加速学习
2. **Potential-based**：F(s,s') = γΦ(s') - Φ(s)，保证不改变最优策略
3. **设计原则**：与目标对齐、适度引导、可测试
4. **常见陷阱**：Reward hacking、过度引导、缩放问题
5. **评估方法**：学习速度、最终性能、样本效率、稳定性、行为检查

**实践建议**：

- 优先使用 Potential-based（理论保证）
- 从简单 Φ 开始（如负距离）
- 逐步调整权重
- 监控原始奖励（确保真正学到任务）
- A/B 测试验证效果
- 必要时结合学习方法（IRL, RLHF）

**记住**：
> Reward Shaping 是工具，不是目标。最终目的是让 agent 学会完成原始任务。

希望这份指南能帮助你设计和调试有效的 Reward Shaping！
