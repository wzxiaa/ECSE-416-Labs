import socket
import sys
import base64
from PIL import Image

def parser():
    argv = sys.argv[1:]
    if len(argv) != 3:
        print("Invalid number of arguments supplied!")
        sys.exit(1)
    servername = argv[0]
    serverport = int(argv[1])
    filename = argv[2]
    return servername, serverport, filename

if __name__ == "__main__":
    # get the list of arguments except for the filename
    serverName, serverPort, filename = parser()
    # print(("{},{},{}").format(serverName, serverPort, filename))

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((serverName, serverPort))
    except socket.error as msg:
        print("Connection: FAILED")
        exit(1)

    print("Connection: OK")

    # Send data to the socket, returns the number of bytes sent. Message integrity has to
    # be checked by the application itself
    try:
        clientSocket.send(filename.encode())
    except socket.error as msg:
        print("Connection: FAILED")
        exit(1)

    print("Request message sent.")

    while True:
        buf = clientSocket.recv(409600)
        if not buf:
            break

        if filename.endswith('.txt'):
            print("from client",buf.decode())
        elif filename.endswith('.jpg'):
            result = base64.decodebytes(buf)

            Image.open(result)
            # image_result = open('decode.jpg', 'wb')
            # image_result.write(result)
            # display = open('decode.jpg',"rb")
            # display.show()
    # print('From Server: ', modifiedSentence.decode())
    clientSocket.close()