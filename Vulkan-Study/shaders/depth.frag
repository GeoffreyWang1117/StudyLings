#version 450

// 从顶点着色器接收
layout(location = 0) in vec3 fragColor;
layout(location = 1) in vec2 fragTexCoord;

// 输出颜色
layout(location = 0) out vec4 outColor;

void main() {
    // 简单颜色输出，深度测试由管线自动处理
    outColor = vec4(fragColor, 1.0);
}
