/**
 * 练习 03: 创建逻辑设备与队列
 *
 * 学习目标:
 * - 理解队列族的概念
 * - 创建逻辑设备
 * - 获取设备队列
 *
 * 逻辑设备是物理设备的接口，我们通过它与 GPU 交互。
 * 队列是提交命令到 GPU 的通道。
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <iostream>
#include <stdexcept>
#include <cstdlib>
#include <vector>
#include <optional>

const uint32_t WIDTH = 800;
const uint32_t HEIGHT = 600;

// 队列族索引结构
struct QueueFamilyIndices {
    std::optional<uint32_t> graphicsFamily;

    bool isComplete() {
        return graphicsFamily.has_value();
    }
};

class LogicalDeviceApp {
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
    VkDevice device = VK_NULL_HANDLE;        // 逻辑设备
    VkQueue graphicsQueue = VK_NULL_HANDLE;  // 图形队列

    void initWindow() {
        glfwInit();
        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
        window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkan Study - Exercise 03: Logical Device", nullptr, nullptr);
    }

    void initVulkan() {
        createInstance();
        pickPhysicalDevice();
        createLogicalDevice();
    }

    void createInstance() {
        VkApplicationInfo appInfo{};
        appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
        appInfo.pApplicationName = "Vulkanlings Exercise 03";
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
        uint32_t deviceCount = 0;
        vkEnumeratePhysicalDevices(instance, &deviceCount, nullptr);

        if (deviceCount == 0) {
            throw std::runtime_error("Failed to find GPUs with Vulkan support!");
        }

        std::vector<VkPhysicalDevice> devices(deviceCount);
        vkEnumeratePhysicalDevices(instance, &deviceCount, devices.data());

        for (const auto& dev : devices) {
            if (isDeviceSuitable(dev)) {
                physicalDevice = dev;
                break;
            }
        }

        if (physicalDevice == VK_NULL_HANDLE) {
            throw std::runtime_error("Failed to find a suitable GPU!");
        }

        VkPhysicalDeviceProperties deviceProperties;
        vkGetPhysicalDeviceProperties(physicalDevice, &deviceProperties);
        std::cout << "Selected GPU: " << deviceProperties.deviceName << std::endl;
    }

    bool isDeviceSuitable(VkPhysicalDevice dev) {
        QueueFamilyIndices indices = findQueueFamilies(dev);
        return indices.isComplete();
    }

    QueueFamilyIndices findQueueFamilies(VkPhysicalDevice dev) {
        QueueFamilyIndices indices;

        // TODO: 获取队列族数量
        // 提示: 使用 vkGetPhysicalDeviceQueueFamilyProperties(dev, &queueFamilyCount, nullptr)
        // ========== 在下方填写代码 ==========

        uint32_t queueFamilyCount = 0;
        /* ??? */

        // ========== 填写结束 ==========

        // TODO: 获取队列族属性
        // 提示: 使用 vkGetPhysicalDeviceQueueFamilyProperties(dev, &queueFamilyCount, queueFamilies.data())
        // ========== 在下方填写代码 ==========

        std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
        /* ??? */

        // ========== 填写结束 ==========

        int i = 0;
        for (const auto& queueFamily : queueFamilies) {
            // TODO: 检查是否支持图形操作
            // 提示: 检查 queueFamily.queueFlags 是否包含 VK_QUEUE_GRAPHICS_BIT
            // ========== 在下方填写代码 ==========

            if (queueFamily.queueFlags & /* ??? */) {
                indices.graphicsFamily = i;
            }

            // ========== 填写结束 ==========

            if (indices.isComplete()) {
                break;
            }

            i++;
        }

        return indices;
    }

    void createLogicalDevice() {
        QueueFamilyIndices indices = findQueueFamilies(physicalDevice);

        // 队列创建信息
        VkDeviceQueueCreateInfo queueCreateInfo{};

        // TODO: 设置结构体类型
        // 提示: sType 应该是 VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO
        // ========== 在下方填写代码 ==========

        queueCreateInfo.sType = /* ??? */;

        // ========== 填写结束 ==========

        queueCreateInfo.queueFamilyIndex = indices.graphicsFamily.value();
        queueCreateInfo.queueCount = 1;

        float queuePriority = 1.0f;
        queueCreateInfo.pQueuePriorities = &queuePriority;

        // 设备特性（目前不需要任何特殊特性）
        VkPhysicalDeviceFeatures deviceFeatures{};

        // 逻辑设备创建信息
        VkDeviceCreateInfo createInfo{};

        // TODO: 设置结构体类型
        // 提示: sType 应该是 VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO
        // ========== 在下方填写代码 ==========

        createInfo.sType = /* ??? */;

        // ========== 填写结束 ==========

        createInfo.pQueueCreateInfos = &queueCreateInfo;
        createInfo.queueCreateInfoCount = 1;
        createInfo.pEnabledFeatures = &deviceFeatures;
        createInfo.enabledExtensionCount = 0;
        createInfo.enabledLayerCount = 0;

        // TODO: 创建逻辑设备
        // 提示: 使用 vkCreateDevice(physicalDevice, &createInfo, nullptr, &device)
        // ========== 在下方填写代码 ==========

        if (/* ??? */ != VK_SUCCESS) {
            throw std::runtime_error("Failed to create logical device!");
        }

        // ========== 填写结束 ==========

        std::cout << "Logical device created." << std::endl;

        // TODO: 获取图形队列
        // 提示: 使用 vkGetDeviceQueue(device, indices.graphicsFamily.value(), 0, &graphicsQueue)
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        std::cout << "Graphics queue obtained." << std::endl;
    }

    void mainLoop() {
        std::cout << "\nRunning... (Close window to exit)" << std::endl;
        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents();
        }
    }

    void cleanup() {
        // TODO: 销毁逻辑设备
        // 提示: 使用 vkDestroyDevice(device, nullptr)
        // 注意: 队列会随逻辑设备自动销毁
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        vkDestroyInstance(instance, nullptr);
        glfwDestroyWindow(window);
        glfwTerminate();

        std::cout << "Cleanup complete!" << std::endl;
    }
};

int main() {
    std::cout << "=========================================" << std::endl;
    std::cout << "  Vulkanlings Exercise 03: Logical Device" << std::endl;
    std::cout << "=========================================" << std::endl;
    std::cout << std::endl;

    LogicalDeviceApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "\nExercise 03 completed successfully!" << std::endl;
    return EXIT_SUCCESS;
}
