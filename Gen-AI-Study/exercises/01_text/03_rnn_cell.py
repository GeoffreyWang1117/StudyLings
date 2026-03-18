"""
练习 07: RNN 单元 (RNN Cell)

循环神经网络(RNN)通过隐藏状态来处理序列数据。
每个时间步，RNN 会根据当前输入和上一步的隐藏状态计算新的隐藏状态。

RNN 公式：
h_t = tanh(W_ih @ x_t + b_ih + W_hh @ h_{t-1} + b_hh)

在这个练习中，你将学习：
- RNN 的基本原理
- 如何实现 RNN 单元
- 理解隐藏状态的作用
"""

import torch
import torch.nn as nn


class SimpleRNNCell(nn.Module):
    """
    简单的 RNN 单元实现

    数学公式：
    h_t = tanh(x_t @ W_ih^T + h_{t-1} @ W_hh^T + b)
    """

    def __init__(self, input_size, hidden_size):
        """
        Args:
            input_size: 输入特征维度
            hidden_size: 隐藏状态维度
        """
        super().__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size

        # TODO: 定义输入到隐藏的线性变换
        # 输入: (input_size), 输出: (hidden_size)
        self.i2h = nn.___(input_size, hidden_size)  # 使用 nn.Linear

        # TODO: 定义隐藏到隐藏的线性变换
        # 输入: (hidden_size), 输出: (hidden_size)
        self.h2h = nn.___(hidden_size, hidden_size)  # 使用 nn.Linear

    def forward(self, x, h_prev):
        """
        单步 RNN 前向传播

        Args:
            x: 当前时间步的输入，形状 (batch_size, input_size)
            h_prev: 上一时间步的隐藏状态，形状 (batch_size, hidden_size)

        Returns:
            h_new: 新的隐藏状态，形状 (batch_size, hidden_size)
        """
        # TODO: 计算新的隐藏状态
        # h_t = tanh(W_ih @ x_t + W_hh @ h_{t-1})
        h_new = torch.___(self.i2h(x) + self.h2h(h_prev))  # 使用 tanh 激活

        return h_new


class SimpleRNN(nn.Module):
    """
    完整的 RNN 层，处理整个序列
    """

    def __init__(self, input_size, hidden_size):
        super().__init__()

        self.hidden_size = hidden_size

        # TODO: 创建 RNN 单元
        self.rnn_cell = ___(input_size, hidden_size)  # 使用 SimpleRNNCell

    def forward(self, x, h_0=None):
        """
        处理整个序列

        Args:
            x: 输入序列，形状 (batch_size, seq_len, input_size)
            h_0: 初始隐藏状态，形状 (batch_size, hidden_size)
                 如果为 None，使用全零初始化

        Returns:
            output: 所有时间步的隐藏状态，形状 (batch_size, seq_len, hidden_size)
            h_n: 最后一个时间步的隐藏状态，形状 (batch_size, hidden_size)
        """
        batch_size, seq_len, _ = x.shape

        # 初始化隐藏状态
        if h_0 is None:
            h_0 = torch.zeros(batch_size, self.hidden_size, device=x.device)

        # 存储所有时间步的输出
        outputs = []
        h = h_0

        # TODO: 遍历序列的每个时间步
        for t in range(___):  # 填入循环次数
            # 获取当前时间步的输入
            x_t = x[:, t, :]

            # TODO: 计算当前时间步的隐藏状态
            h = self.___(x_t, h)  # 调用 rnn_cell

            outputs.append(h)

        # TODO: 将输出列表堆叠成张量
        # 形状: (batch_size, seq_len, hidden_size)
        output = torch.___(outputs, dim=1)  # 使用 stack

        return output, h


def compare_with_pytorch_rnn():
    """
    将我们的实现与 PyTorch 官方 RNN 对比
    """
    input_size = 10
    hidden_size = 20
    batch_size = 3
    seq_len = 5

    # 创建我们的 RNN
    our_rnn = SimpleRNN(input_size, hidden_size)

    # 创建 PyTorch 的 RNN
    # TODO: 使用 nn.RNN 创建官方 RNN
    # batch_first=True 表示输入形状是 (batch, seq, feature)
    pytorch_rnn = nn.___(input_size, hidden_size, batch_first=True)  # 使用 nn.RNN

    # 创建测试输入
    x = torch.randn(batch_size, seq_len, input_size)

    # 运行我们的 RNN
    our_output, our_h_n = our_rnn(x)

    # 运行 PyTorch RNN
    pytorch_output, pytorch_h_n = pytorch_rnn(x)

    # 形状应该匹配
    assert our_output.shape == pytorch_output.shape
    assert our_h_n.shape == pytorch_h_n.squeeze(0).shape

    return True


def main():
    print("测试 SimpleRNNCell...")
    cell = SimpleRNNCell(input_size=10, hidden_size=20)
    x = torch.randn(4, 10)  # (batch=4, input_size=10)
    h = torch.zeros(4, 20)  # (batch=4, hidden_size=20)
    h_new = cell(x, h)
    assert h_new.shape == (4, 20), f"期望形状 (4, 20)，得到 {h_new.shape}"
    # 验证输出在 [-1, 1] 范围内（tanh 的输出范围）
    assert h_new.min() >= -1.0 and h_new.max() <= 1.0
    print("✓ SimpleRNNCell 通过!")

    print("\n测试 SimpleRNN...")
    rnn = SimpleRNN(input_size=10, hidden_size=20)
    x = torch.randn(4, 8, 10)  # (batch=4, seq_len=8, input_size=10)
    output, h_n = rnn(x)
    assert output.shape == (4, 8, 20), f"期望形状 (4, 8, 20)，得到 {output.shape}"
    assert h_n.shape == (4, 20), f"期望形状 (4, 20)，得到 {h_n.shape}"
    # h_n 应该等于 output 的最后一个时间步
    assert torch.allclose(h_n, output[:, -1, :])
    print("✓ SimpleRNN 通过!")

    print("\n测试与 PyTorch RNN 对比...")
    result = compare_with_pytorch_rnn()
    assert result
    print("✓ 形状与 PyTorch RNN 一致!")

    print("\n🎉 所有测试通过！RNN 基础掌握完成！")


if __name__ == "__main__":
    main()
