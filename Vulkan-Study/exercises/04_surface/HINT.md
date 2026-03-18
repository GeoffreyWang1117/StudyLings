# 练习 04 提示

## 创建窗口表面

GLFW 提供了一个跨平台的函数来创建 Vulkan 表面：

```cpp
VkSurfaceKHR surface;
VkResult result = glfwCreateWindowSurface(instance, window, nullptr, &surface);
if (result != VK_SUCCESS) {
    throw std::runtime_error("Failed to create window surface!");
}
```

这个函数会自动处理不同操作系统（Windows、Linux、macOS）的差异。

## 检查呈现支持

不是所有队列族都支持将图像呈现到表面，我们需要检查：

```cpp
VkBool32 presentSupport = false;
vkGetPhysicalDeviceSurfaceSupportKHR(device, queueFamilyIndex, surface, &presentSupport);

if (presentSupport) {
    // 这个队列族支持呈现
}
```

## 获取呈现队列

```cpp
vkGetDeviceQueue(device, presentFamilyIndex, 0, &presentQueue);
```

## 销毁表面

```cpp
vkDestroySurfaceKHR(instance, surface, nullptr);
```

## 重要顺序

资源创建和销毁的顺序很重要：

创建顺序：
1. Instance
2. Surface (需要 Instance 和 Window)
3. Physical Device (需要 Surface 来检查呈现支持)
4. Logical Device

销毁顺序（与创建相反）：
1. Logical Device
2. Surface
3. Instance
4. Window (GLFW)

## 需要填写的答案

1. 创建表面: `glfwCreateWindowSurface(instance, window, nullptr, &surface)`
2. 检查呈现支持: `vkGetPhysicalDeviceSurfaceSupportKHR(dev, i, surface, &presentSupport);`
3. 获取呈现队列: `vkGetDeviceQueue(device, indices.presentFamily.value(), 0, &presentQueue);`
4. 销毁表面: `vkDestroySurfaceKHR(instance, surface, nullptr);`
