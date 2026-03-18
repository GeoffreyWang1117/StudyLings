/**
 * 练习 01: 创建 Vulkan 实例
 *
 * 学习目标:
 * - 理解 VkInstance 的作用
 * - 学习如何配置应用程序信息
 * - 启用验证层（调试版本）
 *
 * Vulkan 实例是应用程序与 Vulkan 库之间的连接，
 * 创建实例需要指定应用程序的一些基本信息。
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <iostream>
#include <stdexcept>
#include <cstdlib>
#include <vector>
#include <cstring>

const uint32_t WIDTH = 800;
const uint32_t HEIGHT = 600;

// 验证层列表
const std::vector<const char*> validationLayers = {
    "VK_LAYER_KHRONOS_validation"
};

#ifdef NDEBUG
    const bool enableValidationLayers = false;
#else
    const bool enableValidationLayers = true;
#endif

class VulkanInstanceApp {
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

    void initWindow() {
        glfwInit();
        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
        window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkan Study - Exercise 01: Instance", nullptr, nullptr);
    }

    void initVulkan() {
        createInstance();
    }

    void createInstance() {
        // 检查验证层支持
        if (enableValidationLayers && !checkValidationLayerSupport()) {
            throw std::runtime_error("Validation layers requested, but not available!");
        }

        // TODO: 填写应用程序信息结构体
        // VkApplicationInfo 包含关于应用程序的基本信息
        VkApplicationInfo appInfo{};

        // TODO: 设置结构体类型
        // 提示: sType 应该是 VK_STRUCTURE_TYPE_APPLICATION_INFO
        // ========== 在下方填写代码 ==========

        appInfo.sType = /* ??? */;

        // ========== 填写结束 ==========

        appInfo.pApplicationName = "Vulkanlings Exercise 01";
        appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
        appInfo.pEngineName = "No Engine";
        appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);

        // TODO: 设置 Vulkan API 版本
        // 提示: 使用 VK_API_VERSION_1_2 或 VK_API_VERSION_1_0
        // ========== 在下方填写代码 ==========

        appInfo.apiVersion = /* ??? */;

        // ========== 填写结束 ==========

        // 填写实例创建信息
        VkInstanceCreateInfo createInfo{};

        // TODO: 设置结构体类型
        // 提示: sType 应该是 VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO
        // ========== 在下方填写代码 ==========

        createInfo.sType = /* ??? */;

        // ========== 填写结束 ==========

        // TODO: 设置应用程序信息指针
        // 提示: pApplicationInfo 应该指向 appInfo
        // ========== 在下方填写代码 ==========

        createInfo.pApplicationInfo = /* ??? */;

        // ========== 填写结束 ==========

        // 获取所需扩展
        auto extensions = getRequiredExtensions();
        createInfo.enabledExtensionCount = static_cast<uint32_t>(extensions.size());
        createInfo.ppEnabledExtensionNames = extensions.data();

        // 配置验证层
        if (enableValidationLayers) {
            createInfo.enabledLayerCount = static_cast<uint32_t>(validationLayers.size());
            createInfo.ppEnabledLayerNames = validationLayers.data();
        } else {
            createInfo.enabledLayerCount = 0;
        }

        // TODO: 创建 Vulkan 实例
        // 提示: 使用 vkCreateInstance(&createInfo, nullptr, &instance)
        //       检查返回值是否为 VK_SUCCESS
        // ========== 在下方填写代码 ==========

        VkResult result = /* ??? */;
        if (result != VK_SUCCESS) {
            throw std::runtime_error("Failed to create Vulkan instance!");
        }

        // ========== 填写结束 ==========

        std::cout << "Vulkan instance created successfully!" << std::endl;
        printInstanceInfo();
    }

    bool checkValidationLayerSupport() {
        uint32_t layerCount;
        vkEnumerateInstanceLayerProperties(&layerCount, nullptr);

        std::vector<VkLayerProperties> availableLayers(layerCount);
        vkEnumerateInstanceLayerProperties(&layerCount, availableLayers.data());

        for (const char* layerName : validationLayers) {
            bool layerFound = false;

            for (const auto& layerProperties : availableLayers) {
                if (strcmp(layerName, layerProperties.layerName) == 0) {
                    layerFound = true;
                    break;
                }
            }

            if (!layerFound) {
                return false;
            }
        }

        return true;
    }

    std::vector<const char*> getRequiredExtensions() {
        uint32_t glfwExtensionCount = 0;
        const char** glfwExtensions;
        glfwExtensions = glfwGetRequiredInstanceExtensions(&glfwExtensionCount);

        std::vector<const char*> extensions(glfwExtensions, glfwExtensions + glfwExtensionCount);

        if (enableValidationLayers) {
            extensions.push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
        }

        return extensions;
    }

    void printInstanceInfo() {
        // 打印可用扩展
        uint32_t extensionCount = 0;
        vkEnumerateInstanceExtensionProperties(nullptr, &extensionCount, nullptr);
        std::vector<VkExtensionProperties> extensions(extensionCount);
        vkEnumerateInstanceExtensionProperties(nullptr, &extensionCount, extensions.data());

        std::cout << "\nAvailable Vulkan extensions (" << extensionCount << "):" << std::endl;
        for (const auto& extension : extensions) {
            std::cout << "  - " << extension.extensionName
                      << " (v" << extension.specVersion << ")" << std::endl;
        }
    }

    void mainLoop() {
        std::cout << "\nRunning... (Close window to exit)" << std::endl;
        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents();
        }
    }

    void cleanup() {
        // TODO: 销毁 Vulkan 实例
        // 提示: 使用 vkDestroyInstance(instance, nullptr)
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        glfwDestroyWindow(window);
        glfwTerminate();

        std::cout << "Cleanup complete!" << std::endl;
    }
};

int main() {
    std::cout << "======================================" << std::endl;
    std::cout << "  Vulkanlings Exercise 01: Instance  " << std::endl;
    std::cout << "======================================" << std::endl;
    std::cout << std::endl;

    VulkanInstanceApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "\nExercise 01 completed successfully!" << std::endl;
    return EXIT_SUCCESS;
}
