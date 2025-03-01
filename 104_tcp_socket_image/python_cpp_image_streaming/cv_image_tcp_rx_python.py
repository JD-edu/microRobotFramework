import socket
import struct
import numpy as np
import cv2

SERVER_IP = "192.168.35.110"  # Change to server's IP
SERVER_PORT = 8080

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

print("Connected to server!")

try:
    while True:
        # Receive image size (4 bytes - integer)
        data = client_socket.recv(4)
        if not data:
            break
        img_size = struct.unpack("!I", data)[0]  # Convert from network byte order
        print(1)
        # Receive image data
        buffer = b""
        while len(buffer) < img_size:
            packet = client_socket.recv(img_size - len(buffer))
            if not packet:
                break
            buffer += packet
        print(2)
        # Decode the image
        np_array = np.frombuffer(buffer, dtype=np.uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        print(3)
        if frame is None:
            print("Error: Failed to decode image")
            break
        print(4)
        # Display the image
        cv2.imshow("Received Image", frame)
        print(f"Received image of size: {img_size} bytes")
        print(5)
        # Exit if 'q' is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
    cv2.destroyAllWindows()
