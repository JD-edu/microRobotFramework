# C++/microRobotFramework_04/CMakeLists.txt

# 1. Define the interface library (Header and C++ class implementation)
# This creates a reusable library target named 'mrf_lib_04'
add_library(mrf_lib_04 
    microRobotFramework_04.cpp
    microRobotFramework_04.hpp
)

# 2. Define the executable target (Your main application/example)
# This creates the 'mrf_example_04' executable
add_executable(mrf_example_04 
    mrf_example_04.cpp
)

# 3. Specify the necessary compilation flags (C++11 standard)
target_compile_features(mrf_lib_04 PUBLIC cxx_std_11)
target_compile_features(mrf_example_04 PRIVATE cxx_std_11)

# 4. Link the executable to the library
# The example needs the library's code to run.
target_link_libraries(mrf_example_04 PRIVATE mrf_lib_01)

# 5. Tell the executable where to find the header files
# Since the header is in the same directory, we add the current directory.
target_include_directories(mrf_example_04 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})