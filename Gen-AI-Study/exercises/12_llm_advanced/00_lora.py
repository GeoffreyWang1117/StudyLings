"""
练习 53: LoRA (Low-Rank Adaptation)

LoRA 是一种参数高效微调方法，通过低秩分解减少可训练参数。

原理：
- 冻结预训练权重 W
- 添加低秩分解: W' = W + BA
- B: (d, r), A: (r, k), r << min(d, k)
- 只训练 A 和 B

优势：
- 大幅减少可训练参数 (通常 <1%)
- 保持原模型能力
- 可以合并回原权重进行推理

在这个练习中，你将学习：
- LoRA 的数学原理
- 如何实现 LoRA 层
- 参数合并技术
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class LoRALinear(nn.Module):
    """
    带 LoRA 的线性层

    y = Wx + BAx
    其中 W 是冻结的，BA 是可训练的低秩矩阵
    """

    def __init__(self, in_features, out_features, rank=4, alpha=1.0):
        super().__init__()

        self.in_features = in_features
        self.out_features = out_features
        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank

        # 原始权重 (冻结)
        self.weight = nn.Parameter(torch.randn(out_features, in_features))
        self.weight.requires_grad = False  # 冻结

        # TODO: LoRA 分解矩阵
        # A: (rank, in_features), 用高斯初始化
        # B: (out_features, rank), 用零初始化
        self.lora_A = nn.Parameter(torch.randn(rank, ___))  # 填入 in_features
        self.lora_B = nn.Parameter(torch.zeros(out_features, ___))  # 填入 rank

        # 初始化 A
        nn.init.kaiming_uniform_(self.lora_A, a=math.sqrt(5))

    def forward(self, x):
        # 原始输出
        result = F.linear(x, self.weight)

        # TODO: LoRA 增量
        # Δ = x @ A^T @ B^T * scaling
        lora_out = F.linear(F.linear(x, self.lora_A), self.___) * self.scaling  # 填入 lora_B

        return result + lora_out

    def merge_weights(self):
        """将 LoRA 权重合并到原始权重"""
        # TODO: W' = W + scaling * B @ A
        merged = self.weight + self.___ * self.lora_B @ self.lora_A  # 填入 scaling
        return merged

    def get_lora_params(self):
        """获取 LoRA 参数数量"""
        return self.rank * (self.in_features + self.out_features)


class LoRAAttention(nn.Module):
    """
    带 LoRA 的多头注意力

    通常只对 Q, V 应用 LoRA (K 也可以)
    """

    def __init__(self, d_model, num_heads, rank=4, alpha=1.0):
        super().__init__()

        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        # 原始投影 (冻结)
        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model, bias=False)

        # 冻结原始权重
        for param in [self.W_q, self.W_k, self.W_v, self.W_o]:
            param.weight.requires_grad = False

        # TODO: 只对 Q 和 V 添加 LoRA
        self.lora_q = LoRALinear(d_model, d_model, rank, alpha)
        self.lora_v = LoRALinear(d_model, d_model, rank, ___)  # 填入 alpha

    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.shape

        # 使用 LoRA 增强的 Q, V
        Q = self.W_q(x) + self.lora_q(x) - F.linear(x, self.lora_q.weight)
        K = self.W_k(x)  # K 不使用 LoRA
        V = self.W_v(x) + self.lora_v(x) - F.linear(x, self.lora_v.weight)

        # 重塑为多头
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # 注意力计算
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))

        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, V)

        # 合并多头
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        out = self.W_o(out)

        return out


def apply_lora_to_model(model, rank=4, alpha=1.0, target_modules=['q_proj', 'v_proj']):
    """
    给模型添加 LoRA

    Args:
        model: 原始模型
        rank: LoRA 秩
        alpha: LoRA 缩放因子
        target_modules: 要应用 LoRA 的模块名
    """
    lora_params = []

    for name, module in model.named_modules():
        if any(target in name for target in target_modules):
            if isinstance(module, nn.Linear):
                # 创建 LoRA 版本
                lora_layer = LoRALinear(
                    module.in_features,
                    module.out_features,
                    rank=rank,
                    alpha=alpha
                )
                # 复制原始权重
                lora_layer.weight.data = module.weight.data.clone()

                # TODO: 收集 LoRA 参数
                lora_params.extend([lora_layer.lora_A, lora_layer.___])  # 填入 lora_B

    return lora_params


def count_parameters(model, trainable_only=True):
    """统计参数数量"""
    if trainable_only:
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
    return sum(p.numel() for p in model.parameters())


def main():
    print("测试 LoRALinear...")
    lora_linear = LoRALinear(512, 512, rank=8, alpha=16)

    x = torch.randn(2, 10, 512)
    y = lora_linear(x)
    assert y.shape == x.shape
    print(f"✓ 输入: {x.shape} -> 输出: {y.shape}")

    # 检查参数量
    total_params = 512 * 512  # 原始 Linear
    lora_params = lora_linear.get_lora_params()
    print(f"✓ 原始参数: {total_params}, LoRA 参数: {lora_params}")
    print(f"  参数比例: {lora_params/total_params*100:.2f}%")

    print("\n测试权重合并...")
    merged = lora_linear.merge_weights()
    assert merged.shape == lora_linear.weight.shape
    print("✓ 权重合并成功!")

    print("\n测试 LoRAAttention...")
    lora_attn = LoRAAttention(d_model=512, num_heads=8, rank=8)

    x = torch.randn(2, 20, 512)
    out = lora_attn(x)
    assert out.shape == x.shape
    print(f"✓ 注意力输出: {out.shape}")

    # 统计可训练参数
    trainable = count_parameters(lora_attn, trainable_only=True)
    total = count_parameters(lora_attn, trainable_only=False)
    print(f"✓ 可训练参数: {trainable}, 总参数: {total}")
    print(f"  比例: {trainable/total*100:.2f}%")

    print("\n验证 LoRA 初始化...")
    # B 初始化为 0，所以初始时 LoRA 输出应该为 0
    lora = LoRALinear(256, 256, rank=4)
    x = torch.randn(1, 10, 256)

    # 只有原始权重的输出
    original_out = F.linear(x, lora.weight)
    lora_out = lora(x)

    # 初始时应该相等
    diff = (lora_out - original_out).abs().max()
    print(f"✓ 初始化验证: 最大差异 = {diff:.6f} (应接近 0)")

    print("\n🎉 所有测试通过！LoRA 掌握完成！")


if __name__ == "__main__":
    main()
