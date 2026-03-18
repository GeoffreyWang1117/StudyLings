# 练习 08 提示

## 图形管线概述

Vulkan 图形管线由以下阶段组成：

```
输入装配 → 顶点着色器 → 曲面细分 → 几何着色器 → 光栅化 → 片段着色器 → 颜色混合
```

## 着色器模块

```cpp
VkShaderModuleCreateInfo createInfo{};
createInfo.sType = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;
createInfo.codeSize = code.size();
createInfo.pCode = reinterpret_cast<const uint32_t*>(code.data());

vkCreateShaderModule(device, &createInfo, nullptr, &shaderModule);
```

## 顶点输入状态

```cpp
VkPipelineVertexInputStateCreateInfo vertexInputInfo{};
vertexInputInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO;
vertexInputInfo.vertexBindingDescriptionCount = 0;
vertexInputInfo.vertexAttributeDescriptionCount = 0;
```

## 输入装配状态

```cpp
VkPipelineInputAssemblyStateCreateInfo inputAssembly{};
inputAssembly.sType = VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO;
inputAssembly.topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;
inputAssembly.primitiveRestartEnable = VK_FALSE;
```

### 图元拓扑
- `VK_PRIMITIVE_TOPOLOGY_POINT_LIST`: 点
- `VK_PRIMITIVE_TOPOLOGY_LINE_LIST`: 线段
- `VK_PRIMITIVE_TOPOLOGY_LINE_STRIP`: 线带
- `VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST`: 三角形列表
- `VK_PRIMITIVE_TOPOLOGY_TRIANGLE_STRIP`: 三角形带

## 光栅化状态

```cpp
VkPipelineRasterizationStateCreateInfo rasterizer{};
rasterizer.sType = VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO;
rasterizer.polygonMode = VK_POLYGON_MODE_FILL;
rasterizer.cullMode = VK_CULL_MODE_BACK_BIT;
rasterizer.frontFace = VK_FRONT_FACE_CLOCKWISE;
```

### 多边形模式
- `VK_POLYGON_MODE_FILL`: 填充
- `VK_POLYGON_MODE_LINE`: 线框
- `VK_POLYGON_MODE_POINT`: 点

### 剔除模式
- `VK_CULL_MODE_NONE`: 不剔除
- `VK_CULL_MODE_FRONT_BIT`: 剔除正面
- `VK_CULL_MODE_BACK_BIT`: 剔除背面

## 管线布局

```cpp
VkPipelineLayoutCreateInfo pipelineLayoutInfo{};
pipelineLayoutInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;

vkCreatePipelineLayout(device, &pipelineLayoutInfo, nullptr, &pipelineLayout);
```

## 需要填写的答案

1. 着色器模块类型: `VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO`
2. 顶点输入类型: `VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO`
3. 输入装配类型: `VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO`
4. 图元拓扑: `VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST`
5. 光栅化类型: `VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO`
6. 多边形模式: `VK_POLYGON_MODE_FILL`
7. 剔除模式: `VK_CULL_MODE_BACK_BIT`
8. 正面方向: `VK_FRONT_FACE_CLOCKWISE`
9. 管线布局类型: `VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO`
10. 创建管线布局: `vkCreatePipelineLayout(device, &pipelineLayoutInfo, nullptr, &pipelineLayout)`
11. 销毁管线布局: `vkDestroyPipelineLayout(device, pipelineLayout, nullptr);`
