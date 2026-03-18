#pragma once

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <iostream>
#include <vector>
#include <optional>
#include <set>
#include <string>
#include <cstring>
#include <algorithm>
#include <fstream>
#include <stdexcept>
#include <functional>
#include <array>
#include <limits>
#include <cstdint>

// 验证层名称
const std::vector<const char*> validationLayers = {
    "VK_LAYER_KHRONOS_validation"
};

// 设备扩展
const std::vector<const char*> deviceExtensions = {
    VK_KHR_SWAPCHAIN_EXTENSION_NAME
};

#ifdef ENABLE_VALIDATION_LAYERS
    constexpr bool enableValidationLayers = true;
#else
    constexpr bool enableValidationLayers = false;
#endif

// 队列族索引
struct QueueFamilyIndices {
    std::optional<uint32_t> graphicsFamily;
    std::optional<uint32_t> presentFamily;

    bool isComplete() const {
        return graphicsFamily.has_value() && presentFamily.has_value();
    }
};

// 交换链支持信息
struct SwapChainSupportDetails {
    VkSurfaceCapabilitiesKHR capabilities;
    std::vector<VkSurfaceFormatKHR> formats;
    std::vector<VkPresentModeKHR> presentModes;
};

namespace VulkanUtils {

// 检查验证层支持
bool checkValidationLayerSupport();

// 获取所需扩展
std::vector<const char*> getRequiredExtensions();

// 创建调试信使
VkResult createDebugUtilsMessengerEXT(
    VkInstance instance,
    const VkDebugUtilsMessengerCreateInfoEXT* pCreateInfo,
    const VkAllocationCallbacks* pAllocator,
    VkDebugUtilsMessengerEXT* pDebugMessenger
);

// 销毁调试信使
void destroyDebugUtilsMessengerEXT(
    VkInstance instance,
    VkDebugUtilsMessengerEXT debugMessenger,
    const VkAllocationCallbacks* pAllocator
);

// 调试回调函数
VKAPI_ATTR VkBool32 VKAPI_CALL debugCallback(
    VkDebugUtilsMessageSeverityFlagBitsEXT messageSeverity,
    VkDebugUtilsMessageTypeFlagsEXT messageType,
    const VkDebugUtilsMessengerCallbackDataEXT* pCallbackData,
    void* pUserData
);

// 填充调试信使创建信息
void populateDebugMessengerCreateInfo(VkDebugUtilsMessengerCreateInfoEXT& createInfo);

// 查找队列族
QueueFamilyIndices findQueueFamilies(VkPhysicalDevice device, VkSurfaceKHR surface);

// 检查设备扩展支持
bool checkDeviceExtensionSupport(VkPhysicalDevice device);

// 查询交换链支持
SwapChainSupportDetails querySwapChainSupport(VkPhysicalDevice device, VkSurfaceKHR surface);

// 检查设备是否适合
bool isDeviceSuitable(VkPhysicalDevice device, VkSurfaceKHR surface);

// 设备评分
int rateDeviceSuitability(VkPhysicalDevice device);

// 选择交换链表面格式
VkSurfaceFormatKHR chooseSwapSurfaceFormat(const std::vector<VkSurfaceFormatKHR>& availableFormats);

// 选择交换链呈现模式
VkPresentModeKHR chooseSwapPresentMode(const std::vector<VkPresentModeKHR>& availablePresentModes);

// 选择交换链范围
VkExtent2D chooseSwapExtent(const VkSurfaceCapabilitiesKHR& capabilities, GLFWwindow* window);

// 查找内存类型
uint32_t findMemoryType(VkPhysicalDevice physicalDevice, uint32_t typeFilter, VkMemoryPropertyFlags properties);

// 创建缓冲
void createBuffer(
    VkDevice device,
    VkPhysicalDevice physicalDevice,
    VkDeviceSize size,
    VkBufferUsageFlags usage,
    VkMemoryPropertyFlags properties,
    VkBuffer& buffer,
    VkDeviceMemory& bufferMemory
);

// 复制缓冲
void copyBuffer(
    VkDevice device,
    VkCommandPool commandPool,
    VkQueue graphicsQueue,
    VkBuffer srcBuffer,
    VkBuffer dstBuffer,
    VkDeviceSize size
);

// 开始单次命令
VkCommandBuffer beginSingleTimeCommands(VkDevice device, VkCommandPool commandPool);

// 结束单次命令
void endSingleTimeCommands(
    VkDevice device,
    VkCommandPool commandPool,
    VkQueue queue,
    VkCommandBuffer commandBuffer
);

// 创建图像
void createImage(
    VkDevice device,
    VkPhysicalDevice physicalDevice,
    uint32_t width,
    uint32_t height,
    VkFormat format,
    VkImageTiling tiling,
    VkImageUsageFlags usage,
    VkMemoryPropertyFlags properties,
    VkImage& image,
    VkDeviceMemory& imageMemory
);

// 创建图像视图
VkImageView createImageView(
    VkDevice device,
    VkImage image,
    VkFormat format,
    VkImageAspectFlags aspectFlags
);

// 查找支持的格式
VkFormat findSupportedFormat(
    VkPhysicalDevice physicalDevice,
    const std::vector<VkFormat>& candidates,
    VkImageTiling tiling,
    VkFormatFeatureFlags features
);

// 查找深度格式
VkFormat findDepthFormat(VkPhysicalDevice physicalDevice);

// 是否有模板组件
bool hasStencilComponent(VkFormat format);

// 转换图像布局
void transitionImageLayout(
    VkDevice device,
    VkCommandPool commandPool,
    VkQueue queue,
    VkImage image,
    VkFormat format,
    VkImageLayout oldLayout,
    VkImageLayout newLayout
);

// VK_CHECK 宏 - 检查 Vulkan 调用结果
#define VK_CHECK(call) \
    do { \
        VkResult result = call; \
        if (result != VK_SUCCESS) { \
            std::cerr << "Vulkan error at " << __FILE__ << ":" << __LINE__ \
                      << " - " << result << std::endl; \
            throw std::runtime_error("Vulkan call failed"); \
        } \
    } while(0)

} // namespace VulkanUtils
