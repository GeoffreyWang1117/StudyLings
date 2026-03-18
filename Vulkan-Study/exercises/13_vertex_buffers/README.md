# 练习 13: 顶点缓冲

## 学习目标
- 创建顶点缓冲
- 使用暂存缓冲传输数据
- 定义顶点属性

## 关键概念

### 顶点数据结构
```cpp
struct Vertex {
    glm::vec2 pos;
    glm::vec3 color;
};
```

### 创建顶点缓冲
1. 创建暂存缓冲（CPU 可访问）
2. 将顶点数据复制到暂存缓冲
3. 创建设备本地缓冲（GPU 最优）
4. 从暂存缓冲复制到设备缓冲

### 顶点输入描述
- VkVertexInputBindingDescription: 绑定描述
- VkVertexInputAttributeDescription: 属性描述

## 任务
在 main.cpp 中完成 TODO 标记的代码。
