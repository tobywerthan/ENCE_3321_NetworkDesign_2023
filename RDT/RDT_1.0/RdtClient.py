# Imports
import socket

# Global Variables
port = None
host = None
socket_conn = None


# Create Socket
def socket_create():
    global host, port, socket_conn
    host = "localhost"
    port = 8888

    try:
        # Create UDP socket
        socket_conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# State 0
def state0():
    global host, port, socket_conn

    # Write message
    message = str(input("Enter you message: "))

    # Escape loop
    if message == "quit":
        return None
    else:
        try:
            # Send message
            socket_conn.sendto(message.encode("utf-8"), (host, port))
        except socket.error as msg:
            print("Error sending message: " + str(msg))

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
