# 练习 12 提示 - 渲染三角形 🔺

## 渲染循环概述

```
1. 等待上一帧完成 (vkWaitForFences)
2. 获取交换链图像 (vkAcquireNextImageKHR)
3. 重置栅栏 (vkResetFences)
4. 重置命令缓冲 (vkResetCommandBuffer)
5. 录制命令 (vkBeginCommandBuffer ... vkEndCommandBuffer)
6. 提交命令 (vkQueueSubmit)
7. 呈现图像 (vkQueuePresentKHR)
```

## 录制命令缓冲

```cpp
// 开始录制
VkCommandBufferBeginInfo beginInfo{};
beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
vkBeginCommandBuffer(commandBuffer, &beginInfo);

// 开始渲染通道
VkRenderPassBeginInfo renderPassInfo{};
// ... 设置渲染通道信息
vkCmdBeginRenderPass(commandBuffer, &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);

// 绑定管线和绘制
vkCmdBindPipeline(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, pipeline);
vkCmdDraw(commandBuffer, 3, 1, 0, 0);  // 3 个顶点

// 结束
vkCmdEndRenderPass(commandBuffer);
vkEndCommandBuffer(commandBuffer);
```

## 清除颜色

```cpp
// 红色
VkClearValue clearColor = {{{1.0f, 0.0f, 0.0f, 1.0f}}};

// 绿色
VkClearValue clearColor = {{{0.0f, 1.0f, 0.0f, 1.0f}}};

// 蓝色
VkClearValue clearColor = {{{0.0f, 0.0f, 1.0f, 1.0f}}};

// 紫色
VkClearValue clearColor = {{{0.5f, 0.0f, 0.5f, 1.0f}}};
```

## 同步

```cpp
// 等待栅栏
vkWaitForFences(device, 1, &fence, VK_TRUE, UINT64_MAX);

// 重置栅栏
vkResetFences(device, 1, &fence);

// 提交命令（栅栏在完成时触发）
vkQueueSubmit(queue, 1, &submitInfo, fence);
```

## 需要填写的答案

1. 开始命令缓冲: `vkBeginCommandBuffer(cmdBuffer, &beginInfo)`
2. 清除颜色: 例如 `0.2f, 0.3f, 0.8f`（蓝色调）
3. 结束命令缓冲: `vkEndCommandBuffer(cmdBuffer)`
4. 等待栅栏: `vkWaitForFences(device, 1, &inFlightFences[currentFrame], VK_TRUE, UINT64_MAX);`
5. 重置栅栏: `vkResetFences(device, 1, &inFlightFences[currentFrame]);`
6. 提交队列: `vkQueueSubmit(graphicsQueue, 1, &submitInfo, inFlightFences[currentFrame])`

## 恭喜！

如果你能看到一个有颜色的窗口，说明你已经成功实现了 Vulkan 渲染循环的核心部分！

下一步是添加着色器和真正绘制三角形。
