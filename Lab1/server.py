import socket
import sys
serverPort = 12345
serverName = 'localhost'

# a pair (host, port) is used for the AF_INET (IPv4) address family
# SOCK_STREAM: socket type
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverName, serverPort))

# socket.listen method enables a server to accept connections.
# It specifies the number of unaccepted connections that the system will allow
# before refusing new connections
serverSocket.listen(1)
print('The server is ready to receive')
print('The server socket is listening on port: ', serverSocket.getsockname())

while True:
    # socket.accept(): accept a connection; conn is a new socket object usable to send and receive data
    # addr is the address bounded to the socket on the other end of the connection
    connectionSocket, addr = serverSocket.accept()
    print('Connected by: ', addr)
    # Receive data from socket. Returns a bytes object representing the data. Need to specifies buffer size in bytes.
    request = ''
    counter = 0
    while True:
        buffer = connectionSocket.recv(3)
        print(buffer)
        if not buffer:
            print("ssssssssssss")
            break
        request += buffer.decode()
        # print(buffer.decode())
        print(counter)
        counter = counter + 1
    print(request)
    f = open(request, "r")
    response = f.read()
    connectionSocket.send(response.encode())
    connectionSocket.close()