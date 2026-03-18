# 练习 18: 模型加载

## 学习目标
- 加载 OBJ 模型文件
- 处理顶点、法线、纹理坐标
- 构建顶点和索引缓冲

## 关键概念

### OBJ 文件格式
```
v x y z          # 顶点位置
vt u v           # 纹理坐标
vn x y z         # 法线
f v/vt/vn ...    # 面定义
```

### 推荐库
- tinyobjloader: 轻量级 OBJ 加载器
- assimp: 支持多种格式的通用加载器

### 顶点去重
使用 unordered_map 或 set 去除重复顶点，
减少顶点缓冲大小。

### 示例代码
```cpp
tinyobj::attrib_t attrib;
std::vector<tinyobj::shape_t> shapes;

tinyobj::LoadObj(&attrib, &shapes, nullptr, nullptr, MODEL_PATH.c_str());

for (const auto& shape : shapes) {
    for (const auto& index : shape.mesh.indices) {
        Vertex vertex{};
        vertex.pos = {...};
        vertex.texCoord = {...};
        vertex.normal = {...};
        // ...
    }
}
```

## 任务
在 main.cpp 中完成 TODO 标记的代码。
