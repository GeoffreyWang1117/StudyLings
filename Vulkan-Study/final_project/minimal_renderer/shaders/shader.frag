#version 450

layout(location = 0) in vec3 fragPos;
layout(location = 1) in vec3 fragNormal;
layout(location = 2) in vec2 fragTexCoord;

layout(binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
    vec3 lightPos;
    vec3 viewPos;
} ubo;

layout(binding = 1) uniform sampler2D texSampler;

layout(location = 0) out vec4 outColor;

// Blinn-Phong 光照参数
const vec3 lightColor = vec3(1.0, 1.0, 1.0);
const float ambientStrength = 0.1;
const float specularStrength = 0.5;
const float shininess = 32.0;

void main() {
    vec3 color = texture(texSampler, fragTexCoord).rgb;
    vec3 normal = normalize(fragNormal);

    // 环境光
    vec3 ambient = ambientStrength * lightColor;

    // 漫反射
    vec3 lightDir = normalize(ubo.lightPos - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    // Blinn-Phong 镜面反射
    vec3 viewDir = normalize(ubo.viewPos - fragPos);
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), shininess);
    vec3 specular = specularStrength * spec * lightColor;

    // 最终颜色
    vec3 result = (ambient + diffuse + specular) * color;
    outColor = vec4(result, 1.0);
}
