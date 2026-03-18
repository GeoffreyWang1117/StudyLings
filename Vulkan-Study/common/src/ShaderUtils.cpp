#include "ShaderUtils.h"
#include "FileUtils.h"
#include <stdexcept>

namespace ShaderUtils {

VkShaderModule createShaderModule(VkDevice device, const std::vector<char>& code) {
    VkShaderModuleCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;
    createInfo.codeSize = code.size();
    createInfo.pCode = reinterpret_cast<const uint32_t*>(code.data());

    VkShaderModule shaderModule;
    if (vkCreateShaderModule(device, &createInfo, nullptr, &shaderModule) != VK_SUCCESS) {
        throw std::runtime_error("Failed to create shader module!");
    }

    return shaderModule;
}

VkShaderModule createShaderModuleFromFile(VkDevice device, const std::string& filename) {
    auto code = FileUtils::readBinaryFile(filename);
    return createShaderModule(device, code);
}

VkPipelineShaderStageCreateInfo createShaderStageInfo(
    VkShaderStageFlagBits stage,
    VkShaderModule module,
    const char* entryPoint
) {
    VkPipelineShaderStageCreateInfo stageInfo{};
    stageInfo.sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    stageInfo.stage = stage;
    stageInfo.module = module;
    stageInfo.pName = entryPoint;
    return stageInfo;
}

void destroyShaderModule(VkDevice device, VkShaderModule module) {
    vkDestroyShaderModule(device, module, nullptr);
}

} // namespace ShaderUtils
