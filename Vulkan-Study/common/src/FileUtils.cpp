#include "FileUtils.h"
#include <filesystem>

namespace FileUtils {

std::vector<char> readBinaryFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::ate | std::ios::binary);

    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file: " + filename);
    }

    size_t fileSize = static_cast<size_t>(file.tellg());
    std::vector<char> buffer(fileSize);

    file.seekg(0);
    file.read(buffer.data(), fileSize);

    file.close();
    return buffer;
}

std::string readTextFile(const std::string& filename) {
    std::ifstream file(filename);

    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file: " + filename);
    }

    std::string content((std::istreambuf_iterator<char>(file)),
                        std::istreambuf_iterator<char>());

    file.close();
    return content;
}

bool fileExists(const std::string& filename) {
    return std::filesystem::exists(filename);
}

std::string getFileExtension(const std::string& filename) {
    std::filesystem::path path(filename);
    return path.extension().string();
}

std::string getFileName(const std::string& filepath) {
    std::filesystem::path path(filepath);
    return path.filename().string();
}

std::string getDirectory(const std::string& filepath) {
    std::filesystem::path path(filepath);
    return path.parent_path().string();
}

} // namespace FileUtils
