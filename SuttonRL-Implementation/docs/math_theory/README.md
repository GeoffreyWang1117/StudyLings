# 数学理论与面试指南

本目录包含所有新增算法的详细数学推导、理论分析和面试常见问题。

## 📚 文档列表

### 经典RL补全

1. **[SARSA(λ)](./sarsa_lambda.md)** - Eligibility Traces
   - TD(λ)的control版本
   - Forward/Backward view等价性
   - 面试高频：λ参数选择，与Q-learning区别

2. **[GAE (Generalized Advantage Estimation)](./gae.md)** - PPO/TRPO标配
   - 偏差-方差权衡
   - 与TD(λ)的联系
   - 面试高频：反向计算原因，在PPO中应用

3. **[Prioritized Experience Replay](./prioritized_replay.md)** - DQN改进
   - SumTree数据结构
   - Importance sampling修正
   - 面试高频：α/β参数作用，Rainbow DQN

### Pre-RLHF算法

4. **[Behavioral Cloning](./behavioral_cloning.md)** - 模仿学习基础
   - Covariate shift问题
   - RLHF的SFT阶段理论
   - 面试高频：与RL区别，误差累积O(T²)

5. **[DAgger](./dagger.md)** - 迭代数据聚合
   - 解决BC的covariate shift
   - 误差从O(T²)降到O(T)
   - 面试高频：与BC对比，在RLHF中的体现

6. **[GAIL](./gail.md)** - 对抗式模仿学习
   - GAN思想应用
   - 隐式奖励学习
   - 面试高频：与BC/IRL对比，判别器设计

7. **[MaxEnt IRL](./maxent_irl.md)** - 逆强化学习
   - 从演示恢复奖励
   - 特征匹配
   - 面试高频：RLHF奖励建模理论基础

8. **[CQL (Conservative Q-Learning)](./cql.md)** - 离线RL
   - OOD动作惩罚
   - LSE正则化
   - 面试高频：RLHF是离线RL，KL penalty类比

### RLHF核心

9. **[RLHF完整指南](./rlhf_complete.md)** ⭐ 最重要！
   - SFT: Supervised Fine-Tuning
   - Reward Modeling: Bradley-Terry模型
   - PPO + KL Penalty: 策略优化
   - DPO: Direct Preference Optimization
   - 面试高频：三阶段详解，KL penalty原因，DPO推导

## 📖 阅读建议

### 快速上手路径 (2-3小时)
```
1. RLHF完整指南 (1.5小时) - 最重要！
2. GAE (30分钟) - 理解PPO
3. Behavioral Cloning (30分钟) - 理解SFT
```

### 系统学习路径 (1周)
```
Day 1: SARSA(λ) + GAE
       └─ 理解eligibility traces和advantage estimation

Day 2: Behavioral Cloning + DAgger
       └─ 模仿学习基础

Day 3: MaxEnt IRL + CQL
       └─ 理解奖励学习和离线RL

Day 4-5: RLHF完整指南
       └─ 核心重点，详细学习

Day 6: GAIL + Prioritized Replay
       └─ 高级技术补充

Day 7: 复习 + 面试题演练
```

### 面试冲刺路径 (1天)
```
上午 (4小时):
  - RLHF完整指南 (重点：所有Q&A)
  - GAE (重点：Q1-Q9)

下午 (4小时):
  - 每个算法的"面试常见问题"部分
  - 练习手推公式
  - 整理答题框架
```

## 🎯 面试高频题型

### 理论推导类
1. **Bradley-Terry模型推导** (必考！)
2. **DPO从RLHF的推导** (高频)
3. **GAE的偏差-方差权衡** (高频)
4. **Eligibility traces的forward/backward view**

### 概念对比类
1. **RLHF vs DPO** (必考！)
2. **SARSA(λ) vs TD(λ) vs GAE**
3. **BC vs DAgger vs GAIL**
4. **On-policy vs Off-policy在RLHF中**

### 实践问题类
1. **KL penalty的β如何选择？** (必考！)
2. **如何检测reward hacking？**
3. **GAE的λ如何选择？**
4. **SFT和RM数据有何区别？**

### 系统设计类
1. **设计一个RLHF系统**
2. **如何评估RLHF模型？**
3. **计算资源估算**
4. **处理多模态偏好**

## 💡 学习技巧

### 1. 理解公式而非死记
```python
# 坏: 死记
"GAE = sum (gamma * lambda)^l delta_{t+l}"

# 好: 理解
"GAE是不同n-step advantages的指数加权平均
 - lambda=0: 只看一步 (TD)
 - lambda=1: 看完整轨迹 (MC)
 - lambda∈(0,1): 权衡偏差-方差"
```

### 2. 画图辅助理解
```
RLHF流程图:
预训练 → SFT → RM → RL → 对齐模型
        ↓     ↓    ↓
      13K   50K  大量
    demos  pairs GPU

DPO流程图:
预训练 → SFT → DPO → 对齐模型
        ↓     ↓
      13K   50K
    demos  pairs
```

### 3. 代码实现加深印象
- 核心算法用Python手写一遍
- 特别是：GAE计算、Bradley-Terry loss、DPO loss
- 调试过程能发现很多细节

### 4. 关联记忆
```
相似技术类比:
- Eligibility traces (SARSA) ≈ GAE (Policy Gradient)
- KL penalty (RLHF) ≈ CQL penalty (Offline RL)
- BC (Imitation Learning) ≈ SFT (RLHF)
```

## 🔧 面试答题框架

### 解释一个算法的框架
```
1. 背景与动机
   "这个算法解决什么问题？"

2. 核心思想（1-2句话）
   "核心idea是什么？"

3. 数学形式化
   "主要公式是什么？"

4. 与其他方法对比
   "相比XX有什么优势？"

5. 实际应用
   "在哪些地方用到？"
```

### 示例：解释RLHF
```
面试官: "请解释RLHF"

回答框架:
1. 背景: "LLM预训练后不对齐人类价值观，需要对齐"

2. 核心: "RLHF用三阶段实现对齐：
   - SFT学习基本能力
   - RM从人类偏好学习奖励
   - RL用PPO+KL优化策略"

3. 数学: "核心是Bradley-Terry模型：
   P(y_w > y_l) = σ(r(y_w) - r(y_l))
   和KL惩罚：max E[r(x,y) - β·KL(π||π_SFT)]"

4. 对比: "相比纯SFT，RLHF能超越演示数据；
   相比DPO，RLHF更灵活但更复杂"

5. 应用: "ChatGPT、Claude等所有对齐LLM都用RLHF"

(如果面试官追问，再深入某个点)
```

## 📊 知识图谱

```
RL基础
├─ Value-Based
│  ├─ Q-learning
│  ├─ DQN
│  └─ Prioritized Replay ← 本项目新增
│
├─ Policy Gradient
│  ├─ REINFORCE
│  ├─ A2C
│  ├─ PPO
│  └─ GAE ← 本项目新增
│
└─ Actor-Critic
   ├─ TD(λ)
   └─ SARSA(λ) ← 本项目新增

模仿学习
├─ Behavioral Cloning ← 本项目新增
├─ DAgger ← 本项目新增
└─ GAIL ← 本项目新增

高级理论
├─ Inverse RL
│  └─ MaxEnt IRL ← 本项目新增
│
└─ Offline RL
   └─ CQL ← 本项目新增

RLHF ⭐
├─ SFT (← Behavioral Cloning)
├─ Reward Modeling (← Inverse RL理论)
├─ PPO + KL (← Offline RL保守性)
└─ DPO (← RLHF简化版)
    └─ 本项目新增完整讲解
```

## 🌟 重点标记

### 必看 (⭐⭐⭐)
- **RLHF完整指南**: ChatGPT训练方法，必须精通
- **GAE**: 现代policy gradient必备
- **Behavioral Cloning**: RLHF的SFT基础

### 重要 (⭐⭐)
- **SARSA(λ)**: 理解eligibility traces
- **DPO**: 2023新方法，快速流行
- **CQL**: 理解离线RL和RLHF联系

### 补充 (⭐)
- **DAgger**: BC的改进
- **MaxEnt IRL**: 奖励学习理论
- **GAIL**: 对抗式模仿学习
- **Prioritized Replay**: DQN改进

## 📝 复习Checklist

### RLHF核心 (必须全部掌握)
- [ ] 能解释RLHF三阶段
- [ ] 能推导Bradley-Terry模型
- [ ] 能解释KL penalty的作用
- [ ] 能推导DPO从RLHF
- [ ] 能说出ChatGPT用的RLHF细节
- [ ] 能回答10个RLHF面试题

### GAE (PPO基础)
- [ ] 能推导GAE公式
- [ ] 能解释λ参数作用
- [ ] 能实现GAE计算（反向递归）
- [ ] 能对比GAE vs TD(λ)
- [ ] 能回答5个GAE面试题

### 其他算法
- [ ] SARSA(λ): eligibility traces概念
- [ ] BC: covariate shift问题
- [ ] CQL: 离线RL与RLHF联系

## 🚀 面试准备Timeline

### 1周前
- 通读所有文档
- 理解所有数学推导
- 手写核心算法实现

### 3天前
- 重点复习RLHF和GAE
- 练习手推公式
- 模拟面试问答

### 1天前
- 复习面试题答案
- 整理答题框架
- 准备追问应对

### 面试当天
- 快速过一遍核心公式
- 放松心态，逻辑清晰
- 不确定的诚实说明

## 📚 扩展资源

### 论文
- **RLHF**: Ouyang et al. (2022) "Training language models to follow instructions"
- **DPO**: Rafailov et al. (2023) "Direct Preference Optimization"
- **GAE**: Schulman et al. (2016) "High-Dimensional Continuous Control Using GAE"

### 博客
- **OpenAI Blog**: InstructGPT解释
- **Anthropic Blog**: Constitutional AI
- **Hugging Face**: RLHF tutorial

### 视频
- **Andrej Karpathy**: State of GPT (YouTube)
- **Nathan Lambert**: RLHF讲解
- **Yannic Kilcher**: 论文解读

## 💬 反馈与贡献

如果发现任何错误或有改进建议，欢迎提Issue或PR！

---

**祝您面试顺利！** 🎉

记住：理解 > 记忆，实践 > 理论，逻辑 > 细节
