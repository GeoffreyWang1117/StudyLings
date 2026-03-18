# 练习 16 提示 - 纹理映射

## 采样器描述符布局

```cpp
VkDescriptorSetLayoutBinding samplerLayoutBinding{};
samplerLayoutBinding.binding = 1;
samplerLayoutBinding.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
samplerLayoutBinding.descriptorCount = 1;
samplerLayoutBinding.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
```

## 创建图像

```cpp
VkImageCreateInfo imageInfo{};
imageInfo.sType = VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO;
imageInfo.imageType = VK_IMAGE_TYPE_2D;
imageInfo.extent.width = width;
imageInfo.extent.height = height;
imageInfo.extent.depth = 1;
imageInfo.mipLevels = 1;
imageInfo.arrayLayers = 1;
imageInfo.format = format;
imageInfo.tiling = tiling;
imageInfo.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
imageInfo.usage = usage;
imageInfo.samples = VK_SAMPLE_COUNT_1_BIT;
```

## 图像内存屏障

```cpp
VkImageMemoryBarrier barrier{};
barrier.sType = VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER;
barrier.oldLayout = oldLayout;
barrier.newLayout = newLayout;
barrier.image = image;
```

## 创建纹理图像

```cpp
createImage(texWidth, texHeight, VK_FORMAT_R8G8B8A8_SRGB,
           VK_IMAGE_TILING_OPTIMAL,
           VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_SAMPLED_BIT,
           VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT,
           textureImage, textureImageMemory);
```

## 采样器配置

```cpp
VkSamplerCreateInfo samplerInfo{};
samplerInfo.sType = VK_STRUCTURE_TYPE_SAMPLER_CREATE_INFO;
samplerInfo.magFilter = VK_FILTER_LINEAR;
samplerInfo.minFilter = VK_FILTER_LINEAR;
samplerInfo.addressModeU = VK_SAMPLER_ADDRESS_MODE_REPEAT;
samplerInfo.addressModeV = VK_SAMPLER_ADDRESS_MODE_REPEAT;
samplerInfo.addressModeW = VK_SAMPLER_ADDRESS_MODE_REPEAT;
samplerInfo.anisotropyEnable = VK_TRUE;
```

## 描述符池大小

```cpp
poolSizes[1].type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
poolSizes[1].descriptorCount = static_cast<uint32_t>(MAX_FRAMES_IN_FLIGHT);
```

## 图像描述符信息

```cpp
VkDescriptorImageInfo imageInfo{};
imageInfo.imageLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
imageInfo.imageView = textureImageView;
imageInfo.sampler = textureSampler;
```

## 采样器描述符写入

```cpp
descriptorWrites[1].dstBinding = 1;
descriptorWrites[1].descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
descriptorWrites[1].pImageInfo = &imageInfo;
```

## 清理纹理资源

```cpp
vkDestroySampler(device, textureSampler, nullptr);
vkDestroyImageView(device, textureImageView, nullptr);
vkDestroyImage(device, textureImage, nullptr);
vkFreeMemory(device, textureImageMemory, nullptr);
```

## 需要填写的答案

1. 采样器描述符布局: `binding=1, descriptorType=VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, descriptorCount=1, stageFlags=VK_SHADER_STAGE_FRAGMENT_BIT`
2. 图像创建: `imageType=VK_IMAGE_TYPE_2D, mipLevels=1, arrayLayers=1, initialLayout=VK_IMAGE_LAYOUT_UNDEFINED, samples=VK_SAMPLE_COUNT_1_BIT`
3. 图像屏障: `oldLayout=oldLayout, newLayout=newLayout, image=image`
4. 纹理图像: `format=VK_FORMAT_R8G8B8A8_SRGB, tiling=VK_IMAGE_TILING_OPTIMAL, usage=VK_IMAGE_USAGE_TRANSFER_DST_BIT | VK_IMAGE_USAGE_SAMPLED_BIT, properties=VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT`
5. 采样器: `magFilter=VK_FILTER_LINEAR, minFilter=VK_FILTER_LINEAR, addressMode=VK_SAMPLER_ADDRESS_MODE_REPEAT, anisotropyEnable=VK_TRUE`
6. 描述符池: `type=VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER`
7. 图像信息: `imageLayout=VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL, imageView=textureImageView, sampler=textureSampler`
8. 采样器写入: `dstBinding=1, descriptorType=VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, pImageInfo=&imageInfo`
9. 清理: `textureSampler, textureImageView, textureImage, textureImageMemory`
