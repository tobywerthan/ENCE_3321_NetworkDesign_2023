import socket

# Global Variables
s = None
host = None
port = None


class mySocketError(Exception):
    pass


# Create Socket
def socket_create():
    global host
    global port
    global s
    host = ''
    port = 1001

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
        print("Socket creation error: " + str(e))
        raise mySocketError("Socket creation error...")


# Bind to Socket
def socket_bind():
    global host
    global port
    global s

    try:
        s.bind((host, port))
        print("The server is ready to receive")
    except socket.error as e:
        print("Socket biding error: " + str(e))
        raise mySocketError("Socket creation error...")


# TCP Server Protocol
def tcp_server():
    global s

    try:

        # Listen for incoming connections
        s.listen(1)

        while True:
            try:
                connectionSocket, addr = s.accept()

                data = connectionSocket.recv(2048)
                print("IP: " + addr[0] + " | Port: " + str(addr[1]))
                print("Message: " + str(data.decode('utf-8')))

                connectionSocket.sendto(data.upper(), (addr[0], addr[1]))

                connectionSocket.close()

            except socket.error as e:
                print(str(e))
                raise mySocketError("Socket protocol error...")

    except socket.error as e:
        print(str(e))
        raise mySocketError(e)


# Main Function
if __name__ == "__main__":

    try:
        # created socket
        socket_create()
        # bind socket
        socket_bind()
        # tcp server
        tcp_server()

    except mySocketError as msg:
        print(msg)
