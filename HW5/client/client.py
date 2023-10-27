import socket

host = None
port = None
server_socket = None
auth_flag = 0
currentDir = ""


# Create Socket
def create_socket():
    global host, port, server_socket

    # Define socket host and port
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
        # Close the socket
        server_socket.close()
    except socket.error as msg:
        print("Socket closing error: ")
        print(str(msg))


# Main client loop
def tcp_client():
    # Infinite Loop
    while True:
        # Recieve the command from the client, split the result using a delimeter of " "
        cmd = input("turtle" + currentDir + "> ").split(" ")
        # Available commands based on authentication level
        if auth_flag:
            if cmd[0] == "quit":
                break
            elif cmd[0] == "send":
                cmd_send(cmd)
            elif cmd[0] == "help":
                cmd_help()
            elif cmd[0] == "logout":
                cmd_logout()
            elif cmd[0] == "retr":
                cmd_retr(cmd)
            elif cmd[0] == "list":
                cmd_list()
            elif cmd[0] == "stor":
                cmd_stor(cmd)
            elif cmd[0] == "remv":
                cmd_remv(cmd)
            elif cmd[0] == "cd":
                cmd_cd(cmd)
            elif cmd[0] == "mdir":
                cmd_mdir(cmd)
            elif cmd[0] == "rdir":
                cmd_rdir(cmd)
            else:
                print("")
                print("Unrecognized command: " + cmd[0])
                print(
                    "List of valid turtle commands: quit, send, help, logout, retr, list, stor, remv, cd, mdir, rdir"
                )
                print("")
        else:
            if cmd[0] == "quit":
                break
            elif cmd[0] == "send":
                cmd_send(cmd)
            elif cmd[0] == "help":
                cmd_help()
            elif cmd[0] == "login":
                cmd_login(cmd)
            elif (
                cmd[0] == "retr"
                or cmd[0] == "list"
                or cmd[0] == "stor"
                or cmd[0] == "remv"
                or cmd[0] == "cd"
                or cmd[0] == "mdir"
                or cmd[0] == "rdir"
            ):
                print("")
                print("Please login to access: " + cmd[0])
                print("")
            else:
                print("")
                print("Unrecognized command: " + cmd[0])
                print("List of valid turtle commands: quit, send, help, login")
                print("")


# Help Command
def cmd_help():
    print("")
    # Commands printed based on authentication level
    if auth_flag:
        print("-----------------------------------------------------------")
        print("List of valid turtle commands: ")
        print("     quit: exit the program")
        print("     help: lists valid turtle commands")
        print("     send: tests server connection")
        print("     logout: logout of the server")
        print("     retr: gets a file from current directory")
        print("     list: lists all files in the current directory")
        print("     stor: stores a file in the current directory")
        print("     remv: removes a file in the current directory")
        print("     cd: navigates to the specified path")
        print("     mdir: creates a new folder in the current directory")
        print("     rdir: removes a folder in the current directory")
    else:
        print("-----------------------------------------------------------")
        print("List of valid turtle commands: ")
        print("     quit: exit the program")
        print("     help: lists valid turtle commands")
        print("     send: tests server connection")
        print("     login: login")
    print("")


# Login Command
def cmd_login(cmd):
    global auth_flag, server_socket

    # Syntax check
    if len(cmd) != 3:
        print("Syntax Error:")
        print("     Expected format: login username password")
    else:
        # Create socket and socket connection to server
        create_socket()
        connect_socket()

        # Construct the packet
        packet = "login " + cmd[1] + " " + cmd[2]

        try:
            # Send the ecnoded packet to the server
            server_socket.send(packet.encode("utf-8"))

            # Revieve the auth value provided by the server
            recv_auth = server_socket.recv(1024)

            # Set the auth value based on the server's response
            auth_flag = int(recv_auth.decode("utf-8"))

            # Print login success
            if auth_flag:
                print("Login successful")
            else:
                print("Invalid credentials")

        except socket.error as e:
            print(str(e))

        # Close the socket
        close_socket()


# Logout Command
def cmd_logout():
    global server_socket, auth_flag

    # Create socket and socket connection to server
    create_socket()
    connect_socket()

    try:
        # Send the command
        server_socket.send("logout ".encode("utf-8"))
    except socket.error as msg:
        print(str(msg))

    try:
        # Recieve the auhtorization flag
        recv_auth = server_socket.recv(1024)

        # Set the auth value based on the server's response
        auth_flag = int(recv_auth.decode("utf-8"))
    except socket.error as msg:
        print(str(msg))

    # Log out if error or if successfuk
    if auth_flag == 0 or auth_flag == -1:
        auth_flag = 0
        print("Log out successful")
    else:
        print("Unable to log out")

    # Close the socket
    close_socket()


# Send Command
def cmd_send(cmd):
    global server_socket

    # Syntax check
    if len(cmd) != 2:
        print("Syntax Error:")
        print("     Expected format: send message")
    else:
        # Create socket and socket connection to server
        create_socket()
        connect_socket()

        # Construct packet
        packet = "send " + cmd[1]

        try:
            # Send the command and message
            server_socket.send(packet.encode("utf-8"))

        except socket.error as msg:
            print(str(msg))

        try:
            # Recieve the server response
            response = server_socket.recv(1024).decode("utf-8").split(" ")
            # Print the response
            get_cmd_status(response, cmd)

        except socket.error as msg:
            print(str(msg))

        # Close the socket
        close_socket()


# Retrieve Command
def cmd_retr(cmd):
    global server_socket

    # Syntax check
    if len(cmd) != 2:
        print("Syntax Error:")
        print("     Expected format: retr filename")
    else:
        # Create socket and socket connection to server
        create_socket()
        connect_socket()

        # Construct the packet
        packet = "retr " + cmd[1]

        # Send the encoded packet to the server
        server_socket.send(packet.encode("utf-8"))

        try:
            # Open a new file
            file = open(cmd[1], "wb")

            # Receive file from server
            recv_file = server_socket.recv(1024)
            while recv_file:
                file.write(recv_file)
                recv_file = server_socket.recv(1024)

            # Close new file
            file.close()
        except socket.error as msg:
            print(str(msg))

        # Close connection
        close_socket()


# Store Command
def cmd_stor(cmd):
    global server_socket

    # Syntax check
    if len(cmd) != 2:
        print("Syntax Error:")
        print("     Expected format: sotr filename")
    else:
        # Create socket and socket connection to server
        create_socket()
        connect_socket()

        # Construct packet
        packet = "stor " + cmd[1]

        try:
            # Send the encoded packet to the server
            server_socket.send(packet.encode("utf-8"))
        except socket.error as msg:
            print(str(msg))

        error = False

        try:
            try:
                # Open and read file
                file = open(cmd[1], "rb")
            except OSError as msg:
                print(
                    "The file "
                    + cmd[1]
                    + " does not exist. Please check the spelling and make sure the file is within your current directory."
                )
                error = True

            if not error:
                # Send file to the server
                server_socket.send(file.read())

                # Flush out the transport layer buffer
                server_socket.shutdown(socket.SHUT_WR)

                # Close file
                file.close()

        except socket.error as msg:
            print(str(msg))

        if not error:
            try:
                # Recieve the server response
                response = server_socket.recv(1024).decode("utf-8").split(" ")

                # Print the response
                get_cmd_status(response, cmd)

            except socket.error as msg:
                print(str(msg))

        # Close connection
        close_socket()


# List Command
def cmd_list():
    global server_socket

    # Create socket and socket connection to server
    create_socket()
    connect_socket()

    # Construct the packet
    packet = "list"

    # Send the encoded packet to the server
    server_socket.send(packet.encode("utf-8"))

    try:
        # Receive the list of files from server
        recv_list = server_socket.recv(1024)
        while recv_list:
            list = recv_list
            recv_list = server_socket.recv(1024)

        # Print the list of files
        print("Current files on the server:")
        print(list.decode("utf-8"))

    except socket.error as msg:
        print(str(msg))

    # Close connection
    close_socket()


# Remove Command
def cmd_remv(cmd):
    global server_socket

    # Syntax check
    if len(cmd) != 2:
        print("Syntax Error:")
        print("     Expected format: remv filename")
    else:
        # Create socket and socket connection to server
        create_socket()
        connect_socket()

        # Construct the packet
        packet = "remv " + cmd[1]

        try:
            # Send the encoded packet to the server
            server_socket.send(packet.encode("utf-8"))
        except socket.error as msg:
            print(str(msg))

        try:
            # Recieve os error
            os_error = server_socket.recv(1024).decode("utf-8")
            if os_error:
                print(os_error)

        except socket.error as msg:
            print(str(msg))

        # Close connection
        close_socket()


# Directory Navigation Command
def cmd_cd(cmd):
    global server_socket, currentDir
    tempDir = ""

    # Syntax check
    if len(cmd) != 2:
        print("Syntax Error:")
        print("     Expected format: cd path")
    else:
        # Create socket and socket connection to server
        create_socket()
        connect_socket()

        # Construct packet
        packet = "cd " + cmd[1]

        try:
            # Send the encoded packet
            server_socket.send(packet.encode("utf-8"))
        except socket.error as msg:
            print(str(msg))

        try:
            # Receive new directory from the server
            tempDir = str(server_socket.recv(1024).decode("utf-8"))
        except FileExistsError:
            print("Directory {} does not exist".format(cmd[1]))

        # Check for error
        if tempDir[0] == "1":
            print(tempDir.replace(tempDir[0], ""))
        else:
            currentDir = tempDir.replace(tempDir[0], "")

        # Close connection
        close_socket()


# Make Directory Command
def cmd_mdir(cmd):
    global server_socket

    # Syntax check
    if len(cmd) != 2:
        print("Syntax Error:")
        print("     Expected format: mdir name")
    else:
        # Create socket and socket connection to server
        create_socket()
        connect_socket()

        # Construct packet
        packet = "mdir " + cmd[1]

        try:
            # Send the packet to the server
            server_socket.send(packet.encode("utf-8"))

        except socket.error as msg:
            print(str(msg))

        try:
            # Recieve os error
            os_error = server_socket.recv(1024).decode("utf-8")
            if os_error:
                print(os_error)

        except socket.error as msg:
            print(str(msg))

        # Close the socket
        close_socket()


# Remove Directory Command
def cmd_rdir(cmd):
    global server_socket

    # Syntax check
    if len(cmd) != 2:
        print("Syntax Error:")
        print("     Expected format: rdir name")
    else:
        # Create socket and socket connection to server
        create_socket()
        connect_socket()

        # Construct packet
        packet = "rdir " + cmd[1]

        try:
            # Send the packet to the server
            server_socket.send(packet.encode("utf-8"))

        except socket.error as msg:
            print(str(msg))

        try:
            # Recieve os error
            os_error = server_socket.recv(1024).decode("utf-8")
            if os_error:
                print(os_error)

        except socket.error as msg:
            print(str(msg))

        # Close the socket
        close_socket()


# Get command status (WORK IN PROGRESS)
def get_cmd_status(packet, cmd):
    global server_socket

    if packet[0] == "SEND":
        if packet[1] == "1":
            print("The message, '" + cmd[1] + "' was sent successfully")
        else:
            print(
                "SERVER ERROR: The message, '" + cmd[1] + "' was not sent successfully"
            )
    elif packet[0] == "STORE":
        if packet[1] == "1":
            print("The file, '" + cmd[1] + "' was uploaded successfully")
        else:
            print(
                "SERVER ERROR: The file, '" + cmd[1] + "' was not uploaded successfully"
            )
    else:
        if packet[1] == "1":
            print("An unknown command was executed successfuly")
        else:
            print("SERVER ERROR: An unknown command was not successful")


# Main
if __name__ == "__main__":
    # Main client loop
    tcp_client()
