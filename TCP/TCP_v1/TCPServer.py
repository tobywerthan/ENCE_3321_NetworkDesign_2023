import socket

serverPort = 8888

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind(("", serverPort))

serverSocket.listen(1)

while True:
    connectionSocket, address = serverSocket.accept()

    message = connectionSocket.recv(1024)
    modifiedMessage = message.upper()
    connectionSocket.send(modifiedMessage)
    connectionSocket.close()
