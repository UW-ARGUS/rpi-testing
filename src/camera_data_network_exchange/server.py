# server_struct.py
import socket
import struct
import numpy as np
import cv2

HOST = '0.0.0.0'
PORT = 65432

def recv_exact(sock, num_bytes):
    """Receive exact number of bytes"""
    data = b''
    while len(data) < num_bytes:
        packet = sock.recv(num_bytes - len(data))
        if not packet:
            raise ConnectionError("Socket closed before expected data received.")
        data += packet
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[+] Listening on {HOST}:{PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"[+] Connected by {addr}")

        # Receive header
        header = recv_exact(conn, 12)  # 8 bytes for double, 4 for uint32
        timestamp, length = struct.unpack('>dI', header)
        print("[+] Received timestamp:", timestamp)
        print("[+] Expecting", length, "bytes of image data")

        # Receive image data
        image_data = recv_exact(conn, length)

        # Decode image
        img_array = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if image is not None:
            cv2.imshow("Received Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("[-] Failed to decode image.")
