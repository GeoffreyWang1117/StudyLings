#pragma once

#include <string>
#include <vector>
#include <fstream>
#include <stdexcept>

namespace FileUtils {

// 读取二进制文件
std::vector<char> readBinaryFile(const std::string& filename);

// 读取文本文件
std::string readTextFile(const std::string& filename);

// 检查文件是否存在
bool fileExists(const std::string& filename);

// 获取文件扩展名
std::string getFileExtension(const std::string& filename);

// 获取文件名（不含路径）
std::string getFileName(const std::string& filepath);

// 获取目录路径
std::string getDirectory(const std::string& filepath);

} // namespace FileUtils
