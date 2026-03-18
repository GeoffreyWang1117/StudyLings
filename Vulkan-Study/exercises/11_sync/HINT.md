# 练习 11 提示

## Vulkan 同步概述

Vulkan 提供了多种同步原语：
- **信号量 (Semaphore)**: GPU-GPU 同步
- **栅栏 (Fence)**: CPU-GPU 同步
- **事件 (Event)**: 细粒度同步
- **管线屏障 (Pipeline Barrier)**: 命令之间的依赖

## 信号量

信号量用于在 GPU 操作之间同步：

```cpp
// 创建信号量
VkSemaphoreCreateInfo semaphoreInfo{};
semaphoreInfo.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;

VkSemaphore semaphore;
vkCreateSemaphore(device, &semaphoreInfo, nullptr, &semaphore);

// 销毁信号量
vkDestroySemaphore(device, semaphore, nullptr);
```

### 典型使用
- `imageAvailableSemaphore`: 交换链图像可用时触发
- `renderFinishedSemaphore`: 渲染完成时触发

## 栅栏

栅栏用于 CPU 等待 GPU 完成：

```cpp
// 创建栅栏
VkFenceCreateInfo fenceInfo{};
fenceInfo.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
fenceInfo.flags = VK_FENCE_CREATE_SIGNALED_BIT;  // 初始已触发

VkFence fence;
vkCreateFence(device, &fenceInfo, nullptr, &fence);

// 等待栅栏
vkWaitForFences(device, 1, &fence, VK_TRUE, UINT64_MAX);

// 重置栅栏
vkResetFences(device, 1, &fence);

// 销毁栅栏
vkDestroyFence(device, fence, nullptr);
```

## 渲染循环中的同步

```
1. 等待上一帧的栅栏 (CPU 等待 GPU)
2. 获取交换链图像（等待 imageAvailable 信号量）
3. 录制命令缓冲
4. 提交命令（等待 imageAvailable，触发 renderFinished）
5. 呈现图像（等待 renderFinished）
```

## 需要填写的答案

1. 信号量类型: `VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO`
2. 栅栏类型: `VK_STRUCTURE_TYPE_FENCE_CREATE_INFO`
3. 栅栏标志: `VK_FENCE_CREATE_SIGNALED_BIT`
4. 创建信号量: `vkCreateSemaphore(device, &semaphoreInfo, nullptr, &imageAvailableSemaphores[i])`
5. 创建信号量: `vkCreateSemaphore(device, &semaphoreInfo, nullptr, &renderFinishedSemaphores[i])`
6. 创建栅栏: `vkCreateFence(device, &fenceInfo, nullptr, &inFlightFences[i])`
7. 销毁信号量: `vkDestroySemaphore(device, renderFinishedSemaphores[i], nullptr);`
8. 销毁信号量: `vkDestroySemaphore(device, imageAvailableSemaphores[i], nullptr);`
9. 销毁栅栏: `vkDestroyFence(device, inFlightFences[i], nullptr);`
