"""
练习 09: GRU 单元 (Gated Recurrent Unit)

GRU 是 LSTM 的简化版本，使用更少的门控但效果相近。

GRU 门控：
- 更新门 (Update Gate): z = σ(W_z·[h, x])
- 重置门 (Reset Gate): r = σ(W_r·[h, x])
- 候选状态: h̃ = tanh(W_h·[r*h, x])
- 新状态: h = (1-z)*h + z*h̃

相比 LSTM：
- 2 个门 vs 3 个门
- 无细胞状态，只有隐藏状态
- 参数更少，计算更快

在这个练习中，你将学习：
- GRU 的门控机制
- 与 LSTM 的对比
- 梯度流动分析
"""

import torch
import torch.nn as nn


class GRUCell(nn.Module):
    """
    GRU 单元

    z = σ(W_iz·x + W_hz·h + b_z)     # 更新门
    r = σ(W_ir·x + W_hr·h + b_r)     # 重置门
    h̃ = tanh(W_ih·x + W_hh·(r*h) + b_h)  # 候选状态
    h' = (1-z)*h + z*h̃               # 新状态
    """

    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size

        # 输入到隐藏层的权重
        self.W_iz = nn.Linear(input_size, hidden_size)
        self.W_ir = nn.Linear(input_size, hidden_size)
        self.W_ih = nn.Linear(input_size, hidden_size)

        # 隐藏层到隐藏层的权重
        self.W_hz = nn.Linear(hidden_size, hidden_size)
        self.W_hr = nn.Linear(hidden_size, hidden_size)
        self.W_hh = nn.Linear(hidden_size, hidden_size)

    def forward(self, x, h=None):
        """
        Args:
            x: 输入 (batch_size, input_size)
            h: 隐藏状态 (batch_size, hidden_size)

        Returns:
            h_new: 新隐藏状态
        """
        if h is None:
            h = torch.zeros(x.size(0), self.hidden_size, device=x.device)

        # TODO: 计算更新门
        z = torch.sigmoid(self.W_iz(x) + self.___(h))  # 填入 W_hz

        # TODO: 计算重置门
        r = torch.sigmoid(self.W_ir(x) + self.W_hr(h))

        # TODO: 计算候选隐藏状态
        # 注意: 重置门用于控制历史信息的保留程度
        h_tilde = torch.tanh(self.W_ih(x) + self.W_hh(___ * h))  # 填入 r

        # TODO: 计算新隐藏状态
        # h_new = (1-z)*h + z*h_tilde
        h_new = (1 - z) * h + ___ * h_tilde  # 填入 z

        return h_new


class GRU(nn.Module):
    """
    多层 GRU
    """

    def __init__(self, input_size, hidden_size, num_layers=1):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # 第一层
        self.cells = nn.ModuleList([GRUCell(input_size, hidden_size)])

        # 后续层
        for _ in range(num_layers - 1):
            self.cells.append(GRUCell(hidden_size, hidden_size))

    def forward(self, x, h=None):
        """
        Args:
            x: 输入序列 (seq_len, batch_size, input_size)
            h: 初始隐藏状态 (num_layers, batch_size, hidden_size)

        Returns:
            output: 所有时间步的输出 (seq_len, batch_size, hidden_size)
            h_n: 最后的隐藏状态 (num_layers, batch_size, hidden_size)
        """
        seq_len, batch_size, _ = x.shape

        if h is None:
            h = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=x.device)

        h_list = list(h)
        outputs = []

        for t in range(seq_len):
            x_t = x[t]
            for layer_idx, cell in enumerate(self.cells):
                h_list[layer_idx] = cell(x_t, h_list[layer_idx])
                x_t = h_list[layer_idx]

            outputs.append(x_t)

        output = torch.stack(outputs, dim=0)
        h_n = torch.stack(h_list, dim=0)

        return output, h_n


class BidirectionalGRU(nn.Module):
    """
    双向 GRU

    正向和反向各跑一遍，拼接输出
    """

    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.forward_gru = GRU(input_size, hidden_size)
        self.backward_gru = GRU(input_size, hidden_size)
        self.hidden_size = hidden_size

    def forward(self, x):
        """
        Args:
            x: (seq_len, batch, input_size)

        Returns:
            output: (seq_len, batch, hidden_size * 2)
        """
        # 正向
        output_forward, _ = self.forward_gru(x)

        # TODO: 反向 (翻转序列)
        x_reversed = torch.flip(x, dims=[___])  # 填入 0 (沿序列维度翻转)
        output_backward, _ = self.backward_gru(x_reversed)
        output_backward = torch.flip(output_backward, dims=[0])

        # TODO: 拼接
        output = torch.___(output_forward, output_backward], dim=-1)  # 使用 cat

        return output


def compare_gru_lstm():
    """比较 GRU 和 LSTM 的参数量"""
    input_size = 256
    hidden_size = 512

    # GRU: 3 个门 (z, r, h), 每个门有 2 组权重
    gru_params = 3 * (input_size * hidden_size + hidden_size * hidden_size + hidden_size)

    # LSTM: 4 个门 (i, f, o, g)
    lstm_params = 4 * (input_size * hidden_size + hidden_size * hidden_size + hidden_size)

    print(f"GRU 参数量: {gru_params:,}")
    print(f"LSTM 参数量: {lstm_params:,}")
    print(f"GRU 是 LSTM 的 {gru_params/lstm_params*100:.1f}%")


def main():
    torch.manual_seed(42)

    print("测试 GRUCell...")
    cell = GRUCell(input_size=128, hidden_size=256)
    x = torch.randn(32, 128)
    h = torch.randn(32, 256)

    h_new = cell(x, h)
    assert h_new.shape == (32, 256)
    print(f"✓ GRUCell 输出: {h_new.shape}")

    print("\n测试 GRU (多时间步)...")
    gru = GRU(input_size=128, hidden_size=256, num_layers=2)
    x_seq = torch.randn(20, 32, 128)

    output, h_n = gru(x_seq)
    assert output.shape == (20, 32, 256)
    assert h_n.shape == (2, 32, 256)
    print(f"✓ GRU 输出: {output.shape}, 隐藏状态: {h_n.shape}")

    print("\n与 PyTorch GRU 比较...")
    torch_gru = nn.GRU(128, 256, num_layers=2)
    torch_output, torch_h_n = torch_gru(x_seq)
    print(f"✓ PyTorch GRU 输出: {torch_output.shape}")

    print("\n测试双向 GRU...")
    bi_gru = BidirectionalGRU(input_size=128, hidden_size=256)
    output = bi_gru(x_seq)
    assert output.shape == (20, 32, 512)  # hidden_size * 2
    print(f"✓ 双向 GRU 输出: {output.shape}")

    print("\nGRU vs LSTM 参数对比:")
    compare_gru_lstm()

    print("\n🎉 所有测试通过！GRU 掌握完成！")


if __name__ == "__main__":
    main()
