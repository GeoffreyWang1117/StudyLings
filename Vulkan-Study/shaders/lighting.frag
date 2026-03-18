#version 450

// 光照 Uniform Buffer Object
layout(binding = 1) uniform LightUBO {
    vec3 lightPos;          // 光源位置
    vec3 viewPos;           // 观察者位置
    vec3 lightColor;        // 光照颜色
    float ambientStrength;  // 环境光强度
    float specularStrength; // 高光强度
    float shininess;        // 高光指数
} light;

// 从顶点着色器接收
layout(location = 0) in vec3 fragPos;
layout(location = 1) in vec3 fragNormal;
layout(location = 2) in vec3 fragColor;
layout(location = 3) in vec2 fragTexCoord;

// 输出颜色
layout(location = 0) out vec4 outColor;

void main() {
    // ========== Blinn-Phong 光照模型 ==========

    // 1. 环境光 (Ambient)
    // 模拟间接光照，使阴影区域不会完全黑暗
    vec3 ambient = light.ambientStrength * light.lightColor;

    // 2. 漫反射 (Diffuse)
    // 基于兰伯特余弦定律：光照强度与法线和光线夹角的余弦成正比
    vec3 norm = normalize(fragNormal);
    vec3 lightDir = normalize(light.lightPos - fragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * light.lightColor;

    // 3. 高光/镜面反射 (Specular) - Blinn-Phong
    // 使用半程向量而不是反射向量，计算更高效
    vec3 viewDir = normalize(light.viewPos - fragPos);
    vec3 halfwayDir = normalize(lightDir + viewDir);  // 半程向量

    // 高光强度：法线与半程向量夹角越小，高光越强
    float spec = pow(max(dot(norm, halfwayDir), 0.0), light.shininess);
    vec3 specular = light.specularStrength * spec * light.lightColor;

    // 4. 合成最终颜色
    vec3 result = (ambient + diffuse + specular) * fragColor;

    outColor = vec4(result, 1.0);
}
