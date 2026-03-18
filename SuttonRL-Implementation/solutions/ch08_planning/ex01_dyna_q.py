"""
解答: Dyna-Q算法

这是 ex01_dyna_q.py 的完整实现解答
"""

import numpy as np
from collections import defaultdict


class SimpleMaze:
    """简单迷宫环境（同练习）"""

    def __init__(self, height=6, width=9):
        self.height = height
        self.width = width
        self.n_actions = 4
        self.start = (2, 0)
        self.goal = (0, 8)
        self.walls = set()
        for i in range(1, 9):
            self.walls.add((2, i))
        self.reset()

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        row, col = self.state

        if action == 0:  # 上
            new_row, new_col = row - 1, col
        elif action == 1:  # 下
            new_row, new_col = row + 1, col
        elif action == 2:  # 左
            new_row, new_col = row, col - 1
        elif action == 3:  # 右
            new_row, new_col = row, col + 1

        if new_row < 0 or new_row >= self.height or new_col < 0 or new_col >= self.width:
            new_row, new_col = row, col

        if (new_row, new_col) in self.walls:
            new_row, new_col = row, col

        next_state = (new_row, new_col)

        if next_state == self.goal:
            reward = 1
            done = True
        else:
            reward = 0
            done = False

        self.state = next_state
        return next_state, reward, done


class DynaQAgent:
    """Dyna-Q智能体"""

    def __init__(self, n_actions=4, alpha=0.1, gamma=0.95, epsilon=0.1, planning_steps=5):
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.planning_steps = planning_steps

        self.Q = defaultdict(lambda: np.zeros(n_actions))
        self.model = {}
        self.visited_sa = []

    def select_action(self, state):
        """ε-greedy动作选择"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        else:
            return np.argmax(self.Q[state])

    def update_q(self, state, action, reward, next_state):
        """Q-Learning更新"""
        # TD target
        td_target = reward + self.gamma * np.max(self.Q[next_state])

        # TD error
        td_error = td_target - self.Q[state][action]

        # 更新Q值
        self.Q[state][action] += self.alpha * td_error

    def update_model(self, state, action, reward, next_state):
        """更新环境模型"""
        # 存储转移
        self.model[(state, action)] = (reward, next_state)

        # 记录访问过的状态-动作对
        if (state, action) not in self.visited_sa:
            self.visited_sa.append((state, action))

    def planning(self):
        """使用模型进行规划"""
        if len(self.visited_sa) == 0:
            return

        for _ in range(self.planning_steps):
            # 随机选择访问过的状态-动作对
            idx = np.random.randint(len(self.visited_sa))
            state, action = self.visited_sa[idx]

            # 从模型获取模拟经验
            reward, next_state = self.model[(state, action)]

            # 使用模拟经验更新Q值
            self.update_q(state, action, reward, next_state)


def dyna_q(env, agent, episodes=50):
    """运行Dyna-Q算法"""
    steps_per_episode = []

    for episode in range(episodes):
        state = env.reset()
        steps = 0

        while True:
            # 选择动作
            action = agent.select_action(state)

            # 执行动作
            next_state, reward, done = env.step(action)
            steps += 1

            # Direct RL: 从真实经验更新Q
            agent.update_q(state, action, reward, next_state)

            # Model Learning: 更新模型
            agent.update_model(state, action, reward, next_state)

            # Planning: 使用模型规划
            agent.planning()

            state = next_state

            if done:
                break

        steps_per_episode.append(steps)

    return steps_per_episode


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Dyna-Q - 迷宫 [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = SimpleMaze()

    planning_steps_list = [0, 5, 50]

    print(f"\n比较不同规划步数的效果:\n")

    for n in planning_steps_list:
        agent = DynaQAgent(planning_steps=n)
        steps = dyna_q(env, agent, episodes=50)
        avg_steps = np.mean(steps[-10:])
        print(f"规划步数 n={n:2d}: 最后10回合平均步数 = {avg_steps:.1f}")

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

    print(f"\n✅ 解答说明:")
    print(f"  1. update_q(): Q-Learning更新")
    print(f"  2. update_model(): 存储(s,a) -> (r,s')")
    print(f"  3. planning(): 随机采样模拟经验并更新Q")
    print(f"  4. Dyna-Q = Direct RL + Model Learning + Planning")
