# 练习 17: 深度缓冲

## 学习目标
- 创建深度图像
- 配置深度测试
- 正确处理 3D 场景的遮挡

## 关键概念

### 深度格式选择
```cpp
VkFormat depthFormat = findDepthFormat();
// 常见格式: VK_FORMAT_D32_SFLOAT, VK_FORMAT_D24_UNORM_S8_UINT
```

### 渲染通道配置
```cpp
VkAttachmentDescription depthAttachment{};
depthAttachment.format = depthFormat;
depthAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
depthAttachment.storeOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
depthAttachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
depthAttachment.finalLayout = VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL;
```

### 管线深度状态
```cpp
VkPipelineDepthStencilStateCreateInfo depthStencil{};
depthStencil.depthTestEnable = VK_TRUE;
depthStencil.depthWriteEnable = VK_TRUE;
depthStencil.depthCompareOp = VK_COMPARE_OP_LESS;
```

## 任务
在 main.cpp 中完成 TODO 标记的代码。
