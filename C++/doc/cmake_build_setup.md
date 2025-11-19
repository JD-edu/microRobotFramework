# 🤖 CMake Build Guide for Micro Robot Framework
This document outlines the standard configuration and build process using CMake for projects with a nested structure, specifically for the microRobotFramework components (microRobotFramework_01, microRobotFramework_02, etc.).

## 1. 📁 Required Project Structure
The project uses a standard multi-level structure where a top-level CMakeLists.txt manages the overall project and delegates the actual build definitions to the subdirectories.

The structure for the microRobotFramework_01 component should be:

/C++<br>
├── CMakeLists.txt  <-- Top-level project<br>
├── microRobotFramework_01<br>
│   ├── microRobotFramework_01.hpp    (Header)<br>
│   ├── microRobotFramework_01.cpp    (Source/Library Implementation)<br>
│   ├── mrf_example_01.cpp          (Executable/Main Application)<br>
│   └── CMakeLists.txt              <-- Sub-project build definition<br> 
└── microRobotFramework_02<br> 
    └── ... (similar files and CMakeLists.txt)<br>

## 2. ⚙️ CMake Configuration Files
### 2.1. Top-Level CMakeLists.txt (in /C++)
This file initializes the project and tells CMake to look inside the subdirectories for specific build targets.
```CMake
# /C++/CMakeLists.txt
# Specify the minimum required CMake version
cmake_minimum_required(VERSION 3.10)
# Define the project name and the language used
project(RobotFrameworks CXX)
# Add all subdirectories that contain their own CMakeLists.txt files
add_subdirectory(microRobotFramework1)
add_subdirectory(microRobotFramework2)
# Optional: Set common build properties for the entire project
# set(CMAKE_BUILD_TYPE Debug)
```

### 2.2. Sub-Project CMakeLists.txt (in /C++/microRobotFramework_01)
This file defines two separate targets: the Library (mrf_lib_01) and the Executable (mrf_example_01), and handles their linkage.

```CMake
# /C++/microRobotFramework1/CMakeLists.txt

# Define the reusable class implementation as a static/shared library.
# This target contains the core functionality (microRobotFramework_01.cpp).
add_library(mrf_lib_01 
    microRobotFramework_01.cpp
    microRobotFramework_01.hpp
)

# Define the main application/example as an executable.
# This target contains the 'main' function (mrf_example_01.cpp).
add_executable(mrf_example_01 
    mrf_example_01.cpp
)

# Ensure C++11 standard is used for compilation.
target_compile_features(mrf_lib_01 PUBLIC cxx_std_11)
target_compile_features(mrf_example_01 PRIVATE cxx_std_11)

# Link the executable to the library.
# The executable depends on the compiled code in mrf_lib_01.
target_link_libraries(mrf_example_01 PRIVATE mrf_lib_01)

# Specify include path so the executable can find "microRobotFramework.hpp"
# (Assuming the header is in the same directory as the source files.)
target_include_directories(mrf_example_01 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}) 
```

## 3. 🛠️ Build Process
Follow these steps from the root /C++ directory to configure and build your project. This process uses an out-of-source build, which is the recommended practice.

### Step 1: Create Build Directory
```Bash
cd /C++
mkdir build
cd build
```
### Step 2: Configure CMake
Run CMake to generate the build files (e.g., Makefiles or Visual Studio projects).

```Bash

# The '..' points to the parent directory where the root CMakeLists.txt is located
cmake ..
```
 
### Step 3: Build the Targets
Use the multi-platform build command to compile the project.

```Bash

# This command automatically runs the compiler.
make 
```
The resulting executable, mrf_example_01, will be located in the build/microRobotFramework1 directory (or similar, depending on the generator and OS).


