import http.server
import socketserver

handler = http.server.SimpleHTTPRequestHandler

socket_server = socketserver.TCPServer(("", 80), handler)
print("Now serving on localhost:80")

socket_server.serve_forever()
