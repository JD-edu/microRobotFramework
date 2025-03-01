#include <opencv2/opencv.hpp>
#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_PORT 8080

int main() {
    // OpenCV: Capture image from webcam
    cv::Mat frame;
    cv::VideoCapture cap(0);  // 0 = default webcam

    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open webcam" << std::endl;
        return -1;
    }

    // Create server socket
    int server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock < 0) {
        std::cerr << "Error: Could not create socket" << std::endl;
        return -1;
    }

    // Define server address
    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(SERVER_PORT);

    // Bind socket
    if (bind(server_sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Error: Bind failed" << std::endl;
        close(server_sock);
        return -1;
    }

    // Listen for connections
    if (listen(server_sock, 1) < 0) {
        std::cerr << "Error: Listen failed" << std::endl;
        close(server_sock);
        return -1;
    }

    std::cout << "Waiting for client connection..." << std::endl;

    // Accept client connection
    sockaddr_in client_addr{};
    socklen_t client_len = sizeof(client_addr);
    int client_sock = accept(server_sock, (struct sockaddr*)&client_addr, &client_len);
    if (client_sock < 0) {
        std::cerr << "Error: Client connection failed" << std::endl;
        close(server_sock);
        return -1;
    }

    std::cout << "Client connected!" << std::endl;

    while (true) {
        cap >> frame;  // Capture frame
        if (frame.empty()) break;

        // Encode image as a byte stream
        std::vector<uchar> buffer;
        cv::imencode(".jpg", frame, buffer);
        int img_size = buffer.size();

        // Send image size first
        if (send(client_sock, &img_size, sizeof(img_size), 0) <= 0) break;

        // Send image data
        if (send(client_sock, buffer.data(), img_size, 0) <= 0) break;

        std::cout << "Sent image of size: " << img_size << " bytes" << std::endl;

        // Exit if 'q' is pressed
        if (cv::waitKey(30) == 'q') break;
    }

    // Cleanup
    close(client_sock);
    close(server_sock);
    return 0;
}
