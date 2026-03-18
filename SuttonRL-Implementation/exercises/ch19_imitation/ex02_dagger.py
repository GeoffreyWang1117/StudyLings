"""
练习: DAgger (Dataset Aggregation)

算法描述:
DAgger通过迭代收集数据解决BC的covariate shift问题。
让专家在学习者遇到的状态上标注，从而覆盖测试时的状态分布。

核心思想:
- BC问题: 训练分布 p_expert(s) ≠ 测试分布 p_π(s)
- DAgger解决: 在π遇到的状态上请专家标注
- 迭代聚合数据集，逐渐覆盖π的状态分布

算法流程:
1. 初始化: D = D_expert (专家演示)
2. 训练策略: π ← BC(D)
3. 执行策略: 收集轨迹 τ ~ π
4. 专家标注: 对τ中的状态，请专家标注动作
5. 聚合数据: D ← D ∪ τ
6. 重复步骤2-5

数学分析:
- BC误差界: ε_T = O(T²ε)  (T时间步，ε单步误差)
- DAgger误差界: ε_T = O(Tε)  (线性而非二次！)

优势:
- 解决covariate shift
- 理论保证更好
- 收敛到近似专家性能

局限:
- 需要专家在线标注（成本高）
- 需要环境交互
- 标注质量依赖专家可用性

在RLHF中的意义:
- 理论基础: 说明为什么需要迭代数据收集
- 实践: RLHF的迭代训练（SFT -> RL -> 新数据 -> 再SFT）

参考: Ross et al. (2011) "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning"
"""

import numpy as np

class DAgger:
    """DAgger算法实现"""
    def __init__(self, state_dim, action_dim, learning_rate=0.001):
        """
        初始化

        Args:
            state_dim: 状态维度
            action_dim: 动作维度
            learning_rate: 学习率
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = learning_rate

        # 策略网络
        self.weights = np.random.randn(state_dim, action_dim) * 0.01
        self.bias = np.zeros(action_dim)

        # 聚合的数据集
        self.aggregated_data = []

    def get_action_probs(self, state):
        """获取动作概率"""
        logits = state @ self.weights + self.bias
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def predict_action(self, state, deterministic=False):
        """预测动作"""
        probs = self.get_action_probs(state)
        if deterministic:
            return np.argmax(probs)
        return np.random.choice(len(probs), p=probs)

    def train_on_data(self, data, epochs=10, batch_size=32):
        """
        在数据上训练

        Args:
            data: [(state, action), ...]
            epochs: 训练轮数
            batch_size: 批大小
        """
        # TODO: 实现训练
        # 提示1: 与BC相同的训练过程
        # 提示2: 在聚合的数据集上训练
        pass  # TODO

    def collect_trajectory(self, env, deterministic=False):
        """
        使用当前策略收集轨迹

        Args:
            env: 环境
            deterministic: 是否确定性策略

        Returns:
            trajectory: [(state, action, reward), ...]
        """
        # TODO: 实现轨迹收集
        # 提示1: 重置环境
        # 提示2: 使用当前策略π决策
        # 提示3: 记录(state, action, reward)
        # 提示4: 执行动作
        pass  # TODO

    def get_expert_labels(self, states, expert_policy):
        """
        获取专家对状态的标注

        Args:
            states: 需要标注的状态列表
            expert_policy: 专家策略函数

        Returns:
            labels: 专家动作列表
        """
        # TODO: 实现专家标注
        # 提示: 对每个state，调用expert_policy获取动作
        pass  # TODO

    def dagger_iteration(self, env, expert_policy, n_trajectories=10):
        """
        DAgger的一次迭代

        Args:
            env: 环境
            expert_policy: 专家策略
            n_trajectories: 收集的轨迹数

        Returns:
            new_data_size: 新增数据量
        """
        # TODO: 实现DAgger迭代
        # 提示1: 使用当前策略π收集轨迹
        new_states = []
        # for _ in range(n_trajectories):
        #     trajectory = self.collect_trajectory(env)
        #     states = [s for s, a, r in trajectory]
        #     new_states.extend(states)

        # 提示2: 请专家标注这些状态
        # expert_actions = self.get_expert_labels(new_states, expert_policy)

        # 提示3: 聚合到数据集
        # for state, action in zip(new_states, expert_actions):
        #     self.aggregated_data.append((state, action))

        # 提示4: 在聚合数据集上重新训练
        # self.train_on_data(self.aggregated_data)

        pass  # TODO

    def train_with_dagger(self, env, expert_policy, initial_data,
                          n_iterations=10, trajectories_per_iter=10):
        """
        完整DAgger训练

        Args:
            env: 环境
            expert_policy: 专家策略
            initial_data: 初始专家数据
            n_iterations: DAgger迭代次数
            trajectories_per_iter: 每次迭代收集的轨迹数

        Returns:
            history: 训练历史
        """
        # TODO: 实现完整DAgger训练
        # 提示1: 初始化数据集
        self.aggregated_data = initial_data.copy()

        # 提示2: 初始训练
        # self.train_on_data(self.aggregated_data)

        history = []

        # 提示3: DAgger迭代
        # for iteration in range(n_iterations):
        #     提示4: 评估当前性能
        #     performance = self.evaluate(env)
        #     history.append(performance)
        #
        #     提示5: DAgger迭代
        #     self.dagger_iteration(env, expert_policy, trajectories_per_iter)
        #
        #     提示6: 输出进度

        pass  # TODO

    def evaluate(self, env, n_episodes=10):
        """评估策略"""
        # TODO: 实现评估
        pass  # TODO


def compare_bc_and_dagger():
    """比较BC和DAgger的性能"""
    print("\n=== BC vs DAgger ===")
    print("\nBehavioral Cloning:")
    print("  数据: 仅使用初始专家演示")
    print("  分布: p_expert(s) - 专家访问的状态")
    print("  问题: π偏离 -> 未见过状态 -> 错误决策 -> 持续偏离")
    print("  误差: O(T²ε) - 二次增长")
    print("\nDAgger:")
    print("  数据: 初始演示 + 迭代收集")
    print("  分布: p_π(s) - 学习者访问的状态")
    print("  解决: π偏离 -> 专家标注 -> 学会纠正 -> 回到正轨")
    print("  误差: O(Tε) - 线性增长")
    print("\n关键insight:")
    print("  BC: 'What should I do in states the expert visits?'")
    print("  DAgger: 'What should I do in states I actually encounter?'")


def visualize_dagger_process():
    """可视化DAgger迭代过程"""
    print("\n=== DAgger迭代过程 ===")
    print("\n第0轮 (初始BC):")
    print("  D_0 = {专家演示}")
    print("  π_0 ← BC(D_0)")
    print("  性能: 60%")
    print("\n第1轮:")
    print("  执行π_0 -> 遇到新状态s_new")
    print("  专家标注: a_expert = expert(s_new)")
    print("  D_1 = D_0 ∪ {(s_new, a_expert)}")
    print("  π_1 ← BC(D_1)")
    print("  性能: 75% ↑")
    print("\n第2轮:")
    print("  执行π_1 -> 遇到更多新状态")
    print("  专家继续标注")
    print("  D_2 = D_1 ∪ {新标注}")
    print("  π_2 ← BC(D_2)")
    print("  性能: 85% ↑")
    print("\n...")
    print("\n第N轮:")
    print("  π_N接近专家性能")
    print("  数据集覆盖π_N的状态分布")


def dagger_in_rlhf():
    """DAgger在RLHF中的体现"""
    print("\n=== DAgger思想在RLHF中 ===")
    print("\n直接应用:")
    print("  1. 初始SFT: 在人类演示数据上BC")
    print("  2. 生成回复: 用π生成新回复")
    print("  3. 人类评估: 对新回复打分/修改")
    print("  4. 聚合数据: 加入训练集")
    print("  5. 重新SFT: 在扩充数据上训练")
    print("\n间接体现:")
    print("  RLHF的迭代性:")
    print("    SFT -> RL -> 收集新数据 -> 再训练")
    print("  奖励模型:")
    print("    用偏好数据训练 -> 相当于'隐式专家'")
    print("\nDAgger vs RLHF:")
    print("  DAgger: 专家标注动作（显式）")
    print("  RLHF: 奖励模型指导（隐式）")
    print("  共同点: 都在学习者分布上收集信号")


# 简单环境
class GridWorld:
    def __init__(self, size=10):
        self.size = size
        self.state_dim = 2  # [x, y]
        self.action_dim = 4  # 上下左右
        self.reset()

    def reset(self):
        self.pos = np.array([0, 0])
        self.goal = np.array([self.size-1, self.size-1])
        return self.pos.copy()

    def step(self, action):
        move = {0: [0, 1], 1: [0, -1], 2: [-1, 0], 3: [1, 0]}
        self.pos += move[action]
        self.pos = np.clip(self.pos, 0, self.size-1)

        dist = np.linalg.norm(self.pos - self.goal)
        reward = -dist
        done = dist < 1.0

        return self.pos.copy(), reward, done


def expert_policy(state, goal=np.array([9, 9])):
    """专家策略: 贪心朝目标"""
    diff = goal - state
    if abs(diff[0]) > abs(diff[1]):
        return 3 if diff[0] > 0 else 2
    else:
        return 0 if diff[1] > 0 else 1


if __name__ == "__main__":
    print("练习: DAgger - Dataset Aggregation")
    print("核心: 迭代收集数据，覆盖学习者的状态分布")
    print("\n算法:")
    print("  1. π ← BC(D_expert)")
    print("  2. 执行π，收集轨迹")
    print("  3. 专家标注新状态")
    print("  4. D ← D ∪ 新数据")
    print("  5. 重复2-4")

    compare_bc_and_dagger()
    visualize_dagger_process()
    dagger_in_rlhf()

    print("\n" + "="*50)
    print("训练示例...")

    env = GridWorld(size=10)

    # 收集初始专家数据
    print("\n收集初始专家数据...")
    # TODO: 实现

    # DAgger训练
    print("\nDAgger迭代训练...")
    # agent = DAgger(state_dim=2, action_dim=4)
    # TODO: 实现

    print("\n2025年相关性: RLHF迭代训练的理论基础")
