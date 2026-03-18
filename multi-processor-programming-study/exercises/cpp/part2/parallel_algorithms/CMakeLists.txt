# Parallel Algorithms Exercises

# Exercise 01: Parallel Sorting
add_executable(exercise01_parallel_sorting exercise01_parallel_sorting.cpp)
target_link_libraries(exercise01_parallel_sorting PRIVATE pthread)

# Add to tests
add_test(NAME Exercise01_ParallelSorting COMMAND exercise01_parallel_sorting)
