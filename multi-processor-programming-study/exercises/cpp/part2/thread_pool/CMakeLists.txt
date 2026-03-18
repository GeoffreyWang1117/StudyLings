# Thread Pool Exercise

add_executable(exercise01_thread_pool
    exercise01_thread_pool.cpp
)

target_link_libraries(exercise01_thread_pool PRIVATE pthread)

# Set C++20 standard
set_property(TARGET exercise01_thread_pool PROPERTY CXX_STANDARD 20)
