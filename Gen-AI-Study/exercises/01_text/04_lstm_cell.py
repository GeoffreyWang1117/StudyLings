"""
练习 08: LSTM 单元 (LSTM Cell)

长短期记忆网络(LSTM)通过门控机制解决了 RNN 的梯度消失问题。
LSTM 有三个门：遗忘门、输入门、输出门，以及一个细胞状态。

LSTM 公式：
- 遗忘门: f_t = sigmoid(W_f @ [h_{t-1}, x_t] + b_f)
- 输入门: i_t = sigmoid(W_i @ [h_{t-1}, x_t] + b_i)
- 候选值: c̃_t = tanh(W_c @ [h_{t-1}, x_t] + b_c)
- 细胞状态: c_t = f_t * c_{t-1} + i_t * c̃_t
- 输出门: o_t = sigmoid(W_o @ [h_{t-1}, x_t] + b_o)
- 隐藏状态: h_t = o_t * tanh(c_t)

在这个练习中，你将学习：
- LSTM 的门控机制
- 细胞状态和隐藏状态的区别
- 为什么 LSTM 能解决梯度消失
"""

import torch
import torch.nn as nn


class SimpleLSTMCell(nn.Module):
    """
    简单的 LSTM 单元实现
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

        # 为了效率，我们将四个门的参数合并成一个大矩阵
        # 输出维度是 4 * hidden_size (f, i, o, c̃ 各占 hidden_size)

        # TODO: 定义输入到门的线性变换
        self.x2gates = nn.Linear(input_size, ___ * hidden_size)  # 填入 4

        # TODO: 定义隐藏状态到门的线性变换
        self.h2gates = nn.Linear(hidden_size, ___ * hidden_size)  # 填入 4

    def forward(self, x, state):
        """
        单步 LSTM 前向传播

        Args:
            x: 当前输入，形状 (batch_size, input_size)
            state: 上一步的状态 (h_prev, c_prev)
                   h_prev: (batch_size, hidden_size)
                   c_prev: (batch_size, hidden_size)

        Returns:
            h_new: 新的隐藏状态，形状 (batch_size, hidden_size)
            c_new: 新的细胞状态，形状 (batch_size, hidden_size)
        """
        h_prev, c_prev = state

        # 计算所有门的预激活值
        gates = self.x2gates(x) + self.h2gates(h_prev)

        # 分割成四个门
        # TODO: 将 gates 按照 hidden_size 分割成四部分
        f_gate, i_gate, o_gate, c_tilde = gates.chunk(___, dim=1)  # 填入分块数

        # TODO: 遗忘门 - 使用 sigmoid 激活
        # 决定从细胞状态中丢弃多少信息
        f_t = torch.___(f_gate)  # 使用 sigmoid

        # TODO: 输入门 - 使用 sigmoid 激活
        # 决定存储多少新信息
        i_t = torch.___(i_gate)  # 使用 sigmoid

        # TODO: 输出门 - 使用 sigmoid 激活
        # 决定输出多少信息
        o_t = torch.___(o_gate)  # 使用 sigmoid

        # TODO: 候选细胞值 - 使用 tanh 激活
        # 新的候选信息
        c_tilde_t = torch.___(c_tilde)  # 使用 tanh

        # TODO: 更新细胞状态
        # c_t = f_t * c_{t-1} + i_t * c̃_t
        c_new = f_t * ___ + i_t * ___  # 填入正确的变量

        # TODO: 计算隐藏状态
        # h_t = o_t * tanh(c_t)
        h_new = o_t * torch.___(c_new)  # 使用 tanh

        return h_new, c_new


class SimpleLSTM(nn.Module):
    """
    完整的 LSTM 层，处理整个序列
    """

    def __init__(self, input_size, hidden_size):
        super().__init__()

        self.hidden_size = hidden_size
        self.lstm_cell = SimpleLSTMCell(input_size, hidden_size)

    def forward(self, x, state=None):
        """
        处理整个序列

        Args:
            x: 输入序列，形状 (batch_size, seq_len, input_size)
            state: 初始状态 (h_0, c_0)

        Returns:
            output: 所有时间步的隐藏状态，形状 (batch_size, seq_len, hidden_size)
            (h_n, c_n): 最后一个时间步的状态
        """
        batch_size, seq_len, _ = x.shape

        # 初始化状态
        if state is None:
            h = torch.zeros(batch_size, self.hidden_size, device=x.device)
            c = torch.zeros(batch_size, self.hidden_size, device=x.device)
        else:
            h, c = state

        outputs = []

        # 遍历序列
        for t in range(seq_len):
            x_t = x[:, t, :]
            # TODO: 更新状态
            h, c = self.___(x_t, (h, c))  # 调用 lstm_cell
            outputs.append(h)

        # TODO: 堆叠输出
        output = torch.stack(outputs, dim=___)  # 填入正确的维度

        return output, (h, c)


def understand_gates():
    """
    理解门的作用

    这个函数演示了 LSTM 各个门的功能
    """
    hidden_size = 4

    # 模拟各个门的值
    f_t = torch.tensor([1.0, 1.0, 0.0, 0.0])  # 遗忘门：前两个记住，后两个遗忘
    i_t = torch.tensor([0.0, 0.0, 1.0, 1.0])  # 输入门：后两个接收新信息
    o_t = torch.tensor([1.0, 1.0, 1.0, 1.0])  # 输出门：全部输出

    c_prev = torch.tensor([0.5, 0.5, 0.5, 0.5])  # 旧的细胞状态
    c_tilde = torch.tensor([0.0, 0.0, 0.8, 0.8])  # 新的候选值

    # TODO: 计算新的细胞状态
    c_new = f_t * c_prev + ___ * ___  # 填入 i_t 和 c_tilde

    # 预期结果：[0.5, 0.5, 0.8, 0.8]
    # - 前两个维度被遗忘门保留了旧值
    # - 后两个维度被输入门更新为新值

    return c_new


def main():
    print("测试 SimpleLSTMCell...")
    cell = SimpleLSTMCell(input_size=10, hidden_size=20)
    x = torch.randn(4, 10)
    h = torch.zeros(4, 20)
    c = torch.zeros(4, 20)
    h_new, c_new = cell(x, (h, c))
    assert h_new.shape == (4, 20), f"期望 h 形状 (4, 20)，得到 {h_new.shape}"
    assert c_new.shape == (4, 20), f"期望 c 形状 (4, 20)，得到 {c_new.shape}"
    print("✓ SimpleLSTMCell 通过!")

    print("\n测试 SimpleLSTM...")
    lstm = SimpleLSTM(input_size=10, hidden_size=20)
    x = torch.randn(4, 8, 10)  # (batch=4, seq_len=8, input_size=10)
    output, (h_n, c_n) = lstm(x)
    assert output.shape == (4, 8, 20), f"期望形状 (4, 8, 20)，得到 {output.shape}"
    assert h_n.shape == (4, 20)
    assert c_n.shape == (4, 20)
    # 最后一个输出应该等于 h_n
    assert torch.allclose(h_n, output[:, -1, :])
    print("✓ SimpleLSTM 通过!")

    print("\n测试 understand_gates...")
    c_new = understand_gates()
    expected = torch.tensor([0.5, 0.5, 0.8, 0.8])
    assert torch.allclose(c_new, expected), f"期望 {expected}，得到 {c_new}"
    print("✓ understand_gates 通过!")

    print("\n🎉 所有测试通过！LSTM 掌握完成！")


if __name__ == "__main__":
    main()
