#version 450

// 亮度提取着色器 - 用于 Bloom 效果的第一步
// 提取图像中高亮度区域

layout(location = 0) in vec2 fragTexCoord;

layout(binding = 0) uniform sampler2D sceneTexture;

layout(location = 0) out vec4 outColor;

// 亮度阈值
const float threshold = 1.0;

void main() {
    vec3 color = texture(sceneTexture, fragTexCoord).rgb;

    // 计算亮度 (使用人眼感知权重)
    float brightness = dot(color, vec3(0.2126, 0.7152, 0.0722));

    // 如果亮度超过阈值，输出颜色；否则输出黑色
    if (brightness > threshold) {
        outColor = vec4(color, 1.0);
    } else {
        outColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
}
