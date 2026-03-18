"""
练习 06: 学习率调度 (Learning Rate Schedule)

学习率是训练中最重要的超参数之一。
学习率调度器可以在训练过程中动态调整学习率。

常见策略：
- Step Decay: 每隔固定步数降低学习率
- Cosine Annealing: 余弦退火
- Warmup: 预热阶段逐渐增加学习率
- Linear Decay: 线性衰减

在这个练习中，你将学习：
- 不同学习率调度策略
- Warmup 的重要性
- 如何实现自定义调度器
"""

import torch
import math


class StepLR:
    """
    阶梯式学习率衰减

    每 step_size 步，学习率乘以 gamma
    """

    def __init__(self, optimizer, step_size, gamma=0.1):
        self.optimizer = optimizer
        self.step_size = step_size
        self.gamma = gamma
        self.current_step = 0
        self.base_lr = optimizer.param_groups[0]['lr']

    def step(self):
        self.current_step += 1

        # TODO: 计算新的学习率
        # 每 step_size 步，lr = base_lr * gamma^n，n 是衰减次数
        n_decays = self.current_step // self.___  # 填入 step_size
        new_lr = self.base_lr * (self.gamma ** n_decays)

        # 更新优化器中的学习率
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = new_lr

    def get_lr(self):
        return self.optimizer.param_groups[0]['lr']


class CosineAnnealingLR:
    """
    余弦退火学习率

    lr = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(π * t / T))

    平滑地从 lr_max 降低到 lr_min
    """

    def __init__(self, optimizer, T_max, eta_min=0):
        self.optimizer = optimizer
        self.T_max = T_max
        self.eta_min = eta_min
        self.current_step = 0
        self.base_lr = optimizer.param_groups[0]['lr']

    def step(self):
        self.current_step += 1

        # TODO: 计算余弦退火学习率
        # lr = eta_min + 0.5 * (base_lr - eta_min) * (1 + cos(π * t / T_max))
        cos_value = math.cos(math.___ * self.current_step / self.T_max)  # 使用 pi
        new_lr = self.eta_min + 0.5 * (self.base_lr - self.eta_min) * (1 + cos_value)

        for param_group in self.optimizer.param_groups:
            param_group['lr'] = new_lr

    def get_lr(self):
        return self.optimizer.param_groups[0]['lr']


class WarmupLR:
    """
    线性预热学习率

    在 warmup_steps 内，学习率从 0 线性增加到 base_lr
    """

    def __init__(self, optimizer, warmup_steps):
        self.optimizer = optimizer
        self.warmup_steps = warmup_steps
        self.current_step = 0
        self.base_lr = optimizer.param_groups[0]['lr']

    def step(self):
        self.current_step += 1

        if self.current_step <= self.warmup_steps:
            # TODO: 线性预热
            # lr = base_lr * (current_step / warmup_steps)
            new_lr = self.___ * (self.current_step / self.warmup_steps)  # 填入 base_lr
        else:
            new_lr = self.base_lr

        for param_group in self.optimizer.param_groups:
            param_group['lr'] = new_lr

    def get_lr(self):
        return self.optimizer.param_groups[0]['lr']


class WarmupCosineAnnealingLR:
    """
    带预热的余弦退火 (Transformer 常用)

    1. Warmup 阶段: 线性增加到 base_lr
    2. Cosine 阶段: 余弦退火到 eta_min
    """

    def __init__(self, optimizer, warmup_steps, T_max, eta_min=0):
        self.optimizer = optimizer
        self.warmup_steps = warmup_steps
        self.T_max = T_max
        self.eta_min = eta_min
        self.current_step = 0
        self.base_lr = optimizer.param_groups[0]['lr']

    def step(self):
        self.current_step += 1

        if self.current_step <= self.warmup_steps:
            # Warmup 阶段
            new_lr = self.base_lr * (self.current_step / self.warmup_steps)
        else:
            # Cosine 退火阶段
            progress = (self.current_step - self.warmup_steps) / (self.T_max - self.warmup_steps)
            # TODO: 计算余弦退火
            cos_value = math.cos(math.pi * ___)  # 填入 progress
            new_lr = self.eta_min + 0.5 * (self.base_lr - self.eta_min) * (1 + cos_value)

        for param_group in self.optimizer.param_groups:
            param_group['lr'] = new_lr

    def get_lr(self):
        return self.optimizer.param_groups[0]['lr']


class LinearDecayLR:
    """
    线性衰减学习率

    lr = base_lr * (1 - t / T_max)
    """

    def __init__(self, optimizer, T_max, eta_min=0):
        self.optimizer = optimizer
        self.T_max = T_max
        self.eta_min = eta_min
        self.current_step = 0
        self.base_lr = optimizer.param_groups[0]['lr']

    def step(self):
        self.current_step += 1

        # TODO: 线性衰减
        decay = 1 - self.current_step / self.___  # 填入 T_max
        new_lr = max(self.eta_min, self.base_lr * decay)

        for param_group in self.optimizer.param_groups:
            param_group['lr'] = new_lr

    def get_lr(self):
        return self.optimizer.param_groups[0]['lr']


def visualize_schedules():
    """可视化不同学习率调度策略"""
    print("不同学习率调度策略的变化:")

    total_steps = 100
    warmup_steps = 10

    # 创建虚拟参数和优化器
    def create_optimizer():
        param = torch.tensor([1.0], requires_grad=True)
        return torch.optim.SGD([param], lr=0.1)

    schedulers = {
        'StepLR': StepLR(create_optimizer(), step_size=30, gamma=0.1),
        'CosineAnnealingLR': CosineAnnealingLR(create_optimizer(), T_max=total_steps),
        'WarmupLR': WarmupLR(create_optimizer(), warmup_steps=warmup_steps),
        'WarmupCosine': WarmupCosineAnnealingLR(create_optimizer(), warmup_steps, total_steps),
        'LinearDecay': LinearDecayLR(create_optimizer(), T_max=total_steps),
    }

    # 记录学习率变化
    lr_histories = {name: [] for name in schedulers}

    for step in range(total_steps):
        for name, scheduler in schedulers.items():
            lr_histories[name].append(scheduler.get_lr())
            scheduler.step()

    # 打印关键点
    print("\n步数\t" + "\t".join(schedulers.keys()))
    for step in [0, 10, 30, 50, 70, 99]:
        values = [f"{lr_histories[name][step]:.4f}" for name in schedulers]
        print(f"{step}\t" + "\t".join(values))

    return lr_histories


def main():
    print("测试 StepLR...")
    param = torch.tensor([1.0], requires_grad=True)
    optimizer = torch.optim.SGD([param], lr=0.1)
    scheduler = StepLR(optimizer, step_size=10, gamma=0.5)

    for _ in range(25):
        scheduler.step()

    # 经过 20 步，应该衰减 2 次: 0.1 * 0.5^2 = 0.025
    assert abs(scheduler.get_lr() - 0.025) < 0.001
    print("✓ StepLR 通过!")

    print("\n测试 CosineAnnealingLR...")
    optimizer = torch.optim.SGD([param], lr=0.1)
    scheduler = CosineAnnealingLR(optimizer, T_max=100)

    # 走到一半应该接近 0.05
    for _ in range(50):
        scheduler.step()
    assert abs(scheduler.get_lr() - 0.05) < 0.01
    print("✓ CosineAnnealingLR 通过!")

    print("\n测试 WarmupLR...")
    optimizer = torch.optim.SGD([param], lr=0.1)
    scheduler = WarmupLR(optimizer, warmup_steps=10)

    for _ in range(5):
        scheduler.step()
    assert abs(scheduler.get_lr() - 0.05) < 0.01  # 一半预热
    print("✓ WarmupLR 通过!")

    print("\n测试 WarmupCosineAnnealingLR...")
    optimizer = torch.optim.SGD([param], lr=0.1)
    scheduler = WarmupCosineAnnealingLR(optimizer, warmup_steps=10, T_max=100)

    # 10 步预热后应该达到峰值
    for _ in range(10):
        scheduler.step()
    assert abs(scheduler.get_lr() - 0.1) < 0.01
    print("✓ WarmupCosineAnnealingLR 通过!")

    print("\n测试 LinearDecayLR...")
    optimizer = torch.optim.SGD([param], lr=0.1)
    scheduler = LinearDecayLR(optimizer, T_max=100)

    for _ in range(50):
        scheduler.step()
    assert abs(scheduler.get_lr() - 0.05) < 0.01
    print("✓ LinearDecayLR 通过!")

    print("\n可视化学习率变化...")
    visualize_schedules()

    print("\n🎉 所有测试通过！学习率调度掌握完成！")


if __name__ == "__main__":
    main()
