# 练习 16: 纹理映射

## 学习目标
- 加载图像文件
- 创建纹理图像和视图
- 配置采样器
- 在着色器中采样纹理

## 关键概念

### 创建纹理
1. 加载图像数据
2. 创建暂存缓冲
3. 创建图像对象
4. 转换图像布局
5. 复制缓冲到图像
6. 创建图像视图
7. 创建采样器

### 采样器配置
```cpp
VkSamplerCreateInfo samplerInfo{};
samplerInfo.magFilter = VK_FILTER_LINEAR;
samplerInfo.minFilter = VK_FILTER_LINEAR;
samplerInfo.addressModeU = VK_SAMPLER_ADDRESS_MODE_REPEAT;
samplerInfo.anisotropyEnable = VK_TRUE;
```

### 着色器采样
```glsl
layout(binding = 1) uniform sampler2D texSampler;

vec4 color = texture(texSampler, fragTexCoord);
```

## 任务
在 main.cpp 中完成 TODO 标记的代码。
