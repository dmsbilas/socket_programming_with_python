import socket
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432
BUFFER_SIZE = 4096

def upload_file(filename):
    if not os.path.exists(f"./image_source/{filename}"):
        print("File does not exist!")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.send(f"UPLOAD {filename}".encode())
        with open(f"./image_source/{filename}", "rb") as f:
            while (chunk := f.read(BUFFER_SIZE)):
                sock.send(chunk)
        print(f"Uploaded {filename} successfully.")

def download_file(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.send(f"DOWNLOAD {filename}".encode())
        with open(f"./download/{filename}", "wb") as f:
            while True:
                data = sock.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
        print(f"Downloaded {filename}.")

if __name__ == "__main__":
    # Choose either upload or download
    upload_file("1.jpg")
    download_file("1.jpg")
