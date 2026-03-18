"""
练习: Dyna-Q 算法 (Planning and Learning)

算法描述:
Dyna-Q 整合了直接RL、模型学习和规划。它在每次与环境交互后：
1. 使用直接RL更新值函数（Q-Learning）
2. 更新环境模型
3. 使用模型进行规划（模拟经验）

核心思想:
- Direct RL: 从真实经验学习
- Model Learning: 学习环境动态模型
- Planning: 使用模型生成模拟经验

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: Q(s,a), Model(s,a) 任意值                  │
│                                                    │
│ 循环（对每个回合）:                                │
│   初始化 S                                         │
│                                                    │
│   循环（对回合中的每一步）:                        │
│     A ← ε-greedy(Q(S,·))                           │
│     执行 A, 观察 R, S'                             │
│                                                    │
│     Q(S,A) ← Q(S,A) + α[R + γ max_a Q(S',a) - Q(S,A)]│
│     Model(S,A) ← R, S'  (确定性环境)               │
│                                                    │
│     循环 n 次 (规划步数):                          │
│       S_sim ← 随机已访问状态                       │
│       A_sim ← 随机在S_sim执行过的动作              │
│       R_sim, S'_sim ← Model(S_sim, A_sim)          │
│       Q(S_sim,A_sim) ← Q(S_sim,A_sim) +            │
│            α[R_sim + γ max_a Q(S'_sim,a) - Q(S_sim,A_sim)]│
│                                                    │
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用简单的迷宫环境:
- 状态: (x, y) 位置
- 动作: 上、下、左、右
- 奖励: 到达目标 +1, 其他 0
- 墙壁: 碰撞则停留原地

要求:
- 实现 Dyna-Q 算法
- 实现环境模型学习
- 实现规划（模拟经验）
- 比较不同规划步数 n 的效果

参考: Sutton & Barto 第8章, 第8.2节
"""

import numpy as np
from collections import defaultdict


class SimpleMaze:
    """简单迷宫环境"""

    def __init__(self, height=6, width=9):
        self.height = height
        self.width = width
        self.n_actions = 4  # 上、下、左、右

        # 起点和终点
        self.start = (2, 0)
        self.goal = (0, 8)

        # 墙壁位置
        self.walls = set()
        for i in range(1, 9):
            self.walls.add((2, i))  # 水平墙

        self.reset()

    def reset(self):
        """重置环境"""
        self.state = self.start
        return self.state

    def step(self, action):
        """
        执行动作

        Args:
            action: 0=上, 1=下, 2=左, 3=右

        Returns:
            next_state, reward, done
        """
        row, col = self.state

        # 计算新位置
        if action == 0:  # 上
            new_row, new_col = row - 1, col
        elif action == 1:  # 下
            new_row, new_col = row + 1, col
        elif action == 2:  # 左
            new_row, new_col = row, col - 1
        elif action == 3:  # 右
            new_row, new_col = row, col + 1

        # 检查边界
        if new_row < 0 or new_row >= self.height or new_col < 0 or new_col >= self.width:
            new_row, new_col = row, col  # 撞墙，停留原地

        # 检查墙壁
        if (new_row, new_col) in self.walls:
            new_row, new_col = row, col  # 撞墙，停留原地

        next_state = (new_row, new_col)

        # 奖励和终止
        if next_state == self.goal:
            reward = 1
            done = True
        else:
            reward = 0
            done = False

        self.state = next_state
        return next_state, reward, done


class DynaQAgent:
    """Dyna-Q 智能体"""

    def __init__(self, n_actions=4, alpha=0.1, gamma=0.95, epsilon=0.1, planning_steps=5):
        """
        初始化

        Args:
            n_actions: 动作数量
            alpha: 学习率
            gamma: 折扣因子
            epsilon: 探索概率
            planning_steps: 每次真实交互后的规划步数
        """
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.planning_steps = planning_steps

        # Q值函数
        self.Q = defaultdict(lambda: np.zeros(n_actions))

        # 环境模型: Model(s,a) = (r, s')
        self.model = {}

        # 记录访问过的状态-动作对
        self.visited_sa = []

    def select_action(self, state):
        """ε-greedy 动作选择"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        else:
            return np.argmax(self.Q[state])

    def update_q(self, state, action, reward, next_state):
        """
        Q-Learning 更新

        Args:
            state: 当前状态
            action: 动作
            reward: 奖励
            next_state: 下一状态
        """
        # TODO: 实现 Q-Learning 更新
        # 提示1: 计算 TD target = reward + gamma * max_a Q(next_state, a)
        # 提示2: 计算 TD error = target - Q(state, action)
        # 提示3: 更新 Q(state, action) += alpha * td_error
        # 提示4: 使用 np.max(self.Q[next_state]) 获取最大Q值

        pass  # TODO: 删除这一行，实现Q更新

    def update_model(self, state, action, reward, next_state):
        """
        更新环境模型

        Args:
            state: 当前状态
            action: 动作
            reward: 奖励
            next_state: 下一状态
        """
        # TODO: 实现模型更新
        # 提示1: 存储转移: self.model[(state, action)] = (reward, next_state)
        # 提示2: 记录访问过的状态-动作对（用于规划采样）
        # 提示3: if (state, action) not in self.visited_sa:
        #           self.visited_sa.append((state, action))

        pass  # TODO: 删除这一行，实现模型更新

    def planning(self):
        """
        使用模型进行规划（模拟经验）

        执行 n 次规划步骤，每次：
        1. 随机选择一个访问过的状态-动作对
        2. 使用模型获取模拟的奖励和下一状态
        3. 使用模拟经验更新Q值
        """
        # TODO: 实现规划
        # 提示1: 如果没有访问过任何状态-动作对，直接返回
        # 提示2: for _ in range(self.planning_steps):
        # 提示3:   随机选择: idx = np.random.randint(len(self.visited_sa))
        # 提示4:   state, action = self.visited_sa[idx]
        # 提示5:   从模型获取: reward, next_state = self.model[(state, action)]
        # 提示6:   使用模拟经验更新Q: self.update_q(state, action, reward, next_state)

        pass  # TODO: 删除这一行，实现规划


def dyna_q(env, agent, episodes=50):
    """
    运行 Dyna-Q 算法

    Args:
        env: 环境
        agent: Dyna-Q 智能体
        episodes: 回合数

    Returns:
        steps_per_episode: 每个回合的步数
    """
    steps_per_episode = []

    # TODO: 实现 Dyna-Q 主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   steps = 0
    # 提示4:   while True:
    # 提示5:     action = agent.select_action(state)
    # 提示6:     next_state, reward, done = env.step(action)
    # 提示7:     steps += 1
    # 提示8:
    # 提示9:     # Direct RL: 从真实经验更新Q
    # 提示10:    agent.update_q(state, action, reward, next_state)
    # 提示11:
    # 提示12:    # Model Learning: 更新模型
    # 提示13:    agent.update_model(state, action, reward, next_state)
    # 提示14:
    # 提示15:    # Planning: 使用模型规划
    # 提示16:    agent.planning()
    # 提示17:
    # 提示18:    state = next_state
    # 提示19:
    # 提示20:    if done:
    # 提示21:      break
    # 提示22:
    # 提示23:  steps_per_episode.append(steps)

    pass  # TODO: 删除这一行，实现主循环

    return steps_per_episode


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Dyna-Q - 迷宫")
    print("=" * 60)

    np.random.seed(42)

    env = SimpleMaze()

    # 测试不同的规划步数
    planning_steps_list = [0, 5, 50]

    print(f"\n比较不同规划步数的效果:\n")

    for n in planning_steps_list:
        agent = DynaQAgent(
            n_actions=4,
            alpha=0.1,
            gamma=0.95,
            epsilon=0.1,
            planning_steps=n
        )

        steps = dyna_q(env, agent, episodes=50)

        avg_steps = np.mean(steps[-10:])  # 最后10回合平均
        print(f"规划步数 n={n:2d}: 最后10回合平均步数 = {avg_steps:.1f}")

    # 验证
    # Dyna-Q 应该比纯Q-Learning (n=0) 更快学习
    agent_no_planning = DynaQAgent(planning_steps=0)
    steps_no_planning = dyna_q(env, agent_no_planning, episodes=50)

    agent_with_planning = DynaQAgent(planning_steps=5)
    steps_with_planning = dyna_q(env, agent_with_planning, episodes=50)

    improvement = np.mean(steps_no_planning[-10:]) - np.mean(steps_with_planning[-10:])

    return {
        'converges': improvement > 0,
        'planning_helps': improvement > 0,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - Dyna-Q 整合了学习和规划")
    print(f"  - 规划步数越多，学习越快（但计算代价更高）")
    print(f"  - 模型学习使sample efficiency更高")
    print(f"  - 适用于确定性环境")
