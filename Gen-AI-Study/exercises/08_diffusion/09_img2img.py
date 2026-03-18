"""
练习 44: 图像到图像 (Image-to-Image)

Img2Img 通过在扩散过程的中间步骤开始，
基于输入图像生成变体。

核心思想：
1. 对输入图像添加噪声到某个时间步
2. 从该时间步开始去噪
3. 控制噪声添加程度来控制与原图的相似度

应用：
- 风格迁移
- 图像编辑
- 超分辨率
- 图像修复

在这个练习中，你将学习：
- Img2Img 流程
- 强度控制 (strength)
- SDEdit 方法
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class NoiseScheduler:
    """简化的噪声调度器"""

    def __init__(self, num_steps=1000, beta_start=0.0001, beta_end=0.02):
        self.num_steps = num_steps

        betas = torch.linspace(beta_start, beta_end, num_steps)
        alphas = 1 - betas
        self.alphas_cumprod = torch.cumprod(alphas, dim=0)
        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1 - self.alphas_cumprod)

    def add_noise(self, x_0, noise, t):
        """添加噪声: x_t = √ᾱ_t * x_0 + √(1-ᾱ_t) * ε"""
        sqrt_alpha = self.sqrt_alphas_cumprod[t].view(-1, 1, 1, 1)
        sqrt_one_minus_alpha = self.sqrt_one_minus_alphas_cumprod[t].view(-1, 1, 1, 1)
        return sqrt_alpha * x_0 + sqrt_one_minus_alpha * noise

    def get_start_timestep(self, strength):
        """根据强度计算起始时间步"""
        # TODO: strength 越高，从越早的时间步开始
        return int(self.num_steps * ___)  # 填入 strength


def img2img(model, scheduler, init_image, prompt_embedding, strength=0.75,
            num_inference_steps=50, guidance_scale=7.5):
    """
    图像到图像生成

    Args:
        model: 扩散模型 (UNet)
        scheduler: 噪声调度器
        init_image: 初始图像 (batch, C, H, W)
        prompt_embedding: 文本条件嵌入
        strength: 修改强度 (0-1)，越高改变越大
        num_inference_steps: 推理步数
        guidance_scale: CFG 引导强度

    Returns:
        生成的图像
    """
    device = init_image.device
    batch_size = init_image.shape[0]

    # TODO: 计算起始时间步
    start_step = scheduler.get_start_timestep(___)  # 填入 strength

    # 实际执行的步数
    actual_steps = num_inference_steps - int(num_inference_steps * (1 - strength))

    # 对初始图像添加噪声
    noise = torch.randn_like(init_image)
    t_start = torch.full((batch_size,), start_step, device=device, dtype=torch.long)
    x_t = scheduler.add_noise(init_image, noise, t_start)

    # 从 start_step 开始去噪
    timesteps = torch.linspace(start_step, 0, actual_steps, dtype=torch.long, device=device)

    for t in timesteps:
        t_batch = torch.full((batch_size,), t.item(), device=device, dtype=torch.long)

        # CFG: 同时计算有条件和无条件输出
        if guidance_scale > 1:
            noise_pred_uncond = model(x_t, t_batch, None)
            noise_pred_cond = model(x_t, t_batch, prompt_embedding)
            # TODO: CFG 组合
            noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_cond - ___)  # 填入 noise_pred_uncond
        else:
            noise_pred = model(x_t, t_batch, prompt_embedding)

        # 去噪步骤 (简化版 DDPM)
        x_t = denoise_step(x_t, noise_pred, t.item(), scheduler)

    return x_t


def denoise_step(x_t, noise_pred, t, scheduler):
    """单步去噪"""
    alpha_t = scheduler.alphas_cumprod[t]

    if t > 0:
        alpha_t_prev = scheduler.alphas_cumprod[t - 1]
    else:
        alpha_t_prev = torch.tensor(1.0)

    beta_t = 1 - alpha_t / alpha_t_prev

    # 预测 x_0
    x_0_pred = (x_t - torch.sqrt(1 - alpha_t) * noise_pred) / torch.sqrt(alpha_t)
    x_0_pred = x_0_pred.clamp(-1, 1)

    # 计算 x_{t-1}
    if t > 0:
        noise = torch.randn_like(x_t)
        x_t_prev = torch.sqrt(alpha_t_prev) * x_0_pred + torch.sqrt(1 - alpha_t_prev) * noise
    else:
        x_t_prev = x_0_pred

    return x_t_prev


class SDEdit:
    """
    SDEdit: 基于引导的图像合成

    通过添加噪声再去噪来编辑图像
    """

    def __init__(self, model, scheduler):
        self.model = model
        self.scheduler = scheduler

    def edit(self, image, edit_strength=0.5, prompt_embedding=None):
        """
        编辑图像

        Args:
            image: 原始图像
            edit_strength: 编辑强度
            prompt_embedding: 可选的文本引导
        """
        return img2img(
            self.model, self.scheduler, image,
            prompt_embedding, strength=edit_strength
        )


def inpaint(model, scheduler, image, mask, prompt_embedding,
            num_inference_steps=50, guidance_scale=7.5):
    """
    图像修复 (Inpainting)

    只在 mask 区域生成新内容

    Args:
        image: 原始图像 (batch, C, H, W)
        mask: 遮罩 (batch, 1, H, W)，1 表示需要修复的区域
        prompt_embedding: 文本条件
    """
    device = image.device
    batch_size = image.shape[0]

    # 从纯噪声开始
    x_t = torch.randn_like(image)

    timesteps = torch.linspace(scheduler.num_steps - 1, 0, num_inference_steps,
                               dtype=torch.long, device=device)

    for t in timesteps:
        t_batch = torch.full((batch_size,), t.item(), device=device, dtype=torch.long)

        # 预测噪声
        noise_pred = model(x_t, t_batch, prompt_embedding)

        # 去噪
        x_t_denoised = denoise_step(x_t, noise_pred, t.item(), scheduler)

        # TODO: 在非遮罩区域保持原始图像
        # x_t = mask * x_t_denoised + (1 - mask) * noised_original
        if t > 0:
            t_prev = torch.full((batch_size,), t.item(), device=device, dtype=torch.long)
            noise = torch.randn_like(image)
            noised_original = scheduler.add_noise(image, noise, t_prev)

            x_t = mask * x_t_denoised + (1 - ___) * noised_original  # 填入 mask
        else:
            x_t = mask * x_t_denoised + (1 - mask) * image

    return x_t


class ImageVariation:
    """
    图像变体生成

    生成与输入图像相似但有变化的新图像
    """

    def __init__(self, model, scheduler, image_encoder=None):
        self.model = model
        self.scheduler = scheduler
        self.image_encoder = image_encoder

    def generate_variations(self, image, num_variations=4, variation_strength=0.7):
        """
        生成多个变体

        Args:
            image: 原始图像
            num_variations: 生成的变体数量
            variation_strength: 变化程度
        """
        # 编码图像作为条件
        if self.image_encoder:
            image_embedding = self.image_encoder(image)
        else:
            image_embedding = None

        variations = []
        for _ in range(num_variations):
            # TODO: 添加不同的噪声产生变体
            noise = torch.randn_like(image)
            t = int(self.scheduler.num_steps * ___)  # 填入 variation_strength
            t_tensor = torch.tensor([t], device=image.device)

            x_t = self.scheduler.add_noise(image, noise, t_tensor)

            # 去噪生成变体
            var = self._denoise(x_t, t, image_embedding)
            variations.append(var)

        return torch.cat(variations, dim=0)

    def _denoise(self, x_t, start_t, condition):
        """从 start_t 去噪到 0"""
        for t in range(start_t, -1, -1):
            t_batch = torch.tensor([t], device=x_t.device)
            noise_pred = self.model(x_t, t_batch, condition)
            x_t = denoise_step(x_t, noise_pred, t, self.scheduler)
        return x_t


def interpolate_latents(z1, z2, num_steps=10):
    """
    潜在空间插值

    在两个潜在向量之间插值，生成平滑过渡
    """
    interpolations = []

    for i in range(num_steps):
        # TODO: 线性插值
        alpha = i / (num_steps - 1)
        z = (1 - ___) * z1 + alpha * z2  # 填入 alpha
        interpolations.append(z)

    return torch.stack(interpolations)


def main():
    torch.manual_seed(42)

    print("测试 NoiseScheduler...")
    scheduler = NoiseScheduler(num_steps=1000)

    # 测试不同强度对应的起始步
    for strength in [0.3, 0.5, 0.75, 1.0]:
        start_step = scheduler.get_start_timestep(strength)
        print(f"  strength={strength} -> start_step={start_step}")

    print("\n测试噪声添加...")
    x_0 = torch.randn(2, 3, 64, 64)
    noise = torch.randn_like(x_0)
    t = torch.tensor([500, 800])

    x_t = scheduler.add_noise(x_0, noise, t)
    assert x_t.shape == x_0.shape
    print(f"✓ 添加噪声后形状: {x_t.shape}")

    # 验证不同时间步的噪声程度
    t_low = torch.tensor([100])
    t_high = torch.tensor([900])
    x_low = scheduler.add_noise(x_0[:1], noise[:1], t_low)
    x_high = scheduler.add_noise(x_0[:1], noise[:1], t_high)

    diff_low = (x_low - x_0[:1]).abs().mean()
    diff_high = (x_high - x_0[:1]).abs().mean()
    print(f"✓ t=100 与原图差异: {diff_low:.4f}")
    print(f"✓ t=900 与原图差异: {diff_high:.4f}")
    assert diff_high > diff_low, "更高的 t 应该有更多噪声"

    print("\n测试潜在空间插值...")
    z1 = torch.randn(1, 4, 8, 8)
    z2 = torch.randn(1, 4, 8, 8)
    interpolations = interpolate_latents(z1, z2, num_steps=5)
    assert interpolations.shape == (5, 1, 4, 8, 8)
    print(f"✓ 插值结果: {interpolations.shape}")

    # 验证端点
    assert torch.allclose(interpolations[0], z1)
    assert torch.allclose(interpolations[-1], z2)
    print("✓ 插值端点验证通过")

    print("\n图像编辑流程说明:")
    print("  1. img2img: 基于原图 + 提示词生成新图")
    print("  2. SDEdit: 添加噪声再去噪进行编辑")
    print("  3. Inpainting: 只修复遮罩区域")
    print("  4. Variation: 生成原图的多个变体")

    print("\n参数影响:")
    print("  strength:")
    print("    - 0.0: 完全保持原图")
    print("    - 0.5: 中等程度修改")
    print("    - 1.0: 完全重新生成")
    print("  guidance_scale:")
    print("    - 1.0: 无引导")
    print("    - 7.5: 标准引导 (推荐)")
    print("    - 15+: 强引导 (可能过饱和)")

    print("\n🎉 所有测试通过！Img2Img 掌握完成！")


if __name__ == "__main__":
    main()
