/**
 * 练习 09: 创建帧缓冲
 *
 * 学习目标:
 * - 理解帧缓冲的作用
 * - 为每个交换链图像创建帧缓冲
 * - 理解帧缓冲与渲染通道的关系
 *
 * 帧缓冲是渲染通道附件的具体实例，
 * 它引用图像视图作为实际的渲染目标。
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <iostream>
#include <stdexcept>
#include <vector>
#include <optional>
#include <set>
#include <algorithm>
#include <limits>
#include <array>

const uint32_t WIDTH = 800;
const uint32_t HEIGHT = 600;
const std::vector<const char*> deviceExtensions = {VK_KHR_SWAPCHAIN_EXTENSION_NAME};

struct QueueFamilyIndices {
    std::optional<uint32_t> graphicsFamily;
    std::optional<uint32_t> presentFamily;
    bool isComplete() { return graphicsFamily.has_value() && presentFamily.has_value(); }
};

struct SwapChainSupportDetails {
    VkSurfaceCapabilitiesKHR capabilities;
    std::vector<VkSurfaceFormatKHR> formats;
    std::vector<VkPresentModeKHR> presentModes;
};

class FramebufferApp {
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
    VkSurfaceKHR surface = VK_NULL_HANDLE;
    VkPhysicalDevice physicalDevice = VK_NULL_HANDLE;
    VkDevice device = VK_NULL_HANDLE;
    VkQueue graphicsQueue = VK_NULL_HANDLE;
    VkQueue presentQueue = VK_NULL_HANDLE;
    VkSwapchainKHR swapChain = VK_NULL_HANDLE;
    std::vector<VkImage> swapChainImages;
    VkFormat swapChainImageFormat;
    VkExtent2D swapChainExtent;
    std::vector<VkImageView> swapChainImageViews;
    VkRenderPass renderPass = VK_NULL_HANDLE;
    VkPipelineLayout pipelineLayout = VK_NULL_HANDLE;
    std::vector<VkFramebuffer> swapChainFramebuffers;  // 帧缓冲

    void initWindow() {
        glfwInit();
        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
        window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkan Study - Exercise 09: Framebuffers", nullptr, nullptr);
    }

    void initVulkan() {
        createInstance();
        createSurface();
        pickPhysicalDevice();
        createLogicalDevice();
        createSwapChain();
        createImageViews();
        createRenderPass();
        createPipelineLayout();
        createFramebuffers();
    }

    // 辅助函数（简化版 - 与前面练习相同）
    void createInstance() {
        VkApplicationInfo appInfo{};
        appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
        appInfo.pApplicationName = "Vulkanlings Exercise 09";
        appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
        appInfo.pEngineName = "No Engine";
        appInfo.engineVersion = VK_MAKE_VERSION(1, 0, 0);
        appInfo.apiVersion = VK_API_VERSION_1_2;
        VkInstanceCreateInfo createInfo{};
        createInfo.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
        createInfo.pApplicationInfo = &appInfo;
        uint32_t glfwExtCount = 0;
        const char** glfwExts = glfwGetRequiredInstanceExtensions(&glfwExtCount);
        createInfo.enabledExtensionCount = glfwExtCount;
        createInfo.ppEnabledExtensionNames = glfwExts;
        if (vkCreateInstance(&createInfo, nullptr, &instance) != VK_SUCCESS)
            throw std::runtime_error("Failed to create instance!");
    }

    void createSurface() {
        if (glfwCreateWindowSurface(instance, window, nullptr, &surface) != VK_SUCCESS)
            throw std::runtime_error("Failed to create surface!");
    }

    QueueFamilyIndices findQueueFamilies(VkPhysicalDevice dev) {
        QueueFamilyIndices indices;
        uint32_t count = 0;
        vkGetPhysicalDeviceQueueFamilyProperties(dev, &count, nullptr);
        std::vector<VkQueueFamilyProperties> families(count);
        vkGetPhysicalDeviceQueueFamilyProperties(dev, &count, families.data());
        int i = 0;
        for (const auto& f : families) {
            if (f.queueFlags & VK_QUEUE_GRAPHICS_BIT) indices.graphicsFamily = i;
            VkBool32 present = false;
            vkGetPhysicalDeviceSurfaceSupportKHR(dev, i, surface, &present);
            if (present) indices.presentFamily = i;
            if (indices.isComplete()) break;
            i++;
        }
        return indices;
    }

    SwapChainSupportDetails querySwapChainSupport(VkPhysicalDevice dev) {
        SwapChainSupportDetails details;
        vkGetPhysicalDeviceSurfaceCapabilitiesKHR(dev, surface, &details.capabilities);
        uint32_t fmtCount;
        vkGetPhysicalDeviceSurfaceFormatsKHR(dev, surface, &fmtCount, nullptr);
        if (fmtCount) { details.formats.resize(fmtCount); vkGetPhysicalDeviceSurfaceFormatsKHR(dev, surface, &fmtCount, details.formats.data()); }
        uint32_t pmCount;
        vkGetPhysicalDeviceSurfacePresentModesKHR(dev, surface, &pmCount, nullptr);
        if (pmCount) { details.presentModes.resize(pmCount); vkGetPhysicalDeviceSurfacePresentModesKHR(dev, surface, &pmCount, details.presentModes.data()); }
        return details;
    }

    bool checkDeviceExtSupport(VkPhysicalDevice dev) {
        uint32_t count;
        vkEnumerateDeviceExtensionProperties(dev, nullptr, &count, nullptr);
        std::vector<VkExtensionProperties> exts(count);
        vkEnumerateDeviceExtensionProperties(dev, nullptr, &count, exts.data());
        std::set<std::string> required(deviceExtensions.begin(), deviceExtensions.end());
        for (const auto& e : exts) required.erase(e.extensionName);
        return required.empty();
    }

    bool isDeviceSuitable(VkPhysicalDevice dev) {
        auto indices = findQueueFamilies(dev);
        bool extOk = checkDeviceExtSupport(dev);
        bool scOk = false;
        if (extOk) { auto sc = querySwapChainSupport(dev); scOk = !sc.formats.empty() && !sc.presentModes.empty(); }
        return indices.isComplete() && extOk && scOk;
    }

    void pickPhysicalDevice() {
        uint32_t count = 0;
        vkEnumeratePhysicalDevices(instance, &count, nullptr);
        std::vector<VkPhysicalDevice> devs(count);
        vkEnumeratePhysicalDevices(instance, &count, devs.data());
        for (const auto& d : devs) { if (isDeviceSuitable(d)) { physicalDevice = d; break; } }
        if (physicalDevice == VK_NULL_HANDLE) throw std::runtime_error("Failed to find suitable GPU!");
    }

    void createLogicalDevice() {
        auto indices = findQueueFamilies(physicalDevice);
        std::vector<VkDeviceQueueCreateInfo> queueInfos;
        std::set<uint32_t> uniqueFamilies = {indices.graphicsFamily.value(), indices.presentFamily.value()};
        float priority = 1.0f;
        for (uint32_t f : uniqueFamilies) {
            VkDeviceQueueCreateInfo info{}; info.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
            info.queueFamilyIndex = f; info.queueCount = 1; info.pQueuePriorities = &priority;
            queueInfos.push_back(info);
        }
        VkPhysicalDeviceFeatures features{};
        VkDeviceCreateInfo info{}; info.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
        info.pQueueCreateInfos = queueInfos.data(); info.queueCreateInfoCount = static_cast<uint32_t>(queueInfos.size());
        info.pEnabledFeatures = &features; info.enabledExtensionCount = static_cast<uint32_t>(deviceExtensions.size());
        info.ppEnabledExtensionNames = deviceExtensions.data();
        if (vkCreateDevice(physicalDevice, &info, nullptr, &device) != VK_SUCCESS) throw std::runtime_error("Failed to create device!");
        vkGetDeviceQueue(device, indices.graphicsFamily.value(), 0, &graphicsQueue);
        vkGetDeviceQueue(device, indices.presentFamily.value(), 0, &presentQueue);
    }

    void createSwapChain() {
        auto support = querySwapChainSupport(physicalDevice);
        VkSurfaceFormatKHR fmt = support.formats[0];
        for (const auto& f : support.formats) if (f.format == VK_FORMAT_B8G8R8A8_SRGB && f.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR) { fmt = f; break; }
        VkPresentModeKHR mode = VK_PRESENT_MODE_FIFO_KHR;
        for (const auto& m : support.presentModes) if (m == VK_PRESENT_MODE_MAILBOX_KHR) { mode = m; break; }
        VkExtent2D extent = support.capabilities.currentExtent;
        if (extent.width == std::numeric_limits<uint32_t>::max()) {
            int w, h; glfwGetFramebufferSize(window, &w, &h);
            extent = {std::clamp((uint32_t)w, support.capabilities.minImageExtent.width, support.capabilities.maxImageExtent.width),
                      std::clamp((uint32_t)h, support.capabilities.minImageExtent.height, support.capabilities.maxImageExtent.height)};
        }
        uint32_t imgCount = support.capabilities.minImageCount + 1;
        if (support.capabilities.maxImageCount > 0 && imgCount > support.capabilities.maxImageCount) imgCount = support.capabilities.maxImageCount;

        VkSwapchainCreateInfoKHR info{}; info.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
        info.surface = surface; info.minImageCount = imgCount; info.imageFormat = fmt.format; info.imageColorSpace = fmt.colorSpace;
        info.imageExtent = extent; info.imageArrayLayers = 1; info.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;
        auto indices = findQueueFamilies(physicalDevice);
        uint32_t qfIndices[] = {indices.graphicsFamily.value(), indices.presentFamily.value()};
        if (indices.graphicsFamily != indices.presentFamily) { info.imageSharingMode = VK_SHARING_MODE_CONCURRENT; info.queueFamilyIndexCount = 2; info.pQueueFamilyIndices = qfIndices; }
        else { info.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE; }
        info.preTransform = support.capabilities.currentTransform; info.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
        info.presentMode = mode; info.clipped = VK_TRUE; info.oldSwapchain = VK_NULL_HANDLE;
        if (vkCreateSwapchainKHR(device, &info, nullptr, &swapChain) != VK_SUCCESS) throw std::runtime_error("Failed to create swap chain!");
        vkGetSwapchainImagesKHR(device, swapChain, &imgCount, nullptr);
        swapChainImages.resize(imgCount);
        vkGetSwapchainImagesKHR(device, swapChain, &imgCount, swapChainImages.data());
        swapChainImageFormat = fmt.format; swapChainExtent = extent;
    }

    void createImageViews() {
        swapChainImageViews.resize(swapChainImages.size());
        for (size_t i = 0; i < swapChainImages.size(); i++) {
            VkImageViewCreateInfo info{}; info.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
            info.image = swapChainImages[i]; info.viewType = VK_IMAGE_VIEW_TYPE_2D; info.format = swapChainImageFormat;
            info.components = {VK_COMPONENT_SWIZZLE_IDENTITY,VK_COMPONENT_SWIZZLE_IDENTITY,VK_COMPONENT_SWIZZLE_IDENTITY,VK_COMPONENT_SWIZZLE_IDENTITY};
            info.subresourceRange = {VK_IMAGE_ASPECT_COLOR_BIT, 0, 1, 0, 1};
            if (vkCreateImageView(device, &info, nullptr, &swapChainImageViews[i]) != VK_SUCCESS) throw std::runtime_error("Failed to create image view!");
        }
    }

    void createRenderPass() {
        VkAttachmentDescription colorAttachment{};
        colorAttachment.format = swapChainImageFormat; colorAttachment.samples = VK_SAMPLE_COUNT_1_BIT;
        colorAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR; colorAttachment.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
        colorAttachment.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE; colorAttachment.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
        colorAttachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED; colorAttachment.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;
        VkAttachmentReference colorRef{}; colorRef.attachment = 0; colorRef.layout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;
        VkSubpassDescription subpass{}; subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
        subpass.colorAttachmentCount = 1; subpass.pColorAttachments = &colorRef;
        VkSubpassDependency dep{}; dep.srcSubpass = VK_SUBPASS_EXTERNAL; dep.dstSubpass = 0;
        dep.srcStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT; dep.srcAccessMask = 0;
        dep.dstStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT; dep.dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
        VkRenderPassCreateInfo info{}; info.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
        info.attachmentCount = 1; info.pAttachments = &colorAttachment;
        info.subpassCount = 1; info.pSubpasses = &subpass;
        info.dependencyCount = 1; info.pDependencies = &dep;
        if (vkCreateRenderPass(device, &info, nullptr, &renderPass) != VK_SUCCESS) throw std::runtime_error("Failed to create render pass!");
    }

    void createPipelineLayout() {
        VkPipelineLayoutCreateInfo info{}; info.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
        if (vkCreatePipelineLayout(device, &info, nullptr, &pipelineLayout) != VK_SUCCESS)
            throw std::runtime_error("Failed to create pipeline layout!");
    }

    void createFramebuffers() {
        // 为每个交换链图像视图创建帧缓冲
        swapChainFramebuffers.resize(swapChainImageViews.size());

        for (size_t i = 0; i < swapChainImageViews.size(); i++) {
            // 帧缓冲附件（只有一个颜色附件）
            std::array<VkImageView, 1> attachments = {
                swapChainImageViews[i]
            };

            VkFramebufferCreateInfo framebufferInfo{};

            // TODO: 设置结构体类型
            // 提示: VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO
            // ========== 在下方填写代码 ==========

            framebufferInfo.sType = /* ??? */;

            // ========== 填写结束 ==========

            // TODO: 设置渲染通道
            // 提示: 帧缓冲必须与渲染通道兼容
            // ========== 在下方填写代码 ==========

            framebufferInfo.renderPass = /* ??? */;

            // ========== 填写结束 ==========

            // TODO: 设置附件数量和附件数组
            // 提示: attachmentCount = attachments.size()
            //       pAttachments = attachments.data()
            // ========== 在下方填写代码 ==========

            framebufferInfo.attachmentCount = static_cast<uint32_t>(/* ??? */);
            framebufferInfo.pAttachments = /* ??? */;

            // ========== 填写结束 ==========

            // TODO: 设置帧缓冲尺寸
            // 提示: 使用交换链范围
            // ========== 在下方填写代码 ==========

            framebufferInfo.width = /* ??? */;
            framebufferInfo.height = /* ??? */;

            // ========== 填写结束 ==========

            framebufferInfo.layers = 1;  // 非立体渲染

            // TODO: 创建帧缓冲
            // 提示: vkCreateFramebuffer(device, &framebufferInfo, nullptr, &swapChainFramebuffers[i])
            // ========== 在下方填写代码 ==========

            if (/* ??? */ != VK_SUCCESS) {
                throw std::runtime_error("Failed to create framebuffer!");
            }

            // ========== 填写结束 ==========
        }

        std::cout << "Created " << swapChainFramebuffers.size() << " framebuffers." << std::endl;
    }

    void mainLoop() {
        std::cout << "\nRunning... (Close window to exit)" << std::endl;
        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents();
        }
    }

    void cleanup() {
        // TODO: 销毁所有帧缓冲
        // 提示: 遍历 swapChainFramebuffers，使用 vkDestroyFramebuffer
        // ========== 在下方填写代码 ==========

        for (auto framebuffer : swapChainFramebuffers) {
            /* ??? */
        }

        // ========== 填写结束 ==========

        vkDestroyPipelineLayout(device, pipelineLayout, nullptr);
        vkDestroyRenderPass(device, renderPass, nullptr);
        for (auto iv : swapChainImageViews) vkDestroyImageView(device, iv, nullptr);
        vkDestroySwapchainKHR(device, swapChain, nullptr);
        vkDestroyDevice(device, nullptr);
        vkDestroySurfaceKHR(instance, surface, nullptr);
        vkDestroyInstance(instance, nullptr);
        glfwDestroyWindow(window);
        glfwTerminate();
        std::cout << "Cleanup complete!" << std::endl;
    }
};

int main() {
    std::cout << "=========================================" << std::endl;
    std::cout << "  Vulkanlings Exercise 09: Framebuffers  " << std::endl;
    std::cout << "=========================================" << std::endl;
    std::cout << std::endl;

    FramebufferApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "\nExercise 09 completed successfully!" << std::endl;
    return EXIT_SUCCESS;
}
