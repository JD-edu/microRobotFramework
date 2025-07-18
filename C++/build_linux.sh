#!/bin/bash

echo "microRobotFramework Linux Build Script"
echo "======================================="

# 빌드 디렉토리 생성
mkdir -p build
cd build

# CMake 구성
echo "Configuring CMake..."
cmake -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_CAMERA_MODULES=ON \
    -DBUILD_SERIAL_MODULES=ON \
    -DBUILD_TCP_MODULES=ON \
    -DBUILD_FRAMEWORK_MODULES=ON \
    -DBUILD_EXAMPLES=ON \
    ..

if [ $? -ne 0 ]; then
    echo "CMake configuration failed!"
    exit 1
fi

# 빌드 실행
echo "Building project..."
make -j$(nproc)

if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi

# 설치 (선택사항)
echo "Installing..."
sudo make install

echo "Build completed successfully!"
