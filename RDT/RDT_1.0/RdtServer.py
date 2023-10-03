# Imports
import socket

# Global Variables
port = None
host = None
socket_conn = None


# Create Socket
def socket_create():
    global host, port, socket_conn
    host = ""
    port = 8888

    try:
        # Create UDP socket
        socket_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to UDP socket
        bind_socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind Socket
def bind_socket():
    global host, port, socket_conn
    host = ""
    port = 8888

    try:
        # Bind to UDP socket
        socket_conn.bind((host, port))

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# State 0
def state0():
    global host, port, socket_conn

    try:
        # Recieve Data
        data, addr = socket_conn.recvfrom(1024)

        # Print Data
        print("IP: " + str(addr[0]))
        print("Port: " + str(addr[1]))
        print("Data: " + str(data.decode("utf-8")))

    except socket.error as msg:
        print("Error recieving data: " + str(msg))

    return state0


# Main
if __name__ == "__main__":
    # Create socket
    socket_create()

    # Initial state
    state = state0

    while state:
        # Loop FSM
        state = state()

    # Close socket
    socket_conn.close()
