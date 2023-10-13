import socket
from random import random


# Create Sockets
def socket_create():
    # Global variables
    global host
    global port
    global s

    # Assign host and port
    host = "localhost"
    port = 1001

    # Try except for socket creation
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind socket
def socket_bind():
    # Global variables
    global host
    global port
    global s

    # Try except for binding socket
    try:
        s.bind((host, port))
        print("The server is ready to receive")
    except socket.error as msg:
        print("Socket binding error: " + str(msg))


# Ping server
def ping_server():
    # Global variables
    global host
    global port
    global s

    # Define and set flag
    flag = 0

    # Infinite loop
    while True:
        # Recieve message and address from client
        message, clientAddress = s.recvfrom(2048)

        # Decode the message from client
        str_msg = str(message.decode("utf-8"))

        # Print the client address and decoded message
        print("Message from {0}: {1}".format(clientAddress[0], str_msg))

        # Try except for sending message to client
        try:
            # Conditional determining packet loss based on client message
            if str_msg == "NO RND":  # NO PKTs LOSS
                flag = 1
            elif str_msg == "RND":  # PKTs LOSS
                # Generate a random number
                if random() > 0.5:
                    flag = 0
                else:
                    flag = 1

            # Send acknowledgement to client based on flag value
            if flag == 1:
                message = "GOOD STRING"
                s.sendto(message.encode("utf-8"), clientAddress)

        except:
            print("Sending message error...")


# **************************************
if __name__ == "__main__":
    socket_create()
    socket_bind()
    ping_server()
