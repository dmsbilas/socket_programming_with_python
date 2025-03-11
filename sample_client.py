import socket

REMOTE_SERVER_IP = "103.56.89.10"  # Change this to your server's IP
REMOTE_PORT = 65432
PASSWORD = "secure123"
TEXT_MESSAGE = "Hello, this is a secure message!"
FILE_PATH = "/Users/abuhaidersiddiq/codes/playground/socket_communication/3mb.HEIC"  # Change this to the file you want to send

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((REMOTE_SERVER_IP, REMOTE_PORT))

# Send password for authentication
client.sendall(PASSWORD.encode())

# Receive authentication result
auth_response = client.recv(1024).decode()
if auth_response != "AUTH_SUCCESS":
    print("Authentication Failed!")
    client.close()
    exit()

# Send text message
client.sendall(TEXT_MESSAGE.encode())
text_message_response = client.recv(1024).decode()
print(text_message_response)

# Send file name
file_name = FILE_PATH.split("/")[-1]
client.sendall(file_name.encode())

# Receive file name response
file_name_response = client.recv(1024).decode()
print(file_name_response)

# Send file data
with open(FILE_PATH, "rb") as file:
    while chunk := file.read(1024):
        client.sendall(chunk)

print("Text and File sent successfully!")
client.close()