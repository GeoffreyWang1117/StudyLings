# 练习 01 提示

## VkApplicationInfo

这个结构体包含关于应用程序的信息：

```cpp
VkApplicationInfo appInfo{};
appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
appInfo.pApplicationName = "My App";
appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
appInfo.pEngineName = "No Engine";
appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
appInfo.apiVersion = VK_API_VERSION_1_2;
```

## VkInstanceCreateInfo

这个结构体包含创建实例所需的所有信息：

```cpp
VkInstanceCreateInfo createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
createInfo.pApplicationInfo = &appInfo;
```

## 创建实例

使用 `vkCreateInstance` 创建 Vulkan 实例：

```cpp
VkResult result = vkCreateInstance(&createInfo, nullptr, &instance);
if (result != VK_SUCCESS) {
    throw std::runtime_error("Failed to create instance!");
}
```

## 销毁实例

程序结束时需要销毁实例：

```cpp
vkDestroyInstance(instance, nullptr);
```

## 需要填写的答案

1. `appInfo.sType` = `VK_STRUCTURE_TYPE_APPLICATION_INFO`
2. `appInfo.apiVersion` = `VK_API_VERSION_1_2`
3. `createInfo.sType` = `VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO`
4. `createInfo.pApplicationInfo` = `&appInfo`
5. 创建实例: `vkCreateInstance(&createInfo, nullptr, &instance)`
6. 销毁实例: `vkDestroyInstance(instance, nullptr);`
