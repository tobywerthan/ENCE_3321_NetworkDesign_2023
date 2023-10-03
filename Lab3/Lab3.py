import socket
import struct
import time


# Print Machine Information
# ----------------------------------------
def print_machine_info():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    print("Host Name: {}".format(host_name))
    print("IP Address: {}".format(ip_address))


# Get Remote Machine Information
# ----------------------------------------
def get_remote_machine_info():
    remote_host = "www.engredu.com"

    try:
        print(
            "IP Adress of {0}: {1}".format(
                remote_host, socket.gethostbyname(remote_host)
            )
        )
    except socket.error as err:
        print("%s: %s" % (remote_host, err))


# Test Socket Timeout
# ----------------------------------------
def test_socket_timeout():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Default socket timeout: {}".format(s.gettimeout()))

    s.settimeout(100)
    print("Modified socket tieout: {}".format(s.gettimeout()))


# Test Socket Modes: Blocking/Non Blocking
# ----------------------------------------
def test_socket_modes():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.setblocking(0)
    s.settimeout(0.5)
    s.bind(("127.0.0.1", 0))

    socket_address = s.getsockname()

    print("Trivial Server launched on socket: %s" % str(socket_address))

    while 1:
        s.listen(1)


# Simple Network Time Protocol
# ----------------------------------------
def sntp_client():
    NTP_SERVER = "0.uk.pool.ntp.org"
    TIME1970 = 2208988800

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    data = "\x1b" + 47 * "\0"
    client.sendto(data.encode("utf-8"), (NTP_SERVER, 123))
    data, address = client.recvfrom(1024)

    if data:
        print("Response received from: ", address)
        t = struct.unpack("!12I", data)[10]
        t -= TIME1970
        print("\t Time = %s" % time.ctime(t))


# Main Function
# ----------------------------------------
if __name__ == "__main__":
    sntp_client()
