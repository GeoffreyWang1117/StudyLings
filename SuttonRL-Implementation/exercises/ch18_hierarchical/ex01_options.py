"""
练习: Options Framework

算法描述:
Options是时间扩展动作的形式化框架，允许智能体学习和使用高层技能。
这是分层强化学习的基础理论。

核心思想:
- Option o = (I, π, β)
  * I: 初始集合（何时可用）
  * π: 子策略（如何执行）
  * β: 终止条件（何时结束）
- Semi-MDP: 在option层面决策
- 时间抽象: 一个option可执行多步

优势:
- 学习可复用技能
- 时间抽象加速学习
- 更好的探索

应用:
- 机器人技能学习
- 层次化任务分解
- 迁移学习

参考: Sutton et al. (1999) "Between MDPs and semi-MDPs: A framework for temporal abstraction"
"""

import numpy as np

class Option:
    """Option: (Initiation, Policy, Termination)"""
    def __init__(self, name, initiation_set, policy, termination):
        """
        初始化Option
        
        Args:
            name: Option名称
            initiation_set: 可初始化的状态集合
            policy: 子策略 π(a|s)
            termination: 终止函数 β(s) -> [0,1]
        """
        self.name = name
        self.initiation_set = initiation_set
        self.policy = policy
        self.termination = termination
    
    def can_initiate(self, state):
        """检查是否可以在state初始化"""
        return state in self.initiation_set
    
    def select_action(self, state):
        """根据子策略选择动作"""
        return self.policy(state)
    
    def should_terminate(self, state):
        """检查是否应该终止"""
        return np.random.random() < self.termination(state)


class OptionsQLearning:
    """使用Options的Q-learning"""
    def __init__(self, n_states, options):
        """
        初始化
        
        Args:
            n_states: 状态数
            options: 可用的Options列表
        """
        self.n_states = n_states
        self.options = options
        # Q(s, o): 在状态s执行option o的价值
        self.Q = np.zeros((n_states, len(options)))
    
    def select_option(self, state, epsilon=0.1):
        """选择一个option"""
        # TODO: ε-greedy选择option
        # 提示1: 过滤可用options
        # 提示2: available = [i for i, opt in enumerate(self.options) if opt.can_initiate(state)]
        # 提示3: ε-greedy选择
        pass  # TODO
    
    def execute_option(self, env, state, option):
        """
        执行一个option直到终止
        
        Returns:
            total_reward: 累积奖励
            final_state: 终止状态
            steps: 执行步数
        """
        # TODO: 执行option
        # 提示1: 初始化累积奖励和步数
        # 提示2: while not option.should_terminate(state):
        # 提示3:   action = option.select_action(state)
        # 提示4:   next_state, reward, done = env.step(action)
        # 提示5:   累积奖励和步数
        # 提示6:   if done: break
        pass  # TODO
    
    def update(self, state, option_idx, reward, next_state, gamma=0.99):
        """更新Q值（SMDP Q-learning）"""
        # TODO: SMDP Q-learning更新
        # 提示: Q(s,o) ← Q(s,o) + α[r + γ^k max_o' Q(s',o') - Q(s,o)]
        # 其中k是option执行的步数
        pass  # TODO


def create_navigation_options(grid_size=5):
    """创建导航options"""
    # 示例：创建4个方向的options
    def go_north_policy(state):
        return 0  # 向上
    
    def go_south_policy(state):
        return 1  # 向下
    
    # TODO: 定义更复杂的options
    # 例如：go_to_corner, explore_room等
    
    options = [
        Option("go_north", set(range(grid_size * grid_size)), 
               go_north_policy, lambda s: np.random.random() < 0.1),
        Option("go_south", set(range(grid_size * grid_size)), 
               go_south_policy, lambda s: np.random.random() < 0.1),
    ]
    
    return options


print("练习: 实现Options框架")
print("核心: Option = (I, π, β), SMDP Q-learning")
print("效果: 学习高层技能，时间抽象")
