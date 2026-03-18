# Chapter 10: Concurrent Queues

# Exercise 01: Concurrent Queue Implementations
add_executable(exercise01_concurrent_queues
    exercise01_concurrent_queues.cpp
)
target_link_libraries(exercise01_concurrent_queues PRIVATE pthread)

# Tests
add_executable(queues_tests
    test_queues.cpp
)
target_link_libraries(queues_tests PRIVATE GTest::gtest_main pthread)

add_test(NAME QueuesTests COMMAND queues_tests)
