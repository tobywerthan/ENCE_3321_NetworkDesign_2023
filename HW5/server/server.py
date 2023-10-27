# Import necessary libraries
from datetime import datetime, timezone
import os
import socket
import threading

# Define global variables
host = None
port = None
server_socket = None
usernames = ["tobywerthan", "goncalomartins", "johnleseur", "davidki", "joshmejia"]
passwords = ["8818", "password", "password", "password", "password"]
currentDir = ""
active_users = dict()


# Create Socket
def create_socket():
    global host, port, server_socket

    # Define socket host and port
    host = ""
    port = 8888

    try:
        # Create socket and set options
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print(str(msg))


# Bind Socket
def bind_socket():
    global host, port, server_socket

    try:
        # Bind the socket
        server_socket.bind((host, port))
    except socket.error as msg:
        print("Socket bind error: ")
        print(str(msg))


# Close socket
def close_socket():
    try:
        # Close the socket
        server_socket.close()
    except socket.error as msg:
        print("Socket closing error: ")
        print(str(msg))


# Main server loop
def tcp_server():
    global server_socket, port

    # Create and bind the socket
    create_socket()
    bind_socket()

    # Listen for incomming connections
    server_socket.listen(1)

    # Ifinite loop
    while True:
        print("***************************************")
        print("Waiting for client, listening on port " + str(port))

        try:
            # Create new socket connection for client specific operations
            connection_socket, addr = server_socket.accept()

            # Open a new thread for the client
            x = threading.Thread(
                target=client_thread,
                args=(
                    connection_socket,
                    addr,
                ),
            )
            x.setDaemon(True)
            x.start()
        except socket.error as e:
            print(str(e))
        except threading.ThreadError as e:
            print(str(e))

    # Close the socket
    close_socket()


# Client thread
def client_thread(connection_socket, addr):
    # Print connection socket information
    print("Connected to client --> IP: " + str(addr[0]) + " | Port: " + str(addr[1]))

    try:
        # Recieve packet data
        raw_packet = connection_socket.recv(1024)

        # decode and split packet using delimeter of " "
        packet = raw_packet.decode("utf-8").split(" ")

        # Check which command the client sent
        if packet[0] == "send":
            cmd_send(packet, connection_socket, addr)
        elif packet[0] == "retr":
            cmd_retr(packet, connection_socket, addr)
        elif packet[0] == "list":
            cmd_list(connection_socket, addr)
        elif packet[0] == "stor":
            cmd_stor(packet, connection_socket, addr)
        elif packet[0] == "remv":
            cmd_remv(packet, connection_socket, addr)
        elif packet[0] == "login":
            cmd_login(packet, connection_socket, addr)
        elif packet[0] == "cd":
            cmd_cd(packet, connection_socket, addr)
        elif packet[0] == "mdir":
            cmd_mdir(packet, connection_socket, addr)
        elif packet[0] == "rdir":
            cmd_rdir(packet, connection_socket, addr)
        elif packet[0] == "logout":
            cmd_logout(packet, connection_socket, addr)
        else:
            print("Command Unrecognized")

        # Close the connection socket
        connection_socket.close()
    except socket.error as msg:
        print(str(msg))


# Login Command
def cmd_login(packet, connection_socket, clientInfo):
    global usernames, passwords, active_users

    # Set the temporary authorization flag to zero
    auth = 0

    # Check all users and passwords to see if the client's input matches
    for i in range(len(usernames)):
        if packet[1] == usernames[i] and packet[2] == passwords[i]:
            # Set the temporary auth flag to 1
            auth = 1
            active_users.update({str(clientInfo[0]): usernames[i]})
    try:
        # Send the temporary auth flag value
        connection_socket.send(str(auth).encode("utf-8"))

        # Print the action preformed
        print_client_action(packet, clientInfo)

    except socket.error as e:
        print(str(e))


# Logout command
def cmd_logout(packet, connection_socket, clientInfo):
    global active_users

    # Print the action
    print_client_action(packet, clientInfo)

    # Set temporary auth flag to 1
    auth = 1

    # Set current user
    active_users.pop(str(clientInfo[0]))

    # Set the temporary auth flag to zero
    auth = 0

    try:
        # Send the auth flag to the client
        connection_socket.send(str(auth).encode("utf-8"))

    except socket.error as msg:
        print(str(msg))


# Retrieve Command
def cmd_retr(packet, connection_socket, clientInfo):
    # Set the file name
    file_name = packet[1]

    try:
        # Open and read file
        file = open(file_name, "rb")

        # Send file to client
        connection_socket.send(file.read())

        # Flush out the transport layer buffer
        connection_socket.shutdown(socket.SHUT_WR)

        # Close file
        file.close()

        # Print the action preformed
        print_client_action(packet, clientInfo)

    except socket.error as e:
        print(str(e))


# Store Command
def cmd_stor(packet, connection_socket, clientInfo):
    # Set the file name
    file_name = packet[1]

    try:
        # Open a new file
        file = open(file_name, "wb")

        # Receive file from server
        recv_file = connection_socket.recv(1024)
        while recv_file:
            file.write(recv_file)
            recv_file = connection_socket.recv(1024)

        # Close new file
        file.close()

        # Print the action preformed
        print_client_action(packet, clientInfo)

    except socket.error as e:
        print(str(e))

    # Command status (WORK IN PROGRESS)
    if file_name in os.listdir():
        connection_socket.send("STORE 1".encode("utf-8"))
    else:
        connection_socket.send("STORE 0".encode("utf-8"))


# List Command
def cmd_list(connection_socket, clientInfo):
    # Get the list of files
    file_list = os.listdir()

    # Send the file list to the client
    connection_socket.send(str(file_list).encode("utf-8"))

    # Flush out the transport layer buffer
    connection_socket.shutdown(socket.SHUT_WR)

    # Print the action preformed
    print_client_action(["list"], clientInfo)


# Send Command
def cmd_send(packet, connection_socket, clientInfo):
    # Print the action preformed
    print("Message recieved: " + packet[1])

    # Command status (WORK IN PROGRESS)
    if len(packet[1]) > -1:
        connection_socket.send("SEND 1".encode("utf-8"))
    else:
        connection_socket.send("SEND 0".encode("utf-8"))

    print_client_action(packet, clientInfo)


# Remove Command
def cmd_remv(packet, connection_socket, clientInfo):
    # Set the file name
    file_name = packet[1]

    try:
        # Removing file from the server
        os.remove(file_name)

        # Print the action preformed
        print_client_action(packet, clientInfo)

    except os.error as e:
        print(str(e))

        try:
            # Send error to the client
            connection_socket.send(str(e).encode("utf-8"))
        except socket.error as msg:
            print(str(msg))


# Directory Navigation Command
def cmd_cd(packet, connection_socket, clientInfo):
    global currentDir

    # Variables for os error detection
    os_error = 0
    error_message = ""

    # Set the path
    dir_name = packet[1]

    try:
        # Navigate to the path
        os.chdir(dir_name)
    except os.error as msg:
        # Set error flag to 1
        os_error = 1
        # Record and print error message
        error_message = str(msg)
        print(str(msg))

    if os_error == 0:
        try:
            # Parse for navigating upwards
            if dir_name != "../":
                currentDir = currentDir + "/" + dir_name
            else:
                # Removes last element in path
                dirElements = currentDir.split("/")
                length = len(dirElements)
                currentDir = currentDir.replace(dirElements[length - 1], "")
                currentDir = currentDir[: len(currentDir) - 1]

            # Send the new path to the client
            connection_socket.send((str(os_error) + str(currentDir)).encode("utf-8"))

            # Print the action preformed
            print_client_action(packet, clientInfo)
        except socket.error as msg:
            print(str(msg))
    else:
        try:
            # Send the new path to the client
            connection_socket.send((str(os_error) + str(error_message)).encode("utf-8"))
        except socket.error as msg:
            print(str(msg))


# Make Directory Command
def cmd_mdir(packet, connection_socket, clientInfo):
    dir_name = packet[1]

    try:
        # Create directory
        os.mkdir(packet[1])

        # Print the action preformed
        print_client_action(packet, clientInfo)

    except os.error as msg:
        print(str(msg))

        try:
            # Send error to the client
            connection_socket.send(str(msg).encode("utf-8"))
        except socket.error as msg:
            print(str(msg))


# Remove Directory Command
def cmd_rdir(packet, connection_socket, clientInfo):
    dir_name = packet[1]

    try:
        # Create directory
        os.rmdir(packet[1])

        # Print the action preformed
        print_client_action(packet, clientInfo)

    except os.error as msg:
        print(str(msg))

        try:
            # Send error to the client
            connection_socket.send(str(msg).encode("utf-8"))
        except socket.error as msg:
            print(str(msg))


# Print client actions
def print_client_action(packet, clientInfo):
    # Print the action information
    print(
        "Client "
        + str(clientInfo[0])
        + " attempted a "
        + packet[0]
        + " on port "
        + str(clientInfo[1])
    )

    # Add action to server log file
    log_user_action(packet, clientInfo)


# Log user actions
def log_user_action(packet, clientInfo):
    global active_users

    try:
        # Open the log file
        file = open(
            "C:/Users/tobyw/OneDrive/Desktop/workspace/ENCE_3321_NetworkDesign_2023/HW5_v2/server/log.txt",
            "a",
        )

        # Print new line
        file.write("\n")

        # Write header for log entry
        file.write(
            str(datetime.now(timezone.utc))
            + ": User "
            + active_users.get(str(clientInfo[0]), "anonymous")
            + " attempted "
        )

        # Write log entry based on command
        if packet[0] == "send":
            file.write(
                "a send command with message: '"
                + packet[1]
                + "' from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "retr":
            file.write(
                "a retrieve command for the file: '"
                + packet[1]
                + "' from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "list":
            file.write(
                "a list command from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "stor":
            file.write(
                "a store command with file: '"
                + packet[1]
                + "' from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "remv":
            file.write(
                "a remove command for the file: '"
                + packet[1]
                + "' from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "login":
            file.write(
                "a login command from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "cd":
            file.write(
                "a cd command with path: '"
                + packet[1]
                + "' from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "mdir":
            file.write(
                "a make directory command with folder: '"
                + packet[1]
                + "' from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "rdir":
            file.write(
                "a remove directory command for the folder: '"
                + packet[1]
                + "' from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        elif packet[0] == "logout":
            file.write(
                "a logout command from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )
        else:
            file.write(
                "an unrecognized command from IP: "
                + str(clientInfo[0])
                + " and Port: "
                + str(clientInfo[1])
            )

        # Close the file
        file.close()
    except FileNotFoundError:
        print("Unable to locate log.txt within the current directory")


# Main
if __name__ == "__main__":
    # Runs the TCP server
    tcp_server()
