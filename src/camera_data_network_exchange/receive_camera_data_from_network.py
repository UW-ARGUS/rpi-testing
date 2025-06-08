"""
Receive and display images from a network connection.
"""

import cv2
import socket
import struct

import numpy as np

HEADER_LENGTH = 12

def main(host: str, port: int) -> int:
    """
    Main function.
    """
    # Initialize network connection
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.bind((host, port))
    socket_instance.listen()
    print(f"Listening on {host}:{port}")

    connection, address = socket_instance.accept()
    print(f"Connected by address {address}")

    # Receive header from network
    while True:
        header = b""
        while len(header) < HEADER_LENGTH:
            packet = connection.recv(HEADER_LENGTH - len(header))

            if not packet:
                print("Invalid header data")
                return -1

            header += packet

        timestamp, image_data_length = struct.unpack(
            ">dI",  # Big endian (network endiannes), float64, uint32
            header,
        )

        # Receive image data from network 
        image_data = b""
        while len(image_data) < image_data_length:
            packet = connection.recv(image_data_length - len(image_data))

            if not packet:
                print("Invalid image data")
                return -2

            image_data += packet

        image_array = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if image is not None:
            cv2.putText(
                image,
                f"{timestamp:.3f}",
                (10, 20),  # Top-left corner
                cv2.FONT_HERSHEY_SIMPLEX,  # Font type
                0.5, # Font size
                (255, 0, 255),  # Fuschia
                1,
            )  # Line thickness

            cv2.imshow(f"Image display", image)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting image display")
                break
        else:
            print("Failed to decode image")

    cv2.destroyAllWindows()
    
    return 0

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 65432

    result_main = main(host, port)

    if result_main < 0:
        print(f"ERROR: Status code {result_main}")

    print("Done!")
