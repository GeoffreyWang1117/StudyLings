"""
练习 35: 条件 GAN (Conditional GAN, cGAN)

cGAN 在生成过程中引入条件信息（如类别标签），
实现可控的图像生成。

原理：
- G(z, c) -> 生成器接收噪声 z 和条件 c
- D(x, c) -> 判别器判断 (x, c) 是否匹配
- 条件可以是类别标签、文本、图像等

在这个练习中，你将学习：
- 条件 GAN 的架构
- 标签嵌入
- 条件注入方式
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ConditionalGenerator(nn.Module):
    """
    条件生成器

    将噪声 z 和条件 c 结合，生成对应类别的图像
    """

    def __init__(self, latent_dim, num_classes, embed_dim, img_channels=1, img_size=28):
        super().__init__()
        self.latent_dim = latent_dim
        self.img_size = img_size

        # TODO: 类别嵌入层
        self.label_embedding = nn.Embedding(num_classes, ___)  # 填入 embed_dim

        # 组合 z 和嵌入后的 c
        self.fc = nn.Sequential(
            nn.Linear(latent_dim + embed_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 1024),
            nn.LeakyReLU(0.2),
            nn.Linear(1024, img_channels * img_size * img_size),
            nn.Tanh()
        )

        self.img_channels = img_channels

    def forward(self, z, labels):
        """
        Args:
            z: 噪声向量 (batch, latent_dim)
            labels: 类别标签 (batch,)

        Returns:
            生成的图像 (batch, channels, H, W)
        """
        # TODO: 获取标签嵌入
        label_emb = self.___(labels)  # 填入 label_embedding

        # TODO: 拼接噪声和标签嵌入
        x = torch.cat([z, label_emb], dim=___)  # 填入 -1 或 1

        # 生成图像
        img = self.fc(x)
        img = img.view(-1, self.img_channels, self.img_size, self.img_size)

        return img


class ConditionalDiscriminator(nn.Module):
    """
    条件判别器

    判断 (图像, 标签) 对是否真实且匹配
    """

    def __init__(self, num_classes, embed_dim, img_channels=1, img_size=28):
        super().__init__()
        self.img_size = img_size

        # 标签嵌入 (展开为与图像相同的空间尺寸)
        self.label_embedding = nn.Embedding(num_classes, img_size * img_size)

        # 图像 + 标签通道一起判别
        self.model = nn.Sequential(
            nn.Linear((img_channels + 1) * img_size * img_size, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

        self.img_channels = img_channels

    def forward(self, img, labels):
        """
        Args:
            img: 图像 (batch, channels, H, W)
            labels: 类别标签 (batch,)

        Returns:
            真实概率 (batch, 1)
        """
        batch_size = img.shape[0]

        # 获取标签嵌入并调整形状
        label_emb = self.label_embedding(labels)
        label_emb = label_emb.view(batch_size, 1, self.img_size, self.img_size)

        # TODO: 将标签作为额外通道与图像拼接
        x = torch.cat([img, ___], dim=1)  # 填入 label_emb

        # 展平并判别
        x = x.view(batch_size, -1)
        validity = self.model(x)

        return validity


class ConditionalDCGAN_G(nn.Module):
    """
    条件 DCGAN 生成器

    使用卷积的条件生成器
    """

    def __init__(self, latent_dim, num_classes, embed_dim, img_channels=3, feature_maps=64):
        super().__init__()

        self.label_embedding = nn.Embedding(num_classes, embed_dim)

        # 初始投影
        self.fc = nn.Linear(latent_dim + embed_dim, feature_maps * 8 * 4 * 4)

        self.main = nn.Sequential(
            # 4x4 -> 8x8
            nn.ConvTranspose2d(feature_maps * 8, feature_maps * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 4),
            nn.ReLU(True),

            # 8x8 -> 16x16
            nn.ConvTranspose2d(feature_maps * 4, feature_maps * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 2),
            nn.ReLU(True),

            # 16x16 -> 32x32
            nn.ConvTranspose2d(feature_maps * 2, feature_maps, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps),
            nn.ReLU(True),

            # 32x32 -> 64x64
            nn.ConvTranspose2d(feature_maps, img_channels, 4, 2, 1, bias=False),
            nn.Tanh()
        )

        self.feature_maps = feature_maps

    def forward(self, z, labels):
        label_emb = self.label_embedding(labels)
        x = torch.cat([z, label_emb], dim=1)

        x = self.fc(x)
        x = x.view(-1, self.feature_maps * 8, 4, 4)
        return self.main(x)


class ConditionalDCGAN_D(nn.Module):
    """
    条件 DCGAN 判别器

    使用投影方式注入条件
    """

    def __init__(self, num_classes, embed_dim, img_channels=3, feature_maps=64):
        super().__init__()

        self.label_embedding = nn.Embedding(num_classes, embed_dim)

        # 图像编码器
        self.encoder = nn.Sequential(
            # 64x64 -> 32x32
            nn.Conv2d(img_channels, feature_maps, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            # 32x32 -> 16x16
            nn.Conv2d(feature_maps, feature_maps * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 2),
            nn.LeakyReLU(0.2, inplace=True),

            # 16x16 -> 8x8
            nn.Conv2d(feature_maps * 2, feature_maps * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 4),
            nn.LeakyReLU(0.2, inplace=True),

            # 8x8 -> 4x4
            nn.Conv2d(feature_maps * 4, feature_maps * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 8),
            nn.LeakyReLU(0.2, inplace=True),
        )

        # 投影头 (使用内积方式)
        self.fc = nn.Linear(feature_maps * 8 * 4 * 4, embed_dim)
        self.classifier = nn.Linear(feature_maps * 8 * 4 * 4, 1)

    def forward(self, img, labels):
        # 编码图像
        features = self.encoder(img)
        features = features.view(features.size(0), -1)

        # 图像特征
        img_emb = self.fc(features)

        # TODO: 标签嵌入
        label_emb = self.label_embedding(___)  # 填入 labels

        # TODO: 计算内积作为条件匹配分数
        projection = (img_emb * label_emb).sum(dim=___)  # 填入 1 或 -1

        # 无条件判别分数
        unconditional = self.classifier(features).squeeze()

        # 组合
        return torch.sigmoid(unconditional + projection)


def cgan_loss(d_real, d_fake):
    """
    cGAN 损失函数

    与标准 GAN 相同，但判别器接收条件
    """
    # TODO: 判别器损失
    d_loss_real = F.binary_cross_entropy(d_real, torch.ones_like(d_real))
    d_loss_fake = F.binary_cross_entropy(d_fake, torch.zeros_like(d_fake))
    d_loss = (d_loss_real + d_loss_fake) / 2

    # TODO: 生成器损失
    g_loss = F.binary_cross_entropy(d_fake, torch.___(d_fake))  # 使用 ones_like

    return d_loss, g_loss


def auxiliary_classifier_loss(logits, labels):
    """
    辅助分类器损失 (用于 AC-GAN)

    判别器同时预测类别
    """
    return F.cross_entropy(logits, labels)


def main():
    torch.manual_seed(42)

    latent_dim = 100
    num_classes = 10
    embed_dim = 50
    batch_size = 8

    print("测试 ConditionalGenerator...")
    gen = ConditionalGenerator(latent_dim, num_classes, embed_dim)
    z = torch.randn(batch_size, latent_dim)
    labels = torch.randint(0, num_classes, (batch_size,))

    fake_imgs = gen(z, labels)
    assert fake_imgs.shape == (batch_size, 1, 28, 28)
    print(f"✓ 生成图像: {fake_imgs.shape}")

    print("\n测试 ConditionalDiscriminator...")
    disc = ConditionalDiscriminator(num_classes, embed_dim)
    validity = disc(fake_imgs, labels)
    assert validity.shape == (batch_size, 1)
    print(f"✓ 判别输出: {validity.shape}")

    print("\n测试条件一致性...")
    # 使用错误的标签应该得到较低的分数
    wrong_labels = (labels + 1) % num_classes
    validity_wrong = disc(fake_imgs, wrong_labels)
    print(f"  正确标签得分: {validity.mean():.4f}")
    print(f"  错误标签得分: {validity_wrong.mean():.4f}")

    print("\n测试 ConditionalDCGAN...")
    gen_dc = ConditionalDCGAN_G(latent_dim, num_classes, embed_dim, img_channels=3)
    disc_dc = ConditionalDCGAN_D(num_classes, embed_dim, img_channels=3)

    fake_imgs_dc = gen_dc(z, labels)
    assert fake_imgs_dc.shape == (batch_size, 3, 64, 64)
    print(f"✓ DCGAN 生成: {fake_imgs_dc.shape}")

    validity_dc = disc_dc(fake_imgs_dc, labels)
    assert validity_dc.shape == (batch_size,)
    print(f"✓ DCGAN 判别: {validity_dc.shape}")

    print("\n测试损失计算...")
    real_imgs = torch.randn(batch_size, 3, 64, 64)

    d_real = disc_dc(real_imgs, labels)
    d_fake = disc_dc(fake_imgs_dc.detach(), labels)

    d_loss, g_loss = cgan_loss(d_real, d_fake)
    print(f"✓ D 损失: {d_loss:.4f}, G 损失: {g_loss:.4f}")

    print("\n🎉 所有测试通过！条件 GAN 掌握完成！")


if __name__ == "__main__":
    main()
