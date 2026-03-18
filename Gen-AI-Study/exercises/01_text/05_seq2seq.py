"""
练习 10: 序列到序列模型 (Seq2Seq)

Seq2Seq 是编码器-解码器架构的经典实现，
用于机器翻译、文本摘要等任务。

架构：
1. Encoder: 将输入序列编码为上下文向量
2. Decoder: 基于上下文向量生成输出序列

在这个练习中，你将学习：
- Encoder-Decoder 架构
- Teacher Forcing 训练策略
- 序列生成过程
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Encoder(nn.Module):
    """
    编码器

    将输入序列编码为隐藏状态
    """

    def __init__(self, vocab_size, embed_size, hidden_size, num_layers=1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)

    def forward(self, src):
        """
        Args:
            src: 源序列 (batch, src_len)

        Returns:
            outputs: 所有隐藏状态 (batch, src_len, hidden)
            hidden: (h_n, c_n) 最后的隐藏状态
        """
        # TODO: 词嵌入
        embedded = self.___(src)  # 填入 embedding

        # TODO: RNN 编码
        outputs, hidden = self.rnn(embedded)

        return outputs, hidden


class Decoder(nn.Module):
    """
    解码器

    基于编码器的隐藏状态生成目标序列
    """

    def __init__(self, vocab_size, embed_size, hidden_size, num_layers=1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_size)
        self.rnn = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, tgt, hidden):
        """
        Args:
            tgt: 目标序列 (batch, tgt_len)
            hidden: 编码器的最后隐藏状态

        Returns:
            output: 词汇表上的 logits (batch, tgt_len, vocab_size)
            hidden: 新的隐藏状态
        """
        # TODO: 词嵌入
        embedded = self.embedding(tgt)

        # TODO: RNN 解码
        output, hidden = self.___(embedded, hidden)  # 填入 rnn

        # TODO: 投影到词汇表
        output = self.fc(___)  # 填入 output

        return output, hidden


class Seq2Seq(nn.Module):
    """
    完整的 Seq2Seq 模型
    """

    def __init__(self, encoder, decoder, device):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.device = device

    def forward(self, src, tgt, teacher_forcing_ratio=0.5):
        """
        Args:
            src: 源序列 (batch, src_len)
            tgt: 目标序列 (batch, tgt_len)
            teacher_forcing_ratio: 使用真实目标的概率

        Returns:
            outputs: 预测的 logits (batch, tgt_len, vocab_size)
        """
        batch_size = src.shape[0]
        tgt_len = tgt.shape[1]
        vocab_size = self.decoder.fc.out_features

        # 存储输出
        outputs = torch.zeros(batch_size, tgt_len, vocab_size).to(self.device)

        # 编码
        _, hidden = self.encoder(src)

        # 解码器的第一个输入 (通常是 <SOS> token)
        decoder_input = tgt[:, 0:1]  # (batch, 1)

        for t in range(1, tgt_len):
            # 解码一步
            output, hidden = self.decoder(decoder_input, hidden)
            outputs[:, t:t+1, :] = output

            # 决定下一个输入: teacher forcing 或 自回归
            teacher_force = torch.rand(1).item() < teacher_forcing_ratio

            if teacher_force:
                # TODO: 使用真实目标
                decoder_input = tgt[:, ___:t+1]  # 填入 t
            else:
                # TODO: 使用模型预测
                top1 = output.argmax(dim=___)  # 填入 -1
                decoder_input = top1

        return outputs

    def generate(self, src, max_len, sos_idx, eos_idx):
        """
        推理时的序列生成

        Args:
            src: 源序列 (batch, src_len)
            max_len: 最大生成长度
            sos_idx: <SOS> token 的索引
            eos_idx: <EOS> token 的索引

        Returns:
            generated: 生成的序列
        """
        batch_size = src.shape[0]

        # 编码
        _, hidden = self.encoder(src)

        # 初始输入
        decoder_input = torch.full((batch_size, 1), sos_idx, dtype=torch.long, device=self.device)
        generated = [decoder_input]

        for _ in range(max_len):
            output, hidden = self.decoder(decoder_input, hidden)
            next_token = output.argmax(dim=-1)
            generated.append(next_token)

            # 检查是否全部生成了 <EOS>
            if (next_token == eos_idx).all():
                break

            decoder_input = next_token

        return torch.cat(generated, dim=1)


class Seq2SeqWithAttention(nn.Module):
    """
    带注意力的 Seq2Seq

    解码时动态关注源序列的不同部分
    """

    def __init__(self, vocab_size, embed_size, hidden_size):
        super().__init__()

        # 编码器
        self.encoder_embedding = nn.Embedding(vocab_size, embed_size)
        self.encoder_rnn = nn.LSTM(embed_size, hidden_size, batch_first=True, bidirectional=True)

        # 解码器
        self.decoder_embedding = nn.Embedding(vocab_size, embed_size)
        self.decoder_rnn = nn.LSTM(embed_size + hidden_size * 2, hidden_size, batch_first=True)

        # 注意力
        self.attention = nn.Linear(hidden_size * 3, 1)

        # 输出
        self.fc = nn.Linear(hidden_size, vocab_size)

        self.hidden_size = hidden_size

    def attention_score(self, decoder_hidden, encoder_outputs):
        """
        计算注意力权重

        Args:
            decoder_hidden: (batch, 1, hidden)
            encoder_outputs: (batch, src_len, hidden*2)
        """
        src_len = encoder_outputs.shape[1]

        # 扩展 decoder_hidden
        decoder_hidden = decoder_hidden.repeat(1, src_len, 1)

        # TODO: 拼接并计算注意力分数
        concat = torch.cat([decoder_hidden, encoder_outputs], dim=___)  # 填入 -1
        energy = self.attention(concat).squeeze(-1)

        # TODO: Softmax 归一化
        attn_weights = F.softmax(energy, dim=-1)

        return attn_weights

    def forward(self, src, tgt):
        batch_size = src.shape[0]
        tgt_len = tgt.shape[1]

        # 编码
        encoder_embedded = self.encoder_embedding(src)
        encoder_outputs, (h_n, c_n) = self.encoder_rnn(encoder_embedded)

        # 初始化解码器隐藏状态
        h_n = h_n.view(1, batch_size, -1)[:, :, :self.hidden_size]
        c_n = c_n.view(1, batch_size, -1)[:, :, :self.hidden_size]
        hidden = (h_n.contiguous(), c_n.contiguous())

        outputs = []
        decoder_input = tgt[:, 0:1]

        for t in range(1, tgt_len):
            # 嵌入
            embedded = self.decoder_embedding(decoder_input)

            # 注意力
            attn_weights = self.attention_score(
                hidden[0].transpose(0, 1),
                encoder_outputs
            )

            # 上下文向量
            context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs)

            # 解码
            rnn_input = torch.cat([embedded, context], dim=-1)
            output, hidden = self.decoder_rnn(rnn_input, hidden)

            output = self.fc(output)
            outputs.append(output)

            decoder_input = tgt[:, t:t+1]

        return torch.cat(outputs, dim=1)


def main():
    torch.manual_seed(42)
    device = torch.device('cpu')

    vocab_size = 1000
    embed_size = 128
    hidden_size = 256

    print("测试 Encoder...")
    encoder = Encoder(vocab_size, embed_size, hidden_size)
    src = torch.randint(0, vocab_size, (4, 20))
    enc_outputs, hidden = encoder(src)
    assert enc_outputs.shape == (4, 20, hidden_size)
    print(f"✓ Encoder 输出: {enc_outputs.shape}")

    print("\n测试 Decoder...")
    decoder = Decoder(vocab_size, embed_size, hidden_size)
    tgt = torch.randint(0, vocab_size, (4, 15))
    dec_output, _ = decoder(tgt, hidden)
    assert dec_output.shape == (4, 15, vocab_size)
    print(f"✓ Decoder 输出: {dec_output.shape}")

    print("\n测试 Seq2Seq...")
    seq2seq = Seq2Seq(encoder, decoder, device)
    outputs = seq2seq(src, tgt, teacher_forcing_ratio=0.5)
    assert outputs.shape == (4, 15, vocab_size)
    print(f"✓ Seq2Seq 输出: {outputs.shape}")

    print("\n测试序列生成...")
    generated = seq2seq.generate(src, max_len=20, sos_idx=1, eos_idx=2)
    print(f"✓ 生成序列: {generated.shape}")

    print("\n测试带注意力的 Seq2Seq...")
    seq2seq_attn = Seq2SeqWithAttention(vocab_size, embed_size, hidden_size)
    outputs = seq2seq_attn(src, tgt)
    assert outputs.shape == (4, 14, vocab_size)  # tgt_len - 1
    print(f"✓ Seq2Seq+Attention 输出: {outputs.shape}")

    print("\n🎉 所有测试通过！Seq2Seq 掌握完成！")


if __name__ == "__main__":
    main()
