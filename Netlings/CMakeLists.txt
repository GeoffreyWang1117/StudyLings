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
find_package(PkgConfig)

# Per-chapter libraries (pkg-config names). When one is missing, that chapter's targets become
# stubs that fail with an install hint, so every other chapter still builds.
set(SL_LIBS_08_io_uring liburing)
set(SL_LIBS_10_ebpf_xdp libbpf)
set(SL_LIBS_12_rdma_roce libibverbs librdmacm)

# Chapters whose exercise files hold BOTH a BPF program (#ifdef __BPF__) and its user-space
# loader: the file is compiled twice, once by clang -target bpf into bin/<name>.bpf.o.
set(SL_BPF_CHAPTERS "10_ebpf_xdp")
find_program(SL_BPF_CLANG NAMES clang-21 clang-20 clang-19 clang-18 clang)
if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64|AMD64")
  set(SL_BPF_ARCH x86)
elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64|arm64")
  set(SL_BPF_ARCH arm64)
else()
  set(SL_BPF_ARCH ${CMAKE_SYSTEM_PROCESSOR})
endif()

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

  set(libs)
  set(missing)
  foreach(pkg IN LISTS SL_LIBS_${chapter})
    string(MAKE_C_IDENTIFIER ${pkg} pkg_id)
    if(PKG_CONFIG_FOUND)
      pkg_check_modules(SLPKG_${pkg_id} QUIET IMPORTED_TARGET ${pkg})
    endif()
    if(SLPKG_${pkg_id}_FOUND)
      list(APPEND libs PkgConfig::SLPKG_${pkg_id})
    else()
      list(APPEND missing ${pkg})
    endif()
  endforeach()
  if(chapter IN_LIST SL_BPF_CHAPTERS AND NOT SL_BPF_CLANG)
    list(APPEND missing clang)
  endif()

  file(GLOB sources CONFIGURE_DEPENDS ${chapter_dir}/*.c)
  foreach(src IN LISTS sources)
    get_filename_component(target ${src} NAME_WE)
    if(missing)
      add_custom_target(${target}
        COMMAND ${CMAKE_COMMAND} -E echo "error: ${target} needs: ${missing} (apt install liburing-dev libbpf-dev libibverbs-dev librdmacm-dev clang)"
        COMMAND ${CMAKE_COMMAND} -E false)
      continue()
    endif()
    add_executable(${target} ${src})
    target_link_libraries(${target} PRIVATE ${libs})
    if(chapter IN_LIST SL_BPF_CHAPTERS)
      set(bpf_obj ${CMAKE_BINARY_DIR}/bin/${target}.bpf.o)
      add_custom_command(
        OUTPUT ${bpf_obj}
        COMMAND ${SL_BPF_CLANG} -O2 -g -target bpf -D__TARGET_ARCH_${SL_BPF_ARCH}
                -I${CMAKE_SOURCE_DIR}/include -I/usr/include/${CMAKE_LIBRARY_ARCHITECTURE}
                -c ${src} -o ${bpf_obj}
        DEPENDS ${src}
        COMMENT "BPF ${target}.bpf.o")
      add_custom_target(${target}_bpf DEPENDS ${bpf_obj})
      add_dependencies(${target} ${target}_bpf)
      target_compile_definitions(${target} PRIVATE SL_BPF_OBJ="${bpf_obj}")
    endif()
    target_include_directories(${target} PRIVATE ${CMAKE_SOURCE_DIR}/include)
    target_link_libraries(${target} PRIVATE Threads::Threads)
    if(san)
      target_compile_options(${target} PRIVATE -fsanitize=${san} -fno-sanitize-recover=all)
      target_link_options(${target} PRIVATE -fsanitize=${san})
    endif()
  endforeach()
endforeach()
