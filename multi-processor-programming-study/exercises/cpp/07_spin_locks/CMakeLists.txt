# Chapter 7: Spin Locks

# Exercise 01: Spin Lock Implementations
add_executable(exercise01_spin_locks
    exercise01_spin_locks.cpp
)
target_link_libraries(exercise01_spin_locks PRIVATE pthread)

# Tests
add_executable(spin_locks_tests
    test_spin_locks.cpp
)
target_link_libraries(spin_locks_tests PRIVATE GTest::gtest_main pthread)

add_test(NAME SpinLocksTests COMMAND spin_locks_tests)
