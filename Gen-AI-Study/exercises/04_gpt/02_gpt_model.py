"""
练习 18: GPT 模型架构

GPT (Generative Pre-trained Transformer) 是基于 Transformer 解码器的自回归语言模型。
它通过预测下一个 token 来学习语言表示。

GPT 架构:
Token Embedding + Position Embedding
    ↓
N × Transformer Decoder Block
    ↓
Layer Norm
    ↓
LM Head (Linear to vocab)

在这个练习中，你将学习：
- 完整 GPT 架构的细节
- 权重初始化策略
- 参数量计算
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class GPTConfig:
    """GPT 配置类"""

    def __init__(
        self,
        vocab_size=50257,    # GPT-2 词表大小
        max_seq_len=1024,
        d_model=768,
        num_heads=12,
        num_layers=12,
        d_ff=None,           # 默认 4 * d_model
        dropout=0.1,
        bias=True,           # 是否使用偏置
    ):
        self.vocab_size = vocab_size
        self.max_seq_len = max_seq_len
        self.d_model = d_model
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.d_ff = d_ff if d_ff is not None else 4 * d_model
        self.dropout = dropout
        self.bias = bias


class CausalSelfAttention(nn.Module):
    """因果自注意力"""

    def __init__(self, config):
        super().__init__()

        assert config.d_model % config.num_heads == 0

        self.num_heads = config.num_heads
        self.d_model = config.d_model
        self.d_k = config.d_model // config.num_heads

        # TODO: QKV 合并投影（更高效）
        self.c_attn = nn.Linear(config.d_model, ___ * config.d_model, bias=config.bias)

        # 输出投影
        self.c_proj = nn.Linear(config.d_model, config.d_model, bias=config.bias)

        # Dropout
        self.attn_dropout = nn.Dropout(config.dropout)
        self.proj_dropout = nn.Dropout(config.dropout)

        # 因果掩码
        mask = torch.triu(torch.ones(config.max_seq_len, config.max_seq_len), diagonal=1).bool()
        self.register_buffer('causal_mask', mask)

    def forward(self, x):
        batch_size, seq_len, _ = x.shape

        # TODO: 一次计算 Q, K, V
        qkv = self.c_attn(x)

        # TODO: 分割成 Q, K, V
        q, k, v = qkv.split(self.d_model, dim=___)  # 填入正确的维度

        # 重塑为多头
        q = q.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        k = k.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        v = v.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)

        # 缩放点积注意力
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_k)
        scores = scores.masked_fill(self.causal_mask[:seq_len, :seq_len], float('-inf'))
        attn = self.attn_dropout(F.softmax(scores, dim=-1))
        output = torch.matmul(attn, v)

        # 合并头
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)

        return self.proj_dropout(self.c_proj(output))


class MLP(nn.Module):
    """GPT 的 MLP 层"""

    def __init__(self, config):
        super().__init__()

        # TODO: 第一个线性层（扩展）
        self.c_fc = nn.Linear(config.d_model, config.___, bias=config.bias)

        # GELU 激活
        self.gelu = nn.GELU()

        # TODO: 第二个线性层（收缩）
        self.c_proj = nn.Linear(config.___, config.d_model, bias=config.bias)

        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        x = self.c_fc(x)
        x = self.gelu(x)
        x = self.c_proj(x)
        x = self.dropout(x)
        return x


class GPTBlock(nn.Module):
    """GPT Transformer 块"""

    def __init__(self, config):
        super().__init__()

        # TODO: Pre-LN 结构
        self.ln1 = nn.LayerNorm(config.d_model)
        self.attn = ___(config)  # 使用 CausalSelfAttention

        self.ln2 = nn.LayerNorm(config.d_model)
        self.mlp = ___(config)  # 使用 MLP

    def forward(self, x):
        # TODO: Pre-LN 残差连接
        x = x + self.attn(self.___(x))  # 填入归一化
        x = x + self.mlp(self.___(x))   # 填入归一化
        return x


class GPT(nn.Module):
    """完整的 GPT 模型"""

    def __init__(self, config):
        super().__init__()

        self.config = config

        # TODO: Token 嵌入
        self.wte = nn.___(config.vocab_size, config.d_model)

        # TODO: 位置嵌入
        self.wpe = nn.___(config.max_seq_len, config.d_model)

        self.drop = nn.Dropout(config.dropout)

        # TODO: Transformer 块
        self.blocks = nn.ModuleList([
            ___(config) for _ in range(config.num_layers)
        ])

        # 最终层归一化
        self.ln_f = nn.LayerNorm(config.d_model)

        # 语言模型头
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # 权重绑定
        self.wte.weight = self.lm_head.weight

        # 初始化权重
        self.apply(self._init_weights)

        # 特殊初始化：残差投影层使用更小的初始化
        for name, p in self.named_parameters():
            if name.endswith('c_proj.weight'):
                torch.nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * config.num_layers))

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, input_ids, targets=None):
        """
        Args:
            input_ids: (batch_size, seq_len)
            targets: (batch_size, seq_len) 可选，用于计算损失

        Returns:
            logits: (batch_size, seq_len, vocab_size)
            loss: 如果提供了 targets
        """
        batch_size, seq_len = input_ids.shape

        # TODO: 获取位置索引
        positions = torch.___(seq_len, device=input_ids.device)

        # TODO: 嵌入
        tok_emb = self.wte(input_ids)
        pos_emb = self.wpe(positions)
        x = self.drop(tok_emb + pos_emb)

        # 通过 Transformer 块
        for block in self.blocks:
            x = block(x)

        x = self.ln_f(x)
        logits = self.lm_head(x)

        # 计算损失（如果提供了 targets）
        loss = None
        if targets is not None:
            # TODO: 计算交叉熵损失
            loss = F.___(
                logits.view(-1, logits.size(-1)),
                targets.view(-1)
            )

        return logits, loss


def count_parameters(model):
    """计算模型参数量"""
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return total, trainable


def estimate_model_size(config):
    """估算模型参数量（不创建模型）"""
    # Embedding: vocab_size * d_model + max_seq_len * d_model
    emb_params = config.vocab_size * config.d_model + config.max_seq_len * config.d_model

    # 每个 Transformer 块
    # Attention: 3 * d_model * d_model + d_model * d_model (QKV + output)
    attn_params = 4 * config.d_model * config.d_model

    # MLP: d_model * d_ff + d_ff * d_model
    mlp_params = 2 * config.d_model * config.d_ff

    # LayerNorm: 2 * d_model (gamma + beta) * 2
    ln_params = 4 * config.d_model

    # 每块的参数
    block_params = attn_params + mlp_params + ln_params

    # 总参数
    total = emb_params + config.num_layers * block_params + config.d_model  # 最后的 ln

    return total


def main():
    # 创建小型 GPT 配置
    config = GPTConfig(
        vocab_size=1000,
        max_seq_len=128,
        d_model=64,
        num_heads=4,
        num_layers=2,
        dropout=0.0
    )

    print("测试 CausalSelfAttention...")
    attn = CausalSelfAttention(config)
    x = torch.randn(2, 16, 64)
    output = attn(x)
    assert output.shape == (2, 16, 64)
    print("✓ CausalSelfAttention 通过!")

    print("\n测试 MLP...")
    mlp = MLP(config)
    output = mlp(x)
    assert output.shape == (2, 16, 64)
    print("✓ MLP 通过!")

    print("\n测试 GPTBlock...")
    block = GPTBlock(config)
    output = block(x)
    assert output.shape == (2, 16, 64)
    print("✓ GPTBlock 通过!")

    print("\n测试 GPT...")
    model = GPT(config)
    input_ids = torch.randint(0, config.vocab_size, (2, 16))
    logits, loss = model(input_ids)
    assert logits.shape == (2, 16, config.vocab_size)
    assert loss is None
    print("✓ GPT 前向传播通过!")

    print("\n测试带损失的前向传播...")
    targets = torch.randint(0, config.vocab_size, (2, 16))
    logits, loss = model(input_ids, targets)
    assert loss is not None
    print(f"✓ 损失: {loss.item():.4f}")

    print("\n参数统计...")
    total, trainable = count_parameters(model)
    estimated = estimate_model_size(config)
    print(f"  实际参数: {total:,}")
    print(f"  估算参数: {estimated:,}")

    print("\nGPT-2 规模估算:")
    gpt2_small = GPTConfig(vocab_size=50257, d_model=768, num_heads=12, num_layers=12)
    print(f"  GPT-2 Small (124M): ~{estimate_model_size(gpt2_small)/1e6:.0f}M")

    gpt2_medium = GPTConfig(vocab_size=50257, d_model=1024, num_heads=16, num_layers=24)
    print(f"  GPT-2 Medium (350M): ~{estimate_model_size(gpt2_medium)/1e6:.0f}M")

    print("\n🎉 所有测试通过！GPT 模型架构掌握完成！")


if __name__ == "__main__":
    main()
