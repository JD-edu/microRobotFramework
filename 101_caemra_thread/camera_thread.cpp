/*
g++ -std=c++11 -pthread -o camera_thread camera_thread.cpp -I/usr/local/include/opencv4 -L/usr/local/lib -lopencv_core -lopencv_videoio -lopencv_highgui -lopencv_imgcodecs -lopencv_imgproc
*/
#include <thread>
#include <opencv2/opencv.hpp>
#include <iostream>
#include <atomic>

std::atomic<bool> running(true);
std::mutex frameMutex;
cv::Mat sharedFrame;

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

    std::thread camThread(cameraThread);
    std::thread displayCamThread(displayThread);

    camThread.join();
    displayCamThread.join();
    return 0;

}
