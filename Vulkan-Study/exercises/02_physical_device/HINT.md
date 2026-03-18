# 练习 02 提示

## 枚举物理设备

Vulkan 中枚举物理设备分两步：

```cpp
// 第一步：获取设备数量
uint32_t deviceCount = 0;
vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);

// 第二步：获取设备列表
std::vector<VkPhysicalDevice> devices(deviceCount);
vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());
```

## 获取设备属性

```cpp
VkPhysicalDeviceProperties deviceProperties;
vkGetPhysicalDeviceProperties(device, &deviceProperties);

// 可以访问：
// deviceProperties.deviceName - 设备名称
// deviceProperties.deviceType - 设备类型
// deviceProperties.apiVersion - API 版本
// deviceProperties.limits - 设备限制
```

## 获取设备特性

```cpp
VkPhysicalDeviceFeatures deviceFeatures;
vkGetPhysicalDeviceFeatures(device, &deviceFeatures);

// 可以检查：
// deviceFeatures.geometryShader - 几何着色器支持
// deviceFeatures.tessellationShader - 曲面细分支持
// deviceFeatures.samplerAnisotropy - 各向异性过滤
```

## 检查 VK_NULL_HANDLE

```cpp
if (physicalDevice == VK_NULL_HANDLE) {
    throw std::runtime_error("Failed to find a suitable GPU!");
}
```

## 需要填写的答案

1. 枚举设备数量: `vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);`
2. 获取设备列表: `vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());`
3. 空句柄检查: `VK_NULL_HANDLE`
4. 获取属性: `vkGetPhysicalDeviceProperties(device, &deviceProperties);`
5. 获取特性: `vkGetPhysicalDeviceFeatures(device, &deviceFeatures);`
