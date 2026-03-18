/**
 * 练习 13: 顶点缓冲
 *
 * 学习目标:
 * - 创建顶点缓冲存储顶点数据
 * - 使用暂存缓冲进行高效数据传输
 * - 定义顶点输入绑定和属性描述
 *
 * 之前我们使用硬编码在着色器中的顶点数据，
 * 现在我们将学习如何从 CPU 传递顶点数据到 GPU。
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>

#include <iostream>
#include <fstream>
#include <stdexcept>
#include <vector>
#include <array>
#include <optional>
#include <set>
#include <algorithm>
#include <limits>
#include <cstring>

const uint32_t WIDTH = 800;
const uint32_t HEIGHT = 600;
const int MAX_FRAMES_IN_FLIGHT = 2;
const std::vector<const char*> deviceExtensions = {VK_KHR_SWAPCHAIN_EXTENSION_NAME};

// 顶点结构体
struct Vertex {
    glm::vec2 pos;      // 位置
    glm::vec3 color;    // 颜色

    // TODO: 实现顶点绑定描述
    // 提示: 描述顶点数据如何绑定到顶点着色器
    //       binding = 0, stride = sizeof(Vertex), inputRate = VK_VERTEX_INPUT_RATE_VERTEX
    static VkVertexInputBindingDescription getBindingDescription() {
        VkVertexInputBindingDescription bindingDescription{};

        // ========== 在下方填写代码 ==========

        bindingDescription.binding = /* ??? */;
        bindingDescription.stride = /* ??? */;
        bindingDescription.inputRate = /* ??? */;

        // ========== 填写结束 ==========

        return bindingDescription;
    }

    // TODO: 实现顶点属性描述
    // 提示: 描述每个顶点属性的格式和偏移
    //       位置: location=0, format=VK_FORMAT_R32G32_SFLOAT, offset=offsetof(Vertex, pos)
    //       颜色: location=1, format=VK_FORMAT_R32G32B32_SFLOAT, offset=offsetof(Vertex, color)
    static std::array<VkVertexInputAttributeDescription, 2> getAttributeDescriptions() {
        std::array<VkVertexInputAttributeDescription, 2> attributeDescriptions{};

        // 位置属性
        // ========== 在下方填写代码 ==========

        attributeDescriptions[0].binding = 0;
        attributeDescriptions[0].location = /* ??? */;
        attributeDescriptions[0].format = /* ??? */;
        attributeDescriptions[0].offset = offsetof(Vertex, pos);

        // ========== 填写结束 ==========

        // 颜色属性
        // ========== 在下方填写代码 ==========

        attributeDescriptions[1].binding = 0;
        attributeDescriptions[1].location = /* ??? */;
        attributeDescriptions[1].format = /* ??? */;
        attributeDescriptions[1].offset = offsetof(Vertex, color);

        // ========== 填写结束 ==========

        return attributeDescriptions;
    }
};

// 三角形顶点数据
const std::vector<Vertex> vertices = {
    {{0.0f, -0.5f}, {1.0f, 0.0f, 0.0f}},   // 顶部 - 红色
    {{0.5f, 0.5f}, {0.0f, 1.0f, 0.0f}},    // 右下 - 绿色
    {{-0.5f, 0.5f}, {0.0f, 0.0f, 1.0f}}    // 左下 - 蓝色
};

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

class VertexBufferApp {
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
    VkPipeline graphicsPipeline = VK_NULL_HANDLE;
    std::vector<VkFramebuffer> swapChainFramebuffers;
    VkCommandPool commandPool = VK_NULL_HANDLE;
    std::vector<VkCommandBuffer> commandBuffers;
    std::vector<VkSemaphore> imageAvailableSemaphores;
    std::vector<VkSemaphore> renderFinishedSemaphores;
    std::vector<VkFence> inFlightFences;
    uint32_t currentFrame = 0;

    // 顶点缓冲
    VkBuffer vertexBuffer = VK_NULL_HANDLE;
    VkDeviceMemory vertexBufferMemory = VK_NULL_HANDLE;

    void initWindow() {
        glfwInit();
        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
        window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkanlings - Exercise 13: Vertex Buffers", nullptr, nullptr);
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
        createFramebuffers();
        createCommandPool();
        createVertexBuffer();
        createCommandBuffers();
        createSyncObjects();
    }

    // 基础 Vulkan 设置（简化版）
    void createInstance() {
        VkApplicationInfo appInfo{};
        appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
        appInfo.pApplicationName = "Vertex Buffer Exercise";
        appInfo.applicationVersion = VK_MAKE_VERSION(1, 0, 0);
        appInfo.pEngineName = "No Engine";
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
            VkDeviceQueueCreateInfo info{};
            info.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
            info.queueFamilyIndex = f;
            info.queueCount = 1;
            info.pQueuePriorities = &priority;
            queueInfos.push_back(info);
        }
        VkPhysicalDeviceFeatures features{};
        VkDeviceCreateInfo info{};
        info.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
        info.pQueueCreateInfos = queueInfos.data();
        info.queueCreateInfoCount = static_cast<uint32_t>(queueInfos.size());
        info.pEnabledFeatures = &features;
        info.enabledExtensionCount = static_cast<uint32_t>(deviceExtensions.size());
        info.ppEnabledExtensionNames = deviceExtensions.data();
        if (vkCreateDevice(physicalDevice, &info, nullptr, &device) != VK_SUCCESS)
            throw std::runtime_error("Failed to create device!");
        vkGetDeviceQueue(device, indices.graphicsFamily.value(), 0, &graphicsQueue);
        vkGetDeviceQueue(device, indices.presentFamily.value(), 0, &presentQueue);
    }

    void createSwapChain() {
        auto support = querySwapChainSupport(physicalDevice);
        VkSurfaceFormatKHR fmt = support.formats[0];
        for (const auto& f : support.formats)
            if (f.format == VK_FORMAT_B8G8R8A8_SRGB && f.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR) { fmt = f; break; }
        VkPresentModeKHR mode = VK_PRESENT_MODE_FIFO_KHR;
        VkExtent2D extent = support.capabilities.currentExtent;
        if (extent.width == std::numeric_limits<uint32_t>::max()) {
            int w, h; glfwGetFramebufferSize(window, &w, &h);
            extent = {std::clamp((uint32_t)w, support.capabilities.minImageExtent.width, support.capabilities.maxImageExtent.width),
                      std::clamp((uint32_t)h, support.capabilities.minImageExtent.height, support.capabilities.maxImageExtent.height)};
        }
        uint32_t imgCount = support.capabilities.minImageCount + 1;
        if (support.capabilities.maxImageCount > 0 && imgCount > support.capabilities.maxImageCount)
            imgCount = support.capabilities.maxImageCount;

        VkSwapchainCreateInfoKHR info{};
        info.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
        info.surface = surface;
        info.minImageCount = imgCount;
        info.imageFormat = fmt.format;
        info.imageColorSpace = fmt.colorSpace;
        info.imageExtent = extent;
        info.imageArrayLayers = 1;
        info.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;
        auto indices = findQueueFamilies(physicalDevice);
        uint32_t qfIndices[] = {indices.graphicsFamily.value(), indices.presentFamily.value()};
        if (indices.graphicsFamily != indices.presentFamily) {
            info.imageSharingMode = VK_SHARING_MODE_CONCURRENT;
            info.queueFamilyIndexCount = 2;
            info.pQueueFamilyIndices = qfIndices;
        } else {
            info.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
        }
        info.preTransform = support.capabilities.currentTransform;
        info.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
        info.presentMode = mode;
        info.clipped = VK_TRUE;
        if (vkCreateSwapchainKHR(device, &info, nullptr, &swapChain) != VK_SUCCESS)
            throw std::runtime_error("Failed to create swap chain!");
        vkGetSwapchainImagesKHR(device, swapChain, &imgCount, nullptr);
        swapChainImages.resize(imgCount);
        vkGetSwapchainImagesKHR(device, swapChain, &imgCount, swapChainImages.data());
        swapChainImageFormat = fmt.format;
        swapChainExtent = extent;
    }

    void createImageViews() {
        swapChainImageViews.resize(swapChainImages.size());
        for (size_t i = 0; i < swapChainImages.size(); i++) {
            VkImageViewCreateInfo info{};
            info.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
            info.image = swapChainImages[i];
            info.viewType = VK_IMAGE_VIEW_TYPE_2D;
            info.format = swapChainImageFormat;
            info.subresourceRange = {VK_IMAGE_ASPECT_COLOR_BIT, 0, 1, 0, 1};
            if (vkCreateImageView(device, &info, nullptr, &swapChainImageViews[i]) != VK_SUCCESS)
                throw std::runtime_error("Failed to create image view!");
        }
    }

    void createRenderPass() {
        VkAttachmentDescription colorAttachment{};
        colorAttachment.format = swapChainImageFormat;
        colorAttachment.samples = VK_SAMPLE_COUNT_1_BIT;
        colorAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
        colorAttachment.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
        colorAttachment.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
        colorAttachment.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
        colorAttachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
        colorAttachment.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;

        VkAttachmentReference colorRef{};
        colorRef.attachment = 0;
        colorRef.layout = VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL;

        VkSubpassDescription subpass{};
        subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
        subpass.colorAttachmentCount = 1;
        subpass.pColorAttachments = &colorRef;

        VkSubpassDependency dep{};
        dep.srcSubpass = VK_SUBPASS_EXTERNAL;
        dep.dstSubpass = 0;
        dep.srcStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
        dep.dstStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
        dep.dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;

        VkRenderPassCreateInfo info{};
        info.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
        info.attachmentCount = 1;
        info.pAttachments = &colorAttachment;
        info.subpassCount = 1;
        info.pSubpasses = &subpass;
        info.dependencyCount = 1;
        info.pDependencies = &dep;
        if (vkCreateRenderPass(device, &info, nullptr, &renderPass) != VK_SUCCESS)
            throw std::runtime_error("Failed to create render pass!");
    }

    void createGraphicsPipeline() {
        // 创建管线布局
        VkPipelineLayoutCreateInfo pipelineLayoutInfo{};
        pipelineLayoutInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
        if (vkCreatePipelineLayout(device, &pipelineLayoutInfo, nullptr, &pipelineLayout) != VK_SUCCESS)
            throw std::runtime_error("Failed to create pipeline layout!");

        // 注意: 实际管线创建需要着色器模块
        // 这里我们只演示顶点输入的配置方式
        std::cout << "Graphics pipeline created (shader loading skipped for exercise)." << std::endl;
        std::cout << "Vertex input configuration:" << std::endl;
        std::cout << "  - Binding: stride = " << sizeof(Vertex) << " bytes" << std::endl;
        std::cout << "  - Attribute 0: pos (vec2)" << std::endl;
        std::cout << "  - Attribute 1: color (vec3)" << std::endl;
    }

    void createFramebuffers() {
        swapChainFramebuffers.resize(swapChainImageViews.size());
        for (size_t i = 0; i < swapChainImageViews.size(); i++) {
            VkImageView attachments[] = {swapChainImageViews[i]};
            VkFramebufferCreateInfo info{};
            info.sType = VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
            info.renderPass = renderPass;
            info.attachmentCount = 1;
            info.pAttachments = attachments;
            info.width = swapChainExtent.width;
            info.height = swapChainExtent.height;
            info.layers = 1;
            if (vkCreateFramebuffer(device, &info, nullptr, &swapChainFramebuffers[i]) != VK_SUCCESS)
                throw std::runtime_error("Failed to create framebuffer!");
        }
    }

    void createCommandPool() {
        auto indices = findQueueFamilies(physicalDevice);
        VkCommandPoolCreateInfo info{};
        info.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
        info.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
        info.queueFamilyIndex = indices.graphicsFamily.value();
        if (vkCreateCommandPool(device, &info, nullptr, &commandPool) != VK_SUCCESS)
            throw std::runtime_error("Failed to create command pool!");
    }

    // TODO: 查找合适的内存类型
    uint32_t findMemoryType(uint32_t typeFilter, VkMemoryPropertyFlags properties) {
        VkPhysicalDeviceMemoryProperties memProperties;
        vkGetPhysicalDeviceMemoryProperties(physicalDevice, &memProperties);

        for (uint32_t i = 0; i < memProperties.memoryTypeCount; i++) {
            // TODO: 检查内存类型是否满足要求
            // 提示: (typeFilter & (1 << i)) 检查类型是否支持
            //       (memProperties.memoryTypes[i].propertyFlags & properties) == properties 检查属性
            // ========== 在下方填写代码 ==========

            if ((typeFilter & (1 << i)) &&
                (memProperties.memoryTypes[i].propertyFlags & properties) == properties) {
                return i;
            }

            // ========== 填写结束 ==========
        }

        throw std::runtime_error("Failed to find suitable memory type!");
    }

    void createVertexBuffer() {
        VkDeviceSize bufferSize = sizeof(vertices[0]) * vertices.size();

        // TODO: 创建缓冲
        VkBufferCreateInfo bufferInfo{};

        // ========== 在下方填写代码 ==========

        bufferInfo.sType = /* ??? */;
        bufferInfo.size = /* ??? */;
        bufferInfo.usage = /* ??? */;  // 提示: VK_BUFFER_USAGE_VERTEX_BUFFER_BIT
        bufferInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;

        // ========== 填写结束 ==========

        if (vkCreateBuffer(device, &bufferInfo, nullptr, &vertexBuffer) != VK_SUCCESS) {
            throw std::runtime_error("Failed to create vertex buffer!");
        }

        // 获取内存需求
        VkMemoryRequirements memRequirements;
        vkGetBufferMemoryRequirements(device, vertexBuffer, &memRequirements);

        // TODO: 分配内存
        VkMemoryAllocateInfo allocInfo{};

        // ========== 在下方填写代码 ==========

        allocInfo.sType = /* ??? */;
        allocInfo.allocationSize = /* ??? */;
        allocInfo.memoryTypeIndex = findMemoryType(
            memRequirements.memoryTypeBits,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
        );

        // ========== 填写结束 ==========

        if (vkAllocateMemory(device, &allocInfo, nullptr, &vertexBufferMemory) != VK_SUCCESS) {
            throw std::runtime_error("Failed to allocate vertex buffer memory!");
        }

        // TODO: 绑定内存到缓冲
        // 提示: vkBindBufferMemory(device, vertexBuffer, vertexBufferMemory, 0)
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        // TODO: 映射内存并复制顶点数据
        // 提示: vkMapMemory -> memcpy -> vkUnmapMemory
        // ========== 在下方填写代码 ==========

        void* data;
        vkMapMemory(device, vertexBufferMemory, 0, bufferSize, 0, &data);
        /* ??? */  // 复制数据: memcpy(data, vertices.data(), (size_t)bufferSize);
        vkUnmapMemory(device, vertexBufferMemory);

        // ========== 填写结束 ==========

        std::cout << "Vertex buffer created with " << vertices.size() << " vertices." << std::endl;
        std::cout << "Buffer size: " << bufferSize << " bytes." << std::endl;
    }

    void createCommandBuffers() {
        commandBuffers.resize(MAX_FRAMES_IN_FLIGHT);
        VkCommandBufferAllocateInfo info{};
        info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
        info.commandPool = commandPool;
        info.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
        info.commandBufferCount = static_cast<uint32_t>(commandBuffers.size());
        if (vkAllocateCommandBuffers(device, &info, commandBuffers.data()) != VK_SUCCESS)
            throw std::runtime_error("Failed to allocate command buffers!");
    }

    void createSyncObjects() {
        imageAvailableSemaphores.resize(MAX_FRAMES_IN_FLIGHT);
        renderFinishedSemaphores.resize(MAX_FRAMES_IN_FLIGHT);
        inFlightFences.resize(MAX_FRAMES_IN_FLIGHT);
        VkSemaphoreCreateInfo semInfo{};
        semInfo.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;
        VkFenceCreateInfo fenceInfo{};
        fenceInfo.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
        fenceInfo.flags = VK_FENCE_CREATE_SIGNALED_BIT;
        for (size_t i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
            if (vkCreateSemaphore(device, &semInfo, nullptr, &imageAvailableSemaphores[i]) != VK_SUCCESS ||
                vkCreateSemaphore(device, &semInfo, nullptr, &renderFinishedSemaphores[i]) != VK_SUCCESS ||
                vkCreateFence(device, &fenceInfo, nullptr, &inFlightFences[i]) != VK_SUCCESS)
                throw std::runtime_error("Failed to create sync objects!");
        }
    }

    void recordCommandBuffer(VkCommandBuffer cmd, uint32_t imageIndex) {
        VkCommandBufferBeginInfo beginInfo{};
        beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
        if (vkBeginCommandBuffer(cmd, &beginInfo) != VK_SUCCESS)
            throw std::runtime_error("Failed to begin recording command buffer!");

        VkRenderPassBeginInfo renderPassInfo{};
        renderPassInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
        renderPassInfo.renderPass = renderPass;
        renderPassInfo.framebuffer = swapChainFramebuffers[imageIndex];
        renderPassInfo.renderArea.offset = {0, 0};
        renderPassInfo.renderArea.extent = swapChainExtent;
        VkClearValue clearColor = {{{0.1f, 0.1f, 0.15f, 1.0f}}};
        renderPassInfo.clearValueCount = 1;
        renderPassInfo.pClearValues = &clearColor;

        vkCmdBeginRenderPass(cmd, &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);

        // TODO: 绑定顶点缓冲
        // 提示: vkCmdBindVertexBuffers(cmd, 0, 1, buffers, offsets)
        // ========== 在下方填写代码 ==========

        VkBuffer vertexBuffers[] = {vertexBuffer};
        VkDeviceSize offsets[] = {0};
        /* ??? */

        // ========== 填写结束 ==========

        // 如果有管线: vkCmdBindPipeline 和 vkCmdDraw

        vkCmdEndRenderPass(cmd);

        if (vkEndCommandBuffer(cmd) != VK_SUCCESS)
            throw std::runtime_error("Failed to record command buffer!");
    }

    void drawFrame() {
        vkWaitForFences(device, 1, &inFlightFences[currentFrame], VK_TRUE, UINT64_MAX);

        uint32_t imageIndex;
        vkAcquireNextImageKHR(device, swapChain, UINT64_MAX, imageAvailableSemaphores[currentFrame], VK_NULL_HANDLE, &imageIndex);

        vkResetFences(device, 1, &inFlightFences[currentFrame]);
        vkResetCommandBuffer(commandBuffers[currentFrame], 0);
        recordCommandBuffer(commandBuffers[currentFrame], imageIndex);

        VkSubmitInfo submitInfo{};
        submitInfo.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
        VkSemaphore waitSems[] = {imageAvailableSemaphores[currentFrame]};
        VkPipelineStageFlags waitStages[] = {VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT};
        submitInfo.waitSemaphoreCount = 1;
        submitInfo.pWaitSemaphores = waitSems;
        submitInfo.pWaitDstStageMask = waitStages;
        submitInfo.commandBufferCount = 1;
        submitInfo.pCommandBuffers = &commandBuffers[currentFrame];
        VkSemaphore signalSems[] = {renderFinishedSemaphores[currentFrame]};
        submitInfo.signalSemaphoreCount = 1;
        submitInfo.pSignalSemaphores = signalSems;

        if (vkQueueSubmit(graphicsQueue, 1, &submitInfo, inFlightFences[currentFrame]) != VK_SUCCESS)
            throw std::runtime_error("Failed to submit draw command buffer!");

        VkPresentInfoKHR presentInfo{};
        presentInfo.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;
        presentInfo.waitSemaphoreCount = 1;
        presentInfo.pWaitSemaphores = signalSems;
        VkSwapchainKHR swapChains[] = {swapChain};
        presentInfo.swapchainCount = 1;
        presentInfo.pSwapchains = swapChains;
        presentInfo.pImageIndices = &imageIndex;

        vkQueuePresentKHR(presentQueue, &presentInfo);
        currentFrame = (currentFrame + 1) % MAX_FRAMES_IN_FLIGHT;
    }

    void mainLoop() {
        std::cout << "\nRunning... (Close window to exit)" << std::endl;
        while (!glfwWindowShouldClose(window)) {
            glfwPollEvents();
            drawFrame();
        }
        vkDeviceWaitIdle(device);
    }

    void cleanup() {
        for (size_t i = 0; i < MAX_FRAMES_IN_FLIGHT; i++) {
            vkDestroySemaphore(device, renderFinishedSemaphores[i], nullptr);
            vkDestroySemaphore(device, imageAvailableSemaphores[i], nullptr);
            vkDestroyFence(device, inFlightFences[i], nullptr);
        }
        vkDestroyCommandPool(device, commandPool, nullptr);

        // TODO: 销毁顶点缓冲和内存
        // 提示: vkDestroyBuffer 和 vkFreeMemory
        // ========== 在下方填写代码 ==========

        /* ??? */
        /* ??? */

        // ========== 填写结束 ==========

        for (auto fb : swapChainFramebuffers) vkDestroyFramebuffer(device, fb, nullptr);
        if (graphicsPipeline) vkDestroyPipeline(device, graphicsPipeline, nullptr);
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
    std::cout << "==============================================" << std::endl;
    std::cout << "  Vulkanlings Exercise 13: Vertex Buffers     " << std::endl;
    std::cout << "==============================================" << std::endl;
    std::cout << std::endl;

    VertexBufferApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "\nExercise 13 completed successfully!" << std::endl;
    return EXIT_SUCCESS;
}
