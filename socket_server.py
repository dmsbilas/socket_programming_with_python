import socket
import os


# Server credentials
PASSWORD = "secure123"
HOST = "0.0.0.0"
PORT = 65432
SAVE_IMAGE_FILE = "received_image_file"  # Where to save the received file

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")

    # Receive authentication
    received_password = conn.recv(1024).decode().strip()
    
    if received_password != PASSWORD:
        conn.sendall(b"AUTH_FAILED")
        conn.close()
        continue  # Reject connection if password is wrong

    conn.sendall(b"AUTH_SUCCESS")

    # Receive text message
    text_data = conn.recv(1024).decode()
    print(f"Received text: {text_data}")

    conn.sendall(b"TEXT_RECEIVED")

    # Receive file name
    file_name = conn.recv(1024).decode()
    print(f"File name: {file_name}")
    conn.sendall(b"FILE_NAME_RECEIVED")

    # Receive file data
    with open(SAVE_IMAGE_FILE, "wb") as file:
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            file.write(chunk)
        os.rename(SAVE_IMAGE_FILE, f"{file_name}")
        print(f"File received successfully")
    
    conn.close()