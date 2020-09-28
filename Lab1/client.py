import socket
import sys
import pickle
import math
import matplotlib.pyplot as plt
import time

def parser():
    argv = sys.argv[1:]
    if len(argv) != 3:
        print("Invalid number of arguments supplied!")
        sys.exit(1)
    servername = argv[0]
    serverport = int(argv[1])
    filename = argv[2]
    if(len(argv)==4):
        timeout = int(argv[3])
    else: timeout = 5
    return servername, serverport, filename, timeout

class Client():
    def __init__(self, headerSize=64, bufferSize=4096):
        self.headerSize = headerSize
        self.bufferSize = bufferSize
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, serverName, serverPort, timeout=5):
        try:
            self.clientSocket.settimeout(timeout)
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
        time_start = time.time()
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
            time_end = time.time()
            if full_response["status"] == 200:
                if full_response["ext"] == "txt":
                    print(full_response["response"])
                    print("Time taken: ", time_end - time_start)
                elif full_response["ext"] == "jpg":
                    print("Time taken: ", time_end - time_start)
                    plt.imshow(full_response["response"])
                    plt.show()

            else:
                print(full_response["response"])
                print("Time taken: ", time_end - time_start)

    def close(self):
        self.clientSocket.close()
        print("Socket closed.")

if __name__ == "__main__":

    serverName, serverPort, filename, timeout = parser()
    client = Client()
    try:
        client.connect(serverName, serverPort, timeout)
        client.send(filename)
        client.get_response()
    except socket.error as err:
        print("Socket Timeout")
    client.close()

