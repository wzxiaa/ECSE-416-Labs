import socket
import sys
import pickle
import math
import matplotlib.pyplot as plt

def parser():
    argv = sys.argv[1:]
    if len(argv) != 3:
        print("Invalid number of arguments supplied!")
        sys.exit(1)
    servername = argv[0]
    serverport = int(argv[1])
    filename = argv[2]
    return servername, serverport, filename

class Client():
    def __init__(self, headerSize=64, bufferSize=4096):
        self.headerSize = headerSize
        self.bufferSize = bufferSize
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, serverName, serverPort):
        try:
            self.clientSocket.connect((serverName, serverPort))
        except socket.error as msg:
            print("Connection: FAILED")
            exit(1)
        print("Connection: OK")

    def send(self, msg):
        message = msg.encode()
        msg_length = len(message)
        send_length = str(msg_length).encode()
        send_length += b' ' * (self.headerSize - len(send_length))
        self.clientSocket.send(send_length)
        self.clientSocket.send(message)
        print("Request message sent.")

    def get_response(self):
        msg_length = self.clientSocket.recv(self.headerSize).decode()
        if msg_length:
            msg_length = int(msg_length)
            n_recvs = math.ceil(msg_length / self.bufferSize)
            full_response = []
            for i in range(n_recvs):
                msg = self.clientSocket.recv(self.bufferSize)
                full_response.append(msg)
            full_response = pickle.loads(b"".join(full_response))
            print(full_response["header"])
            if full_response["status"] == 200:
                if full_response["ext"] == "txt":
                    print(full_response["response"])
                elif full_response["ext"] == "jpg":
                    plt.imshow(full_response["response"])
                    plt.show()
            else:
                print(full_response["response"])

    def close(self):
        self.clientSocket.close()
        print("Socket closed.")

if __name__ == "__main__":

    serverName, serverPort, filename = parser()
    client = Client()
    client.connect(serverName, serverPort)
    client.send(filename)
    client.get_response()
    client.close()

