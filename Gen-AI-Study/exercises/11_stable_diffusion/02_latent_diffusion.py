"""
练习 50: 潜在扩散模型

潜在扩散在压缩的潜在空间而非像素空间进行扩散，大大提高了效率。

架构:
图像 → VAE Encoder → 潜在空间 → Diffusion → VAE Decoder → 图像
"""

import torch
import torch.nn as nn


class LatentDiffusion:
    """潜在扩散模型框架"""
    
    def __init__(self, vae, unet, text_encoder, scheduler):
        self.vae = vae
        self.unet = unet
        self.text_encoder = text_encoder
        self.scheduler = scheduler
    
    def encode_image(self, image):
        """编码图像到潜在空间"""
        with torch.no_grad():
            latent = self.vae.encode(image)
        return latent
    
    def decode_latent(self, latent):
        """从潜在空间解码到图像"""
        with torch.no_grad():
            image = self.vae.decode(latent)
        return image
    
    def encode_text(self, text):
        """编码文本条件"""
        with torch.no_grad():
            text_embeddings = self.text_encoder(text)
        return text_embeddings


def main():
    print("潜在扩散模型特点：")
    print("1. 在潜在空间进行扩散（如 64x64x4）")
    print("2. 比像素空间小 48 倍 (512x512x3 vs 64x64x4)")
    print("3. 计算量大大减少")
    print("4. 使用预训练的 VAE 进行编解码")
    print("\n✓ 潜在扩散概念理解完成！")

if __name__ == "__main__":
    main()
