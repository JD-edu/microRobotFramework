/*
g++ -std=c++11 -pthread -o camera_serial_thread camera_serial_thread.cpp -I/usr/local/include/opencv4 -L/usr/local/lib -lopencv_core -lopencv_videoio -lopencv_highgui -lopencv_imgcodecs -lopencv_imgproc
*/
#include <thread>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <atomic>
#include <fcntl.h>  // File control for serial
#include <unistd.h> // POSIX API for serial
#include <termios.h> // Serial settings

std::atomic<bool> running(true);
std::mutex frameMutex;
cv::Mat sharedFrame;

// Serial Port Settings (Modify accordingly)
const char* SERIAL_PORT = "/dev/ttyUSB0";
int serial_fd;

// Function to initialize serial communication
bool initSerial(const char* port) {
    serial_fd = open(port, O_RDWR | O_NOCTTY);
    if (serial_fd == -1) {
        std::cerr << "Failed to open serial port!\n";
        return false;
    }

    struct termios tty;
    if (tcgetattr(serial_fd, &tty) != 0) {
        std::cerr << "Error getting terminal attributes\n";
        return false;
    }

    cfsetospeed(&tty, B115200);
    cfsetispeed(&tty, B115200);
    tty.c_cflag = CS8 | CLOCAL | CREAD;
    tty.c_iflag = IGNPAR;
    tty.c_oflag = 0;
    tty.c_lflag = 0;
    tcflush(serial_fd, TCIFLUSH);
    tcsetattr(serial_fd, TCSANOW, &tty);

    return true;
}

// Function to read from serial and send data
void serialThread() {
    uint8_t buffer[12];
    while (running) {
        int n = read(serial_fd, buffer, 12);
        if (n == 12) {
            float accelX, accelY, accelZ;
            memcpy(&accelX, buffer, 4);
            memcpy(&accelY, buffer + 4, 4);
            memcpy(&accelZ, buffer + 8, 4);

            std::cout << std::fixed << std::setprecision(3);
            std::cout << "Accel X: " << accelX 
                      << ", Y: " << accelY 
                      << ", Z: " << accelZ << std::endl;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    close(serial_fd);
}

void cameraThread() {
    cv::VideoCapture cap(0); // Open default camera
    if (!cap.isOpened()) {
        std::cerr << "Error: Couldn't open camera\n";
        running = false;
        return;
    }

    while (running) {
        cv::Mat frame;
        //cap >> frame;
        bool ret = cap.read(frame);
        if (frame.empty()) continue;

        {
            std::lock_guard<std::mutex> lock(frameMutex);
            sharedFrame = frame.clone();
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(30));
    }
}

void displayThread() {
    while (running) {
        cv::Mat frame;
        //{
            std::lock_guard<std::mutex> lock(frameMutex);
            if (!sharedFrame.empty()) {
                frame = sharedFrame.clone();
            }
        //}

        if (!frame.empty()) {
            cv::imshow("Camera Feed", frame);
        }

        if (cv::waitKey(10) == 27) { // Press 'ESC' to exit
            running = false;
        }
    }
}

int main(){

    if (!initSerial(SERIAL_PORT)) return -1;

    std::thread camThread(cameraThread);
    std::thread displayCamThread(displayThread);
    std::thread serialComThread(serialThread);
    camThread.join();
    displayCamThread.join();
    serialComThread.join();
    return 0;

}
