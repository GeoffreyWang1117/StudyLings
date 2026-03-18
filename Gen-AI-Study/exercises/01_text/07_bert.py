"""
练习 12: BERT (Bidirectional Encoder Representations from Transformers)

BERT 是一个双向 Transformer 编码器，通过预训练获得强大的语言表示。

预训练任务：
1. Masked Language Modeling (MLM): 预测被遮蔽的词
2. Next Sentence Prediction (NSP): 预测两句话是否连续

架构特点：
- 只有 Encoder (双向)
- [CLS] token 用于分类
- [SEP] token 分隔句子
- 位置编码 + 段编码

在这个练习中，你将学习：
- BERT 的架构
- MLM 预训练
- 下游任务微调
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class BertEmbedding(nn.Module):
    """
    BERT 嵌入层

    包含三个嵌入:
    1. Token Embedding: 词嵌入
    2. Position Embedding: 位置嵌入
    3. Segment Embedding: 段嵌入 (区分句子 A 和 B)
    """

    def __init__(self, vocab_size, d_model, max_len=512):
        super().__init__()

        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_len, d_model)
        self.segment_embedding = nn.Embedding(2, d_model)  # 0 或 1

        self.layer_norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(0.1)

    def forward(self, tokens, segments=None):
        """
        Args:
            tokens: (batch, seq_len) token 索引
            segments: (batch, seq_len) 段索引 (0 或 1)
        """
        seq_len = tokens.shape[1]
        positions = torch.arange(seq_len, device=tokens.device)

        if segments is None:
            segments = torch.zeros_like(tokens)

        # TODO: 组合三种嵌入
        x = self.___(tokens) + self.position_embedding(positions) + self.segment_embedding(segments)  # 填入 token_embedding

        x = self.layer_norm(x)
        x = self.dropout(x)

        return x


class BertAttention(nn.Module):
    """BERT 多头自注意力"""

    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads

        self.query = nn.Linear(d_model, d_model)
        self.key = nn.Linear(d_model, d_model)
        self.value = nn.Linear(d_model, d_model)
        self.output = nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        batch_size, seq_len, d_model = x.shape

        # 线性投影
        Q = self.query(x)
        K = self.key(x)
        V = self.value(x)

        # 分头
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)

        # 注意力
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))

        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, V)

        # 合并多头
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        return self.output(out)


class BertFeedForward(nn.Module):
    """BERT 前馈网络"""

    def __init__(self, d_model, d_ff):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)

    def forward(self, x):
        # TODO: BERT 使用 GELU 激活函数
        return self.fc2(F.___(self.fc1(x)))  # 使用 gelu


class BertEncoderLayer(nn.Module):
    """BERT 编码器层"""

    def __init__(self, d_model, num_heads, d_ff):
        super().__init__()
        self.attention = BertAttention(d_model, num_heads)
        self.feed_forward = BertFeedForward(d_model, d_ff)

        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x, mask=None):
        # 自注意力 + 残差
        attn_out = self.attention(x, mask)
        x = self.norm1(x + self.dropout(attn_out))

        # 前馈网络 + 残差
        ff_out = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_out))

        return x


class BERT(nn.Module):
    """BERT 模型"""

    def __init__(self, vocab_size, d_model=768, num_heads=12, num_layers=12, d_ff=3072):
        super().__init__()

        self.embedding = BertEmbedding(vocab_size, d_model)
        self.encoder_layers = nn.ModuleList([
            BertEncoderLayer(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ])

        self.d_model = d_model

    def forward(self, tokens, segments=None, mask=None):
        """
        Args:
            tokens: (batch, seq_len)
            segments: (batch, seq_len) optional
            mask: attention mask

        Returns:
            hidden_states: (batch, seq_len, d_model)
        """
        x = self.embedding(tokens, segments)

        for layer in self.encoder_layers:
            x = layer(x, mask)

        return x

    def get_cls_embedding(self, tokens, segments=None, mask=None):
        """获取 [CLS] token 的表示，用于分类任务"""
        hidden = self(tokens, segments, mask)
        # TODO: 返回 [CLS] 位置的向量
        return hidden[:, ___, :]  # 填入 0


class BertMLM(nn.Module):
    """
    BERT Masked Language Modeling 头

    预测被遮蔽位置的原始 token
    """

    def __init__(self, bert, vocab_size, d_model):
        super().__init__()
        self.bert = bert
        self.fc = nn.Linear(d_model, d_model)
        self.layer_norm = nn.LayerNorm(d_model)
        self.decoder = nn.Linear(d_model, vocab_size)

    def forward(self, tokens, segments=None, mask=None):
        hidden = self.bert(tokens, segments, mask)

        # MLM 头
        x = F.gelu(self.fc(hidden))
        x = self.layer_norm(x)

        # TODO: 投影到词汇表
        logits = self.___(x)  # 填入 decoder

        return logits


class BertForClassification(nn.Module):
    """
    BERT 用于序列分类

    使用 [CLS] token 的表示进行分类
    """

    def __init__(self, bert, num_classes, d_model):
        super().__init__()
        self.bert = bert
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(d_model, num_classes)

    def forward(self, tokens, segments=None, mask=None):
        # TODO: 获取 [CLS] 表示
        cls_embedding = self.bert.get_cls_embedding(tokens, segments, ___)  # 填入 mask

        cls_embedding = self.dropout(cls_embedding)
        logits = self.classifier(cls_embedding)

        return logits


def create_mlm_data(tokens, mask_token_id, vocab_size, mask_prob=0.15):
    """
    创建 MLM 训练数据

    15% 的 token 被选中:
    - 80% 替换为 [MASK]
    - 10% 替换为随机 token
    - 10% 保持不变
    """
    labels = tokens.clone()

    # 随机选择 15% 的位置
    probability_matrix = torch.full(tokens.shape, mask_prob)
    masked_indices = torch.bernoulli(probability_matrix).bool()

    # 只预测被遮蔽的位置，其他位置设为 -100 (忽略)
    labels[~masked_indices] = -100

    # 80% 替换为 [MASK]
    indices_replaced = torch.bernoulli(torch.full(tokens.shape, 0.8)).bool() & masked_indices
    tokens[indices_replaced] = mask_token_id

    # 10% 替换为随机 token
    indices_random = torch.bernoulli(torch.full(tokens.shape, 0.5)).bool() & masked_indices & ~indices_replaced
    random_words = torch.randint(vocab_size, tokens.shape, dtype=torch.long)
    tokens[indices_random] = random_words[indices_random]

    # 10% 保持不变 (不需要额外处理)

    return tokens, labels


def main():
    torch.manual_seed(42)

    vocab_size = 30000
    d_model = 256
    num_heads = 8
    num_layers = 4
    d_ff = 1024

    print("测试 BertEmbedding...")
    embedding = BertEmbedding(vocab_size, d_model)
    tokens = torch.randint(0, vocab_size, (2, 20))
    segments = torch.zeros_like(tokens)
    segments[:, 10:] = 1

    emb = embedding(tokens, segments)
    assert emb.shape == (2, 20, d_model)
    print(f"✓ Embedding 输出: {emb.shape}")

    print("\n测试 BERT...")
    bert = BERT(vocab_size, d_model, num_heads, num_layers, d_ff)
    hidden = bert(tokens, segments)
    assert hidden.shape == (2, 20, d_model)
    print(f"✓ BERT 输出: {hidden.shape}")

    print("\n测试 get_cls_embedding...")
    cls_emb = bert.get_cls_embedding(tokens, segments)
    assert cls_emb.shape == (2, d_model)
    print(f"✓ CLS 嵌入: {cls_emb.shape}")

    print("\n测试 BertMLM...")
    mlm = BertMLM(bert, vocab_size, d_model)
    mlm_logits = mlm(tokens, segments)
    assert mlm_logits.shape == (2, 20, vocab_size)
    print(f"✓ MLM 输出: {mlm_logits.shape}")

    print("\n测试 BertForClassification...")
    classifier = BertForClassification(bert, num_classes=2, d_model=d_model)
    class_logits = classifier(tokens, segments)
    assert class_logits.shape == (2, 2)
    print(f"✓ 分类输出: {class_logits.shape}")

    print("\n测试 MLM 数据创建...")
    original_tokens = torch.randint(0, vocab_size, (4, 32))
    masked_tokens, labels = create_mlm_data(original_tokens.clone(), mask_token_id=103, vocab_size=vocab_size)

    num_masked = (labels != -100).sum()
    expected_masked = int(4 * 32 * 0.15)
    print(f"✓ 遮蔽了 {num_masked} 个 token (期望约 {expected_masked})")

    # 计算 MLM 损失
    mlm_logits = mlm(masked_tokens)
    mlm_loss = F.cross_entropy(mlm_logits.view(-1, vocab_size), labels.view(-1), ignore_index=-100)
    print(f"✓ MLM 损失: {mlm_loss:.4f}")

    print("\n统计参数量...")
    total_params = sum(p.numel() for p in bert.parameters())
    print(f"  BERT 参数: {total_params:,}")

    # 对比 BERT-Base
    bert_base_params = 110_000_000
    print(f"  BERT-Base 参数: ~{bert_base_params:,}")

    print("\n🎉 所有测试通过！BERT 掌握完成！")


if __name__ == "__main__":
    main()
