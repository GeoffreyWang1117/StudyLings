/**
 * 练习 02: 选择物理设备（GPU）
 *
 * 学习目标:
 * - 枚举系统中的物理设备
 * - 查询设备属性和特性
 * - 选择合适的 GPU
 *
 * 物理设备代表系统中的 GPU。我们需要选择一个
 * 支持我们所需功能的设备。
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <iostream>
#include <stdexcept>
#include <cstdlib>
#include <vector>
#include <cstring>
#include <map>

const uint32_t WIDTH = 800;
const uint32_t HEIGHT = 600;

class PhysicalDeviceApp {
public:
    void run() {
        initWindow();
        initVulkan();
        mainLoop();
        cleanup();
    }

private:
    GLFWwindow* window = nullptr;
    VkInstance instance = VK_NULL_HANDLE;
    VkPhysicalDevice physicalDevice = VK_NULL_HANDLE;

    void initWindow() {
        glfwInit();
        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
        window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkan Study - Exercise 02: Physical Device", nullptr, nullptr);
    }

    void initVulkan() {
        createInstance();
        pickPhysicalDevice();
    }

    void createInstance() {
        VkApplicationInfo appInfo{};
        appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
        appInfo.pApplicationName = "Vulkanlings Exercise 02";
        appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
        appInfo.pEngineName = "No Engine";
        appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
        appInfo.apiVersion = VK_API_VERSION_1_2;

        VkInstanceCreateInfo createInfo{};
        createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
        createInfo.pApplicationInfo = &appInfo;

        uint32_t glfwExtensionCount = 0;
        const char** glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);
        createInfo.enabledExtensionCount = glfwExtensionCount;
        createInfo.ppEnabledExtensionNames = glfwExtensions;
        createInfo.enabledLayerCount = 0;

        if (vkCreateInstance(&createInfo, nullptr, &instance) != VK_SUCCESS) {
            throw std::runtime_error("Failed to create instance!");
        }

        std::cout << "Vulkan instance created." << std::endl;
    }

    void pickPhysicalDevice() {
        // TODO: 获取物理设备数量
        // 提示: 使用 vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr)
        // ========== 在下方填写代码 ==========

        uint32_t deviceCount = 0;
        /* ??? */

        // ========== 填写结束 ==========

        if (deviceCount == 0) {
            throw std::runtime_error("Failed to find GPUs with Vulkan support!");
        }

        std::cout << "Found " << deviceCount << " physical device(s)." << std::endl;

        // TODO: 获取物理设备列表
        // 提示: 使用 vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data())
        // ========== 在下方填写代码 ==========

        std::vector<VkPhysicalDevice> devices(deviceCount);
        /* ??? */

        // ========== 填写结束 ==========

        // 打印所有设备信息并评分
        std::multimap<int, VkPhysicalDevice> candidates;

        for (const auto& device : devices) {
            int score = rateDeviceSuitability(device);
            candidates.insert(std::make_pair(score, device));
        }

        // 选择得分最高的设备
        if (candidates.rbegin()->first > 0) {
            physicalDevice = candidates.rbegin()->second;
        }

        // TODO: 检查是否成功选择了设备
        // 提示: physicalDevice 不应该是 VK_NULL_HANDLE
        // ========== 在下方填写代码 ==========

        if (physicalDevice == /* ??? */) {
            throw std::runtime_error("Failed to find a suitable GPU!");
        }

        // ========== 填写结束 ==========

        // 打印选中设备信息
        VkPhysicalDeviceProperties deviceProperties;
        vkGetPhysicalDeviceProperties(physicalDevice, &deviceProperties);
        std::cout << "\nSelected GPU: " << deviceProperties.deviceName << std::endl;
    }

    int rateDeviceSuitability(VkPhysicalDevice device) {
        // TODO: 获取设备属性
        // 提示: 使用 vkGetPhysicalDeviceProperties(device, &deviceProperties)
        // ========== 在下方填写代码 ==========

        VkPhysicalDeviceProperties deviceProperties;
        /* ??? */

        // ========== 填写结束 ==========

        // TODO: 获取设备特性
        // 提示: 使用 vkGetPhysicalDeviceFeatures(device, &deviceFeatures)
        // ========== 在下方填写代码 ==========

        VkPhysicalDeviceFeatures deviceFeatures;
        /* ??? */

        // ========== 填写结束 ==========

        int score = 0;

        // 打印设备信息
        std::cout << "\nDevice: " << deviceProperties.deviceName << std::endl;
        std::cout << "  Type: ";
        switch (deviceProperties.deviceType) {
            case VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU:
                std::cout << "Discrete GPU";
                score += 1000;  // 离散 GPU 得分更高
                break;
            case VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU:
                std::cout << "Integrated GPU";
                score += 500;
                break;
            case VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU:
                std::cout << "Virtual GPU";
                score += 200;
                break;
            case VK_PHYSICAL_DEVICE_TYPE_CPU:
                std::cout << "CPU";
                score += 100;
                break;
            default:
                std::cout << "Unknown";
                break;
        }
        std::cout << std::endl;

        // API 版本
        std::cout << "  API Version: "
                  << VK_VERSION_MAJOR(deviceProperties.apiVersion) << "."
                  << VK_VERSION_MINOR(deviceProperties.apiVersion) << "."
                  << VK_VERSION_PATCH(deviceProperties.apiVersion) << std::endl;

        // 最大纹理尺寸影响评分
        score += deviceProperties.limits.maxImageDimension2D;

        std::cout << "  Max Texture Size: " << deviceProperties.limits.maxImageDimension2D << std::endl;
        std::cout << "  Geometry Shader: " << (deviceFeatures.geometryShader ? "Yes" : "No") << std::endl;
        std::cout << "  Tessellation: " << (deviceFeatures.tessellationShader ? "Yes" : "No") << std::endl;
        std::cout << "  Score: " << score << std::endl;

        return score;
    }

    void mainLoop() {
        std::cout << "\nRunning... (Close window to exit)" << std::endl;
        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents();
        }
    }

    void cleanup() {
        // 注意: 物理设备不需要手动销毁
        // 它会在实例销毁时自动清理
        vkDestroyInstance(instance, nullptr);
        glfwDestroyWindow(window);
        glfwTerminate();

        std::cout << "Cleanup complete!" << std::endl;
    }
};

int main() {
    std::cout << "=========================================" << std::endl;
    std::cout << "  Vulkanlings Exercise 02: Physical Device" << std::endl;
    std::cout << "=========================================" << std::endl;
    std::cout << std::endl;

    PhysicalDeviceApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "\nExercise 02 completed successfully!" << std::endl;
    return EXIT_SUCCESS;
}
