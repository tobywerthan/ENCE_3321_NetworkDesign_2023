import socket

serverName = "10.7.4.156"
serverPort = 1001

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clientSocket.connect((serverName, serverPort))

sentence = input("Message: ")

clientSocket.sendto(sentence.encode(), (serverName, serverPort))

modifiedSentence = clientSocket.recv(1024)

print("From Server: ", modifiedSentence)

clientSocket.close()
