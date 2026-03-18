"""
Exercise information and metadata
"""

EXERCISE_LIST = [
    # ========== Chapter 2: Multi-armed Bandits ==========
    {
        'id': 'ch02_ex01_epsilon_greedy',
        'chapter': 'ch02',
        'chapter_name': '第2章: Multi-armed Bandits (多臂老虎机)',
        'name': 'ε-贪心算法 (ε-Greedy)',
        'path': 'ch02_bandits/ex01_epsilon_greedy.py',
        'difficulty': 'easy',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 2, Section 2.3',
        'hints': [
            '以概率 ε 随机选择动作，以概率 1-ε 选择当前最优动作',
            '使用增量式更新：Q(a) = Q(a) + α[R - Q(a)]',
            '初始值可以设为0，步长 α 可以使用 1/n',
        ],
        'learning_points': [
            '理解探索与利用的权衡 (Exploration vs. Exploitation)',
            '掌握增量式更新公式',
            '了解 ε 参数对性能的影响',
        ],
    },
    {
        'id': 'ch02_ex02_ucb',
        'chapter': 'ch02',
        'chapter_name': '第2章: Multi-armed Bandits',
        'name': 'UCB算法 (Upper-Confidence-Bound)',
        'path': 'ch02_bandits/ex02_ucb.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 2, Section 2.7',
        'hints': [
            '选择动作 a = argmax[Q(a) + c*sqrt(ln(t)/N(a))]',
            '探索奖励项随时间衰减，平衡探索与利用',
            '注意处理 N(a)=0 的情况（优先选择未尝试的动作）',
        ],
        'learning_points': [
            '理解置信上界的概念',
            '掌握确定性探索策略',
            '了解 UCB 相比 ε-贪心的优势',
        ],
    },
    {
        'id': 'ch02_ex03_gradient_bandit',
        'chapter': 'ch02',
        'chapter_name': '第2章: Multi-armed Bandits',
        'name': '梯度老虎机算法 (Gradient Bandit)',
        'path': 'ch02_bandits/ex03_gradient_bandit.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 2, Section 2.8',
        'hints': [
            '维护偏好值 H(a)，不是动作值',
            '使用 softmax 将偏好转换为概率：π(a) = exp(H(a))/Σexp(H(b))',
            '更新规则：H(a) = H(a) + α(R - R̄)(1 - π(a)) 对选择的动作',
        ],
        'learning_points': [
            '理解基于梯度的方法',
            '掌握 softmax 动作选择',
            '理解基线 (baseline) 的作用',
        ],
    },
    {
        'id': 'ch02_ex04_optimistic_initial',
        'chapter': 'ch02',
        'chapter_name': '第2章: Multi-armed Bandits',
        'name': '乐观初始值 (Optimistic Initial Values)',
        'path': 'ch02_bandits/ex04_optimistic_initial.py',
        'difficulty': 'easy',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 2, Section 2.6',
        'hints': [
            '将初始动作值设置得很高（如 +5）',
            '结合贪心策略，agent 会因失望而自然探索',
            '观察早期的探索行为',
        ],
        'learning_points': [
            '理解初始值对探索的影响',
            '掌握鼓励探索的简单技巧',
            '了解方法的局限性（只在开始时有效）',
        ],
    },

    # ========== Chapter 4: Dynamic Programming ==========
    {
        'id': 'ch04_ex01_policy_evaluation',
        'chapter': 'ch04',
        'chapter_name': '第4章: Dynamic Programming (动态规划)',
        'name': '策略评估 (Policy Evaluation)',
        'path': 'ch04_dp/ex01_policy_evaluation.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 4, Section 4.1',
        'hints': [
            '迭代应用 Bellman 期望方程',
            'V(s) = Σ_a π(a|s) Σ_{s\',r} p(s\',r|s,a)[r + γV(s\')]',
            '使用两个数组：当前值函数和新值函数',
            '当最大变化 < θ 时停止',
        ],
        'learning_points': [
            '理解 Bellman 期望方程',
            '掌握迭代式策略评估',
            '理解收敛条件',
        ],
    },
    {
        'id': 'ch04_ex02_policy_iteration',
        'chapter': 'ch04',
        'chapter_name': '第4章: Dynamic Programming',
        'name': '策略迭代 (Policy Iteration)',
        'path': 'ch04_dp/ex02_policy_iteration.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 4, Section 4.3',
        'hints': [
            '交替进行策略评估和策略改进',
            '策略改进：π(s) = argmax_a Σ_{s\',r} p(s\',r|s,a)[r + γV(s\')]',
            '当策略不再变化时停止',
        ],
        'learning_points': [
            '理解策略迭代的两步循环',
            '掌握贪心策略改进',
            '理解为何算法会收敛到最优策略',
        ],
    },
    {
        'id': 'ch04_ex03_value_iteration',
        'chapter': 'ch04',
        'chapter_name': '第4章: Dynamic Programming',
        'name': '值迭代 (Value Iteration)',
        'path': 'ch04_dp/ex03_value_iteration.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 4, Section 4.4',
        'hints': [
            '结合策略评估和改进为一步',
            'V(s) = max_a Σ_{s\',r} p(s\',r|s,a)[r + γV(s\')]',
            '直接更新值函数，最后提取策略',
        ],
        'learning_points': [
            '理解 Bellman 最优方程',
            '掌握值迭代算法',
            '理解与策略迭代的关系',
        ],
    },
    {
        'id': 'ch04_ex04_gamblers_problem',
        'chapter': 'ch04',
        'chapter_name': '第4章: Dynamic Programming',
        'name': '赌徒问题 (Gambler\'s Problem)',
        'path': 'ch04_dp/ex04_gamblers_problem.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 4, Section 4.4, Example 4.3',
        'hints': [
            '状态：当前资金 (0-100)',
            '动作：下注金额 (1 到 min(s, 100-s))',
            '目标：达到100美元',
            '使用值迭代求解',
        ],
        'learning_points': [
            '应用值迭代解决实际问题',
            '理解终止状态的处理',
            '观察最优策略的结构',
        ],
    },

    # ========== Chapter 5: Monte Carlo Methods ==========
    {
        'id': 'ch05_ex01_first_visit_mc',
        'chapter': 'ch05',
        'chapter_name': '第5章: Monte Carlo Methods (蒙特卡洛方法)',
        'name': '首次访问MC (First-Visit MC Prediction)',
        'path': 'ch05_mc/ex01_first_visit_mc.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 5, Section 5.1',
        'hints': [
            '对每个回合，记录状态首次出现后的回报',
            'V(s) = 平均该状态的所有回报',
            '无需环境模型，从完整回合学习',
        ],
        'learning_points': [
            '理解蒙特卡洛方法的基本思想',
            '掌握首次访问与每次访问的区别',
            '理解无模型学习',
        ],
    },
    {
        'id': 'ch05_ex02_mc_es',
        'chapter': 'ch05',
        'chapter_name': '第5章: Monte Carlo Methods',
        'name': 'MC探索启动 (MC with Exploring Starts)',
        'path': 'ch05_mc/ex02_mc_es.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 5, Section 5.3',
        'hints': [
            '随机选择初始状态-动作对',
            '评估 Q(s,a) 并改进为贪心策略',
            '探索启动保证所有状态-动作对被访问',
        ],
        'learning_points': [
            '理解探索启动的重要性',
            '掌握 on-policy MC 控制',
            '理解贪心策略改进',
        ],
    },
    {
        'id': 'ch05_ex03_off_policy_mc',
        'chapter': 'ch05',
        'chapter_name': '第5章: Monte Carlo Methods',
        'name': '离策略MC (Off-Policy MC)',
        'path': 'ch05_mc/ex03_off_policy_mc.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 5, Section 5.6',
        'hints': [
            '行为策略 b(a|s) 用于生成数据',
            '目标策略 π(a|s) 是我们想学习的策略',
            '使用重要性采样比率：ρ = π(A|S)/b(A|S)',
        ],
        'learning_points': [
            '理解 on-policy 与 off-policy 的区别',
            '掌握重要性采样',
            '理解覆盖假设 (coverage)',
        ],
    },

    # ========== Chapter 6: Temporal-Difference Learning ==========
    {
        'id': 'ch06_ex01_td0',
        'chapter': 'ch06',
        'chapter_name': '第6章: Temporal-Difference Learning (时序差分学习)',
        'name': 'TD(0)预测 (TD(0) Prediction)',
        'path': 'ch06_td/ex01_td0.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 6, Section 6.1',
        'hints': [
            'V(S) ← V(S) + α[R + γV(S\') - V(S)]',
            'TD误差：δ = R + γV(S\') - V(S)',
            '每步更新，无需等待回合结束',
        ],
        'learning_points': [
            '理解TD学习的核心思想',
            '掌握自举 (bootstrapping)',
            '理解TD与MC的区别',
        ],
    },
    {
        'id': 'ch06_ex02_sarsa',
        'chapter': 'ch06',
        'chapter_name': '第6章: Temporal-Difference Learning',
        'name': 'SARSA (On-Policy TD Control)',
        'path': 'ch06_td/ex02_sarsa.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 6, Section 6.4',
        'hints': [
            'Q(S,A) ← Q(S,A) + α[R + γQ(S\',A\') - Q(S,A)]',
            '使用当前策略选择 A\'',
            'SARSA = (S, A, R, S\', A\')',
        ],
        'learning_points': [
            '理解 on-policy TD 控制',
            '掌握 SARSA 算法',
            '理解策略改进',
        ],
    },
    {
        'id': 'ch06_ex03_q_learning',
        'chapter': 'ch06',
        'chapter_name': '第6章: Temporal-Difference Learning',
        'name': 'Q-Learning (Off-Policy TD Control)',
        'path': 'ch06_td/ex03_q_learning.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 6, Section 6.5',
        'hints': [
            'Q(S,A) ← Q(S,A) + α[R + γ max_a Q(S\',a) - Q(S,A)]',
            '学习最优策略，但行为可以是探索性的',
            '直接逼近 Q*',
        ],
        'learning_points': [
            '理解 off-policy 学习',
            '掌握 Q-Learning 算法',
            '理解与 SARSA 的区别',
        ],
    },
    {
        'id': 'ch06_ex04_expected_sarsa',
        'chapter': 'ch06',
        'chapter_name': '第6章: Temporal-Difference Learning',
        'name': 'Expected SARSA',
        'path': 'ch06_td/ex04_expected_sarsa.py',
        'difficulty': 'medium',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 6, Section 6.6',
        'hints': [
            'Q(S,A) ← Q(S,A) + α[R + γ Σ_a π(a|S\')Q(S\',a) - Q(S,A)]',
            '使用期望而不是样本',
            '方差更小，更稳定',
        ],
        'learning_points': [
            '理解期望更新',
            '掌握 Expected SARSA',
            '理解采样更新与期望更新的权衡',
        ],
    },

    # ========== Chapter 7: n-step Bootstrapping ==========
    {
        'id': 'ch07_ex01_n_step_td',
        'chapter': 'ch07',
        'chapter_name': '第7章: n-step Bootstrapping (n步自举法)',
        'name': 'n步TD预测 (n-step TD Prediction)',
        'path': 'ch07_nstep/ex01_n_step_td.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 7, Section 7.1',
        'hints': [
            'n步回报：G_t^{(n)} = R_{t+1} + γR_{t+2} + ... + γ^{n-1}R_{t+n} + γ^nV(S_{t+n})',
            'V(S_t) ← V(S_t) + α[G_t^{(n)} - V(S_t)]',
            '需要存储最近 n 步的经验',
        ],
        'learning_points': [
            '理解 n 步方法统一 TD 和 MC',
            '掌握 n 步回报的计算',
            '理解 n 的选择对性能的影响',
        ],
    },
    {
        'id': 'ch07_ex02_n_step_sarsa',
        'chapter': 'ch07',
        'chapter_name': '第7章: n-step Bootstrapping',
        'name': 'n步SARSA (n-step SARSA)',
        'path': 'ch07_nstep/ex02_n_step_sarsa.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 7, Section 7.2',
        'hints': [
            'n步Q回报：G_t^{(n)} = R_{t+1} + ... + γ^{n-1}R_{t+n} + γ^nQ(S_{t+n}, A_{t+n})',
            '存储 (S, A, R) 序列',
            '延迟 n 步更新',
        ],
        'learning_points': [
            '掌握 n 步 SARSA 算法',
            '理解 n 步控制方法',
            '理解延迟更新',
        ],
    },
    {
        'id': 'ch07_ex03_tree_backup',
        'chapter': 'ch07',
        'chapter_name': '第7章: n-step Bootstrapping',
        'name': '树回溯算法 (Tree Backup)',
        'path': 'ch07_nstep/ex03_tree_backup.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 7, Section 7.5',
        'hints': [
            '不需要重要性采样的 off-policy 方法',
            '使用未选择动作的估计值',
            '备份树结构：选择的动作 + 其他动作的期望',
        ],
        'learning_points': [
            '理解树回溯的思想',
            '掌握不使用重要性采样的 off-policy 方法',
            '理解与 Q-Learning 的关系',
        ],
    },

    # ========== Chapter 9: On-policy Prediction with Approximation ==========
    {
        'id': 'ch09_ex01_gradient_mc',
        'chapter': 'ch09',
        'chapter_name': '第9章: On-policy Prediction with Approximation (函数近似)',
        'name': '梯度MC (Gradient Monte Carlo)',
        'path': 'ch09_approximation/ex01_gradient_mc.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 9, Section 9.3',
        'hints': [
            '使用参数化函数 v̂(s, w) 近似值函数',
            '权重更新：w ← w + α[G - v̂(S, w)]∇v̂(S, w)',
            '可以使用线性函数或神经网络',
        ],
        'learning_points': [
            '理解函数近似的必要性',
            '掌握梯度下降方法',
            '理解特征工程',
        ],
    },
    {
        'id': 'ch09_ex02_semi_gradient_td',
        'chapter': 'ch09',
        'chapter_name': '第9章: On-policy Prediction with Approximation',
        'name': '半梯度TD (Semi-gradient TD)',
        'path': 'ch09_approximation/ex02_semi_gradient_td.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 9, Section 9.3',
        'hints': [
            '权重更新：w ← w + α[R + γv̂(S\', w) - v̂(S, w)]∇v̂(S, w)',
            '"半梯度"：目标包含当前参数 w',
            '实践中效果很好，尽管不是真正的梯度下降',
        ],
        'learning_points': [
            '理解半梯度方法',
            '掌握 TD 的函数近似版本',
            '理解收敛性质',
        ],
    },

    # ========== Chapter 10: On-policy Control with Approximation ==========
    {
        'id': 'ch10_ex01_episodic_sarsa',
        'chapter': 'ch10',
        'chapter_name': '第10章: On-policy Control with Approximation',
        'name': '分节式半梯度SARSA (Episodic Semi-gradient SARSA)',
        'path': 'ch10_control/ex01_episodic_sarsa.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 10, Section 10.1',
        'hints': [
            '使用函数近似 q̂(s, a, w)',
            'w ← w + α[R + γq̂(S\', A\', w) - q̂(S, A, w)]∇q̂(S, A, w)',
            '可应用于连续状态空间',
        ],
        'learning_points': [
            '掌握控制问题的函数近似',
            '理解半梯度 SARSA',
            '应用于连续空间问题',
        ],
    },
    {
        'id': 'ch10_ex02_differential_sarsa',
        'chapter': 'ch10',
        'chapter_name': '第10章: On-policy Control with Approximation',
        'name': '差分半梯度SARSA (Differential Semi-gradient SARSA)',
        'path': 'ch10_control/ex02_differential_sarsa.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 10, Section 10.3',
        'hints': [
            '用于持续任务（无终止）',
            '使用平均奖励：R̄',
            'δ = R - R̄ + q̂(S\', A\', w) - q̂(S, A, w)',
        ],
        'learning_points': [
            '理解持续任务',
            '掌握平均奖励设定',
            '理解差分更新',
        ],
    },

    # ========== Chapter 12: Eligibility Traces ==========
    {
        'id': 'ch12_ex01_td_lambda',
        'chapter': 'ch12',
        'chapter_name': '第12章: Eligibility Traces (资格迹)',
        'name': 'TD(λ)预测',
        'path': 'ch12_eligibility/ex01_td_lambda.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 12, Section 12.1',
        'hints': [
            '资格迹：z_t = γλz_{t-1} + ∇v̂(S_t, w)',
            'TD误差：δ_t = R_{t+1} + γv̂(S_{t+1}, w) - v̂(S_t, w)',
            '权重更新：w ← w + αδ_t z_t',
        ],
        'learning_points': [
            '理解资格迹的概念',
            '掌握 TD(λ) 算法',
            '理解 λ 参数的作用',
        ],
    },
    {
        'id': 'ch12_ex02_sarsa_lambda',
        'chapter': 'ch12',
        'chapter_name': '第12章: Eligibility Traces',
        'name': 'SARSA(λ)',
        'path': 'ch12_eligibility/ex02_sarsa_lambda.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 12, Section 12.7',
        'hints': [
            '扩展到动作值函数',
            'z_t = γλz_{t-1} + ∇q̂(S_t, A_t, w)',
            '更快的信用分配',
        ],
        'learning_points': [
            '掌握 SARSA(λ) 算法',
            '理解控制中的资格迹',
            '理解替代迹与累积迹',
        ],
    },
    {
        'id': 'ch12_ex03_true_online_td',
        'chapter': 'ch12',
        'chapter_name': '第12章: Eligibility Traces',
        'name': 'True Online TD(λ)',
        'path': 'ch12_eligibility/ex03_true_online_td.py',
        'difficulty': 'expert',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 12, Section 12.8',
        'hints': [
            '完全在线的 TD(λ)',
            '修正传统 TD(λ) 的不精确性',
            '需要额外的旧值记录',
        ],
        'learning_points': [
            '理解真正的在线学习',
            '掌握精确的 λ-return 算法',
            '理解理论与实践的差异',
        ],
    },

    # ========== Chapter 13: Policy Gradient Methods ==========
    {
        'id': 'ch13_ex01_reinforce',
        'chapter': 'ch13',
        'chapter_name': '第13章: Policy Gradient Methods (策略梯度方法)',
        'name': 'REINFORCE',
        'path': 'ch13_policy_gradient/ex01_reinforce.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 13, Section 13.3',
        'hints': [
            '参数化策略：π(a|s, θ)',
            '策略梯度：∇J(θ) = E[G_t ∇ln π(A_t|S_t, θ)]',
            'θ ← θ + α G_t ∇ln π(A_t|S_t, θ)',
        ],
        'learning_points': [
            '理解策略梯度定理',
            '掌握 REINFORCE 算法',
            '理解高方差问题',
        ],
    },
    {
        'id': 'ch13_ex02_reinforce_baseline',
        'chapter': 'ch13',
        'chapter_name': '第13章: Policy Gradient Methods',
        'name': 'REINFORCE with Baseline',
        'path': 'ch13_policy_gradient/ex02_reinforce_baseline.py',
        'difficulty': 'hard',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 13, Section 13.4',
        'hints': [
            '引入基线 b(s) 减少方差',
            '更新：θ ← θ + α(G_t - b(S_t))∇ln π(A_t|S_t, θ)',
            '基线通常是状态值函数 v̂(s, w)',
        ],
        'learning_points': [
            '理解基线的作用',
            '掌握方差减少技术',
            '理解偏差-方差权衡',
        ],
    },
    {
        'id': 'ch13_ex03_actor_critic',
        'chapter': 'ch13',
        'chapter_name': '第13章: Policy Gradient Methods',
        'name': 'Actor-Critic',
        'path': 'ch13_policy_gradient/ex03_actor_critic.py',
        'difficulty': 'expert',
        'test_func': 'test',
        'reference': 'Sutton & Barto, Chapter 13, Section 13.5',
        'hints': [
            'Actor：策略网络 π(a|s, θ)',
            'Critic：值函数网络 v̂(s, w)',
            'TD误差作为优势：δ = R + γv̂(S\', w) - v̂(S, w)',
        ],
        'learning_points': [
            '理解 Actor-Critic 架构',
            '掌握两个网络的协同训练',
            '理解优势函数',
        ],
    },
]


def get_exercise_by_id(exercise_id: str):
    """Get exercise info by ID"""
    for ex in EXERCISE_LIST:
        if ex['id'] == exercise_id or ex['id'].endswith(exercise_id):
            return ex
    return None


def get_exercises_by_chapter(chapter: str):
    """Get all exercises in a chapter"""
    return [ex for ex in EXERCISE_LIST if ex['chapter'] == chapter]


def get_all_chapters():
    """Get list of all chapters"""
    chapters = {}
    for ex in EXERCISE_LIST:
        if ex['chapter'] not in chapters:
            chapters[ex['chapter']] = ex['chapter_name']
    return chapters
