"""
练习 49: 交叉注意力

交叉注意力让图像生成能够基于文本条件。
Q 来自图像特征，K/V 来自文本特征。
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class CrossAttention(nn.Module):
    """交叉注意力层"""
    
    def __init__(self, query_dim, context_dim=None, heads=8, dim_head=64):
        super().__init__()
        
        if context_dim is None:
            context_dim = query_dim
            
        inner_dim = dim_head * heads
        
        self.heads = heads
        self.dim_head = dim_head
        
        self.to_q = nn.Linear(query_dim, inner_dim, bias=False)
        self.to_k = nn.Linear(context_dim, inner_dim, bias=False)
        self.to_v = nn.Linear(context_dim, inner_dim, bias=False)
        self.to_out = nn.Linear(inner_dim, query_dim)
    
    def forward(self, x, context=None):
        """
        Args:
            x: 图像特征 (batch, seq_len, query_dim)
            context: 文本特征 (batch, context_len, context_dim)
        """
        if context is None:
            context = x  # 自注意力
        
        B, N, _ = x.shape
        
        # 投影
        q = self.to_q(x)
        k = self.to_k(context)
        v = self.to_v(context)
        
        # 分头
        q = q.view(B, N, self.heads, self.dim_head).transpose(1, 2)
        k = k.view(B, -1, self.heads, self.dim_head).transpose(1, 2)
        v = v.view(B, -1, self.heads, self.dim_head).transpose(1, 2)
        
        # 注意力
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.dim_head)
        attn = F.softmax(scores, dim=-1)
        out = torch.matmul(attn, v)
        
        # 合并头
        out = out.transpose(1, 2).contiguous().view(B, N, -1)
        
        return self.to_out(out)


def main():
    print("测试交叉注意力...")
    
    cross_attn = CrossAttention(query_dim=512, context_dim=768, heads=8)
    
    # 图像特征
    image_features = torch.randn(4, 196, 512)  # 14x14 patches
    # 文本特征
    text_features = torch.randn(4, 77, 768)
    
    out = cross_attn(image_features, text_features)
    
    assert out.shape == (4, 196, 512)
    print(f"✓ 输出形状: {out.shape}")
    
    print("\n🎉 交叉注意力测试通过！")

if __name__ == "__main__":
    main()
