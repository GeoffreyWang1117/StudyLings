# Chapter 2: Mutual Exclusion

# Exercise 01: Peterson Lock
add_executable(exercise01_peterson_lock
    exercise01_peterson_lock.cpp
)
target_link_libraries(exercise01_peterson_lock PRIVATE pthread)

# Exercise 02: Filter Lock
add_executable(exercise02_filter_lock
    exercise02_filter_lock.cpp
)
target_link_libraries(exercise02_filter_lock PRIVATE pthread)

# Exercise 03: Memory Ordering
add_executable(exercise03_memory_ordering
    exercise03_memory_ordering.cpp
)
target_link_libraries(exercise03_memory_ordering PRIVATE pthread)

# Exercise 04: Bakery Lock
add_executable(exercise04_bakery_lock
    exercise04_bakery_lock.cpp
)
target_link_libraries(exercise04_bakery_lock PRIVATE pthread)

# Tests
add_executable(mutual_exclusion_tests
    test_mutual_exclusion.cpp
    exercise01_peterson_lock.cpp
    exercise02_filter_lock.cpp
)
target_link_libraries(mutual_exclusion_tests PRIVATE GTest::gtest_main pthread)

add_test(NAME MutualExclusionTests COMMAND mutual_exclusion_tests)
