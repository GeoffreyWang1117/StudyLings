# 练习 19: Blinn-Phong 光照

## 学习目标
- 实现环境光、漫反射、镜面反射
- 使用 Blinn-Phong 模型计算高光
- 传递光源和相机位置到着色器

## 关键概念

### Blinn-Phong 模型

```glsl
// 环境光
vec3 ambient = ambientStrength * lightColor;

// 漫反射
vec3 lightDir = normalize(lightPos - fragPos);
float diff = max(dot(normal, lightDir), 0.0);
vec3 diffuse = diff * lightColor;

// Blinn-Phong 镜面反射
vec3 viewDir = normalize(viewPos - fragPos);
vec3 halfwayDir = normalize(lightDir + viewDir);
float spec = pow(max(dot(normal, halfwayDir), 0.0), shininess);
vec3 specular = specularStrength * spec * lightColor;

// 最终颜色
vec3 result = (ambient + diffuse + specular) * objectColor;
```

### Uniform 数据
```cpp
struct UniformBufferObject {
    glm::mat4 model;
    glm::mat4 view;
    glm::mat4 proj;
    glm::vec3 lightPos;
    glm::vec3 viewPos;
};
```

### 法线变换
```glsl
// 正确变换法线
mat3 normalMatrix = mat3(transpose(inverse(model)));
vec3 worldNormal = normalMatrix * inNormal;
```

## 任务
在 main.cpp 中完成 TODO 标记的代码，实现完整的 Blinn-Phong 光照。
