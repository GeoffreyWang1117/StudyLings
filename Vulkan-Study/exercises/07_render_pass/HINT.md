# 练习 07 提示

## 渲染通道概念

渲染通道 (Render Pass) 描述了渲染操作的结构：
- **附件 (Attachments)**: 渲染目标（颜色缓冲、深度缓冲等）
- **子通道 (Subpasses)**: 渲染阶段
- **依赖 (Dependencies)**: 子通道之间的同步

## 附件描述

```cpp
VkAttachmentDescription colorAttachment{};
colorAttachment.format = swapChainImageFormat;      // 图像格式
colorAttachment.samples = VK_SAMPLE_COUNT_1_BIT;    // 采样数
colorAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;     // 加载时清除
colorAttachment.storeOp = VK_ATTACHMENT_STORE_OP_STORE;   // 存储渲染结果
colorAttachment.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
colorAttachment.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
colorAttachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;      // 初始布局
colorAttachment.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;  // 最终布局
```

### 加载操作
- `VK_ATTACHMENT_LOAD_OP_LOAD`: 保留现有内容
- `VK_ATTACHMENT_LOAD_OP_CLEAR`: 清除为常量值
- `VK_ATTACHMENT_LOAD_OP_DONT_CARE`: 不关心

### 存储操作
- `VK_ATTACHMENT_STORE_OP_STORE`: 存储到内存
- `VK_ATTACHMENT_STORE_OP_DONT_CARE`: 不需要存储

### 图像布局
- `VK_IMAGE_LAYOUT_UNDEFINED`: 未定义
- `VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL`: 颜色附件最优
- `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR`: 呈现源

## 子通道

```cpp
VkSubpassDescription subpass{};
subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
subpass.colorAttachmentCount = 1;
subpass.pColorAttachments = &colorAttachmentRef;
```

## 创建渲染通道

```cpp
VkRenderPassCreateInfo createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
createInfo.attachmentCount = 1;
createInfo.pAttachments = &colorAttachment;
createInfo.subpassCount = 1;
createInfo.pSubpasses = &subpass;

vkCreateRenderPass(device, &createInfo, nullptr, &renderPass);
```

## 需要填写的答案

1. 附件格式: `swapChainImageFormat`
2. 加载操作: `VK_ATTACHMENT_LOAD_OP_CLEAR`
3. 存储操作: `VK_ATTACHMENT_STORE_OP_STORE`
4. 初始布局: `VK_IMAGE_LAYOUT_UNDEFINED`
5. 最终布局: `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR`
6. 附件引用布局: `VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL`
7. 管线绑定点: `VK_PIPELINE_BIND_POINT_GRAPHICS`
8. 结构体类型: `VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO`
9. 创建渲染通道: `vkCreateRenderPass(device, &renderPassInfo, nullptr, &renderPass)`
10. 销毁渲染通道: `vkDestroyRenderPass(device, renderPass, nullptr);`
