#version 450

layout(location = 0) in vec2 fragTexCoord;

layout(binding = 0) uniform sampler2D sceneTexture;
layout(binding = 1) uniform sampler2D bloomTexture;

layout(location = 0) out vec4 outColor;

// Bloom 参数
const float bloomStrength = 0.3;
const float exposure = 1.0;
const float gamma = 2.2;

void main() {
    vec3 sceneColor = texture(sceneTexture, fragTexCoord).rgb;
    vec3 bloomColor = texture(bloomTexture, fragTexCoord).rgb;

    // 混合场景和 Bloom
    vec3 result = sceneColor + bloomColor * bloomStrength;

    // HDR 色调映射 (Reinhard)
    result = result / (result + vec3(1.0));

    // Gamma 校正
    result = pow(result, vec3(1.0 / gamma));

    outColor = vec4(result, 1.0);
}
