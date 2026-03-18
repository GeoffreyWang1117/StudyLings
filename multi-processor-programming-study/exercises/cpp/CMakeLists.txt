cmake_minimum_required(VERSION 3.20)
project(MultiprocessorProgrammingExercises VERSION 1.0 LANGUAGES CXX)

# Require C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Add compiler warnings
if(MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

# Enable testing
enable_testing()

# Find Google Test
find_package(GTest QUIET)
if(NOT GTest_FOUND)
    # Download and build Google Test if not found
    include(FetchContent)
    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG v1.14.0
    )
    # For Windows: Prevent overriding the parent project's compiler/linker settings
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)
endif()

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Add subdirectories for each module
add_subdirectory(01_basics)
add_subdirectory(02_mutual_exclusion)
add_subdirectory(03_concurrent_objects)
add_subdirectory(04_foundations)
add_subdirectory(05_synchronization)
add_subdirectory(06_consensus)
add_subdirectory(07_spin_locks)
add_subdirectory(08_monitors)
add_subdirectory(09_linked_lists)
add_subdirectory(10_queues)
add_subdirectory(11_stacks)

# Part 2: Advanced Topics
add_subdirectory(part2)

# Runner executable
add_subdirectory(runner)

# Print configuration summary
message(STATUS "========================================")
message(STATUS "Multi-Processor Programming Exercises")
message(STATUS "========================================")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "========================================")
