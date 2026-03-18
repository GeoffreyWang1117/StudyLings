# Chapter 11: Concurrent Stacks

# Exercise 01: Concurrent Stack Implementations
add_executable(exercise01_concurrent_stacks
    exercise01_concurrent_stacks.cpp
)
target_link_libraries(exercise01_concurrent_stacks PRIVATE pthread)

# Tests
add_executable(stacks_tests
    test_stacks.cpp
)
target_link_libraries(stacks_tests PRIVATE GTest::gtest_main pthread)

add_test(NAME StacksTests COMMAND stacks_tests)
