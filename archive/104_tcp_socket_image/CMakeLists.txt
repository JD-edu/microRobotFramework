cmake_minimum_required(VERSION 3.12)

# 프로젝트 이름
set(PROJECT_NAME tcp_socket_image)

# 소스 파일들
file(GLOB_RECURSE SOURCES "*.cpp" "*.c")
file(GLOB_RECURSE HEADERS "*.h" "*.hpp")

# 실행 파일 생성
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# 라이브러리 링크
target_link_libraries(${PROJECT_NAME}
    microRobotCommon
    ${OpenCV_LIBS}
    Threads::Threads
)

# 네트워킹 플랫폼별 설정
if(WIN32)
    target_link_libraries(${PROJECT_NAME} ws2_32)
    target_compile_definitions(${PROJECT_NAME} PRIVATE WINDOWS_SOCKET)
elseif(UNIX)
    target_compile_definitions(${PROJECT_NAME} PRIVATE UNIX_SOCKET)
endif()

# 컴파일 정의
target_compile_definitions(${PROJECT_NAME} PRIVATE
    MODULE_NAME="TcpSocketImage"
    VERSION_MAJOR=1
    VERSION_MINOR=0
    DEFAULT_PORT=8080
)

# 설치 설정
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)
