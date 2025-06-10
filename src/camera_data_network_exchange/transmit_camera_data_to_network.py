"""
Capture images from camera device and send over a network connection.
"""

import cv2
import socket
import struct
import time


def main(
    host: str,
    port: int,
    camera_device_index: int,
    transmission_frequency: float,
) -> int:
    """
    Main function.
    """
    # Initialize network connection
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_instance.settimeout(10.0)

    try:
        print(f"Connecting to {host}:{port}")
        socket_instance.connect((host, port))
    except socket.timeout:
        print("Connection timed out")
        socket_instance.close()
        return -1
    except Exception as e:
        print(f"Connection error: {e}")
        socket_instance.close()
        return -2

    print("Connection successful")

    # Open camera device
    camera = cv2.VideoCapture(camera_device_index)
    
    if not camera.isOpened():
        return -3

    while True:
        # Capture image
        result, image = camera.read()

        if not result:
            print("Failed to capture image")
            continue

        # Encode image
        result, encoded_image = cv2.imencode(".jpg", image)

        if not result:
            print("Failed to encode image")
            continue
        
        data_to_send = encoded_image.tobytes()

        # Transmit image
        timestamp = time.time()
        length = len(data_to_send)

        header = struct.pack(
            ">dI",  # Big endian (network endianess), float64, uint32
            timestamp,
            length,
        )

        payload = header + data_to_send
        socket_instance.sendall(payload)

        delay = float(1 / transmission_frequency)
        time.sleep(delay)

    return 0

if __name__ == "__main__":
    host = "192.168.194.44" # replace with server IP address
    port = 65432
    device_index = 0 # replace if needed with index
    transmission_frequency = 60.0

    result_main = main(host, port, device_index, transmission_frequency)

    if result_main < 0:
        print(f"ERROR: Status code {result_main}")

    print("Done!")
