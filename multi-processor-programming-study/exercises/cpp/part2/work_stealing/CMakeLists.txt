# Work Stealing Exercises

# Exercise 01: Work-Stealing Deque (Chase-Lev)
add_executable(exercise01_work_stealing_deque exercise01_work_stealing_deque.cpp)
target_link_libraries(exercise01_work_stealing_deque PRIVATE pthread)

# Add to tests
add_test(NAME Exercise01_WorkStealingDeque COMMAND exercise01_work_stealing_deque)
