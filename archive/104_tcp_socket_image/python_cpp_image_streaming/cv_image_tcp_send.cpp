#include <opencv2/opencv.hpp>
#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_PORT 8080

int main() {
    cv::Mat frame;
    cv::VideoCapture cap(0);  // Open the webcam

    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open webcam" << std::endl;
        return -1;
    }

    int server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock < 0) {
        std::cerr << "Error: Could not create socket" << std::endl;
        return -1;
    }

    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(SERVER_PORT);

    if (bind(server_sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Error: Bind failed" << std::endl;
        close(server_sock);
        return -1;
    }

    if (listen(server_sock, 1) < 0) {
        std::cerr << "Error: Listen failed" << std::endl;
        close(server_sock);
        return -1;
    }

    std::cout << "Waiting for client connection..." << std::endl;

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
        cap >> frame;
        if (frame.empty()) break;

        std::vector<uchar> buffer;
        cv::imencode(".jpg", frame, buffer);
        int img_size = buffer.size();

        // Convert image size to network byte order (htonl ensures compatibility)
        int img_size_net = htonl(img_size);
        
        // Send image size (4 bytes)
        if (send(client_sock, &img_size_net, sizeof(img_size_net), 0) <= 0) break;

        // Send image data
        if (send(client_sock, buffer.data(), img_size, 0) <= 0) break;

        std::cout << "Sent image of size: " << img_size << " bytes" << std::endl;

        if (cv::waitKey(30) == 'q') break;
    }

    close(client_sock);
    close(server_sock);
    return 0;
}
