#ifndef COMMON_TYPES_H
#define COMMON_TYPES_H

#include <opencv2/opencv.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <string>
#include <vector>
#include <memory>

namespace microRobot {
    
    // 공통 타입 정의
    using ImageType = cv::Mat;
    using ThreadType = std::thread;
    using MutexType = std::mutex;
    using AtomicBool = std::atomic<bool>;
    
    // 로봇 상태 열거형
    enum class RobotState {
        IDLE,
        RUNNING,
        PAUSED,
        ERROR,
        SHUTDOWN
    };
    
    // 통신 상태 열거형
    enum class CommStatus {
        DISCONNECTED,
        CONNECTING,
        CONNECTED,
        ERROR
    };
    
    // 설정 구조체
    struct RobotConfig {
        std::string serial_port;
        int baud_rate;
        int tcp_port;
        std::string tcp_host;
        int camera_index;
        int frame_width;
        int frame_height;
        int frame_rate;
    };
    
    // 센서 데이터 구조체
    struct SensorData {
        double timestamp;
        float temperature;
        float humidity;
        float battery_voltage;
        int encoder_left;
        int encoder_right;
    };
    
    // 이미지 데이터 구조체
    struct ImageData {
        ImageType image;
        double timestamp;
        int sequence_number;
        bool is_valid;
    };
    
} // namespace microRobot

#endif // COMMON_TYPES_H
