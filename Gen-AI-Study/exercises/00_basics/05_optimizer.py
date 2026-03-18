"""
练习 05: 优化器 (Optimizer)

优化器是深度学习训练的核心，负责更新模型参数。
本练习将帮助你理解 SGD 和 Adam 优化器的原理。

在这个练习中，你将学习：
- SGD (随机梯度下降) 的实现
- 动量 (Momentum) 的作用
- Adam 优化器的原理
"""

import torch
import torch.nn as nn


class SimpleSGD:
    """
    简单 SGD 优化器

    更新规则: θ = θ - lr * ∇θ
    """

    def __init__(self, params, lr=0.01):
        self.params = list(params)
        self.lr = lr

    def step(self):
        """执行一步参数更新"""
        for param in self.params:
            if param.grad is not None:
                # TODO: 更新参数
                # θ = θ - lr * grad
                param.data = param.data - self.___ * param.grad  # 填入 lr

    def zero_grad(self):
        """清零梯度"""
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()


class SGDWithMomentum:
    """
    带动量的 SGD

    v_t = μ * v_{t-1} + ∇θ
    θ = θ - lr * v_t

    动量帮助加速收敛并穿越局部最小值
    """

    def __init__(self, params, lr=0.01, momentum=0.9):
        self.params = list(params)
        self.lr = lr
        self.momentum = momentum
        # 初始化速度
        self.velocities = [torch.zeros_like(p) for p in self.params]

    def step(self):
        for i, param in enumerate(self.params):
            if param.grad is not None:
                # TODO: 更新速度
                # v = momentum * v + grad
                self.velocities[i] = self.___ * self.velocities[i] + param.grad  # 填入 momentum

                # TODO: 更新参数
                param.data = param.data - self.lr * self.___[i]  # 填入 velocities

    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()


class SimpleAdam:
    """
    Adam 优化器

    Adam = Adaptive Moment Estimation
    结合了动量和自适应学习率

    m_t = β1 * m_{t-1} + (1-β1) * g_t       # 一阶矩估计
    v_t = β2 * v_{t-1} + (1-β2) * g_t^2     # 二阶矩估计

    m̂_t = m_t / (1 - β1^t)                  # 偏差修正
    v̂_t = v_t / (1 - β2^t)

    θ = θ - lr * m̂_t / (√v̂_t + ε)
    """

    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-8):
        self.params = list(params)
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        self.t = 0  # 时间步

        # 初始化一阶和二阶矩
        self.m = [torch.zeros_like(p) for p in self.params]
        self.v = [torch.zeros_like(p) for p in self.params]

    def step(self):
        self.t += 1

        for i, param in enumerate(self.params):
            if param.grad is None:
                continue

            g = param.grad

            # TODO: 更新一阶矩估计 (动量)
            # m = β1 * m + (1 - β1) * g
            self.m[i] = self.beta1 * self.m[i] + (1 - self.___) * g  # 填入 beta1

            # TODO: 更新二阶矩估计 (自适应学习率)
            # v = β2 * v + (1 - β2) * g^2
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g ** ___  # 填入 2

            # TODO: 偏差修正
            m_hat = self.m[i] / (1 - self.beta1 ** self.___)  # 填入 t
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)

            # TODO: 更新参数
            # θ = θ - lr * m_hat / (√v_hat + ε)
            param.data = param.data - self.lr * m_hat / (torch.___(v_hat) + self.eps)  # 使用 sqrt

    def zero_grad(self):
        for param in self.params:
            if param.grad is not None:
                param.grad.zero_()


def test_optimizer(optimizer_class, optimizer_kwargs, name):
    """测试优化器"""
    # 简单的二次函数优化: f(x) = x^2
    x = torch.tensor([5.0], requires_grad=True)

    optimizer = optimizer_class([x], **optimizer_kwargs)

    initial_x = x.item()

    for _ in range(100):
        optimizer.zero_grad()
        loss = x ** 2  # 最小值在 x=0
        loss.backward()
        optimizer.step()

    final_x = x.item()

    print(f"{name}: {initial_x:.4f} -> {final_x:.4f}")
    return abs(final_x) < 0.1  # 应该接近 0


def compare_with_pytorch():
    """与 PyTorch 官方优化器比较"""
    print("\n与 PyTorch 官方优化器比较:")

    # 使用相同初始值
    torch.manual_seed(42)

    # 我们的 Adam
    x1 = torch.tensor([5.0], requires_grad=True)
    our_adam = SimpleAdam([x1], lr=0.1)

    # PyTorch Adam
    x2 = torch.tensor([5.0], requires_grad=True)
    torch_adam = torch.optim.Adam([x2], lr=0.1)

    for _ in range(50):
        # 我们的
        our_adam.zero_grad()
        loss1 = x1 ** 2
        loss1.backward()
        our_adam.step()

        # PyTorch
        torch_adam.zero_grad()
        loss2 = x2 ** 2
        loss2.backward()
        torch_adam.step()

    print(f"  我们的 Adam: {x1.item():.6f}")
    print(f"  PyTorch Adam: {x2.item():.6f}")

    return abs(x1.item() - x2.item()) < 0.01


def main():
    print("测试 SimpleSGD...")
    assert test_optimizer(SimpleSGD, {'lr': 0.1}, "SimpleSGD")
    print("✓ SimpleSGD 通过!")

    print("\n测试 SGDWithMomentum...")
    assert test_optimizer(SGDWithMomentum, {'lr': 0.1, 'momentum': 0.9}, "SGDWithMomentum")
    print("✓ SGDWithMomentum 通过!")

    print("\n测试 SimpleAdam...")
    assert test_optimizer(SimpleAdam, {'lr': 0.1}, "SimpleAdam")
    print("✓ SimpleAdam 通过!")

    assert compare_with_pytorch()
    print("✓ 与 PyTorch 结果一致!")

    print("\n🎉 所有测试通过！优化器掌握完成！")


if __name__ == "__main__":
    main()
