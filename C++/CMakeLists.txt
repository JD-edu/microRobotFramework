cmake_minimum_required(VERSION 3.12)
project(microRobotFramework 
    VERSION 1.0.0
    DESCRIPTION "Micro Robot Framework for Autonomous Robots"
    LANGUAGES CXX
)

# C++ 표준 설정
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 빌드 타입 설정
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# 컴파일 옵션
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -Wall -Wextra")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# 출력 디렉토리 설정
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# 필수 패키지 찾기
find_package(OpenCV REQUIRED)
find_package(Threads REQUIRED)

# OpenCV 버전 확인
if(OpenCV_VERSION VERSION_LESS "4.0")
    message(FATAL_ERROR "OpenCV 4.0 or higher is required")
endif()

# 전역 포함 디렉토리
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/common/include)

# 공통 라이브러리 빌드
add_subdirectory(common)

# 옵션 설정
option(BUILD_CAMERA_MODULES "Build camera-related modules" ON)
option(BUILD_SERIAL_MODULES "Build serial communication modules" ON)
option(BUILD_TCP_MODULES "Build TCP networking modules" ON)
option(BUILD_FRAMEWORK_MODULES "Build framework modules" ON)
option(BUILD_EXAMPLES "Build example applications" ON)
option(BUILD_TESTS "Build test applications" OFF)

# 모듈별 빌드
if(BUILD_CAMERA_MODULES)
    add_subdirectory(101_caemra_thread)
    add_subdirectory(102_camera_serial_thread)
endif()

if(BUILD_TCP_MODULES)
    add_subdirectory(104_tcp_socket_image)
endif()

if(BUILD_SERIAL_MODULES AND BUILD_CAMERA_MODULES AND BUILD_TCP_MODULES)
    add_subdirectory(105_serial_camera_tcp_thread)
endif()

if(BUILD_FRAMEWORK_MODULES)
    add_subdirectory(106_robot_micro_framework)
    add_subdirectory(microRobotFramework_01)
    add_subdirectory(microRobotFramework_02)
    add_subdirectory(microRobotFramework_03)
    add_subdirectory(microRobotFramework_04)
endif()

# 설치 설정
install(DIRECTORY common/include/ DESTINATION include/microRobotFramework)

# 패키지 설정
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/microRobotFrameworkConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/microRobotFrameworkConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/microRobotFrameworkConfig.cmake"
    INSTALL_DESTINATION lib/cmake/microRobotFramework
)

# 정보 출력
message(STATUS "")
message(STATUS "==================================================")
message(STATUS "microRobotFramework Build Configuration")
message(STATUS "==================================================")
message(STATUS "Version: ${PROJECT_VERSION}")
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "OpenCV Version: ${OpenCV_VERSION}")
message(STATUS "")
message(STATUS "Build Options:")
message(STATUS "  BUILD_CAMERA_MODULES: ${BUILD_CAMERA_MODULES}")
message(STATUS "  BUILD_SERIAL_MODULES: ${BUILD_SERIAL_MODULES}")
message(STATUS "  BUILD_TCP_MODULES: ${BUILD_TCP_MODULES}")
message(STATUS "  BUILD_FRAMEWORK_MODULES: ${BUILD_FRAMEWORK_MODULES}")
message(STATUS "  BUILD_EXAMPLES: ${BUILD_EXAMPLES}")
message(STATUS "  BUILD_TESTS: ${BUILD_TESTS}")
message(STATUS "==================================================")
message(STATUS "")
