# 공통 라이브러리 빌드
cmake_minimum_required(VERSION 3.12)

# 공통 소스 파일들
set(COMMON_SOURCES
    src/SerialCommunication.cpp
    src/CameraManager.cpp
    src/TcpSocketManager.cpp
    src/ThreadManager.cpp
    src/RobotController.cpp
    src/ImageProcessor.cpp
    src/Logger.cpp
    src/ConfigManager.cpp
)

# 공통 헤더 파일들
set(COMMON_HEADERS
    include/SerialCommunication.h
    include/CameraManager.h
    include/TcpSocketManager.h
    include/ThreadManager.h
    include/RobotController.h
    include/ImageProcessor.h
    include/Logger.h
    include/ConfigManager.h
    include/CommonTypes.h
)

# 공통 라이브러리 생성
add_library(microRobotCommon STATIC ${COMMON_SOURCES} ${COMMON_HEADERS})

# 라이브러리 링크
target_link_libraries(microRobotCommon
    ${OpenCV_LIBS}
    Threads::Threads
)

# 플랫폼별 라이브러리 링크
if(WIN32)
    target_link_libraries(microRobotCommon ws2_32)
elseif(UNIX)
    target_link_libraries(microRobotCommon pthread)
endif()

# 헤더 파일 경로 설정
target_include_directories(microRobotCommon PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# 설치 설정
install(TARGETS microRobotCommon
    EXPORT microRobotFrameworkTargets
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
)

install(FILES ${COMMON_HEADERS}
    DESTINATION include/microRobotFramework
)
