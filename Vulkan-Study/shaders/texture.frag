#version 450

// 纹理采样器
layout(binding = 1) uniform sampler2D texSampler;

// 从顶点着色器接收
layout(location = 0) in vec3 fragColor;
layout(location = 1) in vec2 fragTexCoord;

// 输出颜色
layout(location = 0) out vec4 outColor;

void main() {
    // 采样纹理并与顶点颜色混合
    vec4 texColor = texture(texSampler, fragTexCoord);
    outColor = texColor * vec4(fragColor, 1.0);
}
