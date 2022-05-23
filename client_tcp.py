import sys
import socket
import time


server_name = sys.argv[1]
port = int(sys.argv[2])
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_name, port))
file_byte = 0
buffer = 65536


# ----------- Commands ---------------- #
def chunk():
    global file_byte
    # Read the txt file as a binary file and determine the size of the byte stream
    file_name = command_split[1]
    file_open = open(file_name, "rb")  # open text file in bytes
    file = file_open.read()  # read byte stream
    file_byte = len(file)
    chunk_size = 1000  # chunk size of 1000
    return [file[x:x + chunk_size] for x in range(0, file_byte + 1, chunk_size)]


def get():
    anon_message = client_socket.recv(buffer).decode()
    anon_file_name = command_split[1]
    file = open(anon_file_name, "w")
    file.writelines(anon_message)


def keyword():
    word = command_split[1]
    client_socket.send(word.encode())


def terminate():
    global stop
    stop = True


def server_message():
    server_response = client_socket.recv(buffer).decode()
    print("Server response: {}".format(server_response))


stop = False
while not stop:
    # -- put test.txt, keyword Fall test.txt, get test_anon.txt, quit --- #
    command = input("Enter Command: ")
    command_split = command.split()
    if command_split[0].lower() == "put":
        message_chunks = chunk()
        length_message = "LEN:{} Bytes".format(file_byte).encode()
        client_socket.send(length_message)
        time.sleep(0.05)
        for num in range(0, len(message_chunks)):
            client_socket.send(message_chunks[num])
        server_message()
        client_socket.send(command_split[1].encode())
    elif command_split[0].lower() == "keyword":
        keyword()
        server_message()
    elif command_split[0].lower() == "get":
        get()
        print("File {} downloaded.".format(command_split[1]))
    elif command_split[0].lower() == "quit":
        terminate()
        print("Exiting program!")
    else:
        print("Enter a valid command")
