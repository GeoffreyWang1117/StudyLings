# RCU (Read-Copy-Update) Exercises

# Exercise 01: RCU
add_executable(exercise01_rcu exercise01_rcu.cpp)
target_link_libraries(exercise01_rcu PRIVATE pthread)

# Add to tests
add_test(NAME Exercise01_RCU COMMAND exercise01_rcu)
