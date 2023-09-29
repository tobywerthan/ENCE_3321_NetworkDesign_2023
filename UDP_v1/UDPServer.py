import socket

serverPort = 8888

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind(("", serverPort))
print("The server is ready to recieve")

while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(clientAddress)
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage, clientAddress)
