import socket

# Global Variables
s = None
host = None
port = None


# Create Socket
def socket_create():
    global host
    global port
    global s
    host = "localhost"
    port = 8888

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# UDP Client Protocol
def udp_client():
    global host
    global port
    global s

    while True:
        message = input("Message: ")
        if message == "quit":
            break
        else:
            try:
                s.sendto(message.encode("utf-8"), (host, port))

                data, addr = s.recvfrom(2048)
                print("IP: " + addr[0] + " | Port: " + str(addr[1]))
                print("Message: " + str(data.decode("utf-8")))

            except socket.error as msg:
                print(str(msg))

    s.close()


# Main Function
if __name__ == "__main__":
    # created socket
    socket_create()
    # udp client
    udp_client()
