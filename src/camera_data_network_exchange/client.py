# client_struct.py
import socket
import cv2
import struct
import time

HOST = '127.0.0.1'
PORT = 65432

# Capture from webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if not ret:
    print("[-] Failed to capture image.")
    exit()

# Encode image as JPEG
_, img_encoded = cv2.imencode('.jpg', frame)
image_bytes = img_encoded.tobytes()

# Prepare timestamp and length
timestamp = time.time()
length = len(image_bytes)

# Pack header: 8-byte double for timestamp, 4-byte unsigned int for length
header = struct.pack('>dI', timestamp, length)  # Big endian

# Send over TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(header + image_bytes)
    print("[+] Sent image with timestamp:", timestamp)
