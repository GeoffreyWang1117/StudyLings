"""
练习 56: 混合专家 (Mixture of Experts, MoE)

MoE 通过稀疏激活增加模型容量而不显著增加计算量。

核心思想：
- 多个"专家"网络 (通常是 FFN)
- 门控网络选择 top-k 个专家
- 只激活选中的专家进行计算

优势：
- 大幅增加模型容量 (参数量)
- 计算量只略微增加 (稀疏激活)
- 每个 token 只使用部分专家

在这个练习中，你将学习：
- MoE 层的实现
- 门控机制 (Top-K Gating)
- 负载均衡损失
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Expert(nn.Module):
    """单个专家网络 (简单 FFN)"""

    def __init__(self, d_model, d_ff):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)

    def forward(self, x):
        # TODO: 实现 FFN
        return self.fc2(F.gelu(self.___(x)))  # 填入 fc1


class TopKGating(nn.Module):
    """
    Top-K 门控网络

    选择 top-k 个专家处理每个 token
    """

    def __init__(self, d_model, num_experts, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k

        # 门控投影
        self.gate = nn.Linear(d_model, num_experts, bias=False)

    def forward(self, x):
        """
        Args:
            x: (batch, seq_len, d_model)

        Returns:
            gates: (batch, seq_len, top_k) - 归一化权重
            indices: (batch, seq_len, top_k) - 选中的专家索引
        """
        # 计算门控分数
        logits = self.gate(x)  # (batch, seq_len, num_experts)

        # TODO: 选择 top-k 专家
        top_k_logits, indices = torch.topk(logits, self.___, dim=-1)  # 填入 top_k

        # TODO: 对选中的专家计算 softmax 权重
        gates = F.softmax(top_k_logits, dim=___)  # 填入 -1

        return gates, indices


class MoELayer(nn.Module):
    """
    混合专家层

    每个 token 由 top-k 个专家处理，结果加权求和
    """

    def __init__(self, d_model, d_ff, num_experts=8, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k

        # 创建专家
        self.experts = nn.ModuleList([
            Expert(d_model, d_ff) for _ in range(num_experts)
        ])

        # 门控网络
        self.gating = TopKGating(d_model, num_experts, top_k)

    def forward(self, x):
        """
        Args:
            x: (batch, seq_len, d_model)

        Returns:
            output: (batch, seq_len, d_model)
        """
        batch_size, seq_len, d_model = x.shape

        # 获取门控权重和专家索引
        gates, indices = self.gating(x)  # gates: (B, S, K), indices: (B, S, K)

        # 初始化输出
        output = torch.zeros_like(x)

        # 对每个专家计算输出
        for expert_idx in range(self.num_experts):
            # 找出选择了这个专家的位置
            # TODO: 创建专家掩码
            mask = (indices == ___).any(dim=-1)  # 填入 expert_idx

            if not mask.any():
                continue

            # 获取选择这个专家的 token
            expert_input = x[mask]

            if expert_input.shape[0] == 0:
                continue

            # 计算专家输出
            expert_output = self.experts[expert_idx](expert_input)

            # 获取对应的权重
            # 找出这个专家在 top-k 中的位置
            expert_mask = (indices == expert_idx)
            weights = (gates * expert_mask.float()).sum(dim=-1)  # (B, S)

            # 加权累加到输出
            output[mask] += expert_output * weights[mask].unsqueeze(-1)

        return output


class SimplifiedMoE(nn.Module):
    """
    简化版 MoE (便于理解)

    循环遍历专家，效率较低但逻辑清晰
    """

    def __init__(self, d_model, d_ff, num_experts=4, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.d_model = d_model

        self.experts = nn.ModuleList([
            Expert(d_model, d_ff) for _ in range(num_experts)
        ])
        self.gate = nn.Linear(d_model, num_experts)

    def forward(self, x):
        batch_size, seq_len, _ = x.shape
        x_flat = x.view(-1, self.d_model)

        # 门控
        logits = self.gate(x_flat)
        top_k_logits, top_k_indices = torch.topk(logits, self.top_k, dim=-1)
        top_k_gates = F.softmax(top_k_logits, dim=-1)

        # 收集每个专家需要处理的 token
        output = torch.zeros_like(x_flat)

        for i in range(self.top_k):
            expert_idx = top_k_indices[:, i]  # 每个 token 选择的第 i 个专家
            gate_weight = top_k_gates[:, i]   # 对应的权重

            for e in range(self.num_experts):
                mask = (expert_idx == e)
                if mask.any():
                    expert_input = x_flat[mask]
                    # TODO: 计算专家输出并加权
                    expert_output = self.experts[e](expert_input)
                    output[mask] += expert_output * gate_weight[mask].unsqueeze(___)  # 填入 -1

        return output.view(batch_size, seq_len, -1)


def load_balance_loss(gates, indices, num_experts):
    """
    负载均衡损失

    鼓励专家被均匀使用，防止某些专家过载

    L = num_experts * Σ f_i * P_i
    其中:
    - f_i: 分配给专家 i 的 token 比例
    - P_i: 专家 i 的平均门控概率
    """
    batch_size, seq_len, top_k = indices.shape

    # 计算每个专家被选中的频率
    one_hot = F.one_hot(indices, num_experts).float()  # (B, S, K, E)
    # TODO: 计算 f_i
    f = one_hot.sum(dim=(0, 1, 2)) / (batch_size * seq_len * ___)  # 填入 top_k

    # 计算平均门控概率
    # 扩展 gates 以匹配 one_hot
    gates_expanded = gates.unsqueeze(-1)  # (B, S, K, 1)
    P = (gates_expanded * one_hot).sum(dim=(0, 1, 2)) / (batch_size * seq_len * top_k)

    # TODO: 计算负载均衡损失
    loss = num_experts * (f * ___).sum()  # 填入 P

    return loss


def router_z_loss(logits):
    """
    Router Z-Loss

    惩罚门控 logits 过大，提高训练稳定性
    """
    # TODO: 计算 z-loss
    z_loss = torch.logsumexp(logits, dim=-1).square().___()  # 使用 mean
    return z_loss


def main():
    torch.manual_seed(42)

    print("测试 Expert...")
    expert = Expert(d_model=256, d_ff=1024)
    x = torch.randn(2, 10, 256)
    out = expert(x)
    assert out.shape == x.shape
    print(f"✓ Expert 输出: {out.shape}")

    print("\n测试 TopKGating...")
    gating = TopKGating(d_model=256, num_experts=8, top_k=2)
    gates, indices = gating(x)
    assert gates.shape == (2, 10, 2)
    assert indices.shape == (2, 10, 2)
    print(f"✓ Gates: {gates.shape}, Indices: {indices.shape}")

    # 验证 gates 归一化
    assert torch.allclose(gates.sum(dim=-1), torch.ones(2, 10), atol=1e-5)
    print("✓ Gates 已归一化")

    print("\n测试 MoELayer...")
    moe = MoELayer(d_model=256, d_ff=1024, num_experts=8, top_k=2)
    out = moe(x)
    assert out.shape == x.shape
    print(f"✓ MoE 输出: {out.shape}")

    print("\n测试 SimplifiedMoE...")
    simple_moe = SimplifiedMoE(d_model=256, d_ff=1024, num_experts=4, top_k=2)
    out = simple_moe(x)
    assert out.shape == x.shape
    print(f"✓ SimplifiedMoE 输出: {out.shape}")

    print("\n测试负载均衡损失...")
    lb_loss = load_balance_loss(gates, indices, num_experts=8)
    print(f"✓ 负载均衡损失: {lb_loss:.4f}")

    print("\n测试 Router Z-Loss...")
    logits = gating.gate(x)
    z_loss = router_z_loss(logits)
    print(f"✓ Z-Loss: {z_loss:.4f}")

    print("\n参数量分析:")
    # MoE 的优势: 参数多但计算稀疏
    d_model, d_ff = 4096, 16384
    num_experts, top_k = 8, 2

    dense_params = d_model * d_ff * 2  # 标准 FFN
    moe_params = num_experts * d_model * d_ff * 2  # MoE 参数
    moe_active = top_k * d_model * d_ff * 2  # MoE 每次激活的参数

    print(f"  Dense FFN 参数: {dense_params:,}")
    print(f"  MoE 总参数: {moe_params:,} ({moe_params/dense_params:.1f}x)")
    print(f"  MoE 激活参数: {moe_active:,} ({moe_active/dense_params:.1f}x)")

    print("\n🎉 所有测试通过！MoE 掌握完成！")


if __name__ == "__main__":
    main()
