import socket

serverName = "10.7.4.156"
serverPort = 1001

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

message = input("Message: ")

clientSocket.sendto(message.encode(), (serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print(modifiedMessage)

clientSocket.close()
