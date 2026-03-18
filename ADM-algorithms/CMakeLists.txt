cmake_minimum_required(VERSION 3.15)
project(ADM_Judge VERSION 1.0 LANGUAGES CXX)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 编译选项
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pedantic")

# 包含目录
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/judge)

# 判题系统可执行文件
add_executable(adm-judge
    judge/main.cpp
)

# 安装目标
install(TARGETS adm-judge DESTINATION bin)

# 可选：构建所有练习（用于验证）
option(BUILD_ALL_EXERCISES "Build all exercises for verification" OFF)

if(BUILD_ALL_EXERCISES)
    file(GLOB_RECURSE EXERCISE_FILES "exercises/**/*.cpp")
    foreach(EXERCISE_FILE ${EXERCISE_FILES})
        get_filename_component(EXERCISE_NAME ${EXERCISE_FILE} NAME_WE)
        add_executable(${EXERCISE_NAME} ${EXERCISE_FILE})
    endforeach()
endif()

# 测试支持
enable_testing()
