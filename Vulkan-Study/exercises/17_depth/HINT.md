# 练习 17 提示 - 深度缓冲

## 深度格式选择

```cpp
return findSupportedFormat(
    {VK_FORMAT_D32_SFLOAT, VK_FORMAT_D32_SFLOAT_S8_UINT, VK_FORMAT_D24_UNORM_S8_UINT},
    VK_IMAGE_TILING_OPTIMAL,
    VK_FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT
);
```

常用深度格式:
- `VK_FORMAT_D32_SFLOAT`: 32位浮点深度
- `VK_FORMAT_D32_SFLOAT_S8_UINT`: 32位深度 + 8位模板
- `VK_FORMAT_D24_UNORM_S8_UINT`: 24位深度 + 8位模板

## 深度附件描述

```cpp
VkAttachmentDescription depthAttachment{};
depthAttachment.format = depthFormat;
depthAttachment.samples = VK_SAMPLE_COUNT_1_BIT;
depthAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
depthAttachment.storeOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
depthAttachment.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
depthAttachment.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
depthAttachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
depthAttachment.finalLayout = VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL;
```

## 深度附件引用

```cpp
VkAttachmentReference depthAttachmentRef{};
depthAttachmentRef.attachment = 1;
depthAttachmentRef.layout = VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL;
```

## 深度模板状态

```cpp
VkPipelineDepthStencilStateCreateInfo depthStencil{};
depthStencil.sType = VK_STRUCTURE_TYPE_PIPELINE_DEPTH_STENCIL_STATE_CREATE_INFO;
depthStencil.depthTestEnable = VK_TRUE;
depthStencil.depthWriteEnable = VK_TRUE;
depthStencil.depthCompareOp = VK_COMPARE_OP_LESS;
depthStencil.depthBoundsTestEnable = VK_FALSE;
depthStencil.stencilTestEnable = VK_FALSE;
```

比较操作:
- `VK_COMPARE_OP_LESS`: 新值 < 旧值时通过 (常用)
- `VK_COMPARE_OP_LESS_OR_EQUAL`: 新值 <= 旧值时通过
- `VK_COMPARE_OP_GREATER`: 新值 > 旧值时通过 (反向深度)

## 创建深度图像

```cpp
createImage(swapChainExtent.width, swapChainExtent.height,
           depthFormat,
           VK_IMAGE_TILING_OPTIMAL,
           VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT,
           VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
           depthImage, depthImageMemory);
```

## 创建深度图像视图

```cpp
depthImageView = createImageView(depthImage, depthFormat, VK_IMAGE_ASPECT_DEPTH_BIT);
```

## 帧缓冲附件

```cpp
std::array<VkImageView, 2> attachments = {
    swapChainImageViews[i],
    depthImageView
};
```

## 清除值

```cpp
std::array<VkClearValue, 2> clearValues{};
clearValues[0].color = {{0.0f, 0.0f, 0.0f, 1.0f}};
clearValues[1].depthStencil = {1.0f, 0};
```

深度清除值 `1.0f` 表示最远距离 (Vulkan 深度范围是 0-1，0 是近平面，1 是远平面)

## 清理深度资源

```cpp
vkDestroyImageView(device, depthImageView, nullptr);
vkDestroyImage(device, depthImage, nullptr);
vkFreeMemory(device, depthImageMemory, nullptr);
```

## 需要填写的答案

1. 深度格式: `{VK_FORMAT_D32_SFLOAT, VK_FORMAT_D32_SFLOAT_S8_UINT, VK_FORMAT_D24_UNORM_S8_UINT}, VK_IMAGE_TILING_OPTIMAL, VK_FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT`
2. 深度附件: `loadOp=VK_ATTACHMENT_LOAD_OP_CLEAR, storeOp=VK_ATTACHMENT_STORE_OP_DONT_CARE, initialLayout=VK_IMAGE_LAYOUT_UNDEFINED, finalLayout=VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL`
3. 深度引用: `attachment=1, layout=VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL`
4. 深度状态: `depthTestEnable=VK_TRUE, depthWriteEnable=VK_TRUE, depthCompareOp=VK_COMPARE_OP_LESS`
5. 深度图像: `tiling=VK_IMAGE_TILING_OPTIMAL, usage=VK_IMAGE_USAGE_DEPTH_STENCIL_ATTACHMENT_BIT, properties=VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT`
6. 深度视图: `aspectFlags=VK_IMAGE_ASPECT_DEPTH_BIT`
7. 帧缓冲: `attachments = {swapChainImageViews[i], depthImageView}`
8. 清除值: `depthStencil = {1.0f, 0}`
9. 清理: `depthImageView, depthImage, depthImageMemory`
