"""
练习 17: BPE 分词器 (Byte Pair Encoding)

BPE 是现代语言模型常用的分词算法。
它通过迭代合并最频繁出现的字符对来构建词表。

BPE 的优点：
1. 可以处理任意词汇（包括新词）
2. 平衡了字符级和词级分词的优缺点
3. 压缩效率较高

在这个练习中，你将学习：
- BPE 算法的原理
- 如何训练 BPE 词表
- 如何使用 BPE 进行分词
"""

import re
from collections import defaultdict


def get_vocab_from_text(text):
    """
    从文本获取初始词表

    将每个词拆分成字符，并在词尾添加特殊结束符 '</w>'
    例如: "low" -> ['l', 'o', 'w', '</w>']
    """
    vocab = defaultdict(int)
    words = text.lower().split()

    for word in words:
        # TODO: 将词拆分成字符元组，并在末尾添加 '</w>'
        # 例如: "low" -> ('l', 'o', 'w', '</w>')
        chars = tuple(list(word) + ['</w>'])
        vocab[___] += 1  # 填入正确的键

    return vocab


def get_pair_stats(vocab):
    """
    统计所有相邻字符对的频率

    Args:
        vocab: 词表，键是字符元组，值是频率

    Returns:
        pairs: 字典，键是字符对，值是频率
    """
    pairs = defaultdict(int)

    for word, freq in vocab.items():
        # TODO: 遍历相邻字符对
        for i in range(len(word) - ___):  # 填入正确的值
            pair = (word[i], word[i + 1])
            pairs[pair] += freq

    return pairs


def merge_vocab(pair, vocab):
    """
    在词表中合并指定的字符对

    Args:
        pair: 要合并的字符对，如 ('l', 'o')
        vocab: 当前词表

    Returns:
        new_vocab: 合并后的词表
    """
    new_vocab = {}

    # 创建正则表达式模式
    p = re.escape(' '.join(pair))
    pattern = re.compile(r'(?<!\S)' + p + r'(?!\S)')

    for word, freq in vocab.items():
        # 将元组转为空格分隔的字符串
        word_str = ' '.join(word)
        # 合并字符对
        new_word_str = pattern.sub(''.join(pair), word_str)
        # 转回元组
        new_word = tuple(new_word_str.split())
        new_vocab[new_word] = freq

    return new_vocab


def train_bpe(text, num_merges):
    """
    训练 BPE 词表

    Args:
        text: 训练文本
        num_merges: 合并操作的次数

    Returns:
        vocab: 最终词表
        merges: 合并规则列表
    """
    # 初始化词表
    vocab = get_vocab_from_text(text)
    merges = []

    for i in range(num_merges):
        # TODO: 获取字符对统计
        pairs = ___(vocab)  # 调用 get_pair_stats

        if not pairs:
            break

        # TODO: 找出频率最高的字符对
        best_pair = max(pairs, key=pairs.___)  # 使用 get 方法

        # 合并
        vocab = merge_vocab(best_pair, vocab)
        merges.append(best_pair)

        print(f"Merge {i+1}: {best_pair} -> {''.join(best_pair)}")

    return vocab, merges


def encode_word(word, merges):
    """
    使用学习到的 BPE 规则编码单词

    Args:
        word: 要编码的单词
        merges: BPE 合并规则列表

    Returns:
        tokens: BPE token 列表
    """
    # TODO: 初始化为字符列表
    tokens = list(word) + ['</w>']

    for pair in merges:
        i = 0
        while i < len(tokens) - 1:
            # TODO: 如果找到匹配的字符对，进行合并
            if tokens[i] == pair[0] and tokens[i + 1] == pair[___]:  # 填入索引
                tokens = tokens[:i] + [''.join(pair)] + tokens[i + 2:]
            else:
                i += 1

    return tokens


class SimpleBPE:
    """
    简单的 BPE 分词器类
    """

    def __init__(self):
        self.merges = []
        self.vocab = {}
        self.token_to_id = {}
        self.id_to_token = {}

    def train(self, text, num_merges):
        """训练 BPE"""
        self.vocab, self.merges = train_bpe(text, num_merges)

        # 构建 token 到 ID 的映射
        all_tokens = set()
        for word in self.vocab.keys():
            all_tokens.update(word)

        # TODO: 创建 token 到 ID 的映射
        for i, token in enumerate(sorted(all_tokens)):
            self.___(token, i)  # 应该添加到哪个字典？

        # ID 到 token 的反向映射
        self.id_to_token = {v: k for k, v in self.token_to_id.items()}

    def encode(self, text):
        """将文本编码为 token ID 列表"""
        words = text.lower().split()
        ids = []

        for word in words:
            tokens = encode_word(word, self.merges)
            for token in tokens:
                if token in self.token_to_id:
                    ids.append(self.token_to_id[token])

        return ids

    def decode(self, ids):
        """将 token ID 列表解码为文本"""
        tokens = [self.id_to_token.get(i, '<unk>') for i in ids]

        # TODO: 将 tokens 连接成文本
        # '</w>' 表示词的结束，应该替换为空格
        text = ''.join(tokens)
        text = text.replace('</w>', ' ')

        return text.strip()


def main():
    # 示例文本
    text = """
    low low low low low
    lower lower
    newest newest newest newest newest newest
    widest widest widest
    """

    print("训练 BPE...")
    print("=" * 40)
    vocab, merges = train_bpe(text, num_merges=10)

    print("\n最终词表:")
    for word, freq in sorted(vocab.items(), key=lambda x: -x[1]):
        print(f"  {word}: {freq}")

    print("\n测试 encode_word...")
    test_word = "lowest"
    tokens = encode_word(test_word, merges)
    print(f"  '{test_word}' -> {tokens}")

    print("\n测试 SimpleBPE 类...")
    bpe = SimpleBPE()
    bpe.train(text, num_merges=10)

    test_text = "low lower lowest"
    encoded = bpe.encode(test_text)
    decoded = bpe.decode(encoded)

    print(f"  原文: '{test_text}'")
    print(f"  编码: {encoded}")
    print(f"  解码: '{decoded}'")

    # 验证
    assert len(merges) == 10, "应该有 10 次合并"
    print("\n✓ 所有测试通过！")

    print("\n🎉 BPE 分词器掌握完成！")


if __name__ == "__main__":
    main()
