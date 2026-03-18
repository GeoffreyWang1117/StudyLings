# 练习 05 提示

## 交换链概念

交换链是一系列等待呈现到屏幕的图像队列。它实现了双缓冲或三缓冲机制：
- **双缓冲**: 一张图像显示，另一张正在渲染
- **三缓冲**: 减少等待时间，提高性能

## 查询交换链支持

```cpp
// 获取表面能力
vkGetPhysicalDeviceSurfaceCapabilitiesKHR(device, surface, &capabilities);

// 获取表面格式
uint32_t formatCount;
vkGetPhysicalDeviceSurfaceFormatsKHR(device, surface, &formatCount, nullptr);
std::vector<VkSurfaceFormatKHR> formats(formatCount);
vkGetPhysicalDeviceSurfaceFormatsKHR(device, surface, &formatCount, formats.data());

// 获取呈现模式
uint32_t presentModeCount;
vkGetPhysicalDeviceSurfacePresentModesKHR(device, surface, &presentModeCount, nullptr);
std::vector<VkPresentModeKHR> presentModes(presentModeCount);
vkGetPhysicalDeviceSurfacePresentModesKHR(device, surface, &presentModeCount, presentModes.data());
```

## 选择最佳设置

### 表面格式
```cpp
// 优先选择 SRGB 颜色空间
if (format.format == VK_FORMAT_B8G8R8A8_SRGB &&
    format.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR) {
    // 理想选择
}
```

### 呈现模式
- `VK_PRESENT_MODE_IMMEDIATE_KHR`: 立即显示，可能撕裂
- `VK_PRESENT_MODE_FIFO_KHR`: 垂直同步，必须支持
- `VK_PRESENT_MODE_FIFO_RELAXED_KHR`: 宽松的垂直同步
- `VK_PRESENT_MODE_MAILBOX_KHR`: 三缓冲，推荐使用

## 创建交换链

```cpp
VkSwapchainCreateInfoKHR createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
createInfo.surface = surface;
// ... 其他设置

vkCreateSwapchainKHR(device, &createInfo, nullptr, &swapChain);
```

## 销毁交换链

```cpp
vkDestroySwapchainKHR(device, swapChain, nullptr);
```

## 需要填写的答案

1. 获取表面能力: `vkGetPhysicalDeviceSurfaceCapabilitiesKHR(dev, surface, &details.capabilities);`
2. 获取呈现模式数量: `vkGetPhysicalDeviceSurfacePresentModesKHR(dev, surface, &presentModeCount, nullptr);`
3. 获取呈现模式数据: `vkGetPhysicalDeviceSurfacePresentModesKHR(dev, surface, &presentModeCount, details.presentModes.data());`
4. 格式: `VK_FORMAT_B8G8R8A8_SRGB`
5. 颜色空间: `VK_COLOR_SPACE_SRGB_NONLINEAR_KHR`
6. 呈现模式: `VK_PRESENT_MODE_MAILBOX_KHR`
7. 结构体类型: `VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR`
8. 创建交换链: `vkCreateSwapchainKHR(device, &createInfo, nullptr, &swapChain)`
9. 销毁交换链: `vkDestroySwapchainKHR(device, swapChain, nullptr);`
