# 练习 15 提示 - Uniform 缓冲对象

## 描述符集布局绑定

```cpp
VkDescriptorSetLayoutBinding uboLayoutBinding{};
uboLayoutBinding.binding = 0;
uboLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
uboLayoutBinding.descriptorCount = 1;
uboLayoutBinding.stageFlags = VK_SHADER_STAGE_VERTEX_BIT;
```

## 管线布局

```cpp
VkPipelineLayoutCreateInfo pipelineLayoutInfo{};
pipelineLayoutInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
pipelineLayoutInfo.setLayoutCount = 1;
pipelineLayoutInfo.pSetLayouts = &descriptorSetLayout;
```

## 创建 Uniform 缓冲

```cpp
createBuffer(bufferSize, VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
            uniformBuffers[i], uniformBuffersMemory[i]);
```

## 描述符池

```cpp
VkDescriptorPoolSize poolSize{};
poolSize.type = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
poolSize.descriptorCount = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);
```

## 描述符写入

```cpp
VkWriteDescriptorSet descriptorWrite{};
descriptorWrite.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
descriptorWrite.dstSet = descriptorSets[i];
descriptorWrite.dstBinding = 0;
descriptorWrite.dstArrayElement = 0;
descriptorWrite.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
descriptorWrite.descriptorCount = 1;
descriptorWrite.pBufferInfo = &bufferInfo;
```

## 变换矩阵

```cpp
// 模型矩阵 - 绕 Z 轴旋转
ubo.model = glm::rotate(glm::mat4(1.0f), time * glm::radians(90.0f), glm::vec3(0.0f, 0.0f, 1.0f));

// 视图矩阵
ubo.view = glm::lookAt(glm::vec3(2.0f, 2.0f, 2.0f), glm::vec3(0.0f, 0.0f, 0.0f), glm::vec3(0.0f, 0.0f, 1.0f));

// 投影矩阵
ubo.proj = glm::perspective(glm::radians(45.0f), aspectRatio, 0.1f, 10.0f);
ubo.proj[1][1] *= -1;  // Y 轴翻转
```

## 绑定描述符集

```cpp
vkCmdBindDescriptorSets(commandBuffer, VK_PIPELINE_BIND_POINT_GRAPHICS, pipelineLayout,
                       0, 1, &descriptorSets[currentFrame], 0, nullptr);
```

## 清理

```cpp
vkDestroyDescriptorPool(device, descriptorPool, nullptr);
vkDestroyDescriptorSetLayout(device, descriptorSetLayout, nullptr);
```

## 需要填写的答案

1. 描述符布局绑定: `binding=0, descriptorType=VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER, descriptorCount=1, stageFlags=VK_SHADER_STAGE_VERTEX_BIT`
2. 管线布局: `setLayoutCount=1, pSetLayouts=&descriptorSetLayout`
3. Uniform 缓冲: `usage=VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT, properties=VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT`
4. 描述符池: `type=VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER, descriptorCount=MAX_FRAMES_IN_FLIGHT`
5. 描述符写入: `dstSet=descriptorSets[i], dstBinding=0, descriptorType=VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER, descriptorCount=1, pBufferInfo=&bufferInfo`
6. 旋转矩阵: `time * glm::radians(90.0f)`
7. 绑定描述符集: `VK_PIPELINE_BIND_POINT_GRAPHICS`
8. 清理: `descriptorPool, descriptorSetLayout`
