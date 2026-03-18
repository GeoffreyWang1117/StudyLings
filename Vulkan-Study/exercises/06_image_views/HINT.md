# 练习 06 提示

## 图像视图概念

图像视图 (VkImageView) 描述了如何访问图像：
- 图像的哪些部分可以访问
- 以什么方式解释图像数据
- 使用什么格式

即使是同一个图像，不同的视图可以以不同的方式访问它。

## 创建图像视图

```cpp
VkImageViewCreateInfo createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
createInfo.image = image;
createInfo.viewType = VK_IMAGE_VIEW_TYPE_2D;
createInfo.format = imageFormat;

// 颜色通道映射
createInfo.components.r = VK_COMPONENT_SWIZZLE_IDENTITY;
createInfo.components.g = VK_COMPONENT_SWIZZLE_IDENTITY;
createInfo.components.b = VK_COMPONENT_SWIZZLE_IDENTITY;
createInfo.components.a = VK_COMPONENT_SWIZZLE_IDENTITY;

// 子资源范围
createInfo.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
createInfo.subresourceRange.baseMipLevel = 0;
createInfo.subresourceRange.levelCount = 1;
createInfo.subresourceRange.baseArrayLayer = 0;
createInfo.subresourceRange.layerCount = 1;

VkImageView imageView;
vkCreateImageView(device, &createInfo, nullptr, &imageView);
```

## 视图类型

- `VK_IMAGE_VIEW_TYPE_1D`: 一维纹理
- `VK_IMAGE_VIEW_TYPE_2D`: 二维纹理
- `VK_IMAGE_VIEW_TYPE_3D`: 三维纹理
- `VK_IMAGE_VIEW_TYPE_CUBE`: 立方体贴图
- `VK_IMAGE_VIEW_TYPE_1D_ARRAY`: 一维纹理数组
- `VK_IMAGE_VIEW_TYPE_2D_ARRAY`: 二维纹理数组
- `VK_IMAGE_VIEW_TYPE_CUBE_ARRAY`: 立方体贴图数组

## 子资源范围

- `aspectMask`: 图像的哪个方面（颜色、深度、模板）
- `baseMipLevel`: 起始 mip 级别
- `levelCount`: mip 级别数量
- `baseArrayLayer`: 起始数组层
- `layerCount`: 数组层数量

## 销毁图像视图

```cpp
vkDestroyImageView(device, imageView, nullptr);
```

## 需要填写的答案

1. 结构体类型: `VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO`
2. 图像: `swapChainImages[i]`
3. 视图类型: `VK_IMAGE_VIEW_TYPE_2D`
4. aspectMask: `VK_IMAGE_ASPECT_COLOR_BIT`
5. baseMipLevel: `0`
6. levelCount: `1`
7. baseArrayLayer: `0`
8. layerCount: `1`
9. 创建视图: `vkCreateImageView(device, &createInfo, nullptr, &swapChainImageViews[i])`
10. 销毁视图: `vkDestroyImageView(device, imageView, nullptr);`
