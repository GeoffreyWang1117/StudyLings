/**
 * 练习 04: 创建窗口表面
 *
 * 学习目标:
 * - 理解 VkSurfaceKHR 的作用
 * - 使用 GLFW 创建 Vulkan 表面
 * - 查找支持呈现的队列族
 *
 * 表面是 Vulkan 与窗口系统之间的接口，
 * 它让我们可以将渲染结果显示到窗口上。
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <iostream>
#include <stdexcept>
#include <cstdlib>
#include <vector>
#include <optional>
#include <set>

const uint32_t WIDTH = 800;
const uint32_t HEIGHT = 600;

struct QueueFamilyIndices {
    std::optional<uint32_t> graphicsFamily;
    std::optional<uint32_t> presentFamily;  // 新增：呈现队列族

    bool isComplete() {
        return graphicsFamily.has_value() && presentFamily.has_value();
    }
};

class SurfaceApp {
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
    VkSurfaceKHR surface = VK_NULL_HANDLE;  // 窗口表面
    VkPhysicalDevice physicalDevice = VK_NULL_HANDLE;
    VkDevice device = VK_NULL_HANDLE;
    VkQueue graphicsQueue = VK_NULL_HANDLE;
    VkQueue presentQueue = VK_NULL_HANDLE;  // 呈现队列

    void initWindow() {
        glfwInit();
        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
        window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkan Study - Exercise 04: Surface", nullptr, nullptr);
    }

    void initVulkan() {
        createInstance();
        createSurface();  // 注意：表面必须在选择物理设备之前创建
        pickPhysicalDevice();
        createLogicalDevice();
    }

    void createInstance() {
        VkApplicationInfo appInfo{};
        appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
        appInfo.pApplicationName = "Vulkanlings Exercise 04";
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

    void createSurface() {
        // TODO: 使用 GLFW 创建 Vulkan 表面
        // 提示: 使用 glfwCreateWindowSurface(instance, window, nullptr, &surface)
        //       这个函数会自动处理不同平台的差异
        // ========== 在下方填写代码 ==========

        VkResult result = /* ??? */;
        if (result != VK_SUCCESS) {
            throw std::runtime_error("Failed to create window surface!");
        }

        // ========== 填写结束 ==========

        std::cout << "Window surface created." << std::endl;
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

        uint32_t queueFamilyCount = 0;
        vkGetPhysicalDeviceQueueFamilyProperties(dev, &queueFamilyCount, nullptr);

        std::vector<VkQueueFamilyProperties> queueFamilies(queueFamilyCount);
        vkGetPhysicalDeviceQueueFamilyProperties(dev, &queueFamilyCount, queueFamilies.data());

        int i = 0;
        for (const auto& queueFamily : queueFamilies) {
            // 检查图形支持
            if (queueFamily.queueFlags & VK_QUEUE_GRAPHICS_BIT) {
                indices.graphicsFamily = i;
            }

            // TODO: 检查呈现支持
            // 提示: 使用 vkGetPhysicalDeviceSurfaceSupportKHR(dev, i, surface, &presentSupport)
            //       如果 presentSupport 为 VK_TRUE，则该队列族支持呈现
            // ========== 在下方填写代码 ==========

            VkBool32 presentSupport = false;
            /* ??? */

            if (presentSupport) {
                indices.presentFamily = i;
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

        // 创建多个队列（如果图形和呈现队列族不同）
        std::vector<VkDeviceQueueCreateInfo> queueCreateInfos;
        std::set<uint32_t> uniqueQueueFamilies = {
            indices.graphicsFamily.value(),
            indices.presentFamily.value()
        };

        float queuePriority = 1.0f;
        for (uint32_t queueFamily : uniqueQueueFamilies) {
            VkDeviceQueueCreateInfo queueCreateInfo{};
            queueCreateInfo.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
            queueCreateInfo.queueFamilyIndex = queueFamily;
            queueCreateInfo.queueCount = 1;
            queueCreateInfo.pQueuePriorities = &queuePriority;
            queueCreateInfos.push_back(queueCreateInfo);
        }

        VkPhysicalDeviceFeatures deviceFeatures{};

        VkDeviceCreateInfo createInfo{};
        createInfo.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
        createInfo.pQueueCreateInfos = queueCreateInfos.data();
        createInfo.queueCreateInfoCount = static_cast<uint32_t>(queueCreateInfos.size());
        createInfo.pEnabledFeatures = &deviceFeatures;
        createInfo.enabledExtensionCount = 0;
        createInfo.enabledLayerCount = 0;

        if (vkCreateDevice(physicalDevice, &createInfo, nullptr, &device) != VK_SUCCESS) {
            throw std::runtime_error("Failed to create logical device!");
        }

        std::cout << "Logical device created." << std::endl;

        // 获取图形队列
        vkGetDeviceQueue(device, indices.graphicsFamily.value(), 0, &graphicsQueue);

        // TODO: 获取呈现队列
        // 提示: 使用 vkGetDeviceQueue(device, indices.presentFamily.value(), 0, &presentQueue)
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        std::cout << "Graphics queue family index: " << indices.graphicsFamily.value() << std::endl;
        std::cout << "Present queue family index: " << indices.presentFamily.value() << std::endl;

        if (indices.graphicsFamily.value() == indices.presentFamily.value()) {
            std::cout << "Graphics and present queues are from the same family." << std::endl;
        } else {
            std::cout << "Graphics and present queues are from different families." << std::endl;
        }
    }

    void mainLoop() {
        std::cout << "\nRunning... (Close window to exit)" << std::endl;
        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents();
        }
    }

    void cleanup() {
        vkDestroyDevice(device, nullptr);

        // TODO: 销毁窗口表面
        // 提示: 使用 vkDestroySurfaceKHR(instance, surface, nullptr)
        // 注意: 表面必须在实例之前销毁
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
    std::cout << "  Vulkanlings Exercise 04: Surface       " << std::endl;
    std::cout << "=========================================" << std::endl;
    std::cout << std::endl;

    SurfaceApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "\nExercise 04 completed successfully!" << std::endl;
    return EXIT_SUCCESS;
}
