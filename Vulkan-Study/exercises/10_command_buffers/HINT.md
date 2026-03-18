# 练习 10 提示

## 命令池

命令池用于分配命令缓冲的内存：

```cpp
VkCommandPoolCreateInfo poolInfo{};
poolInfo.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
poolInfo.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
poolInfo.queueFamilyIndex = graphicsQueueFamily;

VkCommandPool commandPool;
vkCreateCommandPool(device, &poolInfo, nullptr, &commandPool);
```

### 命令池标志
- `VK_COMMAND_POOL_CREATE_TRANSIENT_BIT`: 命令缓冲生命周期短
- `VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT`: 允许单独重置

## 命令缓冲分配

```cpp
VkCommandBufferAllocateInfo allocInfo{};
allocInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
allocInfo.commandPool = commandPool;
allocInfo.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
allocInfo.commandBufferCount = count;

std::vector<VkCommandBuffer> commandBuffers(count);
vkAllocateCommandBuffers(device, &allocInfo, commandBuffers.data());
```

### 命令缓冲级别
- `VK_COMMAND_BUFFER_LEVEL_PRIMARY`: 主命令缓冲，可直接提交到队列
- `VK_COMMAND_BUFFER_LEVEL_SECONDARY`: 辅助命令缓冲，由主缓冲调用

## 录制命令

```cpp
// 开始录制
VkCommandBufferBeginInfo beginInfo{};
beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
vkBeginCommandBuffer(commandBuffer, &beginInfo);

// 开始渲染通道
VkRenderPassBeginInfo renderPassInfo{};
renderPassInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
renderPassInfo.renderPass = renderPass;
renderPassInfo.framebuffer = framebuffer;
vkCmdBeginRenderPass(commandBuffer, &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);

// 绘制命令...

// 结束渲染通道
vkCmdEndRenderPass(commandBuffer);

// 结束录制
vkEndCommandBuffer(commandBuffer);
```

## 需要填写的答案

1. 命令池类型: `VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO`
2. 命令池标志: `VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT`
3. 队列族索引: `queueFamilyIndices.graphicsFamily.value()`
4. 创建命令池: `vkCreateCommandPool(device, &poolInfo, nullptr, &commandPool)`
5. 分配信息类型: `VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO`
6. 命令池: `commandPool`
7. 命令缓冲级别: `VK_COMMAND_BUFFER_LEVEL_PRIMARY`
8. 分配命令缓冲: `vkAllocateCommandBuffers(device, &allocInfo, commandBuffers.data())`
9. 开始渲染通道: `vkCmdBeginRenderPass(commandBuffers[i], &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);`
10. 结束渲染通道: `vkCmdEndRenderPass(commandBuffers[i]);`
11. 销毁命令池: `vkDestroyCommandPool(device, commandPool, nullptr);`
