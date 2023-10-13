import os


def get_tcp_congestion():
    result = None
    result = os.popen("netsh interface tcp show supplemental").read()
    for line in result.splitlines():
        if "Congestion Control Provider" in line:
            result = line.split(":")[1].strip()
    return result


if __name__ == "__main__":
    answer = get_tcp_congestion()
    if answer:
        print("TCP Algorithim: {}".format(answer))
    else:
        print("TCP Algorithim not found")
