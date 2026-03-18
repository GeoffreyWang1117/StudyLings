/**
 * 练习 08: 创建图形管线
 *
 * 学习目标:
 * - 理解图形管线的各个阶段
 * - 配置管线状态
 * - 加载和创建着色器模块
 *
 * 图形管线是 Vulkan 中最复杂的对象之一，
 * 它定义了从顶点数据到最终像素的整个渲染流程。
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <iostream>
#include <fstream>
#include <stdexcept>
#include <vector>
#include <optional>
#include <set>
#include <algorithm>
#include <limits>

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

class PipelineApp {
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
    VkPipelineLayout pipelineLayout = VK_NULL_HANDLE;  // 管线布局
    VkPipeline graphicsPipeline = VK_NULL_HANDLE;       // 图形管线

    // ... 简化的辅助函数（与前面练习相同）
    void initWindow() {
        glfwInit();
        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
        window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkan Study - Exercise 08: Pipeline", nullptr, nullptr);
    }

    void initVulkan() {
        createInstance();
        createSurface();
        pickPhysicalDevice();
        createLogicalDevice();
        createSwapChain();
        createImageViews();
        createRenderPass();
        createGraphicsPipeline();
    }

    // 辅助函数（简化版）
    void createInstance() {
        VkApplicationInfo appInfo{};
        appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
        appInfo.pApplicationName = "Vulkanlings Exercise 08";
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

    static std::vector<char> readFile(const std::string& filename) {
        std::ifstream file(filename, std::ios::ate | std::ios::binary);
        if (!file.is_open()) throw std::runtime_error("Failed to open file: " + filename);
        size_t fileSize = (size_t)file.tellg();
        std::vector<char> buffer(fileSize);
        file.seekg(0);
        file.read(buffer.data(), fileSize);
        file.close();
        return buffer;
    }

    VkShaderModule createShaderModule(const std::vector<char>& code) {
        VkShaderModuleCreateInfo createInfo{};

        // TODO: 设置结构体类型
        // 提示: VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO
        // ========== 在下方填写代码 ==========

        createInfo.sType = /* ??? */;

        // ========== 填写结束 ==========

        createInfo.codeSize = code.size();
        createInfo.pCode = reinterpret_cast<const uint32_t*>(code.data());

        VkShaderModule shaderModule;
        if (vkCreateShaderModule(device, &createInfo, nullptr, &shaderModule) != VK_SUCCESS) {
            throw std::runtime_error("Failed to create shader module!");
        }
        return shaderModule;
    }

    void createGraphicsPipeline() {
        // 由于本练习没有实际的着色器文件，我们创建一个简化的管线
        // 在实际项目中，你需要加载编译好的 SPIR-V 着色器

        std::cout << "Creating graphics pipeline..." << std::endl;

        // 顶点输入状态（硬编码顶点，不需要输入）
        VkPipelineVertexInputStateCreateInfo vertexInputInfo{};

        // TODO: 设置结构体类型
        // 提示: VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO
        // ========== 在下方填写代码 ==========

        vertexInputInfo.sType = /* ??? */;

        // ========== 填写结束 ==========

        vertexInputInfo.vertexBindingDescriptionCount = 0;
        vertexInputInfo.vertexAttributeDescriptionCount = 0;

        // 输入装配状态
        VkPipelineInputAssemblyStateCreateInfo inputAssembly{};

        // TODO: 设置结构体类型
        // 提示: VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO
        // ========== 在下方填写代码 ==========

        inputAssembly.sType = /* ??? */;

        // ========== 填写结束 ==========

        // TODO: 设置图元拓扑类型（三角形列表）
        // 提示: VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST
        // ========== 在下方填写代码 ==========

        inputAssembly.topology = /* ??? */;

        // ========== 填写结束 ==========

        inputAssembly.primitiveRestartEnable = VK_FALSE;

        // 视口状态（动态设置）
        VkPipelineViewportStateCreateInfo viewportState{};
        viewportState.sType = VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO;
        viewportState.viewportCount = 1;
        viewportState.scissorCount = 1;

        // 光栅化状态
        VkPipelineRasterizationStateCreateInfo rasterizer{};

        // TODO: 设置结构体类型
        // 提示: VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO
        // ========== 在下方填写代码 ==========

        rasterizer.sType = /* ??? */;

        // ========== 填写结束 ==========

        rasterizer.depthClampEnable = VK_FALSE;
        rasterizer.rasterizerDiscardEnable = VK_FALSE;

        // TODO: 设置多边形模式（填充）
        // 提示: VK_POLYGON_MODE_FILL
        // ========== 在下方填写代码 ==========

        rasterizer.polygonMode = /* ??? */;

        // ========== 填写结束 ==========

        rasterizer.lineWidth = 1.0f;

        // TODO: 设置剔除模式（剔除背面）
        // 提示: VK_CULL_MODE_BACK_BIT
        // ========== 在下方填写代码 ==========

        rasterizer.cullMode = /* ??? */;

        // ========== 填写结束 ==========

        // TODO: 设置正面方向（顺时针）
        // 提示: VK_FRONT_FACE_CLOCKWISE
        // ========== 在下方填写代码 ==========

        rasterizer.frontFace = /* ??? */;

        // ========== 填写结束 ==========

        rasterizer.depthBiasEnable = VK_FALSE;

        // 多重采样状态
        VkPipelineMultisampleStateCreateInfo multisampling{};
        multisampling.sType = VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO;
        multisampling.sampleShadingEnable = VK_FALSE;
        multisampling.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;

        // 颜色混合附件
        VkPipelineColorBlendAttachmentState colorBlendAttachment{};
        colorBlendAttachment.colorWriteMask =
            VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT |
            VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT;
        colorBlendAttachment.blendEnable = VK_FALSE;

        // 颜色混合状态
        VkPipelineColorBlendStateCreateInfo colorBlending{};
        colorBlending.sType = VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO;
        colorBlending.logicOpEnable = VK_FALSE;
        colorBlending.attachmentCount = 1;
        colorBlending.pAttachments = &colorBlendAttachment;

        // 动态状态
        std::vector<VkDynamicState> dynamicStates = {
            VK_DYNAMIC_STATE_VIEWPORT,
            VK_DYNAMIC_STATE_SCISSOR
        };

        VkPipelineDynamicStateCreateInfo dynamicState{};
        dynamicState.sType = VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO;
        dynamicState.dynamicStateCount = static_cast<uint32_t>(dynamicStates.size());
        dynamicState.pDynamicStates = dynamicStates.data();

        // 管线布局
        VkPipelineLayoutCreateInfo pipelineLayoutInfo{};

        // TODO: 设置结构体类型
        // 提示: VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO
        // ========== 在下方填写代码 ==========

        pipelineLayoutInfo.sType = /* ??? */;

        // ========== 填写结束 ==========

        pipelineLayoutInfo.setLayoutCount = 0;
        pipelineLayoutInfo.pushConstantRangeCount = 0;

        // TODO: 创建管线布局
        // 提示: vkCreatePipelineLayout(device, &pipelineLayoutInfo, nullptr, &pipelineLayout)
        // ========== 在下方填写代码 ==========

        if (/* ??? */ != VK_SUCCESS) {
            throw std::runtime_error("Failed to create pipeline layout!");
        }

        // ========== 填写结束 ==========

        std::cout << "Pipeline layout created successfully!" << std::endl;
        std::cout << "Note: Full graphics pipeline creation requires shader modules." << std::endl;
        std::cout << "This exercise demonstrates pipeline configuration structure." << std::endl;
    }

    void mainLoop() {
        std::cout << "\nRunning... (Close window to exit)" << std::endl;
        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents();
        }
    }

    void cleanup() {
        // TODO: 销毁管线布局
        // 提示: vkDestroyPipelineLayout(device, pipelineLayout, nullptr)
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

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
    std::cout << "  Vulkanlings Exercise 08: Pipeline      " << std::endl;
    std::cout << "=========================================" << std::endl;
    std::cout << std::endl;

    PipelineApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "\nExercise 08 completed successfully!" << std::endl;
    return EXIT_SUCCESS;
}
