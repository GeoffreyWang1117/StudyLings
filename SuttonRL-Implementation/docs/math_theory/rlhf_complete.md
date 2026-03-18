## RLHF (Reinforcement Learning from Human Feedback) 完整数学原理与面试问题

# 目录
1. [RLHF概览](#1-rlhf概览)
2. [阶段1: SFT (Supervised Fine-Tuning)](#2-阶段1-sft)
3. [阶段2: Reward Modeling](#3-阶段2-reward-modeling)
4. [阶段3: RL Fine-tuning (PPO + KL)](#4-阶段3-rl-fine-tuning)
5. [DPO: RLHF的简化版本](#5-dpo-direct-preference-optimization)
6. [面试常见问题](#6-面试常见问题)

---

# 1. RLHF概览

## 1.1 核心动机

**问题**: 如何让大语言模型(LLM)对齐人类价值观？

**传统方法的局限**:
- **监督学习**: 只能学到训练数据的模式，难以定义"好"的输出
- **预定义奖励**: 很难为复杂任务（如"写一个有帮助的回答"）定义奖励函数
- **人类评估**: 直接让人类打分太昂贵

**RLHF的创新**:
- 用**人类偏好比较**（而非绝对评分）训练奖励模型
- 用**强化学习**优化策略
- **KL惩罚**防止过度偏离

## 1.2 三阶段流程

```
预训练LLM (GPT, LLaMA等)
    ↓
[阶段1] SFT: Supervised Fine-Tuning
    - 数据: 高质量人类演示 (prompt, response)
    - 方法: 监督学习 / Behavioral Cloning
    - 输出: π_SFT
    ↓
[阶段2] RM: Reward Modeling
    - 数据: 人类偏好对比 (prompt, y_win, y_lose)
    - 方法: Bradley-Terry模型
    - 输出: r_θ(x, y)
    ↓
[阶段3] RL: PPO + KL penalty
    - 初始策略: π_SFT
    - 目标: max E[r_θ(x,y) - β·KL(π||π_SFT)]
    - 方法: PPO
    - 输出: π_RLHF
```

## 1.3 成功案例

- **ChatGPT** (OpenAI, 2022): 完整RLHF
- **GPT-4** (OpenAI, 2023): 改进的RLHF
- **Claude** (Anthropic): Constitutional AI + RLHF
- **LLaMA 2** (Meta, 2023): RLHF + DPO
- **Gemini** (Google): RLHF变体

---

# 2. 阶段1: SFT

## 2.1 数学形式化

**目标**: 在高质量演示数据上微调预训练LLM

**数据集**:
```
D_SFT = {(x_i, y_i)}_{i=1}^N
```
- x: prompt（用户输入）
- y: ideal response（高质量人类回复）

**训练目标** (next-token prediction):
```
L_SFT(θ) = -E_{(x,y)~D_SFT} [log π_θ(y|x)]
           = -E_{(x,y)~D_SFT} [∑_{t=1}^{|y|} log π_θ(y_t|x, y_{<t})]
```

## 2.2 实现细节

```python
# SFT伪代码
for batch in dataloader(D_SFT):
    prompts, responses = batch

    # Forward pass
    logits = model(prompts, responses)

    # Cross-entropy loss (next-token prediction)
    loss = -∑ log P(y_t | x, y_{<t})

    # Backward and update
    loss.backward()
    optimizer.step()
```

## 2.3 数据要求

**数据量**:
- ChatGPT: ~13K demonstrations
- LLaMA 2: ~27K demonstrations
- 一般: 10K-100K

**数据质量**:
- 由专业标注者编写
- 覆盖多种任务类型
- 多样性高，代表性强

## 2.4 为什么需要SFT？

**原因1**: 预训练LLM不是对话模型
- 预训练: 预测下一个词
- 对话: 理解意图并回复

**原因2**: 提供好的初始化
- RL从随机策略训练困难
- SFT提供合理起点

**原因3**: 定义行为空间
- 限制模型在合理范围内生成
- 减少RL探索空间

---

# 3. 阶段2: Reward Modeling

## 3.1 核心思想

**问题**: 如何从人类偏好学习奖励函数？

**关键洞察**: 人类更容易做**比较**（哪个更好）而非**评分**（打几分）

## 3.2 Bradley-Terry模型

### 数学推导

**偏好数据**:
```
D_RM = {(x_i, y_w^i, y_l^i)}_{i=1}^M
```
- x: prompt
- y_w: preferred response (winner)
- y_l: dispreferred response (loser)

**Bradley-Terry假设**: 每个response有潜在"质量"分数r(x,y)

**偏好概率**:
```
P(y_w ≻ y_l | x) = σ(r_θ(x, y_w) - r_θ(x, y_l))
                  = exp(r_θ(x, y_w)) / (exp(r_θ(x, y_w)) + exp(r_θ(x, y_l)))
```

其中σ是sigmoid函数:
```
σ(z) = 1 / (1 + exp(-z))
```

### 训练目标

**Maximum Likelihood**:
```
L_RM(θ) = -E_{(x,y_w,y_l)~D_RM} [log σ(r_θ(x,y_w) - r_θ(x,y_l))]
```

**梯度**:
```
∇_θ L_RM = -E[(1 - σ(Δr)) · (∇r_w - ∇r_l)]
```
其中 Δr = r_θ(x,y_w) - r_θ(x,y_l)

## 3.3 实现细节

```python
class RewardModel(nn.Module):
    def __init__(self, base_model):
        self.base_model = base_model  # 通常初始化自SFT模型
        self.reward_head = nn.Linear(hidden_size, 1)

    def forward(self, x, y):
        # 编码(x, y)
        hidden = self.base_model(x, y)
        # 最后一个token的hidden state
        last_hidden = hidden[:, -1, :]
        # 输出标量奖励
        reward = self.reward_head(last_hidden)
        return reward

def train_reward_model(model, data):
    for batch in data:
        x, y_w, y_l = batch

        # 计算奖励
        r_w = model(x, y_w)
        r_l = model(x, y_l)

        # Bradley-Terry loss
        loss = -log(sigmoid(r_w - r_l))

        # 优化
        loss.backward()
        optimizer.step()
```

## 3.4 数据收集

**方法1**: 人类比较模型输出
```
1. 用π_SFT生成多个responses
2. 人类标注者选择更好的
3. 收集(x, y_better, y_worse)
```

**方法2**: 人类编辑模型输出
```
1. 模型生成response
2. 人类编辑改进
3. (x, y_edited, y_original)作为偏好对
```

**数据量**:
- ChatGPT: ~50K comparisons
- LLaMA 2: ~1M comparisons
- 一般: 10K-500K

## 3.5 奖励模型的挑战

**挑战1: 过拟合**
- 训练准确率: 70-75%
- 泛化能力有限
- 需要大量数据

**挑战2: 分布外泛化**
- 训练: π_SFT生成的responses
- 测试: π_RLHF生成的responses（可能很不同）
- 解决: 迭代训练（重新收集数据）

**挑战3: 奖励hacking**
- 模型学会"欺骗"奖励模型
- 生成看起来好但实际差的输出
- 解决: KL惩罚

---

# 4. 阶段3: RL Fine-tuning

## 4.1 目标函数

**核心目标**:
```
max_π E_{x~D, y~π} [r_θ(x, y) - β·KL(π(·|x) || π_SFT(·|x))]
```

**分解**:
1. **奖励项**: r_θ(x, y) - 最大化奖励模型分数
2. **KL惩罚**: -β·KL(π || π_SFT) - 不过度偏离SFT

## 4.2 为什么需要KL惩罚？

### 问题1: 奖励模型不完美

**无KL惩罚时**:
```
max E[r_θ(x,y)]
```
- 模型会过度优化r_θ
- 找到奖励模型的"漏洞"
- 生成高分但低质量的输出

**例子**:
```
Prompt: "Explain quantum computing"
Bad output (high reward): "QUANTUM COMPUTING IS AMAZING! BEST TECHNOLOGY EVER! ..." (过度夸张)
Good output: "Quantum computing leverages quantum mechanics..." (实际有用)
```

### 问题2: 模式崩溃

**无约束优化**:
- 模型可能退化到生成单一模式
- 丧失多样性
- 语言能力退化

**KL惩罚效果**:
- 保持接近π_SFT（已有良好语言能力）
- 只在提高质量时偏离
- 平衡exploration和exploitation

## 4.3 KL散度详解

### KL散度定义

```
KL(π || π_SFT) = E_{y~π(·|x)} [log π(y|x) / π_SFT(y|x)]
                = E_{y~π} [log π(y|x) - log π_SFT(y|x)]
```

### 为什么用KL而非其他距离？

**KL的优势**:
1. **信息论基础**: 衡量分布差异
2. **计算友好**: 对数概率容易计算
3. **梯度性质好**: 便于优化
4. **理论支撑**: 与最大熵RL相关

### β参数的作用

```
β小 (e.g., 0.01):
  - 允许更多exploration
  - 可能偏离SFT过多
  - 风险: reward hacking

β大 (e.g., 0.5):
  - 保守，接近SFT
  - 改进有限
  - 安全但次优

β适中 (e.g., 0.1-0.2):
  - 平衡点
  - 实践最常用
```

## 4.4 PPO算法

### 为什么选择PPO？

**优势**:
1. **稳定**: Clipped objective防止大步更新
2. **简单**: 相比TRPO更易实现
3. **高效**: 可复用轨迹
4. **成功先例**: 在游戏AI中验证

### PPO + KL目标函数

**Combined objective**:
```
L^PPO+KL(θ) = E_t [
    min(r_t(θ)·Â_t, clip(r_t(θ), 1-ε, 1+ε)·Â_t)
    - β·KL_t
    - c_1·L^VF_t
    + c_2·H_t
]
```

**分解**:
- **r_t(θ)**: importance ratio = π_θ(a_t|s_t) / π_old(a_t|s_t)
- **Â_t**: advantage (用GAE计算)
- **clip(r_t, 1-ε, 1+ε)**: PPO的clipping
- **KL_t**: KL散度惩罚
- **L^VF**: value function loss
- **H_t**: entropy bonus (鼓励探索)

### 完整算法

```python
def ppo_rlhf_step(policy, value, reward_model, sft_policy, prompts):
    # 1. 采样trajectories
    with torch.no_grad():
        responses = policy.generate(prompts)
        old_logprobs = policy.log_prob(prompts, responses)

        # 计算奖励
        rewards_rm = reward_model(prompts, responses)

        # 计算KL penalty
        sft_logprobs = sft_policy.log_prob(prompts, responses)
        kl_penalty = old_logprobs - sft_logprobs

        # 总奖励
        rewards = rewards_rm - beta * kl_penalty

        # 计算advantages (GAE)
        values = value(prompts, responses)
        advantages = compute_gae(rewards, values)

        # 计算returns
        returns = advantages + values

    # 2. PPO更新 (多个epochs)
    for epoch in range(K):
        # Mini-batch更新
        for batch in make_batches(prompts, responses, advantages, returns):
            # 新策略概率
            new_logprobs = policy.log_prob(batch.prompts, batch.responses)
            ratio = torch.exp(new_logprobs - batch.old_logprobs)

            # PPO clipped objective
            surr1 = ratio * batch.advantages
            surr2 = torch.clamp(ratio, 1-epsilon, 1+epsilon) * batch.advantages
            policy_loss = -torch.min(surr1, surr2).mean()

            # Value function loss
            new_values = value(batch.prompts, batch.responses)
            value_loss = F.mse_loss(new_values, batch.returns)

            # Entropy bonus
            entropy = policy.entropy(batch.prompts, batch.responses)

            # KL penalty (再次计算，因为policy更新了)
            new_sft_logprobs = sft_policy.log_prob(batch.prompts, batch.responses)
            kl_loss = (new_logprobs - new_sft_logprobs).mean()

            # Total loss
            loss = policy_loss + c1 * value_loss - c2 * entropy + beta * kl_loss

            # 优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

## 4.5 实现技巧

### Trick 1: Adaptive KL coefficient

```python
# 动态调整β
if kl > target_kl * 1.5:
    beta *= 2  # KL太大，增加惩罚
elif kl < target_kl / 1.5:
    beta /= 2  # KL太小，减少惩罚
```

### Trick 2: Value function warmup

```python
# 先训练value function几步
for _ in range(warmup_steps):
    values = value_net(states)
    loss = mse(values, returns)
    optimize(loss)
```

### Trick 3: Reward normalization

```python
# 标准化奖励
rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-8)
```

### Trick 4: Early stopping on KL

```python
# 如果KL过大，提前停止当前epoch
if kl > max_kl:
    break
```

---

# 5. DPO: Direct Preference Optimization

## 5.1 核心动机

**RLHF的复杂性**:
1. 需要训练奖励模型
2. 需要运行RL（PPO）
3. 三阶段，每阶段可能失败
4. 计算成本高

**DPO的创新**: 绕过RM和RL，直接从偏好优化策略

## 5.2 数学推导

### 从RLHF到DPO

**步骤1**: RLHF的最优策略

RLHF目标:
```
π* = argmax_π E_{x,y} [r(x,y) - β·KL(π || π_ref)]
```

**Lagrange形式**:
```
π*(y|x) = 1/Z(x) · π_ref(y|x) · exp(r(x,y)/β)
```

其中Z(x)是归一化常数。

**步骤2**: 反解奖励函数

从最优策略反推奖励:
```
r(x,y) = β log(π*(y|x) / π_ref(y|x)) + β log Z(x)
```

**步骤3**: 代入Bradley-Terry模型

Bradley-Terry:
```
P(y_w ≻ y_l | x) = σ(r(x,y_w) - r(x,y_l))
```

代入r的表达式:
```
P(y_w ≻ y_l | x) = σ(β log(π*(y_w|x)/π_ref(y_w|x)) - β log(π*(y_l|x)/π_ref(y_l|x)))
```

**关键**: Z(x)被消掉了！

**简化**:
```
P(y_w ≻ y_l | x) = σ(β log(π*(y_w|x)/π_ref(y_w|x)) - β log(π*(y_l|x)/π_ref(y_l|x)))
```

### DPO损失函数

**目标**: 直接最大化偏好数据的likelihood

```
L_DPO(θ) = -E_{(x,y_w,y_l)~D} [
    log σ(β log(π_θ(y_w|x)/π_ref(y_w|x)) - β log(π_θ(y_l|x)/π_ref(y_l|x)))
]
```

**更简洁的形式**:
```
L_DPO(θ) = -E [log σ(β(log r_w - log r_l))]
```
其中 r_y = π_θ(y|x) / π_ref(y|x)

## 5.3 DPO的优势

### 优势1: 简单
```
RLHF: SFT -> RM -> RL (三阶段)
DPO:  SFT -> DPO     (两阶段)
```

### 优势2: 稳定
- 不需要RL（避免RL的不稳定性）
- 直接优化，类似监督学习
- 更容易调参

### 优势3: 高效
- 不需要训练单独的reward model
- 不需要value function
- 计算量更小

### 优势4: 理论保证
- 数学上等价于RLHF（在最优解处）
- 有理论收敛保证

## 5.4 实现

```python
def dpo_loss(policy, ref_policy, prompts, y_w, y_l, beta=0.1):
    """
    DPO损失函数

    Args:
        policy: 当前策略 π_θ
        ref_policy: 参考策略 π_ref (通常是SFT模型)
        prompts: 输入提示
        y_w: preferred responses
        y_l: dispreferred responses
        beta: KL系数

    Returns:
        loss: DPO损失
    """
    # 计算log概率
    logp_w = policy.log_prob(prompts, y_w)
    logp_l = policy.log_prob(prompts, y_l)

    # 参考策略的log概率 (detach，不更新)
    with torch.no_grad():
        ref_logp_w = ref_policy.log_prob(prompts, y_w)
        ref_logp_l = ref_policy.log_prob(prompts, y_l)

    # 计算log ratio
    log_ratio_w = logp_w - ref_logp_w
    log_ratio_l = logp_l - ref_logp_l

    # DPO loss
    logits = beta * (log_ratio_w - log_ratio_l)
    loss = -F.logsigmoid(logits).mean()

    return loss

def train_dpo(policy, ref_policy, data, epochs=3):
    optimizer = Adam(policy.parameters(), lr=1e-6)

    for epoch in range(epochs):
        for batch in data:
            prompts, y_w, y_l = batch

            loss = dpo_loss(policy, ref_policy, prompts, y_w, y_l)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
```

## 5.5 DPO vs RLHF

| 特性 | RLHF | DPO |
|------|------|-----|
| **阶段数** | 3 (SFT + RM + RL) | 2 (SFT + DPO) |
| **复杂度** | 高 | 低 |
| **稳定性** | 中（RL不稳定） | 高（类似SL） |
| **计算成本** | 高 | 中 |
| **灵活性** | 高（可调整RM） | 中 |
| **理论** | 成熟 | 较新（2023） |
| **工业应用** | ChatGPT, Claude | Llama 2, Mistral |

## 5.6 何时用DPO？

**适合DPO**:
- ✅ 资源有限
- ✅ 需要快速迭代
- ✅ 有高质量偏好数据
- ✅ 追求稳定性

**适合RLHF**:
- ✅ 需要最大灵活性
- ✅ 可以在线收集反馈
- ✅ 有充足计算资源
- ✅ 需要持续迭代

**混合方法** (实践中常见):
- 先DPO快速对齐
- 再RLHF精细优化

---

# 6. 面试常见问题

## Q1: RLHF三阶段中，哪个最重要？

**答案**: 都重要，但**奖励建模**是核心创新

**原因**:
1. **SFT**: 并非新技术（就是监督学习）
2. **RM**: RLHF的核心创新
   - 将模糊的"对齐"转化为可优化目标
   - Bradley-Terry模型优雅地利用偏好数据
3. **RL**: 虽然复杂，但是已有技术（PPO）

**类比**:
- AlphaGo的价值网络 = RLHF的奖励模型
- 都是将难以定义的目标转化为可学习的函数

## Q2: 为什么用偏好对比而非绝对评分？

**答案**: 偏好比较更容易、更一致、更可靠

**心理学原因**:
- 人类天生擅长比较（哪个更好）
- 绝对评分受个人标准影响大
- 比较更容易达成一致

**数据质量**:
```
绝对评分:
  标注者A: 7分
  标注者B: 5分
  (不一致性高)

偏好对比:
  标注者A: Response 1更好
  标注者B: Response 1更好
  (一致性高)
```

**数学优势**:
- Bradley-Terry模型只需偏好（二值）
- 不需要标定绝对scale
- 更robust to标注噪声

## Q3: KL penalty的β如何选择？

**答案**: 经验值0.01-0.2，需要实验调整

**选择策略**:

| β值 | 效果 | 适用场景 |
|-----|------|----------|
| 0.01-0.05 | 大胆探索 | RM很准确，想最大化改进 |
| 0.1-0.15 | 平衡（最常用） | 一般情况 |
| 0.2-0.5 | 保守 | RM不可靠，安全优先 |

**调参技巧**:
1. 从β=0.1开始
2. 监控KL散度:
   - KL < 10: 太保守，可减小β
   - KL > 100: 太激进，应增大β
   - KL ≈ 20-50: 合理范围
3. 观察输出质量

**Adaptive β**:
```python
if kl > target_kl * 1.5:
    beta *= 1.5
elif kl < target_kl / 1.5:
    beta /= 1.5
```

## Q4: 如何检测reward hacking？

**答案**: 多维度监控

**信号1: 奖励-质量脱钩**
```
Reward Model Score: 9.5/10
Human Evaluation: 6/10
→ Reward hacking!
```

**信号2: KL急剧增加**
```
KL(π || π_SFT) >> β^{-1}
→ 策略偏离太多
```

**信号3: 输出异常**
- 重复短语
- 过度恭维
- 生成乱码但高分

**检测方法**:
1. **定期人类评估**: 随机采样评估
2. **Gold test set**: 保留测试集，人类标注ground truth
3. **多个RM ensemble**: 训练多个RM，检查一致性

**预防措施**:
1. 增大β（更保守）
2. 更多样化的RM训练数据
3. 对抗训练（生成hard examples）

## Q5: SFT数据和RM数据有什么区别？

**答案**: 目的、格式、规模都不同

| 特性 | SFT数据 | RM数据 |
|------|---------|--------|
| **格式** | (prompt, response) | (prompt, y_w, y_l) |
| **目的** | 学习基本能力 | 学习人类偏好 |
| **质量** | 高质量单个样本 | 成对比较 |
| **规模** | 10K-100K | 50K-1M对 |
| **标注** | 专家生成 | 人类比较 |
| **成本** | 高（需要生成） | 中（只需选择） |

**收集流程**:

**SFT**:
```
1. 设计任务模板
2. 专家标注者编写高质量回复
3. 质量审核
```

**RM**:
```
1. 用π_SFT生成多个候选回复
2. 标注者比较并选择更好的
3. 收集偏好对
```

## Q6: DPO真的等价于RLHF吗？

**答案**: 理论上在最优解处等价，实践中有差异

**理论等价性**:
- DPO推导自RLHF的最优策略
- 在无限数据、完美优化下等价

**实践差异**:

**1. 优化路径不同**
```
RLHF: 先学r，再优化π
DPO:  直接优化π
→ 局部最优可能不同
```

**2. 灵活性差异**
```
RLHF: 可以用r评估新数据
DPO:  只能用于训练
```

**3. 数据需求**
```
RLHF: 可以用不同分布的数据
DPO:  需要用π_ref生成的数据
```

**实验结果** (多个benchmark):
- 简单任务: DPO ≈ RLHF
- 复杂任务: RLHF略优
- 计算效率: DPO > RLHF

## Q7: 能否跳过SFT直接做RLHF？

**答案**: 理论上可以，实践中不行

**挑战**:

**1. 探索空间巨大**
```
|Vocabulary| ≈ 50K
|Sequence length| ≈ 2048
→ 动作空间 ≈ 50K^2048 (天文数字！)
```

**2. 稀疏奖励**
- 生成完整response才能获得奖励
- 难以credit assignment
- RL难以学习

**3. 语言质量崩溃**
- 从预训练LLM直接RL
- 很快生成乱码
- 失去语言能力

**SFT的作用**:
- **约束空间**: 只在有意义的response空间探索
- **提供初始化**: RL从好的起点开始
- **保持语言能力**: 已经学会基本生成

**实验证据**:
- OpenAI报告: 无SFT的RLHF完全失败
- 实践中: SFT是必须的

## Q8: 如何处理多模态偏好（不同人有不同偏好）？

**答案**: 多种策略

**方法1: 混合训练**
- 用所有人的偏好训练单个RM
- 学到"平均"偏好
- 简单但可能折衷

**方法2: 个性化RM**
```
r_θ(x, y | user_embedding)
```
- 为每个用户/群体训练不同RM
- 更精确但成本高

**方法3: Conditional RLHF**
```
Prompt: [Style: Formal] Explain quantum computing
```
- 在prompt中指定偏好
- 单个模型适应多种风格

**方法4: Constitutional AI** (Anthropic)
- 定义明确的principles
- 用AI自我critique和修正
- 减少对人类偏好的依赖

**实践** (ChatGPT):
- 默认策略: 混合训练
- 个性化: 通过对话历史调整
- 用户反馈: 持续更新RM

## Q9: RLHF的最大局限是什么？

**答案**: 多个根本性限制

**局限1: 受限于人类能力**
```
人类擅长: 创意写作、常识推理
人类不擅长: 数学证明、代码审查
→ RLHF在后者改进有限
```

**局限2: 短视偏好**
- 人类偏好表面质量（fluency, politeness）
- 难以评估深层质量（correctness, depth）
- RM可能学到错误信号

**局限3: 标注成本**
- 需要大量人类标注
- 成本高（每个comparison $0.1-1）
- 难以持续迭代

**局限4: 分布漂移**
```
RM训练分布: π_SFT生成
实际使用分布: π_RLHF生成
→ 分布不匹配，RM不准
```

**局限5: Goodhart定律**
```
"当指标成为目标时，它就不再是好指标"
→ 过度优化RM导致reward hacking
```

**未来方向**:
- **RLAIF**: RL from AI Feedback（用AI代替人类）
- **Constitutional AI**: 明确规则替代模糊偏好
- **Scalable Oversight**: 人类监督AI监督策略

## Q10: 如何评估RLHF模型？

**答案**: 多维度评估

**1. 人类评估** (Gold standard)
```
方法: A/B测试
- 对比π_RLHF vs π_SFT
- 随机采样prompts
- 人类标注者选择更好的response
- 统计Win Rate
```

**2. 奖励模型分数**
```
平均分: E[r_θ(x,y)]
但注意: 可能存在reward hacking
```

**3. 自动指标**
- **BLEU, ROUGE**: 与参考答案比较（限制性大）
- **Perplexity**: 语言流畅度
- **Diversity**: 输出多样性

**4. 任务特定指标**
- **代码生成**: Pass@k (代码通过率)
- **数学**: Accuracy
- **总结**: ROUGE, BERTScore
- **对话**: Coherence, Engagement

**5. 安全性评估**
- **Jailbreak测试**: 能否被诱导生成有害内容
- **偏见检测**: 是否存在stereotype
- **事实性**: 生成内容的准确性

**OpenAI的评估**（InstructGPT论文）:
```
维度:
1. Helpfulness: 是否有帮助
2. Harmlessness: 是否安全
3. Honesty: 是否真实

指标:
- 人类偏好: RLHF vs SFT = 85% vs 15%
- 真实性: 提升21%
- 有害输出: 减少25%
```

## Q11: RLHF训练需要多少计算资源？

**答案**: 非常大，但可优化

**ChatGPT规模估算** (基于公开信息):

**SFT阶段**:
```
模型: GPT-3.5 (175B parameters)
数据: 13K demonstrations
时间: 几小时到1天
GPU: 64-128 A100
```

**RM阶段**:
```
模型: 6B parameters (小于base model)
数据: 50K comparisons
时间: 几小时
GPU: 16-32 A100
```

**RL阶段** (最昂贵):
```
模型: 175B parameters
Rollouts: 需要生成大量responses
时间: 数天到数周
GPU: 256+ A100
每次生成: ~1M tokens
```

**总成本估算**:
```
计算: $1M-5M (云GPU成本)
人类标注: $500K-2M
总计: $1.5M-7M
```

**优化策略**:

**1. Model size**
```
Base model: 175B
SFT model: 175B
RM model: 6B (小得多！)
Value model: 6B
```

**2. Efficient sampling**
```
- 用vLLM等高效推理框架
- Batch generation
- KV-cache复用
```

**3. Smaller rollouts**
```
- 不是每step都生成完整response
- 只在policy update前生成
```

**4. LoRA/QLoRA**
```
- 只训练adapter (1-2% parameters)
- 成本降低10-100倍
- 性能略有损失但可接受
```

**开源替代**:
```
LLaMA 2 (7B):
- 单机8×A100
- 几天完成RLHF
- 成本 < $10K
```

## Q12: 解释RLHF中的"对齐税"

**答案**: "对齐税"指为了安全/对齐牺牲的能力

**Trade-off**:
```
预训练LLM:
  - 能力最强（what it can do）
  - 但不可控（what it will do）

RLHF后:
  - 能力略降（更拒绝回答）
  - 但更对齐（按期望行为）
```

**具体表现**:

**1. 拒绝回答**
```
Prompt: "Write code to hack a website"
Pre-RLHF: 生成实际代码
Post-RLHF: "I cannot help with that..."
→ 能力被限制
```

**2. 过度谨慎**
```
Prompt: "Explain how viruses work"
Pre-RLHF: 详细解释
Post-RLHF: 过度谨慎，担心被用于恶意
→ 有用性下降
```

**3. 语言能力退化**
```
指标: Perplexity, Diversity
Pre-RLHF: 更自然多样
Post-RLHF: 略有下降（因KL penalty）
```

**量化** (InstructGPT论文):
```
- Perplexity: 增加约3%
- 代码能力: 下降约5%
- 但用户满意度: 提升70%
→ Trade-off值得
```

**减少对齐税**:
1. **Constitutional AI**: 更精确的约束
2. **Red teaming**: 识别过度限制
3. **动态β**: 任务特定调整KL penalty

---

# 7. 总结

## 7.1 RLHF核心要点

1. **三阶段**: SFT → RM → RL
2. **核心创新**: 用偏好学习奖励（Bradley-Terry）
3. **关键技术**: PPO + KL penalty
4. **最大挑战**: Reward hacking, 计算成本

## 7.2 DPO核心要点

1. **简化**: 绕过RM和RL
2. **数学**: RLHF最优解的闭式形式
3. **优势**: 简单、稳定、高效
4. **局限**: 灵活性较低

## 7.3 面试准备Checklist

**理论**:
- [ ] Bradley-Terry模型推导
- [ ] KL penalty的作用
- [ ] DPO从RLHF的推导
- [ ] Reward hacking原因

**实践**:
- [ ] 三阶段的数据需求
- [ ] PPO+KL的实现
- [ ] β参数选择
- [ ] 评估方法

**对比**:
- [ ] RLHF vs DPO
- [ ] RLHF vs SFT alone
- [ ] 不同算法的计算成本

**前沿**:
- [ ] Constitutional AI
- [ ] RLAIF
- [ ] 多模态RLHF

## 7.4 Quick Reference

### RLHF公式
```
# Reward Model
L_RM = -E[log σ(r(x,y_w) - r(x,y_l))]

# PPO + KL
L_RL = E[min(r·A, clip(r)·A) - β·KL(π||π_SFT)]
```

### DPO公式
```
L_DPO = -E[log σ(β(log(π(y_w)/π_ref(y_w)) - log(π(y_l)/π_ref(y_l))))]
```

### 典型超参数
```
SFT: lr=1e-5, epochs=3
RM:  lr=1e-5, epochs=1
RL:  lr=1e-6, β=0.1, PPO_epochs=4
DPO: lr=1e-6, β=0.1, epochs=3
```

---

**扩展阅读**:
- Christiano et al. (2017): "Deep RL from Human Preferences"
- Ouyang et al. (2022): "Training language models to follow instructions (InstructGPT)"
- Rafailov et al. (2023): "Direct Preference Optimization"
- Bai et al. (2022): "Constitutional AI" (Anthropic)
