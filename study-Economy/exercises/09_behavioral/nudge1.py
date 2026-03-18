# EXERCISE: nudge1
# DIFFICULTY: ★★★☆☆
# TOPIC: 助推与行为干预
#
# 说明：
# 助推（Nudge）是一种在不禁止任何选项或显著改变经济激励的情况下，
# 通过改变选择环境来引导人们做出更好决策的干预方式。
#
# 【理论背景】
#
# Richard Thaler 和 Cass Sunstein 在《Nudge》(2008) 中系统阐述了这一概念，
# Thaler 因此于2017年获得诺贝尔经济学奖。
#
# 核心理念：
# - 承认人的有限理性
# - 利用而非对抗行为偏误
# - 保持选择自由
# - 低成本、高效果
#
# 【与传统经济政策的区别】
#
# 传统干预方式：
# 1. 命令与控制（禁止或强制）
# 2. 经济激励（税收、补贴）
# 3. 信息提供（教育、披露）
#
# 助推的独特性：
# - 不改变选择集
# - 不显著改变相对价格
# - 利用心理机制影响决策
# - "自由意志家长主义"（Libertarian Paternalism）
#
# 【选择架构】
#
# 选择架构（Choice Architecture）指设计选择环境的方式：
# - 默认选项的设置
# - 选项的呈现顺序
# - 信息的框架
# - 反馈机制
# - 社会比较
#
# 选择架构师有责任设计好的选择环境，
# 因为没有"中性"的选择架构。
#
# 【常见助推工具】
#
# 1. 默认选项（Defaults）
#    - 器官捐献：opt-in vs opt-out
#    - 养老金：自动加入
#    - 隐私设置：默认值
#    效果：可能改变50%以上的选择
#
# 2. 简化（Simplification）
#    - 减少表格复杂性
#    - 一键式操作
#    - 预填信息
#    效果：降低交易成本，提高参与
#
# 3. 社会规范（Social Norms）
#    - "大多数人都这样做"
#    - 描述性规范 vs 禁令性规范
#    - 同伴效应
#    效果：利用从众心理
#
# 4. 凸显性（Salience）
#    - 使重要信息更突出
#    - 标签、颜色、位置
#    - 即时反馈
#    效果：引导注意力
#
# 5. 承诺设备（Commitment Devices）
#    - 预先承诺
#    - 目标设定
#    - 社会压力
#    效果：帮助克服自控问题
#
# 6. 提醒（Reminders）
#    - 短信提醒
#    - 邮件通知
#    - 日历提醒
#    效果：减少遗忘和拖延
#
# 【经典案例】
#
# 1. Save More Tomorrow (SMarT) 计划
#    - Thaler & Benartzi (2004)
#    - 承诺将未来加薪的一部分用于储蓄
#    - 3年内储蓄率从3.5%增至13.6%
#
# 2. 英国HMRC税收提醒
#    - "9/10的人按时缴税"
#    - 社会规范信息提高5%的遵从率
#
# 3. 器官捐献制度
#    - Opt-out国家捐献率约90%
#    - Opt-in国家捐献率约15%
#
# 4. 食堂健康饮食
#    - 健康食品放在显眼位置
#    - 不健康食品需要额外努力获取
#
# 【伦理争议】
#
# 1. 家长主义问题
#    - 谁有权决定什么是"好"的选择？
#    - 可能侵犯自主权
#
# 2. 透明性
#    - 助推应该是透明的吗？
#    - 隐蔽的助推是否是操纵？
#
# 3. 效果持续性
#    - 长期效果可能减弱
#    - 人们可能适应或反抗
#
# 4. 谁受益？
#    - 助推可能被滥用
#    - 企业的"黑暗助推"
#
# 【设计原则（EAST）】
# 英国行为洞察团队的框架：
# - Easy（容易）：简化流程
# - Attractive（吸引）：引起注意
# - Social（社会）：利用社会规范
# - Timely（及时）：在关键时刻干预
#
# 任务：
# 1. 理解各类助推机制
# 2. 量化助推效果
# 3. 设计助推策略
# 4. 考虑伦理问题
#
# HINT1: 默认选项的力量巨大，可能改变多数人的选择
# HINT2: 好的助推应该是透明的，且符合决策者的长期利益
# HINT3: 要考虑助推的可能副作用和伦理边界

import numpy as np


def default_effect(
    base_rate: float,
    default_is_yes: bool,
    inertia: float = 0.7
) -> float:
    """
    默认选项效应：人们倾向于保持默认选择。

    【公式推导】
    默认效应模型：

    设 base_rate 为真实偏好的参与率（如果没有交易成本）。

    实际参与率取决于默认选项：
    - 默认参与（opt-out）：参与率 = base_rate + inertia × (1 - base_rate)
    - 默认不参与（opt-in）：参与率 = base_rate × (1 - inertia)

    其中 inertia 是惰性/现状偏好强度（0-1）。

    更简化的版本：
    - Opt-out: 参与率 ≈ base_rate + inertia
    - Opt-in: 参与率 ≈ base_rate - inertia

    【心理学机制】

    1. 惰性/拖延
       - 改变需要努力
       - 默认选项减少认知负担

    2. 暗示性规范
       - 默认被视为"推荐"
       - "他们这样设置一定有道理"

    3. 损失厌恶
       - 改变现状被视为潜在损失
       - 保持默认感觉更安全

    4. 信息不对称
       - 不确定时依赖默认
       - 默认提供了决策参考

    【实验证据】

    Johnson & Goldstein (2003) 器官捐献研究：
    - Opt-in国家（德国）：12%同意率
    - Opt-out国家（奥地利）：99.98%同意率

    401(k)自动加入：
    - 自动加入：参与率90%+
    - 手动加入：参与率约50%

    参数:
        base_rate: 有选择时的基础参与率（真实偏好）
            - 0.5表示50%的人真正想参与
        default_is_yes: 默认是否为参与
            - True：默认参与（opt-out）
            - False：默认不参与（opt-in）
        inertia: 惰性程度（0-1）
            - 0：无惰性，所有人都按真实偏好选择
            - 1：完全惰性，所有人都接受默认
            - 典型值约0.7

    返回:
        实际参与率

    示例:
        养老金自动加入效果：

        假设50%的人真正想加入养老金计划
        >>> # 传统opt-in
        >>> default_effect(0.5, default_is_yes=False, inertia=0.7)
        0.15  # 只有15%真正加入

        >>> # 自动加入opt-out
        >>> default_effect(0.5, default_is_yes=True, inertia=0.7)
        0.85  # 85%保持加入

        >>> # 惰性降低（教育、提醒）
        >>> default_effect(0.5, True, inertia=0.5)
        0.75  # 效果降低但仍显著

        器官捐献：
        >>> default_effect(0.7, True, 0.9)   # 70%想捐献，opt-out
        0.97  # 97%登记捐献
        >>> default_effect(0.7, False, 0.9)  # 同样偏好，opt-in
        0.07  # 只有7%登记！
    """
    # TODO: 实现默认效应
    # 提示1：如果默认是参与，很多本不会主动参与的人会保持默认
    # 提示2：如果默认是不参与，很多本想参与的人也不会行动
    # 提示3：参与率 = base_rate + direction × inertia × (1 - base_rate)
    pass


def opt_in_vs_opt_out(
    true_preference: float,
    switching_cost: float
) -> tuple[float, float]:
    """
    比较自动加入（opt-out）与主动加入（opt-in）的参与率差异。

    【公式推导】
    更精确的模型考虑"切换成本"：

    决策规则：
    如果 |效用差| > 切换成本，则改变默认
    否则，保持默认

    Opt-in（默认不参与）：
    - 想参与且效用足够高的人才会参与
    - 参与率 = P(想参与且能克服成本) ≈ true_preference × (1 - switching_cost)

    Opt-out（默认参与）：
    - 不想参与且反感足够强的人才会退出
    - 参与率 = 1 - P(不想且能克服成本)
              ≈ 1 - (1 - true_preference) × (1 - switching_cost)
              = true_preference + switching_cost × (1 - true_preference)

    参与率差异：
    Δ = opt_out_rate - opt_in_rate
    ≈ switching_cost

    【政策含义】

    1. 默认选项的选择非常重要
       - 可以改变50%+的行为

    2. 应该将默认设为对多数人有利的选项
       - 养老金、保险、器官捐献

    3. 简化流程可以减少切换成本
       - 但可能降低默认的力量

    参数:
        true_preference: 真实偏好率（想参与的比例）
        switching_cost: 切换成本（主观感知，0-1）
            - 表示改变默认的心理/实际成本

    返回:
        (opt-in参与率, opt-out参与率)

    示例:
        退休储蓄计划：

        假设60%的人真正想参与，切换成本0.5
        >>> opt_in_vs_opt_out(0.6, 0.5)
        (0.3, 0.8)

        Opt-in：0.6 × 0.5 = 0.3（30%参与）
        Opt-out：0.6 + 0.5 × 0.4 = 0.8（80%参与）

        差异50个百分点！

        切换成本很低时：
        >>> opt_in_vs_opt_out(0.6, 0.1)
        (0.54, 0.64)
        # 差异只有10个百分点

        切换成本很高时：
        >>> opt_in_vs_opt_out(0.6, 0.9)
        (0.06, 0.96)
        # 差异90个百分点
    """
    # TODO: 计算opt-in和opt-out参与率
    # 提示1：opt_in = true_preference × (1 - switching_cost)
    # 提示2：opt_out = true_preference + switching_cost × (1 - true_preference)
    pass


def social_norm_nudge(
    base_behavior: float,
    norm_message: float,
    conformity: float
) -> float:
    """
    社会规范助推：利用"大多数人都这样做"的信息影响行为。

    【公式推导】
    社会规范效应模型：

    行为调整 = 基础行为 + 从众系数 × (规范信息 - 基础行为)

    即：
    new_behavior = base + conformity × (norm - base)

    这是一个向规范趋同的调整过程。

    【心理学机制】

    1. 描述性规范（Descriptive Norms）
       - "大多数人这样做"
       - 提供行为参照

    2. 禁令性规范（Injunctive Norms）
       - "应该这样做"
       - 提供道德标准

    3. 从众心理
       - 人们希望与他人保持一致
       - 减少社会风险

    【经典研究】

    Schultz et al. (2007) 能源消费研究：
    - 告知邻居的用电量
    - 高用户减少用电
    - 低用户...增加用电！（回旋效应）

    解决方案：加入禁令性规范
    - 低于平均：:)
    - 高于平均：:(

    HMRC税收提醒：
    - "9/10的人按时缴税"
    - 提高5%遵从率

    参数:
        base_behavior: 基础行为水平（0-1，或具体数值）
        norm_message: 规范信息（告知的他人行为水平）
        conformity: 从众程度（0-1）
            - 0：不受他人影响
            - 1：完全跟随规范
            - 典型值0.3-0.5

    返回:
        调整后的行为水平

    示例:
        能源节约助推：

        某人用电量120度，告知邻居平均100度
        >>> social_norm_nudge(120, 100, 0.4)
        112  # 减少8度

        但如果他本来用电80度：
        >>> social_norm_nudge(80, 100, 0.4)
        88  # 增加8度！（回旋效应）

        税收遵从：
        原本只有70%按时缴税，告知"90%按时"
        >>> social_norm_nudge(0.7, 0.9, 0.3)
        0.76  # 提高6个百分点

        注意：虚假的规范信息可能适得其反
    """
    # TODO: 计算社会规范助推效果
    # 提示：new_behavior = base + conformity × (norm - base)
    pass


def save_more_tomorrow(
    current_savings_rate: float,
    future_raise: float,
    commitment_rate: float
) -> float:
    """
    "明天储蓄更多"（SMarT）计划：承诺将未来加薪用于增加储蓄。

    【理论背景】

    SMarT计划（Save More Tomorrow）由Thaler和Benartzi (2004)提出，
    利用多种行为洞见：

    1. 损失厌恶
       - 从现有工资扣款感觉是"损失"
       - 从未来加薪扣款不感觉是损失

    2. 现在偏好
       - 人们更容易承诺未来行动
       - 因为未来的牺牲感觉较小

    3. 惰性
       - 一旦加入，倾向于保持
       - 自动升级储蓄率

    4. 锚定
       - 起始承诺比例设定了锚

    【计划设计】
    1. 员工承诺将下次加薪的一部分用于增加储蓄
    2. 储蓄率在每次加薪后自动增加
    3. 可以随时退出
    4. 储蓄率有上限（如15%）

    【实验结果】
    Thaler & Benartzi (2004)：
    - 初始储蓄率：3.5%
    - 一年后：6.5%
    - 两年后：9.4%
    - 三年半后：13.6%

    参数:
        current_savings_rate: 当前储蓄率（如0.035表示3.5%）
        future_raise: 预期加薪比例（如0.03表示3%加薪）
        commitment_rate: 承诺将加薪用于储蓄的比例（如0.5表示50%）

    返回:
        加薪后的新储蓄率

    示例:
        典型SMarT参与者：

        当前储蓄率5%，预期加薪3%，承诺将50%加薪用于储蓄
        >>> save_more_tomorrow(0.05, 0.03, 0.5)
        0.065  # 储蓄率增加到6.5%

        计算过程：
        - 加薪3%意味着收入变为1.03倍
        - 其中50%×3%=1.5%用于增加储蓄
        - 新储蓄率 = 5% + 1.5% = 6.5%

        连续三次加薪：
        >>> rate = 0.05
        >>> for _ in range(3):
        ...     rate = save_more_tomorrow(rate, 0.03, 0.5)
        >>> rate
        0.095  # 接近10%

        SMarT的力量：
        - 无需减少当前消费
        - 储蓄自动增长
        - 克服惰性和现在偏好
    """
    # TODO: 计算SMarT后的储蓄率
    # 提示1：增加的储蓄来自加薪的一部分
    # 提示2：新储蓄率 = 当前储蓄率 + 加薪比例 × 承诺比例
    pass


def simplification_effect(
    base_participation: float,
    complexity: float,
    simplification: float
) -> float:
    """
    简化效应：降低复杂性提高参与率。

    【公式推导】
    复杂性对参与的影响：

    有效参与门槛 = 基础门槛 × (1 + complexity)
    实际参与率 = base_participation × (1 - complexity + simplification)

    或者更简单地：
    参与率 = base × (1 - complexity × (1 - simplification))

    当 simplification = 1 时，complexity 被完全抵消。

    【心理学机制】

    1. 认知负荷
       - 复杂表格让人放弃
       - 太多选项导致决策瘫痪

    2. 拖延
       - 复杂任务更容易被推迟
       - "以后再说"变成"永不"

    3. 恐惧/回避
       - 复杂程序引发焦虑
       - 避免而非面对

    【经典案例】

    大学助学金申请（FAFSA）：
    - 原始表格：复杂，约100问题
    - 很多低收入家庭放弃申请
    - 简化后参与率显著提高

    纳税申报：
    - 预填税表提高遵从率
    - 一键式申报减少错误

    选择过载：
    - 选项从24个减到6个
    - 参与率从3%提高到30%

    参数:
        base_participation: 无复杂性时的基础参与率
        complexity: 复杂性水平（0-1）
            - 0：完全简单
            - 1：极其复杂（几乎无人能完成）
        simplification: 简化程度（0-1）
            - 0：无简化
            - 1：完全简化（消除复杂性）

    返回:
        简化后的实际参与率

    示例:
        助学金申请：

        90%的人想申请，但表格复杂度0.6
        >>> simplification_effect(0.9, 0.6, 0)
        0.36  # 只有36%完成申请

        简化表格（简化度0.5）：
        >>> simplification_effect(0.9, 0.6, 0.5)
        0.63  # 63%完成

        完全简化（简化度1.0）：
        >>> simplification_effect(0.9, 0.6, 1.0)
        0.9  # 恢复到基础率

        政策启示：
        - 简化是成本效益很高的干预
        - 减少表格问题
        - 预填已知信息
        - 提供清晰指导
    """
    # TODO: 计算简化效应
    # 提示：参与率 = base × (1 - complexity × (1 - simplification))
    pass


def reminder_effectiveness(
    forgetting_rate: float,
    reminder_timing: int,
    deadline: int
) -> float:
    """
    提醒的有效性：通过及时提醒减少遗忘和拖延。

    【公式推导】
    遗忘曲线和提醒模型：

    记忆保持率 ≈ exp(-遗忘率 × 时间)

    提醒效果：
    完成概率提升 = (1 - 原始完成率) × 记忆恢复率

    提醒时机影响：
    - 太早：可能再次遗忘
    - 太晚：没有时间行动
    - 最优：距截止日1-3天

    【心理学机制】

    1. 遗忘
       - 意图被其他事情覆盖
       - 艾宾浩斯遗忘曲线

    2. 拖延
       - "以后再做"的心态
       - 时间贴现导致的延迟

    3. 凸显性
       - 提醒使任务重新变得突出
       - 重置优先级

    【实验证据】

    疫苗接种提醒：
    - 短信提醒提高5-7%接种率

    药物依从性：
    - 每日提醒提高20%+依从性

    还款提醒：
    - 适时提醒减少逾期率

    参数:
        forgetting_rate: 遗忘率（每天）
            - 0.1：低遗忘（重要事项）
            - 0.3：中度遗忘（一般事项）
            - 0.5：高遗忘（容易忽略）
        reminder_timing: 提醒时点（距离截止日的天数）
        deadline: 截止日（从现在起的天数）

    返回:
        提醒带来的完成率提升

    示例:
        缴费提醒：

        遗忘率0.3，截止日30天后，提前7天提醒
        >>> reminder_effectiveness(0.3, 7, 30)
        0.25  # 完成率提升25%

        提前1天提醒（太晚）：
        >>> reminder_effectiveness(0.3, 1, 30)
        0.05  # 只提升5%（没时间行动）

        提前20天提醒（太早）：
        >>> reminder_effectiveness(0.3, 20, 30)
        0.10  # 可能再次遗忘

        最优提醒策略：
        - 多次提醒（7天、3天、1天）
        - 个性化时机
        - 行动链接（短信中包含直接链接）
    """
    # TODO: 计算提醒效果
    # 提示1：考虑遗忘曲线
    # 提示2：提醒太早或太晚效果都不好
    # 提示3：可以用凸函数建模最优提醒时机
    pass


def choice_overload(
    n_options: int,
    optimal_n: int = 6
) -> float:
    """
    选择过载：过多选项导致决策质量下降或放弃选择。

    【理论背景】

    Iyengar & Lepper (2000) 果酱实验：
    - 24种选项：3%购买
    - 6种选项：30%购买

    过多选项导致：
    1. 决策瘫痪（无法选择）
    2. 决策质量下降（随机选择）
    3. 满意度降低（后悔未选的）
    4. 购买延迟或放弃

    【公式推导】
    决策质量与选项数的关系：

    一种建模方式：
    决策质量 = 最优质量 × exp(-|n - optimal_n| / 缩放系数)

    或者分段函数：
    n ≤ optimal_n: 质量随n增加
    n > optimal_n: 质量随n减少

    【最优选项数】
    研究表明最优选项数约为5-9个（Miller的7±2法则）：
    - 太少：可能错过最优
    - 太多：认知负荷过大

    【应用】
    1. 零售
       - 适度减少SKU可能增加销售
    2. 投资
       - 401(k)选项过多降低参与
    3. 菜单设计
       - 精简菜单提高满意度

    参数:
        n_options: 选项数量
        optimal_n: 最优选项数（默认6）

    返回:
        决策质量（0-1）

    示例:
        产品选择场景：

        >>> choice_overload(6, 6)
        1.0  # 最优选项数，决策质量最高

        >>> choice_overload(24, 6)
        0.3  # 选项过多，决策质量下降

        >>> choice_overload(2, 6)
        0.7  # 选项太少也不理想

        401(k)投资选项：
        >>> choice_overload(50, 6)
        0.15  # 过多基金选项导致决策瘫痪

        策略：
        - 提供默认选项
        - 分类呈现
        - 使用筛选工具
    """
    # TODO: 计算选择过载效应
    # 提示1：决策质量在最优选项数时最高
    # 提示2：偏离最优越多，质量越低
    # 提示3：可以用高斯函数或指数衰减建模
    pass


def libertarian_paternalism_score(
    welfare_improvement: float,
    choice_preserved: bool,
    transparency: float
) -> float:
    """
    自由意志家长主义评分：评估助推是否符合伦理原则。

    【理论背景】

    "自由意志家长主义"（Libertarian Paternalism）的核心原则：
    1. 提升福利（家长主义元素）
    2. 保持选择自由（自由意志元素）
    3. 透明（可被识别和抵制）

    好的助推应该：
    - 对被助推者有利（不是操纵）
    - 不禁止或限制选择
    - 可以被轻易规避
    - 是透明的

    【评估维度】

    1. 福利改善
       - 助推是否真的让人过得更好？
       - 以谁的标准判断？

    2. 选择自由
       - 所有选项是否仍然可用？
       - 选择其他选项的成本是否过高？

    3. 透明度
       - 助推是否可被识别？
       - 是否披露了助推的存在？

    【争议案例】

    明显OK：
    - 器官捐献opt-out（可轻易退出）
    - 养老金自动加入（可退出）

    有争议：
    - "黑暗模式"（让退订很困难）
    - 误导性默认（如预选广告邮件）

    明显不OK：
    - 欺骗性信息
    - 隐藏费用
    - 无法改变的默认

    参数:
        welfare_improvement: 福利改善程度（0-1）
            - 对被助推者的客观收益
        choice_preserved: 选择自由是否完全保留
            - True：所有选项仍可选择
            - False：某些选项被移除或成本显著增加
        transparency: 透明度（0-1）
            - 0：完全隐蔽的助推
            - 1：完全透明，告知正在被助推

    返回:
        自由意志家长主义评分（0-1）
        高分表示符合伦理原则

    示例:
        评估不同助推策略：

        养老金自动加入：
        >>> libertarian_paternalism_score(
        ...     welfare_improvement=0.8,  # 显著提高储蓄
        ...     choice_preserved=True,    # 可以退出
        ...     transparency=0.9          # 告知默认设置
        ... )
        0.85  # 高分，符合原则

        "黑暗模式"退订：
        >>> libertarian_paternalism_score(
        ...     welfare_improvement=0.1,  # 对用户不利
        ...     choice_preserved=True,    # 技术上可退出
        ...     transparency=0.2          # 故意隐蔽
        ... )
        0.2  # 低分，不符合原则

        禁烟政策（对比）：
        >>> libertarian_paternalism_score(
        ...     welfare_improvement=0.9,
        ...     choice_preserved=False,   # 禁止了选择
        ...     transparency=1.0
        ... )
        0.5  # 中等分数，不是助推而是禁令
    """
    # TODO: 计算LP评分
    # 提示1：三个维度都重要
    # 提示2：选择自由是关键（如果不保留，分数大幅降低）
    # 提示3：可以用加权平均或乘法组合
    pass


# === 不要修改以下代码 ===
if __name__ == "__main__":
    from economlings.checker import check
    check(__file__)
