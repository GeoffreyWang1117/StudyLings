# 练习 15: Uniform 缓冲对象

## 学习目标
- 创建描述符集布局
- 创建 Uniform 缓冲
- 更新着色器中的 uniform 数据

## 关键概念

### Uniform 数据结构
```cpp
struct UniformBufferObject {
    glm::mat4 model;
    glm::mat4 view;
    glm::mat4 proj;
};
```

### 描述符集
1. VkDescriptorSetLayout: 定义布局
2. VkDescriptorPool: 分配描述符集
3. VkDescriptorSet: 实际的描述符

### 着色器声明
```glsl
layout(binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
} ubo;
```

## 任务
在 main.cpp 中完成 TODO 标记的代码。
