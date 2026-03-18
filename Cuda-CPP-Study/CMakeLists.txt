cmake_minimum_required(VERSION 3.18)
project(CUDAlings LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CUDA_STANDARD 14)
set(CMAKE_CUDA_STANDARD_REQUIRED ON)

# 查找 CUDA
find_package(CUDA QUIET)
if(NOT CUDA_FOUND)
    message(STATUS "CUDA not found. Building without CUDA support (exercises won't compile).")
    set(BUILD_CUDA_EXERCISES OFF)
else()
    message(STATUS "CUDA found: ${CUDA_VERSION}")
    set(BUILD_CUDA_EXERCISES ON)

    # 设置 CUDA 架构
    set(CMAKE_CUDA_ARCHITECTURES 60 70 75 80)
endif()

# 源文件
set(SOURCES
    src/main.cpp
    src/exercise_manager.cpp
    src/progress.cpp
    src/runner.cpp
)

# 创建可执行文件
add_executable(cudalings ${SOURCES})

# 包含目录
target_include_directories(cudalings PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

# 需要文件系统库
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND CMAKE_CXX_COMPILER_VERSION VERSION_LESS 9.0)
    target_link_libraries(cudalings stdc++fs)
endif()

# 安装
install(TARGETS cudalings DESTINATION bin)

# 显示构建信息
message(STATUS "==================================")
message(STATUS "CUDAlings Configuration")
message(STATUS "==================================")
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER}")
if(BUILD_CUDA_EXERCISES)
    message(STATUS "CUDA Compiler: ${CMAKE_CUDA_COMPILER}")
    message(STATUS "CUDA Version: ${CUDA_VERSION}")
endif()
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "==================================")
