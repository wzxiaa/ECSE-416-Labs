import socket

serverPort = 12345
serverName = 'localhost'

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print('The client socket is listening on port: ', clientSocket.getsockname())

sentence = "HELLO WORLD"
# Send data to the socket, returns the number of bytes sent. Message integrity has to
# be checked by the application itself
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode())
clientSocket.close()

