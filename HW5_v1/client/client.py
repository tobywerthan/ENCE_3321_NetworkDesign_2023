import socket

host = None
port = None
server_socket = None
auth_flag = 0
currentDir = ""


# Create Socket
def create_socket():
    global host, port, server_socket

    host = "localhost"
    port = 8888

    try:
        # Create socket and set options
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Socket create error: ")
        print(str(msg))


# Connect Socket
def connect_socket():
    global host, port, server_socket

    try:
        # Connect to socket, print connection status
        server_socket.connect((host, port))
        print("Connected to server --> IP: " + host + " | Port: " + str(port))
    except socket.error as msg:
        print("Socket connection error: ")
        print(str(msg))


# Close socket
def close_socket():
    try:
        server_socket.close()
    except socket.error as msg:
        print("Socket closing error: ")
        print(str(msg))


def tcp_client():
    while True:
        cmd = input("turtle" + currentDir + "> ")
        if auth_flag:
            if cmd == "quit":
                break
            elif cmd == "send":
                cmd_send()
            elif cmd == "help":
                cmd_help()
            elif cmd == "logout":
                cmd_logout()
            elif cmd == "retr":
                cmd_retr()
            elif cmd == "list":
                cmd_list()
            elif cmd == "stor":
                cmd_stor()
            elif cmd == "remv":
                cmd_remv()
            elif cmd == "mdir":
                cmd_mdir()
            elif cmd == "cd":
                cmd_cd()
            else:
                print("")
                print("Unrecognized command: " + cmd)
                print(
                    "List of valid turtle commands: quit, send, help, logout, retr, list, stor, remv, cd"
                )
                print("")
        else:
            if cmd == "quit":
                break
            elif cmd == "send":
                cmd_send()
            elif cmd == "help":
                cmd_help()
            elif cmd == "login":
                cmd_login()
            elif (
                cmd == "retr"
                or cmd == "list"
                or cmd == "stor"
                or cmd == "remv"
                or cmd == "mdir"
                or cmd == "cd"
            ):
                print("")
                print("Please login to access: " + cmd)
                print("")
            else:
                print("")
                print("Unrecognized command: " + cmd)
                print("List of valid turtle commands: quit, send, help, login")
                print("")


def cmd_help():
    print("")
    if auth_flag:
        print("-----------------------------------------------------------")
        print("List of valid turtle commands: ")
        print("     quit: exit the program")
        print("     help: lists valid turtle commands")
        print("     send: tests server connection")
        print("     login: login to the server")
        print("     retr: get file from current directory")
        print("     list: lists all files in the current directory")
        print("     stor: stores a new file in the current directory")
        print("     remv: removes a file the current directory")
        print("     mdir: creates a new directory based on the current directory")
        print("     cd: navigates to the specified directory")
    else:
        print("-----------------------------------------------------------")
        print("List of valid turtle commands: ")
        print("     quit: exit the program")
        print("     help: lists valid turtle commands")
        print("     send: tests server connection")
        print("     login: login")
    print("")


def cmd_login():
    global auth_flag

    print("")
    print("turtle" + currentDir + "> Login format: username password")
    username = input("turtle" + currentDir + "> ").split(" ")
    if len(username) == 2:
        if username[0] == "user" and username[1] == "password":
            print("Login success")
            auth_flag = 1
        else:
            print("Incorrect login")
    else:
        print("Incorrect login")


def cmd_logout():
    global auth_flag
    print("")
    print("Logging out...")

    auth_flag = 0

    print("Logout successful")
    print("")


def cmd_send():
    global server_socket

    create_socket()
    connect_socket()
    message = input("Message: ")
    packet = "send " + message
    server_socket.send(packet.encode("utf-8"))

    close_socket()


def cmd_retr():
    global server_socket

    create_socket()
    connect_socket()

    # Ask user for file name
    file_name = input("turtle" + currentDir + "> File Name: ")

    # Send file name to server
    packet = "retr " + file_name
    server_socket.send(packet.encode("utf-8"))
    print("File name sent.")
    print("Waiting for file...")

    try:
        # Open a new file
        file = open(file_name, "wb")

        # Receive file from server
        print("Receiving file...")
        recv_file = server_socket.recv(1024)
        while recv_file:
            file.write(recv_file)
            recv_file = server_socket.recv(1024)

        print("File received.")

        # Close new file
        file.close()

    except FileExistsError as e:
        print(str(e))

    # Close connection
    close_socket()

    print("Connection closed.")


def cmd_stor():
    global server_socket

    create_socket()
    connect_socket()

    # Receive file name
    file_name = input("turtle" + currentDir + "> File Name: ")

    # Send file name and command
    packet = "stor " + file_name
    server_socket.send(packet.encode("utf-8"))
    print("Storing " + file_name + "...")

    try:
        # Open and read file
        file = open(file_name, "rb")

        # Send file to client
        server_socket.send(file.read())

        # Flush out the transport layer buffer
        server_socket.shutdown(socket.SHUT_WR)

        # Close file
        file.close()

    except FileNotFoundError as e:
        print(str(e))

    # Close connection
    close_socket()

    print("Connection closed.")


def cmd_list():
    global server_socket

    create_socket()
    connect_socket()
    packet = "list"
    server_socket.send(packet.encode("utf-8"))

    try:
        # Receive file from server
        print("Receiving file list...")
        recv_list = server_socket.recv(1024)
        while recv_list:
            list = recv_list
            recv_list = server_socket.recv(1024)

        # Print the list of files
        print("Current files on the server:")
        print(list.decode("utf-8"))

    except FileExistsError as e:
        print(str(e))

    close_socket()

    print("Connection closed.")


def cmd_remv():
    global server_socket

    create_socket()
    connect_socket()

    # Receive file name
    file_name = input("turtle" + currentDir + "> File Name: ")

    # Send file name and command
    packet = "remv " + file_name
    server_socket.send(packet.encode("utf-8"))
    print("Removing " + file_name + "...")

    close_socket()

    print("Connection closed.")


def cmd_mdir():
    global server_socket

    create_socket()
    connect_socket()

    # Receive directory name
    dir_name = input("turtle" + currentDir + "> Directory name: ")

    # Send directory name and command
    packet = "mdir " + dir_name
    server_socket.send(packet.encode("utf-8"))
    print("Creating directory " + dir_name + "...")

    close_socket()

    print("Connection closed.")


def cmd_cd():
    global server_socket, currentDir

    create_socket()
    connect_socket()

    dir_name = input("turtle" + currentDir + "> Directory name: ")

    # Send file name and command
    packet = "cd " + dir_name
    server_socket.send(packet.encode("utf-8"))
    print("Navigating to " + dir_name + "...")

    try:
        # Receive file from server
        print("Receiving directory...")
        new_dir = server_socket.recv(1024)
        while new_dir:
            currentDir = str(new_dir.decode("utf-8"))
            new_dir = server_socket.recv(1024)

        # Print the list of files
        print("Current directory:")
        print(currentDir)

    except FileExistsError:
        print("Directory {} does not exist".format(dir_name))


# Main
if __name__ == "__main__":
    tcp_client()
