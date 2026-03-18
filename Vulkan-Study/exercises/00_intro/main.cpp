/**
 * 练习 00: Vulkan 概述与环境配置
 *
 * 学习目标:
 * - 理解 Vulkan 的基本架构
 * - 验证开发环境配置正确
 * - 学习 GLFW 窗口创建
 *
 * 任务:
 * 1. 填写 GLFW 初始化代码
 * 2. 创建一个窗口
 * 3. 运行主循环直到窗口关闭
 */

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <iostream>
#include <stdexcept>
#include <cstdlib>

const uint32_t WIDTH = 800;
const uint32_t HEIGHT = 600;

class HelloVulkanApp {
public:
    void run() {
        initWindow();
        mainLoop();
        cleanup();
    }

private:
    GLFWwindow* window = nullptr;

    void initWindow() {
        // TODO: 初始化 GLFW 库
        // 提示: 使用 glfwInit() 函数
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        // TODO: 设置 GLFW 不创建 OpenGL 上下文
        // 提示: 使用 glfwWindowHint(GLFW_CLIENT_API, ???)
        // ========== 在下方填写代码 ==========

        glfwWindowHint(GLFW_CLIENT_API, /* ??? */);

        // ========== 填写结束 ==========

        // 禁止窗口调整大小（简化练习）
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);

        // TODO: 创建窗口
        // 提示: 使用 glfwCreateWindow(宽度, 高度, 标题, nullptr, nullptr)
        // ========== 在下方填写代码 ==========

        window = glfwCreateWindow(/* ??? */, /* ??? */, "Vulkan Study - Exercise 00", nullptr, nullptr);

        // ========== 填写结束 ==========

        if (window == nullptr) {
            throw std::runtime_error("Failed to create GLFW window!");
        }

        std::cout << "Window created successfully!" << std::endl;

        // 打印 Vulkan 支持信息
        if (glfwVulkanSupported()) {
            std::cout << "Vulkan is supported!" << std::endl;

            uint32_t extensionCount = 0;
            const char** extensions = glfwGetRequiredInstanceExtensions(&extensionCount);
            std::cout << "Required Vulkan extensions for GLFW:" << std::endl;
            for (uint32_t i = 0; i < extensionCount; i++) {
                std::cout << "  - " << extensions[i] << std::endl;
            }
        } else {
            std::cout << "Vulkan is NOT supported!" << std::endl;
        }
    }

    void mainLoop() {
        std::cout << "\nRunning main loop... (Close window to exit)" << std::endl;

        // TODO: 运行主循环直到窗口应该关闭
        // 提示: 使用 glfwWindowShouldClose() 检查窗口状态
        //       使用 glfwPollEvents() 处理事件
        // ========== 在下方填写代码 ==========

        while (!glfwWindowShouldClose(/* ??? */)) {
            /* ??? */  // 处理事件
        }

        // ========== 填写结束 ==========

        std::cout << "Main loop ended." << std::endl;
    }

    void cleanup() {
        // TODO: 销毁窗口
        // 提示: 使用 glfwDestroyWindow()
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        // TODO: 终止 GLFW
        // 提示: 使用 glfwTerminate()
        // ========== 在下方填写代码 ==========

        /* ??? */

        // ========== 填写结束 ==========

        std::cout << "Cleanup complete!" << std::endl;
    }
};

int main() {
    std::cout << "======================================" << std::endl;
    std::cout << "  Vulkanlings Exercise 00: Intro     " << std::endl;
    std::cout << "======================================" << std::endl;
    std::cout << std::endl;

    HelloVulkanApp app;

    try {
        app.run();
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "\nExercise 00 completed successfully!" << std::endl;
    return EXIT_SUCCESS;
}
