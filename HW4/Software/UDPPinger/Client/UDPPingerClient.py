import sys, time
from time import sleep
import socket


# Socket create
def socket_create():
    # Global variables
    global host
    global port
    global s
    global addr

    # Assign host and port and define timeout
    host = "localhost"
    port = 1001
    timeout = 1

    # Try except for socket creation
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(timeout)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Ping client
def ping_client():
    # Global variables
    global s, host, port, RTT, ptime, addr, time, packet_lost

    # Sequence number of the ping message
    ptime = 0
    RTT = 0
    packet_lost = 0
    client_input = ""
    input_count = 0

    # Get the input message from the client
    while not (client_input == "RND" or client_input == "NO RND"):
        if input_count > 0:
            print("ping> Unrecognized Command: {}".format(client_input))
            print("      Valid Commands: RND, NO RND")
        client_input = input("ping> ").strip()
        input_count += 1
    print("")
    print("Pinging server in mode: {}".format(client_input))
    print("")

    # Ping for 10 times
    while ptime < 10:
        ptime += 1
        # Format the message to be sent
        message = client_input

        try:
            # Sent time
            RTTb = time.time()

            # Send the UDP packet with the ping message
            try:
                s.sendto(message.encode("utf-8"), (host, port))
            except socket.error as msg:
                print(str(msg))

            # Receive the server response
            data, addr = s.recvfrom(2048)

            # Received time
            RTTa = time.time()

            # Compute RTT
            RTT_packet = RTTa - RTTb
            RTT = (RTT_packet) + RTT

            # Display packet time
            dataCount = len(data)
            print(
                "{} bytes from {}: seq={} time={} ms".format(
                    dataCount, addr[0], ptime, RTT_packet * 1000
                )
            )

            # Delay for readability
            sleep(1)

        except:
            # Server does not response
            # Assume the packet is lost
            print("Request timed out.")
            packet_lost += 1
            continue

    # Close socket
    s.close()


# Run ping statistics
def ping_statistics(ptime, time):
    # Global variables
    global s, host, port, RTT, addr

    print("")
    print("--- IP ping statistics ---")

    # Print statistics
    packet_loss = ((packet_lost) / 10) * 100
    packet_recieved = 10 - packet_lost
    print(
        "{} packets transmitted, {} recieved, {}% packet loss, time {} ms".format(
            ptime, packet_recieved, packet_loss, RTT * 1000
        )
    )


# **************************************
if __name__ == "__main__":
    socket_create()
    ping_client()
    ping_statistics(ptime, time)
