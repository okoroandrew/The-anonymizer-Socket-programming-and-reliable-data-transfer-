import sys
import socket
import time


server_name = ""
port = int(sys.argv[1])
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_name, port))
server_socket.listen(5)
print("Server is listening")
server_socket, address = server_socket.accept()
buffer = 65536
message_chunks = []
received_byte = 0


def anonymize_keyword(key_word, content):
    length = len(key_word)
    replace_with = length * "X"
    content = " ".join(content)
    return content.replace(key_word, replace_with)


len_message = server_socket.recv(1024)  # server receiver the len message
len_message = len_message.decode()
print(len_message)
total_byte = len_message.split(":")[1].split(" ")[0]
print(total_byte)
time.sleep(0.05)

while True:
    if received_byte < int(total_byte):
        message = server_socket.recv(1024).decode()         # server receives message
        message_chunks.append(message)
        received_byte = sum([len(item) for item in message_chunks])

    if received_byte == int(total_byte):
        server_socket.send("File uploaded".encode())        # server sends an ack

        file_name = server_socket.recv(1024).decode()       # server receives file name
        file_name_anon = file_name.split(".")[0]+"_anon.txt"

        keyword = server_socket.recv(1024).decode()         # server receives keyword
        message_refined = anonymize_keyword(keyword, message_chunks)               # server anonymize keyword

        server_socket.send("File {} anonymize. Output file is {}".format(file_name, file_name_anon).encode())
        time.sleep(0.01)
        server_socket.send(message_refined.encode())        # server sends back anon message

        break
