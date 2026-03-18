#version 450

// Uniform Buffer Object - MVP 矩阵
layout(binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
} ubo;

// 顶点输入
layout(location = 0) in vec2 inPosition;
layout(location = 1) in vec3 inColor;

// 输出到片段着色器
layout(location = 0) out vec3 fragColor;

void main() {
    // 应用 MVP 变换
    gl_Position = ubo.proj * ubo.view * ubo.model * vec4(inPosition, 0.0, 1.0);
    fragColor = inColor;
}
