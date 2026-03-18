cmake_minimum_required(VERSION 3.16)
project(Vulkanlings VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 查找依赖
find_package(Vulkan REQUIRED)
find_package(glfw3 3.3 REQUIRED)

# GLM 配置
find_package(glm QUIET)
if(NOT glm_FOUND)
    # 如果没有安装 GLM，使用头文件路径
    set(GLM_INCLUDE_DIR "/usr/include/glm" CACHE PATH "GLM include directory")
    if(EXISTS ${GLM_INCLUDE_DIR})
        message(STATUS "Using GLM from: ${GLM_INCLUDE_DIR}")
    else()
        message(WARNING "GLM not found. Some exercises may not compile.")
    endif()
endif()

# 编译选项
add_compile_options(-Wall -Wextra -Wpedantic)

# Debug 模式启用验证层
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_definitions(-DENABLE_VALIDATION_LAYERS)
endif()

# 公共头文件
include_directories(${CMAKE_SOURCE_DIR}/common/include)
include_directories(${Vulkan_INCLUDE_DIRS})

# 公共库
add_library(vulkanlings_common STATIC
    common/src/VulkanUtils.cpp
    common/src/FileUtils.cpp
    common/src/ShaderUtils.cpp
)
target_link_libraries(vulkanlings_common PUBLIC
    Vulkan::Vulkan
    glfw
)
if(glm_FOUND)
    target_link_libraries(vulkanlings_common PUBLIC glm::glm)
endif()

# 编译着色器的函数
function(compile_shader TARGET SHADER)
    get_filename_component(SHADER_NAME ${SHADER} NAME)
    set(SPIRV_OUTPUT "${CMAKE_BINARY_DIR}/shaders/${SHADER_NAME}.spv")

    add_custom_command(
        OUTPUT ${SPIRV_OUTPUT}
        COMMAND ${CMAKE_COMMAND} -E make_directory "${CMAKE_BINARY_DIR}/shaders"
        COMMAND Vulkan::glslangValidator -V ${SHADER} -o ${SPIRV_OUTPUT}
        DEPENDS ${SHADER}
        COMMENT "Compiling shader: ${SHADER_NAME}"
    )

    set_property(TARGET ${TARGET} APPEND PROPERTY
        ADDITIONAL_CLEAN_FILES ${SPIRV_OUTPUT}
    )

    target_sources(${TARGET} PRIVATE ${SPIRV_OUTPUT})
endfunction()

# 练习目标
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

foreach(EXERCISE ${EXERCISES})
    if(EXISTS "${CMAKE_SOURCE_DIR}/exercises/${EXERCISE}/main.cpp")
        add_executable(${EXERCISE} "exercises/${EXERCISE}/main.cpp")
        target_link_libraries(${EXERCISE} PRIVATE vulkanlings_common)

        # 如果练习有着色器，编译它们
        file(GLOB EXERCISE_SHADERS "exercises/${EXERCISE}/*.vert" "exercises/${EXERCISE}/*.frag")
        foreach(SHADER ${EXERCISE_SHADERS})
            compile_shader(${EXERCISE} ${SHADER})
        endforeach()
    endif()
endforeach()

# 最终项目
if(EXISTS "${CMAKE_SOURCE_DIR}/final_project/minimal_renderer/src/main.cpp")
    file(GLOB_RECURSE RENDERER_SOURCES "final_project/minimal_renderer/src/*.cpp")
    add_executable(minimal_renderer ${RENDERER_SOURCES})
    target_include_directories(minimal_renderer PRIVATE
        "${CMAKE_SOURCE_DIR}/final_project/minimal_renderer/include"
    )
    target_link_libraries(minimal_renderer PRIVATE vulkanlings_common)

    # 编译渲染器着色器
    file(GLOB RENDERER_SHADERS "final_project/minimal_renderer/shaders/*.vert"
                               "final_project/minimal_renderer/shaders/*.frag")
    foreach(SHADER ${RENDERER_SHADERS})
        compile_shader(minimal_renderer ${SHADER})
    endforeach()
endif()

# Vulkanlings 运行器
configure_file(
    "${CMAKE_SOURCE_DIR}/tools/vulkanlings.in"
    "${CMAKE_BINARY_DIR}/vulkanlings"
    @ONLY
)

# 复制着色器到构建目录
add_custom_target(copy_shaders ALL
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        "${CMAKE_SOURCE_DIR}/shaders"
        "${CMAKE_BINARY_DIR}/shaders"
    COMMENT "Copying shaders to build directory"
)

# 安装目标
install(TARGETS vulkanlings_common DESTINATION lib)
install(DIRECTORY common/include/ DESTINATION include)
