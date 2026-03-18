# 练习 03 提示

## 队列族

Vulkan 中的命令通过队列提交到 GPU。不同的队列族支持不同类型的操作：
- 图形操作 (VK_QUEUE_GRAPHICS_BIT)
- 计算操作 (VK_QUEUE_COMPUTE_BIT)
- 传输操作 (VK_QUEUE_TRANSFER_BIT)

```cpp
// 获取队列族数量
uint32_t queueFamilyCount = 0;
vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, nullptr);

// 获取队列族属性
std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
vkGetPhysicalDeviceQueueFamilyProperties(device, &queueFamilyCount, queueFamilies.data());

// 检查图形支持
if (queueFamily.queueFlags & VK_QUEUE_GRAPHICS_BIT) {
    // 这个队列族支持图形操作
}
```

## 创建逻辑设备

```cpp
VkDeviceQueueCreateInfo queueCreateInfo{};
queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
queueCreateInfo.queueFamilyIndex = graphicsFamily;
queueCreateInfo.queueCount = 1;
float priority = 1.0f;
queueCreateInfo.pQueuePriorities = &priority;

VkDeviceCreateInfo createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
createInfo.pQueueCreateInfos = &queueCreateInfo;
createInfo.queueCreateInfoCount = 1;

vkCreateDevice(physicalDevice, &createInfo, nullptr, &device);
```

## 获取队列

```cpp
vkGetDeviceQueue(device, graphicsFamily, 0, &graphicsQueue);
```

## 销毁逻辑设备

```cpp
vkDestroyDevice(device, nullptr);
```

## 需要填写的答案

1. 获取队列族数量: `vkGetPhysicalDeviceQueueFamilyProperties(dev, &queueFamilyCount, nullptr);`
2. 获取队列族属性: `vkGetPhysicalDeviceQueueFamilyProperties(dev, &queueFamilyCount, queueFamilies.data());`
3. 图形位标志: `VK_QUEUE_GRAPHICS_BIT`
4. 队列创建信息类型: `VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO`
5. 设备创建信息类型: `VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO`
6. 创建逻辑设备: `vkCreateDevice(physicalDevice, &createInfo, nullptr, &device)`
7. 获取队列: `vkGetDeviceQueue(device, indices.graphicsFamily.value(), 0, &graphicsQueue);`
8. 销毁设备: `vkDestroyDevice(device, nullptr);`
