import socket
from random import random
from time import sleep
import struct

# Global Variables
host = None
port = None


# UDP Checksum Function
def checksum_func(data):
    checksum = 0
    data_len = len(data)

    # Appends 0's to the end of data and adjusts data_len
    if data_len % 2:
        data_len += 1
        data += struct.pack("!B", 0)

    # Compute the sum
    for i in range(0, data_len, 2):
        w = (data[i] << 8) + (data[i + 1])
        checksum += w

    # Wrap around bit
    checksum = (checksum >> 16) + (checksum & 0xFFFF)

    # Complement the result
    checksum = ~checksum & 0xFFFF
    return checksum


# Create Socket
def socket_create():
    global host
    global port
    global s
    host = ""
    port = 1001

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind to Socket
def socket_bind():
    global host
    global port
    global s

    try:
        s.bind((host, port))
        print("The server is ready to receive")
    except socket.error as msg:
        print("Socket biding error: " + str(msg))


# State 0
def state0():
    global s

    try:
        data, addr = s.recvfrom(2048)
        print("IP: " + addr[0] + " | Port: " + str(addr[1]))
        print("Message: " + str(data.decode("utf-8")))

        # Split data to get message and checksum
        str_data = str(data.decode("utf-8"))
        message, rcv_checksum = str_data.split("|")

        # Compute checksum
        # Random is used to simulating data being corrupted...
        if random() > 0.5:
            checksum = checksum_func(bytes(message.encode("utf-8")))
        else:
            checksum = 0

        if str(checksum) == rcv_checksum:
            print("Send ACK")
            s.sendto("ACK".encode("utf-8"), addr)

            # Send message to the application layer
            print("Message sent to the application layer.")

        else:
            print("Send NACK")
            s.sendto("NACK".encode("utf-8"), addr)

    except socket.error as msg:
        print(str(msg))

    return state0


# Main Function
if __name__ == "__main__":
    global s

    # created socket
    socket_create()
    # bind socket
    socket_bind()

    # Initial State
    state = state0
    while state:
        state = state()

    s.close()
    print("FSM Done")
