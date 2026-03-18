"""
练习 12: 因果掩码 (Causal Mask)

因果掩码确保模型只能看到当前位置之前的信息。
这对于自回归生成（如 GPT）至关重要，因为在生成时我们不能"偷看"未来。

因果掩码的结构：
位置 0 可以看到: [0]
位置 1 可以看到: [0, 1]
位置 2 可以看到: [0, 1, 2]
...

掩码矩阵（True 表示需要掩盖）：
[[False, True,  True,  True ],
 [False, False, True,  True ],
 [False, False, False, True ],
 [False, False, False, False]]

在这个练习中，你将学习：
- 为什么需要因果掩码
- 如何创建因果掩码
- 掩码在注意力中的应用
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


def create_causal_mask(seq_len):
    """
    创建因果掩码（上三角掩码）

    Args:
        seq_len: 序列长度

    Returns:
        mask: 布尔掩码，形状 (seq_len, seq_len)
              True 表示该位置应被掩盖
    """
    # TODO: 创建上三角矩阵（不包含对角线）
    # 使用 torch.triu 创建上三角矩阵
    # diagonal=1 表示从主对角线上方一行开始
    ones = torch.ones(seq_len, seq_len)
    mask = torch.___(ones, diagonal=___).bool()  # 使用 triu，填入 diagonal 参数

    return mask


def create_causal_mask_efficient(seq_len, device='cpu'):
    """
    更高效的因果掩码创建方式

    Args:
        seq_len: 序列长度
        device: 设备

    Returns:
        mask: 布尔掩码
    """
    # TODO: 使用索引比较创建掩码
    # 位置 i 不能看到位置 j，当 j > i
    i = torch.arange(seq_len, device=device).unsqueeze(1)  # (seq_len, 1)
    j = torch.arange(seq_len, device=device).unsqueeze(0)  # (1, seq_len)

    # TODO: 掩码条件：j > i
    mask = j ___ i  # 填入比较运算符

    return mask


def apply_causal_mask(scores, mask):
    """
    将因果掩码应用到注意力分数

    Args:
        scores: 注意力分数，形状 (batch_size, num_heads, seq_len, seq_len)
        mask: 因果掩码，形状 (seq_len, seq_len)

    Returns:
        masked_scores: 掩码后的分数
    """
    # TODO: 将掩码位置设为负无穷
    # 使用 masked_fill 方法
    masked_scores = scores.masked_fill(mask, float("___"))  # 填入负无穷表示

    return masked_scores


class CausalSelfAttention(nn.Module):
    """
    带因果掩码的自注意力

    这是 GPT 类模型的核心组件
    """

    def __init__(self, d_model, num_heads, max_seq_len=512):
        super().__init__()

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

        # TODO: 预先注册因果掩码作为 buffer
        # 这样掩码会随模型一起保存和移动到正确的设备
        causal_mask = create_causal_mask(max_seq_len)
        self.___("causal_mask", causal_mask)  # 使用 register_buffer

    def forward(self, x):
        """
        Args:
            x: 输入，形状 (batch_size, seq_len, d_model)

        Returns:
            output: 形状 (batch_size, seq_len, d_model)
        """
        batch_size, seq_len, _ = x.shape

        # 线性投影
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)

        # 分割多头
        Q = Q.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)

        # 计算注意力分数
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        # TODO: 应用因果掩码
        # 只取当前序列长度的掩码部分
        mask = self.causal_mask[:seq_len, :___]  # 填入正确的切片
        scores = apply_causal_mask(scores, mask)

        # Softmax 和加权求和
        attention_weights = F.softmax(scores, dim=-1)
        attention_output = torch.matmul(attention_weights, V)

        # 合并头并输出投影
        attention_output = attention_output.transpose(1, 2).contiguous()
        attention_output = attention_output.view(batch_size, seq_len, self.d_model)
        output = self.W_o(attention_output)

        return output, attention_weights


def visualize_causal_attention():
    """
    可视化因果注意力的效果

    展示每个位置只能注意到之前的位置
    """
    seq_len = 4

    # 创建因果掩码
    mask = create_causal_mask(seq_len)

    # 创建简单的注意力分数（全 1）
    scores = torch.ones(1, 1, seq_len, seq_len)

    # 应用掩码
    masked_scores = apply_causal_mask(scores, mask)

    # TODO: 计算注意力权重
    attention_weights = F.___(masked_scores, dim=-1)  # 使用 softmax

    # 验证每行的注意力分布
    # 第 0 行：只能看位置 0，所以是 [1, 0, 0, 0]
    # 第 1 行：只能看位置 0,1，所以是 [0.5, 0.5, 0, 0]
    # ...

    return attention_weights.squeeze()


def sliding_window_mask(seq_len, window_size):
    """
    创建滑动窗口掩码

    有些模型（如 Longformer）使用滑动窗口来限制注意力范围，
    每个位置只能看到窗口内的位置

    Args:
        seq_len: 序列长度
        window_size: 窗口大小（单侧）

    Returns:
        mask: 布尔掩码
    """
    i = torch.arange(seq_len).unsqueeze(1)
    j = torch.arange(seq_len).unsqueeze(0)

    # TODO: 计算距离，超出窗口范围的位置需要掩盖
    distance = torch.___(j - i)  # 使用 abs 计算绝对距离

    # TODO: 超出窗口的位置应该被掩盖
    mask = distance ___ window_size  # 填入比较运算符（>）

    return mask


def main():
    print("测试 create_causal_mask...")
    mask = create_causal_mask(4)
    expected = torch.tensor([
        [False, True, True, True],
        [False, False, True, True],
        [False, False, False, True],
        [False, False, False, False]
    ])
    assert torch.equal(mask, expected), f"期望:\n{expected}\n得到:\n{mask}"
    print("✓ create_causal_mask 通过!")

    print("\n测试 create_causal_mask_efficient...")
    mask2 = create_causal_mask_efficient(4)
    assert torch.equal(mask, mask2), "两种方法应该产生相同的掩码"
    print("✓ create_causal_mask_efficient 通过!")

    print("\n测试 apply_causal_mask...")
    scores = torch.ones(1, 1, 4, 4)
    masked = apply_causal_mask(scores, mask)
    assert masked[0, 0, 0, 1] == float('-inf'), "掩码位置应该是负无穷"
    assert masked[0, 0, 0, 0] == 1.0, "非掩码位置应该保持原值"
    print("✓ apply_causal_mask 通过!")

    print("\n测试 CausalSelfAttention...")
    attn = CausalSelfAttention(d_model=64, num_heads=8)
    x = torch.randn(2, 10, 64)
    output, weights = attn(x)
    assert output.shape == (2, 10, 64)
    # 验证因果性：位置 i 对位置 j>i 的注意力应该是 0
    for i in range(10):
        for j in range(i + 1, 10):
            assert weights[0, 0, i, j] < 1e-6, f"位置 {i} 不应该注意位置 {j}"
    print("✓ CausalSelfAttention 通过!")

    print("\n测试 visualize_causal_attention...")
    weights = visualize_causal_attention()
    # 验证注意力分布
    assert torch.allclose(weights[0], torch.tensor([1.0, 0.0, 0.0, 0.0]))
    assert torch.allclose(weights[1], torch.tensor([0.5, 0.5, 0.0, 0.0]))
    print("✓ visualize_causal_attention 通过!")

    print("\n测试 sliding_window_mask...")
    window_mask = sliding_window_mask(6, window_size=2)
    # 位置 0 和位置 4 距离是 4，超过窗口 2，应该被掩盖
    assert window_mask[0, 4] == True
    # 位置 0 和位置 1 距离是 1，在窗口内
    assert window_mask[0, 1] == False
    print("✓ sliding_window_mask 通过!")

    print("\n🎉 所有测试通过！因果掩码掌握完成！")


if __name__ == "__main__":
    main()
