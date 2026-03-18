#pragma once

#define GLFW_INCLUDE_VULKAN
#include <GLFW/glfw3.h>

#include <string>
#include <vector>

namespace ShaderUtils {

// 从 SPIR-V 文件创建着色器模块
VkShaderModule createShaderModule(VkDevice device, const std::vector<char>& code);

// 从文件创建着色器模块
VkShaderModule createShaderModuleFromFile(VkDevice device, const std::string& filename);

// 创建着色器阶段信息
VkPipelineShaderStageCreateInfo createShaderStageInfo(
    VkShaderStageFlagBits stage,
    VkShaderModule module,
    const char* entryPoint = "main"
);

// 销毁着色器模块
void destroyShaderModule(VkDevice device, VkShaderModule module);

} // namespace ShaderUtils
