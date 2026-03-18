#version 450

layout(location = 0) in vec2 fragTexCoord;

layout(binding = 0) uniform sampler2D inputTexture;

layout(push_constant) uniform PushConstants {
    int horizontal;  // 0 = 垂直, 1 = 水平
} pc;

layout(location = 0) out vec4 outColor;

// 高斯模糊权重 (5x5 kernel)
const float weight[5] = float[](
    0.2270270270,
    0.1945945946,
    0.1216216216,
    0.0540540541,
    0.0162162162
);

void main() {
    vec2 texOffset = 1.0 / textureSize(inputTexture, 0);
    vec3 result = texture(inputTexture, fragTexCoord).rgb * weight[0];

    if (pc.horizontal == 1) {
        for (int i = 1; i < 5; ++i) {
            result += texture(inputTexture, fragTexCoord + vec2(texOffset.x * i, 0.0)).rgb * weight[i];
            result += texture(inputTexture, fragTexCoord - vec2(texOffset.x * i, 0.0)).rgb * weight[i];
        }
    } else {
        for (int i = 1; i < 5; ++i) {
            result += texture(inputTexture, fragTexCoord + vec2(0.0, texOffset.y * i)).rgb * weight[i];
            result += texture(inputTexture, fragTexCoord - vec2(0.0, texOffset.y * i)).rgb * weight[i];
        }
    }

    outColor = vec4(result, 1.0);
}
