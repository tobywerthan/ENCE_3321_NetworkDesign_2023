import socket
import struct

# Global Variables
host = None
port = None
data = None


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
    host = "localhost"
    port = 1001

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# State0
def state0():
    global host
    global port
    global s
    global data

    message = input("Message: ")
    if message == "quit":
        return None
    else:
        try:
            # Compute checksum
            checksum = checksum_func(bytes(message.encode("utf-8")))

            # Append checksum to data
            data = str(message) + "|" + str(checksum)
            s.sendto(data.encode("utf-8"), (host, port))

        except socket.error as msg:
            print("Error sending message: " + str(msg))

    return state1


# State 1
def state1():
    global host
    global port
    global s
    global data

    try:
        print("Waiting for ACK or NACK...")

        response, addr = s.recvfrom(1024)

        answer = str(response.decode("utf-8"))
        if answer == "NACK":
            # Resend message
            s.sendto(data.encode("utf-8"), (host, port))
            print("Sending message again...")
            return state1

        elif answer == "ACK":
            print("Message received.")
            return state0

    except socket.error as msg:
        print("Error sending message: " + str(msg))


# Main Function
if __name__ == "__main__":
    global s

    # created socket
    socket_create()

    # Initial State
    state = state0
    while state:
        state = state()

    s.close()
    print("FSM Done")
