/**
 * 练习 14: 索引缓冲
 *
 * 学习目标:
 * - 创建索引缓冲减少顶点重复
 * - 使用 vkCmdDrawIndexed 进行索引绘制
 * - 理解索引绘制的性能优势
 *
 * 索引绘制允许我们复用顶点，减少内存使用和带宽消耗。
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>

#include <iostream>
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

struct Vertex {
    glm::vec2 pos;
    glm::vec3 color;

    static VkVertexInputBindingDescription getBindingDescription() {
        VkVertexInputBindingDescription desc{};
        desc.binding = 0;
        desc.stride = sizeof(Vertex);
        desc.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
        return desc;
    }

    static std::array<VkVertexInputAttributeDescription, 2> getAttributeDescriptions() {
        std::array<VkVertexInputAttributeDescription, 2> attrs{};
        attrs[0] = {0, 0, VK_FORMAT_R32G32_SFLOAT, offsetof(Vertex, pos)};
        attrs[1] = {1, 0, VK_FORMAT_R32G32B32_SFLOAT, offsetof(Vertex, color)};
        return attrs;
    }
};

// 正方形的 4 个顶点（而不是 6 个）
const std::vector<Vertex> vertices = {
    {{-0.5f, -0.5f}, {1.0f, 0.0f, 0.0f}},  // 左上 - 红
    {{ 0.5f, -0.5f}, {0.0f, 1.0f, 0.0f}},  // 右上 - 绿
    {{ 0.5f,  0.5f}, {0.0f, 0.0f, 1.0f}},  // 右下 - 蓝
    {{-0.5f,  0.5f}, {1.0f, 1.0f, 1.0f}}   // 左下 - 白
};

// TODO: 定义索引数据
// 提示: 两个三角形组成正方形
//       第一个三角形: 0, 1, 2
//       第二个三角形: 2, 3, 0
// ========== 在下方填写代码 ==========

const std::vector<uint16_t> indices = {
    /* ??? */
};

// ========== 填写结束 ==========

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

class IndexBufferApp {
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
    std::vector<VkFramebuffer> swapChainFramebuffers;
    VkCommandPool commandPool = VK_NULL_HANDLE;
    std::vector<VkCommandBuffer> commandBuffers;
    std::vector<VkSemaphore> imageAvailableSemaphores;
    std::vector<VkSemaphore> renderFinishedSemaphores;
    std::vector<VkFence> inFlightFences;
    uint32_t currentFrame = 0;

    VkBuffer vertexBuffer = VK_NULL_HANDLE;
    VkDeviceMemory vertexBufferMemory = VK_NULL_HANDLE;
    VkBuffer indexBuffer = VK_NULL_HANDLE;           // 索引缓冲
    VkDeviceMemory indexBufferMemory = VK_NULL_HANDLE;

    void initWindow() {
        glfwInit();
        glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);
        window = glfwCreateWindow(WIDTH, HEIGHT, "Vulkanlings - Exercise 14: Index Buffers", nullptr, nullptr);
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
        createCommandPool();
        createVertexBuffer();
        createIndexBuffer();
        createCommandBuffers();
        createSyncObjects();
    }

    // 基础设置函数（简化）
    void createInstance() {
        VkApplicationInfo appInfo{};
        appInfo.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
        appInfo.pApplicationName = "Index Buffer Exercise";
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

    void pickPhysicalDevice() {
        uint32_t count = 0;
        vkEnumeratePhysicalDevices(instance, &count, nullptr);
        std::vector<VkPhysicalDevice> devs(count);
        vkEnumeratePhysicalDevices(instance, &count, devs.data());
        for (const auto& d : devs) {
            auto indices = findQueueFamilies(d);
            bool extOk = checkDeviceExtSupport(d);
            auto sc = querySwapChainSupport(d);
            if (indices.isComplete() && extOk && !sc.formats.empty() && !sc.presentModes.empty()) {
                physicalDevice = d;
                break;
            }
        }
        if (physicalDevice == VK_NULL_HANDLE) throw std::runtime_error("Failed to find suitable GPU!");
    }

    void createLogicalDevice() {
        auto indices = findQueueFamilies(physicalDevice);
        std::set<uint32_t> uniqueFamilies = {indices.graphicsFamily.value(), indices.presentFamily.value()};
        std::vector<VkDeviceQueueCreateInfo> queueInfos;
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
        VkExtent2D extent = support.capabilities.currentExtent;
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
        info.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
        info.preTransform = support.capabilities.currentTransform;
        info.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
        info.presentMode = VK_PRESENT_MODE_FIFO_KHR;
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
            vkCreateImageView(device, &info, nullptr, &swapChainImageViews[i]);
        }
    }

    void createRenderPass() {
        VkAttachmentDescription colorAttachment{};
        colorAttachment.format = swapChainImageFormat;
        colorAttachment.samples = VK_SAMPLE_COUNT_1_BIT;
        colorAttachment.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
        colorAttachment.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
        colorAttachment.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
        colorAttachment.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;
        VkAttachmentReference colorRef{0, VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL};
        VkSubpassDescription subpass{};
        subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
        subpass.colorAttachmentCount = 1;
        subpass.pColorAttachments = &colorRef;
        VkRenderPassCreateInfo info{};
        info.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
        info.attachmentCount = 1;
        info.pAttachments = &colorAttachment;
        info.subpassCount = 1;
        info.pSubpasses = &subpass;
        vkCreateRenderPass(device, &info, nullptr, &renderPass);
    }

    void createPipelineLayout() {
        VkPipelineLayoutCreateInfo info{};
        info.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
        vkCreatePipelineLayout(device, &info, nullptr, &pipelineLayout);
        std::cout << "Pipeline layout created." << std::endl;
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
            vkCreateFramebuffer(device, &info, nullptr, &swapChainFramebuffers[i]);
        }
    }

    void createCommandPool() {
        auto indices = findQueueFamilies(physicalDevice);
        VkCommandPoolCreateInfo info{};
        info.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
        info.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
        info.queueFamilyIndex = indices.graphicsFamily.value();
        vkCreateCommandPool(device, &info, nullptr, &commandPool);
    }

    uint32_t findMemoryType(uint32_t typeFilter, VkMemoryPropertyFlags properties) {
        VkPhysicalDeviceMemoryProperties memProps;
        vkGetPhysicalDeviceMemoryProperties(physicalDevice, &memProps);
        for (uint32_t i = 0; i < memProps.memoryTypeCount; i++) {
            if ((typeFilter & (1 << i)) && (memProps.memoryTypes[i].propertyFlags & properties) == properties)
                return i;
        }
        throw std::runtime_error("Failed to find suitable memory type!");
    }

    void createBuffer(VkDeviceSize size, VkBufferUsageFlags usage, VkMemoryPropertyFlags properties,
                      VkBuffer& buffer, VkDeviceMemory& bufferMemory) {
        VkBufferCreateInfo bufferInfo{};
        bufferInfo.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
        bufferInfo.size = size;
        bufferInfo.usage = usage;
        bufferInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
        vkCreateBuffer(device, &bufferInfo, nullptr, &buffer);

        VkMemoryRequirements memReqs;
        vkGetBufferMemoryRequirements(device, buffer, &memReqs);

        VkMemoryAllocateInfo allocInfo{};
        allocInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
        allocInfo.allocationSize = memReqs.size;
        allocInfo.memoryTypeIndex = findMemoryType(memReqs.memoryTypeBits, properties);
        vkAllocateMemory(device, &allocInfo, nullptr, &bufferMemory);
        vkBindBufferMemory(device, buffer, bufferMemory, 0);
    }

    void createVertexBuffer() {
        VkDeviceSize bufferSize = sizeof(vertices[0]) * vertices.size();
        createBuffer(bufferSize, VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
                     VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                     vertexBuffer, vertexBufferMemory);

        void* data;
        vkMapMemory(device, vertexBufferMemory, 0, bufferSize, 0, &data);
        memcpy(data, vertices.data(), (size_t)bufferSize);
        vkUnmapMemory(device, vertexBufferMemory);

        std::cout << "Vertex buffer created with " << vertices.size() << " vertices." << std::endl;
    }

    void createIndexBuffer() {
        VkDeviceSize bufferSize = sizeof(indices[0]) * indices.size();

        // TODO: 创建索引缓冲
        // 提示: 使用 VK_BUFFER_USAGE_INDEX_BUFFER_BIT
        // ========== 在下方填写代码 ==========

        createBuffer(bufferSize, /* ??? */,
                     VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
                     indexBuffer, indexBufferMemory);

        // ========== 填写结束 ==========

        void* data;
        vkMapMemory(device, indexBufferMemory, 0, bufferSize, 0, &data);
        memcpy(data, indices.data(), (size_t)bufferSize);
        vkUnmapMemory(device, indexBufferMemory);

        std::cout << "Index buffer created with " << indices.size() << " indices." << std::endl;
        std::cout << "Drawing a square with 4 vertices and 6 indices." << std::endl;
    }

    void createCommandBuffers() {
        commandBuffers.resize(MAX_FRAMES_IN_FLIGHT);
        VkCommandBufferAllocateInfo info{};
        info.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
        info.commandPool = commandPool;
        info.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
        info.commandBufferCount = static_cast<uint32_t>(commandBuffers.size());
        vkAllocateCommandBuffers(device, &info, commandBuffers.data());
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
            vkCreateSemaphore(device, &semInfo, nullptr, &imageAvailableSemaphores[i]);
            vkCreateSemaphore(device, &semInfo, nullptr, &renderFinishedSemaphores[i]);
            vkCreateFence(device, &fenceInfo, nullptr, &inFlightFences[i]);
        }
    }

    void recordCommandBuffer(VkCommandBuffer cmd, uint32_t imageIndex) {
        VkCommandBufferBeginInfo beginInfo{};
        beginInfo.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
        vkBeginCommandBuffer(cmd, &beginInfo);

        VkRenderPassBeginInfo renderPassInfo{};
        renderPassInfo.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
        renderPassInfo.renderPass = renderPass;
        renderPassInfo.framebuffer = swapChainFramebuffers[imageIndex];
        renderPassInfo.renderArea = {{0, 0}, swapChainExtent};
        VkClearValue clearColor = {{{0.05f, 0.05f, 0.1f, 1.0f}}};
        renderPassInfo.clearValueCount = 1;
        renderPassInfo.pClearValues = &clearColor;

        vkCmdBeginRenderPass(cmd, &renderPassInfo, VK_SUBPASS_CONTENTS_INLINE);

        // 绑定顶点缓冲
        VkBuffer vertexBuffers[] = {vertexBuffer};
        VkDeviceSize offsets[] = {0};
        vkCmdBindVertexBuffers(cmd, 0, 1, vertexBuffers, offsets);

        // TODO: 绑定索引缓冲
        // 提示: vkCmdBindIndexBuffer(cmd, indexBuffer, 0, VK_INDEX_TYPE_UINT16)
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        // TODO: 使用索引绘制
        // 提示: vkCmdDrawIndexed(cmd, indexCount, instanceCount, firstIndex, vertexOffset, firstInstance)
        //       indexCount = indices.size()
        // ========== 在下方填写代码 ==========

        // vkCmdDrawIndexed(cmd, /* ??? */, 1, 0, 0, 0);

        // ========== 填写结束 ==========

        vkCmdEndRenderPass(cmd);
        vkEndCommandBuffer(cmd);
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
        vkQueueSubmit(graphicsQueue, 1, &submitInfo, inFlightFences[currentFrame]);

        VkPresentInfoKHR presentInfo{};
        presentInfo.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;
        presentInfo.waitSemaphoreCount = 1;
        presentInfo.pWaitSemaphores = signalSems;
        presentInfo.swapchainCount = 1;
        presentInfo.pSwapchains = &swapChain;
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

        // TODO: 销毁索引缓冲
        // ========== 在下方填写代码 ==========

        /* ??? */
        /* ??? */

        // ========== 填写结束 ==========

        vkDestroyBuffer(device, vertexBuffer, nullptr);
        vkFreeMemory(device, vertexBufferMemory, nullptr);

        for (auto fb : swapChainFramebuffers) vkDestroyFramebuffer(device, fb, nullptr);
        vkDestroyPipelineLayout(device, pipelineLayout, nullptr);
        vkDestroyRenderPass(device, renderPass, nullptr);
        for (auto iv : swapChainImageViews) vkDestroyImageView(device, iv, nullptr);
        vkDestroySwapchainKHR(device, swapChain, nullptr);
        vkDestroyDevice(device, nullptr);
        vkDestroySurfaceKHR(instance, surface, nullptr);
        vkDestroyInstance(instance, nullptr);
        glfwDestroyWindow(window);
        glfwTerminate();
    }
};

int main() {
    std::cout << "=============================================" << std::endl;
    std::cout << "  Vulkanlings Exercise 14: Index Buffers     " << std::endl;
    std::cout << "=============================================" << std::endl;
    std::cout << std::endl;

    IndexBufferApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
