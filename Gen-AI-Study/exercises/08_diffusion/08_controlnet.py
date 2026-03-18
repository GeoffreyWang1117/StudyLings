"""
练习 43: ControlNet

ControlNet 在预训练的扩散模型上添加空间条件控制，
如边缘、深度、姿态等，实现精确的图像生成控制。

核心思想：
1. 复制 UNet 编码器作为控制网络
2. 使用 zero convolution 连接
3. 冻结原始模型，只训练控制网络

在这个练习中，你将学习：
- ControlNet 架构
- Zero Convolution
- 条件注入方式
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ZeroConv2d(nn.Module):
    """
    零卷积 (Zero Convolution)

    初始化为零，让 ControlNet 在训练开始时不影响原模型
    随着训练进行，逐渐学习到有意义的特征
    """

    def __init__(self, in_channels, out_channels, kernel_size=1, padding=0):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, padding=padding)

        # TODO: 将权重和偏置初始化为零
        nn.init.zeros_(self.conv.___)  # 填入 weight
        nn.init.zeros_(self.conv.bias)

    def forward(self, x):
        return self.conv(x)


class ControlNetBlock(nn.Module):
    """
    ControlNet 基本块

    与 UNet 编码器块结构相同
    """

    def __init__(self, in_channels, out_channels, time_emb_dim):
        super().__init__()

        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.norm1 = nn.GroupNorm(8, out_channels)
        self.norm2 = nn.GroupNorm(8, out_channels)

        # 时间嵌入投影
        self.time_mlp = nn.Linear(time_emb_dim, out_channels)

        # 残差连接
        if in_channels != out_channels:
            self.residual = nn.Conv2d(in_channels, out_channels, 1)
        else:
            self.residual = nn.Identity()

    def forward(self, x, time_emb):
        h = self.conv1(x)
        h = self.norm1(h)
        h = F.silu(h)

        # TODO: 添加时间嵌入
        time_emb = self.time_mlp(time_emb)
        h = h + time_emb[:, :, None, ___]  # 填入 None

        h = self.conv2(h)
        h = self.norm2(h)
        h = F.silu(h)

        return h + self.residual(x)


class ControlNetEncoder(nn.Module):
    """
    ControlNet 编码器

    复制 UNet 编码器的结构，处理控制条件
    """

    def __init__(self, condition_channels, base_channels, channel_mults, time_emb_dim):
        super().__init__()

        # 条件输入卷积
        self.input_conv = nn.Conv2d(condition_channels, base_channels, 3, padding=1)

        # 编码器块
        self.encoder_blocks = nn.ModuleList()
        self.zero_convs = nn.ModuleList()

        in_channels = base_channels
        for mult in channel_mults:
            out_channels = base_channels * mult

            self.encoder_blocks.append(
                ControlNetBlock(in_channels, out_channels, time_emb_dim)
            )
            # TODO: 每个块后面添加 zero conv
            self.zero_convs.append(
                ZeroConv2d(out_channels, ___)  # 填入 out_channels
            )

            in_channels = out_channels

    def forward(self, condition, time_emb):
        """
        Args:
            condition: 控制条件 (batch, C, H, W) 如 Canny 边缘图
            time_emb: 时间嵌入 (batch, time_emb_dim)

        Returns:
            控制特征列表，每个对应 UNet 的一层
        """
        x = self.input_conv(condition)

        control_features = []
        for block, zero_conv in zip(self.encoder_blocks, self.zero_convs):
            x = block(x, time_emb)
            # TODO: 通过 zero conv 输出
            control_features.append(___(x))  # 填入 zero_conv

            # 下采样
            x = F.avg_pool2d(x, 2)

        return control_features


class ControlNet(nn.Module):
    """
    完整的 ControlNet

    结合控制编码器和原始 UNet
    """

    def __init__(self, unet, condition_channels, time_emb_dim):
        super().__init__()

        self.unet = unet

        # 冻结原始 UNet
        for param in self.unet.parameters():
            param.requires_grad = False

        # ControlNet 编码器 (可训练)
        base_channels = 64
        channel_mults = [1, 2, 4]

        self.control_encoder = ControlNetEncoder(
            condition_channels, base_channels, channel_mults, time_emb_dim
        )

    def forward(self, x, t, condition):
        """
        Args:
            x: 噪声图像 (batch, C, H, W)
            t: 时间步 (batch,)
            condition: 控制条件 (batch, condition_C, H, W)

        Returns:
            预测的噪声
        """
        # 获取控制特征
        time_emb = self.unet.time_embed(t)
        control_features = self.control_encoder(condition, time_emb)

        # TODO: 将控制特征注入 UNet
        # 这里简化为直接传递给 UNet
        noise_pred = self.unet(x, t, control_features=control_features)

        return noise_pred

    def train_step(self, x_0, condition, noise_scheduler):
        """训练步骤"""
        batch_size = x_0.shape[0]

        # 随机时间步
        t = torch.randint(0, noise_scheduler.num_steps, (batch_size,), device=x_0.device)

        # 添加噪声
        noise = torch.randn_like(x_0)
        x_t = noise_scheduler.add_noise(x_0, noise, t)

        # 预测噪声
        noise_pred = self(x_t, t, condition)

        # TODO: 计算损失
        loss = F.mse_loss(noise_pred, ___)  # 填入 noise

        return loss


class ConditionEncoder(nn.Module):
    """
    条件编码器

    将不同类型的条件 (边缘、深度、姿态等) 编码为统一格式
    """

    def __init__(self, condition_type, out_channels):
        super().__init__()
        self.condition_type = condition_type

        if condition_type == 'canny':
            # Canny 边缘: 1 通道二值图
            in_channels = 1
        elif condition_type == 'depth':
            # 深度图: 1 通道
            in_channels = 1
        elif condition_type == 'pose':
            # 姿态: 可能是多通道热图
            in_channels = 18
        elif condition_type == 'segmentation':
            # 语义分割: 多通道
            in_channels = 150
        else:
            in_channels = 3

        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels, 64, 3, padding=1),
            nn.SiLU(),
            nn.Conv2d(64, 128, 3, padding=1, stride=2),
            nn.SiLU(),
            nn.Conv2d(128, out_channels, 3, padding=1),
        )

    def forward(self, condition):
        return self.encoder(condition)


def prepare_canny_condition(image, low_threshold=100, high_threshold=200):
    """
    准备 Canny 边缘条件 (模拟)

    实际使用时需要 cv2.Canny
    """
    # 这里使用 Sobel 算子近似
    sobel_x = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=torch.float32)
    sobel_y = sobel_x.t()

    sobel_x = sobel_x.view(1, 1, 3, 3)
    sobel_y = sobel_y.view(1, 1, 3, 3)

    if image.dim() == 3:
        image = image.unsqueeze(0)

    # 转灰度
    gray = image.mean(dim=1, keepdim=True)

    # Sobel 边缘
    edge_x = F.conv2d(gray, sobel_x, padding=1)
    edge_y = F.conv2d(gray, sobel_y, padding=1)

    edge = torch.sqrt(edge_x**2 + edge_y**2)

    # 二值化
    edge = (edge > edge.mean()).float()

    return edge


def main():
    torch.manual_seed(42)

    print("测试 ZeroConv2d...")
    zero_conv = ZeroConv2d(64, 64)
    x = torch.randn(2, 64, 32, 32)
    out = zero_conv(x)

    # 验证初始输出接近零
    assert out.abs().max() < 1e-6, "ZeroConv 初始输出应该接近零"
    print(f"✓ ZeroConv 输出最大值: {out.abs().max():.6f}")

    print("\n测试 ControlNetBlock...")
    block = ControlNetBlock(64, 128, time_emb_dim=256)
    x = torch.randn(2, 64, 32, 32)
    t_emb = torch.randn(2, 256)
    out = block(x, t_emb)
    assert out.shape == (2, 128, 32, 32)
    print(f"✓ Block 输出: {out.shape}")

    print("\n测试 ControlNetEncoder...")
    encoder = ControlNetEncoder(
        condition_channels=1,
        base_channels=64,
        channel_mults=[1, 2, 4],
        time_emb_dim=256
    )
    condition = torch.randn(2, 1, 64, 64)  # Canny 边缘
    t_emb = torch.randn(2, 256)

    features = encoder(condition, t_emb)
    print(f"✓ 生成 {len(features)} 层控制特征:")
    for i, f in enumerate(features):
        print(f"    层 {i}: {f.shape}")

    print("\n测试 ConditionEncoder...")
    for cond_type in ['canny', 'depth', 'pose']:
        enc = ConditionEncoder(cond_type, out_channels=64)
        if cond_type == 'canny':
            cond = torch.randn(2, 1, 64, 64)
        elif cond_type == 'depth':
            cond = torch.randn(2, 1, 64, 64)
        else:
            cond = torch.randn(2, 18, 64, 64)

        out = enc(cond)
        print(f"  ✓ {cond_type}: {cond.shape} -> {out.shape}")

    print("\n测试 Canny 条件准备...")
    image = torch.randn(3, 256, 256)
    canny = prepare_canny_condition(image)
    print(f"✓ Canny 条件: {canny.shape}")

    print("\n🎉 所有测试通过！ControlNet 掌握完成！")


if __name__ == "__main__":
    main()
