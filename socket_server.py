import socket
import os

HOST = '0.0.0.0'
PORT = 65432
BUFFER_SIZE = 4096

def handle_client(conn):
    command = conn.recv(BUFFER_SIZE).decode()
    if command.startswith("UPLOAD"):
        filename = command.split()[1]
        with open("upload/" + filename, "wb") as f:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
        print(f"File {filename} uploaded successfully.")

    elif command.startswith("DOWNLOAD"):
        filename = command.split()[1]
        if not os.path.exists("upload/" + filename):
            conn.send(b"ERROR: File not found")
            return
        with open("upload/" + filename, "rb") as f:
            while (chunk := f.read(BUFFER_SIZE)):
                conn.send(chunk)
        print(f"File {filename} sent to client.")

    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()
