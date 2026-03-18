# 练习 CMakeLists.txt
# 为每个练习创建独立的可执行文件

cmake_minimum_required(VERSION 3.16)

# 查找 Vulkan
find_package(Vulkan REQUIRED)

# 查找 GLFW
find_package(glfw3 3.3 REQUIRED)

# 公共包含目录
set(COMMON_INCLUDE_DIRS
    ${CMAKE_SOURCE_DIR}/common/include
    ${CMAKE_SOURCE_DIR}/external/stb
    ${CMAKE_SOURCE_DIR}/external/tinyobjloader
    ${CMAKE_SOURCE_DIR}/external/glm
)

# 公共源文件
set(COMMON_SOURCES
    ${CMAKE_SOURCE_DIR}/common/src/VulkanUtils.cpp
    ${CMAKE_SOURCE_DIR}/common/src/FileUtils.cpp
    ${CMAKE_SOURCE_DIR}/common/src/ShaderUtils.cpp
)

# 练习列表
set(EXERCISES
    00_intro
    01_instance
    02_physical_device
    03_logical_device
    04_surface
    05_swapchain
    06_image_views
    07_render_pass
    08_pipeline
    09_framebuffers
    10_command_buffers
    11_sync
    12_triangle
    13_vertex_buffers
    14_index_buffers
    15_uniforms
    16_textures
    17_depth
    18_model_loading
    19_lighting
)

# 为每个练习创建目标
foreach(EXERCISE ${EXERCISES})
    set(EXERCISE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/${EXERCISE})
    set(EXERCISE_MAIN ${EXERCISE_DIR}/main.cpp)

    if(EXISTS ${EXERCISE_MAIN})
        # 创建可执行文件
        add_executable(${EXERCISE} ${EXERCISE_MAIN} ${COMMON_SOURCES})

        # 包含目录
        target_include_directories(${EXERCISE} PRIVATE
            ${COMMON_INCLUDE_DIRS}
            ${Vulkan_INCLUDE_DIRS}
        )

        # 链接库
        target_link_libraries(${EXERCISE} PRIVATE
            Vulkan::Vulkan
            glfw
        )

        # 设置输出目录
        set_target_properties(${EXERCISE} PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/exercises
        )

        message(STATUS "Added exercise: ${EXERCISE}")
    else()
        message(WARNING "Exercise ${EXERCISE} not found: ${EXERCISE_MAIN}")
    endif()
endforeach()
