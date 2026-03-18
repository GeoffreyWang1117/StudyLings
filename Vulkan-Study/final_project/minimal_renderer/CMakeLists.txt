cmake_minimum_required(VERSION 3.16)
project(MinimalVulkanRenderer VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找 Vulkan
find_package(Vulkan REQUIRED)

# 查找 GLFW
find_package(glfw3 3.3 REQUIRED)

# 源文件
set(SOURCES
    src/main.cpp
    src/VulkanRenderer.cpp
)

# 头文件目录
set(INCLUDE_DIRS
    include
    ${CMAKE_SOURCE_DIR}/../../external/stb
    ${CMAKE_SOURCE_DIR}/../../external/tinyobjloader
    ${CMAKE_SOURCE_DIR}/../../external/glm
)

# 创建可执行文件
add_executable(${PROJECT_NAME} ${SOURCES})

# 包含目录
target_include_directories(${PROJECT_NAME} PRIVATE
    ${INCLUDE_DIRS}
    ${Vulkan_INCLUDE_DIRS}
)

# 链接库
target_link_libraries(${PROJECT_NAME} PRIVATE
    Vulkan::Vulkan
    glfw
)

# 编译着色器
find_program(GLSLC glslc HINTS $ENV{VULKAN_SDK}/Bin)

if(GLSLC)
    set(SHADER_DIR ${CMAKE_CURRENT_SOURCE_DIR}/shaders)
    set(SHADER_OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/shaders)

    file(MAKE_DIRECTORY ${SHADER_OUTPUT_DIR})

    # 获取所有着色器文件
    file(GLOB SHADER_SOURCES
        "${SHADER_DIR}/*.vert"
        "${SHADER_DIR}/*.frag"
    )

    # 编译每个着色器
    foreach(SHADER ${SHADER_SOURCES})
        get_filename_component(SHADER_NAME ${SHADER} NAME)
        set(SPIRV_OUTPUT "${SHADER_OUTPUT_DIR}/${SHADER_NAME}.spv")

        add_custom_command(
            OUTPUT ${SPIRV_OUTPUT}
            COMMAND ${GLSLC} ${SHADER} -o ${SPIRV_OUTPUT}
            DEPENDS ${SHADER}
            COMMENT "Compiling ${SHADER_NAME}"
        )

        list(APPEND SPIRV_OUTPUTS ${SPIRV_OUTPUT})
    endforeach()

    add_custom_target(Shaders ALL DEPENDS ${SPIRV_OUTPUTS})
    add_dependencies(${PROJECT_NAME} Shaders)
endif()

# 复制资源
file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/models DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/textures DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# 安装
install(TARGETS ${PROJECT_NAME} DESTINATION bin)
install(DIRECTORY ${SHADER_OUTPUT_DIR} DESTINATION bin)
