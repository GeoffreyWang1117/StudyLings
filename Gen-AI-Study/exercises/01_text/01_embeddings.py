"""
练习 05: 词嵌入 (Word Embeddings)

词嵌入将离散的词语映射到连续的向量空间。
这是所有 NLP 模型的基础，让模型能够理解词语之间的语义关系。

在这个练习中，你将学习：
- 什么是词嵌入
- 如何使用 nn.Embedding
- 嵌入的查表过程
"""

import torch
import torch.nn as nn


def create_embedding_layer():
    """创建一个词嵌入层"""
    vocab_size = 1000  # 词表大小
    embedding_dim = 128  # 嵌入维度

    # TODO: 创建一个嵌入层
    # nn.Embedding(num_embeddings, embedding_dim)
    # num_embeddings 是词表大小，embedding_dim 是每个词向量的维度
    embedding = nn.___(vocab_size, embedding_dim)  # 使用 nn.Embedding

    return embedding


def lookup_embeddings(embedding, indices):
    """查询词嵌入

    Args:
        embedding: nn.Embedding 层
        indices: 词索引张量，形状为 (batch_size, seq_len)

    Returns:
        嵌入向量，形状为 (batch_size, seq_len, embedding_dim)
    """
    # TODO: 通过索引查询嵌入
    # 嵌入层的输入是整数索引，输出是对应的向量
    # 直接调用 embedding(indices) 即可
    output = ___(indices)  # 调用 embedding

    return output


class TokenEmbedding(nn.Module):
    """Token 嵌入层，通常用于 Transformer 模型的输入"""

    def __init__(self, vocab_size, d_model):
        """
        Args:
            vocab_size: 词表大小
            d_model: 模型维度/嵌入维度
        """
        super().__init__()

        # TODO: 创建词嵌入层
        self.embedding = nn.___(___, ___)  # 填入参数

        # 保存 d_model 用于缩放
        self.d_model = d_model

    def forward(self, x):
        """
        Args:
            x: 输入 token 索引，形状 (batch_size, seq_len)

        Returns:
            嵌入向量，形状 (batch_size, seq_len, d_model)
            注意：Transformer 论文中建议将嵌入乘以 sqrt(d_model)
        """
        # TODO: 获取嵌入并缩放
        # 论文 "Attention Is All You Need" 中提到:
        # 将嵌入乘以 sqrt(d_model) 可以使嵌入和位置编码在相近的尺度
        import math
        return self.___(x) * math.sqrt(self.___)  # 获取嵌入并乘以缩放因子


def embedding_similarity():
    """演示词嵌入可以捕捉语义相似性"""
    # 假设我们有一个简单的词表
    # 0: "king", 1: "queen", 2: "man", 3: "woman", 4: "apple", 5: "orange"
    vocab_size = 6
    embedding_dim = 4

    # 创建嵌入层
    embedding = nn.Embedding(vocab_size, embedding_dim)

    # 手动设置一些嵌入，模拟训练后的结果
    # 让相似的词有相似的向量
    with torch.no_grad():
        embedding.weight[0] = torch.tensor([1.0, 0.8, 0.2, 0.1])  # king
        embedding.weight[1] = torch.tensor([1.0, 0.8, -0.2, -0.1])  # queen
        embedding.weight[2] = torch.tensor([0.3, 0.2, 0.9, 0.8])  # man
        embedding.weight[3] = torch.tensor([0.3, 0.2, -0.9, -0.8])  # woman
        embedding.weight[4] = torch.tensor([-1.0, -0.8, 0.0, 0.0])  # apple
        embedding.weight[5] = torch.tensor([-0.9, -0.7, 0.0, 0.0])  # orange

    # TODO: 计算 "king" 和 "queen" 的余弦相似度
    king = embedding(torch.tensor([0])).squeeze()
    queen = embedding(torch.tensor([1])).squeeze()

    # 余弦相似度 = (a · b) / (|a| * |b|)
    dot_product = torch.___(king, queen)  # 使用 torch.dot()
    norm_king = torch.norm(king)
    norm_queen = torch.norm(queen)
    similarity = dot_product / (norm_king * norm_queen)

    return similarity


def main():
    print("测试 create_embedding_layer...")
    emb = create_embedding_layer()
    assert isinstance(emb, nn.Embedding)
    assert emb.num_embeddings == 1000
    assert emb.embedding_dim == 128
    print("✓ create_embedding_layer 通过!")

    print("\n测试 lookup_embeddings...")
    emb = nn.Embedding(100, 32)
    indices = torch.tensor([[1, 2, 3], [4, 5, 6]])  # (2, 3)
    output = lookup_embeddings(emb, indices)
    assert output.shape == (2, 3, 32), f"期望形状 (2, 3, 32)，得到 {output.shape}"
    print("✓ lookup_embeddings 通过!")

    print("\n测试 TokenEmbedding...")
    tok_emb = TokenEmbedding(vocab_size=1000, d_model=256)
    x = torch.randint(0, 1000, (4, 10))  # (batch=4, seq_len=10)
    output = tok_emb(x)
    assert output.shape == (4, 10, 256), f"期望形状 (4, 10, 256)，得到 {output.shape}"
    print("✓ TokenEmbedding 通过!")

    print("\n测试 embedding_similarity...")
    sim = embedding_similarity()
    # king 和 queen 应该有较高的相似度
    assert sim > 0.8, f"king 和 queen 的相似度应该较高，得到 {sim}"
    print(f"✓ embedding_similarity 通过! (king-queen 相似度: {sim:.4f})")

    print("\n🎉 所有测试通过！词嵌入掌握完成！")


if __name__ == "__main__":
    main()
