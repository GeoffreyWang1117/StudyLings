#version 450

// Uniform Buffer Object - 变换矩阵
layout(binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
    mat4 normalMatrix;  // 法线变换矩阵 = transpose(inverse(model))
} ubo;

// 顶点输入
layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec3 inNormal;
layout(location = 2) in vec3 inColor;
layout(location = 3) in vec2 inTexCoord;

// 输出到片段着色器
layout(location = 0) out vec3 fragPos;      // 世界空间位置
layout(location = 1) out vec3 fragNormal;   // 世界空间法线
layout(location = 2) out vec3 fragColor;
layout(location = 3) out vec2 fragTexCoord;

void main() {
    // 计算世界空间位置
    vec4 worldPos = ubo.model * vec4(inPosition, 1.0);
    fragPos = worldPos.xyz;

    // 使用法线矩阵变换法线 (处理非均匀缩放)
    fragNormal = mat3(ubo.normalMatrix) * inNormal;

    fragColor = inColor;
    fragTexCoord = inTexCoord;

    // 最终裁剪空间位置
    gl_Position = ubo.proj * ubo.view * worldPos;
}
