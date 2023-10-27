import os
import socket
import threading

host = None
port = None
server_socket = None
currentDir = ""


# Create Socket
def create_socket():
    global host, port, server_socket

    host = ""
    port = 8888

    try:
        # Create socket and set options
        print("Creating and binding socket...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Socket create error: ")
        print(str(msg))


# Bind Socket
def bind_socket():
    global host, port, server_socket

    try:
        # Connect to socket, print connection status
        server_socket.bind((host, port))
        print("Socket created & binded.")
    except socket.error as msg:
        print("Socket bind error: ")
        print(str(msg))


# Close socket
def close_socket():
    try:
        server_socket.close()
        print("Socket closed.")
    except socket.error as msg:
        print("Socket closing error: ")
        print(str(msg))


def tcp_server():
    global server_socket, port

    create_socket()
    bind_socket()

    # Listening for incomming connections
    server_socket.listen(1)

    while True:
        print("***************************************")
        print("Waiting for client, listening on port " + str(port))

        try:
            # create new socket for client connection
            connection_socket, addr = server_socket.accept()
            print("Connection socket created.")

            # Open a new thread for the client
            print("Creating new thread for client...")
            x = threading.Thread(
                target=client_thread,
                args=(
                    connection_socket,
                    addr,
                ),
            )
            x.setDaemon(True)
            x.start()
            print("Thread created for client.")

        except socket.error as e:
            print("Threading error")

    close_socket()


def client_thread(connection_socket, addr):
    print("Connected to client --> IP: " + str(addr[0]) + " | Port: " + str(addr[1]))
    try:
        raw_packet = connection_socket.recv(1024)

        packet = raw_packet.decode("utf-8").split(" ")

        if packet[0] == "send":
            cmd_send(packet)
        elif packet[0] == "retr":
            cmd_retr(packet, connection_socket)
        elif packet[0] == "list":
            cmd_list(connection_socket)
        elif packet[0] == "stor":
            cmd_stor(packet, connection_socket)
        elif packet[0] == "remv":
            cmd_remv(packet, connection_socket)
        elif packet[0] == "mdir":
            cmd_mdir(packet, connection_socket)
        elif packet[0] == "cd":
            cmd_cd(packet, connection_socket)
        else:
            print("command unrecognized")

        # Close the connection socket
        connection_socket.close()
    except socket.error as msg:
        print("Socket closing error: ")
        print(str(msg))


def cmd_retr(packet, connection_socket):
    # Receive file name
    file_name = packet[1]
    print(file_name)

    try:
        # Open and read file
        file = open(file_name, "rb")

        # Send file to client
        connection_socket.send(file.read())

        # Flush out the transport layer buffer
        connection_socket.shutdown(socket.SHUT_WR)

        # Close file
        file.close()

    except FileNotFoundError as e:
        print(str(e))


def cmd_stor(packet, connection_socket):
    file_name = packet[1]
    print("Storing " + file_name + "...")

    try:
        # Open a new file
        file = open(file_name, "wb")

        # Receive file from server
        print("Receiving file...")
        recv_file = connection_socket.recv(1024)
        while recv_file:
            file.write(recv_file)
            recv_file = connection_socket.recv(1024)

        print("File received.")

        # Flush out the transport layer buffer
        connection_socket.shutdown(socket.SHUT_WR)

        # Close new file
        file.close()

    except FileExistsError as e:
        print(str(e))


def cmd_list(connection_socket):
    # Get the list of files
    file_list = os.listdir()
    print("Files currently on the server:")
    print(file_list)

    # Send the file list to the client
    connection_socket.send(str(file_list).encode("utf-8"))

    # Flush out the transport layer buffer
    connection_socket.shutdown(socket.SHUT_WR)


def cmd_send(packet):
    print(packet[1])


def cmd_remv(packet, connection_socket):
    file_name = packet[1]

    try:
        # Removing file from the server
        print("Removing " + file_name + "...")
        os.remove(file_name)
        print("File removed.")

        # Flush out the transport layer buffer
        connection_socket.shutdown(socket.SHUT_WR)

    except FileExistsError as e:
        print(str(e))


def cmd_mdir(packet, connection_socket):
    dir_name = packet[1]

    try:
        print("Creating directory " + dir_name + "...")
        os.mkdir(dir_name)
        print("Directory created")

    except FileExistsError:
        print("Directory {} already exists".format(dir_name))


def cmd_cd(packet, connection_socket):
    global currentDir

    dir_name = packet[1]

    try:
        print("Navigating to " + dir_name + "...")
        os.chdir(dir_name)
        if dir_name != "../":
            currentDir = currentDir + "/" + dir_name
        else:
            dirElements = currentDir.split("/")
            print(dirElements)
            length = len(dirElements)
            currentDir = currentDir.replace(dirElements[length - 1], "")
            currentDir = currentDir[: len(currentDir) - 1]
        print(currentDir)

        # Send the file list to the client
        connection_socket.send(str(currentDir).encode("utf-8"))

        # Flush out the transport layer buffer
        connection_socket.shutdown(socket.SHUT_WR)

    except FileExistsError:
        print("Directory {} already exists".format(dir_name))


def log_action():
    ...


# Main
if __name__ == "__main__":
    # Runs the TCP server
    tcp_server()
