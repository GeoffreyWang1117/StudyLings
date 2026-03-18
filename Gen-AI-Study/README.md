# Genlings - 生成式AI算法填空练习

类似 Rustlings 的交互式学习工具，帮助你掌握生成式AI的核心算法。

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ███████╗███╗   ██╗██╗     ██╗███╗   ██╗ ██████╗ ███████╗ ║
║  ██╔════╝ ██╔════╝████╗  ██║██║     ██║████╗  ██║██╔════╝ ██╔════╝ ║
║  ██║  ███╗█████╗  ██╔██╗ ██║██║     ██║██╔██╗ ██║██║  ███╗███████╗ ║
║  ██║   ██║██╔══╝  ██║╚██╗██║██║     ██║██║╚██╗██║██║   ██║╚════██║ ║
║  ╚██████╔╝███████╗██║ ╚████║███████╗██║██║ ╚████║╚██████╔╝███████║ ║
║   ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ║
║                                                               ║
║           生成式AI算法填空练习 - 从基础到前沿                    ║
╚═══════════════════════════════════════════════════════════════╝
```

## 快速开始

```bash
# 安装依赖
pip install torch numpy

# 开始练习 (监视模式)
python genlings.py watch

# 或者查看所有练习
python genlings.py list
```

## 使用方法

### 监视模式 (推荐)

```bash
python genlings.py watch
```

自动检测文件变化，保存后立即验证。通过后自动进入下一个练习。

### 其他命令

```bash
python genlings.py list      # 查看所有练习和进度
python genlings.py verify    # 验证当前练习
python genlings.py hint <name>  # 获取提示
python genlings.py run <name>   # 运行指定练习
python genlings.py reset     # 重置进度
```

## 练习目录 (67个练习)

### 00 基础知识 (8个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 00 | hello | ★☆☆☆☆ | 欢迎！第一个 Python 程序 |
| 01 | numpy_basics | ★☆☆☆☆ | NumPy 数组操作基础 |
| 02 | tensor_basics | ★☆☆☆☆ | PyTorch 张量基础 |
| 03 | autograd | ★★☆☆☆ | 自动微分机制 |
| 04 | nn_module | ★★☆☆☆ | 神经网络模块基础 |
| 05 | optimizer | ★★☆☆☆ | 优化器 (SGD, Adam) |
| 06 | lr_schedule | ★★☆☆☆ | 学习率调度 |
| 07 | loss_functions | ★★☆☆☆ | 损失函数 |

### 01 文本生成基础 (8个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 08 | embeddings | ★★☆☆☆ | 词嵌入 |
| 09 | positional_encoding | ★★★☆☆ | 位置编码 |
| 10 | rnn_cell | ★★☆☆☆ | RNN 单元 |
| 11 | lstm_cell | ★★★☆☆ | LSTM 单元 |
| 12 | gru_cell | ★★★☆☆ | GRU 单元 |
| 13 | seq2seq | ★★★☆☆ | 序列到序列模型 |
| 14 | beam_search | ★★★☆☆ | 束搜索解码 |
| 15 | bert | ★★★★☆ | BERT 模型 |

### 02 注意力机制 (4个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 16 | attention_score | ★★★☆☆ | 注意力分数计算 |
| 17 | self_attention | ★★★☆☆ | 自注意力机制 |
| 18 | multi_head_attention | ★★★★☆ | 多头注意力 |
| 19 | causal_mask | ★★★☆☆ | 因果掩码 |

### 03 Transformer (4个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 20 | feed_forward | ★★★☆☆ | 前馈网络 |
| 21 | layer_norm | ★★★☆☆ | 层归一化 |
| 22 | transformer_block | ★★★★☆ | Transformer 块 |
| 23 | decoder_only | ★★★★☆ | Decoder-Only 架构 |

### 04 GPT (7个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 24 | tokenizer_bpe | ★★★☆☆ | BPE 分词器 |
| 25 | gpt_model | ★★★★☆ | GPT 模型架构 |
| 26 | kv_cache | ★★★★☆ | KV 缓存加速 |
| 27 | sampling | ★★★☆☆ | 采样策略 |
| 28 | rope | ★★★★★ | 旋转位置编码 RoPE |
| 29 | rmsnorm | ★★★☆☆ | RMSNorm |
| 30 | gqa | ★★★★☆ | 分组查询注意力 GQA |

### 05 图像生成基础 (3个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 31 | conv_basics | ★★☆☆☆ | 卷积基础 |
| 32 | transposed_conv | ★★★☆☆ | 转置卷积 |
| 33 | autoencoder | ★★★☆☆ | 自编码器 |

### 06 VAE (3个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 34 | reparameterization | ★★★★☆ | 重参数化技巧 |
| 35 | vae_loss | ★★★★☆ | VAE 损失函数 |
| 36 | vae_model | ★★★★☆ | 完整 VAE 模型 |

### 07 GAN (7个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 37 | discriminator | ★★★☆☆ | 判别器 |
| 38 | generator | ★★★☆☆ | 生成器 |
| 39 | gan_loss | ★★★★☆ | GAN 损失函数 |
| 40 | dcgan | ★★★★☆ | DCGAN |
| 41 | spectral_norm | ★★★★☆ | 谱归一化 |
| 42 | cgan | ★★★★☆ | 条件 GAN |
| 43 | stylegan | ★★★★★ | StyleGAN 核心组件 |

### 08 Diffusion (10个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 44 | noise_schedule | ★★★☆☆ | 噪声调度 |
| 45 | forward_diffusion | ★★★☆☆ | 前向扩散 |
| 46 | unet | ★★★★☆ | U-Net 架构 |
| 47 | time_embedding | ★★★☆☆ | 时间步嵌入 |
| 48 | reverse_diffusion | ★★★★☆ | 反向扩散 |
| 49 | ddpm_loss | ★★★★☆ | DDPM 损失 |
| 50 | ddim | ★★★★★ | DDIM 加速采样 |
| 51 | cfg | ★★★★☆ | Classifier-Free Guidance |
| 52 | controlnet | ★★★★☆ | ControlNet |
| 53 | img2img | ★★★★☆ | 图像到图像生成 |

### 09 多模态基础 (3个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 54 | patch_embedding | ★★★☆☆ | 图像块嵌入 |
| 55 | vit | ★★★★☆ | Vision Transformer |
| 56 | contrastive_loss | ★★★★☆ | 对比学习损失 |

### 10 CLIP (3个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 57 | clip_encoders | ★★★★☆ | CLIP 编码器 |
| 58 | clip_loss | ★★★★☆ | CLIP 损失函数 |
| 59 | clip_inference | ★★★☆☆ | CLIP 零样本推理 |

### 11 Stable Diffusion (4个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 60 | cross_attention | ★★★★☆ | 交叉注意力 |
| 61 | latent_diffusion | ★★★★★ | 潜在扩散 |
| 62 | sd_unet | ★★★★★ | SD U-Net |
| 63 | text_to_image | ★★★★★ | 文本到图像生成 |

### 12 LLM 进阶 (4个)
| # | 练习 | 难度 | 描述 |
|---|------|-----|------|
| 64 | lora | ★★★★☆ | LoRA 参数高效微调 |
| 65 | flash_attention | ★★★★★ | Flash Attention |
| 66 | quantization | ★★★★☆ | 量化 (INT8/INT4) |
| 67 | moe | ★★★★★ | 混合专家 (MoE) |

## 如何完成练习

每个练习文件中都有 `TODO` 标记和 `___` 空白处：

```python
# TODO: 创建一个包含 [1, 2, 3, 4, 5] 的一维数组
arr = np.___([1, 2, 3, 4, 5])  # 使用 np.array()
```

你需要：
1. 找到 `TODO` 注释
2. 将 `___` 替换为正确的代码
3. 保存文件
4. 自动验证（监视模式）或运行 `python genlings.py verify`

## 学习路径建议

1. **初学者**: 从 00_basics 开始，掌握 PyTorch 基础
2. **NLP 方向**: 01_text → 02_attention → 03_transformer → 04_gpt → 12_llm_advanced
3. **CV 方向**: 05_image → 06_vae → 07_gan → 08_diffusion
4. **多模态**: 09_multimodal → 10_clip → 11_stable_diffusion

## 难度分布

- ★☆☆☆☆ 入门级 (3个)
- ★★☆☆☆ 基础级 (10个)
- ★★★☆☆ 中等级 (17个)
- ★★★★☆ 进阶级 (26个)
- ★★★★★ 挑战级 (11个)

## 依赖

```bash
pip install torch numpy
```

## 进度保存

进度自动保存在 `.genlings_progress.json` 中。

## 贡献

欢迎提交 Issue 和 PR！

## 许可

MIT License
