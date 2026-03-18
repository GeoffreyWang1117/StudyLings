"""
练习: Prioritized Experience Replay (PER)

算法描述:
PER根据TD error对经验进行优先级采样，让智能体更多地从"意外"经验中学习。
是DQN的重要改进，在2025年仍是标准配置。

核心思想:
- 根据TD error分配采样优先级
- TD error大的transition更重要
- 使用importance sampling修正偏差

数学公式:
1. 优先级: p_i = |δ_i| + ε  (proportional)
   或: p_i = 1/rank(i)  (rank-based)

2. 采样概率: P(i) = p_i^α / Σ_k p_k^α
   α控制优先级强度: α=0为uniform, α=1为full prioritization

3. Importance Sampling权重:
   w_i = (N · P(i))^{-β} / max_j w_j
   β从β_0退火到1，修正偏差

数据结构:
- SumTree: O(log N)的优先级采样和更新
- 存储(state, action, reward, next_state, done, priority)

优势:
- 加速学习（样本效率↑）
- 关注重要经验
- 在2025年已是DQN标配

参考: Schaul et al. (2016) "Prioritized Experience Replay"
"""

import numpy as np
from collections import deque

class SumTree:
    """
    Sum Tree数据结构，用于高效的优先级采样

    结构:
    - 叶节点存储优先级
    - 父节点存储子节点优先级之和
    - 根节点存储总优先级
    """
    def __init__(self, capacity):
        """
        初始化

        Args:
            capacity: 最大容量
        """
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)  # 存储优先级的完全二叉树
        self.data = np.zeros(capacity, dtype=object)  # 存储实际数据
        self.write = 0  # 当前写指针
        self.n_entries = 0  # 当前存储数量

    def _propagate(self, idx, change):
        """向上传播优先级变化"""
        # TODO: 实现向上传播
        # 提示1: 父节点索引: parent = (idx - 1) // 2
        # 提示2: 更新父节点值: tree[parent] += change
        # 提示3: 递归直到根节点: idx = 0
        pass  # TODO

    def _retrieve(self, idx, s):
        """
        从树中检索数据

        Args:
            idx: 当前节点索引
            s: 目标累积优先级值

        Returns:
            叶节点索引
        """
        # TODO: 实现检索
        # 提示1: 左子节点: left = 2 * idx + 1
        # 提示2: 右子节点: right = left + 1
        # 提示3: 如果s <= tree[left]: 搜索左子树
        # 提示4: 否则: 搜索右子树，s -= tree[left]
        # 提示5: 叶节点条件: left >= len(tree)
        pass  # TODO

    def total(self):
        """返回总优先级"""
        # TODO: 返回根节点值
        pass  # TODO

    def add(self, priority, data):
        """添加新数据"""
        # TODO: 实现添加
        # 提示1: 计算叶节点索引: idx = self.write + self.capacity - 1
        # 提示2: 存储数据: self.data[self.write] = data
        # 提示3: 更新优先级: self.update(idx, priority)
        # 提示4: 更新写指针: self.write = (self.write + 1) % self.capacity
        # 提示5: 更新计数: self.n_entries = min(...)
        pass  # TODO

    def update(self, idx, priority):
        """更新节点优先级"""
        # TODO: 实现更新
        # 提示1: 计算变化: change = priority - self.tree[idx]
        # 提示2: 更新当前节点: self.tree[idx] = priority
        # 提示3: 向上传播: self._propagate(idx, change)
        pass  # TODO

    def get(self, s):
        """
        根据累积优先级采样

        Args:
            s: 采样值 [0, total()]

        Returns:
            (idx, priority, data)
        """
        # TODO: 实现采样
        # 提示1: 检索叶节点: idx = self._retrieve(0, s)
        # 提示2: 计算数据索引: data_idx = idx - self.capacity + 1
        # 提示3: 返回: (idx, self.tree[idx], self.data[data_idx])
        pass  # TODO


class PrioritizedReplayBuffer:
    """优先级经验回放缓冲区"""
    def __init__(self, capacity, alpha=0.6, beta_start=0.4, beta_frames=100000):
        """
        初始化

        Args:
            capacity: 缓冲区容量
            alpha: 优先级指数 (0=uniform, 1=full prioritization)
            beta_start: IS权重初始值
            beta_frames: β退火到1的步数
        """
        self.tree = SumTree(capacity)
        self.capacity = capacity
        self.alpha = alpha
        self.beta_start = beta_start
        self.beta_frames = beta_frames
        self.frame = 1
        self.epsilon = 0.01  # 小常数，避免零优先级

    def _get_priority(self, td_error):
        """从TD error计算优先级"""
        # TODO: 计算优先级
        # 提示: p = (|td_error| + ε)^α
        pass  # TODO

    def add(self, state, action, reward, next_state, done, td_error):
        """添加经验到缓冲区"""
        # TODO: 实现添加
        # 提示1: 计算优先级: priority = self._get_priority(td_error)
        # 提示2: 存储数据: data = (state, action, reward, next_state, done)
        # 提示3: 添加到树: self.tree.add(priority, data)
        pass  # TODO

    def sample(self, batch_size):
        """
        采样一个batch

        Returns:
            batch: 采样的经验
            indices: SumTree中的索引
            weights: IS权重
        """
        # TODO: 实现采样
        # 提示1: 计算当前β: beta = min(1.0, self.beta_start + self.frame * ...)
        # 提示2: 划分区间: segment = self.tree.total() / batch_size
        # 提示3: 对每个区间采样:
        #   - 随机值: s = uniform(segment * i, segment * (i+1))
        #   - 获取经验: idx, priority, data = self.tree.get(s)
        # 提示4: 计算IS权重: w = (N * P(i))^(-β)
        # 提示5: 归一化权重: w /= max(weights)
        pass  # TODO

    def update_priorities(self, indices, td_errors):
        """更新采样经验的优先级"""
        # TODO: 更新优先级
        # 提示: 对每个(idx, td_error):
        #       priority = self._get_priority(td_error)
        #       self.tree.update(idx, priority)
        pass  # TODO


class DQNWithPER:
    """使用PER的DQN"""
    def __init__(self, state_dim, action_dim, buffer_size=10000):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = 0.99
        self.epsilon = 0.1
        self.lr = 0.001

        # Q网络
        self.q_weights = np.random.randn(state_dim, action_dim) * 0.01
        # 目标网络
        self.target_weights = self.q_weights.copy()

        # PER缓冲区
        self.buffer = PrioritizedReplayBuffer(buffer_size)

    def get_q_values(self, state, use_target=False):
        """计算Q值"""
        weights = self.target_weights if use_target else self.q_weights
        return state @ weights

    def select_action(self, state):
        """ε-greedy选择动作"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_dim)
        return np.argmax(self.get_q_values(state))

    def train_step(self, batch_size=32):
        """训练一步"""
        # TODO: 实现训练
        # 提示1: 从PER采样: batch, indices, weights = self.buffer.sample(batch_size)
        # 提示2: 计算TD errors
        # 提示3: 使用IS权重加权loss
        # 提示4: 更新Q网络
        # 提示5: 更新PER优先级: self.buffer.update_priorities(indices, td_errors)
        pass  # TODO

    def update_target_network(self):
        """更新目标网络"""
        self.target_weights = self.q_weights.copy()


def compare_with_uniform_replay():
    """对比PER和uniform replay的性能"""
    # TODO: 实验对比
    # 提示1: 训练两个DQN: 一个用PER，一个用uniform replay
    # 提示2: 记录学习曲线
    # 提示3: 比较样本效率
    pass  # TODO


if __name__ == "__main__":
    print("练习: Prioritized Experience Replay (PER)")
    print("核心: 根据TD error优先采样重要经验")
    print("\n关键公式:")
    print("  优先级: p_i = (|δ_i| + ε)^α")
    print("  采样概率: P(i) = p_i^α / Σ_k p_k^α")
    print("  IS权重: w_i = (N·P(i))^(-β)")
    print("\n参数:")
    print("  α: 控制优先级强度 (0=uniform, 1=full)")
    print("  β: IS修正强度 (从0.4退火到1)")
    print("\n优势:")
    print("  - 提高样本效率")
    print("  - 加速学习")
    print("  - 2025年DQN标配")

    # 测试SumTree
    print("\n=== 测试SumTree ===")
    tree = SumTree(capacity=4)
    # TODO: 添加测试

    print("\n应用: DQN及其变体 (Rainbow DQN等)")
