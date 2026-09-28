# Netlings — every exercises/<chapter>/<name>.c becomes its own executable target <name>.
#   cmake --preset dev        && cmake --build --preset dev --target tcp2_echo_server
#   cmake --preset solutions  (maintainers: builds solutions/ instead of exercises/)
cmake_minimum_required(VERSION 3.28...4.1)
project(netlings LANGUAGES C)

set(CMAKE_C_STANDARD 23)           # GCC 15 / Clang 20+: -std=gnu23 (older compilers fall back to gnu2x)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)  # for clangd / clang-tidy
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(SL_SOURCE_DIR "exercises" CACHE STRING "Which tree to build: exercises or solutions")
set(SL_SANITIZE "address,undefined" CACHE STRING "Default sanitizers (empty to disable)")
set(SL_TSAN_CHAPTERS "07_pthread_sync" CACHE STRING "Chapters built with ThreadSanitizer instead")

find_package(Threads REQUIRED)

add_compile_definitions(_GNU_SOURCE)
add_compile_options(
  -Wall -Wextra -Wshadow -Wno-unused-parameter
  -Werror=implicit-function-declaration -Werror=incompatible-pointer-types
  -Werror=int-conversion -Werror=return-type
  -g -fno-omit-frame-pointer
  -fmacro-prefix-map=${CMAKE_SOURCE_DIR}/=)

file(GLOB chapter_dirs LIST_DIRECTORIES true ${CMAKE_SOURCE_DIR}/${SL_SOURCE_DIR}/*)
foreach(chapter_dir IN LISTS chapter_dirs)
  if(NOT IS_DIRECTORY ${chapter_dir})
    continue()
  endif()
  get_filename_component(chapter ${chapter_dir} NAME)
  if(chapter IN_LIST SL_TSAN_CHAPTERS AND SL_SANITIZE)
    set(san thread)
  else()
    set(san ${SL_SANITIZE})
  endif()

  file(GLOB sources CONFIGURE_DEPENDS ${chapter_dir}/*.c)
  foreach(src IN LISTS sources)
    get_filename_component(target ${src} NAME_WE)
    add_executable(${target} ${src})
    target_include_directories(${target} PRIVATE ${CMAKE_SOURCE_DIR}/include)
    target_link_libraries(${target} PRIVATE Threads::Threads)
    if(san)
      target_compile_options(${target} PRIVATE -fsanitize=${san} -fno-sanitize-recover=all)
      target_link_options(${target} PRIVATE -fsanitize=${san})
    endif()
  endforeach()
endforeach()
