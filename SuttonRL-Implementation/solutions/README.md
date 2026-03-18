# Solutions 解答

本目录包含所有练习的完整实现，供参考学习。

## ⚠️ 使用建议

1. **先自己尝试**：在查看解答之前，请先尝试自己实现
2. **理解代码**：不要直接复制，要理解每一行的作用
3. **实验修改**：尝试修改参数、算法细节，观察效果
4. **对比学习**：将你的实现与解答对比，找出差异

## 📁 目录结构

```
solutions/
├── ch02_bandits/          # 第2章：多臂老虎机解答
├── ch04_dp/               # 第4章：动态规划解答
├── ch05_mc/               # 第5章：蒙特卡洛方法解答
├── ch06_td/               # 第6章：TD学习解答
├── ch07_nstep/            # 第7章：n步方法解答
├── ch12_eligibility/      # 第12章：资格迹解答
└── ch13_policy_gradient/  # 第13章：策略梯度解答
```

## 🎯 如何使用解答

### 方法1：直接运行

```bash
# 运行解答代码查看结果
python solutions/ch02_bandits/ex01_epsilon_greedy.py
```

### 方法2：对比学习

```bash
# 使用 diff 工具对比你的实现和解答
diff exercises/ch02_bandits/ex01_epsilon_greedy.py \
     solutions/ch02_bandits/ex01_epsilon_greedy.py
```

### 方法3：学习特定部分

打开解答文件，查找你遇到困难的部分（如 `select_action` 方法），
理解实现思路后，回到练习文件自己实现。

## 💡 学习建议

### 卡住了怎么办？

1. **重读提示**：练习中的提示通常包含关键信息
2. **查看伪代码**：对照伪代码检查你的实现
3. **部分查看解答**：只看你卡住的函数，不要看全部
4. **理解后重写**：看懂解答后，关闭文件，自己重新写一遍

### 完成练习后

1. **对比实现**：比较你的代码和解答的区别
2. **性能对比**：运行你的版本和解答，对比性能
3. **理解优化**：解答可能包含优化技巧，理解它们
4. **尝试改进**：基于解答，尝试进一步优化

## 📚 解答说明

每个解答文件包含：

- ✅ 完整的、可运行的代码
- ✅ 详细的注释说明关键步骤
- ✅ 符合算法规范的实现
- ✅ 通过所有测试的代码

## 🔍 解答特点

### 代码风格
- 遵循 PEP 8 规范
- 清晰的变量命名
- 适当的注释

### 算法实现
- 严格遵循 Sutton & Barto 书中的伪代码
- 使用高效的 NumPy 操作
- 包含必要的数值稳定性处理

### 教学价值
- 关键步骤有详细注释
- 复杂部分有说明
- 展示最佳实践

## 📖 章节索引

### 第2章：Multi-armed Bandits
- `ex01_epsilon_greedy.py` - ε-贪心算法
- `ex02_ucb.py` - UCB 算法
- `ex03_gradient_bandit.py` - 梯度老虎机
- `ex04_optimistic_initial.py` - 乐观初始值

### 第4章：Dynamic Programming
- `ex01_policy_evaluation.py` - 策略评估
- `ex03_value_iteration.py` - 值迭代

### 第5章：Monte Carlo Methods
- `ex01_first_visit_mc.py` - 首次访问 MC
- `ex02_mc_es.py` - MC 探索启动

### 第6章：Temporal-Difference Learning
- `ex02_sarsa.py` - SARSA
- `ex03_q_learning.py` - Q-Learning

### 第7章：n-step Bootstrapping
- `ex01_n_step_td.py` - n步TD预测

### 第12章：Eligibility Traces
- `ex01_td_lambda.py` - TD(λ)

### 第13章：Policy Gradient
- `ex01_reinforce.py` - REINFORCE

## ⚖️ 诚信使用

这些解答是为了帮助你学习，而不是为了让你直接复制。

**请遵守学术诚信**：
- ❌ 不要直接复制粘贴到作业中
- ❌ 不要不理解就使用
- ✅ 用作学习参考
- ✅ 理解后自己实现
- ✅ 在理解的基础上进行修改和实验

## 🤝 贡献

如果你发现解答中的问题或有更好的实现：
1. 提交 Issue 说明问题
2. 或者提交 Pull Request 改进解答

---

祝学习愉快！记住：理解算法比复制代码重要得多。🎓
