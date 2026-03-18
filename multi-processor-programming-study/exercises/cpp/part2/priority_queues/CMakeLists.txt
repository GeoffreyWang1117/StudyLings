# Priority Queue Exercises

# Exercise 01: Concurrent Priority Queues
add_executable(exercise01_concurrent_priority_queue exercise01_concurrent_priority_queue.cpp)
target_link_libraries(exercise01_concurrent_priority_queue PRIVATE pthread)

# Add to tests
add_test(NAME Exercise01_ConcurrentPriorityQueue COMMAND exercise01_concurrent_priority_queue)
