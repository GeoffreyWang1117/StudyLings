# Chapter 1: Basics

# Exercise 01: Hello Threads
add_executable(exercise01_hello_threads
    exercise01_hello_threads.cpp
)
target_link_libraries(exercise01_hello_threads PRIVATE pthread)

# Exercise 02: Race Condition
add_executable(exercise02_race_condition
    exercise02_race_condition.cpp
)
target_link_libraries(exercise02_race_condition PRIVATE pthread)

# Exercise 03: Synchronization
add_executable(exercise03_synchronization
    exercise03_synchronization.cpp
)
target_link_libraries(exercise03_synchronization PRIVATE pthread)

# Tests
add_executable(basics_tests
    test_basics.cpp
    exercise01_hello_threads.cpp
    exercise02_race_condition.cpp
    exercise03_synchronization.cpp
)
target_link_libraries(basics_tests PRIVATE GTest::gtest_main pthread)

add_test(NAME BasicsTests COMMAND basics_tests)
