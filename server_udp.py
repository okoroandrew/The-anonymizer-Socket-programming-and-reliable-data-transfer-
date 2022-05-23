import socket
import sys
import time


server_name = ""
port_number = int(sys.argv[1])
done = False
message_chunks = []


def anonymize_keyword(keyword, chunks):
    """ """
    length = len(keyword)
    replace_with = length * "X"
    message = " ".join([(item.decode()) for item in chunks])
    return message.replace(keyword, replace_with)


# --------- terminate function ---------- #
def terminate():
    global done
    done = True
    pass


# ------- Server function --------------- #
def server():
    global done
    received_bytes = 0
    time_ack_sent = 0
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_name, port_number))
    print("server is running")

    len_message, address = server_socket.recvfrom(1024)  # server receiver the len message
    time_len_message = time.time()
    len_message = len_message.decode()
    print(len_message)
    total_file_byte = len_message.split(":")[1].split(" ")[0]

    while not done:
        if received_bytes < int(total_file_byte):
            message, address = server_socket.recvfrom(1024)  # receive from client
            time_chunk_receive = time.time()
            if time_chunk_receive > time_len_message + 1 and not message_chunks:
                print("Did not receive data. Terminating.")
                terminate()
            if message_chunks:
                if time_chunk_receive > time_ack_sent + 1:
                    print("Data transmission terminated prematurely.")
                    terminate()
            message_chunks.append(message)
            received_bytes = sum([len(item) for item in message_chunks])

            server_socket.sendto("ACK".encode(), address)
            time_ack_sent = time.time()

        if received_bytes >= int(total_file_byte):
            f_name, __ = server_socket.recvfrom(1024)
            f_name = f_name.decode()
            f_name_anon = f_name.split(".")[0] + "_anon.txt"

            server_socket.sendto("FIN, File uploaded".encode(), address)

            keyword, address = server_socket.recvfrom(1024)
            anon_message = anonymize_keyword(keyword.decode(), message_chunks)

            server_socket.sendto("File {} anonymized. Output file is {}".format(f_name, f_name_anon).encode(), address)

            # -------- send Anon message chunk by chunk --------#
            total_anon_file_byte = len(bytes(anon_message, "utf-8"))
            chunk_size = 1000               # chunk size should be 1000
            length_anon_message = "LEN:{} Bytes".format(total_anon_file_byte)
            server_socket.sendto(length_anon_message.encode(), address)
            anon_message_chunks = [anon_message[x:x + chunk_size] for x in range(0, total_anon_file_byte + 1, chunk_size)]
            for num in range(0, len(anon_message_chunks)):
                server_socket.sendto(anon_message_chunks[num].encode(), address)
                try:
                    if num > 0:
                        server_socket.settimeout(1)
                    ack_message, __ = server_socket.recvfrom(1024)  # receive message from sender
                    print("anon_chunk[{}]: ".format(num), ack_message.decode())
                except socket.timeout:
                    print("Did not receive ACK. Terminating")
                    return
            fin_message, server_address = server_socket.recvfrom(1024)
            if fin_message:
                print(fin_message.decode())
                terminate()
    server_socket.close()
    print('server down')
    pass


if __name__ == "__main__":
    server()
