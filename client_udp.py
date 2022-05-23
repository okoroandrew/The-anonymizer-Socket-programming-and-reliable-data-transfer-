import socket
import sys
import time

server_name = sys.argv[1]
server_port = int(sys.argv[2])
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create the UDP socket
stop = False
anon_text = []
command_split = []
file_byte = 0


def chunk():
    global file_byte
    # Read the txt file as a binary file and determine the size of the byte stream
    file_name = command_split[1]
    file_open = open(file_name, "rb")  # open text file in bytes
    file = file_open.read()  # read byte stream
    file_byte = len(file)
    chunk_size = 1000  # chunk size of 1000
    return [file[x:x + chunk_size] for x in range(0, file_byte + 1, chunk_size)]


def get(message):
    anon_file_name = command_split[1]
    file_obj = open(anon_file_name, "w")
    message_string = " ".join(item.decode() for item in message)
    file_obj.writelines(message_string)


def keyword():
    keyword_command = input("Enter Command: ")
    word = keyword_command.split()[1]
    client_socket.sendto(word.encode(), (server_name, server_port))


def terminate():
    global stop
    stop = True


def server_message():
    server_response, address = client_socket.recvfrom(1024)
    print("Server response: {}".format(server_response.decode()))


def main():
    global command_split
    received_anon_bytes = 0
    time_ack_sent = 0
    anon_message_chunks = []
    while not stop:
        # -- put test.txt, keyword Fall test.txt, get test_anon.txt, quit --- #
        command = input("Enter Command: ")
        command_split = command.split()
        if command_split[0].lower() == "put":
            message_chunks = chunk()
            length_message = "LEN:{} Bytes".format(file_byte).encode()
            client_socket.sendto(length_message, (server_name, server_port))
            for num in range(0, len(message_chunks)):
                client_socket.sendto(message_chunks[num], (server_name, server_port))
                try:
                    client_socket.settimeout(1)
                    ack_message, server_address = client_socket.recvfrom(1024)  # receive message from sender
                    print("message_chunk[{}]: ".format(num), ack_message.decode())
                except socket.timeout:
                    print("Did not receive ACK. Terminating")
                    return
            print("Awaiting server response.")
            client_socket.sendto(command_split[1].encode(), (server_name, server_port))
            fin_message, __ = client_socket.recvfrom(1024)         # Receive FIN
            if fin_message:
                print("Server response: {}".format(fin_message.decode()))
                keyword()
                print("Awaiting server response.")
                server_message()
            else:
                break
        elif command_split[0].lower() == "get":
            len_message, __ = client_socket.recvfrom(1024)
            time_len_message = time.time()
            len_message = len_message.decode()
            print(len_message)
            total_anon_file_byte = len_message.split(":")[1].split(" ")[0]
            while True:
                if received_anon_bytes < int(total_anon_file_byte):
                    message, address = client_socket.recvfrom(1024)  # receive from client
                    time_chunk_receive = time.time()
                    if time_chunk_receive - time_len_message > 1 and not anon_message_chunks:
                        print("Did not receive data. Terminating.")
                        terminate()
                    if anon_message_chunks:
                        if time_chunk_receive > time_ack_sent + 1:
                            print("Data transmission terminated prematurely.")
                            terminate()
                    anon_message_chunks.append(message)
                    received_anon_bytes = sum([len(item) for item in anon_message_chunks])
                    client_socket.sendto("ACK".encode(), (server_name, server_port))
                    time_ack_sent = time.time()
                if received_anon_bytes >= int(total_anon_file_byte):
                    client_socket.sendto("FIN".encode(), (server_name, server_port))
                    get(anon_message_chunks)
                    print("File {} downloaded.".format(command_split[1]))
                    break
        elif command_split[0].lower() == "quit":
            print("Exiting program!")
            terminate()
        else:
            print("Enter a valid command")

    client_socket.close()
    pass


if __name__ == "__main__":
    main()
