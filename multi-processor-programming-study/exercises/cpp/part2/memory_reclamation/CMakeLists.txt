# Memory Reclamation Exercises

# Exercise 01: Hazard Pointers
add_executable(exercise01_hazard_pointers exercise01_hazard_pointers.cpp)
target_link_libraries(exercise01_hazard_pointers PRIVATE pthread)

# Exercise 02: Epoch-Based Reclamation
add_executable(exercise02_epoch_based_reclamation exercise02_epoch_based_reclamation.cpp)
target_link_libraries(exercise02_epoch_based_reclamation PRIVATE pthread)

# Add to tests
add_test(NAME Exercise01_HazardPointers COMMAND exercise01_hazard_pointers)
add_test(NAME Exercise02_EpochBasedReclamation COMMAND exercise02_epoch_based_reclamation)
