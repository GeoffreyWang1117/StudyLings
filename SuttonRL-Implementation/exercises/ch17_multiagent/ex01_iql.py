"""
练习: IQL (Independent Q-Learning)

算法描述:
IQL是最简单的多智能体RL方法，每个智能体独立学习Q函数，
将其他智能体视为环境的一部分。

核心思想:
- 每个智能体i独立维护Q_i(s,a_i)
- 忽略其他智能体的动作
- 去中心化执行

优势:
- 简单易实现
- 可扩展性好
- 去中心化

局限:
- 非平稳环境（其他智能体在变化）
- 缺乏协调

应用:
- 多机器人协作
- 交通控制
- 分布式系统

参考: Tan (1993) "Multi-agent Reinforcement Learning: Independent vs. Cooperative Agents"
"""

import numpy as np

class MultiAgentEnv:
    """简单的多智能体环境（资源收集）"""
    def __init__(self, n_agents=2, grid_size=5):
        self.n_agents = n_agents
        self.grid_size = grid_size
        self.n_actions = 5  # 上下左右+停留
        self.reset()
    
    def reset(self):
        self.agent_positions = [np.random.randint(0, self.grid_size, 2) for _ in range(self.n_agents)]
        self.resource_pos = np.random.randint(0, self.grid_size, 2)
        return self._get_states()
    
    def _get_states(self):
        # 每个智能体观察：自己位置+资源位置
        return [tuple(np.concatenate([pos, self.resource_pos])) for pos in self.agent_positions]
    
    def step(self, actions):
        """
        执行联合动作
        
        Args:
            actions: [action_1, action_2, ...]
            
        Returns:
            states, rewards, done
        """
        rewards = [0.0] * self.n_agents
        
        # 移动智能体
        for i, action in enumerate(actions):
            if action == 0: self.agent_positions[i][0] = max(0, self.agent_positions[i][0] - 1)  # 上
            elif action == 1: self.agent_positions[i][0] = min(self.grid_size-1, self.agent_positions[i][0] + 1)  # 下
            elif action == 2: self.agent_positions[i][1] = max(0, self.agent_positions[i][1] - 1)  # 左
            elif action == 3: self.agent_positions[i][1] = min(self.grid_size-1, self.agent_positions[i][1] + 1)  # 右
            # action == 4: 停留
        
        # 检查谁到达资源
        for i in range(self.n_agents):
            if np.array_equal(self.agent_positions[i], self.resource_pos):
                rewards[i] = 1.0
        
        # 碰撞惩罚
        for i in range(self.n_agents):
            for j in range(i+1, self.n_agents):
                if np.array_equal(self.agent_positions[i], self.agent_positions[j]):
                    rewards[i] -= 0.5
                    rewards[j] -= 0.5
        
        done = any(r > 0 for r in rewards)
        
        return self._get_states(), rewards, done


def independent_q_learning(env, episodes=1000, alpha=0.1, gamma=0.99, epsilon=0.1):
    """
    Independent Q-Learning
    
    Args:
        env: 多智能体环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子
        epsilon: 探索率
        
    Returns:
        Q_tables: 每个智能体的Q表
    """
    # TODO: 为每个智能体初始化Q表
    # 提示1: Q_tables = [defaultdict(...) for _ in range(env.n_agents)]
    # 提示2: 每个智能体独立学习
    # 提示3: for episode in range(episodes):
    # 提示4:   states = env.reset()
    # 提示5:   每个智能体独立选择动作
    # 提示6:   每个智能体独立更新Q值
    
    pass  # TODO
    
    return None  # TODO: 返回Q_tables


print("练习: 实现IQL - 每个智能体独立Q-learning")
print("核心: 多个独立的Q-learner，将他人视为环境")
