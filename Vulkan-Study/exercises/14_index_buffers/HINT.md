# 练习 14 提示 - 索引缓冲

## 索引数据

正方形由两个三角形组成：

```cpp
const std::vector<uint16_t> indices = {
    0, 1, 2,  // 第一个三角形
    2, 3, 0   // 第二个三角形
};
```

## 创建索引缓冲

```cpp
createBuffer(bufferSize, VK_BUFFER_USAGE_INDEX_BUFFER_BIT,
             VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
             indexBuffer, indexBufferMemory);
```

## 绑定索引缓冲

```cpp
vkCmdBindIndexBuffer(commandBuffer, indexBuffer, 0, VK_INDEX_TYPE_UINT16);
```

索引类型：
- `VK_INDEX_TYPE_UINT16`: 16位索引，最多 65535 个顶点
- `VK_INDEX_TYPE_UINT32`: 32位索引，更多顶点

## 索引绘制

```cpp
vkCmdDrawIndexed(commandBuffer, static_cast<uint32_t>(indices.size()), 1, 0, 0, 0);
```

参数：
- indexCount: 索引数量
- instanceCount: 实例数量
- firstIndex: 起始索引
- vertexOffset: 顶点偏移
- firstInstance: 起始实例

## 销毁

```cpp
vkDestroyBuffer(device, indexBuffer, nullptr);
vkFreeMemory(device, indexBufferMemory, nullptr);
```

## 需要填写的答案

1. 索引数据: `0, 1, 2, 2, 3, 0`
2. 缓冲用途: `VK_BUFFER_USAGE_INDEX_BUFFER_BIT`
3. 绑定索引: `vkCmdBindIndexBuffer(cmd, indexBuffer, 0, VK_INDEX_TYPE_UINT16);`
4. 索引绘制: `vkCmdDrawIndexed(cmd, static_cast<uint32_t>(indices.size()), 1, 0, 0, 0);`
5. 销毁: `vkDestroyBuffer(device, indexBuffer, nullptr);` 和 `vkFreeMemory(device, indexBufferMemory, nullptr);`
