/*
g++ -std=c++11 -pthread -o socket_image_serial_thread cv_image_tcp_serial_thread.cpp -I/usr/local/include/opencv4 -L/usr/local/lib -lopencv_core -lopencv_videoio -lopencv_highgui -lopencv_imgcodecs -lopencv_imgproc
*/
#include <iostream>
#include <thread>
#include <vector>
#include <opencv2/opencv.hpp>
#include <boost/asio.hpp>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_PORT 8080
#define SERIAL_PORT "/dev/ttyUSB0"  // Change this to match your Arduino's serial port
#define BAUD_RATE 115200

//using namespace boost::asio;
int serial_fd;

// Serial communication function
void serialThread() {
    std::cout << "Serial start ... \n";
    try {
        serial_fd = open(SERIAL_PORT, O_RDWR | O_NOCTTY);

        if (serial_fd == -1) {
            std::cerr << "Failed to open serial port!\n";
        }
         
        struct termios tty;
        if (tcgetattr(serial_fd, &tty) != 0) {
            std::cerr << "Error getting terminal attributes\n";
        }
      
        cfsetospeed(&tty, B115200);
        cfsetispeed(&tty, B115200);
        tty.c_cflag = CS8 | CLOCAL | CREAD;
        tty.c_iflag = IGNPAR;
        tty.c_oflag = 0;
        tty.c_lflag = 0;
        tcflush(serial_fd, TCIFLUSH);
        tcsetattr(serial_fd, TCSANOW, &tty);
        uint8_t buffer[12];
        while (true) {
            /*
            // Send data to Arduino
            std::string msg = "Hello Arduino\n";
            write(serial, buffer(msg));

            // Read response from Arduino
            char buf[256];
            size_t n = read(serial, buffer(buf, sizeof(buf) - 1));
            buf[n] = '\0';  // Null-terminate the received string
            std::cout << "[Serial] Received: " << buf << std::endl;

            std::this_thread::sleep_for(std::chrono::seconds(1));  // 1-second delay
            */
           
            int n = read(serial_fd, buffer, 6);
            if (n == 6) {
                int16_t accelX, accelY, accelZ;
                memcpy(&accelX, buffer, 2);
                memcpy(&accelY, buffer + 2, 2);
                memcpy(&accelZ, buffer + 4, 2);

                //std::cout << std::fixed << std::setprecision(3);
                std::cout << "roll: " << accelX 
                        << ", pitch: " << accelY 
                        << ", yaw: " << accelZ << std::endl;
            }

            std::this_thread::sleep_for(std::chrono::milliseconds(50));
        }
    } catch (std::exception& e) {
        std::cerr << "Serial Error: " << e.what() << std::endl;
    }
}

// Socket server function
void socketServerThread() {
    int server_sock, client_sock;
    struct sockaddr_in server_addr{}, client_addr{};
    socklen_t client_len = sizeof(client_addr);

    // Create socket
    server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock < 0) {
        std::cerr << "Socket creation failed" << std::endl;
        return;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(SERVER_PORT);

    // Bind socket
    if (bind(server_sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Bind failed" << std::endl;
        close(server_sock);
        return;
    }

    // Listen for clients
    if (listen(server_sock, 1) < 0) {
        std::cerr << "Listen failed" << std::endl;
        close(server_sock);
        return;
    }

    std::cout << "[Socket] Waiting for client connection..." << std::endl;
    client_sock = accept(server_sock, (struct sockaddr*)&client_addr, &client_len);
    if (client_sock < 0) {
        std::cerr << "Client connection failed" << std::endl;
        close(server_sock);
        return;
    }

    std::cout << "[Socket] Client connected!" << std::endl;

    // OpenCV camera capture
    cv::VideoCapture cap(0);  // Open default camera
    if (!cap.isOpened()) {
        std::cerr << "Camera failed to open" << std::endl;
        close(client_sock);
        close(server_sock);
        return;
    }

    while (true) {
        cv::Mat frame;
        cap >> frame;
        if (frame.empty()) break;

        // Encode image
        std::vector<uchar> buffer;
        cv::imencode(".jpg", frame, buffer);
        int img_size = buffer.size();

        // Send image size
        int img_size_net = htonl(img_size);
        if (send(client_sock, &img_size_net, sizeof(img_size_net), 0) <= 0) break;

        // Send image data
        if (send(client_sock, buffer.data(), img_size, 0) <= 0) break;

        //std::cout << "[Socket] Sent image of size: " << img_size << " bytes" << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));  // Small delay
    }

    close(client_sock);
    close(server_sock);
}

int main() {
    std::thread t1(serialThread);
    std::thread t2(socketServerThread);

    t1.join();
    t2.join();

    return 0;
}
