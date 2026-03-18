# 练习 00 提示

## GLFW 初始化

GLFW 是一个用于创建窗口和处理输入的跨平台库。在使用任何 GLFW 函数之前，必须先初始化它：

```cpp
glfwInit();
```

## 禁用 OpenGL 上下文

因为我们使用 Vulkan 而不是 OpenGL，需要告诉 GLFW 不要创建 OpenGL 上下文：

```cpp
glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
```

## 创建窗口

使用 `glfwCreateWindow` 创建窗口：

```cpp
GLFWwindow* window = glfwCreateWindow(WIDTH, HEIGHT, "Title", nullptr, nullptr);
```

## 主循环

窗口应用程序需要一个主循环来保持窗口打开并处理事件：

```cpp
while (!glfwWindowShouldClose(window)) {
    glfwPollEvents();
}
```

## 清理

程序结束时需要清理资源：

```cpp
glfwDestroyWindow(window);
glfwTerminate();
```

## 完整答案

如果你仍然卡住了，这里是需要填写的代码：

1. 初始化 GLFW: `glfwInit();`
2. 设置 Client API: `GLFW_NO_API`
3. 创建窗口: `WIDTH, HEIGHT`
4. 主循环检查: `window`
5. 处理事件: `glfwPollEvents();`
6. 销毁窗口: `glfwDestroyWindow(window);`
7. 终止 GLFW: `glfwTerminate();`
