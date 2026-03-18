# 快速参考卡 - 所有新增算法

## 1. SARSA(λ) - Eligibility Traces

**核心公式**:
```
δ_t = R_{t+1} + γQ(S_{t+1}, A_{t+1}) - Q(S_t, A_t)
e_t(s,a) = γλe_{t-1}(s,a) + 1_{S_t=s, A_t=a}
∀(s,a): Q(s,a) ← Q(s,a) + α·δ_t·e_t(s,a)
```

**面试一句话**: "用eligibility traces将TD error传播到所有最近访问的状态-动作对，实现高效credit assignment"

**λ参数**: 0=TD(0), 1=MC, 0.9=最常用

---

## 2. GAE - Generalized Advantage Estimation

**核心公式**:
```
δ_t = r_t + γV(s_{t+1}) - V(s_t)
A_t^GAE = δ_t + (γλ)A_{t+1}^GAE
```

**面试一句话**: "指数加权所有n-step advantages，λ参数平衡偏差-方差，PPO/TRPO标配"

**λ参数**: 0.95最常用

---

## 3. Prioritized Experience Replay

**核心公式**:
```
p_i = (|δ_i| + ε)^α
P(i) = p_i^α / ∑_k p_k^α
w_i = (N·P(i))^{-β} / max_j w_j
```

**面试一句话**: "根据TD error优先采样重要经验，用importance sampling修正偏差，SumTree实现O(log N)"

**参数**: α=0.6 (优先级强度), β=0.4→1 (IS修正)

---

## 4. Behavioral Cloning

**核心公式**:
```
L(θ) = -E_{(s,a)~D}[log π_θ(a|s)]
```

**面试一句话**: "监督学习模仿专家，简单但有covariate shift问题（误差O(T²)），是RLHF的SFT基础"

**问题**: 训练分布 ≠ 测试分布

---

## 5. DAgger - Dataset Aggregation

**核心算法**:
```
1. π ← BC(D)
2. 执行π，收集状态
3. 专家标注这些状态
4. D ← D ∪ 新数据
5. 重复2-4
```

**面试一句话**: "迭代收集学习者遇到的状态让专家标注，解决BC的covariate shift，误差降到O(T)"

---

## 6. GAIL - Generative Adversarial Imitation Learning

**核心公式**:
```
max_D E_expert[log D(s,a)] + E_π[log(1-D(s,a))]
min_π E_π[-log D(s,a)] - λH(π)
```

**面试一句话**: "用GAN思想做模仿学习，判别器区分专家vs学习者，策略骗过判别器，不需要显式奖励"

---

## 7. MaxEnt IRL - Maximum Entropy Inverse RL

**核心公式**:
```
π*(y|x) ∝ exp(r(x,y)/β)
∇_θ r = E_expert[φ] - E_π[φ]  (特征匹配)
```

**面试一句话**: "假设专家遵循最大熵策略，通过特征匹配从演示恢复奖励函数，RLHF奖励建模的理论基础"

---

## 8. CQL - Conservative Q-Learning

**核心公式**:
```
L = α·E[LSE_a Q(s,a) - Q(s,a_data)] + L_Bellman
LSE = log ∑_a exp(Q(s,a))
```

**面试一句话**: "离线RL，惩罚OOD动作的Q值，保守估计，RLHF本质是离线RL，KL penalty类似CQL思想"

**参数**: α=1.0 (保守性系数)

---

## 9. Reward Modeling (RLHF阶段2)

**核心公式**:
```
P(y_w > y_l | x) = σ(r(x,y_w) - r(x,y_l))
L = -E[log σ(r(x,y_w) - r(x,y_l))]
```

**面试一句话**: "Bradley-Terry模型从人类偏好对比学习奖励函数，ChatGPT等LLM对齐的核心创新"

---

## 10. PPO + KL Penalty (RLHF阶段3)

**核心公式**:
```
max_π E[r(x,y) - β·KL(π||π_SFT)]
KL = E_y[log π(y|x) - log π_SFT(y|x)]
```

**面试一句话**: "用PPO优化策略，KL penalty防止过度偏离SFT（避免reward hacking和模式崩溃）"

**参数**: β=0.1-0.2

---

## 11. DPO - Direct Preference Optimization

**核心公式**:
```
L = -E[log σ(β(log π(y_w)/π_ref(y_w) - log π(y_l)/π_ref(y_l)))]
```

**面试一句话**: "RLHF的闭式解，直接从偏好优化策略，绕过RM和RL，更简单稳定，2023新方法"

**参数**: β=0.1

---

## 面试记忆口诀

### RLHF完整流程
```
SFT (BC) → RM (Bradley-Terry) → RL (PPO+KL) → Aligned LLM
或: SFT → DPO → Aligned LLM (简化版)
```

### 算法关系
```
Eligibility Traces (SARSA) ≈ GAE (Policy Gradient)
Behavioral Cloning (IL) ≈ SFT (RLHF)
MaxEnt IRL理论 → Reward Modeling实践
CQL保守性 ≈ KL penalty保守性
DPO = RLHF最优解的闭式形式
```

### 参数选择
```
SARSA: λ=0.9
GAE: λ=0.95
PER: α=0.6, β=0.4→1
RLHF: β=0.1-0.2
DPO: β=0.1
```

### 核心对比
```
TD vs MC: 偏差-方差
BC vs DAgger: O(T²) vs O(T)
RLHF vs DPO: 灵活 vs 简单
On-policy vs Off-policy: SARSA vs Q-learning
```

---

## 1分钟Pitch（每个算法）

**面试官: "快速讲讲XXX"**

### SARSA(λ)
"SARSA的改进版本，使用eligibility traces记录访问历史。当获得TD error时，不只更新当前状态-动作对，而是更新所有有trace的状态-动作对，权重按γλ指数衰减。λ=0就是普通SARSA，λ=1就是Monte Carlo，实践中λ=0.9最常用。这样做的好处是更快的credit assignment，收敛速度比SARSA快很多。"

### GAE
"PPO和TRPO用来计算advantage的标准方法。核心思想是对不同n-step advantages做指数加权平均，λ参数控制偏差-方差权衡。实现时用反向递归：A_t = δ_t + γλA_{t+1}，从episode末尾往前算。λ=0.95是最常用值。这是现代policy gradient算法的必备组件，显著提升样本效率和训练稳定性。"

### PER
"DQN的重要改进，不再均匀采样，而是根据TD error优先采样'意外'的经验。用SumTree数据结构实现O(log N)采样，用importance sampling修正off-policy偏差。α控制优先级强度，β从0.4退火到1修正偏差。现在是DQN系列算法的标配，Rainbow DQN的核心组件之一。"

### Behavioral Cloning
"最简单的模仿学习方法，就是监督学习。给定专家演示(s,a)，训练策略最大化log π(a|s)。优点是简单快速，缺点是有covariate shift问题：训练时看到专家的状态，测试时遇到自己的状态，分布不匹配导致误差累积O(T²)。这是RLHF第一阶段SFT的理论基础。"

### DAgger
"解决BC的covariate shift的方法。不只用初始专家数据，而是迭代：用当前策略执行，收集遇到的新状态，请专家标注，加入数据集，重新训练。这样数据分布逐渐覆盖学习者的分布，误差从O(T²)降到O(T)。体现了RLHF迭代训练的思想。"

### GAIL
"用GAN思想做模仿学习。训练一个判别器区分专家和学习者的(s,a)，策略作为生成器试图骗过判别器。优点是不需要显式奖励函数，可以从未标注轨迹学习。数学上等价于IRL+RL，但实现更简单。"

### MaxEnt IRL
"逆强化学习的一种，假设专家遵循最大熵策略。目标是从演示恢复奖励函数，通过特征匹配：让学习者的特征期望等于专家的。是RLHF奖励建模的理论基础：都是从行为/偏好中学习奖励。"

### CQL
"离线强化学习的SOTA方法。核心思想是保守：惩罚OOD（训练数据外）动作的Q值。通过最小化log-sum-exp所有动作的Q值，同时最大化数据内动作的Q值。RLHF本质是离线RL，KL penalty类似CQL的保守性思想。"

### RLHF完整
"三阶段训练对齐LLM。第一阶段SFT：监督学习on人类演示，学基本能力。第二阶段RM：用Bradley-Terry模型从人类偏好对比学习奖励函数。第三阶段RL：用PPO优化策略，KL penalty防止过度偏离SFT。ChatGPT、Claude等都用这个流程。"

### DPO
"2023年提出的RLHF简化版本。数学上推导出RLHF最优策略的闭式解，发现可以直接从偏好数据优化策略，不需要训练奖励模型和运行RL。更简单、更稳定、更高效。LLaMA 2、Mistral等开源模型大量采用。"

---

## 高频追问应对

### "为什么RLHF需要KL penalty?"
"三个原因：1)奖励模型不完美，过度优化会exploit漏洞（reward hacking）；2)防止模式崩溃，保持多样性；3)保持语言能力，SFT已经学到好的语言模型。β控制偏离程度，一般0.1-0.2。"

### "DPO真的等价于RLHF吗?"
"理论上在最优解处等价，实践中有差异。DPO推导自RLHF的最优策略闭式解，数学上严格。但优化路径不同：RLHF先学r再优化π，DPO直接优化π。实验表明简单任务DPO≈RLHF，复杂任务RLHF略优，但DPO效率更高。"

### "GAE为什么要反向计算?"
"因为递归关系A_t = δ_t + γλA_{t+1}，A_t依赖于A_{t+1}，必须从后往前算。前向算的话A_{t+1}还没计算出来，无法用。实现时维护last_advantage，从T-1遍历到0。"

### "如何检测reward hacking?"
"多个信号：1)奖励模型分数高但人类评估差；2)KL散度急剧增加；3)输出异常（重复、乱码、过度恭维）。预防方法：增大β更保守，多样化RM训练数据，定期人类评估，Gold test set监控。"

### "能跳过SFT直接做RLHF吗?"
"理论上可以，实践不行。探索空间太大（50K^2048），稀疏奖励难以学习，语言能力会崩溃。SFT的作用：1)约束探索空间在有意义的response；2)提供好的初始化；3)保持基本语言能力。OpenAI报告无SFT的RLHF完全失败。"

---

希望这份快速参考能帮助你快速复习和面试准备！
