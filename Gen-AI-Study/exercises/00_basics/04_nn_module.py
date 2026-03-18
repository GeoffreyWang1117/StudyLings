"""
练习 04: nn.Module 基础

nn.Module 是 PyTorch 中所有神经网络的基类。
理解如何正确使用 nn.Module 是构建复杂模型的基础。

在这个练习中，你将学习：
- 如何继承 nn.Module
- 如何定义层（在 __init__ 中）
- 如何定义前向传播（在 forward 中）
- 如何访问模型参数
"""

import torch
import torch.nn as nn


class SimpleLinear(nn.Module):
    """一个简单的线性层封装"""

    def __init__(self, in_features, out_features):
        # TODO: 调用父类的初始化方法
        ___.__init__(self)  # 调用 super().__init__()

        # TODO: 定义一个线性层
        # 线性层执行 y = xW^T + b
        self.linear = nn.___(in_features, out_features)  # 使用 nn.Linear

    def forward(self, x):
        # TODO: 在前向传播中使用线性层
        return self.___(x)  # 调用 self.linear


class TwoLayerMLP(nn.Module):
    """两层多层感知机（MLP）"""

    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()

        # TODO: 定义第一个线性层（输入到隐藏）
        self.fc1 = nn.Linear(___, ___)  # 填入正确的维度

        # TODO: 定义激活函数
        self.relu = nn.___()  # 使用 ReLU

        # TODO: 定义第二个线性层（隐藏到输出）
        self.fc2 = nn.Linear(___, ___)  # 填入正确的维度

    def forward(self, x):
        # TODO: 实现前向传播
        # x -> fc1 -> relu -> fc2 -> output
        x = self.fc1(x)
        x = self.___(x)  # 应用激活函数
        x = self.___(x)  # 应用第二个线性层
        return x


class SequentialMLP(nn.Module):
    """使用 nn.Sequential 构建 MLP"""

    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()

        # TODO: 使用 nn.Sequential 定义整个网络
        self.network = nn.___(  # 使用 nn.Sequential
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        # TODO: 使用 Sequential 网络
        return self.___(x)  # 调用 self.network


def count_parameters(model):
    """计算模型的可训练参数数量"""
    # TODO: 遍历模型参数并计算总数
    # model.parameters() 返回所有参数的迭代器
    # 每个参数用 .numel() 获取元素数量
    total = 0
    for param in model.___():  # 使用 parameters() 方法
        total += param.___()  # 使用 numel() 方法
    return total


def get_named_parameters(model):
    """获取模型的命名参数"""
    # TODO: 返回一个字典，键是参数名，值是参数形状
    param_dict = {}
    for name, param in model.___():  # 使用 named_parameters() 方法
        param_dict[name] = param.shape
    return param_dict


def main():
    print("测试 SimpleLinear...")
    simple = SimpleLinear(10, 5)
    x = torch.randn(3, 10)
    y = simple(x)
    assert y.shape == (3, 5), f"期望形状 (3, 5)，得到 {y.shape}"
    print("✓ SimpleLinear 通过!")

    print("\n测试 TwoLayerMLP...")
    mlp = TwoLayerMLP(10, 20, 5)
    x = torch.randn(4, 10)
    y = mlp(x)
    assert y.shape == (4, 5), f"期望形状 (4, 5)，得到 {y.shape}"
    print("✓ TwoLayerMLP 通过!")

    print("\n测试 SequentialMLP...")
    seq_mlp = SequentialMLP(10, 20, 5)
    x = torch.randn(4, 10)
    y = seq_mlp(x)
    assert y.shape == (4, 5), f"期望形状 (4, 5)，得到 {y.shape}"
    print("✓ SequentialMLP 通过!")

    print("\n测试 count_parameters...")
    simple = SimpleLinear(10, 5)
    # Linear(10, 5) 有 10*5 + 5 = 55 个参数
    num_params = count_parameters(simple)
    assert num_params == 55, f"期望 55 个参数，得到 {num_params}"
    print("✓ count_parameters 通过!")

    print("\n测试 get_named_parameters...")
    simple = SimpleLinear(10, 5)
    params = get_named_parameters(simple)
    assert "linear.weight" in params, "应该包含 linear.weight"
    assert "linear.bias" in params, "应该包含 linear.bias"
    assert params["linear.weight"] == torch.Size([5, 10])
    assert params["linear.bias"] == torch.Size([5])
    print("✓ get_named_parameters 通过!")

    print("\n🎉 所有测试通过！nn.Module 基础掌握完成！")


if __name__ == "__main__":
    main()
