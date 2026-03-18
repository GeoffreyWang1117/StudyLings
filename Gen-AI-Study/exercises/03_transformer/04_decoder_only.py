"""
练习 16: Decoder-Only 架构

Decoder-Only 架构是 GPT 系列模型的基础。
与编码器-解码器架构不同，它只使用解码器，通过因果掩码实现自回归生成。

架构：
1. Token Embedding + Position Embedding
2. N × Transformer Decoder Block (带因果掩码)
3. Layer Norm
4. Language Model Head (线性层到词表)

在这个练习中，你将学习：
- 完整的 Decoder-Only 实现
- 自回归语言模型的训练
- 文本生成的基本流程
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class CausalSelfAttention(nn.Module):
    """带因果掩码的自注意力"""

    def __init__(self, d_model, num_heads, max_seq_len, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

        self.attn_dropout = nn.Dropout(dropout)
        self.proj_dropout = nn.Dropout(dropout)

        # 注册因果掩码
        mask = torch.triu(torch.ones(max_seq_len, max_seq_len), diagonal=1).bool()
        self.register_buffer('causal_mask', mask)

    def forward(self, x):
        batch_size, seq_len, _ = x.shape

        Q = self.W_q(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        scores = scores.masked_fill(self.causal_mask[:seq_len, :seq_len], float('-inf'))

        attn = self.attn_dropout(F.softmax(scores, dim=-1))
        output = torch.matmul(attn, V)
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)

        return self.proj_dropout(self.W_o(output))


class DecoderBlock(nn.Module):
    """Decoder-Only 架构的单个块"""

    def __init__(self, d_model, num_heads, max_seq_len, d_ff=None, dropout=0.1):
        super().__init__()

        if d_ff is None:
            d_ff = 4 * d_model

        # TODO: 层归一化 1
        self.ln1 = nn.___(d_model)

        # TODO: 因果自注意力
        self.attn = ___(d_model, num_heads, max_seq_len, dropout)

        # TODO: 层归一化 2
        self.ln2 = nn.___(d_model)

        # FFN
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Linear(d_ff, d_model),
            nn.Dropout(dropout)
        )

    def forward(self, x):
        # TODO: Pre-LN 结构
        # 注意力子层
        x = x + self.attn(self.___(x))  # 填入归一化

        # FFN 子层
        x = x + self.ffn(self.___(x))  # 填入归一化

        return x


class GPTModel(nn.Module):
    """
    GPT 风格的 Decoder-Only 模型
    """

    def __init__(self, vocab_size, d_model, num_heads, num_layers,
                 max_seq_len, d_ff=None, dropout=0.1):
        """
        Args:
            vocab_size: 词表大小
            d_model: 模型维度
            num_heads: 注意力头数
            num_layers: Decoder 块数量
            max_seq_len: 最大序列长度
            d_ff: FFN 中间维度
            dropout: dropout 概率
        """
        super().__init__()

        self.d_model = d_model
        self.max_seq_len = max_seq_len

        # TODO: Token 嵌入
        self.token_embedding = nn.___(vocab_size, d_model)

        # TODO: 位置嵌入（可学习的）
        self.position_embedding = nn.___(max_seq_len, d_model)

        # Dropout
        self.dropout = nn.Dropout(dropout)

        # TODO: 堆叠多个 Decoder 块
        self.blocks = nn.ModuleList([
            ___(d_model, num_heads, max_seq_len, d_ff, dropout)
            for _ in range(num_layers)
        ])

        # TODO: 最终的层归一化
        self.ln_f = nn.___(d_model)

        # TODO: 语言模型头（映射到词表）
        self.lm_head = nn.___(d_model, vocab_size, bias=False)

        # 权重绑定：让 token embedding 和 lm_head 共享权重
        # 这是常用的技巧，可以减少参数并提升性能
        self.token_embedding.weight = self.lm_head.weight

        self._init_weights()

    def _init_weights(self):
        """初始化权重"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if module.bias is not None:
                    torch.nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, input_ids):
        """
        Args:
            input_ids: 输入 token ID，形状 (batch_size, seq_len)

        Returns:
            logits: 输出 logits，形状 (batch_size, seq_len, vocab_size)
        """
        batch_size, seq_len = input_ids.shape

        assert seq_len <= self.max_seq_len, f"序列长度 {seq_len} 超过最大长度 {self.max_seq_len}"

        # TODO: 获取 token 嵌入
        token_emb = self.___(input_ids)  # 调用 token_embedding

        # TODO: 获取位置嵌入
        positions = torch.arange(seq_len, device=input_ids.device)
        pos_emb = self.___(positions)  # 调用 position_embedding

        # TODO: 相加并 dropout
        x = self.___(token_emb + pos_emb)

        # 通过所有 Decoder 块
        for block in self.blocks:
            x = block(x)

        # TODO: 最终归一化
        x = self.___(x)  # 调用 ln_f

        # TODO: 映射到词表
        logits = self.___(x)  # 调用 lm_head

        return logits


def compute_lm_loss(logits, targets):
    """
    计算语言模型损失

    Args:
        logits: 模型输出，形状 (batch_size, seq_len, vocab_size)
        targets: 目标 token ID，形状 (batch_size, seq_len)

    Returns:
        loss: 交叉熵损失
    """
    batch_size, seq_len, vocab_size = logits.shape

    # TODO: 将 logits 和 targets 展平以计算交叉熵
    # logits: (batch * seq, vocab_size)
    # targets: (batch * seq,)
    logits_flat = logits.view(-1, ___)  # 填入 vocab_size
    targets_flat = targets.view(___)  # 填入 -1

    # TODO: 计算交叉熵损失
    loss = F.___(logits_flat, targets_flat)  # 使用 cross_entropy

    return loss


@torch.no_grad()
def generate(model, input_ids, max_new_tokens, temperature=1.0):
    """
    简单的自回归生成

    Args:
        model: GPT 模型
        input_ids: 初始 token ID，形状 (1, seq_len)
        max_new_tokens: 生成的最大新 token 数
        temperature: 温度参数，控制随机性

    Returns:
        生成的 token ID 序列
    """
    model.eval()

    for _ in range(max_new_tokens):
        # 如果序列太长，截断到最大长度
        input_ids_truncated = input_ids[:, -model.max_seq_len:]

        # 前向传播
        logits = model(input_ids_truncated)

        # 只取最后一个位置的 logits
        logits = logits[:, -1, :] / temperature

        # TODO: 从概率分布中采样
        probs = F.___(logits, dim=-1)  # 使用 softmax

        # TODO: 采样下一个 token
        next_token = torch.___(probs, num_samples=1)  # 使用 multinomial

        # 拼接新 token
        input_ids = torch.cat([input_ids, next_token], dim=1)

    return input_ids


def main():
    # 设置小规模参数用于测试
    vocab_size = 1000
    d_model = 64
    num_heads = 4
    num_layers = 2
    max_seq_len = 128
    batch_size = 2
    seq_len = 16

    print("测试 DecoderBlock...")
    block = DecoderBlock(d_model, num_heads, max_seq_len, dropout=0.0)
    x = torch.randn(batch_size, seq_len, d_model)
    output = block(x)
    assert output.shape == (batch_size, seq_len, d_model)
    print("✓ DecoderBlock 通过!")

    print("\n测试 GPTModel...")
    model = GPTModel(
        vocab_size=vocab_size,
        d_model=d_model,
        num_heads=num_heads,
        num_layers=num_layers,
        max_seq_len=max_seq_len,
        dropout=0.0
    )
    input_ids = torch.randint(0, vocab_size, (batch_size, seq_len))
    logits = model(input_ids)
    assert logits.shape == (batch_size, seq_len, vocab_size)
    print(f"✓ GPTModel 通过! 输出形状: {logits.shape}")

    print("\n测试 compute_lm_loss...")
    targets = torch.randint(0, vocab_size, (batch_size, seq_len))
    loss = compute_lm_loss(logits, targets)
    assert loss.dim() == 0, "损失应该是标量"
    assert loss.item() > 0, "损失应该是正数"
    print(f"✓ compute_lm_loss 通过! 损失: {loss.item():.4f}")

    print("\n测试 generate...")
    prompt = torch.randint(0, vocab_size, (1, 5))  # 5 个 token 的 prompt
    generated = generate(model, prompt, max_new_tokens=10, temperature=1.0)
    assert generated.shape == (1, 15), f"期望形状 (1, 15)，得到 {generated.shape}"
    print(f"✓ generate 通过! 生成序列长度: {generated.shape[1]}")

    print("\n测试参数数量...")
    num_params = sum(p.numel() for p in model.parameters())
    print(f"  模型参数数量: {num_params:,}")

    print("\n🎉 所有测试通过！Decoder-Only 架构掌握完成！")


if __name__ == "__main__":
    main()
