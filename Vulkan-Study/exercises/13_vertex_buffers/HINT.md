# 练习 13 提示 - 顶点缓冲

## 顶点绑定描述

```cpp
VkVertexInputBindingDescription bindingDescription{};
bindingDescription.binding = 0;
bindingDescription.stride = sizeof(Vertex);
bindingDescription.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;
```

## 顶点属性描述

```cpp
// 位置 (vec2)
attributeDescriptions[0].location = 0;
attributeDescriptions[0].format = VK_FORMAT_R32G32_SFLOAT;

// 颜色 (vec3)
attributeDescriptions[1].location = 1;
attributeDescriptions[1].format = VK_FORMAT_R32G32B32_SFLOAT;
```

## 创建缓冲

```cpp
VkBufferCreateInfo bufferInfo{};
bufferInfo.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
bufferInfo.size = bufferSize;
bufferInfo.usage = VK_BUFFER_USAGE_VERTEX_BUFFER_BIT;
```

## 分配内存

```cpp
VkMemoryAllocateInfo allocInfo{};
allocInfo.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
allocInfo.allocationSize = memRequirements.size;
```

## 绑定和复制

```cpp
vkBindBufferMemory(device, vertexBuffer, vertexBufferMemory, 0);

void* data;
vkMapMemory(device, vertexBufferMemory, 0, bufferSize, 0, &data);
memcpy(data, vertices.data(), (size_t)bufferSize);
vkUnmapMemory(device, vertexBufferMemory);
```

## 绑定顶点缓冲

```cpp
VkBuffer vertexBuffers[] = {vertexBuffer};
VkDeviceSize offsets[] = {0};
vkCmdBindVertexBuffers(commandBuffer, 0, 1, vertexBuffers, offsets);
```

## 销毁

```cpp
vkDestroyBuffer(device, vertexBuffer, nullptr);
vkFreeMemory(device, vertexBufferMemory, nullptr);
```

## 需要填写的答案

1. binding = `0`
2. stride = `sizeof(Vertex)`
3. inputRate = `VK_VERTEX_INPUT_RATE_VERTEX`
4. location[0] = `0`, format = `VK_FORMAT_R32G32_SFLOAT`
5. location[1] = `1`, format = `VK_FORMAT_R32G32B32_SFLOAT`
6. bufferInfo.sType = `VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO`
7. bufferInfo.size = `bufferSize`
8. bufferInfo.usage = `VK_BUFFER_USAGE_VERTEX_BUFFER_BIT`
9. allocInfo.sType = `VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO`
10. allocInfo.allocationSize = `memRequirements.size`
11. 绑定: `vkBindBufferMemory(device, vertexBuffer, vertexBufferMemory, 0);`
12. 复制: `memcpy(data, vertices.data(), (size_t)bufferSize);`
13. 命令: `vkCmdBindVertexBuffers(cmd, 0, 1, vertexBuffers, offsets);`
14. 销毁: `vkDestroyBuffer(device, vertexBuffer, nullptr);` 和 `vkFreeMemory(device, vertexBufferMemory, nullptr);`
