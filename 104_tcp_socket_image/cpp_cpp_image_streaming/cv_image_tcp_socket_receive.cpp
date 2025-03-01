#include <opencv2/opencv.hpp>
#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

#define SERVER_IP "192.168.35.110"  // Change to server's IP
#define SERVER_PORT 8080

int main() {
    // Create client socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Error: Could not create socket" << std::endl;
        return -1;
    }

    // Define server address
    sockaddr_in server_addr{};
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr);

    // Connect to the server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Error: Connection failed" << std::endl;
        close(sock);
        return -1;
    }

    std::cout << "Connected to server!" << std::endl;

    while (true) {
        int img_size;
        
        // Receive image size
        if (recv(sock, &img_size, sizeof(img_size), 0) <= 0) break;

        // Receive image data
        std::vector<uchar> buffer(img_size);
        if (recv(sock, buffer.data(), img_size, 0) <= 0) break;

        // Decode image
        cv::Mat frame = cv::imdecode(buffer, cv::IMREAD_COLOR);
        if (frame.empty()) break;

        // Display image
        cv::imshow("Received Image", frame);
        std::cout << "Received image of size: " << img_size << " bytes" << std::endl;

        // Exit if 'q' is pressed
        if (cv::waitKey(30) == 'q') break;
    }

    // Cleanup
    close(sock);
    return 0;
}
