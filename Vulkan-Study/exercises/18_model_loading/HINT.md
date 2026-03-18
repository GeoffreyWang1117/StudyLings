# 练习 18 提示 - 模型加载

## 顶点哈希函数

```cpp
namespace std {
    template<> struct hash<Vertex> {
        size_t operator()(Vertex const& vertex) const {
            return ((hash<glm::vec3>()(vertex.pos) ^
                   (hash<glm::vec3>()(vertex.color) << 1)) >> 1) ^
                   (hash<glm::vec2>()(vertex.texCoord) << 1);
        }
    };
}
```

## 加载 OBJ 模型

```cpp
if (!tinyobj::LoadObj(&attrib, &shapes, &materials, &warn, &err, MODEL_PATH.c_str())) {
    throw std::runtime_error(warn + err);
}
```

## tinyobjloader 数据结构

```cpp
// attrib.vertices: 顶点位置 [x0, y0, z0, x1, y1, z1, ...]
// attrib.normals: 法线 [nx0, ny0, nz0, nx1, ny1, nz1, ...]
// attrib.texcoords: 纹理坐标 [u0, v0, u1, v1, ...]

// shapes[i].mesh.indices: 面的索引数据
// index.vertex_index: 顶点索引
// index.normal_index: 法线索引
// index.texcoord_index: 纹理坐标索引
```

## 提取顶点位置

```cpp
vertex.pos = {
    attrib.vertices[3 * index.vertex_index + 0],
    attrib.vertices[3 * index.vertex_index + 1],
    attrib.vertices[3 * index.vertex_index + 2]
};
```

## 提取纹理坐标

```cpp
vertex.texCoord = {
    attrib.texcoords[2 * index.texcoord_index + 0],
    1.0f - attrib.texcoords[2 * index.texcoord_index + 1]  // V 翻转
};
```

OBJ 格式的纹理坐标原点在左下角，Vulkan 在左上角，所以需要翻转 V 坐标。

## 顶点去重

```cpp
if (uniqueVertices.count(vertex) == 0) {
    uniqueVertices[vertex] = static_cast<uint32_t>(vertices.size());
    vertices.push_back(vertex);
}

indices.push_back(uniqueVertices[vertex]);
```

## 32 位索引

```cpp
// 模型可能有超过 65535 个顶点，使用 32 位索引
std::vector<uint32_t> indices;

vkCmdBindIndexBuffer(commandBuffer, indexBuffer, 0, VK_INDEX_TYPE_UINT32);
```

## 需要填写的答案

1. 哈希函数: `vertex.texCoord`
2. 加载模型: `&attrib, &shapes, &materials, &warn, &err, MODEL_PATH.c_str()`
3. 位置 Z: `3 * index.vertex_index + 2`
4. 纹理 V: `2 * index.texcoord_index + 1`
5. 添加顶点: `vertex`
6. 获取索引: `vertex`
7. 索引类型: `VK_INDEX_TYPE_UINT32`

## 常用 OBJ 模型获取

你可以从以下网站获取免费的 OBJ 模型进行测试:
- https://sketchfab.com (选择可下载的免费模型)
- Vulkan Tutorial 使用的 viking_room.obj

## 加载法线 (可选)

```cpp
if (index.normal_index >= 0) {
    vertex.normal = {
        attrib.normals[3 * index.normal_index + 0],
        attrib.normals[3 * index.normal_index + 1],
        attrib.normals[3 * index.normal_index + 2]
    };
}
```
