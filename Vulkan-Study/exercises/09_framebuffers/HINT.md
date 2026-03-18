# 练习 09 提示

## 帧缓冲概念

帧缓冲 (Framebuffer) 是渲染通道附件的具体绑定：
- 渲染通道定义了**附件的格式和用途**
- 帧缓冲指定了**具体使用哪些图像视图**

每个交换链图像都需要一个对应的帧缓冲。

## 创建帧缓冲

```cpp
VkFramebufferCreateInfo framebufferInfo{};
framebufferInfo.sType = VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
framebufferInfo.renderPass = renderPass;        // 必须兼容的渲染通道
framebufferInfo.attachmentCount = 1;            // 附件数量
framebufferInfo.pAttachments = &imageView;      // 图像视图数组
framebufferInfo.width = swapChainExtent.width;  // 宽度
framebufferInfo.height = swapChainExtent.height;// 高度
framebufferInfo.layers = 1;                     // 层数

VkFramebuffer framebuffer;
vkCreateFramebuffer(device, &framebufferInfo, nullptr, &framebuffer);
```

## 附件顺序

帧缓冲附件的顺序必须与渲染通道中附件描述的顺序一致：

```cpp
// 如果渲染通道定义了：
// 附件 0: 颜色附件
// 附件 1: 深度附件
// 那么帧缓冲附件数组应该是：
std::array<VkImageView, 2> attachments = {
    colorImageView,  // 对应附件 0
    depthImageView   // 对应附件 1
};
```

## 销毁帧缓冲

```cpp
vkDestroyFramebuffer(device, framebuffer, nullptr);
```

## 生命周期注意

帧缓冲引用的图像视图必须在帧缓冲存在期间有效。销毁顺序：
1. 销毁帧缓冲
2. 销毁图像视图
3. 销毁交换链（自动销毁交换链图像）

## 需要填写的答案

1. 结构体类型: `VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO`
2. 渲染通道: `renderPass`
3. 附件数量: `attachments.size()`
4. 附件数组: `attachments.data()`
5. 宽度: `swapChainExtent.width`
6. 高度: `swapChainExtent.height`
7. 创建帧缓冲: `vkCreateFramebuffer(device, &framebufferInfo, nullptr, &swapChainFramebuffers[i])`
8. 销毁帧缓冲: `vkDestroyFramebuffer(device, framebuffer, nullptr);`
