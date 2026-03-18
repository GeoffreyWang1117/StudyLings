# 练习 19 提示 - Blinn-Phong 光照

## 描述符集布局

```cpp
VkDescriptorSetLayoutBinding lightLayoutBinding{};
lightLayoutBinding.binding = 1;
lightLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER;
lightLayoutBinding.descriptorCount = 1;
lightLayoutBinding.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
```

## 创建光照 UBO 缓冲

```cpp
createBuffer(lightBufferSize, VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT,
            VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
            lightBuffers[i], lightBuffersMemory[i]);
```

## 描述符池

```cpp
poolSizes[1].descriptorCount = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);
```

## 光照描述符信息

```cpp
VkDescriptorBufferInfo lightBufferInfo{};
lightBufferInfo.buffer = lightBuffers[i];
lightBufferInfo.offset = 0;
lightBufferInfo.range = sizeof(LightUBO);
```

## 光照描述符写入

```cpp
descriptorWrites[1].dstBinding = 1;
descriptorWrites[1].pBufferInfo = &lightBufferInfo;
```

## 法线矩阵

```cpp
// 法线矩阵 = transpose(inverse(model))
// 用于正确变换法线向量，即使模型有非均匀缩放
ubo.normalMatrix = glm::transpose(glm::inverse(ubo.model));
```

## 光照参数

```cpp
LightUBO lightUbo{};
lightUbo.lightPos = glm::vec3(2.0f, 2.0f, 2.0f);
lightUbo.viewPos = glm::vec3(2.0f, 2.0f, 2.0f);  // 与摄像机位置相同
lightUbo.lightColor = glm::vec3(1.0f, 1.0f, 1.0f);
lightUbo.ambientStrength = 0.1f;   // 环境光强度
lightUbo.specularStrength = 0.5f;  // 高光强度
lightUbo.shininess = 32.0f;        // 高光指数
```

## 顶点着色器 - 法线变换

```glsl
fragNormal = mat3(ubo.normalMatrix) * inNormal;
```

## 片段着色器 - Blinn-Phong

```glsl
// 半程向量 (Blinn-Phong 的关键)
vec3 halfwayDir = normalize(lightDir + viewDir);

// 高光强度
float spec = pow(max(dot(norm, halfwayDir), 0.0), light.shininess);
```

## Blinn-Phong vs Phong

Blinn-Phong 使用半程向量而不是反射向量:
- **Phong**: `reflect(-lightDir, norm)` 然后 `dot(viewDir, reflectDir)`
- **Blinn-Phong**: `normalize(lightDir + viewDir)` 然后 `dot(norm, halfwayDir)`

Blinn-Phong 更高效且在某些角度下看起来更自然。

## 需要填写的答案

1. 顶点着色器法线: `mat3(ubo.normalMatrix) * inNormal`
2. 描述符布局: `binding=1, descriptorType=VK_DESCRIPTOR_TYPE_UNIFORM_BUFFER, stageFlags=VK_SHADER_STAGE_FRAGMENT_BIT`
3. 光照缓冲: `VK_BUFFER_USAGE_UNIFORM_BUFFER_BIT`
4. 描述符池: `MAX_FRAMES_IN_FLIGHT`
5. 光照信息: `lightBuffers[i], LightUBO`
6. 描述符写入: `dstBinding=1, pBufferInfo=&lightBufferInfo`
7. 法线矩阵: `ubo.model`
8. 光照参数: `viewPos=glm::vec3(2.0f, 2.0f, 2.0f), ambientStrength=0.1f, specularStrength=0.5f, shininess=32.0f`
9. 半程向量: `lightDir + viewDir`
10. 高光指数: `light.shininess`
