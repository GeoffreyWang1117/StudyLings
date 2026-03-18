# Chapter 3: Concurrent Objects

# Exercise 01: Sequential Consistency
add_executable(exercise01_sequential_consistency
    exercise01_sequential_consistency.cpp
)
target_link_libraries(exercise01_sequential_consistency PRIVATE pthread)

# Exercise 02: Linearizability
add_executable(exercise02_linearizability
    exercise02_linearizability.cpp
)
target_link_libraries(exercise02_linearizability PRIVATE pthread)

# Exercise 03: Progress Conditions
add_executable(exercise03_progress_conditions
    exercise03_progress_conditions.cpp
)
target_link_libraries(exercise03_progress_conditions PRIVATE pthread)

# Tests
add_executable(concurrent_objects_tests
    test_concurrent_objects.cpp
)
target_link_libraries(concurrent_objects_tests PRIVATE GTest::gtest_main pthread)

add_test(NAME ConcurrentObjectsTests COMMAND concurrent_objects_tests)
